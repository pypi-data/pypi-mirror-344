from typing import Any
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()
DEFAULT_API_KEY = os.getenv("MANYCHAT_API_KEY")

MANYCHAT_API_BASE = "https://api.manychat.com/fb/sending"

async def make_manychat_request(url: str, api_key: str, data: dict) -> dict[str, Any] | None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Failed request to {url}: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"[DEBUG] Response content: {e.response.text}")
            return {"error": str(e)}

async def send_message(api_key: str, subscriber_id: int, message: str, message_tag: str = "ACCOUNT_UPDATE") -> str:
    url = f"{MANYCHAT_API_BASE}/sendContent"
    data = {
        "subscriber_id": subscriber_id,
        "data": {
            "version": "v2",
            "content": {
                "type": "instagram",
                "messages": [{"type": "text", "text": message}],
                "actions": [],
                "quick_replies": []
            }
        },
        "message_tag": message_tag
    }

    response = await make_manychat_request(url, api_key, data)
    if response is None or "error" in response:
        return f"Error: {response.get('error', 'Unknown error')}" if response else "Failed to send message"
    return f"Message sent successfully to subscriber ID {subscriber_id}. Response: {json.dumps(response, indent=2)}"

async def send_call_button(api_key: str, subscriber_id: int, message: str, phone_number: str, button_caption: str = "Call me", message_tag: str = "ACCOUNT_UPDATE") -> str:
    url = f"{MANYCHAT_API_BASE}/sendContent"
    data = {
        "subscriber_id": subscriber_id,
        "data": {
            "version": "v2",
            "content": {
                "type": "instagram",
                "messages": [{
                    "type": "text",
                    "text": message,
                    "buttons": [{
                        "type": "call",
                        "caption": button_caption,
                        "phone": phone_number
                    }]
                }],
                "actions": [],
                "quick_replies": []
            }
        },
        "message_tag": message_tag
    }

    response = await make_manychat_request(url, api_key, data)
    if response is None or "error" in response:
        return f"Error: {response.get('error', 'Unknown error')}" if response else "Failed to send message"
    return f"Call button message sent successfully to subscriber ID {subscriber_id}. Response: {json.dumps(response, indent=2)}"
