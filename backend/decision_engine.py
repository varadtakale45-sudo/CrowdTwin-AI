def recommendations(stadium):
    notes=[]
    for n in stadium.nodes.values():
        if n["blocked"]: notes.append({"level":"critical","message":f"{n['id']} is blocked; calculate an alternative route."})
        elif n["predicted_density"] >= .85: notes.append({"level":"critical","message":f"High predicted congestion at {n['id']}."})
        elif n["density"] >= .72: notes.append({"level":"warning","message":f"Monitor {n['id']}; current density is {n['density']:.0%}."})
    return notes or [{"level":"normal","message":"No threshold-based intervention is currently indicated."}]

