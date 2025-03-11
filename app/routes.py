from flask import Blueprint, request, jsonify
from app.chatbot import chat_with_ai

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    user_id = request.json.get("user_id")
    user_input = request.json.get("message")

    if not user_id or not user_input:
        return jsonify({"error": "Missing user_id or message"}), 400

    try:
        reply = chat_with_ai(user_id, user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
