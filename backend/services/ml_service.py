import joblib
import numpy as np
import os

# Get absolute path safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "predictive_maintenance_model.pkl")

# Load model once when server starts
model = joblib.load(MODEL_PATH)

def predict_failure(data):
    try:
        input_data = np.array([[
            data.get("air_temp"),
            data.get("process_temp"),
            data.get("rpm"),
            data.get("torque"),
            data.get("tool_wear")
        ]])

        prediction = model.predict(input_data)[0]

        if prediction == 1:
            return "Machine Failure Likely ⚠️"
        else:
            return "Machine is Healthy ✅"

    except Exception as e:
        return f"Prediction Error: {str(e)}"