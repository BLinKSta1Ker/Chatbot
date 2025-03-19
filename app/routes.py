from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_jwt_extended import jwt_required, get_jwt
from app.chatbot import chat_with_ai
from app.utils import sanitize_input
from models.conversation import get_chat_history
from app.database import redis_client
import logging

chat_bp = Blueprint("chat", __name__)

limiter = Limiter(key_func=lambda: request.remote_addr)

logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

def is_token_blacklisted(jti):
    return redis_client.exists(f"blacklist:{jti}")

@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def chat():
    try:
        user_id = request.json.get("user_id")
        user_input = request.json.get("message")

        if not user_id or not user_input:
            return jsonify({"error": "Missing user_id or message"}), 400

        user_input = sanitize_input(user_input)

        jti = get_jwt()["jti"]
        if is_token_blacklisted(jti):
            return jsonify({"error": "Token has been revoked"}), 401

        reply = chat_with_ai(user_id, user_input)
        return jsonify({"reply": reply})

    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

@chat_bp.route("/history", methods=["GET"])
@jwt_required()
def chat_history():
    try:
        user_id = request.args.get("user_id")

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        jti = get_jwt()["jti"]
        if is_token_blacklisted(jti):
            return jsonify({"error": "Token has been revoked"}), 401

        history = get_chat_history(user_id)
        return jsonify({"history": history})

    except Exception as e:
        logging.error(f"Error in chat history endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500