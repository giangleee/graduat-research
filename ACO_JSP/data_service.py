from typing import List, Dict, Union
from models import Environments, KpiOutput, Equipment, KpiCondition, Employees
from numpy import array


class DataService:
    def __init__(self) -> None:
        pass

    def calculate_mean_effect_point(environmentsEffect: List[Environments], kpiOutputsEffect: List[KpiOutput], equipmentsEffect: List[Equipment]) -> List[Dict[str, Union[int, float]]]:
        all_factors = environmentsEffect + kpiOutputsEffect + equipmentsEffect
        kpi_points = {}
        kpi_counts = {}

        # Accumulate points for each kpi_id
        for factor in all_factors:
            for effect_point in factor.effect_point:
                kpi_id = effect_point.kpi_id
                point = effect_point.point
                kpi_points.setdefault(kpi_id, 0)
                kpi_points[kpi_id] += point
                kpi_counts.setdefault(kpi_id, 0)
                kpi_counts[kpi_id] += 1

        # Calculate mean points for each kpi_id
        mean_points = [{"kpi_id": kpi_id, "mean_point": kpi_points[kpi_id] /
                        kpi_counts[kpi_id]} for kpi_id in kpi_points]

        return mean_points

    def calculate_mean_product_output_point(kpiOutputsEffect: List[KpiOutput]) -> List[Dict[str, Union[int, float]]]:
        kpi_points = {}
        kpi_counts = {}

        # Accumulate points for each kpi_id
        for factor in kpiOutputsEffect:
            for effect_point in factor.effect_point:
                kpi_id = effect_point.kpi_id
                point = effect_point.point
                kpi_points.setdefault(kpi_id, 0)
                kpi_points[kpi_id] += point
                kpi_counts.setdefault(kpi_id, 0)
                kpi_counts[kpi_id] += 1

        # Calculate mean points for each kpi_id
        mean_points = [{"kpi_id": kpi_id, "mean_point": kpi_points[kpi_id] /
                        kpi_counts[kpi_id]} for kpi_id in kpi_points]

        return mean_points

    def calculate_sum_employees_point(listEmployees: List[Employees]) -> float:

        # Calculate the sum of point values
        total_points = sum(employee.point for employee in listEmployees)

        return total_points

    def generate_matrix(kpiCondition: List[KpiCondition], value: float, mean_effect_point) -> array:
        point: int = len(kpiCondition)

        def get_mean_point_base_kpi_id(kpi_id):
           data_dict = {item['kpi_id']: item['mean_point']
                        for item in mean_effect_point}

           mean_point = data_dict.get(kpi_id)
           return mean_point

        data = [[0.0 for _ in range(point + 2)] for _ in range(point + 2)]

        for row in range(point + 2):
            if (row == point + 1):
                for col in range(point + 2):
                    data[row][col] = 0.0
                break
            else:
                for col in range(point + 2):
                    if (row == 0.0 and col == point + 1):
                        data[row][col] = 0.0
                    elif (row == 0.0 and col != 0.0):
                        data[row][col] = value
                    elif (col != 0.0 and col != row):
                        if (col == point + 1):
                            data[row][col] = value

        # Adjust loop ranges to avoid unnecessary boundary checks
        for col in range(1, point + 1):
            for row in range(1, point + 1):
                if row in kpiCondition[col - 1].pre_condition or col in kpiCondition[row - 1].post_condition:
                    data[row][col] = value

        for row in range(1, point + 1):
            for col in range(1, point + 1):
                data[row][col] *= get_mean_point_base_kpi_id(col)

        return array(data)
