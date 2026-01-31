"""Template tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import DEPLOY_TEMPLATE_MUTATION
from ..graphql.queries import GET_TEMPLATE_QUERY, LIST_TEMPLATES_QUERY


async def list_templates(client: RailwayClient, limit: int = 50) -> list[dict[str, Any]]:
    """List available templates from Railway Template Library.

    Args:
        client: Railway API client
        limit: Maximum number of templates to return

    Returns:
        List of template dictionaries
    """
    data = await client.execute(LIST_TEMPLATES_QUERY, {"first": limit})
    templates = []

    edges = data.get("templates", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        templates.append(
            {
                "id": node.get("id"),
                "code": node.get("code"),
                "name": node.get("name"),
                "description": node.get("description"),
                "category": node.get("category"),
                "health": node.get("health"),
                "activeProjects": node.get("activeProjects"),
            }
        )

    return templates


async def get_template(client: RailwayClient, code: str) -> dict[str, Any]:
    """Get template details.

    Args:
        client: Railway API client
        code: Template code (e.g., "redis", "postgres")

    Returns:
        Template information
    """
    data = await client.execute(GET_TEMPLATE_QUERY, {"code": code})
    template = data.get("template", {})

    return {
        "id": template.get("id"),
        "code": template.get("code"),
        "name": template.get("name"),
        "description": template.get("description"),
        "category": template.get("category"),
        "health": template.get("health"),
        "activeProjects": template.get("activeProjects"),
        "services": template.get("services", []),
    }


async def deploy_template(
    client: RailwayClient,
    project_id: str,
    environment_id: str,
    template_code: str,
    services: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Deploy from Railway Template Library.

    Args:
        client: Railway API client
        project_id: Project ID to deploy to
        environment_id: Environment ID to deploy to
        template_code: Template code (e.g., "redis", "postgres")
        services: Optional list of service configurations

    Returns:
        Deployment result
    """
    variables = {
        "projectId": project_id,
        "environmentId": environment_id,
        "templateCode": template_code,
    }
    if services:
        variables["services"] = services

    data = await client.execute(DEPLOY_TEMPLATE_MUTATION, variables)
    result = data.get("templateDeploy", {})

    return {
        "projectId": result.get("projectId"),
        "workflowId": result.get("workflowId"),
        "templateCode": template_code,
        "message": f"Template '{template_code}' deployment initiated",
    }
