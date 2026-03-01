from flask import Blueprint, request, jsonify
from services.health_service import calculate_health
from services.ml_service import predict_failure
from core.database import get_db_connection
from flask_jwt_extended import jwt_required

transformer_bp = Blueprint("transformer_bp", __name__)

# -------------------------------
# POST API - Receive Sensor Data
# -------------------------------
@transformer_bp.route("/data", methods=["POST"])
def receive_data():
    try:
        data = request.json

        result = calculate_health(data)
        ml_prediction = predict_failure(data)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transformer_data
            (temperature, current, voltage, vibration, humidity, oil_color,
             health_score, prediction, risk_percentage, status, ml_prediction)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data.get("temperature"),
            data.get("current"),
            data.get("voltage"),
            data.get("vibration"),
            data.get("humidity"),
            data.get("oil_color"),
            result["health_score"],
            result["prediction"],
            result["risk_percentage"],
            result["status"],
            ml_prediction
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "health_score": result["health_score"],
            "risk_percentage": result["risk_percentage"],
            "status": result["status"],
            "rule_based_prediction": result["prediction"],
            "ml_prediction": ml_prediction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# GET API - Fetch Reports (Protected)
# -------------------------------
@transformer_bp.route("/reports", methods=["GET"])
@jwt_required()
def get_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM transformer_data ORDER BY created_at DESC")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500