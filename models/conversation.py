from app.database import chat_collection

def get_chat_history(user_id):
    """Fetch user's chat history from MongoDB."""
    conversation = chat_collection.find_one({"user_id": user_id})
    return conversation["history"] if conversation else []

def save_chat_history(user_id, user_input, bot_reply):
    """Store chat history in MongoDB."""
    chat_collection.update_one(
        {"user_id": user_id},
        {"$push": {"history": {"$each": [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": bot_reply}
        ]}}},
        upsert=True
    )