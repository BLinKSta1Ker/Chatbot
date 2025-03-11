from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.chatbot import chat_with_ai

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
@jwt_required()  # Require JWT authentication
def chat():
    user_id = get_jwt_identity()  # Get user identity from token
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    try:
        reply = chat_with_ai(user_id, user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500