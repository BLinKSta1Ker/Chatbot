from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from app.database import chat_collection  # Import MongoDB collection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user with a hashed password."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if the user already exists
    if chat_collection.find_one({"user_id": username}):
        return jsonify({"error": "User already exists"}), 400

    # Store user with a hashed password
    hashed_password = generate_password_hash(password)
    chat_collection.insert_one({"user_id": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Fetch user from MongoDB
    user = chat_collection.find_one({"user_id": username})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify({"token": access_token})