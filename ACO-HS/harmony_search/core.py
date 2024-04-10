import random
from object import ObjectiveFunction
from typing import List, Optional, Any, Union


class HarmonySearch(object):
    # __slots__ = ['__objective_function', '__harmony_memory']

    def __init__(self, objective_function: ObjectiveFunction) -> None:
        self.__object_function = objective_function
        self.__harmony_memory = list()
        # fill harmony_memory using random parameter values by default, but with initial_harmonies if provided
        self.__initialize__harmony_memory()

    def __initialize__harmony_memory(self) -> None:
        initial_harmonies = list()
        for _ in range(0, self.__object_function.get_hms()):
            harmony = list()
            for _ in range(0, self.__object_function.get_number_parameters()):
                self.__random_selection(harmony)
            initial_harmonies.append(harmony)

        for i in range(0, self.__object_function.get_hms()):
            fitness = self.__object_function.get_fitness(initial_harmonies[i])
            self.__harmony_memory.append((initial_harmonies[i], fitness))

    def __random_selection(self, harmony: List) -> None:
        harmony.append(self.__object_function.get_value())

    def __memory_consideration(self, harmony: List, candidate: int) -> None:
        memory_index = random.randint(0, self.__object_function.get_hms() - 1)
        harmony.append(self.__harmony_memory[memory_index][0][candidate])

    def __pitch_adjustment(self, harmony: List, candidate: int):
        # continuous variable
        if random.random() < 0.5:
            # adjust pitch down
            harmony[candidate] -= ((harmony[candidate] - self.__object_function.get_lower_bound()) * random.random()
                                   * self.__object_function.get_bw())
        else:
            # adjust pitch up
            harmony[candidate] += (self.__object_function.get_upper_bound() - harmony[
                candidate]) * random.random() * self.__object_function.get_bw()

    def __update_harmony_memory(self, considered_harmony: List, considered_fitness: float) -> None:
        if (considered_harmony, considered_fitness) not in self.__harmony_memory:
            worst_index = None
            worst_fitness = float('+inf') if self.__object_function.get_is_maximize() else float('-inf')
            for i, (_, fitness) in enumerate(self.__harmony_memory):
                if (self.__object_function.get_is_maximize() and fitness < worst_fitness) or (
                        not self.__object_function.get_is_maximize() and fitness > worst_fitness):
                    worst_index = i
                    worst_fitness = fitness
            if (self.__object_function.get_is_maximize() and considered_fitness > worst_fitness) or (
                    not self.__object_function.get_is_maximize() and considered_fitness < worst_fitness):
                self.__harmony_memory[worst_index] = (considered_harmony, considered_fitness)

    def run(self) -> tuple[Optional[Any], Union[float, Any], list[Any]]:
        for _ in range(self.__object_function.get_max_improvisations()):
            # generate new harmony
            harmony = list()
            for parameter in range(0, self.__object_function.get_number_parameters()):
                if random.random() < self.__object_function.get_hmcr():
                    self.__memory_consideration(harmony, parameter)
                    if random.random() < self.__object_function.get_par():
                        self.__pitch_adjustment(harmony, parameter)
                else:
                    self.__random_selection(harmony)
            fitness = self.__object_function.get_fitness(harmony)
            self.__update_harmony_memory(harmony, fitness)

        # return best harmony
        best_harmony = None
        best_fitness = float('-inf') if self.__object_function.get_is_maximize() else float('+inf')
        for harmony, fitness in self.__harmony_memory:
            if (self.__object_function.get_is_maximize() and fitness > best_fitness) or (
                    not self.__object_function.get_is_maximize() and fitness < best_fitness):
                best_harmony = harmony
                best_fitness = fitness
        return best_harmony, best_fitness, self.__harmony_memory
