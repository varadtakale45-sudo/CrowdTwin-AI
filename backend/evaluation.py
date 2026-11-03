from backend.routing import shortest_path
from backend.searching_sorting import benchmark


def crowd_metrics(stadium, route=None):
    nodes=list(stadium.nodes.values()); route=route or {}
    return {"average_travel_time": route.get("travel_time",0), "maximum_density": max(n["density"] for n in nodes),
            "congestion_events": sum(n["density"] >= .8 for n in nodes), "queue_length": sum(n["queue"] for n in nodes),
            "evacuation_time": round(sum(n["crowd"] for n in nodes)/max(1,sum(n["capacity"] for n in nodes if n["kind"]=="exit"))*60,2),
            "route_computation_time": route.get("computation_ms",0), "throughput": sum(n["outflow"] for n in nodes),
            "reroutes": sum(e["blocked"] for e in stadium.edges)}


def compare_strategies(stadium, source="G1", destination="E2"):
    rows=[]
    for strategy in ("static","reactive","prediction"):
        try:
            route=shortest_path(stadium,source,destination,strategy,"dijkstra"); rows.append({"strategy":strategy,**route,**crowd_metrics(stadium,route)})
        except ValueError as exc: rows.append({"strategy":strategy,"error":str(exc)})
    return rows


def dsa_benchmark(stadium):
    return benchmark([int(n["density"]*1000) for n in stadium.nodes.values()]*30)

