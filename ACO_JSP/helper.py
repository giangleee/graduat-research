from typing import List, Dict
from numpy import ndarray, array, zeros_like
from csv import reader

# define const
START_POINT_VALUE = 'start'
FINISH_POINT_VALUE = 'finish'


def get_matrix_data(filename: str = './test_data/3jobs3ops.csv') -> array:


    # with open(filename, newline='') as csvFile:
    #     csv_reader = reader(csvFile, delimiter=',')
    #     data = [[float(element) for element in row] for row in csv_reader]
    #
    # return array(data)
    data = [
        [0.0, 0.175177305, 0.1819148936, 0.1684397163,
            0.165070922, 0.1603546099, 0.0],
        [0.0, 0.0, 0.1819148936, 0.1684397163, 0.165070922, 0.1603546099, 0.0],
        [0.0, 0.175177305, 0.0, 0.1684397163, 0.165070922, 0.1603546099, 0.0],
        [0.0, 0.175177305, 0.1819148936, 0.0, 0.165070922, 0.1603546099, 0.0],
        [0.0, 0.175177305, 0.1819148936, 0.1684397163, 0.0, 0.1603546099, 0.0],
        [0.0, 0.175177305, 0.1819148936, 0.1684397163, 0.165070922, 0.0, 0.0],
    ]
    return array(data)


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
    smallest_length_item = max(list_current_gen_path, key=lambda x: x['length'])

    for index, path_item in enumerate(smallest_length_item['path']):
        if index + 1 < len(smallest_length_item['path']):
            if start_point == path_item and end_point == smallest_length_item['path'][index + 1]:
                total += 1 / smallest_length_item['length']

    return total * number_elite_ant


def generate_pheromone_matrix(matrix: ndarray) -> ndarray:
    binary_matrix = zeros_like(matrix, dtype=float)

    for i, row in enumerate(matrix):
        binary_matrix[i] = [0.1 if item > 0 else 0.0 for item in row]

    return binary_matrix

