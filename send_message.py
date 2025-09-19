import requests

ACCESS_TOKEN = "EAAX3zeKfwksBPZAJcYyZCGFIZCmwErDmDxsvtcxfRNal577LQdaAu0VEhFkIOgbKErZBe7F4oUkiMLKT1IrlVaJ4IXCnKd5HUBIVZBvyXPXagpAjx3tPf4mupeHP0nmSLInKPSZBVZBWN3mwp9YKUZCLqsFQrsRLMjQrBEs6VH3MIW1lWZBQztA8Q9bJNIAOTKHmmFQZDZD"
PHONE_NUMBER_ID = "782792474922761"
TO_NUMBER = "whatsapp:+923155561689"  # ✅ must include "whatsapp:"

url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": TO_NUMBER,
    "type": "text",
    "text": {"body": "Hello 👋, this is your bot test!"}
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code, response.text)
