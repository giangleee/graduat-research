from abc import ABC, abstractmethod
from typing import List, Dict


class AntColonyInterfaceOperation(ABC):
    @abstractmethod
    def calculate_length(self, path: List[str]) -> float:
        pass

    @abstractmethod
    def update_pheromone_intensity(self, list_current_gen_path: List[Dict[str, List[str] | float]]) -> None:
        pass

    @abstractmethod
    def update_pheromone_evaporation(self) -> None:
        pass

    @abstractmethod
    def get_eta_value(self, start_point: str, end_point: str) -> float:
        pass

    @abstractmethod
    def get_list_available_next_note(self, start_point: str, list_visited_point: List[str]) -> List[str]:
        pass

    @abstractmethod
    def calculate_equation_value(self, start_point: str, next_point: str) -> float:
        pass

    @abstractmethod
    def get_best_next_point(self, start_point: str, list_reachable_point: List[str]) -> str:
        pass
