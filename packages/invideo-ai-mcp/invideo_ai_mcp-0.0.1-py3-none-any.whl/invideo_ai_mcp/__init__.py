"""InVideo AI MCP - API client and MCP server for InVideo AI API interaction."""

__version__ = "0.0.1"

from invideo_ai_mcp.api_client import InVideoApiClient
from invideo_ai_mcp.server import main, mcp

__all__ = ["InVideoApiClient", "mcp", "main"]
