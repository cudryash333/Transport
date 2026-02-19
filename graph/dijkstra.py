import heapq
import math
from typing import List
from graph.graph import TransportGraph


def dijkstra(
    graph: TransportGraph,
    source: int,
) -> List[float]:
    """
    Классический Dijkstra.
    Возвращает расстояния от source до всех вершин.
    """

    n = graph.num_nodes
    dist = [math.inf] * n
    dist[source] = 0.0

    pq = [(0.0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if current_dist > dist[u]:
            continue

        for v, weight in graph.neighbors(u):
            alt = current_dist + weight
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(pq, (alt, v))

    return dist
