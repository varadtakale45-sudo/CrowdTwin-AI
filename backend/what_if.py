from backend.routing import shortest_path
from backend.evaluation import crowd_metrics


def simulate(stadium, scenario, source="G1", destination="E2", amount=500, element_id=None, predictor=None):
    twin=stadium.clone()
    if scenario in {"block_corridor","block_gate","close_exit"}:
        if not element_id: raise ValueError("element_id is required for a blocking scenario")
        twin.set_blocked(element_id,True)
    elif scenario in {"increase_crowd","increase_density"}:
        targets=[n for n in twin.nodes.values() if n["kind"]=="zone"]
        for n in targets: n["crowd"] += int(amount/len(targets))
    elif scenario == "emergency":
        for n in twin.nodes.values(): n["outflow"] = int(n["outflow"]*1.5)
    else: raise ValueError("Unsupported what-if scenario")
    twin.refresh()
    if predictor is not None:
        predictor.predict(twin, 3)
    if scenario == "emergency":
        candidates=[]
        for node in twin.nodes.values():
            if node["kind"] == "exit" and not node["blocked"] and node["id"] != source:
                try: candidates.append(shortest_path(twin,source,node["id"],"prediction","dijkstra"))
                except ValueError: pass
        if not candidates: raise ValueError("No reachable evacuation exit is available")
        route=min(candidates,key=lambda item:item["travel_time"])
    else:
        route=shortest_path(twin,source,destination,"prediction","dijkstra")
    affected=[n["id"] for n in twin.nodes.values() if n["blocked"] or n["density"]>=.8]
    result = crowd_metrics(twin,route)
    result['blocked_edges'] = result['reroutes']
    try:
        baseline_route = shortest_path(stadium,source,route['path'][-1],'prediction','dijkstra')
        result['reroutes'] = int(baseline_route['path'] != route['path'])
    except ValueError:
        result['reroutes'] = 0
    return {"scenario":scenario,"route":route,"affected_zones":affected,**result}
