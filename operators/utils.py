def route_length(route, graph):
    total = 0.0
    for u, v in zip(route.nodes[:-1], route.nodes[1:]):
        for x, w in graph.neighbors(u):
            if x == v:
                total += w
                break
    return total
