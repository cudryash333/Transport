import random
from data.loader import load_graph, load_demand_matrix
from icrsgp.pipeline import icrsgp
from algorithms.nsga2 import nsga2
from algorithms.nsga2 import non_dominated_sort


def run_nsga2_experiment(seed=0):
    random.seed(seed)

    NUM_NODES = 15
    NUM_ROUTES = 4
    MIN_LEN = 2
    MAX_LEN = 8

    POP_SIZE = 400
    GENERATIONS = 2000

    graph = load_graph("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_links.txt", NUM_NODES)
    demand = load_demand_matrix("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_demand.txt", NUM_NODES)

    initial = [
        icrsgp(graph, NUM_NODES, NUM_ROUTES, MIN_LEN, MAX_LEN)
        for _ in range(POP_SIZE)
    ]

    population = nsga2(
        initial,
        graph,
        demand,
        MIN_LEN,
        MAX_LEN,
        population_size=POP_SIZE,
        generations=GENERATIONS,
    )

    pareto = non_dominated_sort(population)[0]

    return [(ind.att, ind.trt) for ind in pareto]


if __name__ == "__main__":
    res = run_nsga2_experiment()
    print(res)
