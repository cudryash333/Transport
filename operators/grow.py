import random
from copy import deepcopy
from model.evaluation import evaluate_solution


ACCEPT_WORSE_PROB = 0.1


def grow_route(
    route_set,
    graph,
    demand_matrix,
    max_len,
):
    current_att, current_trt = evaluate_solution(
        route_set, graph, demand_matrix
    )

    candidates = []

    for r_idx, route in enumerate(route_set.routes):
        if route.length >= max_len:
            continue

        for terminal in (route.nodes[0], route.nodes[-1]):
            for v, _ in graph.neighbors(terminal):
                if v in route.nodes:
                    continue

                candidate = deepcopy(route_set)
                r = candidate.routes[r_idx]

                if terminal == r.nodes[0]:
                    r.nodes.insert(0, v)
                else:
                    r.nodes.append(v)

                att, trt = evaluate_solution(
                    candidate, graph, demand_matrix
                )

                candidates.append((candidate, att, trt))

    if not candidates:
        return route_set

    # лучший кандидат
    best = min(candidates, key=lambda x: x[1])

    # === ПРАВИЛО ПРИНЯТИЯ ===
    if best[1] < current_att:
        return best[0]

    if random.random() < ACCEPT_WORSE_PROB:
        return random.choice(candidates)[0]

    return route_set

