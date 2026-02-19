from typing import Dict, List, Tuple


class TransportGraph:
    """
    Взвешенный граф транспортной сети.
    Узлы — остановки
    Рёбра — дороги с временем в минутах
    """

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.adj: Dict[int, List[Tuple[int, float]]] = {
            i: [] for i in range(num_nodes)
        }

    def add_edge(self, u: int, v: int, weight: float, bidirectional: bool = True):
        self.adj[u].append((v, weight))
        if bidirectional:
            self.adj[v].append((u, weight))

    def neighbors(self, u: int):
        return self.adj[u]

    def __repr__(self):
        return f"TransportGraph(nodes={self.num_nodes})"
