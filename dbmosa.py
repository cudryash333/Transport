import math
import random
from copy import deepcopy
from model.evaluation import evaluate_solution


def dominates_obj(a, b):
    """
    a, b — кортежи (att, trt)
    """
    return (
        a[0] <= b[0]
        and a[1] <= b[1]
        and (a[0] < b[0] or a[1] < b[1])
    )



class DBMOSA:
    def __init__(
        self,
        graph,
        demand,
        hyperheuristic,
        initial_temp=0.1,
        cooling_rate=0.97,
        iterations=500,
    ):
        self.graph = graph
        self.demand = demand
        self.hh = hyperheuristic

        self.T = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations = iterations

    def acceptance_probability(self, curr, cand):
        att_x, trt_x = curr
        att_y, trt_y = cand

        delta = max(
            (att_y - att_x) / att_x,
            (trt_y - trt_x) / trt_x,
        )

        return math.exp(-delta / self.T)

    def run(self, initial_route_set, pareto_archive):
        current = deepcopy(initial_route_set)
        curr_att, curr_trt = evaluate_solution(
            current, self.graph, self.demand
        )

        pareto_archive.update(current, curr_att, curr_trt)

        for it in range(self.iterations):
            candidate = self.hh.step(current)
            cand_att, cand_trt = evaluate_solution(
                candidate, self.graph, self.demand
            )

            accepted = False

            if dominates_obj(
                (cand_att, cand_trt),
                (curr_att, curr_trt),
            ):
                accepted = True

            elif dominates_obj(
                (curr_att, curr_trt),
                (cand_att, cand_trt),
            ):
                if random.random() < self.acceptance_probability(
                    (curr_att, curr_trt),
                    (cand_att, cand_trt),
                ):
                    accepted = True

            else:
                # недоминируемые
                if random.random() < self.acceptance_probability(
                    (curr_att, curr_trt),
                    (cand_att, cand_trt),
                ):
                    accepted = True

            if accepted:
                current = candidate
                curr_att, curr_trt = cand_att, cand_trt
                pareto_archive.update(
                    current, curr_att, curr_trt
                )

            # охлаждение
            if (it + 1) % 20 == 0:
                self.T *= self.cooling_rate

        return pareto_archive
