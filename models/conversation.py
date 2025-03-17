from datetime import datetime, timedelta
from app.database import chat_collection

def get_chat_history(user_id):
    """Fetch user's chat history from MongoDB, filtering messages from the last 30 days."""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    conversation = chat_collection.find_one({"user_id": user_id}, {"history": 1, "_id": 0})
    
    if not conversation:
        return []

    # Filter messages based on timestamp
    filtered_history = [
        msg for msg in conversation["history"]
        if msg.get("timestamp", datetime.utcnow()) >= thirty_days_ago
    ]

    return filtered_history


def save_chat_history(user_id, user_input, bot_reply):
    """Store chat history in MongoDB with timestamps."""
    chat_collection.update_one(
        {"user_id": user_id},
        {"$push": {"history": {"$each": [
            {"role": "user", "content": user_input, "timestamp": datetime.utcnow()},
            {"role": "assistant", "content": bot_reply, "timestamp": datetime.utcnow()}
        ]}}},
        upsert=True
    )


def delete_old_messages():
    """Remove messages older than 30 days from chat history."""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    chat_collection.update_many(
        {},
        {"$pull": {"history": {"timestamp": {"$lt": thirty_days_ago}}}}
    )