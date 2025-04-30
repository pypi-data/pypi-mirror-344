"""
Utility functions for MCP processing.

This module provides utility functions for handling MCP requests.
"""
import logging
from typing import Dict, Callable

logger = logging.getLogger(__name__)

def get_registered_tools() -> Dict[str, Callable]:
    """
    Get the dictionary of registered MCP tools from the FastMCP server.

    This function retrieves the currently registered tools directly from the 
    underlying official MCP server instance managed by the `FastMCP` wrapper.
    It provides a convenient way to access the toolset without needing direct
    access to the `FastMCP` instance itself.
        
    Returns:
        A dictionary mapping tool names (str) to their corresponding callable 
        functions. Returns an empty dictionary if the server or tools 
        cannot be accessed.
    """
    try:
        # Import necessary modules locally to avoid potential top-level issues
        from django.apps import apps 
        from pulse_django_mcp.config import mcp_config
        
        # Get the server instance
        server = mcp_config.get_server()
        
        if not server:
            logger.warning("MCP server instance not found.")
            raise ValueError("Server not available") # Raise to go to except block
            
        # Navigate through the wrapper to the official server's tools
        if not (hasattr(server, '_official_server') and hasattr(server._official_server, '_mcp_server')):
            logger.warning("FastMCP server instance or its internal structure not found as expected.")
            raise ValueError("Server structure invalid") # Raise to go to except block
            
        mcp_server = server._official_server._mcp_server
        if not hasattr(mcp_server, 'tools'):
            logger.warning("FastMCP server found, but '_mcp_server.tools' attribute not present.")
            raise ValueError("Tools attribute missing") # Raise to go to except block

        # We have the tools dictionary, process it
        tools_dict = mcp_server.tools # This is the dict from the official SDK
        result = {}
        for name, tool_object in tools_dict.items(): 
            # Extract the actual callable function from the tool object
            handler_func = None
            if hasattr(tool_object, 'fn'):
                handler_func = tool_object.fn
            elif hasattr(tool_object, 'func'): # Check for 'func' attribute as well
                handler_func = tool_object.func 
            elif hasattr(tool_object, '__call__'): # Check if the tool object itself is callable
                handler_func = tool_object 
            
            if handler_func:
                result[name] = handler_func
            else:
                 logger.warning(f"Could not extract callable function for tool '{name}'")
                
        logger.debug(f"Retrieved {len(result)} tools from FastMCP server: {list(result.keys())}")
        return result
            
    except Exception as e:
        # Log the full exception for better debugging
        logger.warning(f"Failed to get tools from FastMCP server: {e}", exc_info=True)
    
    # If tools cannot be retrieved from the server, return an empty dictionary
    logger.warning("Could not retrieve tools from FastMCP server. Returning empty dictionary.")
    return {} 