import random
from fastapi import FastAPI, Request
from typing import List
from data_service import DataService
from models import KpiRequest, KpiCondition, Employees, Environments, KpiOutput, Equipment
from aco_core import AntColonyForJSP
from collections import defaultdict

app = FastAPI()


@app.get("/")
async def root(request: Request):
    data = await request.json()
    return data


@app.post("/core")
async def get_core_response(listKpi: List[KpiRequest], kpiCondition: List[KpiCondition], listEmployees: List[Employees], environmentsEffect: List[Environments], kpiOutputsEffect: List[KpiOutput], equipmentsEffect: List[Equipment]):
    data_service = DataService
    mean_effect_point = data_service.calculate_mean_effect_point(
        environmentsEffect, kpiOutputsEffect, equipmentsEffect)
    mean_kpi_product_output_point = data_service.calculate_mean_product_output_point(
        kpiOutputsEffect)
    sum_employees_point = data_service.calculate_sum_employees_point(
        listEmployees)

    weight_response = []

    for employee in listEmployees:
        employee_weight = employee.point / sum_employees_point
        default_weight_matrix = data_service.generate_matrix(
            kpiCondition, employee.point, mean_effect_point)
        aco = AntColonyForJSP(
            10, 100, mean_kpi_product_output_point, mean_effect_point, default_weight_matrix)
        result = aco.run()
        kpi_weight = aco.get_each_path_length(result['best_path'])

        for item in listKpi:
            convert_value = {
                "kpi_id": item.id,
                "weights": {
                    "employee_id": employee.id,
                    "weight": kpi_weight[item.id]
                }
            }
            weight_response.append(convert_value)

    grouped_data = defaultdict(list)

    for item in weight_response:
        kpi_id = item['kpi_id']
        weights = item['weights']
        grouped_data[kpi_id].append(weights)

    result = [{'kpi_id': kpi_id, 'weights': weights_list, 'total_weight': sum(employee['weight'] for employee in weights_list)}
              for kpi_id, weights_list in grouped_data.items()]

    return result
