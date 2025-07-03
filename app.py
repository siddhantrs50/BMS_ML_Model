from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Dict
from database import fetch_data, engine
from utils import prepare_vehicle_summary
import uuid
from sqlalchemy import text

app = FastAPI()
model = joblib.load("model/xgb_model.pkl")

class PredictionOutput(BaseModel):
    vehicleid: int
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
    summary_df = prepare_vehicle_summary(raw_df)

    vehicle_ids = summary_df["vehicleid"]
    features = summary_df.drop(columns=["vehicleid"])

    probs = model.predict_proba(features)
    preds = probs.argmax(axis=1)
    statuses = ["Critical", "Warning", "Healthy"]

    output = [
        {
            "vehicleid": int(vid),
            "status": statuses[int(p)],
            "probabilities": {
                statuses[i]: round(float(prob), 4) for i, prob in enumerate(prob_dist)
            },
            "recommendation": generate_recommendation(statuses[int(p)])
        }
        for vid, p, prob_dist in zip(vehicle_ids, preds, probs)
    ]

    with engine.connect() as conn:
        for record in output:
            stmt = text("""
                INSERT INTO predictions (prediction_id, vehicle_id, prediction_status, probability, recc)
                VALUES (:id, :vehicle_id, :status, :prob, :recc)
            """)
            conn.execute(stmt, {
                "id": str(uuid.uuid4()),
                "vehicle_id": record["vehicleid"],
                "status": record["status"],
                "prob": round(record["probabilities"][record["status"]], 4),
                "recc": record["recommendation"]
            })
        conn.commit()

    return output