import heapq
import math
from typing import List, Tuple, Dict
from graph.graph import TransportGraph
from graph.dijkstra import dijkstra

def dijkstra_path(
    graph: TransportGraph,
    source: int,
    target: int,
    banned_edges: set = None,
    banned_nodes: set = None,
) -> Tuple[float, List[int]]:
    """
    Dijkstra с восстановлением пути и возможностью запрещать рёбра / вершины.
    """

    if banned_edges is None:
        banned_edges = set()
    if banned_nodes is None:
        banned_nodes = set()

    n = graph.num_nodes
    dist = [math.inf] * n
    prev = [None] * n

    dist[source] = 0.0
    pq = [(0.0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        if u == target:
            break

        if current_dist > dist[u]:
            continue

        for v, w in graph.neighbors(u):
            if (u, v) in banned_edges:
                continue
            if v in banned_nodes:
                continue

            alt = current_dist + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    if dist[target] == math.inf:
        return math.inf, []

    # восстановление пути
    path = []
    v = target
    while v is not None:
        path.append(v)
        v = prev[v]
    path.reverse()

    return dist[target], path


def yen_k_shortest_paths(
    graph: TransportGraph,
    source: int,
    target: int,
    K: int = 50,
) -> List[Tuple[float, List[int]]]:
    """
    Yen's K-shortest loopless paths algorithm.
    Возвращает список (length, path).
    """

    # A — найденные кратчайшие пути
    A: List[Tuple[float, List[int]]] = []

    # B — кандидаты
    B: List[Tuple[float, List[int]]] = []

    # 1. Первый кратчайший путь
    dist, path = dijkstra_path(graph, source, target)
    if not path:
        return []

    A.append((dist, path))

    # 2. Итерации
    for k in range(1, K):
        prev_dist, prev_path = A[k - 1]

        for i in range(len(prev_path) - 1):
            spur_node = prev_path[i]
            root_path = prev_path[: i + 1]

            banned_edges = set()
            banned_nodes = set()

            # Запрещаем рёбра, которые создают дубликаты
            for dist_a, path_a in A:
                if len(path_a) > i and path_a[: i + 1] == root_path:
                    u = path_a[i]
                    v = path_a[i + 1]
                    banned_edges.add((u, v))

            # Запрещаем вершины root_path, кроме spur_node
            for node in root_path[:-1]:
                banned_nodes.add(node)

            spur_dist, spur_path = dijkstra_path(
                graph,
                spur_node,
                target,
                banned_edges=banned_edges,
                banned_nodes=banned_nodes,
            )

            if not spur_path:
                continue

            total_path = root_path[:-1] + spur_path
            total_dist = 0.0

            # считаем длину пути
            for u, v in zip(total_path[:-1], total_path[1:]):
                for x, w in graph.neighbors(u):
                    if x == v:
                        total_dist += w
                        break

            candidate = (total_dist, total_path)

            if candidate not in B:
                heapq.heappush(B, candidate)

        if not B:
            break

        # добавляем лучший кандидат
        A.append(heapq.heappop(B))

    return A
