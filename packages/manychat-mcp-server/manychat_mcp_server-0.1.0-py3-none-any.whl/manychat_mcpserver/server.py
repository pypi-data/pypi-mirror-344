from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("WebExtractor")

@mcp.tool()
def send_manychat_message(subscriber_id: int, text_message: str) -> dict:
    """Send a message to ManyChat API"""
    url = 'https://api.manychat.com/fb/sending/sendContent'
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 2756782:557a171ce3cffeca797fa6dce06dc4be',
        'Content-Type': 'application/json'
    }
    data = {
        "subscriber_id": subscriber_id,
        "data": {
            "version": "v2",
            "content": {
                "type": "instagram",
                "messages": [
                    {
                        "type": "text",
                        "text": text_message
                    }
                ],
                "actions": [],
                "quick_replies": []
            }
        },
        "message_tag": "ACCOUNT_UPDATE"
    }
    
    # Make the POST request to the ManyChat API
    response = requests.post(url, json=data, headers=headers)
    
    # Return the response JSON to the client
    return response.json()

if __name__ == "__main__":
    mcp.run()