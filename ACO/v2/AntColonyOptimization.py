"""
AntColonyOptimization
Mô hình Ant Colony Optimization giải bài toán TSP
"""
from numpy import ndarray, zeros, ones, eye, random, array
from typing import List, Tuple
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor


class AntColonyOptimization:
    __number_dimension: int
    __size_population: int
    __max_iterations: int
    __alpha: int
    __beta: int
    __rho: float
    __matrix: ndarray[int, int]
    __pheromone_matrix: ndarray[int]
    __prob_matrix_distance: ndarray[float]
    __goal_function: any
    __generation_best_path: list
    __generation_best_time: list

    def __init__(self, number_dimension: int, distance_matrix: ndarray[float], goal_function: any, size_population: int = 200, max_iterations: int = 50, alpha: int = 1, beta: int = 2, rho: float = 0.1):
        self.__number_dimension = number_dimension
        self.__size_population = size_population
        self.__max_iterations = max_iterations
        self.__goal_function = goal_function

        # pheromone control parameters
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho

        # generate matrix
        self.__matrix = zeros(
            (self.__size_population, self.__number_dimension)).astype(int)  # Dòng này khởi tạo ma trận đường đi của kiến trúc Table với toàn bộ là 0 và đặt kiểu dữ liệu thành số nguyên.
        self.__pheromone_matrix = ones(
            (self.__number_dimension, self.__number_dimension)).astype(int)
        # ma trận nghịch đảo của ma trận khoảng cách
        self.__prob_matrix_distance = 1 / \
            (distance_matrix + 1e-10 * eye(number_dimension, number_dimension))

        # Record the best solutions for each generation
        self.__generation_best_path, self.__generation_best_time = [], []

    def update_pheromone_matrix(self, current_y: ndarray[float]):
        delta_tau = zeros(
            (self.__number_dimension, self.__number_dimension))

        for people in range(self.__size_population):
            indices = self.__matrix[people]
            delta_tau[indices[:-1], indices[1:]] += 1 / current_y[people]
            delta_tau[indices[-1], indices[0]] += 1 / current_y[people]

        self.__pheromone_matrix = (1 - self.__rho) * \
            self.__pheromone_matrix + delta_tau

    def build_ant_road_matrix_base_probability(self, people: int, prob_matrix: ndarray[int, int]):
        # Start point
        self.__matrix[people, 0] = 0

        for dimension in range(self.__number_dimension - 1):
            # Save current visited town
            taboo_set = set(self.__matrix[people, :dimension + 1])

            # Rest of it
            allow_visit_list = list(
                set(range(self.__number_dimension)) - taboo_set)

            prob = prob_matrix[self.__matrix[people,
                                             dimension], allow_visit_list]
            prob /= prob.sum()

            # Choose next point based on probability
            next_point = random.choice(allow_visit_list, p=prob)
            self.__matrix[people, dimension + 1] = next_point

    def execute(self, max_iterations: int = 0):
        # handle update max iterations
        self.__max_iterations = max_iterations or self.__max_iterations

        for _ in range(self.__max_iterations):
            # công thức tính ma trận nghịch đảo (bội số alpha beta)
            prob_matrix = (self.__pheromone_matrix ** self.__alpha) * \
                (self.__prob_matrix_distance) ** self.__beta

            for people in range(self.__size_population):
                self.build_ant_road_matrix_base_probability(
                    people=people, prob_matrix=prob_matrix)
            # Xây dựng đường đi kiến trúc của kiến trúc đồng thời
            # parallel_build = partial(
            #     self.build_ant_road_matrix_base_probability, prob_matrix=prob_matrix)
            # with ProcessPoolExecutor() as executor:
            #     executor.map(parallel_build, range(self.__size_population))

            current_y = array([self.__goal_function(element)
                               for element in self.__matrix])

            best_index = current_y.argmin()
            best_x, best_y = self.__matrix[best_index, :].copy(
            ), current_y[best_index].copy()
            self.__generation_best_path.append(best_x)
            self.__generation_best_time.append(best_y)

            self.update_pheromone_matrix(current_y=current_y)

        best_generation = array(self.__generation_best_time).argmin()
        return self.__generation_best_path[best_generation], self.__generation_best_time[best_generation]

    fit = execute
