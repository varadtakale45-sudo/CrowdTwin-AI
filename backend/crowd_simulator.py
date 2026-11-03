import random
from backend.data_structures import CircularQueue, LinkedList, Stack


class CrowdSimulator:
    def __init__(self, stadium):
        self.stadium, self.running, self.tick = stadium, False, 0
        self.history, self.movements, self.checkpoints = Stack(), LinkedList(), CircularQueue(24)
        self.initial = stadium.clone()
        self.transfers = []

    def start(self): self.running = True; return self.step()
    def pause(self): self.running = False; return self.status()
    def reset(self):
        self.stadium.nodes, self.stadium.edges = self.initial.clone().nodes, self.initial.clone().edges
        self.running, self.tick = False, 0
        return self.status()

    def step(self):
        self.history.push({k: v["crowd"] for k, v in self.stadium.nodes.items()})
        self.transfers = []
        for edge in self.stadium.edges:
            a, b = self.stadium.nodes[edge['source']], self.stadium.nodes[edge['target']]
            if edge['blocked'] or a['blocked'] or b['blocked']: continue
            source, target = (a, b) if a['density'] > b['density'] else (b, a)
            amount = min(source['crowd'], max(0, int((source['density']-target['density'])*18)))
            if amount:
                source['crowd'] -= amount; target['crowd'] += amount
                self.transfers.append({'source':source['id'],'target':target['id'],'count':amount})
        ids = list(self.stadium.nodes)
        for i, node_id in enumerate(ids):
            node = self.stadium.nodes[node_id]
            variation = random.randint(-10, 14) + node["inflow"] - node["outflow"]
            node["crowd"] += variation
            self.movements.append((self.tick, node_id, variation)); self.checkpoints.enqueue(node_id)
        self.tick += 1; self.stadium.refresh()
        return self.status()

    def adjust(self, amount):
        zones = [n for n in self.stadium.nodes.values() if n["kind"] == "zone"]
        each = int(amount / len(zones))
        for node in zones: node["crowd"] += each
        self.stadium.refresh(); return self.status()

    def status(self):
        nodes = list(self.stadium.nodes.values())
        return {"running": self.running, "tick": self.tick, "crowd": sum(n["crowd"] for n in nodes),
                "active_zones": sum(n["crowd"] > 0 for n in nodes),
                "average_density": round(sum(n["density"] for n in nodes)/len(nodes), 4),
                "maximum_density": max(n["density"] for n in nodes), "queue_length": sum(n["queue"] for n in nodes)}
