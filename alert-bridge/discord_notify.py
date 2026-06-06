import os
import requests


def send_discord_message(content: str) -> bool:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        print("DISCORD_WEBHOOK_URL not set. Skipping Discord notification.")
        return False

    response = requests.post(webhook_url, json={"content": content}, timeout=10)
    response.raise_for_status()
    return True
