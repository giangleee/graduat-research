from typing import List, Dict
from random import randint
from ant_colony_operation import AntColonyOperation

# define const
START_POINT_VALUE = 'start'


class AntColony(AntColonyOperation):
    def __init__(self, population: int, generation: int):
        super().__init__(population=population, generation=generation)

    def run(self) -> None:
        for _ in range(self.get_generation()):
            current_generation_path: List[Dict[str, List[str] | float]] = []

            for index in range(self.get_population()):
                current_ant_path: List[str] = []
                if not current_ant_path:
                    current_ant_path.append(START_POINT_VALUE)

                current_ant_path.append(str(randint(1, len(self.get_weight_matrix()) - 2)))

                while len(current_ant_path) != len(self.get_weight_matrix()):
                    reachable_point = self.get_list_available_next_note(current_ant_path[-1], current_ant_path)
                    best_next_point = self.get_best_next_point(current_ant_path[-1], reachable_point)
                    current_ant_path.append(best_next_point)

                convert_data: Dict[str, List[str] | float] = {"ant": index + 1,
                                                              "length": self.calculate_length(current_ant_path),
                                                              "path": current_ant_path}
                current_generation_path.append(convert_data)

            self.update_pheromone_evaporation()
            self.update_pheromone_intensity(current_generation_path)
            smallest_length_item = min(current_generation_path, key=lambda x: x['length'])

            if self.get_best_path_length() == 0 or smallest_length_item['length'] <= self.get_best_path_length():
                self.set_best_path(smallest_length_item['path'])
                self.set_best_path_length(smallest_length_item['length'])

        print(self.get_best_path_length())
        print(self.get_best_path())
        print(self.get_pheromone_tao_matrix())


if __name__ == "__main__":
    aco = AntColony(100, 10)
    aco.run()
