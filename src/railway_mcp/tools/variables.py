"""Variable tools."""

from typing import Any

from ..client import RailwayClient
from ..graphql.mutations import SET_VARIABLES_MUTATION
from ..graphql.queries import LIST_VARIABLES_QUERY


async def list_variables(
    client: RailwayClient,
    project_id: str,
    environment_id: str,
    service_id: str | None = None,
    include_values: bool = False,
) -> dict[str, str]:
    """List environment variables.

    Args:
        client: Railway API client
        project_id: Project ID
        environment_id: Environment ID
        service_id: Optional service ID (for service-specific variables)
        include_values: If True, return actual values; if False, return masked values

    Returns:
        Dictionary of variable names and values (masked or actual based on include_values)
    """
    variables = {
        "projectId": project_id,
        "environmentId": environment_id,
    }
    if service_id:
        variables["serviceId"] = service_id

    data = await client.execute(LIST_VARIABLES_QUERY, variables)

    # The variables query returns a JSON object directly
    result = data.get("variables", {})

    if not include_values:
        # Mask all values for security
        return dict.fromkeys(result, "***")

    return result


async def set_variables(
    client: RailwayClient,
    project_id: str,
    environment_id: str,
    variables: dict[str, str],
    service_id: str | None = None,
) -> dict[str, Any]:
    """Set environment variables.

    Args:
        client: Railway API client
        project_id: Project ID
        environment_id: Environment ID
        variables: Dictionary of variable names and values to set
        service_id: Optional service ID (for service-specific variables)

    Returns:
        Result of the operation
    """
    mutation_variables = {
        "projectId": project_id,
        "environmentId": environment_id,
        "variables": variables,
    }
    if service_id:
        mutation_variables["serviceId"] = service_id

    data = await client.execute(SET_VARIABLES_MUTATION, mutation_variables)

    # variableCollectionUpsert returns a boolean
    success = data.get("variableCollectionUpsert", False)

    return {
        "success": success,
        "variablesSet": list(variables.keys()),
        "message": "Variables set successfully" if success else "Failed to set variables",
    }
