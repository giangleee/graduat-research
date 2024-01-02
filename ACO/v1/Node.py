from dataclasses import dataclass

@dataclass
class Node():
    # define attribute
    _name: str
    # _neighbors: list[dict]
    # # _is_expanded: bool

    # getter
    @property
    def name(self) -> str:
        return self._name

    @property
    def neighbors(self) -> list[dict]:
        return self._neighbors

    # setter
    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @neighbors.setter
    def neighbors(self, value: list[dict]) -> None:
        self._neighbors = value



node = Node("hello")
print(node._name)
