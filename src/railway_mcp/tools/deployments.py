"""Deployment and logs tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.queries import (
    GET_BUILD_LOGS_QUERY,
    GET_DEPLOYMENT_LOGS_QUERY,
    LIST_DEPLOYMENTS_QUERY,
)


async def list_deployments(
    client: RailwayClient,
    service_id: str,
    environment_id: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """List deployments for a service.

    Args:
        client: Railway API client
        service_id: Service ID
        environment_id: Environment ID
        limit: Maximum number of deployments to return

    Returns:
        List of deployment dictionaries
    """
    data = await client.execute(
        LIST_DEPLOYMENTS_QUERY,
        {"serviceId": service_id, "environmentId": environment_id, "first": limit},
    )
    deployments = []

    edges = data.get("deployments", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        deployments.append(
            {
                "id": node.get("id"),
                "status": node.get("status"),
                "createdAt": node.get("createdAt"),
                "updatedAt": node.get("updatedAt"),
                "staticUrl": node.get("staticUrl"),
                "meta": node.get("meta"),
            }
        )

    return deployments


async def get_logs(
    client: RailwayClient,
    deployment_id: str,
    log_type: str = "deployment",
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Retrieve build or deployment logs.

    Args:
        client: Railway API client
        deployment_id: Deployment ID
        log_type: Type of logs to retrieve ("build" or "deployment")
        limit: Maximum number of log entries

    Returns:
        List of log entries
    """
    if log_type == "build":
        query = GET_BUILD_LOGS_QUERY
        key = "buildLogs"
    else:
        query = GET_DEPLOYMENT_LOGS_QUERY
        key = "deploymentLogs"

    data = await client.execute(
        query,
        {"deploymentId": deployment_id, "limit": limit},
    )

    logs = data.get(key, [])
    return [
        {
            "message": log.get("message"),
            "timestamp": log.get("timestamp"),
            "severity": log.get("severity"),
        }
        for log in logs
    ]
