from ant_colony.core import AntColony
from numpy import array, ndarray
from harmony_search.object_define import ObjectiveFunction
from harmony_search.core import HarmonySearch
from typing import List, Dict
from datetime import datetime
from copy import deepcopy
import torch
from random import random, randint
from t_normal import is_truncated_normal

START_NODE: str = 'start'
FINISH_NODE: str = 'finish'


def build_transition_prob_matrix(path_solution_candidate: List[Dict]) -> torch.Tensor:
    matrix = torch.zeros(num_kpi + 2, num_kpi + 2)
    # print(matrix)
    for item in path_solution_candidate:
        from_index: int = 0 \
            if item['from'] == START_NODE else num_kpi + 1 if item['from'] == FINISH_NODE else int(item['from'])

        to_index: int = 0 if item['to'] == START_NODE else num_kpi + 1 if item['to'] == FINISH_NODE else int(item['to'])
        # print(item['transition_prob_for_harmony_candidate'])
        matrix[from_index, to_index] = max(item['transition_prob_for_harmony_candidate'])

    return matrix


def update_transition_prob_for_harmony_candidate(path_solution_candidate: List[Dict]) -> None:
    for path_candidate in path_solution_candidate:
        total: float = 0
        for index in range(len(path_candidate['harmony_memory'])):
            total += (pow(1 / path_candidate['harmony_memory'][index][1], beta)
                      * pow(path_candidate['harmony_pheromone_candidate_value'][index], alpha))

        matrix = [(pow(path_candidate['harmony_pheromone_candidate_value'][index_harmony], alpha)
                   * pow(1 / path_candidate['harmony_memory'][index_harmony][1], beta)) / total
                  for index_harmony in range(len(path_candidate['harmony_memory']))]

        path_candidate['transition_prob_for_harmony_candidate'] = matrix


def update_weight_matrix(path_solution_candidate: List[Dict]):
    new_matrix = relationship_matrix.clone().detach()

    for path_candidate in path_solution_candidate:
        from_index: int = 0 if path_candidate['from'] == START_NODE else num_kpi + 1 \
            if path_candidate['from'] == FINISH_NODE else int(path_candidate['from'])
        to_index: int = 0 if path_candidate['to'] == START_NODE else num_kpi + 1 \
            if path_candidate['to'] == FINISH_NODE else int(path_candidate['to'])

        new_matrix[from_index, to_index] = path_candidate['best_candidate'][1]

    return new_matrix


if __name__ == '__main__':

    start = datetime.now()
    print("Start generate data")

    # build ant path matrix
    relationship_matrix: torch.Tensor = torch.tensor([
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 1, 0, 1],
        [0, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0]
    ], dtype=torch.float32)

    num_kpi: int = 5

    object_function = ObjectiveFunction()
    harmony_search = HarmonySearch(object_function)

    # define generation, number, alpha, beta of ants in ant colony
    generation: int = 500
    number_ants: int = 10
    alpha: float = 0.4
    beta: float = 2

    # define max of improvisations in harmony search solution
    # max_improvisations: int = 500000

    # define best solution variable
    best_ant_path: List[str] = list()
    best_ant_path_length: float = 0

    best_solution_each_path: List[List[float]] = list()  # harmony search solution

    # build weight matrix base candidate of harmony search
    weight_matrix = torch.zeros((num_kpi + 2, num_kpi + 2))

    # build harmony search solution candidate
    path_solution_candidate: List[Dict] = list()
    for row in range(relationship_matrix.size(0)):
        for col in range(relationship_matrix.size(1)):
            if relationship_matrix[row, col] > 0 and col != num_kpi + 1:
                harmony_memory = harmony_search.initialize__harmony_memory()
                harmony_pheromone_candidate_value = torch.ones(len(harmony_memory))

                total = 0
                for index, harmony in enumerate(harmony_memory):
                    total += pow(1 / harmony[1], beta) * pow(harmony_pheromone_candidate_value[index], alpha)

                transition_prob_for_harmony_candidate = torch.Tensor(
                    [pow(p, alpha) * pow((1 / h[1]), beta) / total
                     for h, p in zip(harmony_memory, harmony_pheromone_candidate_value)
                     ])

                payload = {
                    'from': START_NODE if row == 0 else FINISH_NODE if row == num_kpi + 1 else str(row),
                    'to': START_NODE if col == 0 else FINISH_NODE if col == num_kpi + 1 else str(col),
                    'harmony_memory': harmony_memory,
                    'harmony_pheromone_candidate_value': harmony_pheromone_candidate_value,
                    'transition_prob_for_harmony_candidate': transition_prob_for_harmony_candidate,
                    'best_candidate': min(harmony_memory, key=lambda x: x[1])
                }

                weight_matrix[row, col] = payload['best_candidate'][1]
                path_solution_candidate.append(payload)

            if col == num_kpi + 1:
                weight_matrix[row, col] = 1

    # generate aco and hs instance
    aco = AntColony(population=number_ants, generation=generation, local_ro=0.6, global_ro=0.4,
                    weight_matrix=weight_matrix, alpha=alpha, beta=beta)
    hs = HarmonySearch(
        object_function)

    print("Done generate data")

    # end = datetime.now()
    # elapsed_time = end - start
    # print("Elapsed time: " + str(elapsed_time))

    # start loop
    for index_gen in range(10000):
        # build transition prob matrix for edge
        transition_prob_matrix: torch.Tensor = build_transition_prob_matrix(path_solution_candidate)
        # print(transition_prob_matrix)

        # start harmony search
        for index, path_candidate in enumerate(path_solution_candidate):
            # print(path_candidate)
            harmony_search.set_harmony_memory(path_candidate['harmony_memory'])

            # generate new harmony
            while True:
                harmony = list()
                for parameter in range(0, object_function.get_number_parameters()):
                    if random() < object_function.get_hmcr():
                        harmony_search.memory_consideration(harmony, parameter)

                        if random() < object_function.get_par():
                            harmony_search.pitch_adjustment(harmony, parameter)
                    else:
                        harmony_search.random_selection(harmony)

                if is_truncated_normal(harmony):
                    break

            fitness = object_function.get_fitness(harmony)
            harmony_search.update_harmony_memory(harmony, fitness, path_solution_candidate, index)

            path_candidate['best_candidate'] = min(path_candidate['harmony_memory'], key=lambda x: x[1])

        weight_matrix = update_weight_matrix(path_solution_candidate)
        aco.set_weight_matrix(weight_matrix=weight_matrix)
        # end harmony search

        update_transition_prob_for_harmony_candidate(path_solution_candidate)

        # start aco
        current_generation_path = list()

        for _ in range(10):
            current_ant_path: List[str] = [START_NODE, str(randint(1, num_kpi))]

            while len(current_ant_path) != len(aco.get_weight_matrix()):
                reachable_point = aco.get_list_available_next_note(current_ant_path[-1], current_ant_path)
                best_next_point = aco.get_best_next_point(current_ant_path[-1], reachable_point, transition_prob_matrix)
                current_ant_path.append(best_next_point)

            if current_ant_path.count(FINISH_NODE) == 1 and current_ant_path.count(START_NODE) == 1:
                convert_data: Dict[str, List[str] | float] = {
                    'length': aco.calculate_length(current_ant_path),
                    'path': current_ant_path,
                }
                current_generation_path.append(convert_data)

        aco.update_local_pheromone(path_solution_candidate)

        if current_generation_path:
            shortest_length_item: Dict[str, List[str] | float] | None = (
                min(current_generation_path, key=lambda x: x['length']))
            if shortest_length_item is not None and (best_ant_path_length == 0
                                                     or shortest_length_item['length'] < best_ant_path_length):
                best_ant_path_length = shortest_length_item['length']
                best_ant_path = shortest_length_item['path']

            aco.update_global_pheromone(shortest_length_item, path_solution_candidate)
        # end aco

        print("Done index gen?", index_gen)

    end = datetime.now()
    elapsed_time = end - start
    print("Elapsed time: " + str(elapsed_time))

    # print result
    print(best_ant_path_length, best_ant_path)
    total_value_output = 0
    data_to_write = []
    import json

# Function to recursively convert elements within a nested structure to JSON serializable types
    def convert_to_serializable(obj):
        if isinstance(obj, torch.Tensor):
            return obj.tolist()  # Convert Tensor to list
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]  # Recursively convert list elements
        else:
            raise TypeError(f"Type {type(obj)} is not JSON serializable")


    # total_value_output = 0

    for index, path_item in enumerate(best_ant_path[:-1]):
        for path_candidate in path_solution_candidate:
            if (path_candidate['to'] == best_ant_path[index + 1]) and path_candidate['from'] == path_item:
                payload = {
                    'kpi': path_candidate['to'],
                    'matrix': convert_to_serializable(path_candidate['best_candidate'][0])
                }

                total_value_output = path_candidate['best_candidate'][1]

                data_to_write.append(payload)

    print(data_to_write)

    file_path = "output.json"

    file_path_employee_weight = 'weights.json'

    # # Load JSON data from a file
    # with open(file_path, 'r') as file:
    #     data = json.load(file)

    # Format the JSON data with indentation and write it back to the file
    with open(file_path, 'w') as file:
        json.dump(data_to_write, file, indent=4)

    with open(file_path_employee_weight, 'w') as file:
        json.dump(convert_to_serializable(object_function.test_weight_employees), file, indent=4)

    # for path_candidate in path_solution_candidate:
    #     # print(path_candidate['best_candidate'])
    #     print(path_candidate)



        # for index, path_item in enumerate(best_current_gen_path['path'][:-1]):
        #             for path_candidate in path_solution_candidates:
        #                 if (path_candidate['to'] == best_current_gen_path['path'][index + 1]
        #                         and path_candidate['from'] == path_item):
        #                     index_best_candidate: int = next((i for i, x in enumerate(path_candidate['harmony_memory'])
        #                                                       if torch.equal(torch.tensor(x[0]),
        #                                                                      torch.tensor(path_candidate['best_candidate'][0]))
        #                                                       and x[1] == path_candidate['best_candidate'][1]), None)
        #                     update_value: float = ((1 - self.get_global_ro())
        #                                            * float(path_candidate['harmony_pheromone_candidate_value']
        #                                                    [index_best_candidate])
        #                                            + self.get_global_ro() * (1 / path_candidate['best_candidate'][1]))
        #
        #                     path_candidate['harmony_pheromone_candidate_value'][index_best_candidate] = update_value

        # total_value_output += path_candidate['best_candidate'][1]

    print("Result is beter?", total_value_output / 5)
    # print("Employee result?", object_function.test_weight_employees)
