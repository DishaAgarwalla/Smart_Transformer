import os
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv

from api.transformer_routes import transformer_bp
from api.auth_routes import auth_bp

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

    return app


if __name__ == "__main__":
    app = create_app()

    # IMPORTANT CHANGE HERE 👇
    app.run(host="0.0.0.0", port=5000, debug=True)