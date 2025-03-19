from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager
from flask_limiter import Limiter
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
import time
import logging
from app.database import chat_collection, redis_client

auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()

# Limit login attempts to prevent brute force attacks
limiter = Limiter(key_func=lambda: request.remote_addr)

# Logging setup
logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

JWT_BLACKLIST_KEY = "jwt_blacklist"

def add_token_to_blacklist(jti, expires_at):
    """Add token to blacklist with expiry time."""
    ttl = int(expires_at - time.time())
    if ttl > 0:
        redis_client.setex(f"blacklist:{jti}", ttl, "true")

def is_token_blacklisted(jti):
    """Check if token is blacklisted."""
    return redis_client.exists(f"blacklist:{jti}")

@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    return is_token_blacklisted(jwt_payload["jti"])

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        if chat_collection.find_one({"user_id": username}):
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password)
        chat_collection.insert_one({"user_id": username, "password": hashed_password})

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logging.error(f"Error in registration: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        user = chat_collection.find_one({"user_id": username})

        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
        return jsonify({"token": access_token})
    except Exception as e:
        logging.error(f"Error in login: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        expires_at = get_jwt()["exp"]
        add_token_to_blacklist(jti, expires_at)
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        logging.error(f"Error in logout: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500