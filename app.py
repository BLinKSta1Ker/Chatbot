import os
from flask import Flask, request, jsonify, session
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append({"role": "user", "content": user_input})

    if len(session["chat_history"]) > 10:
        session["chat_history"] = session["chat_history"][-10:]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=session["chat_history"]
        )
        reply = response.choices[0].message.content

        session["chat_history"].append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)