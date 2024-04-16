from random import randint
from typing import List, Dict
from numpy import ndarray, array, zeros_like
from copy import deepcopy
import torch

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


def get_index_base_name_point(matrix: ndarray, name_point: str) -> int:
    if name_point == START_POINT_VALUE:
        return 0

    if name_point == FINISH_POINT_VALUE:
        return len(matrix[0]) - 1

    return int(name_point)


def get_name_point_base_index(matrix: ndarray, index: int) -> str:
    if index == 0:
        return START_POINT_VALUE

    if len(matrix[0]) - 1 == index:
        return FINISH_POINT_VALUE

    return str(index)


def calculate_sum_each_path_base_ant(list_current_gen_path: List[Dict[str, List[str] | float]],
                                     start_point: str, end_point: str) -> float:
    return sum(1 / item['length'] for item in list_current_gen_path
               for index, path_item in enumerate(item['path'][:-1])
               if path_item == start_point and item['path'][index + 1] == end_point)


def generate_pheromone_matrix(matrix: ndarray) -> ndarray:
    binary_matrix = zeros_like(matrix, dtype=float)

    for i, row in enumerate(matrix):
        binary_matrix[i] = [0.1 if item > 0 else 0.0 for item in row]

    return binary_matrix


class AntColony(object):
    __slots__ = ("__weight_matrix", "__population", "__generation", "__alpha", "__beta", "__ro", "__best_path",
                 "__best_path_length", "__default_pheromone_tao_matrix", "__pheromone_tao_matrix", "__number_elite_ant",
                 "__local_ro", "__global_ro")

    __weight_matrix: torch.Tensor
    __population: int
    __generation: int
    __alpha: float
    __beta: float
    __ro: float
    __best_path: List[str]
    __best_path_length: float
    __default_pheromone_tao_matrix: torch.Tensor
    __pheromone_tao_matrix: torch.Tensor
    __number_elite_ant: int
    __local_ro: float
    __global_ro: float

    def __init__(self, population: int, generation: int, local_ro: float, global_ro: float, weight_matrix: torch.Tensor,
                 alpha: float, beta: float, ro: float = 0.4):
        self.__population = population
        self.__generation = generation
        self.__alpha = alpha
        self.__beta = beta
        self.__ro = ro
        self.__weight_matrix = weight_matrix
        self.__best_path = []
        self.__best_path_length = 0
        self.__local_ro = local_ro
        self.__global_ro = global_ro

    def get_population(self) -> int:
        return self.__population

    def get_generation(self) -> int:
        return self.__generation

    def get_weight_matrix(self) -> ndarray:
        return self.__weight_matrix

    def set_weight_matrix(self, weight_matrix: ndarray) -> None:
        self.__weight_matrix = weight_matrix

    def get_pheromone_tao_matrix(self) -> ndarray:
        return self.__pheromone_tao_matrix

    def get_default_pheromone_tao_matrix(self) -> ndarray:
        return self.__default_pheromone_tao_matrix

    def set_pheromone_tao_matrix(self, value: float) -> None:
        self.__pheromone_tao_matrix = self.__pheromone_tao_matrix * value

    def set_each_item_pheromone_tao_matrix(self, index_row: int, index_col: int, value: float) -> None:
        self.__pheromone_tao_matrix[index_row, index_col] += value

    def set_assign_value_pheromone_tao_matrix(self, index_row: int, index_col: int, value: float) -> None:
        self.__pheromone_tao_matrix[index_row, index_col] = value

    def get_alpha(self) -> float:
        return self.__alpha

    def get_beta(self) -> float:
        return self.__beta

    def get_ro(self) -> float:
        return self.__ro

    def set_best_path_length(self, length: float) -> None:
        self.__best_path_length = length

    def set_best_path(self, path: List[str]) -> None:
        self.__best_path = path

    def get_best_path(self) -> List[str]:
        return self.__best_path

    def get_best_path_length(self) -> float:
        return self.__best_path_length

    def get_local_ro(self) -> float:
        return self.__local_ro

    def get_global_ro(self) -> float:
        return self.__global_ro

    def calculate_length(self, path: List[str]) -> float:
        total_length: float = 0

        for index, value in enumerate(path):
            if value != FINISH_POINT_VALUE:
                index_start_point: int = get_index_base_name_point(
                    self.get_weight_matrix(), value)
                index_next_point: int = get_index_base_name_point(
                    self.get_weight_matrix(), path[index + 1])
                total_length += self.get_weight_matrix(
                )[index_start_point][index_next_point]

        return total_length

    def get_each_path_length(self, path: List[str]):
        response_data = {}
        for index, value in enumerate(path):
            if value != FINISH_POINT_VALUE:
                index_start_point: int = get_index_base_name_point(
                    self.get_weight_matrix(), value)
                index_next_point: int = get_index_base_name_point(
                    self.get_weight_matrix(), path[index + 1])

                if path[index + 1] == FINISH_POINT_VALUE:
                    key = int(value)
                else:
                    key = int(path[index + 1])
                # key = f"{value}_{path[index + 1]}"
                response_data[key] = self.get_weight_matrix(
                )[index_start_point][index_next_point]

        return response_data

    def get_eta_value(self, start_point: str, end_point: str) -> float:
        index_start_point: int = get_index_base_name_point(
            self.get_weight_matrix(), start_point)
        index_next_point: int = get_index_base_name_point(
            self.get_weight_matrix(), end_point)
        return 1 / float(self.get_weight_matrix()[index_start_point, index_next_point])

    def get_list_available_next_note(self, start_point: str, list_visited_point: List[str]) -> List[str]:
        reachable_point: List[str] = []

        for index, value in enumerate(
                self.get_weight_matrix()[get_index_base_name_point(self.get_weight_matrix(), start_point)]):
            if value > 0 and index + 1 != len(self.get_weight_matrix()) and str(index) not in list_visited_point:
                reachable_point.append(str(index))

        return reachable_point

    def calculate_equation_value(self, start_point: str, next_point: str) -> float:
        index_start_point: int = get_index_base_name_point(
            self.get_weight_matrix(), start_point)
        index_next_point: int = get_index_base_name_point(
            self.get_weight_matrix(), next_point)

        return (pow(self.get_pheromone_tao_matrix()[index_start_point][index_next_point], self.get_alpha())
                * pow(self.get_eta_value(start_point, next_point), self.get_beta()))

    def get_best_next_point(self, start_point: str, list_reachable_point: List[str],
                            transition_prob_matrix) -> str:
        if not list_reachable_point:
            return FINISH_POINT_VALUE

        index_start_point: int = get_index_base_name_point(self.get_weight_matrix(), start_point)

        equation_value: Dict[str, float] = {next_point: float(transition_prob_matrix[index_start_point,
        get_index_base_name_point(self.get_weight_matrix(), next_point)])
                                            for next_point in list_reachable_point}

        total_equation_value = sum(equation_value.values())

        point: Dict[str, float] = {}

        for item, value in equation_value.items():
            point[item] = value / total_equation_value

        return max(point, key=point.get, default=-1)

    def update_local_pheromone(self, path_solution_candidates: List[Dict]) -> None:
        for path_candidate in path_solution_candidates:
            for index, candidate_pheromone_value in enumerate(path_candidate['harmony_pheromone_candidate_value']):
                update_value: float = ((1 - self.get_local_ro()) * float(candidate_pheromone_value)
                                       + candidate_pheromone_value * self.get_local_ro())

                path_candidate['harmony_pheromone_candidate_value'][index] = update_value

    def update_global_pheromone(self, best_current_gen_path, path_solution_candidates: List[Dict]) -> None:
        for index, path_item in enumerate(best_current_gen_path['path'][:-1]):
            for path_candidate in path_solution_candidates:
                if (path_candidate['to'] == best_current_gen_path['path'][index + 1]
                        and path_candidate['from'] == path_item):
                    index_best_candidate: int = next((i for i, x in enumerate(path_candidate['harmony_memory'])
                                                      if torch.equal(torch.tensor(x[0]),
                                                                     torch.tensor(path_candidate['best_candidate'][0]))
                                                      and x[1] == path_candidate['best_candidate'][1]), None)
                    update_value: float = ((1 - self.get_global_ro())
                                           * float(path_candidate['harmony_pheromone_candidate_value']
                                                   [index_best_candidate])
                                           + self.get_global_ro() * (1 / path_candidate['best_candidate'][1]))

                    path_candidate['harmony_pheromone_candidate_value'][index_best_candidate] = update_value

    def run(self):
        for _ in range(self.get_generation()):
            current_generation_path: List[Dict[str, List[str] | float]] = []

            for index in range(self.get_population()):
                # seed(42)
                current_ant_path: List[str] = [START_POINT_VALUE, str(
                    randint(1, len(self.get_weight_matrix()) - 2))]

                while len(current_ant_path) != len(self.get_weight_matrix()):
                    reachable_point = self.get_list_available_next_note(
                        current_ant_path[-1], current_ant_path)
                    best_next_point = self.get_best_next_point(
                        current_ant_path[-1], reachable_point)
                    current_ant_path.append(best_next_point)

                if current_ant_path.count(FINISH_POINT_VALUE) == 1 and current_ant_path.count(START_POINT_VALUE) == 1:
                    convert_data: Dict[str, List[str] | float] = {"ant": index + 1,
                                                                  "length": self.calculate_length(current_ant_path),
                                                                  "path": current_ant_path}
                    current_generation_path.append(convert_data)

            self.update_local_pheromone()
            longest_length_item: Dict[str, List[str] | float] = max(
                current_generation_path, key=lambda x: x['length'])
            if self.get_best_path_length() == 0 or longest_length_item['length'] > self.get_best_path_length():
                self.set_best_path(longest_length_item['path'])
                self.set_best_path_length(longest_length_item['length'])
            self.update_global_pheromone(longest_length_item)

        return {"best_path_length": self.get_best_path_length(), "best_path": self.get_best_path()}
