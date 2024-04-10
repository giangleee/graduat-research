from multiprocessing import cpu_count
from object import ObjectiveFunction
from multiprocessing import Pool, Event
from datetime import datetime
from collections import namedtuple
from core import HarmonySearch

terminating = Event()

HarmonySearchResults = namedtuple('HarmonySearchResults',
                                  ['elapsed_time', 'best_harmony', 'best_fitness', 'harmony_memories'])


def harmony_search(objective_function, num_processes, num_iterations):
    pool = Pool(num_processes)
    try:
        start = datetime.now()
        pool_results = [pool.apply_async(worker, args=(objective_function,)) for _ in
                        range(num_iterations)]
        pool.close()
        pool.join()
        end = datetime.now()
        elapsed_time = end - start

        # find best harmony from all iterations
        best_harmony = None
        best_fitness = float('-inf') if objective_function.get_is_maximize() else float('+inf')
        harmony_memories = list()
        for result in pool_results:
            harmony, fitness, harmony_memory = result.get()
            if (objective_function.get_is_maximize() and fitness > best_fitness) or (
                    not objective_function.get_is_maximize() and fitness < best_fitness):
                best_harmony = harmony
                best_fitness = fitness
            harmony_memories.append(harmony_memory)

        return HarmonySearchResults(elapsed_time=elapsed_time, best_harmony=best_harmony, best_fitness=best_fitness,
                                    harmony_memories=harmony_memories)
    except KeyboardInterrupt:
        pool.terminate()
        raise


def worker(objective_function):
    try:
        if not terminating.is_set():
            hs = HarmonySearch(objective_function)
            return hs.run()
    except KeyboardInterrupt:
        terminating.set()
        raise


if __name__ == '__main__':
    obj_fun = ObjectiveFunction()
    num_processes = cpu_count() - 1
    num_iterations = num_processes
    results = harmony_search(obj_fun, num_processes, num_iterations)
    print('Elapsed time: {}\nBest harmony: {}\nBest fitness: {}'.format(results.elapsed_time, results.best_harmony,
                                                                        results.best_fitness))
