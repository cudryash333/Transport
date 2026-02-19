from operators.grow import grow_route
from operators.trim import trim_route

def cost_based_grow_trim(
    route_set,
    graph,
    demand_matrix,
    min_len,
    max_len,
    iterations=10,
):
    """
    Последовательно применяет grow и trim
    """

    current = route_set

    for _ in range(iterations):
        grown = grow_route(
            current,
            graph,
            demand_matrix,
            max_len,
        )

        trimmed = trim_route(
            grown,
            graph,
            demand_matrix,
            min_len,
        )

        current = trimmed

    return current
