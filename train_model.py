import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Replace with actual data fetch or path
df = pd.read_csv("sample_bms_data.csv")

df["status"] = pd.cut(df["State_of_Health"], bins=[0, 85, 95, 100], labels=["Critical", "Warning", "Good"])

X = df.drop(["Battery_Pack_ID", "VehicleID", "Battery_Pack_Manufacturer", "Battery_Pack_Model", "status"], axis=1)
y = LabelEncoder().fit_transform(df["status"])

model = XGBClassifier()
model.fit(X, y)

joblib.dump(model, "model/xgb_model.pkl")