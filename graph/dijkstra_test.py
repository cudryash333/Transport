from data.loader import load_graph, load_demand_matrix
from graph.dijkstra import dijkstra

NUM_NODES = 15  # Mandl

graph = load_graph("/Users/ds_ba/PycharmProjects/Taffic_flow_modeling/data/edges.txt", NUM_NODES)
D = load_demand_matrix("/Users/ds_ba/PycharmProjects/Taffic_flow_modeling/data/demand.txt", NUM_NODES)

dist = dijkstra(graph, source=1)

print("Distances from node 0:")
for i, d in enumerate(dist):
    print(f"0 -> {i}: {d}")