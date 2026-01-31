"""Project tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import CREATE_PROJECT_MUTATION
from ..graphql.queries import LIST_PROJECTS_QUERY


async def list_projects(client: RailwayClient) -> list[dict[str, Any]]:
    """List all accessible Railway projects.

    Returns:
        List of project dictionaries
    """
    data = await client.execute(LIST_PROJECTS_QUERY)
    projects = []

    edges = data.get("me", {}).get("projects", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        environments = [
            {"id": e["node"]["id"], "name": e["node"]["name"]}
            for e in node.get("environments", {}).get("edges", [])
        ]
        services = [
            {"id": s["node"]["id"], "name": s["node"]["name"]}
            for s in node.get("services", {}).get("edges", [])
        ]
        projects.append(
            {
                "id": node.get("id"),
                "name": node.get("name"),
                "description": node.get("description"),
                "createdAt": node.get("createdAt"),
                "updatedAt": node.get("updatedAt"),
                "environments": environments,
                "services": services,
            }
        )

    return projects


async def create_project_and_link(
    client: RailwayClient,
    name: str,
    description: str | None = None,
    default_environment_name: str | None = None,
) -> dict[str, Any]:
    """Create a new Railway project.

    Args:
        client: Railway API client
        name: Project name
        description: Optional project description
        default_environment_name: Name for the default environment (defaults to "production")

    Returns:
        Created project information
    """
    variables = {"name": name}
    if description:
        variables["description"] = description
    if default_environment_name:
        variables["defaultEnvironmentName"] = default_environment_name

    data = await client.execute(CREATE_PROJECT_MUTATION, variables)
    project = data.get("projectCreate", {})

    environments = [
        {"id": e["node"]["id"], "name": e["node"]["name"]}
        for e in project.get("environments", {}).get("edges", [])
    ]

    return {
        "id": project.get("id"),
        "name": project.get("name"),
        "description": project.get("description"),
        "createdAt": project.get("createdAt"),
        "environments": environments,
    }
