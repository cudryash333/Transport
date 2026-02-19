import random
from copy import deepcopy
from model.evaluation import evaluate_solution


ATT_TOLERANCE = 0.01
ACCEPT_WORSE_PROB = 0.1


def trim_route(
    route_set,
    graph,
    demand_matrix,
    min_len,
):
    current_att, current_trt = evaluate_solution(
        route_set, graph, demand_matrix
    )

    candidates = []

    for r_idx, route in enumerate(route_set.routes):
        if route.length <= min_len:
            continue

        for terminal in ("start", "end"):
            candidate = deepcopy(route_set)
            r = candidate.routes[r_idx]

            removed = r.nodes[0] if terminal == "start" else r.nodes[-1]

            # ⚠️ важно: проверка покрытия (ты уже её добавлял)
            if not any(
                removed in other.nodes
                for i, other in enumerate(route_set.routes)
                if i != r_idx
            ):
                continue

            if terminal == "start":
                r.nodes.pop(0)
            else:
                r.nodes.pop()

            att, trt = evaluate_solution(
                candidate, graph, demand_matrix
            )

            candidates.append((candidate, att, trt))

    if not candidates:
        return route_set

    # лучший по TRT (trim — про TRT)
    best = min(candidates, key=lambda x: x[2])

    # === ПРАВИЛО ПРИНЯТИЯ ===
    if best[2] < current_trt and best[1] <= current_att * (1 + ATT_TOLERANCE):
        return best[0]

    if random.random() < ACCEPT_WORSE_PROB:
        return random.choice(candidates)[0]

    return route_set
