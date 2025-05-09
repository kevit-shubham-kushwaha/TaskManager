import requests  # Keep the original name
from flask import request  # Import `request` from Flask
import json  

TEAMS_WEBHOOK_URL =  "https://adminkevit.webhook.office.com/webhookb2/bd99e22a-3ee1-4be6-ad85-9f08d74f1cd7@4cf93128-6664-4246-bb76-5d7866e8fa94/IncomingWebhook/af518a8689cd47a6bd51460bfde13539/9c259211-7985-43fe-b1a7-f39abe45049e/V2J3ZrqV-5X8Yd8ShXj3nZ7kqzHKDWsLHggMPfwaw-3vw1"

def send_to_teams(message: str):
    """Send a formatted error message to Microsoft Teams via Webhook."""
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000",  
        "summary": "Flask Error",
        "sections": [
            {
                "activityTitle": "🚨 Flask Application Error!",
                "facts": [
                    {"name": "📌 URL", "value": request.url},
                    {"name": "📢 Method", "value": request.method},
                    {"name": "❌ Error", "value": message},
                ],
                "markdown": True,
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(TEAMS_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            print(f"Failed to send message to Teams: {response.text}")
    except Exception as e:
        print(f"Error sending message to Teams: {e}")


