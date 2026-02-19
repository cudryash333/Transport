import random
from data.loader import load_graph, load_demand_matrix
from icrsgp.pipeline import icrsgp
from algorithms.hyperheuristic import HyperHeuristic
from algorithms.dbmosa import DBMOSA
from algorithms.pareto_archive import ParetoArchive


def run_dbmosa_experiment(seed=0):
    random.seed(seed)

    NUM_NODES = 15
    NUM_ROUTES = 4
    MIN_LEN = 2
    MAX_LEN = 8

    graph = load_graph("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_links.txt", NUM_NODES)
    demand = load_demand_matrix("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_demand.txt", NUM_NODES)

    initial = icrsgp(
        graph, NUM_NODES, NUM_ROUTES, MIN_LEN, MAX_LEN
    )

    hh = HyperHeuristic(
        graph,
        demand,
        MIN_LEN,
        MAX_LEN,
    )

    dbmosa = DBMOSA(
        graph,
        demand,
        hyperheuristic=hh,
        initial_temp=1.0,
        cooling_rate=0.95,
        iterations=800,
    )

    archive = ParetoArchive()
    archive = dbmosa.run(initial, archive)

    return [(att, trt) for _, att, trt in archive.solutions]


if __name__ == "__main__":
    res = run_dbmosa_experiment()
    print(res)
