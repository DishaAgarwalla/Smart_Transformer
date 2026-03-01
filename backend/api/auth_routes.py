from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from core.database import get_db_connection
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)

# -------------------------------
# Register User
# -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and Password required"}), 400

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User Registered Successfully ✅"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Login User
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            access_token = create_access_token(identity=username)
            return jsonify({
                "message": "Login Successful ✅",
                "access_token": access_token
            })

        return jsonify({"error": "Invalid Password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500