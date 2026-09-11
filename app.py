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

    # List of models to try in case of rate limits
    models_to_try = ["open-mistral-nemo", "ministral-8b-latest", "open-mistral-7b"]
    response = None
    last_exception = None

    for model_name in models_to_try:
        try:
            response = client.chat.complete(
                model=model_name,
                messages=session['history']
            )
            break
        except Exception as e:
            last_exception = e
            status_code = getattr(e, "status_code", None)
            err_str = str(e).lower()
            # If rate limited (429), try the next fallback model
            if status_code == 429 or "429" in err_str or "rate_limited" in err_str:
                continue
            else:
                # Non-rate-limit exception (e.g., auth error), stop trying
                break

    if response:
        reply = response.choices[0].message.content
        # Add assistant reply to history
        session['history'].append({"role": "assistant", "content": reply})
        session.modified = True
    else:
        status_code = getattr(last_exception, "status_code", None) if last_exception else None
        err_str = str(last_exception).lower() if last_exception else ""
        if status_code == 429 or "429" in err_str or "rate_limited" in err_str:
            reply = "Rate limit reached. Please wait a few seconds and try again."
        else:
            reply = f"Error: {str(last_exception)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Avoid Flask's reloader/signal handling when running under other runners (e.g., Streamlit).
    app.run(debug=True, use_reloader=False)
