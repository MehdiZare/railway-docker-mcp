"""Tests for Railway MCP tools."""

import pytest
import respx
from httpx import Response

from railway_mcp.client import RailwayClient
from railway_mcp.tools.projects import create_project_and_link, list_projects
from railway_mcp.tools.services import list_services
from railway_mcp.tools.status import check_railway_status


@pytest.fixture
def client():
    """Create a test client."""
    return RailwayClient(token="test_token", api_url="https://api.test.com/graphql")


@pytest.mark.asyncio
async def test_check_railway_status(client):
    """Test check_railway_status tool."""
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
            result = await check_railway_status(client)

        assert result["status"] == "connected"
        assert result["user"]["id"] == "user_123"


@pytest.mark.asyncio
async def test_list_projects(client):
    """Test list_projects tool."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "me": {
                            "projects": {
                                "edges": [
                                    {
                                        "node": {
                                            "id": "proj_123",
                                            "name": "My Project",
                                            "description": "A test project",
                                            "createdAt": "2024-01-01T00:00:00Z",
                                            "updatedAt": "2024-01-02T00:00:00Z",
                                            "environments": {"edges": []},
                                            "services": {"edges": []},
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
            )
        )

        async with client:
            projects = await list_projects(client)

        assert len(projects) == 1
        assert projects[0]["id"] == "proj_123"
        assert projects[0]["name"] == "My Project"


@pytest.mark.asyncio
async def test_create_project_and_link(client):
    """Test create_project_and_link tool."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "projectCreate": {
                            "id": "proj_new",
                            "name": "New Project",
                            "description": "A new project",
                            "createdAt": "2024-01-01T00:00:00Z",
                            "environments": {
                                "edges": [{"node": {"id": "env_prod", "name": "production"}}]
                            },
                        }
                    }
                },
            )
        )

        async with client:
            project = await create_project_and_link(
                client, name="New Project", description="A new project"
            )

        assert project["id"] == "proj_new"
        assert project["name"] == "New Project"
        assert len(project["environments"]) == 1


@pytest.mark.asyncio
async def test_list_services(client):
    """Test list_services tool."""
    with respx.mock:
        respx.post("https://api.test.com/graphql").mock(
            return_value=Response(
                200,
                json={
                    "data": {
                        "project": {
                            "services": {
                                "edges": [
                                    {
                                        "node": {
                                            "id": "svc_123",
                                            "name": "web",
                                            "icon": "🌐",
                                            "createdAt": "2024-01-01T00:00:00Z",
                                            "updatedAt": "2024-01-02T00:00:00Z",
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
            )
        )

        async with client:
            services = await list_services(client, project_id="proj_123")

        assert len(services) == 1
        assert services[0]["id"] == "svc_123"
        assert services[0]["name"] == "web"
