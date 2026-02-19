from graph.yen_ksp import yen_k_shortest_paths
from model.route import Route


def generate_candidate_routes(
    graph,
    num_nodes,
    min_len,
    max_len,
    K=50,
    max_routes_per_pair=3,
):
    """
    Генерирует кандидатные маршруты,
    удовлетворяющие ограничениям по длине
    """

    candidates = []

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            paths = yen_k_shortest_paths(graph, i, j, K=K)

            for _, path in paths[:max_routes_per_pair]:
                if min_len <= len(path) <= max_len:
                    candidates.append(Route(path))

    return candidates
