# Railway MCP Server

A Model Context Protocol (MCP) server for the [Railway](https://railway.app) platform. Deploy and manage Railway projects, services, environments, and deployments through MCP-compatible AI assistants.

## Features

- **Project Management**: List, create, and manage Railway projects
- **Service Operations**: List services, trigger deployments, manage configurations
- **Environment Management**: Create environments, manage environment variables
- **Deployment Control**: List deployments, retrieve build/deployment logs
- **Domain Generation**: Generate railway.app domains for services
- **Template Deployment**: Deploy from Railway's Template Library

## Tools

| Tool | Description |
|------|-------------|
| `check_railway_status` | Verify API access and authentication |
| `list_projects` | List all accessible Railway projects |
| `create_project_and_link` | Create a new project |
| `list_services` | List services in a project |
| `link_service` | Get service details for context |
| `deploy` | Trigger deployment for a service |
| `list_deployments` | List deployments for a service |
| `get_logs` | Retrieve build/deployment logs |
| `create_environment` | Create new environment |
| `link_environment` | Get environment details for context |
| `list_variables` | List environment variables |
| `set_variables` | Set environment variables |
| `generate_domain` | Generate railway.app domain |
| `deploy_template` | Deploy from Railway Template Library |

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/MehdiZare/railway-docker-mcp.git
cd railway-docker-mcp

# Install dependencies
uv sync

# Run the server
RAILWAY_TOKEN=your_token uv run python -m railway_mcp
```

### Using pip

```bash
pip install railway-mcp
```

### Using Docker

```bash
docker build -t railway-mcp .
docker run -e RAILWAY_TOKEN=your_token railway-mcp
```

## Configuration

The server requires a Railway API token for authentication:

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `RAILWAY_TOKEN` | Yes | Railway API token |
| `RAILWAY_API_URL` | No | Custom API URL (default: `https://backboard.railway.com/graphql/v2`) |

### Getting a Railway Token

1. Go to [Railway Dashboard](https://railway.app/account/tokens)
2. Create a new API token
3. Set the `RAILWAY_TOKEN` environment variable

## Usage with MCP Clients

### Claude Desktop

Add to your Claude Desktop configuration (`~/.config/claude/claude_desktop_config.json` on Linux/macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "railway": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/railway-docker-mcp", "python", "-m", "railway_mcp"],
      "env": {
        "RAILWAY_TOKEN": "your_token"
      }
    }
  }
}
```

### Docker MCP

```json
{
  "mcpServers": {
    "railway": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "RAILWAY_TOKEN", "railway-mcp"],
      "env": {
        "RAILWAY_TOKEN": "your_token"
      }
    }
  }
}
```

## Development

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .

# Format code
uv run ruff format .
```

### Testing with MCP Inspector

```bash
RAILWAY_TOKEN=your_token npx @modelcontextprotocol/inspector uv run python -m railway_mcp
```

## License

MIT License - see [LICENSE](LICENSE) for details.
