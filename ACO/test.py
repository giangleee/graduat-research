from KPI import get_kpi_weight_matrix, get_list_KPI_unit, get_list_KPI_env_score, get_list_KPI_human_score, get_index_by_kpi_id_in_file, KPIUnit
from Human import get_list_human
import random
import numpy
from decimal import Decimal, getcontext

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


def build_matrix(numPoint, matrixDisc):
    matrix = numpy.zeros((numPoint, numPoint), dtype=float)
    for i, key in enumerate(matrixDisc.keys()):
        matrix[i, :] = numpy.array(matrixDisc[key]) > 0
    return matrix


def get_key_by_index(dictionary, index):
    keys_list = list(dictionary.keys())
    return next((key for i, key in enumerate(keys_list) if i == index), None)

class AntSystemOptimization:
    __slots__ = ("__weight_matrix", "__list_kpi_unit", "__kpi_env_score", "__human_ability_score", "__kpi_human_score", "__pheromone_tao_matrix",
                 "__population", "__generation", "__beta", "__ro", "__best_path", "__best_path_length", "__default_pheromone_tao_matrix")

    def __init__(self, generation: int, population: int, beta: int = 2, ro: float = 0.4) -> None:
        self.__list_kpi_unit = get_list_KPI_unit()
        self.__weight_matrix = get_kpi_weight_matrix()
        self.__kpi_env_score = get_list_KPI_env_score()
        self.__human_ability_score = get_list_human()
        self.__kpi_human_score = get_list_KPI_human_score()
        self.__default_pheromone_tao_matrix = build_matrix(
            len(self.__weight_matrix[START_POINT_VALUE]), self.__weight_matrix)
        self.__pheromone_tao_matrix = numpy.copy(
            self.__default_pheromone_tao_matrix)
        self.__generation = generation
        self.__population = population
        self.__beta = beta
        self.__ro = ro
        self.__best_path = []
        self.__best_path_length = 0

    def get_human_probabilistic_base_kpi(self, humanId: str, endPointId: str) -> float:
        matching_items = [item for item in self.__kpi_human_score if item.human_id ==
                          humanId and endPointId == str(item.kpi_id)]
        return matching_items[0].score if matching_items else 0.0

    def get_list_available_next_point(self, startPoint, currentAntPath):
        convertStartPoint = str(int(startPoint)) if startPoint not in {
            START_POINT_VALUE, FINISH_POINT_VALUE} else startPoint

        reachable_points = [
            get_key_by_index(self.__weight_matrix, index)
            for index, value in enumerate(self.__weight_matrix[convertStartPoint])
            if value > 0 and get_key_by_index(self.__weight_matrix, index) not in currentAntPath
        ]

        return reachable_points

    # check lai cong thuc
    def get_eta_value(self, startPoint: str, endPointIndex: int) -> float:
        return 1/self.__weight_matrix[startPoint][endPointIndex]

    # check lai cong thuc
    def equation_value(self, startPoint: str, endPoint: str) -> float:
        index_start_point = get_index_by_kpi_id_in_file(kpi_id=startPoint)
        index_end_point = get_index_by_kpi_id_in_file(kpi_id=endPoint)
        return self.__pheromone_tao_matrix[index_start_point][index_end_point] * pow(self.get_eta_value(startPoint, endPointIndex=index_end_point), self.__beta) * self.get_human_probabilistic_base_kpi(1, endPoint)

    # check lai cong thuc
    def get_best_next_node(self, startPoint, reachablePoint) -> str:
        if not reachablePoint:
            return 'finish'

        point = {}
        randomNumber = random.random()

        equation_values = {item: self.equation_value(
            startPoint, item) for item in reachablePoint}
        if FINISH_POINT_VALUE in equation_values and len(equation_values) != 1:
            del equation_values[FINISH_POINT_VALUE]

        if FINISH_POINT_VALUE in equation_values and len(equation_values) == 1:
            return FINISH_POINT_VALUE
        else:
            if randomNumber <= self.__ro:
                total_equation_value = sum(equation_values.values())
                for key, value in equation_values.items():
                    # print(item, value)
                    point[key] = 1 - value / total_equation_value
            else:
                total_equation_value = sum(equation_values.values())
                for key, value in equation_values.items():
                    # print(item, value)
                    point[key] = 1 - value / total_equation_value

            return max(point, key=point.get, default=-1)

    def calculate_len(self, path: list = []) -> float:
        total_length = 0

        for index, value in enumerate(path):
            if value != FINISH_POINT_VALUE:
                total_length += self.__weight_matrix[value][get_index_by_kpi_id_in_file(
                    kpi_id=path[index + 1])]
        return total_length

    def get_rho_value(self, humanId: str, endPointIndex: int) -> float:
        endPointEnvScore = next((item.score for item in self.__kpi_env_score if str(
            item.kpi_id) == get_key_by_index(self.__weight_matrix, endPointIndex)), 0)

        humanScore = next((item.ability_score for item in self.__human_ability_score if str(
            item.id) == humanId), 0)

        return (1 - endPointEnvScore) * (1 - humanScore)

    def update_pheromone(self, indexRow: int, indexColumn: int, isGlobal: bool = False):
        if self.__pheromone_tao_matrix[indexRow][indexColumn] != 0:
            current_rho_value = self.get_rho_value('1', indexColumn)
            current_pheromone_value = self.__pheromone_tao_matrix[indexRow][indexColumn]

            update_value = 0

            if isGlobal:
                update_value = (1 - current_rho_value) * current_pheromone_value + \
                    current_rho_value * (1 / self.__best_path_length)
            else:
                update_value = self.__default_pheromone_tao_matrix[indexColumn][indexRow] * current_rho_value + (
                    1 - current_rho_value) * current_pheromone_value

            # print(update_value)
            self.__pheromone_tao_matrix[indexRow][indexColumn] = update_value

    def update_local_pheromone(self):
        for indexRow, row in enumerate(self.__pheromone_tao_matrix):
            for indexColumn, _ in enumerate(row):
                self.update_pheromone(indexRow, indexColumn)

    def update_global_pheromone(self):
        for index, item in enumerate(self.__best_path):
            if item != FINISH_POINT_VALUE:
                indexItem = get_index_by_kpi_id_in_file(kpi_id=item)
                indexNextItem = get_index_by_kpi_id_in_file(
                    kpi_id=self.__best_path[index + 1])
                self.update_pheromone(indexItem, indexNextItem, True)

    def run(self):
        for _ in range(self.__generation):
            current_gen_path = {}

            for _ in range(self.__population):
                current_ant_path = [START_POINT_VALUE]
                # loop
                while len(current_ant_path) != len(self.__list_kpi_unit):
                    reachable_point = self.get_list_available_next_point(
                        startPoint=current_ant_path[-1], currentAntPath=current_ant_path)
                    best_next_point = self.get_best_next_node(
                        current_ant_path[-1], reachable_point)
                    current_ant_path.append(best_next_point)

                current_ant_length = self.calculate_len(current_ant_path)
                current_gen_path[current_ant_length] = current_ant_path

            self.update_local_pheromone()

            self.__best_path_length = max(current_gen_path.keys())
            self.__best_path = current_gen_path[self.__best_path_length]

            self.update_global_pheromone()

        print(self.__best_path, self.__best_path_length)


aco = AntSystemOptimization(10, 10)
aco.run()
