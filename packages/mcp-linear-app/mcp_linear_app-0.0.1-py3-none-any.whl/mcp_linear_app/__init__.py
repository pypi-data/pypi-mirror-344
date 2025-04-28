"""Linear MCP Server - Connect to Linear API through MCP."""

import sys
from . import server

__version__ = "0.0.1"

def main():
    """Main entry point for the package."""
    print("Starting Linear MCP server...", file=sys.stderr)
    server.mcp.run()

if __name__ == "__main__":
    main()
