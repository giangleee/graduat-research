class Graph:
    # define attribute
    _current_depth: int
    _topology: list[dict]

    def __init__(self, current_depth = 0) -> None:
        self._current_depth = current_depth
        self._topology = []

    # getter methods
    @property
    def current_depth(self) -> int:
        return self._current_depth

    @property
    def topology(self) -> dict:
        return self._topology

    # setter methods
    @current_depth.setter
    def current_depth(self, value: int) -> None:
        self._current_depth = value

    # Build topology base depth
    @topology.setter
    def topology(self, depth) -> None:
        while depth > (len(self._topology) - 1):
            self._topology.append({})

    # Method

    # Get node in topology base depth
    def get_node_in_topology(self, depth) -> dict:
        return self._topology[depth]

    # Set node value into topology
    def set_node_in_topology(self, depth, node) -> None:
        self._topology[depth].setdefault(node.name, node)
