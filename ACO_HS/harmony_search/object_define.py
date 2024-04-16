from random import uniform, random
from torch import rand, tensor, sum, round, abs
from typing import List


class ObjectiveFunction(object):

    def __init__(self):
        self._lower_bounds = 0
        self._upper_bounds = 0.2
        self._number_parameters = 20

        # define all input parameters
        self._is_maximize = False  # minimize
        self._max_improvisations = 500  # maximum number of improvisations
        self._hms = 100  # harmony memory size
        self._hmcr = 1 - 1/ self._number_parameters  # harmony memory considering rate
        self._par = 0.5  # pitch adjusting rate
        self._bw = 0.5

        # define random number as weight of employee
        self.test_weight_employees = rand(20)

    def get_fitness(self, vector) -> float:
        tensor_vector = tensor(vector).clone().detach()
        weighted_sum = sum(self.test_weight_employees * tensor_vector)
        fitness = 1000 * abs(weighted_sum - 1)
        return fitness.item()

    def get_value(self):
        return uniform(self._lower_bounds, self._upper_bounds)

    def get_lower_bound(self):
        return self._lower_bounds

    def get_upper_bound(self):
        return self._upper_bounds

    def get_number_parameters(self):
        return self._number_parameters

    def use_random_seed(self):
        return False

    def get_max_improvisations(self):
        return self._max_improvisations

    def get_hmcr(self):
        return self._hmcr

    def get_par(self):
        return self._par

    def get_hms(self):
        return self._hms

    def get_bw(self):
        return self._bw

    def get_is_maximize(self):
        return self._is_maximize
