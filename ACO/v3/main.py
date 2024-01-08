from KPI import get_kpi_weight_matrix, get_list_KPI_unit, get_list_KPI_env_score, get_list_KPI_human_score
from Human import get_list_human
import random


class ASO:
    __slots__ = ("__weight_matrix", "__kpi_unit", "__kpi_env_score", "__human_ability_score", "__kpi_human_score",
                 "__pheromone_tao_matrix", "__population", "__generation", "__beta", "__ro", "__best_path", "__best_path_length", "__default_pheromone_tao_matrix")

    def __init__(self,  generation: int, population: int, beta: int = 2, ro: float = 0.4) -> None:
        self.__weight_matrix = get_kpi_weight_matrix()
        self.__kpi_unit = get_list_KPI_unit()
        self.__kpi_env_score = get_list_KPI_env_score()
        self.__human_ability_score = get_list_human()
        self.__kpi_human_score = get_list_KPI_human_score()
        self.__default_pheromone_tao_matrix = [[0 if i == j else 1 for j in range(
            len(self.__kpi_unit))]for i in range(len(self.__kpi_unit))]
        self.__pheromone_tao_matrix = self.__default_pheromone_tao_matrix
        self.__generation = generation
        self.__population = population
        self.__beta = beta
        self.__ro = ro
        self.__best_path = []
        self.__best_path_length = 0

    def get_eta_value(self, startPoint: int, endPoint: int) -> float:
        return 1/self.__weight_matrix[startPoint][endPoint]

    def get_rho_value(self, endPoint: int, humanId: int) -> float:
        endPointEnvScore = next(
            (item.score for item in self.__kpi_env_score if item.kpi_id == endPoint), 0)
        humanScore = next(
            (human.score for human in self.__human_ability_score if human.id == humanId), 0)

        return (1 - endPointEnvScore) * (1 - humanScore)

    def get_human_probabilistic_base_kpi(self, humanId: int, kpiId: int) -> float:
        matched_item = next(
            (item.score for item in self.__kpi_human_score
             if item.human_id == humanId and item.kpi_id == kpiId), None
        )
        return matched_item if matched_item is not None else 0.0

    def get_list_available_next_note(self, startPoint: int, visitedPoint):
        reachable_points = [
            i + 1 for i, val in enumerate(self.__weight_matrix[startPoint])
            if val > 0 and (i + 1) not in visitedPoint
        ]
        return reachable_points

    def equation_value(self, startNode: int, endNode: int) -> float:
        return self.__pheromone_tao_matrix[startNode - 1][endNode - 1] * pow(
            self.get_eta_value(startNode - 1, endNode - 1), self.__beta)*self.get_human_probabilistic_base_kpi(1, endNode - 1)

    def get_best_next_node(self, startNode, list_reachable_point) -> int:
        if not list_reachable_point:
            return -1

        point = {}
        randomNumber = random.random()

        equation_values = {item: self.equation_value(
            startNode, item) for item in list_reachable_point}

        if randomNumber <= self.__ro:
            for item, value in equation_values.items():
                point[item] = 1 - value
        else:
            total_equation_value = sum(equation_values.values())
            for item, value in equation_values.items():
                point[item] = 1 - value / total_equation_value

        return max(point, key=point.get, default=-1)

    def are_adjacent(self, array, startPoint, endPoint):
        try:
            start_index = array.index(startPoint)
            end_index = array.index(endPoint)
            array_length = len(array)

            return (
                start_index + 1 == end_index or
                (startPoint == array[array_length - 2]
                 and endPoint == array[array_length - 1])
            )
        except ValueError:
            return False


    def update_pheromone(self, indexRow, indexColumn, is_global=False):
        if self.__pheromone_tao_matrix[indexRow][indexColumn] != 0:
            current_rho_value = self.get_rho_value(indexColumn + 1, 1)
            pheromone_value = self.__pheromone_tao_matrix[indexRow][indexColumn]

            if is_global and self.are_adjacent(self.__best_path, indexRow + 1, indexColumn + 1):
                update_value = (1 - current_rho_value) * pheromone_value + \
                    current_rho_value * (1 / self.__best_path_length)
            else:
                update_value = self.__default_pheromone_tao_matrix[indexRow][indexColumn] * current_rho_value + \
                    (1 - current_rho_value) * pheromone_value

            self.__pheromone_tao_matrix[indexRow][indexColumn] = update_value


    def update_local_pheromone(self) -> None:
        for indexRow, row in enumerate(self.__pheromone_tao_matrix):
            for indexColumn, _ in enumerate(row):
                self.update_pheromone(indexRow, indexColumn)


    def update_global_pheromone(self) -> None:
        for indexRow, row in enumerate(self.__pheromone_tao_matrix):
            for indexColumn, _ in enumerate(row):
                self.update_pheromone(indexRow, indexColumn, is_global=True)


    def calculate_len(self, path: list = []) -> int:
        total_length = 0

        for index in range(len(path) - 1):
            current_node = path[index] - 1
            next_node = path[index + 1] - 1
            total_length += self.__weight_matrix[current_node][next_node]

        if len(path) > 1:
            last_but_one_node = path[-2] - 1
            last_node = path[-1] - 1
            total_length += self.__weight_matrix[last_but_one_node][last_node]

        return total_length

    def run(self):
        for _ in range(self.__generation):
            current_gen_path = {}
            for _ in range(self.__population):
                current_ant_path = []
                if (current_ant_path == []):
                    current_ant_path.append(1)
                # loop
                while len(current_ant_path) != len(self.__kpi_unit):
                    reachable_point = self.get_list_available_next_note(
                        current_ant_path[0] - 1, current_ant_path)
                    best_next_point = self.get_best_next_node(
                        current_ant_path[0], reachable_point)
                    current_ant_path.append(best_next_point)

                # add start point into final path
                current_ant_path.append(current_ant_path[0])

                # find best path for this ant
                current_ant_length = self.calculate_len(current_ant_path)
                current_gen_path[current_ant_length] = current_ant_path

            self.update_local_pheromone()

            self.__best_path_length = max(current_gen_path.keys())
            self.__best_path = current_gen_path[self.__best_path_length]

            self.update_global_pheromone()

        print(self.__best_path_length)


aco = ASO(20, 100)
aco.run()
