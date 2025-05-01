"""
Django application configuration for Pulse Django MCP.

This module provides the AppConfig class for the Pulse Django MCP package,
handling settings, initialization, and auto-discovery.
"""
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import logging

logger = logging.getLogger(__name__)


class DjangoMCPConfig(AppConfig):
    """
    Django application configuration for Pulse Django MCP.
    
    This class manages the Pulse Django MCP application, including:
    - Configuration and settings
    - Server initialization
    - Auto-discovery of views and tools
    """
    
    name = 'pulse_django_mcp'
    verbose_name = 'Django MCP'
    
    def ready(self):
        """
        Initialize the Pulse Django MCP application when Django starts.
        
        This method is called by Django when the application is ready.
        It handles initialization tasks such as:
        - Loading settings
        - Setting up middleware
        - Auto-discovering MCP-compatible views
        """
        # Import here to avoid circular imports
        from pulse_django_mcp.config import mcp_config
        
        # Only proceed if MCP is enabled
        if not mcp_config.is_enabled():
            return
            
        # Create the MCP server if it doesn't exist yet
        if not hasattr(self, 'mcp_server'):
            from pulse_django_mcp.mcp_server import create_mcp_server
            
            # Get config settings for the server
            server_name = mcp_config.get('MCP_SERVER_NAME', 'Django MCP Server')
            server_description = mcp_config.get('MCP_SERVER_DESCRIPTION', 'MCP server for Django applications')
            app_name = mcp_config.get('MCP_APP_NAME', 'pulse_django_mcp')
            
            # Create the server
            self.mcp_server = create_mcp_server(
                name=server_name,
                description=server_description,
                app_name=app_name
            )
            
            logger.info(f"Created FastMCP server: {server_name}")
        
        # Then auto-discover views and tools if enabled
        if mcp_config.should_auto_discover():
            # Use the autodiscover function to discover and register views
            autodiscover()
            
            # Log discovered tools using the new FastMCP API
            if hasattr(self.mcp_server, '_official_server') and hasattr(self.mcp_server._official_server, '_mcp_server'):
                mcp_server = self.mcp_server._official_server._mcp_server
                if hasattr(mcp_server, 'tools'):
                    tool_names = list(mcp_server.tools.keys())
            logger.info(f"Discovered {len(tool_names)} MCP tools: {', '.join(tool_names)}")


# Auto-discovery function for Django apps
def autodiscover():
    """
    Auto-discover MCP-compatible views in installed Django apps.
    
    This function:
    1. Looks for 'mcp.py' modules in installed Django apps and imports them to register tools
    2. Discovers Django views and registers them as MCP tools
    """
    # Import standard mcp.py modules from apps
    autodiscover_modules('mcp')
    
    # Import here to avoid circular imports
    from pulse_django_mcp.config import mcp_config
    
    # Only proceed if auto-discovery is enabled
    if not mcp_config.should_auto_discover():
        return
    
    # Get the MCP server instance
    server = mcp_config.get_server()
    
    # If server is None, log warning and return
    if server is None:
        logger.warning("MCP server is not initialized, skipping view registration")
        return
    
    # Import here to avoid circular imports
    from pulse_django_mcp.discovery import ViewDiscovery
    
    # Discover views and register them as tools
    discovery = ViewDiscovery()
    discovery_settings = mcp_config.get_discovery_settings()
    
    # Filter apps based on settings
    include_apps = discovery_settings.get('include_apps', [])
    exclude_apps = discovery_settings.get('exclude_apps', [])
    
    if include_apps:
        # Discover views from specific apps
        for app_name in include_apps:
            if app_name not in exclude_apps:
                discovery.discover_app_views(app_name)
    else:
        # Discover all views
        discovery.discover_all_views()
    
    # Register views as tools with the FastMCP server
    discovery.register_views_as_tools(server) 