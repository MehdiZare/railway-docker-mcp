"""Environment tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import CREATE_ENVIRONMENT_MUTATION
from ..graphql.queries import LIST_ENVIRONMENTS_QUERY


async def list_environments(client: RailwayClient, project_id: str) -> list[dict[str, Any]]:
    """List environments in a project.

    Args:
        client: Railway API client
        project_id: Project ID

    Returns:
        List of environment dictionaries
    """
    data = await client.execute(LIST_ENVIRONMENTS_QUERY, {"projectId": project_id})
    environments = []

    edges = data.get("project", {}).get("environments", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        environments.append(
            {
                "id": node.get("id"),
                "name": node.get("name"),
                "createdAt": node.get("createdAt"),
                "updatedAt": node.get("updatedAt"),
            }
        )

    return environments


async def create_environment(
    client: RailwayClient,
    project_id: str,
    name: str,
) -> dict[str, Any]:
    """Create a new environment in a project.

    Args:
        client: Railway API client
        project_id: Project ID
        name: Environment name

    Returns:
        Created environment information
    """
    data = await client.execute(
        CREATE_ENVIRONMENT_MUTATION,
        {"projectId": project_id, "name": name},
    )
    environment = data.get("environmentCreate", {})

    return {
        "id": environment.get("id"),
        "name": environment.get("name"),
        "createdAt": environment.get("createdAt"),
    }


async def link_environment(
    client: RailwayClient, project_id: str, environment_id: str
) -> dict[str, Any]:
    """Get environment details for linking/context.

    Args:
        client: Railway API client
        project_id: Project ID (for validation)
        environment_id: Environment ID to link

    Returns:
        Environment information
    """
    # Get all environments and find the matching one
    data = await client.execute(LIST_ENVIRONMENTS_QUERY, {"projectId": project_id})

    edges = data.get("project", {}).get("environments", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        if node.get("id") == environment_id:
            return {
                "id": node.get("id"),
                "name": node.get("name"),
                "projectId": project_id,
                "createdAt": node.get("createdAt"),
                "updatedAt": node.get("updatedAt"),
            }

    # If not found, raise an error
    from ..exceptions import EnvironmentNotFoundError

    raise EnvironmentNotFoundError(f"Environment {environment_id} not found in project")
