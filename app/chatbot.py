import openai
from app.config import Config
from app.database import redis_client
from models.conversation import save_chat_history

# Initialize OpenAI client
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

def chat_with_ai(user_id, user_input):
    """Handles conversation with AI, using Redis for short-term memory, with streaming support."""
    
    # Fetch chat history from Redis (short-term memory)
    history = redis_client.lrange(user_id, 0, -1)
    messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": msg} for i, msg in enumerate(history)]
    messages.append({"role": "user", "content": user_input})

    # Call OpenAI API with streaming
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True  # Enable streaming
    )
    
    bot_reply = ""
    for chunk in response:
        bot_reply += chunk.choices[0].delta.content or ""

    # Store conversation in Redis
    redis_client.rpush(user_id, user_input, bot_reply)

    # Limit history in Redis (e.g., keep last 20 messages)
    if redis_client.llen(user_id) > 20:
        redis_client.ltrim(user_id, -20, -1)

    # Store chat in MongoDB for long-term memory
    save_chat_history(user_id, user_input, bot_reply)

    return bot_reply