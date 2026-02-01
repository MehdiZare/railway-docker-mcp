# Docker MCP Registry Submission Guide

This guide provides step-by-step instructions for submitting the Railway MCP server to the Docker MCP Registry.

## Prerequisites

- [ ] GitHub CLI (`gh`) installed and authenticated
- [ ] Docker Desktop installed (for local testing)
- [ ] Go Task runner installed (`brew install go-task` or see https://taskfile.dev)

## Submission Files

The following files are ready for submission in this directory:

| File | Description |
|------|-------------|
| `server.yaml` | Server metadata, configuration, and secrets schema |
| `tools.json` | All 17 MCP tools in Docker registry format |

---

## Step 1: Fork the Docker MCP Registry

```bash
# Navigate to your preferred directory for cloning
cd ~/REPOs  # or your preferred location

# Fork and clone the registry
gh repo fork docker/mcp-registry --clone

# Navigate into the cloned repo
cd mcp-registry
```

## Step 2: Create a Feature Branch

```bash
git checkout -b add-railway-mcp
```

## Step 3: Copy Submission Files

```bash
# Create the server directory
mkdir -p servers/railway-mcp

# Copy the prepared files (adjust path as needed)
cp /path/to/railway-docker-mcp/docker-mcp-submission/server.yaml servers/railway-mcp/
cp /path/to/railway-docker-mcp/docker-mcp-submission/tools.json servers/railway-mcp/
```

## Step 4: Local Testing (Recommended)

Before submitting, validate the server builds correctly:

```bash
# Build the catalog for railway-mcp
task build -- --tools railway-mcp

# Generate the catalog
task catalog -- railway-mcp

# Import into Docker Desktop (requires Docker Desktop running)
docker mcp catalog import $PWD/catalogs/railway-mcp/catalog.yaml
```

### Verify in Docker Desktop

1. Open Docker Desktop
2. Go to Settings → Features in Development → Enable MCP Toolkit
3. Navigate to MCP Toolkit section
4. Verify "railway-mcp" appears in the catalog
5. Try configuring it with a test Railway token

## Step 5: Commit and Push

```bash
git add servers/railway-mcp
git commit -m "Add railway-mcp server"
git push -u origin add-railway-mcp
```

## Step 6: Create Pull Request

```bash
gh pr create \
  --title "Add railway-mcp server" \
  --body "$(cat <<'EOF'
## Summary

Adds Railway MCP server for deploying and managing Railway platform projects, services, environments, and deployments through an MCP interface.

## Server Details

- **Name**: railway-mcp
- **Category**: cloud
- **Source**: https://github.com/MehdiZare/railway-docker-mcp

## Tools Included (17 total)

### Project Management
- `check_railway_status` - Verify API access and authentication
- `list_projects` - List all accessible Railway projects
- `create_project_and_link` - Create a new Railway project

### Service Management
- `list_services` - List services in a project
- `link_service` - Get service details for context/linking
- `deploy` - Trigger deployment for a service

### Deployment Management
- `list_deployments` - List deployments with status
- `get_logs` - Retrieve build or deployment logs

### Environment Management
- `list_environments` - List environments in a project
- `create_environment` - Create a new environment
- `link_environment` - Get environment details

### Variable Management
- `list_variables` - List environment variables (masked by default)
- `set_variables` - Set environment variables

### Domain Management
- `generate_domain` - Generate a railway.app domain

### Template Library
- `list_templates` - List available templates
- `get_template` - Get template details
- `deploy_template` - Deploy from template library (redis, postgres, etc.)

## Configuration

Requires a single secret:
- `RAILWAY_TOKEN` - Railway API token

## Testing

- [ ] Built successfully with `task build -- --tools railway-mcp`
- [ ] Catalog generated with `task catalog -- railway-mcp`
- [ ] Imported into Docker Desktop MCP Toolkit

EOF
)"
```

## Step 7: Post-Submission

### Share Test Credentials (If Requested)

If the Docker team requests test credentials for validation:
1. Create a temporary Railway API token with limited scope
2. Submit via: https://forms.gle/6Lw3nsvu2d6nFg8e6
3. Revoke the token after review is complete

### Monitor PR Status

- Watch for CI checks to pass
- Respond to any review feedback
- The Docker team typically reviews within a few business days

---

## Troubleshooting

### Build Fails

```bash
# Check for YAML syntax errors
python3 -c "import yaml; yaml.safe_load(open('servers/railway-mcp/server.yaml'))"

# Check for JSON syntax errors
python3 -c "import json; json.load(open('servers/railway-mcp/tools.json'))"
```

### Catalog Import Fails

1. Ensure Docker Desktop is running
2. Verify MCP Toolkit feature is enabled in Docker Desktop settings
3. Check Docker Desktop logs for errors

### CI Validation Errors

The registry has automated validation. Common issues:
- Missing required fields in `server.yaml`
- Invalid tool argument format in `tools.json`
- Commit hash doesn't exist in source repository

---

## Reference Links

- [Docker MCP Registry](https://github.com/docker/mcp-registry)
- [Contributing Guide](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)
- [Railway MCP Source](https://github.com/MehdiZare/railway-docker-mcp)
- [Railway API Documentation](https://docs.railway.app/reference/public-api)

---

## Contact

For questions about this submission:
- Railway MCP Issues: https://github.com/MehdiZare/railway-docker-mcp/issues
- Docker MCP Registry Issues: https://github.com/docker/mcp-registry/issues
