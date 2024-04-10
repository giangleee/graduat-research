from typing import List
from numpy import ndarray
from abc import ABC
from helper import generate_pheromone_matrix
from copy import deepcopy


class AntColonyAttribute(ABC):
    __slots__ = ("__weight_matrix", "__population", "__generation", "__alpha", "__beta", "__ro", "__best_path",
                 "__best_path_length", "__default_pheromone_tao_matrix", "__pheromone_tao_matrix", "__number_elite_ant",
                 "__local_ro", "__global_ro")

    __weight_matrix: ndarray
    __population: int
    __generation: int
    __alpha: float
    __beta: float
    __ro: float
    __best_path: List[str]
    __best_path_length: float
    __default_pheromone_tao_matrix: ndarray
    __pheromone_tao_matrix: ndarray
    __number_elite_ant: int
    __local_ro: List
    __global_ro: List

    def __init__(self, population: int, generation: int, local_ro: List, global_ro: List, weight_matrix: ndarray, alpha: float = 0.4, beta: float = 2, ro: float = 0.4,
                 number_elite_ant: int = 20):
        self.__population = population
        self.__generation = generation
        self.__alpha = alpha
        self.__beta = beta
        self.__ro = ro
        self.__weight_matrix = weight_matrix
        self.__default_pheromone_tao_matrix = generate_pheromone_matrix(self.__weight_matrix)
        self.__pheromone_tao_matrix = deepcopy(self.__default_pheromone_tao_matrix)
        self.__best_path = []
        self.__best_path_length = 0
        self.__number_elite_ant = number_elite_ant
        self.__local_ro = local_ro
        self.__global_ro = global_ro

    def get_population(self) -> int:
        return self.__population

    def get_generation(self) -> int:
        return self.__generation

    def get_weight_matrix(self) -> ndarray:
        return self.__weight_matrix

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

    def get_number_elite_ant(self) -> int:
        return self.__number_elite_ant

    def get_local_ro(self, kpi_id: int) -> float:
        for item in self.__local_ro:
            if (item['kpi_id'] == kpi_id):
                return item['mean_point']
            if (kpi_id == len(self.__weight_matrix) - 1 or kpi_id == 0):
                return 0.5

    def get_global_ro(self, kpi_id: int) -> float:
        for item in self.__global_ro:
            if (item['kpi_id'] == kpi_id):
                return item['mean_point']
            if (kpi_id == len(self.__weight_matrix) - 1):
                return 0.5
