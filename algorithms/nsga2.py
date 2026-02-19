from model.evaluation import evaluate_solution
import random
from copy import deepcopy
from operators.grow_trim_control import cost_based_grow_trim
from operators.grow import grow_route
from operators.trim import trim_route
from algorithms.hyperheuristic import mutate_with_hh
from algorithms.hyperheuristic import HyperHeuristic


#Описываем одного кандидата решения
class Individual:
    def __init__(self, route_set):
        self.route_set = route_set
        self.att = None
        self.trt = None

        # NSGA-II attributes
        self.rank = None
        self.crowding_distance = 0.0

    def objectives(self):
        return self.att, self.trt


def evaluate_individual(ind, graph, demand):
    if ind.att is None or ind.trt is None:
        ind.att, ind.trt = evaluate_solution(
            ind.route_set, graph, demand
        )


#Определяем, какое решение доминирует
def dominates(a, b):
    """
    a dominates b if:
    - no worse in all objectives
    - strictly better in at least one
    """
    return (
        a.att <= b.att
        and a.trt <= b.trt
        and (a.att < b.att or a.trt < b.trt)
    )


#Разбивает популяцию на уровни
def non_dominated_sort(population):
    fronts = []
    S = {}
    n = {}

    front = []

    for p in population:
        S[p] = []
        n[p] = 0
        for q in population:
            if dominates(p, q):
                S[p].append(q)
            elif dominates(q, p):
                n[p] += 1

        if n[p] == 0:
            p.rank = 0
            front.append(p)

    fronts.append(front)
    i = 0

    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    q.rank = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    return fronts[:-1]


#
def compute_crowding_distance(front):
    if not front:
        return

    for ind in front:
        ind.crowding_distance = 0.0

    num_obj = 2

    for m in range(num_obj):
        if m == 0:
            front.sort(key=lambda x: x.att)
        else:
            front.sort(key=lambda x: x.trt)

        front[0].crowding_distance = float("inf")
        front[-1].crowding_distance = float("inf")

        min_val = front[0].objectives()[m]
        max_val = front[-1].objectives()[m]

        if max_val == min_val:
            continue

        for i in range(1, len(front) - 1):
            prev_val = front[i - 1].objectives()[m]
            next_val = front[i + 1].objectives()[m]
            front[i].crowding_distance += (
                next_val - prev_val
            ) / (max_val - min_val)



def tournament_selection(population, k=2):
    contenders = random.sample(population, k)
    contenders.sort(
        key=lambda x: (x.rank, -x.crowding_distance)
    )
    return contenders[0]




def mutate(
    parent,
    graph,
    demand,
    min_len,
    max_len,
):
    child = deepcopy(parent.route_set)

    if random.random() < 0.5:
        child = grow_route(
            child,
            graph,
            demand,
            max_len,
        )
    else:
        child = trim_route(
            child,
            graph,
            demand,
            min_len,
        )

    return child


def nsga2(
    initial_route_sets,
    graph,
    demand,
    min_len,
    max_len,
    population_size=20,
    generations=30,
):
    # === инициализация ===
    population = [
        Individual(rs) for rs in initial_route_sets
    ]

    for ind in population:
        evaluate_individual(ind, graph, demand)

    # === эволюция ===
    for gen in range(generations):
        offspring = []

        while len(offspring) < population_size:
            parent = tournament_selection(population)
            #child_routes = mutate(parent, graph, demand, min_len, max_len)
            hh = HyperHeuristic(
                graph,
                demand,
                min_len,
                max_len,
            )
            child_routes = mutate_with_hh(parent, hh)
            child = Individual(child_routes)
            evaluate_individual(child, graph, demand)
            offspring.append(child)

        # объединение
        combined = population + offspring
        fronts = non_dominated_sort(combined)

        new_population = []

        for front in fronts:
            compute_crowding_distance(front)
            if len(new_population) + len(front) <= population_size:
                new_population.extend(front)
            else:
                front.sort(
                    key=lambda x: -x.crowding_distance
                )
                remaining = population_size - len(new_population)
                new_population.extend(front[:remaining])
                break

        population = new_population

        print(
            f"Gen {gen}: "
            f"best ATT={min(i.att for i in population):.2f}, "
            f"best TRT={min(i.trt for i in population):.2f}"
        )

    return population

