import requests

TOKEN = "EAAX3zeKfwksBPZAJcYyZCGFIZCmwErDmDxsvtcxfRNal577LQdaAu0VEhFkIOgbKErZBe7F4oUkiMLKT1IrlVaJ4IXCnKd5HUBIVZBvyXPXagpAjx3tPf4mupeHP0nmSLInKPSZBVZBWN3mwp9YKUZCLqsFQrsRLMjQrBEs6VH3MIW1lWZBQztA8Q9bJNIAOTKHmmFQZDZD"            # paste your permanent token here (only locally)
PHONE_NUMBER_ID = "782792474922761"  # use your phone number id

r1 = requests.get("https://graph.facebook.com/v20.0/me",
                  params={"access_token": TOKEN})
print("me:", r1.status_code, r1.text)

r2 = requests.get(f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}",
                  params={"access_token": TOKEN})
print("phone id:", r2.status_code, r2.text)
