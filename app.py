import os
from flask import Flask, render_template, request, jsonify, session
from mistralai import Mistral
from dotenv import load_dotenv

# load secret key from .env
load_dotenv()

app = Flask(__name__)
# In production, this should be a complex random string stored in an env variable
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key-for-local-use")

# read api key
api_key = os.getenv("MISTRAL_API_KEY")

# Check if API key exists
if not api_key:
    client = None
else:
    client = Mistral(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Empty message."})
    
    # Check if client is initialized
    if client is None:
        return jsonify({"reply": "API key not configured. Please check your .env file."})

    # Initialize history in session if it doesn't exist
    if 'history' not in session:
        session['history'] = []

    # Add user message to history
    session['history'].append({"role": "user", "content": user_message})
    
    # Keep history manageable (last 10 messages to avoid token bloat)
    if len(session['history']) > 10:
        session['history'] = session['history'][-10:]

    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=session['history']
        )

        reply = response.choices[0].message.content
        
        # Add assistant reply to history
        session['history'].append({"role": "assistant", "content": reply})
        session.modified = True 

    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)