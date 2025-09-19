from flask import Flask, request
import requests
import google.generativeai as genai

app = Flask(__name__)

# ----------------------------
# CONFIG
# ----------------------------
VERIFY_TOKEN = "mystorybot"
WHATSAPP_TOKEN = "EAAX3zeKfwksBPZAJcYyZCGFIZCmwErDmDxsvtcxfRNal577LQdaAu0VEhFkIOgbKErZBe7F4oUkiMLKT1IrlVaJ4IXCnKd5HUBIVZBvyXPXagpAjx3tPf4mupeHP0nmSLInKPSZBVZBWN3mwp9YKUZCLqsFQrsRLMjQrBEs6VH3MIW1lWZBQztA8Q9bJNIAOTKHmmFQZDZD"
PHONE_NUMBER_ID = "782792474922761"
GEMINI_API_KEY = "AIzaSyD4RbrByWZV7LQGdxvexF3SjxYWGFgrQS8"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Store conversation state { user_id: {step: int, answers: {}} }
user_sessions = {}

# ----------------------------
# FUNCTIONS
# ----------------------------
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=data)

def generate_story(answers):
    prompt = f"""
    Create a story with these details:
    - Genre: {answers.get('genre')}
    - Characters: {answers.get('characters')}
    - Age group: {answers.get('age')}
    - Theme: {answers.get('theme')}
    - Language: {answers.get('language')}

    Rules:
    - Use **simple language** for easy reading.
    - Keep it engaging and short (1-2 paragraphs).
    - If language is not English, write in that language.
    """
    response = model.generate_content(prompt)
    return response.text

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Verification failed"

    if request.method == "POST":
        data = request.json
        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message["text"]["body"].strip()

            # Initialize session
            if sender not in user_sessions:
                user_sessions[sender] = {"step": 1, "answers": {}}
                send_whatsapp_message(sender, "Hi 👋! Let’s create a story. What genre do you want? (e.g. adventure, fairy tale, horror)")
                return "OK", 200

            session = user_sessions[sender]

            # Stepwise Q&A
            if session["step"] == 1:
                session["answers"]["genre"] = text
                session["step"] = 2
                send_whatsapp_message(sender, "Great! Who are the main characters?")
            elif session["step"] == 2:
                session["answers"]["characters"] = text
                session["step"] = 3
                send_whatsapp_message(sender, "Nice! What is the age group of the audience?")
            elif session["step"] == 3:
                session["answers"]["age"] = text
                session["step"] = 4
                send_whatsapp_message(sender, "Cool! What theme do you want? (funny, serious, educational...)")
            elif session["step"] == 4:
                session["answers"]["theme"] = text
                session["step"] = 5
                send_whatsapp_message(sender, "Almost done! Which language should the story be in?")
            elif session["step"] == 5:
                session["answers"]["language"] = text
                story = generate_story(session["answers"])
                send_whatsapp_message(sender, "Here’s your story:\n\n" + story)

                # Reset session after story
                user_sessions.pop(sender)

        except Exception as e:
            print("Error:", e)

        return "OK", 200

# ----------------------------
if __name__ == "__main__":
    app.run(port=5000)
