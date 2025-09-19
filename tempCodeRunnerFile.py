import requests
from flask import Flask, request
import google.generativeai as genai

# ========================
# CONFIG (replace values)
# ========================
ACCESS_TOKEN = "EAAX3zeKfwksBPZAJcYyZCGFIZCmwErDmDxsvtcxfRNal577LQdaAu0VEhFkIOgbKErZBe7F4oUkiMLKT1IrlVaJ4IXCnKd5HUBIVZBvyXPXagpAjx3tPf4mupeHP0nmSLInKPSZBVZBWN3mwp9YKUZCLqsFQrsRLMjQrBEs6VH3MIW1lWZBQztA8Q9bJNIAOTKHmmFQZDZD"   # Permanent WhatsApp access token
PHONE_NUMBER_ID = "782792474922761"      # WhatsApp phone number ID (from Meta)
GEMINI_API_KEY = "AIzaSyD4RbrByWZV7LQGdxvexF3SjxYWGFgrQS8"        # Your Gemini API key

# Flask app
app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Conversation state storage
user_states = {}

# Function to send WhatsApp message
def send_message(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

# ========================
# WEBHOOK ENDPOINTS
# ========================

# Verification (for Meta dashboard)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    verify_token = "mystorybot"   # Your chosen verify token
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == verify_token:
        return challenge
    return "Invalid verification token", 403

# Handle messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_number = message["from"]
        user_text = message["text"]["body"].strip()

        # Initialize state if new user
        if user_number not in user_states:
            user_states[user_number] = {"step": "genre"}
            send_message(user_number, "Hi 👋! I can tell you stories. What genre would you like? (Adventure, Mystery, Funny...)")
            return "OK", 200

        state = user_states[user_number]

        # Step by step conversation
        if state["step"] == "genre":
            state["genre"] = user_text
            state["step"] = "theme"
            send_message(user_number, "Great! What theme should the story have? (friendship, courage, magic...)")

        elif state["step"] == "theme":
            state["theme"] = user_text
            state["step"] = "characters"
            send_message(user_number, "Cool 👍 Who are the main characters?")

        elif state["step"] == "characters":
            state["characters"] = user_text
            state["step"] = "age"
            send_message(user_number, "Got it! What age group is this story for? (kids, teens, adults)")

        elif state["step"] == "age":
            state["age"] = user_text
            state["step"] = "language"
            send_message(user_number, "Okay! Which language should the story be in?")

        elif state["step"] == "language":
            state["language"] = user_text
            state["step"] = "done"

            # Generate story with Gemini
            prompt = f"""
            Write a short story in very simple {state['language']}.
            Genre: {state['genre']}
            Theme: {state['theme']}
            Characters: {state['characters']}
            Target age group: {state['age']}
            Make the story engaging and easy to understand.
            """

            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            story = response.text
            send_message(user_number, story)

            # Reset for new story
            user_states[user_number] = {"step": "genre"}
            send_message(user_number, "✨ Want another story? Tell me a genre!")

    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Storytelling Bot is Running ✅", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
