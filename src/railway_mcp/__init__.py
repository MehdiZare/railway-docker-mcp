"""Railway MCP Server - Deploy and manage Railway projects via MCP."""

from .server import mcp

__version__ = "0.1.0"


def main():
    """Run the MCP server."""
    mcp.run()


__all__ = ["__version__", "main", "mcp"]
