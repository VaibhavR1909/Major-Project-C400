from twilio.rest import Client
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file (ensure API keys are stored there)
load_dotenv()

# Google API key for Generative AI (replace with environment variable or secure storage)
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

def fetch_logs():
    # Fetches content from stress test log file
    with open('stress_test.log', 'r') as file:
        txt = file.read()
    return txt

def send_logs_to_api(logs):
    # Calls generative AI model to analyze logs and suggest troubleshooting steps
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"suggest troubleshooting steps in 150 words based on the given logs\n{logs}")
    print(response.text)
    return response.text

def send_whatsapp_message(message_body):
    # Twilio credentials loaded from environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    # Sending WhatsApp message
    sent_message = client.messages.create(
        body=message_body,
        from_="whatsapp:+14155238886",  # Twilio sandbox number for WhatsApp
        to="whatsapp:"  # Replace with your target WhatsApp number
    )
    print("WhatsApp message sent with SID:", sent_message.sid)
    return sent_message.sid

def main():
    logs = fetch_logs()
    analysis_result = send_logs_to_api(logs)

    if analysis_result:
        send_whatsapp_message(analysis_result)

if __name__ == "__main__":
    main()
