from KPI import get_kpi_weight_matrix, get_list_KPI_unit, get_list_KPI_env_score, get_list_KPI_human_score, get_index_by_kpi_id_in_file, KPIUnit
from Human import get_list_human
import random
import numpy
from decimal import Decimal, getcontext

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


class AntSystemOptimization:
    __slots__ = ("__weight_matrix", "__kpi_unit", "__kpi_env_score", "__human_ability_score", "__kpi_human_score", "__pheromone_tao_matrix",
                 "__population", "__generation", "__beta", "__ro", "__best_path", "__best_path_length", "__default_pheromone_tao_matrix")

    def __init__(self, generation: int, population: int, beta: int = 2, ro: float = 0.4) -> None:
        self.__kpi_unit = get_list_KPI_unit()
        print(self.__kpi_unit)


aco = AntSystemOptimization(2,5)

