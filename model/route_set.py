class RouteSet:
    """
    Набор маршрутов (решение UTRP)
    """

    def __init__(self, routes):
        self.routes = list(routes)

    def covered_nodes(self):
        covered = set()
        for r in self.routes:
            covered.update(r.nodes)
        return covered

    def is_feasible(self, num_nodes, min_len, max_len):
        if not all(min_len <= r.length <= max_len for r in self.routes):
            return False
        return len(self.covered_nodes()) == num_nodes

    def __repr__(self):
        return f"RouteSet({len(self.routes)} routes)"
