from data.loader import load_graph, load_demand_matrix
from icrsgp.pipeline import icrsgp
from algorithms.hyperheuristic import HyperHeuristic
from algorithms.dbmosa import DBMOSA
from algorithms.pareto_archive import ParetoArchive


def run_dbmosa():
    NUM_NODES = 15
    NUM_ROUTES = 4
    MIN_LEN = 2
    MAX_LEN = 8

    graph = load_graph("/Users/ds_ba/PycharmProjects/Taffic_flow_modeling/edges.txt", NUM_NODES)
    demand = load_demand_matrix("/Users/ds_ba/PycharmProjects/Taffic_flow_modeling/demand.txt", NUM_NODES)

    initial = icrsgp(
        graph,
        NUM_NODES,
        NUM_ROUTES,
        MIN_LEN,
        MAX_LEN,
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
        iterations=500,
    )

    archive = ParetoArchive()

    archive = dbmosa.run(initial, archive)

    print("\n=== DBMOSA PARETO ARCHIVE ===")
    for _, att, trt in archive.solutions:
        print(f"ATT={att:.2f}, TRT={trt:.2f}")


if __name__ == "__main__":
    run_dbmosa()
