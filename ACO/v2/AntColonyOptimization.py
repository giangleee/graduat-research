"""
AntColonyOptimization
Mô hình Ant Colony Optimization giải bài toán TSP
"""

import numpy

class AntColonyOptimization:
    __number_dimension: int
    __size_population: int
    __max_iterations: int
    __alpha: int
    __beta: int
    __rho: float
    __matrix: numpy.ndarray[int]
    __pheromone_matrix: numpy.ndarray[int]
    __prob_matrix_distance: numpy.ndarray[float]
    __goal_function: any
    __generation_best_X: list
    __generation_best_Y: list

    def __init__(self, number_dimension: int, distance_matrix: numpy.ndarray[float], goal_function: any, size_population: int = 200, max_iterations: int = 50, alpha: int = 1, beta: int = 2, rho: float = 0.1):
        self.__number_dimension = number_dimension
        self.__size_population = size_population
        self.__max_iterations = max_iterations
        self.__goal_function = goal_function

        # pheromone control parameters
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho

        # generate matrix
        self.__matrix = numpy.zeros(
            (self.__size_population, self.__number_dimension)).astype(int)  # Dòng này khởi tạo ma trận đường đi của kiến trúc Table với toàn bộ là 0 và đặt kiểu dữ liệu thành số nguyên.
        self.__pheromone_matrix = numpy.ones(
            (self.__number_dimension, self.__number_dimension)).astype(int)
        # ma trận nghịch đảo của ma trận khoảng cách
        self.__prob_matrix_distance = 1 / \
            (distance_matrix + 1e-10 * numpy.eye(number_dimension, number_dimension))

        # Record the best solutions for each generation
        self.__generation_best_X, self.__generation_best_Y = [], []

    def update_pheromone_matrix(self, current_y: numpy.ndarray[float]):
        delta_tau = numpy.zeros((self.__number_dimension, self.__number_dimension))

        for people in range(self.__size_population):
            for dimention in range(self.__number_dimension - 1):
                first_point, second_point = self.__matrix[people, dimention], self.__matrix[people, dimention + 1]
                delta_tau[first_point, second_point] += 1 / current_y[people]

            first_point, second_point = self.__matrix[people, self.__number_dimension - 1], self.__matrix[people, 0]
            delta_tau[first_point, second_point] += 1 / current_y[people]

        self.__pheromone_matrix = (1 - self.__rho) * self.__pheromone_matrix + delta_tau


    def execute(self, max_iterations: int = 0):
        # handle update max iterations
        self.__max_iterations = max_iterations or self.__max_iterations

        for _ in range(self.__max_iterations):
            # công thức tính ma trận nghịch đảo (bội số alpha beta)
            prob_matrix = (self.__pheromone_matrix ** self.__alpha) * \
                (self.__prob_matrix_distance) ** self.__beta

            for people in range(self.__size_population):
                # Start point
                self.__matrix[people, 0] = 0

                for dimension in range(self.__number_dimension - 1):
                    # save current visited town
                    taboo_set = set(self.__matrix[people, :dimension + 1])
                    # rest of it
                    allow_visit_list = list(
                        set(range(self.__number_dimension)) - taboo_set)

                    prob = prob_matrix[self.__matrix[people,
                                                     dimension], allow_visit_list]
                    prob = prob / prob.sum()

                    # choose next point base prob
                    next_point = numpy.random.choice(
                        allow_visit_list, size=1, p=prob)
                    self.__matrix[people, dimension + 1] = next_point

            current_y = numpy.array([self.__goal_function(element)
                                    for element in self.__matrix])

            best_index = current_y.argmin()
            best_x, best_y = self.__matrix[best_index, :].copy(
            ), current_y[best_index].copy()
            self.__generation_best_X.append(best_x)
            self.__generation_best_Y.append(best_y)

            self.update_pheromone_matrix(current_y=current_y)


        best_generation = numpy.array(self.__generation_best_Y).argmin()
        return self.__generation_best_X[best_generation], self.__generation_best_Y[best_generation]

    fit = execute
