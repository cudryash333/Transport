import random
from copy import deepcopy
from model.evaluation import evaluate_solution
from operators.grow import grow_route
from operators.trim import trim_route


class HyperHeuristic:
    def __init__(
        self,
        graph,
        demand,
        min_len,
        max_len,
        alpha=0.2,
        init_weight=1.0,
    ):
        self.graph = graph
        self.demand = demand
        self.min_len = min_len
        self.max_len = max_len

        # learning rate
        self.alpha = alpha

        # LLH weights
        self.weights = {
            "grow": init_weight,
            "trim": init_weight,
        }

    def select_llh(self):
        total = sum(self.weights.values())
        r = random.random() * total

        acc = 0.0
        for llh, w in self.weights.items():
            acc += w
            if r <= acc:
                return llh

        return "grow"

    def apply_llh(self, route_set, llh):
        rs = deepcopy(route_set)

        if llh == "grow":
            return grow_route(
                rs,
                self.graph,
                self.demand,
                self.max_len,
            )

        if llh == "trim":
            return trim_route(
                rs,
                self.graph,
                self.demand,
                self.min_len,
            )

        raise ValueError(llh)

    def update_weight(self, llh, reward):
        """
        reward > 0  → LLH полезна
        reward = 0  → нейтрально
        reward < 0  → вредно
        """
        self.weights[llh] = max(
            0.01,
            (1 - self.alpha) * self.weights[llh]
            + self.alpha * reward
        )

    def step(self, route_set):
        # текущее качество
        att0, trt0 = evaluate_solution(
            route_set, self.graph, self.demand
        )

        llh = self.select_llh()
        new_rs = self.apply_llh(route_set, llh)

        att1, trt1 = evaluate_solution(
            new_rs, self.graph, self.demand
        )

        # === reward (как в статье: improvement-based) ===
        reward = 0.0

        if att1 < att0:
            reward += (att0 - att1) / att0

        if trt1 < trt0:
            reward += (trt0 - trt1) / trt0

        # штраф за ухудшение
        if att1 > att0 and trt1 > trt0:
            reward -= 0.1

        self.update_weight(llh, reward)

        # правило принятия
        if reward > 0 or random.random() < 0.1:
            return new_rs

        return route_set


def mutate_with_hh(parent, hh):
    return hh.step(parent.route_set)