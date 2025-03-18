from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, JWTManager
from flask_limiter import Limiter
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from app.database import chat_collection, redis_client

auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()

# Limit login attempts to prevent brute force attacks
limiter = Limiter(key_func=lambda: request.json.get("username"))

# Store blacklisted tokens in Redis
JWT_BLACKLIST_KEY = "jwt_blacklist"

def add_token_to_blacklist(jti):
    redis_client.sadd(JWT_BLACKLIST_KEY, jti)

def is_token_blacklisted(jti):
    return redis_client.sismember(JWT_BLACKLIST_KEY, jti)

@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    return is_token_blacklisted(jwt_payload["jti"])

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")  # Prevent mass account creation
def register():
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


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")  # Prevent brute-force attacks
def login():
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


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    add_token_to_blacklist(jti)
    return jsonify({"message": "Logged out successfully"}), 200