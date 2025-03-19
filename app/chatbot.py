import openai
from app.config import Config
from app.database import redis_client
from models.conversation import save_chat_history
import logging

# Initialize OpenAI client
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

# Logging setup
logging.basicConfig(level=logging.ERROR, filename="error.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

def chat_with_ai(user_id, user_input):
    """Handles conversation with AI, using Redis for short-term memory, with streaming support."""
    try:
        history = redis_client.lrange(user_id, 0, -1) or []
        redis_client.expire(user_id, 86400)  # Expire after 24 hours

        messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": msg} for i, msg in enumerate(history)]
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        bot_reply = ""
        for chunk in response:
            bot_reply += chunk.choices[0].delta.content or ""

        redis_client.rpush(user_id, user_input, bot_reply)
        redis_client.ltrim(user_id, -20, -1)  # Keep only last 20 messages

        save_chat_history(user_id, user_input, bot_reply)
        return bot_reply

    except Exception as e:
        logging.error(f"Error in AI chat function: {str(e)}", exc_info=True)
        return "Sorry, an error occurred while processing your request."