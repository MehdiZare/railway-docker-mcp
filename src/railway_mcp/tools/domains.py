"""Domain tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import CREATE_SERVICE_DOMAIN_MUTATION


async def generate_domain(
    client: RailwayClient,
    service_id: str,
    environment_id: str,
) -> dict[str, Any]:
    """Generate a railway.app domain for a service.

    Args:
        client: Railway API client
        service_id: Service ID
        environment_id: Environment ID

    Returns:
        Created domain information
    """
    data = await client.execute(
        CREATE_SERVICE_DOMAIN_MUTATION,
        {"serviceId": service_id, "environmentId": environment_id},
    )
    domain = data.get("serviceDomainCreate", {})

    return {
        "id": domain.get("id"),
        "domain": domain.get("domain"),
        "suffix": domain.get("suffix"),
        "fullDomain": f"{domain.get('domain')}.{domain.get('suffix')}"
        if domain.get("domain") and domain.get("suffix")
        else domain.get("domain"),
    }
