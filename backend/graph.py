from collections import defaultdict
from backend.dynamic_cost import edge_cost


def adjacency(stadium, strategy="prediction", weights=None):
    graph = defaultdict(list)
    for edge in stadium.edges:
        cost = edge_cost(edge, stadium.nodes, strategy, weights)
        if cost != float("inf"):
            graph[edge["source"]].append((edge["target"], cost))
            graph[edge["target"]].append((edge["source"], cost))
    return graph

