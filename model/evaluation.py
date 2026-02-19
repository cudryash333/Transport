import math
from graph.dijkstra import dijkstra
from model.route_graph import build_route_graph
from collections import deque


TRANSFER_PENALTY = 5.0


def routes_covering_edge(route_set, u, v):
    count = 0
    for r in route_set.routes:
        for x, y in zip(r.nodes[:-1], r.nodes[1:]):
            if (x == u and y == v) or (x == v and y == u):
                count += 1
                break
    return count


def estimate_transfers(route_set, path):
    """
    Оценка числа пересадок вдоль пути
    (упрощённо, но корректно по статье)
    """
    used_routes = set()

    for u, v in zip(path[:-1], path[1:]):
        for idx, r in enumerate(route_set.routes):
            for x, y in zip(r.nodes[:-1], r.nodes[1:]):
                if (x == u and y == v) or (x == v and y == u):
                    used_routes.add(idx)
                    break

    if not used_routes:
        return 0

    return max(0, len(used_routes) - 1)


def shortest_path_on_routes(route_set, graph, origin, destination):
    """
    Ищет кратчайший путь между origin и destination
    ТОЛЬКО по рёбрам, входящим в маршруты
    Возвращает длину пути или None
    """

    # строим допустимые рёбра
    allowed_edges = set()

    for route in route_set.routes:
        nodes = route.nodes
        for i in range(len(nodes) - 1):
            u, v = nodes[i], nodes[i + 1]
            allowed_edges.add((u, v))
            allowed_edges.add((v, u))  # граф неориентированный

    # BFS (веса = 1 или длины рёбер)
    visited = set()
    queue = deque([(origin, 0)])

    while queue:
        node, dist = queue.popleft()

        if node == destination:
            return dist

        if node in visited:
            continue

        visited.add(node)

        for neigh, w in graph.neighbors(node):
            if (node, neigh) in allowed_edges:
                queue.append((neigh, dist + w))

    return None


BIG_M = 1e6  # штраф за недостижимую OD-пару

def compute_att(route_set, graph, demand_matrix):
    total_time = 0.0
    total_demand = 0.0

    n = len(demand_matrix)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            demand = demand_matrix[i][j]
            if demand <= 0:
                continue

            total_demand += demand

            path_len = shortest_path_on_routes(
                route_set, graph, i, j
            )

            if path_len is None:
                total_time += demand * BIG_M
            else:
                total_time += demand * path_len

    if total_demand == 0:
        raise ValueError("Total demand is zero")

    return total_time / total_demand



def compute_trt(route_set, base_graph):
    """
    Total Route Time (TRT)
    """

    total = 0.0

    for route in route_set.routes:
        for u, v in zip(route.nodes[:-1], route.nodes[1:]):
            for x, w in base_graph.neighbors(u):
                if x == v:
                    total += w
                    break

    return total


def evaluate_solution(route_set, graph, demand_matrix):
    att = compute_att(route_set, graph, demand_matrix)
    trt = compute_trt(route_set, graph)
    return att, trt
