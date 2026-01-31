"""Service tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import DEPLOY_SERVICE_MUTATION
from ..graphql.queries import GET_SERVICE_QUERY, LIST_SERVICES_QUERY


async def list_services(client: RailwayClient, project_id: str) -> list[dict[str, Any]]:
    """List services in a project.

    Args:
        client: Railway API client
        project_id: Project ID

    Returns:
        List of service dictionaries
    """
    data = await client.execute(LIST_SERVICES_QUERY, {"projectId": project_id})
    services = []

    edges = data.get("project", {}).get("services", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        services.append(
            {
                "id": node.get("id"),
                "name": node.get("name"),
                "icon": node.get("icon"),
                "createdAt": node.get("createdAt"),
                "updatedAt": node.get("updatedAt"),
            }
        )

    return services


async def link_service(client: RailwayClient, service_id: str) -> dict[str, Any]:
    """Get service details for linking/context.

    Args:
        client: Railway API client
        service_id: Service ID to link

    Returns:
        Service information
    """
    data = await client.execute(GET_SERVICE_QUERY, {"serviceId": service_id})
    service = data.get("service", {})

    return {
        "id": service.get("id"),
        "name": service.get("name"),
        "icon": service.get("icon"),
        "projectId": service.get("projectId"),
        "createdAt": service.get("createdAt"),
        "updatedAt": service.get("updatedAt"),
    }


async def deploy(
    client: RailwayClient,
    service_id: str,
    environment_id: str,
) -> dict[str, Any]:
    """Trigger deployment for a service.

    Args:
        client: Railway API client
        service_id: Service ID to deploy
        environment_id: Environment ID to deploy to

    Returns:
        Deployment result
    """
    data = await client.execute(
        DEPLOY_SERVICE_MUTATION,
        {"serviceId": service_id, "environmentId": environment_id},
    )

    # serviceInstanceDeploy returns a boolean
    success = data.get("serviceInstanceDeploy", False)

    return {
        "success": success,
        "serviceId": service_id,
        "environmentId": environment_id,
        "message": "Deployment triggered successfully" if success else "Deployment failed",
    }
