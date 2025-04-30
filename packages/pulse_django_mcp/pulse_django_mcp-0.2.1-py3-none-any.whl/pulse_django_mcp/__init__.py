"""
Django MCP - Django integration for Model Context Protocol (MCP).

This package provides tools for integrating Django applications with the
Model Context Protocol (MCP), enabling the use of AI assistants to control
your application.

Use the FastMCP class to initialize and integrate the MCP server.
"""

__version__ = "0.2.0"

# Import the main integration class and context type
from .mcp_server import FastMCP, MCPContext, create_mcp_server

# Removed imports from old server/tools modules:
# from .tools import register_tool
# from .utils import get_registered_tools
# from .server import MCPServer # Deleted
# from .mcp_server import DjangoMCPServer # Removed

__all__ = [
    # "register_tool", # Removed
    # "get_registered_tools", # Removed
    # "MCPServer", # Removed
    # "DjangoMCPServer", # Removed
    "FastMCP",          # The main server wrapper class
    "MCPContext",       # Context type for tool definitions
    "create_mcp_server",# Convenience function to create a server instance
    # Potentially add ViewDiscovery if it's meant to be public?
    # "ViewDiscovery",
    # Potentially add mcp_config if direct access is intended?
    # "mcp_config",
] 