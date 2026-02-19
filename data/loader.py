import numpy as np
from graph.graph import TransportGraph


def load_graph(edge_file: str, num_nodes: int) -> TransportGraph:
    graph = TransportGraph(num_nodes)

    with open(edge_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            u, v, w = line.split(',')
            graph.add_edge(int(u)-1, int(v)-1, float(w)-1)

    return graph


def load_demand_matrix(demand_file: str, num_nodes: int) -> np.ndarray:
    D = np.zeros((num_nodes, num_nodes))

    with open(demand_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            i, j, d = line.split(',')
            D[int(i), int(j)] = float(d)

    return D
