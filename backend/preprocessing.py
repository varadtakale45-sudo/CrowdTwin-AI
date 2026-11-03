from pathlib import Path
import pandas as pd


REQUIRED = ["timestamp", "zone_id", "crowd_count", "capacity", "density", "inflow", "outflow", "queue_length", "gate_status"]


def load_dataset(path=None):
    path = Path(path or Path(__file__).parents[1] / "data" / "crowd_data.csv")
    if not path.exists(): raise ValueError("Crowd dataset is missing")
    frame = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in frame.columns]
    if missing: raise ValueError(f"Dataset missing columns: {', '.join(missing)}")
    frame = frame.dropna(subset=["zone_id", "crowd_count", "capacity"]).copy()
    numeric = ["crowd_count", "capacity", "density", "inflow", "outflow", "queue_length"]
    frame[numeric] = frame[numeric].apply(pd.to_numeric, errors="coerce").fillna(0)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    frame["minute"] = frame["timestamp"].dt.hour.fillna(0)*60 + frame["timestamp"].dt.minute.fillna(0)
    frame["net_flow"] = frame["inflow"] - frame["outflow"]
    return frame


def training_data(frame, horizon):
    data = frame.sort_values(["zone_id", "timestamp"]).copy()
    data["previous_density"] = data.groupby("zone_id")["density"].shift(1).fillna(data["density"])
    data["target"] = data.groupby("zone_id")["density"].shift(-horizon)
    data = data.dropna(subset=["target"])
    features = ["density", "previous_density", "net_flow", "capacity", "queue_length", "inflow", "outflow", "minute"]
    if data.empty: raise ValueError("Dataset is too small for the prediction horizon")
    return data[features], data["target"], features

