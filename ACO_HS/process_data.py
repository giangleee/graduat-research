import json

if __name__ == '__main__':
    output_file = 'output.json'
    weight_file = 'weights.json'

    with open(output_file, 'r') as file:
        # Load JSON data from the file
        output_data = json.load(file)

    with open(weight_file, 'r') as file:
        weight_data = json.load(file)

    for index, item in enumerate(output_data):
        for index_matrix, matrix_item in enumerate(item['matrix']):
            item['matrix'][index_matrix] = matrix_item * weight_data[index_matrix]

    for index, item in enumerate(output_data):
        total = 0
        for index_matrix, matrix_item in enumerate(item['matrix']):
            total += matrix_item

        print(total)
