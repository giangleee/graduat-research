import random
from typing import List, Optional, Any, Union, Dict, Tuple
from .object_define import ObjectiveFunction
from t_normal import generate_truncated_normal_samples
from torch import Tensor, tensor


class HarmonySearch(object):
    def __init__(self, objective_function: ObjectiveFunction, harmony_memory: list[tuple[list[Any], Any]] = None)\
            -> None:
        self.__object_function = objective_function
        self.__harmony_memory = harmony_memory

    def set_harmony_memory(self, harmony_memory) -> None:
        self.__harmony_memory = harmony_memory

    def get_harmony_memory(self) -> list[tuple[list[Any], Any]] | None:
        return self.__harmony_memory

    def initialize__harmony_memory(self) -> List[Tuple[Tensor, float]]:
        initial_harmonies = list()
        for _ in range(self.__object_function.get_hms()):
            size = (1, self.__object_function.get_number_parameters())
            harmony = generate_truncated_normal_samples(size)
            initial_harmonies.append(harmony)

        converted_values = []
        for i in range(self.__object_function.get_hms()):
            harmony = initial_harmonies[i].clone().detach()
            fitness = self.__object_function.get_fitness(harmony)
            converted_values.append((harmony, fitness))

        return converted_values

    def random_selection(self, harmony: List) -> None:
        harmony.append(tensor(self.__object_function.get_value()))

    def memory_consideration(self, harmony, candidate: int) -> None:
        memory_index = random.randint(0, self.__object_function.get_hms() - 1)
        harmony.append(self.__harmony_memory[memory_index][0][candidate])

    def pitch_adjustment(self, harmony: List, candidate: int):
        # continuous variable
        if random.random() < 0.5:
            # adjust pitch down
            harmony[candidate] -= tensor(((harmony[candidate]
                                           - self.__object_function.get_lower_bound())
                                          * random.random()
                                          * self.__object_function.get_bw()))
        else:
            # adjust pitch up
            harmony[candidate] += tensor((self.__object_function.get_upper_bound()
                                          - harmony[candidate])
                                         * random.random()
                                         * self.__object_function.get_bw())

    def update_harmony_memory(self, considered_harmony: List, considered_fitness: float,
                              path_solution_candidate: List[Dict], index: int) -> None:
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
                # update new harmony is make total distance of ant change?
                # print(considered_fitness, worst_fitness)
                path_solution_candidate[index]['harmony_memory'][worst_index] = (considered_harmony, considered_fitness)

    def run(self) -> tuple[Optional[Any], Union[float, Any], list[Any]]:
        for _ in range(self.__object_function.get_max_improvisations()):
            # generate new harmony
            harmony = list()
            for parameter in range(0, self.__object_function.get_number_parameters()):
                if random.random() < self.__object_function.get_hmcr():
                    self.memory_consideration(harmony, parameter)
                    if random.random() < self.__object_function.get_par():
                        self.pitch_adjustment(harmony, parameter)
                else:
                    self.random_selection(harmony)
            fitness = self.__object_function.get_fitness(harmony)
            self.update_harmony_memory(harmony, fitness)

        # return best harmony
        best_harmony = None
        best_fitness = float('-inf') if self.__object_function.get_is_maximize() else float('+inf')
        for harmony, fitness in self.__harmony_memory:
            if (self.__object_function.get_is_maximize() and fitness > best_fitness) or (
                    not self.__object_function.get_is_maximize() and fitness < best_fitness):
                best_harmony = harmony
                best_fitness = fitness
        return best_harmony, best_fitness, self.__harmony_memory
