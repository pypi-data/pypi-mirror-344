"""
HTTP tools for converting Django views to MCP tools.

This module provides utilities for converting Django views into MCP tools,
leveraging the official MCP SDK for tool registration and schema generation.
"""
import inspect
import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Union, get_type_hints

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

logger = logging.getLogger(__name__)


def convert_view_to_tool(view_func: Callable) -> Callable:
    """
    Convert a Django view function to an MCP tool.
    
    This wrapper prepares a Django view function to be compatible with the MCP SDK.
    It preserves the original functionality when called as a Django view,
    but allows it to be registered with an MCP server.
    
    Args:
        view_func: The Django view function to convert.
        
    Returns:
        A wrapped function that can be used as both a Django view and an MCP tool.
    """
    @wraps(view_func)
    def wrapper(request: Optional[HttpRequest] = None, **kwargs) -> Any:
        # If called as a Django view, call the original function
        if request is not None and isinstance(request, HttpRequest):
            return view_func(request, **kwargs)
        
        # Otherwise, it's being called as an MCP tool
        return _execute_tool(view_func, None, **kwargs)
    
    # Copy the docstring and signature to help the SDK extract metadata
    wrapper.__doc__ = view_func.__doc__
    wrapper.__signature__ = inspect.signature(view_func)
    
    return wrapper


def convert_class_based_view_to_tool(view_class: Type[View]) -> Callable:
    """
    Convert a Django class-based view to an MCP tool.
    
    Args:
        view_class: The Django class-based view to convert.
        
    Returns:
        A function that acts as an MCP tool.
    """
    # Find the HTTP method handlers in the view class
    http_methods = []
    for method_name in ('get', 'post', 'put', 'patch', 'delete'):
        if hasattr(view_class, method_name):
            http_methods.append(method_name)
    
    # Use the first available method (prioritizing GET/POST)
    method_name = 'get' if 'get' in http_methods else (
        'post' if 'post' in http_methods else http_methods[0]
    )
    
    method = getattr(view_class, method_name)
    
    # Create a tool function
    @wraps(method)
    def tool_func(**kwargs) -> Any:
        return _execute_tool(view_class, method_name, **kwargs)
    
    # Copy documentation for the SDK to use
    tool_func.__doc__ = view_class.__doc__ or (method.__doc__ if method else "")
    if method:
        tool_func.__signature__ = inspect.signature(method)
    
    return tool_func


def _execute_tool(view, method_name=None, **kwargs) -> Any:
    """
    Execute a view as an MCP tool.
    
    This function handles different types of views (function-based, class-based)
    and different response types.
    
    Args:
        view: The view function or class.
        method_name: The HTTP method name for class-based views.
        **kwargs: The parameters for the view.
        
    Returns:
        The result of executing the view, converted to a format suitable for MCP.
    """
    response = None
    
    # Create an empty request object
    request = None
    
    # Handle class-based views
    if inspect.isclass(view):
        view_instance = view()
        
        # Set the request format to JSON for DRF views
        if hasattr(view_instance, 'format_kwarg'):
            kwargs[view_instance.format_kwarg] = 'json'
        
        try:
            # Call the appropriate method
            method = getattr(view_instance, method_name or 'get')
            response = method(request, **kwargs)
        except Exception as e:
            logger.exception(f"Error executing view method: {str(e)}")
            raise
    else:
        try:
            # Function-based view
            response = view(request, **kwargs)
        except Exception as e:
            logger.exception(f"Error executing view function: {str(e)}")
            raise
    
    # Process the response
    return _process_response(response)


def _process_response(response) -> Any:
    """
    Process a Django/DRF response into a format suitable for MCP.
    
    Args:
        response: The Django/DRF response.
        
    Returns:
        The processed response data.
    """
    # If response is already a dict or list, return it directly
    if isinstance(response, (dict, list)):
        return response
    
    # Handle Django HttpResponse
    if isinstance(response, HttpResponse):
        # If it's a JsonResponse, extract the data
        if isinstance(response, JsonResponse):
            return response.data if hasattr(response, 'data') else response.content
        
        # Otherwise, try to convert content to string
        try:
            return response.content.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            return str(response)
    
    # Handle DRF Response
    if hasattr(response, 'data'):
        return response.data
    
    # If we can't determine the format, return the response as is
    return response