from typing import List, Dict
from numpy import ndarray, array, zeros_like

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


def get_matrix_data(filename: str = './sample.csv') -> ndarray:
    matrix: ndarray = array([])

    # with open(filename, newline='') as csvFile:
    #     csv_reader = reader(csvFile, delimiter=',')
    #     next(csv_reader, None)
    #     for index, row in enumerate(csv_reader):
    #         row_values = [float(value) for value in row[1:]]
    #         matrix.append(row_values)

    var = [
        [0.00, 0.69, 0.56, 0.79, 0.74, 0.24, 0.25, 0.75, 0.42, 0.79, 0.21, 0.86, 0.97, 0.1, 0.02, 0.36, 0.38, 0.8, 0.33,
         0.51, 0.35, 0.00],
        [0.00, 0.0, 0.37, 0.25, 0.47, 0.3, 0.44, 0.99, 0.64, 0.59, 0.61, 0.79, 0.97, 0.99, 0.65, 0.77, 0.02, 0.27, 0.9,
         0.23, 0.46, 0.76],
        [0.00, 0.49, 0.00, 0.14, 0.28, 0.41, 0.97, 0.79, 0.45, 0.79, 0.62, 0.04, 0.16, 0.88, 0.85, 0.26, 0.83, 0.08,
         0.27,
         0.81, 0.56, 0.95],
        [0.00, 0.75, 0.29, 0.0, 0.32, 0.02, 0.22, 0.37, 0.05, 0.82, 0.31, 0.61, 0.7, 0.42, 0.63, 0.75, 0.13, 0.44, 0.38,
         0.71, 0.15, 0.8],
        [0.00, 0.32, 0.74, 0.21, 0.0, 0.49, 0.42, 0.7, 0.46, 0.66, 0.55, 0.59, 0.12, 0.24, 0.73, 0.38, 0.2, 0.64, 0.66,
         0.65, 0.42, 0.74],
        [0.00, 0.44, 0.39, 0.4, 0.55, 0.0, 0.58, 0.41, 0.6, 0.58, 0.9, 0.34, 0.14, 0.14, 0.86, 0.56, 0.75, 0.19, 0.32,
         0.91, 0.55, 0.36],
        [0.00, 0.84, 0.77, 0.91, 0.57, 0.17, 0.0, 0.19, 0.63, 0.4, 0.78, 0.1, 0.63, 0.53, 0.36, 0.69, 0.96, 0.45, 0.69,
         0.05, 0.45, 0.46],
        [0.00, 0.79, 0.18, 0.94, 0.91, 0.13, 0.49, 0.0, 0.91, 0.91, 0.8, 0.29, 0.24, 0.96, 0.97, 0.33, 0.37, 0.07, 0.58,
         0.47, 0.25, 0.93],
        [0.00, 0.93, 0.41, 0.3, 0.95, 0.64, 0.22, 0.9, 0.0, 0.49, 0.92, 0.27, 0.02, 0.14, 0.98, 0.06, 0.08, 0.95, 0.81,
         1.0, 0.24, 0.48],
        [0.00, 0.69, 0.74, 0.39, 0.1, 0.28, 0.69, 0.57, 0.74, 0.0, 0.06, 0.34, 0.77, 0.6, 0.7, 0.71, 0.6, 0.81, 0.65,
         0.03, 0.91, 0.91],
        [0.00, 0.66, 0.5, 0.58, 0.01, 0.85, 0.71, 0.79, 0.27, 0.47, 0.0, 0.69, 0.8, 0.21, 0.33, 0.26, 0.91, 0.54, 0.14,
         0.71, 0.11, 0.79],
        [0.00, 0.42, 0.8, 0.61, 0.04, 0.28, 0.63, 0.88, 0.81, 0.82, 0.72, 0.0, 0.23, 0.03, 0.97, 0.07, 0.03, 0.58, 0.53,
         0.14, 0.88, 0.57],
        [0.00, 0.95, 0.71, 0.59, 0.39, 0.9, 0.95, 0.18, 0.75, 0.1, 0.75, 0.4, 0.0, 0.68, 0.98, 0.98, 0.1, 0.37, 0.96,
         0.72, 0.07, 0.33],
        [0.00, 0.2, 0.44, 0.96, 0.39, 0.43, 0.86, 0.14, 0.45, 0.7, 0.71, 0.19, 0.75, 0.0, 0.3, 0.77, 0.79, 0.42, 0.26,
         0.67, 0.26, 0.83],
        [0.00, 0.84, 0.03, 0.53, 0.73, 0.06, 0.59, 0.58, 0.05, 0.48, 0.36, 0.37, 0.56, 0.26, 0.0, 0.15, 0.91, 0.42,
         0.99,
         0.34, 0.11, 0.42],
        [0.00, 0.37, 0.48, 0.04, 0.73, 0.35, 0.35, 0.74, 0.72, 0.34, 0.16, 0.01, 0.57, 0.78, 0.45, 0.0, 0.71, 0.56,
         0.47,
         0.37, 0.56, 0.39],
        [0.00, 0.14, 0.86, 0.29, 0.06, 0.99, 0.62, 0.94, 0.28, 0.87, 0.22, 0.11, 0.89, 0.08, 0.12, 0.83, 0.0, 0.8, 0.73,
         0.45, 0.36, 0.01],
        [0.00, 0.52, 0.41, 0.19, 0.99, 0.69, 0.62, 0.91, 0.88, 0.6, 0.67, 0.79, 0.44, 0.73, 0.37, 0.28, 0.92, 0.0, 0.25,
         0.82, 0.42, 0.49],
        [0.00, 0.98, 0.86, 0.13, 0.38, 0.07, 0.12, 0.03, 0.21, 0.53, 0.99, 0.25, 0.21, 0.7, 0.2, 0.27, 0.96, 0.28, 0.0,
         0.55, 0.44, 0.75],
        [0.00, 0.79, 0.83, 0.85, 0.4, 0.7, 0.43, 0.04, 0.77, 0.9, 0.29, 0.35, 0.26, 0.72, 0.1, 0.21, 0.76, 0.11, 0.22,
         0.0, 0.39, 0.94],
        [0.00, 0.96, 0.95, 0.21, 0.62, 0.41, 0.52, 0.21, 0.62, 0.61, 0.08, 0.37, 0.98, 0.21, 0.13, 0.09, 0.29, 0.08,
         0.35, 0.22, 0.0, 0.81],
        [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
         0.00,
         0.00, 0.00, 0.00]]
    return array(var)


def get_index_base_name_point(matrix: ndarray, name_point: str) -> int:
    if name_point == START_POINT_VALUE:
        return 0

    if name_point == FINISH_POINT_VALUE:
        return len(matrix[0]) - 1

    return int(name_point)


def get_name_point_base_index(matrix: ndarray, index: int) -> str:
    if index == 0:
        return START_POINT_VALUE

    if len(matrix[0]) - 1 == index:
        return FINISH_POINT_VALUE

    return str(index)


def calculate_sum_each_path_base_ant(list_current_gen_path: List[Dict[str, List[str] | float]],
                                     start_point: str, end_point: str) -> float:
    return sum(1 / item['length'] for item in list_current_gen_path
               for index, path_item in enumerate(item['path'][:-1])
               if path_item == start_point and item['path'][index + 1] == end_point)


def calculate_elite_value(list_current_gen_path: List[Dict[str, List[str] | float]], start_point: str,
                          end_point: str, number_elite_ant) -> float:
    total: float = 0
    smallest_length_item = min(list_current_gen_path, key=lambda x: x['length'])

    for index, path_item in enumerate(smallest_length_item['path']):
        if index + 1 < len(smallest_length_item['path']):
            if start_point == path_item and end_point == smallest_length_item['path'][index + 1]:
                total += 1 / smallest_length_item['length']

    return total * number_elite_ant


def generate_pheromone_matrix(matrix: ndarray) -> ndarray:
    binary_matrix: ndarray = zeros_like(matrix, dtype=int)

    for i, row in enumerate(matrix):
        binary_matrix[i] = [1 if item > 0 else 0 for item in row]

    return binary_matrix
