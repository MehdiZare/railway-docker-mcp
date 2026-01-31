"""FastMCP server for Railway."""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from fastmcp import Context, FastMCP

from .client import RailwayClient
from .config import get_settings
from .tools import deployments as deployment_tools
from .tools import domains as domain_tools
from .tools import environments as environment_tools
from .tools import projects as project_tools
from .tools import services as service_tools
from .tools import status as status_tools
from .tools import templates as template_tools
from .tools import variables as variable_tools


@dataclass
class AppContext:
    """Application context holding the Railway client."""

    client: RailwayClient


@asynccontextmanager
async def lifespan(mcp: FastMCP):
    """Manage server lifecycle - initialize and cleanup Railway client."""
    settings = get_settings()
    client = RailwayClient(settings.railway_token, settings.railway_api_url)

    async with client:
        # Verify token on startup
        await client.verify_token()
        yield AppContext(client=client)


# Create the MCP server
mcp = FastMCP(
    "railway-mcp",
    instructions="MCP server for Railway platform - deploy and manage Railway projects",
    lifespan=lifespan,
)


def get_client(ctx: Context) -> RailwayClient:
    """Get Railway client from context."""
    app_ctx: AppContext = ctx.request_context.lifespan_context
    return app_ctx.client


# Status tool
@mcp.tool()
async def check_railway_status(ctx: Context) -> dict[str, Any]:
    """Verify API access and authentication.

    Returns the current user's information if authenticated.
    """
    client = get_client(ctx)
    return await status_tools.check_railway_status(client)


# Project tools
@mcp.tool()
async def list_projects(ctx: Context) -> list[dict[str, Any]]:
    """List all accessible Railway projects.

    Returns a list of projects with their environments and services.
    """
    client = get_client(ctx)
    return await project_tools.list_projects(client)


@mcp.tool()
async def create_project_and_link(
    ctx: Context,
    name: str,
    description: str | None = None,
    default_environment_name: str | None = None,
) -> dict[str, Any]:
    """Create a new Railway project.

    Args:
        name: Project name
        description: Optional project description
        default_environment_name: Name for the default environment (defaults to "production")

    Returns the created project information.
    """
    client = get_client(ctx)
    return await project_tools.create_project_and_link(
        client, name, description, default_environment_name
    )


# Service tools
@mcp.tool()
async def list_services(ctx: Context, project_id: str) -> list[dict[str, Any]]:
    """List services in a project.

    Args:
        project_id: The Railway project ID
    """
    client = get_client(ctx)
    return await service_tools.list_services(client, project_id)


@mcp.tool()
async def link_service(ctx: Context, service_id: str) -> dict[str, Any]:
    """Get service details for context/linking.

    Args:
        service_id: The Railway service ID
    """
    client = get_client(ctx)
    return await service_tools.link_service(client, service_id)


@mcp.tool()
async def deploy(ctx: Context, service_id: str, environment_id: str) -> dict[str, Any]:
    """Trigger deployment for a service.

    Args:
        service_id: The Railway service ID
        environment_id: The Railway environment ID to deploy to
    """
    client = get_client(ctx)
    return await service_tools.deploy(client, service_id, environment_id)


# Deployment tools
@mcp.tool()
async def list_deployments(
    ctx: Context,
    service_id: str,
    environment_id: str,
    limit: int = 10,
) -> list[dict[str, Any]]:
    """List deployments for a service.

    Args:
        service_id: The Railway service ID
        environment_id: The Railway environment ID
        limit: Maximum number of deployments to return (default: 10)
    """
    client = get_client(ctx)
    return await deployment_tools.list_deployments(client, service_id, environment_id, limit)


@mcp.tool()
async def get_logs(
    ctx: Context,
    deployment_id: str,
    log_type: str = "deployment",
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Retrieve build or deployment logs.

    Args:
        deployment_id: The Railway deployment ID
        log_type: Type of logs to retrieve - "build" or "deployment" (default: "deployment")
        limit: Maximum number of log entries (default: 100)
    """
    client = get_client(ctx)
    return await deployment_tools.get_logs(client, deployment_id, log_type, limit)


# Environment tools
@mcp.tool()
async def create_environment(
    ctx: Context,
    project_id: str,
    name: str,
) -> dict[str, Any]:
    """Create a new environment in a project.

    Args:
        project_id: The Railway project ID
        name: Name for the new environment
    """
    client = get_client(ctx)
    return await environment_tools.create_environment(client, project_id, name)


@mcp.tool()
async def link_environment(
    ctx: Context,
    project_id: str,
    environment_id: str,
) -> dict[str, Any]:
    """Get environment details for context/linking.

    Args:
        project_id: The Railway project ID
        environment_id: The Railway environment ID
    """
    client = get_client(ctx)
    return await environment_tools.link_environment(client, project_id, environment_id)


# Variable tools
@mcp.tool()
async def list_variables(
    ctx: Context,
    project_id: str,
    environment_id: str,
    service_id: str | None = None,
) -> dict[str, str]:
    """List environment variables.

    Args:
        project_id: The Railway project ID
        environment_id: The Railway environment ID
        service_id: Optional service ID for service-specific variables
    """
    client = get_client(ctx)
    return await variable_tools.list_variables(client, project_id, environment_id, service_id)


@mcp.tool()
async def set_variables(
    ctx: Context,
    project_id: str,
    environment_id: str,
    variables: dict[str, str],
    service_id: str | None = None,
) -> dict[str, Any]:
    """Set environment variables.

    Args:
        project_id: The Railway project ID
        environment_id: The Railway environment ID
        variables: Dictionary of variable names and values to set
        service_id: Optional service ID for service-specific variables
    """
    client = get_client(ctx)
    return await variable_tools.set_variables(
        client, project_id, environment_id, variables, service_id
    )


# Domain tools
@mcp.tool()
async def generate_domain(
    ctx: Context,
    service_id: str,
    environment_id: str,
) -> dict[str, Any]:
    """Generate a railway.app domain for a service.

    Args:
        service_id: The Railway service ID
        environment_id: The Railway environment ID
    """
    client = get_client(ctx)
    return await domain_tools.generate_domain(client, service_id, environment_id)


# Template tools
@mcp.tool()
async def deploy_template(
    ctx: Context,
    project_id: str,
    environment_id: str,
    template_code: str,
    services: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Deploy from Railway Template Library.

    Args:
        project_id: The Railway project ID to deploy to
        environment_id: The Railway environment ID to deploy to
        template_code: Template code (e.g., "redis", "postgres", "mysql")
        services: Optional list of service configurations
    """
    client = get_client(ctx)
    return await template_tools.deploy_template(
        client, project_id, environment_id, template_code, services
    )
