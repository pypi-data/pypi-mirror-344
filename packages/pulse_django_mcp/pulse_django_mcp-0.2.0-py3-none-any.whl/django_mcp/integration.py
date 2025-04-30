"""
Integration utilities for Django-MCP.

This module primarily provides the handler wrapper used by the
view discovery mechanism.
"""
import logging
import inspect

from django.http import HttpRequest
from typing import Callable

logger = logging.getLogger(__name__)

def create_handler_wrapper(handler: Callable) -> Callable:
    """
    Create a wrapper function for a handler that can be registered as an MCP tool.
    Handles passing the request object correctly if needed.
    """
    try:
        handler_sig = inspect.signature(handler)
        handler_expects_request = 'request' in handler_sig.parameters
    except ValueError: # Handle builtins or other uninspectable callables
        handler_expects_request = False
        logger.debug(f"Could not inspect signature for handler {getattr(handler, '__name__', 'unknown')}")

    # Create a wrapper function
    # Use *args, **kwargs to be flexible, but handle request specially
    async def wrapper_func(*args, **kwargs):
        final_kwargs = dict(kwargs)
        # Pop request first from kwargs, as it's the most likely place MCPToolService will put it
        request_obj = final_kwargs.pop('request', None) 

        # If request wasn't in kwargs, check if passed positionally (less likely now)
        # Check only for Django HttpRequest now
        if not request_obj and args and isinstance(args[0], HttpRequest):
             request_obj = args[0]
             args = args[1:] # Remove request from positional args
             logger.debug(f"Wrapper received request positionally for {getattr(handler, '__name__', 'unknown')}")

        # Prepare arguments for the actual handler
        handler_args = list(args)
        handler_kwargs = final_kwargs

        if handler_expects_request:
             if request_obj:
                 # Add request back to kwargs if the handler expects it
                 handler_kwargs['request'] = request_obj
                 logger.debug(f"Passing request object via kwargs to handler {getattr(handler, '__name__', 'unknown')}")
             else:
                  logger.warning(f"Handler {getattr(handler, '__name__', 'unknown')} expects 'request', but none was provided/found in wrapper args/kwargs.")
                  # Proceed without request? Or raise error? For now, proceed.

        # Forward the call to the handler with potentially modified args/kwargs
        # We assume the handler is async based on previous usage context
        return await handler(*handler_args, **handler_kwargs) 

    # Copy necessary attributes for SDK inspection if possible
    try:
        wrapper_func.__name__ = handler.__name__
        wrapper_func.__doc__ = handler.__doc__
        wrapper_func.__signature__ = inspect.signature(handler)
    except (AttributeError, TypeError, ValueError):
        logger.debug(f"Could not copy attributes from handler {getattr(handler, '__name__', 'unknown')} to wrapper.")
        
    return wrapper_func 