# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
uv sync                    # Install dependencies (includes dev)
uv run pytest              # Run all tests
uv run pytest tests/test_client.py -v  # Run specific test file
uv run ruff check .        # Lint
uv run ruff format .       # Format
uv run python -m railway_mcp  # Run server locally (requires RAILWAY_TOKEN env var)
```

**Docker:**
```bash
docker build -t railway-mcp .
docker run -e RAILWAY_TOKEN=<token> railway-mcp
```

## Architecture

This is an MCP (Model Context Protocol) server that enables AI assistants to deploy and manage Railway platform projects through Railway's GraphQL API.

**Core Components:**
- `src/railway_mcp/server.py` - FastMCP server setup, tool registration, lifespan management
- `src/railway_mcp/client.py` - Async GraphQL client (httpx-based) with auth and error handling
- `src/railway_mcp/config.py` - Pydantic Settings for `RAILWAY_TOKEN` and `RAILWAY_API_URL`
- `src/railway_mcp/exceptions.py` - Exception hierarchy (RailwayError base → AuthenticationError, GraphQLError, etc.)
- `src/railway_mcp/graphql/` - GraphQL queries and mutations as string constants

**Tool Modules (`src/railway_mcp/tools/`):**
Each module exposes async functions registered as MCP tools in server.py:
- `status.py` - API status verification
- `projects.py` - Project CRUD
- `services.py` - Service management and deployment triggers
- `deployments.py` - Deployment listing and log retrieval
- `environments.py` - Environment management
- `variables.py` - Environment variable operations (project/environment/service scoped)
- `domains.py` - Railway domain generation
- `templates.py` - Template library deployment (redis, postgres, etc.)

**Key Patterns:**
- All tool functions are async and receive `RailwayClient` from server context
- GraphQL operations use parameterized string constants (not dynamic query building)
- Tests use `respx` for HTTP mocking with `pytest-asyncio`

## Configuration

- `RAILWAY_TOKEN` (required) - Railway API token
- `RAILWAY_API_URL` (optional) - Defaults to `https://backboard.railway.com/graphql/v2`

## Docker MCP Registry

This server is designed for the Docker MCP Registry. Key files:
- `server.yaml` - MCP server metadata and config schema
- `tools.json` - Tool specifications for registry discovery
- `Dockerfile` - Multi-stage build with non-root user
