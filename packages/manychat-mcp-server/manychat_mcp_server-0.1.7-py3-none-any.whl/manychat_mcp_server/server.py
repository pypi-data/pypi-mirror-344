from mcp.server.fastmcp import FastMCP
from manychat_mcp_server.manychat import send_message, send_call_button, DEFAULT_API_KEY

# Initialize MCP server
mcp = FastMCP("instagram_messenger")

@mcp.tool()
async def send_instagram_message(
    subscriber_id: int,
    message: str,
    message_tag: str = "ACCOUNT_UPDATE",
    api_key: str = DEFAULT_API_KEY
) -> str:
    """Send a basic Instagram message using ManyChat API."""
    return await send_message(api_key, subscriber_id, message, message_tag)

@mcp.tool()
async def send_call_button_message(
    subscriber_id: int,
    message: str,
    phone_number: str,
    button_caption: str = "Call me",
    message_tag: str = "ACCOUNT_UPDATE",
    api_key: str = DEFAULT_API_KEY
) -> str:
    """Send an Instagram message with a call button using ManyChat API."""
    return await send_call_button(api_key, subscriber_id, message, phone_number, button_caption, message_tag)

if __name__ == "__main__":
    mcp.run(transport="stdio")
