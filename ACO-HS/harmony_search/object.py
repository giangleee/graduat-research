from random import uniform


class ObjectiveFunction(object):
    # __slots__ = ['_lower_bounds', '_upper_bounds', '_number_parameters',
    #              '_is_maximize', '_max_improvisations', '_hms', '_hmcr', '_par', '_bw']

    def __init__(self):
        # all variables vary in the range [-100, 100]
        self._lower_bounds = -100
        self._upper_bounds = 100
        self._number_parameters = 5

        # define all input parameters
        self._is_maximize = False  # minimize
        self._max_improvisations = 500000  # maximum number of improvisations
        self._hms = 250  # harmony memory size
        self._hmcr = 0.75  # harmony memory considering rate
        self._par = 0.5  # pitch adjusting rate
        # maximum pitch adjustment proportion (new parameter defined in pitch_adjustment()) - used for continuous variables only
        self._bw = 0.5

    def get_fitness(self, vector):
        return abs(vector[0] + 2 * vector[1] + 3 * vector[2] + 2 * vector[3] - 19.968) + abs(-vector[1] + vector[2] + 1.15) + abs(2 * vector[1] - 3 * vector[2] + vector[3] - 4.624) + abs(3 * vector[1] + vector[2] + 2 * vector[3] + vector[4] - 22.312) + abs(2 * vector[3] + vector[4] - 15.882)

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
