import os
import sys
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from services.ml_service import get_prediction

# Fix Python path so backend modules work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import routes and services
from api.transformer_routes import transformer_bp
from api.auth_routes import auth_bp
from services.ml_service import get_prediction

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # ===============================
    # Configuration
    # ===============================
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    # Initialize JWT
    jwt = JWTManager(app)

    # ===============================
    # Register Blueprints
    # ===============================
    app.register_blueprint(transformer_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # ===============================
    # Home Route
    # ===============================
    @app.route("/")
    def home():
        return "Smart Transformer Advanced Backend Running 🚀"

    # ===============================
    # LSTM Prediction Route
    # ===============================
    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.json
        result = get_prediction(data)
        return jsonify(result)

    return app


# ===============================
# Main Entry
# ===============================
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)