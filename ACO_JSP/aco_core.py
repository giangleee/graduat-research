from typing import List, Dict
from random import randint
from ant_colony_operation import AntColonyOperation
from numpy import ndarray


# define const
START_POINT_VALUE = 'start'
END_POINT_VALUE = 'finish'


class AntColonyForJSP(AntColonyOperation):
    def __init__(self, populations: int, generations: int, local_ro: List, global_ro: List, weight_matrix: ndarray):
        super().__init__(population=populations, generation=generations, local_ro= local_ro, global_ro=global_ro, weight_matrix=weight_matrix)

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

                if current_ant_path.count(END_POINT_VALUE) == 1 and current_ant_path.count(START_POINT_VALUE) == 1:
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

        return { "best_path_length": self.get_best_path_length(), "best_path": self.get_best_path() }
