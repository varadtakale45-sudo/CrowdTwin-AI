from copy import deepcopy
from math import cos, sin, tau


class Stadium:
    """Mutable digital-twin state for a compact, reproducible stadium graph."""

    def __init__(self):
        names = ["G1", "Z1", "C1", "Z2", "E1", "G2", "Z3", "C2", "Z4", "E2", "X1", "X2"]
        kinds = ["gate", "zone", "corridor", "zone", "exit", "gate", "zone", "corridor", "zone", "exit", "checkpoint", "checkpoint"]
        self.nodes = {}
        for i, (name, kind) in enumerate(zip(names, kinds)):
            angle = tau * i / len(names)
            cap = 1100 if kind == "zone" else (800 if kind in {"gate", "exit"} else 550)
            count = [260, 690, 210, 540, 90, 300, 720, 250, 610, 80, 150, 120][i]
            self.nodes[name] = {
                "id": name, "kind": kind, "capacity": cap, "crowd": count,
                "density": round(count / cap, 4), "predicted_density": round(count / cap, 4),
                "queue": max(0, count - int(cap * .62)), "inflow": 20 + i % 5 * 4,
                "outflow": 16 + i % 4 * 5, "x": round(cos(angle) * 18, 2),
                "y": 0, "z": round(sin(angle) * 13, 2), "blocked": False,
            }
        pairs = [(names[i], names[(i + 1) % len(names)]) for i in range(len(names))]
        pairs += [("G1", "X1"), ("X1", "C2"), ("G2", "X2"), ("X2", "C1"), ("Z1", "Z3"), ("Z2", "Z4")]
        for gate_index in range(3, 9):
            angle = tau * (gate_index - 1) / 8
            gate_id = f'G{gate_index}'
            self.nodes[gate_id] = {'id': gate_id, 'kind': 'gate', 'capacity': 800,
                'crowd': 120, 'density': .15, 'predicted_density': .15, 'queue': 0,
                'inflow': 24, 'outflow': 20, 'x': round(cos(angle)*18, 2),
                'y': 0, 'z': round(sin(angle)*13, 2), 'blocked': False}
            pairs.append((gate_id, ['C1', 'C2', 'X1', 'X2'][gate_index % 4]))
        for gate_index in range(1, 9):
            angle = tau * (gate_index - 1) / 8
            self.nodes[f'G{gate_index}']['x'] = round(cos(angle)*18, 2)
            self.nodes[f'G{gate_index}']['z'] = round(sin(angle)*13, 2)
        self.edges = []
        for a, b in pairs:
            na, nb = self.nodes[a], self.nodes[b]
            distance = round(((na["x"]-nb["x"])**2 + (na["z"]-nb["z"])**2) ** .5, 2)
            self.edges.append({"source": a, "target": b, "distance": distance, "capacity": 500,
                               "waiting_time": 0, "risk": .05, "blocked": False})

    def refresh(self):
        for node in self.nodes.values():
            node["crowd"] = max(0, min(node["crowd"], int(node["capacity"] * 1.25)))
            node["density"] = round(node["crowd"] / node["capacity"], 4)
            node["queue"] = max(0, node["crowd"] - int(node["capacity"] * .62))
        for edge in self.edges:
            density = (self.nodes[edge["source"]]["density"] + self.nodes[edge["target"]]["density"]) / 2
            edge["waiting_time"] = round(max(0, density - .55) * 7, 3)
            edge["risk"] = round(.05 + max(0, density - .7) * 1.5, 3)

    def snapshot(self):
        self.refresh()
        return {"nodes": list(self.nodes.values()), "edges": deepcopy(self.edges)}

    def clone(self):
        return deepcopy(self)

    def set_blocked(self, element_id, blocked=True):
        if element_id not in self.nodes:
            raise ValueError(f"Unknown stadium element: {element_id}")
        self.nodes[element_id]["blocked"] = blocked
        for edge in self.edges:
            if element_id in (edge["source"], edge["target"]):
                edge["blocked"] = blocked
        return self.nodes[element_id]
