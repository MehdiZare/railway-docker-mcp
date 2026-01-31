"""Status check tool."""

from ..client import RailwayClient


async def check_railway_status(client: RailwayClient) -> dict:
    """Verify API access and authentication.

    Returns:
        Dictionary with status and user information
    """
    user = await client.verify_token()
    return {
        "status": "connected",
        "user": {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
        },
    }
