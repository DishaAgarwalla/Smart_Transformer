import os
import sys

# Fix import path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from predict import predict_lstm


def get_prediction(data):
    """
    Calls ML model and formats response safely
    """

    try:
        score = predict_lstm(data)  # expected float

        # If predict_lstm returned an error dictionary
        if isinstance(score, dict):
            return score

        # Ensure score is numeric
        score = float(score)

        health_score = (1 - score) * 100

        if score < 0.3:
            status = "Healthy ✅"
        elif score < 0.6:
            status = "Warning ⚠️"
        else:
            status = "Failure Risk 🚨"

        return {
            "failure_probability": round(score, 4),
            "health_score": round(health_score, 2),
            "status": status
        }

    except Exception as e:
        return {
            "error": str(e)
        }