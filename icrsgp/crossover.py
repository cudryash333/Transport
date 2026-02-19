from model.route_set import RouteSet


def coverage_gain(route, covered):
    return len(set(route.nodes) - covered)


def icrsgp_crossover(
    candidates,
    num_routes,
    #num_nodes,
    max_len,
):
    """
    Coverage-based crossover с учётом max_len
    """

    selected = []
    covered = set()
    remaining = candidates.copy()

    while len(selected) < num_routes and remaining:
        # сортировка по покрытию
        remaining.sort(
            key=lambda r: coverage_gain(r, covered),
            reverse=True,
        )

        chosen = None
        for r in remaining:
            if r.length <= max_len:
                chosen = r
                break

        if chosen is None:
            break

        selected.append(chosen)
        covered.update(chosen.nodes)
        remaining.remove(chosen)

    return RouteSet(selected)
