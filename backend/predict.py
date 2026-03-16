import numpy as np
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "ml_model", "predictive_maintenance_model.pkl")
model = joblib.load(model_path)

print("======================================")
print("Model was trained with these features:")
print(model.feature_names_in_)
print("======================================")


def predict_lstm(data_dict):
    try:
        # Map ONLY the 5 required features
        mapped_data = {
            "Air temperature [K]": data_dict["air_temp"],
            "Process temperature [K]": data_dict["process_temp"],
            "Rotational speed [rpm]": data_dict["rpm"],
            "Torque [Nm]": data_dict["torque"],
            "Tool wear [min]": data_dict["tool_wear"]
        }

        df = pd.DataFrame([mapped_data])

        # Keep exact order
        X = df[model.feature_names_in_]

        prediction = model.predict_proba(X)[0][1]

        return float(prediction)

    except Exception as e:
        return {"error": str(e)}