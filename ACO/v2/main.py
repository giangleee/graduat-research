# from AntColonyOptimization import AntColonyOptimization
import numpy
from scipy import spatial
from AntColonyOptimization import AntColonyOptimization
from matplotlib import pyplot
import pandas

# generate number dimention
number_dimention: int = 50
# chứa toạ độ các điểm từ number_dimention
points_coordinate = numpy.random.rand(number_dimention, 2)
# distance_matrix, là một ma trận vuông trong đó distance_matrix[i, j] biểu thị khoảng cách Euclidean giữa điểm thứ i và j trong mảng points_coordinate.
distance_matrix = spatial.distance.cdist(
    points_coordinate, points_coordinate, metric='euclidean')

# optimize function

def calculateTotalDistance(routine):
    number_dimention, = routine.shape
    return sum([distance_matrix[routine[dimention % number_dimention], routine[(
        dimention + 1) % number_dimention]] for dimention in range(number_dimention)])


aco: AntColonyOptimization = AntColonyOptimization(
    number_dimension=number_dimention, distance_matrix=distance_matrix, goal_function=calculateTotalDistance)
# print(aco.execute())
best_x, best_y = aco.execute()

# plot
fig, ax = pyplot.subplots(1, 2)
best_x_convert_to_circle = numpy.concatenate([best_x, [best_x[0]]])
best_x_with_location = points_coordinate[best_x_convert_to_circle, :]
print(best_x_convert_to_circle)
ax[0].plot(best_x_with_location[:, 0], best_x_with_location[:, 1], 'o-r')
pandas.DataFrame(
    aco._AntColonyOptimization__generation_best_Y).cummin().plot(ax=ax[1])
pyplot.show()

# print(best_points_coordinate)
