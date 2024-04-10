import json
import random

# Generate random point between 0 and 1


def generate_random_point():
    return round(random.uniform(0, 1), 2)


# Generate KPI data
list_kpi = []
for i in range(1, 6):
    kpi = {
        "id": i,
        "name": f"KPI order {i}",
        "value": 1000,
        "symbol": "USD"
    }
    list_kpi.append(kpi)

# Generate KPI condition data
kpi_condition = []
for i in range(1, 6):
    pre_conditions = random.sample(range(1, 6), 2)
    post_conditions = random.sample(range(1, 6), 1)
    condition = {
        "id": i,
        "pre_condition": pre_conditions,
        "post_condition": post_conditions
    }
    kpi_condition.append(condition)

# Generate employee data
list_employees = []
for i in range(1, 6):
    employee = {
        "id": i,
        "name": f"Employee {i}",
        "point": generate_random_point()
    }
    list_employees.append(employee)

# Generate environment effect data
environments_effect = []
for i in range(1, 6):
    effect_point = [{"kpi_id": kpi["id"], "point": generate_random_point()}
                    for kpi in list_kpi]
    environment = {
        "id": i,
        "name": f"Environment factor {i}",
        "effect_point": effect_point
    }
    environments_effect.append(environment)

# Generate KPI outputs effect data
kpi_outputs_effect = []
for i in range(1, 6):
    effect_point = [{"kpi_id": kpi["id"], "point": generate_random_point()}
                    for kpi in list_kpi]
    output_effect = {
        "id": i,
        "name": f"KPI output factor {i}",
        "effect_point": effect_point
    }
    kpi_outputs_effect.append(output_effect)

# Generate equipment effect data
equipments_effect = []
for i in range(1, 6):
    effect_point = [{"kpi_id": kpi["id"], "point": generate_random_point()}
                    for kpi in list_kpi]
    equipment = {
        "id": i,
        "name": f"Equipment factor {i}",
        "effect_point": effect_point
    }
    equipments_effect.append(equipment)

# Construct the JSON object
data = {
    "listKpi": list_kpi,
    "kpiCondition": kpi_condition,
    "listEmployees": list_employees,
    "environmentsEffect": environments_effect,
    "kpiOutputsEffect": kpi_outputs_effect,
    "equipmentsEffect": equipments_effect
}

# Write the JSON data to a file
with open("generated_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Generated data has been saved to generated_data.json")
