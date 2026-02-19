class Route:
    """
    Один маршрут (последовательность вершин)
    """

    def __init__(self, nodes):
        self.nodes = list(nodes)

    @property
    def length(self):
        return len(self.nodes)

    def terminals(self):
        return self.nodes[0], self.nodes[-1]

    def contains(self, node):
        return node in self.nodes

    def __repr__(self):
        return f"Route({self.nodes})"
