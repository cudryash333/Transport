from icrsgp.candidate_generation import generate_candidate_routes
from icrsgp.crossover import icrsgp_crossover
from icrsgp.repair import repair_route_set


def icrsgp(
    graph,
    num_nodes,
    num_routes,
    min_len,
    max_len,
):
    candidates = generate_candidate_routes(
        graph,
        num_nodes,
        min_len=min_len,
        max_len=max_len,
    )

    route_set = icrsgp_crossover(
        candidates,
        num_routes,
        #num_nodes,
        max_len=max_len,
    )

    route_set = repair_route_set(
        route_set,
        graph,
        num_nodes,
        max_len=max_len,
    )

    return route_set
