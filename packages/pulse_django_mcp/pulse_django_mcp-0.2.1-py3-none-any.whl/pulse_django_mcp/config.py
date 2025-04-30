"""
Configuration module for Pulse Django MCP integration.

This module provides configuration utilities for integrating Pulse Django MCP
into Django projects, handling settings and defaults.
"""
from typing import Any, Dict, List, Optional, Union

from django.conf import settings
from django.utils.module_loading import import_string
import logging

logger = logging.getLogger(__name__)


class MCPConfig:
    """
    Manages configuration for the Pulse Django MCP integration.

    Reads settings from Django's `settings.py`, applies defaults for missing
    values, and provides convenient access methods.
    
    It acts as a singleton, accessed via the `mcp_config` instance.
    """
    
    # Default settings
    DEFAULTS = {
        # General MCP settings
        'MCP_ENABLED': True, # Whether to enable the MCP integration
        'MCP_BASE_URL': '/mcp/', # Base URL prefix for MCP endpoints (used by get_urls)
        
        # Server settings (used by FastMCP wrapper)
        'MCP_SERVER_NAME': 'Pulse Django MCP Server', # Name reported by the MCP server
        'MCP_SERVER_DESCRIPTION': 'MCP server for Django integration', # Description reported by the MCP server
        
        # Discovery settings
        'MCP_AUTO_DISCOVER': True, # Automatically discover Django views as tools
        'MCP_INCLUDE_APPS': [], # List of apps to specifically include in discovery (empty means all)
        'MCP_EXCLUDE_APPS': [], # List of apps to specifically exclude from discovery
        'MCP_INCLUDE_PATHS': [], # List of URL path prefixes to include (empty means all)
        'MCP_EXCLUDE_PATHS': [], # List of URL path prefixes to exclude
        
        # Settings below are commented out as they relate to removed/unused features
        # 'MCP_CONVERSATION_STORAGE': 'pulse_django_mcp.storage.DatabaseStorage',
        # 'MCP_CONVERSATION_TTL': 3600, 
        # 'MCP_FORMAT_RESPONSES': True,
        # 'MCP_INCLUDE_SCHEMA_LINKS': True,
        # 'MCP_PRESERVE_RESPONSE_FORMAT': False,
        # 'MCP_MIDDLEWARE_CLASSES': [], 
        # 'MCP_TOOL_REGISTRY_CLASS': 'pulse_django_mcp.registry.ToolRegistry',
        # 'MCP_SERVER_CLASS': 'pulse_django_mcp.server.MCPServer',
    }
    
    def __init__(self):
        """Initializes the configuration object, setting cache attributes to None."""
        self._cached_settings = None
        self._cached_server = None
    
    def _get_setting(self, name: str) -> Any:
        """Internal helper to retrieve a setting value, using defaults."""
        if hasattr(settings, name):
            return getattr(settings, name)
        return self.DEFAULTS.get(name)
    
    @property
    def settings(self) -> Dict[str, Any]:
        """
        Provides access to all resolved MCP settings (Django settings + defaults).
        
        Caches the result after the first access.
        
        Returns:
            A dictionary containing all MCP settings.
        """
        if self._cached_settings is None:
            self._cached_settings = {
                name: self._get_setting(name) for name in self.DEFAULTS
            }
        return self._cached_settings
    
    def get(self, name: str, default: Any = None) -> Any:
        """
        Gets a specific setting value by name.
        
        Args:
            name: The name of the setting (e.g., 'MCP_ENABLED').
            default: A fallback value if the setting is not found in Django
                     settings or the defaults.
            
        Returns:
            The resolved setting value.
        """
        return self.settings.get(name, default)
    
    def get_server(self) -> Any:
        """
        Gets or creates the singleton `FastMCP` server instance for the project.

        Uses cached instance if available, otherwise creates a new one based on
        `MCP_SERVER_NAME` and `MCP_SERVER_DESCRIPTION` settings.
        
        Returns:
            The singleton `pulse_django_mcp.mcp_server.FastMCP` instance.
        """
        # Check if we already have a cached server instance
        if hasattr(self, '_cached_server') and self._cached_server is not None:
            return self._cached_server
            
        # Import here to avoid circular imports
        from pulse_django_mcp.mcp_server import FastMCP, create_mcp_server
        
        # Create a new server instance
        server_name = self.get('MCP_SERVER_NAME', 'Pulse Django MCP Server')
        server_description = self.get('MCP_SERVER_DESCRIPTION', 'MCP server for Django integration')
        
        # Create the server using the utility function
        self._cached_server = create_mcp_server(
            name=server_name, 
            description=server_description,
        )
        
        return self._cached_server
    
    def is_enabled(self) -> bool:
        """Checks if the MCP integration is enabled via the `MCP_ENABLED` setting."""
        return self.get('MCP_ENABLED', True)
    
    def get_base_url(self) -> str:
        """Gets the base URL prefix for MCP endpoints from `MCP_BASE_URL` setting."""
        return self.get('MCP_BASE_URL', '/mcp/')
    
    def should_auto_discover(self) -> bool:
        """Checks if view auto-discovery is enabled via `MCP_AUTO_DISCOVER`."""
        return self.get('MCP_AUTO_DISCOVER', True)
    
    def get_middleware_classes(self) -> List[str]:
        """Gets the list of middleware classes (currently unused after refactor)."""
        return self.get('MCP_MIDDLEWARE_CLASSES', [])
    
    def is_path_included(self, path: str) -> bool:
        """
        Checks if a given URL path should be included in MCP view discovery.
        
        Considers `MCP_INCLUDE_PATHS` and `MCP_EXCLUDE_PATHS` settings.
        (Note: `MCP_PATHS` setting seems unused/obsolete).
        
        Args:
            path: The URL path string to check.
            
        Returns:
            `True` if the path should be included, `False` otherwise.
        """
        included = False
        
        # Check include paths
        include_paths = self.get('MCP_INCLUDE_PATHS', [])
        if include_paths:
            included = any(path.startswith(p) for p in include_paths)
        else:
            # If include_paths is empty, consider all paths included by default
            # unless excluded later.
             included = True 
                
        # Check exclude paths, which take precedence
        exclude_paths = self.get('MCP_EXCLUDE_PATHS', [])
        if exclude_paths and included:
            if any(path.startswith(p) for p in exclude_paths):
                included = False
                
        return included
    
    def get_auth_settings(self) -> Dict[str, Any]:
        """
        Get all authentication-related settings.
        
        Returns:
            A dictionary of authentication settings
        """
        return {
            'require_auth': self.get('MCP_REQUIRE_AUTH', True),
            'backends': self.get('MCP_AUTH_BACKENDS', []),
            'jwt_secret': self.get('MCP_JWT_SECRET'),
            'jwt_algorithm': self.get('MCP_JWT_ALGORITHM', 'HS256'),
            'token_header': self.get('MCP_TOKEN_HEADER', 'Authorization'),
        }
    
    def get_discovery_settings(self) -> Dict[str, Any]:
        """
        Returns a dictionary containing all settings relevant to view discovery.
        """
        return {
            'auto_discover': self.get('MCP_AUTO_DISCOVER', True),
            'include_apps': self.get('MCP_INCLUDE_APPS', []),
            'exclude_apps': self.get('MCP_EXCLUDE_APPS', []),
            'include_paths': self.get('MCP_INCLUDE_PATHS', []),
            'exclude_paths': self.get('MCP_EXCLUDE_PATHS', []),
        }


# Create a singleton instance for easy access throughout the project
mcp_config = MCPConfig() 