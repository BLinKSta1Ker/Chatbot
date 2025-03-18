from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_jwt_extended import jwt_required, get_jwt
from app.chatbot import chat_with_ai
from app.utils import sanitize_input
from models.conversation import get_chat_history
from app.database import redis_client  # Import Redis client

chat_bp = Blueprint("chat", __name__)

limiter = Limiter(key_func=lambda: request.json.get("user_id"))

# Store blacklisted tokens in Redis
JWT_BLACKLIST_KEY = "jwt_blacklist"

def is_token_blacklisted(jti):
    return redis_client.sismember(JWT_BLACKLIST_KEY, jti)

@chat_bp.route("/chat", methods=["POST"])
@jwt_required()  # Ensure authentication
@limiter.limit("10 per minute")
def chat():
    user_id = request.json.get("user_id")
    user_input = request.json.get("message")

    if not user_id or not user_input:
        return jsonify({"error": "Missing user_id or message"}), 400

    user_input = sanitize_input(user_input)

    jti = get_jwt()["jti"]  # Check if token is blacklisted
    if is_token_blacklisted(jti):
        return jsonify({"error": "Token has been revoked"}), 401  # Reject request

    try:
        reply = chat_with_ai(user_id, user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/history", methods=["GET"])
@jwt_required()  # Ensure authentication
def chat_history():
    """Retrieve chat history for a user from MongoDB."""
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    jti = get_jwt()["jti"]  # Check if token is blacklisted
    if is_token_blacklisted(jti):
        return jsonify({"error": "Token has been revoked"}), 401  # Reject request

    history = get_chat_history(user_id)
    return jsonify({"history": history})