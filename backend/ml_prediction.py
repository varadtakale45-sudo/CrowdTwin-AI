from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from backend.preprocessing import load_dataset, training_data


class DensityPredictor:
    def __init__(self, path=None):
        self.frame = load_dataset(path); self.models, self.metrics = {}, {}
        for horizon in (1, 3, 5): self._train(horizon)

    def _train(self, horizon):
        x, y, features = training_data(self.frame, horizon)
        split = max(1, int(len(x)*.8)); split = min(split, len(x)-1) if len(x)>1 else 1
        x_train, x_test, y_train, y_test = x.iloc[:split], x.iloc[split:], y.iloc[:split], y.iloc[split:]
        model = RandomForestRegressor(n_estimators=80, max_depth=7, random_state=42, n_jobs=1).fit(x_train, y_train)
        if len(x_test):
            pred = model.predict(x_test); self.metrics[horizon] = {"mae": float(mean_absolute_error(y_test,pred)), "rmse": float(mean_squared_error(y_test,pred)**.5), "r2": float(r2_score(y_test,pred)) if len(y_test)>1 else 0.0}
        else: self.metrics[horizon] = {"mae": 0.0, "rmse": 0.0, "r2": 0.0}
        self.models[horizon] = (model, features)

    def predict(self, stadium, horizon):
        if horizon not in self.models: raise ValueError("Prediction horizon must be 1, 3, or 5 minutes")
        model, features = self.models[horizon]; results=[]
        for node in stadium.nodes.values():
            row = {"density": node["density"], "previous_density": node["density"], "net_flow": node["inflow"]-node["outflow"],
                   "capacity": node["capacity"], "queue_length": node["queue"], "inflow": node["inflow"], "outflow": node["outflow"], "minute": 720}
            sample = pd.DataFrame([[row[f] for f in features]], columns=features)
            value = float(np.clip(model.predict(sample)[0], 0, 1.25))
            node["predicted_density"] = round(value, 4)
            results.append({"zone": node["id"], "current_density": node["density"], f"predicted_{horizon}m": round(value,4)})
        return results
