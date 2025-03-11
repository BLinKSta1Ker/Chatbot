from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_limiter import Limiter
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from app.database import chat_collection

auth_bp = Blueprint("auth", __name__)

# Limit login attempts to prevent brute force attacks
limiter = Limiter(key_func=lambda: request.json.get("username"))

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