from KPI import get_kpi_weight_matrix, get_list_KPI_unit, get_list_KPI_env_score, get_list_KPI_human_score, get_index_by_kpi_id_in_file, KPIUnit
from Human import get_list_human
import random
import numpy
from decimal import Decimal, getcontext
from random import randint

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


def get_key_by_index(dictionary, index):
    keys_list = list(dictionary.keys())
    return next((key for i, key in enumerate(keys_list) if i == index), None)


def build_matrix(numPoint, matrixDisc):
    matrix = numpy.zeros((numPoint, numPoint), dtype=int)
    for i, key in enumerate(matrixDisc.keys()):
        matrix[i, :] = numpy.array(matrixDisc[key]) > 0
    return matrix


def get_object_by_id(my_list, target_id):
    for obj in my_list:
        if str(obj.id) == target_id:
            return obj


class ASO:
    __slots__ = ("__weight_matrix", "__kpi_unit", "__kpi_env_score", "__human_ability_score", "__kpi_human_score",
                 "__pheromone_tao_matrix", "__population", "__generation", "__beta", "__ro", "__best_path", "__best_path_length", "__default_pheromone_tao_matrix")

    def __init__(self,  generation: int, population: int, beta: int = 2, ro: float = 0.4) -> None:
        self.__kpi_unit = get_list_KPI_unit()
        self.__weight_matrix = get_kpi_weight_matrix()
        self.__kpi_env_score = get_list_KPI_env_score()
        self.__human_ability_score = get_list_human()
        self.__kpi_human_score = get_list_KPI_human_score()
        self.__default_pheromone_tao_matrix = build_matrix(
            len(self.__weight_matrix[START_POINT_VALUE]), self.__weight_matrix)
        self.__pheromone_tao_matrix = self.__default_pheromone_tao_matrix
        self.__generation = generation
        self.__population = population
        self.__beta = beta
        self.__ro = ro
        self.__best_path = []
        self.__best_path_length = 0

    def get_eta_value(self, startPoint: str, endPoint: str) -> float:
        return 1/self.__weight_matrix[startPoint][get_index_by_kpi_id_in_file(kpi_id=endPoint)]

    def get_rho_value(self, endPointIndex: int, humanId: int) -> float:
        endPointEnvScore = next(
            (item.score for item in self.__kpi_env_score if str(int(item.kpi_id)) == get_key_by_index(self.__weight_matrix, endPointIndex)), 0)
        humanScore = next(
            (human.ability_score for human in self.__human_ability_score if human.id == humanId), 0)

        return (1 - endPointEnvScore) * (1 - humanScore)

    def get_human_probabilistic_base_kpi(self, humanId: int, endNode: str) -> float:
        matched_item = next(
            (item.score for item in self.__kpi_human_score
             if item.human_id == humanId and item.kpi_id == get_object_by_id(self.__kpi_unit, endNode).id), None
        )
        return matched_item if matched_item is not None else 0.0

    def get_list_available_next_note(self, startPoint, listVisitedPoint):
        convertStartPoint = str(int(startPoint)) if startPoint not in {
            START_POINT_VALUE, FINISH_POINT_VALUE} else startPoint

        reachable_points = [
            get_key_by_index(self.__weight_matrix, index)
            for index, value in enumerate(self.__weight_matrix[convertStartPoint])
            if value > 0 and get_key_by_index(self.__weight_matrix, index) not in listVisitedPoint
        ]

        return reachable_points

    def equation_value(self, startNode: int, endNode: int) -> float:
        return self.__pheromone_tao_matrix[get_index_by_kpi_id_in_file(kpi_id=startNode)][get_index_by_kpi_id_in_file(kpi_id=endNode)] * pow(
            self.get_eta_value(startNode, endNode), self.__beta) * self.get_human_probabilistic_base_kpi(1, endNode)

    def get_best_next_node(self, startNode, listReachablePoint) -> str:
        if not listReachablePoint:
            return 'finish'

        point = {}
        randomNumber = random.random()

        equation_values = {item: self.equation_value(
            startNode, item) for item in listReachablePoint}
        # print(equation_values)

        if randomNumber <= self.__ro:
            for item, value in equation_values.items():
                point[item] = 1 - value
        else:
            total_equation_value = sum(equation_values.values())
            print(equation_values)
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
        if self.__pheromone_tao_matrix[indexRow][indexColumn] > 0:
            current_rho_value = self.get_rho_value(indexColumn, 1)
            pheromone_value = self.__pheromone_tao_matrix[indexRow][indexColumn]

            update_value = 0

            if is_global:
                update_value = (1 - current_rho_value) * pheromone_value + \
                    current_rho_value * (1 / self.__best_path_length)
            else:
                update_value = self.__default_pheromone_tao_matrix[indexRow][indexColumn] * current_rho_value + \
                    (1 - current_rho_value) * pheromone_value

            self.__pheromone_tao_matrix[indexRow][indexColumn] = update_value
            # print(self.__pheromone_tao_matrix[indexRow][indexColumn])


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

        for index, value in enumerate(path):
            if value != FINISH_POINT_VALUE:
                total_length += self.__weight_matrix[value][get_index_by_kpi_id_in_file(
                    kpi_id=path[index + 1])]

        return total_length

    def run(self):
        for _ in range(self.__generation):
            current_gen_path = {}
            for _ in range(self.__population):
                current_ant_path = []
                if (current_ant_path == []):
                    current_ant_path.append('start')
                current_ant_path.append(
                    str(randint(1, len(self.__weight_matrix) - 2)))

                # loop
                while len(current_ant_path) != len(self.__kpi_unit):
                    reachable_point = self.get_list_available_next_note(
                        current_ant_path[-1], current_ant_path)
                    best_next_point = self.get_best_next_node(
                        current_ant_path[-1], reachable_point)
                    current_ant_path.append(best_next_point)

                # find best path for this ant
                current_ant_length = self.calculate_len(current_ant_path)
                current_gen_path[current_ant_length] = current_ant_path

            self.update_local_pheromone()

            self.__best_path_length = max(current_gen_path.keys())
            self.__best_path = current_gen_path[self.__best_path_length]
            # print(self.__best_path, self.__best_path_length)


            self.update_global_pheromone()

        print(self.__best_path)


aco = ASO(2, 5)
aco.run()
