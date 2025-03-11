from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from app.chatbot import chat_with_ai
from app.utils import sanitize_input  # Import sanitization function

chat_bp = Blueprint("chat", __name__)

# Apply rate limiting (10 requests per minute per user)
limiter = Limiter(key_func=lambda: request.json.get("user_id"))

@chat_bp.route("/chat", methods=["POST"])
@limiter.limit("10 per minute")  # Each user can send 10 messages per minute
def chat():
    user_id = request.json.get("user_id")
    user_input = request.json.get("message")

    if not user_id or not user_input:
        return jsonify({"error": "Missing user_id or message"}), 400

    # Sanitize user input
    user_input = sanitize_input(user_input)

    try:
        reply = chat_with_ai(user_id, user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500