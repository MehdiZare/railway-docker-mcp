"""GraphQL client for Railway API."""

from typing import Any

import httpx

from .exceptions import AuthenticationError, GraphQLError


class RailwayClient:
    """Async GraphQL client for Railway API."""

    def __init__(self, token: str, api_url: str):
        """Initialize the Railway client.

        Args:
            token: Railway API token
            api_url: Railway GraphQL API URL
        """
        self.token = token
        self.api_url = api_url
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "RailwayClient":
        """Enter async context."""
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._client

    async def execute(
        self,
        query: str,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute a GraphQL query or mutation.

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            Query response data

        Raises:
            AuthenticationError: If authentication fails
            GraphQLError: If the query fails
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = await self.client.post(self.api_url, json=payload)

        if response.status_code == 401:
            raise AuthenticationError("Invalid Railway API token")

        if response.status_code != 200:
            raise GraphQLError(f"HTTP error {response.status_code}: {response.text}")

        result = response.json()

        if "errors" in result:
            errors = result["errors"]
            message = errors[0].get("message", "Unknown GraphQL error")
            raise GraphQLError(message, errors)

        return result.get("data", {})

    async def verify_token(self) -> dict[str, Any]:
        """Verify the API token is valid.

        Returns:
            User information

        Raises:
            AuthenticationError: If token is invalid
        """
        query = """
        query Me {
            me {
                id
                name
                email
            }
        }
        """
        data = await self.execute(query)
        if not data.get("me"):
            raise AuthenticationError("Unable to verify token")
        return data["me"]
