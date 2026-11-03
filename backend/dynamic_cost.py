DEFAULT_WEIGHTS = {"distance": 1.0, "congestion": 12.0, "waiting": 3.0, "risk": 18.0}


def edge_cost(edge, nodes, strategy="prediction", weights=None):
    if edge.get("blocked") or nodes[edge["source"]].get("blocked") or nodes[edge["target"]].get("blocked"):
        return float("inf")
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    if strategy == "static":
        return edge["distance"]
    key = "density" if strategy == "reactive" else "predicted_density"
    congestion = (nodes[edge["source"]][key] + nodes[edge["target"]][key]) / 2
    return (w["distance"] * edge["distance"] + w["congestion"] * congestion +
            w["waiting"] * edge["waiting_time"] + w["risk"] * edge["risk"])

