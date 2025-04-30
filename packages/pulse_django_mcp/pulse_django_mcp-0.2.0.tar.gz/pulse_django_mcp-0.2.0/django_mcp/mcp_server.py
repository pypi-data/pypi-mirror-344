"""
MCP Server module for Django-MCP.

Integrates the official MCP Python SDK (mcp.server.fastmcp.FastMCP) with Django.
"""
import logging
from typing import Any, Callable, List, Optional

# Official MCP SDK imports
from mcp.server.fastmcp import FastMCP as OfficialFastMCP
from mcp.server.fastmcp import Context as MCPContext # Expose context if needed
from mcp.server.sse import SseServerTransport

from django.urls import path, include
from django.http import HttpRequest

logger = logging.getLogger(__name__)

# Removed DjangoMCPServer class as the FastMCP wrapper will handle integration

class FastMCP:
    """
    Django wrapper for the official mcp.server.fastmcp.FastMCP server.
    
    Provides a convenient way to create an MCP server instance within a Django
    project and integrate its tool/resource/prompt registration and SSE 
    transport with Django's URL routing.

    This class acts as a bridge, offering a familiar decorator-based API 
    (`@mcp_instance.tool`, `@mcp_instance.resource`, `@mcp_instance.prompt`) 
    while delegating the core MCP logic to the official SDK.

    Attributes:
        server: The underlying `mcp.server.fastmcp.FastMCP` instance.
    """
    
    def __init__(self, name: str = "Django MCP Server", 
                 description: str = "MCP server for Django applications", **kwargs):
        """
        Initializes the FastMCP wrapper and the underlying official MCP server.

        Args:
            name: The name of the MCP server, used during initialization.
            description: A description of the MCP server.
            **kwargs: Additional keyword arguments passed directly to the 
                      `mcp.server.fastmcp.FastMCP` constructor (e.g., 
                      `dependencies`, `lifespan`).
        """
        self._official_server = OfficialFastMCP(
            name=name, 
            description=description, 
            **kwargs
        )
        # Do NOT initialize the transport here, it needs the endpoint first.
        # self._sse_transport = SseServerTransport() # REMOVED
        logger.info(f"Initialized FastMCP wrapper '{name}' using official mcp SDK.")

    @property
    def server(self) -> OfficialFastMCP:
        """Provides direct access to the underlying official FastMCP server instance."""
        return self._official_server
    
    def tool(self, func: Callable = None, *, name: Optional[str] = None, 
                     description: Optional[str] = None):
        """
        Register a function as an MCP tool.

        Can be used as a decorator (`@mcp_instance.tool`) or called directly 
        (`mcp_instance.tool(my_func, name=...)`). Delegates to the underlying 
        `FastMCP.tool()` from the official SDK.

        Args:
            func: The function to register (if not used as a decorator).
            name: Optional name for the tool (defaults to function name).
            description: Optional description (defaults to function docstring).

        Returns:
            The decorator function if `func` is None, otherwise the decorated function.
        """
        # Get the actual decorator function from the official server
        decorator = self._official_server.tool(name=name, description=description)
        if func is None:
            # Return the decorator itself to be applied by Python's @ syntax
            return decorator
        else:
            # Apply the decorator immediately if func is provided
            return decorator(func)

    def resource(self, path_uri: str, *, name: Optional[str] = None, description: Optional[str] = None):
        """
        Register a function as an MCP resource handler.

        Acts as a decorator. Delegates directly to the underlying
        `FastMCP.resource()` from the official SDK.

        Args:
            path_uri: The URI pattern for the resource (can include template variables).
            # name and description are typically inferred by the SDK decorator from the function

        Returns:
            A decorator.
        """
        # The SDK's resource decorator factory typically only takes the path_uri.
        # Name and description are usually handled when the returned decorator is applied.
        # We remove name and description arguments from this call.
        return self._official_server.resource(path_uri)
    
    def prompt(self, func: Callable = None, *, name: Optional[str] = None, description: Optional[str] = None):
        """
        Register a function as an MCP prompt template.

        Can be used as a decorator (`@mcp_instance.prompt`) or called directly.
        Delegates to the underlying `FastMCP.prompt()` from the official SDK.

        Args:
            func: The function generating the prompt text (if not used as a decorator).
            name: Optional name for the prompt (defaults to function name).
            description: Optional description (defaults to function docstring).

        Returns:
            The decorator function if `func` is None, otherwise the decorated function.
        """
        # Get the actual decorator function from the official server
        decorator = self._official_server.prompt(name=name, description=description)
        if func is None:
            # Return the decorator itself
            return decorator
        else:
            # Apply the decorator immediately
            return decorator(func)
    
    def get_asgi_app(self) -> Callable:
        """
        Returns an ASGI application callable that integrates the MCP server
        with the SSE transport.

        This ASGI app handles the MCP communication over Server-Sent Events,
        linking the transport layer to the underlying MCP server's run loop.
        It should be mounted within your main Django ASGI application setup.
            
        Returns:
            An ASGI application callable (the transport instance itself).
        """
        # 1. Define the core ASGI application logic for the MCP server.
        #    This function will handle the actual MCP request processing.
        async def core_mcp_server_logic(reader, writer):
            await self._official_server._mcp_server.run(
                reader,
                writer,
                self._official_server._mcp_server.create_initialization_options(),
            )

        # 2. Initialize the SSE transport, providing the core server logic
        #    as the required 'endpoint'.
        sse_transport = SseServerTransport(endpoint=core_mcp_server_logic)

        # 3. Return the transport instance itself. It acts as the ASGI app
        #    that handles SSE connections and delegates to the endpoint.
        return sse_transport
        
    def get_urls(self, prefix: str = "") -> List[Any]:
        """
        Generates a list containing a Django URL pattern for the MCP SSE endpoint.

        This is the primary way to expose the MCP server to clients via HTTP.
        The single SSE endpoint handles all MCP communication (list, call, etc.).

        Args:
            prefix: Optional URL prefix for the SSE endpoint (e.g., "mcp/").
                    If provided, it should not start but should end with a slash.
                    Defaults to "".
            
        Returns:
            A list containing a Django `path()` object for the SSE endpoint.
        """
        # Ensure prefix formatting (e.g., "mcp/")
        if prefix and not prefix.endswith('/'):
            prefix += '/'
        if prefix.startswith('/'):
             prefix = prefix.lstrip('/')
            
        # Define the final path for the SSE endpoint
        sse_path = f'{prefix}sse/'
        
        # Define an async Django view to wrap the ASGI application
        async def sse_view(request: HttpRequest):
             # Extract ASGI scope, receive, send from the Django request
             scope = request.scope
             receive = getattr(request, 'receive', None) # Standard ASGI receive
             send = getattr(request, 'send', None) # Standard ASGI send
             
             # Check if receive and send are available (might differ in test clients)
             if receive is None or send is None:
                 logger.error("ASGI receive/send not found on request object. Cannot handle MCP SSE request.")
                 # Return an appropriate error response for Django
                 from django.http import HttpResponseServerError
                 return HttpResponseServerError("ASGI channels not available.")

             # Get the correctly initialized ASGI app (transport) on demand
             asgi_app = self.get_asgi_app()
             # Delegate the request handling to the MCP ASGI app (transport)
             await asgi_app(scope, receive, send)
             
             # The ASGI app handles the response directly via the 'send' channel.
             # Return None or an empty response to satisfy Django's view requirements.
             # An empty response might be safer in some edge cases.
             from django.http import HttpResponse
             return HttpResponse() # Return an empty response

        logger.info(f"Generating MCP SSE URL pattern at path: '{sse_path}'")
        return [
            path(sse_path, sse_view, name="mcp_sse_endpoint")
        ]

# Expose the MCP Context type for convenience in tool definitions
MCPContext = MCPContext 

def create_mcp_server(name: str = "Django MCP Server", 
                     description: str = "MCP server for Django applications",
                    **kwargs) -> FastMCP:
    """
    Convenience factory function to create and return a FastMCP instance.
    
    This simplifies the creation of the server wrapper, especially when
    initializing it within Django's app configuration (`apps.py`).
    
    Args:
        name: The name for the MCP server.
        description: The description for the MCP server.
        **kwargs: Additional arguments passed directly to the `FastMCP` constructor.
        
    Returns:
        A new `FastMCP` instance.
    """
    return FastMCP(name=name, description=description, **kwargs) 