from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Dict
from database import fetch_data
from utils import prepare_vehicle_daily_summary

app = FastAPI()
model = joblib.load("model/xgb_model.pkl")

class PredictionOutput(BaseModel):
    vehicleid: int
    date: str
    status: str
    probabilities: Dict[str, float]
    recommendation: str

def generate_recommendation(status: str) -> str:
    if status == "Critical":
        return "Immediate inspection required. Battery performance is severely degraded."
    elif status == "Warning":
        return "Monitor closely. Schedule maintenance within the next few days."
    elif status == "Healthy":
        return "Battery is in good condition. No action needed."
    return "Unknown status."

@app.get("/predict", response_model=list[PredictionOutput])
def predict():
    raw_df = fetch_data()
    daily_df = prepare_vehicle_daily_summary(raw_df)

    vehicle_ids = daily_df["vehicleid"]
    dates = daily_df["date"]
    features = daily_df.drop(columns=["vehicleid", "date"])

    probs = model.predict_proba(features)
    preds = probs.argmax(axis=1)
    statuses = ["Critical", "Warning", "Healthy"]

    output = [
        {
            "vehicleid": int(vid),
            "date": str(d),
            "status": statuses[int(p)],
            "probabilities": {
                statuses[i]: round(float(prob), 4) for i, prob in enumerate(prob_dist)
            },
            "recommendation": generate_recommendation(statuses[int(p)])
        }
        for vid, d, p, prob_dist in zip(vehicle_ids, dates, preds, probs)
    ]
    return output