from graph.graph import TransportGraph


def build_route_graph(
    base_graph: TransportGraph,
    route_set,
) -> TransportGraph:
    """
    Строит подграф, состоящий только из рёбер,
    используемых маршрутами
    """

    g = TransportGraph(base_graph.num_nodes)

    for route in route_set.routes:
        nodes = route.nodes
        for u, v in zip(nodes[:-1], nodes[1:]):
            # находим вес ребра в исходном графе
            for x, w in base_graph.neighbors(u):
                if x == v:
                    g.add_edge(u, v, w, bidirectional=True)
                    break

    return g
