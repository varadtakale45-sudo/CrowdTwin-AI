import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from backend.stadium import Stadium
from backend.crowd_simulator import CrowdSimulator
from backend.ml_prediction import DensityPredictor
from backend.routing import shortest_path, bfs, dfs, floyd_warshall
from backend.what_if import simulate
from backend.evaluation import crowd_metrics, compare_strategies, dsa_benchmark
from backend.decision_engine import recommendations
from backend.database import initialize, save, recent, report_by_id

ROOT=Path(__file__).parents[1]; stadium=Stadium(); simulator=CrowdSimulator(stadium); predictor=None; last_route=None; reroute_count=0


async def simulation_loop():
    while True:
        if simulator.running:
            simulator.step(); save("crowd_states",simulator.status())
        await asyncio.sleep(2)


@asynccontextmanager
async def lifespan(app):
    global predictor
    initialize(); predictor=DensityPredictor(); task=asyncio.create_task(simulation_loop())
    yield
    task.cancel()


app=FastAPI(title="CrowdTwin AI",version="1.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
app.mount("/frontend",StaticFiles(directory=ROOT/"frontend"),name="frontend")
app.mount("/3d",StaticFiles(directory=ROOT/"3d_stadium"),name="3d")


class Adjust(BaseModel): amount:int=Field(ge=-5000,le=5000)
class Predict(BaseModel): horizon:int
class RouteRequest(BaseModel):
    source:str; destination:str; strategy:Literal["static","reactive","prediction"]="prediction"
    algorithm:Literal["dijkstra","astar","a*"]="dijkstra"; weights:Optional[dict]=None
class BlockRequest(BaseModel): element_id:str
class WhatIfRequest(BaseModel):
    scenario:Literal["increase_crowd","increase_density","block_corridor","block_gate","close_exit","emergency"]
    source:str="G1"; destination:str="E2"; amount:int=500; element_id:Optional[str]=None


def guard(fn):
    try: return fn()
    except ValueError as exc: raise HTTPException(400,str(exc))


@app.get("/")
def home(): return FileResponse(ROOT/"frontend"/"index.html")
@app.get("/dashboard.html")
def dashboard_page(): return FileResponse(ROOT/"frontend"/"dashboard.html")
@app.get("/simulation.html")
def simulation_page(): return FileResponse(ROOT/"frontend"/"simulation.html")
@app.get("/api/status")
def status():
    state=simulator.status(); state.update({"prediction_status":"ready" if predictor else "loading","simulation_status":"running" if simulator.running else "paused","routing_strategy":last_route["strategy"] if last_route else "prediction","recommendations":recommendations(stadium)}); return state
@app.get("/api/stadium")
def get_stadium(): return {**stadium.snapshot(), 'tick': simulator.tick, 'running': simulator.running, 'transfers': simulator.transfers}
@app.get("/api/crowd")
def get_crowd(): return list(stadium.nodes.values())
@app.post("/api/simulation/start")
def start(): result=simulator.start(); save("simulation_runs",result); return result
@app.post("/api/simulation/pause")
def pause(): return simulator.pause()
@app.post("/api/simulation/reset")
def reset():
    global last_route, reroute_count
    last_route = None; reroute_count = 0; simulator.transfers = []
    return simulator.reset()
@app.post("/api/crowd/adjust")
def adjust(body:Adjust): return simulator.adjust(body.amount)
@app.post("/api/predict")
def predict(body:Predict):
    result=guard(lambda:predictor.predict(stadium,body.horizon)); save("predictions",{"horizon":body.horizon,"results":result}); return {"horizon":body.horizon,"predictions":result,"metrics":predictor.metrics[body.horizon]}
@app.post("/api/route")
def route(body:RouteRequest):
    global last_route, reroute_count
    algorithm="a*" if body.algorithm in {"astar","a*"} else "dijkstra"
    result=guard(lambda:shortest_path(stadium,body.source,body.destination,body.strategy,algorithm,body.weights))
    if last_route and last_route['path'][0] == body.source and last_route['path'][-1] == body.destination and last_route['path'] != result['path']:
        reroute_count += 1
    last_route=result; save("routes",last_route); return last_route
@app.post("/api/block")
def block(body:BlockRequest): return guard(lambda:stadium.set_blocked(body.element_id,True))
@app.post("/api/unblock")
def unblock(body:BlockRequest): return guard(lambda:stadium.set_blocked(body.element_id,False))
@app.post("/api/what-if")
def whatif(body:WhatIfRequest):
    result=guard(lambda:simulate(stadium,body.scenario,body.source,body.destination,body.amount,body.element_id,predictor)); save("what_if_results",result); return result
@app.get("/api/analytics")
def analytics():
    source = last_route['path'][0] if last_route else 'G1'
    destination = last_route['path'][-1] if last_route else 'E2'
    comparison=compare_strategies(stadium,source,destination)
    metrics={str(k):v for k,v in predictor.metrics.items()}
    crowd = crowd_metrics(stadium,last_route); crowd['blocked_edges'] = crowd['reroutes']; crowd['reroutes'] = reroute_count
    pairs={key:(value if value != float('inf') else None) for key,value in floyd_warshall(stadium)['G1'].items()}
    result={"ml_metrics":metrics,"crowd_metrics":crowd,"strategy_comparison":comparison,"dsa_benchmark":dsa_benchmark(stadium),"traversals":{"bfs":bfs(stadium,"G1"),"dfs":dfs(stadium,"G1")},"all_pairs_sample":pairs}
    save("experiments",result); return result
@app.get("/api/experiments")
def experiments(): return recent("experiments")


@app.post('/api/reports')
def store_report(body: dict):
    if not all(key in body for key in ('status', 'analytics', 'route', 'captured')):
        raise HTTPException(400, 'A captured simulation report is required')
    report_id = save('experiments', {'report': body})
    return {'url': f'/api/reports/{report_id}/export'}


@app.get('/api/reports/{report_id}/export')
def export_report(report_id: int):
    report = report_by_id(report_id)
    if report is None: raise HTTPException(404, 'Report not found')
    return Response(json.dumps(report, indent=2), media_type='application/json',
        headers={'Content-Disposition': f'attachment; filename="CrowdTwin-report-{report_id}.json"'})
