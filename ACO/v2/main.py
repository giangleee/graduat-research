# from AntColonyOptimization import AntColonyOptimization
import time
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


def run_and_measure(func, num_runs=1, *args, **kwargs):
    """
    Run a function multiple times and measure the execution time for each run.

    Parameters:
    - func: The function to be executed.
    - num_runs: The number of times to run the function.
    - *args: Positional arguments to be passed to the function.
    - **kwargs: Keyword arguments to be passed to the function.

    Returns:
    - execution_times: A list containing the execution time for each run.
    """
    execution_times = []

    for _ in range(num_runs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

    return execution_times


# Assuming you have an instance of AntColonyOptimization named ant_colony_optimization
num_runs = 5  # Set the desired number of runs
execution_times = run_and_measure(
    aco.execute, num_runs, max_iterations=100)

for i, time_taken in enumerate(execution_times, start=1):
    print(f"Run {i}: Execution Time - {time_taken} seconds")


best_x, best_y = aco.execute()

# plot
fig, ax = pyplot.subplots(1, 2)
best_x_convert_to_circle = numpy.concatenate([best_x, [best_x[0]]])
best_x_with_location = points_coordinate[best_x_convert_to_circle, :]
ax[0].plot(best_x_with_location[:, 0], best_x_with_location[:, 1], 'o-r')
pandas.DataFrame(
    aco._AntColonyOptimization__generation_best_time).cummin().plot(ax=ax[1])
pyplot.show()
