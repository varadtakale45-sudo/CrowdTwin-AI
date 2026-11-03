import heapq
import math
import time
from collections import deque
from backend.graph import adjacency


def _validate(stadium, source, destination):
    if source not in stadium.nodes or destination not in stadium.nodes:
        raise ValueError("Source or destination is not a stadium node")
    if stadium.nodes[source]["blocked"] or stadium.nodes[destination]["blocked"]:
        raise ValueError("Source or destination is blocked")


def shortest_path(stadium, source, destination, strategy="prediction", algorithm="dijkstra", weights=None):
    _validate(stadium, source, destination)
    graph = adjacency(stadium, strategy, weights)
    started = time.perf_counter()
    queue = [(0.0, 0.0, source, [source])]
    best = {source: 0.0}
    goal = stadium.nodes[destination]
    while queue:
        score, actual, node, path = heapq.heappop(queue)
        if actual != best.get(node):
            continue
        if node == destination:
            elapsed = (time.perf_counter() - started) * 1000
            densities = [stadium.nodes[n]["predicted_density" if strategy == "prediction" else "density"] for n in path]
            return {"path": path, "total_cost": round(actual, 3), "travel_time": round(actual / 1.35, 3),
                    "nodes": len(path), "edges": len(path)-1, "congestion_exposure": round(sum(densities)/len(densities), 4),
                    "algorithm": algorithm, "strategy": strategy, "computation_ms": round(elapsed, 4)}
        for neighbor, cost in graph[node]:
            candidate = actual + cost
            if candidate < best.get(neighbor, float("inf")):
                best[neighbor] = candidate
                h = 0
                if algorithm.lower() in {"a*", "astar"}:
                    n = stadium.nodes[neighbor]
                    h = math.hypot(n["x"]-goal["x"], n["z"]-goal["z"])
                heapq.heappush(queue, (candidate + h, candidate, neighbor, path + [neighbor]))
    raise ValueError("No route is available between the selected nodes")


def bfs(stadium, source):
    graph, seen, order, q = adjacency(stadium), {source}, [], deque([source])
    while q:
        node = q.popleft(); order.append(node)
        for nxt, _ in graph[node]:
            if nxt not in seen: seen.add(nxt); q.append(nxt)
    return order


def dfs(stadium, source):
    graph, seen, order, stack = adjacency(stadium), set(), [], [source]
    while stack:
        node = stack.pop()
        if node in seen: continue
        seen.add(node); order.append(node); stack.extend(n for n, _ in reversed(graph[node]))
    return order


def floyd_warshall(stadium):
    ids = list(stadium.nodes); dist = {a: {b: (0 if a == b else float("inf")) for b in ids} for a in ids}
    for a, links in adjacency(stadium).items():
        for b, cost in links: dist[a][b] = min(dist[a][b], cost)
    for k in ids:
        for i in ids:
            for j in ids: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
