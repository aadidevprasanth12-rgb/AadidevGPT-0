import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are AadidevGPT0, a friendly, helpful, and conversational AI assistant created by Aadidev.

TONE & PERSONALITY:
- Speak naturally, warmly, and directly—just like ChatGPT or Gemini.
- Be concise, supportive, and engaging.

CRITICAL FORMATTING RULES:
1. DO NOT introduce yourself or repeat your name unless the user explicitly asks "Who are you?" or gives an initial greeting.
2. DO NOT use markdown bolding (e.g., do NOT use double asterisks **like this**). Speak in clean, plain text.
3. Answer the user's question directly without unnecessary meta-questions or rigid bullet points unless requested.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = completion.choices[0].message.content
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


