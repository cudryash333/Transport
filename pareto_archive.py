from algorithms.dbmosa import dominates_obj


class ParetoArchive:
    def __init__(self):
        self.solutions = []

    def update(self, route_set, att, trt):
        new = (route_set, att, trt)

        # если доминируется архивом — отбрасываем
        for _, a, t in self.solutions:
            if dominates_obj((a, t), (att, trt)):
                return

        # удалить решения, которые доминируются новым
        self.solutions = [
            s for s in self.solutions
            if not dominates_obj((att, trt), (s[1], s[2]))
        ]

        self.solutions.append(new)
