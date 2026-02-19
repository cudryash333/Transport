from data.loader import load_graph, load_demand_matrix
from icrsgp.pipeline import icrsgp
from algorithms.nsga2 import nsga2
from algorithms.nsga2 import non_dominated_sort


def test_stage6_nsga2():
    # === Параметры Mandl ===
    NUM_NODES = 15
    NUM_ROUTES = 4
    MIN_LEN = 2
    MAX_LEN = 8

    POP_SIZE = 20
    GENERATIONS = 20

    # === Загрузка данных ===
    graph = load_graph("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_links.txt", NUM_NODES)
    demand = load_demand_matrix("D:/Telegram Desktop/Traffic_flow_modeling/data/mandl/mandl2_demand.txt", NUM_NODES)

    # === Начальная популяция (ICRSGP) ===
    initial_route_sets = [
        icrsgp(
            graph,
            num_nodes=NUM_NODES,
            num_routes=NUM_ROUTES,
            min_len=MIN_LEN,
            max_len=MAX_LEN,
        )
        for _ in range(POP_SIZE)
    ]

    # === Запуск NSGA-II ===
    final_population = nsga2(
        initial_route_sets,
        graph,
        demand,
        min_len=MIN_LEN,
        max_len=MAX_LEN,
        population_size=POP_SIZE,
        generations=GENERATIONS,
    )

    # === Проверка 1: размер популяции ===
    assert len(final_population) == POP_SIZE

    # === Проверка 2: допустимость решений ===
    for ind in final_population:
        covered = ind.route_set.covered_nodes()
        assert len(covered) == NUM_NODES

        for r in ind.route_set.routes:
            assert MIN_LEN <= len(r.nodes) <= MAX_LEN

    # === Парето-фронт ===
    fronts = non_dominated_sort(final_population)
    pareto = fronts[0]

    print("\n=== PARETO FRONT ===")
    for ind in pareto:
        print(f"ATT={ind.att:.2f}, TRT={ind.trt:.2f}")

    # === Проверка 3: фронт не пуст ===
    assert len(pareto) >= 2

    # === Проверка 4: есть компромисс ===
    atts = [ind.att for ind in pareto]
    trts = [ind.trt for ind in pareto]

    assert min(atts) < max(atts)
    assert min(trts) < max(trts)

    # === Проверка 5: лучшие значения разумны ===
    assert min(atts) > 0
    assert min(trts) > 0

    print("\nNSGA-II TEST PASSED ✔")


if __name__ == "__main__":
    test_stage6_nsga2()
