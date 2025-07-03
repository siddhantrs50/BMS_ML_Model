import requests
import json
from datetime import datetime

url = "http://127.0.0.1:8000/predict"

try:
    response = requests.get(url)
    response.raise_for_status()
    predictions = response.json()

    with open(f"predictions_{datetime.now().date()}.json", "w") as f:
        json.dump(predictions, f, indent=2)
    print("Predictions saved successfully.")

except Exception as e:
    print("Error during prediction:", e)