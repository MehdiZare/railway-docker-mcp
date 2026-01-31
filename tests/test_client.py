"""Tests for the Railway GraphQL client."""

import pytest
import respx
from httpx import Response

from railway_mcp.client import RailwayClient
from railway_mcp.exceptions import AuthenticationError, GraphQLError


@pytest.fixture
def client():
    """Create a test client."""
    return RailwayClient(token="test_token", api_url="https://api.test.com/graphql")


@pytest.mark.asyncio
async def test_verify_token_success(client):
    """Test successful token verification."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "me": {
                            "id": "user_123",
                            "name": "Test User",
                            "email": "test@example.com",
                        }
                    }
                },
            )
        )

        async with client:
            user = await client.verify_token()

        assert user["id"] == "user_123"
        assert user["name"] == "Test User"
        assert user["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_verify_token_invalid(client):
    """Test invalid token verification."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )

        async with client:
            with pytest.raises(AuthenticationError):
                await client.verify_token()


@pytest.mark.asyncio
async def test_execute_graphql_error(client):
    """Test GraphQL error handling."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "errors": [{"message": "Project not found"}],
                },
            )
        )

        async with client:
            with pytest.raises(GraphQLError) as exc_info:
                await client.execute('query { project(id: "123") { id } }')

        assert "Project not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_execute_success(client):
    """Test successful query execution."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "project": {
                            "id": "proj_123",
                            "name": "My Project",
                        }
                    }
                },
            )
        )

        async with client:
            data = await client.execute('query { project(id: "123") { id name } }')

        assert data["project"]["id"] == "proj_123"
        assert data["project"]["name"] == "My Project"
