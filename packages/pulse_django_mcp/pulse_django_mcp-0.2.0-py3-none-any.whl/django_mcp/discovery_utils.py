"""
Utility classes and functions for view discovery in Django MCP.

This module provides helper classes and utilities used by the discovery process,
including ViewInfo class for storing metadata about views and serialization utilities.
"""
import inspect
import logging
import re
import time
import gc
import weakref
import sys
from functools import lru_cache
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

logger = logging.getLogger(__name__)

# Cache settings
VIEW_CACHE_TIMEOUT = 3600  # 1 hour
VIEW_CACHE_KEY_PREFIX = 'django_mcp:view_discovery:'

# Registry settings
DEFAULT_MAX_REGISTRY_SIZE = 1000  # Maximum number of views to store in registry

@dataclass
class ViewInfo:
    """
    Information about a discovered view.
    
    This class stores metadata about a view, including its path, methods,
    documentation, and parameters.
    
    Attributes:
        view_func: The view function or callable.
        path: The URL path to the view.
        name: The name of the view.
        methods: HTTP methods supported by the view.
        app_name: The name of the app containing the view.
        path_params: Parameters extracted from the URL path.
        doc: Documentation string for the view.
        view_name: The name of the view function.
        parameters: Parameter information extracted from the view function.
        created_at: When this view info was created.
    """
    view_func: Callable
    path: str
    name: str
    methods: List[str]
    app_name: Optional[str] = None
    path_params: List[str] = field(default_factory=list)
    doc: Optional[str] = None
    view_name: Optional[str] = None
    parameters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=timezone.now)
    
    def __post_init__(self) -> None:
        """
        Perform post-initialization processing.
        
        Extracts additional metadata from the view function if not provided.
        """
        # Extract view name if not provided
        if not self.view_name:
            self.view_name = self._extract_view_name()
        
        # Extract doc if not provided
        if not self.doc:
            self.doc = self._extract_doc()
        
        # Extract parameters if not provided
        if not self.parameters:
            self.parameters = self._extract_parameters()
    
    def _extract_view_name(self) -> str:
        """
        Extract the name of the view function.
        
        Returns:
            The name of the view function.
        """
        if hasattr(self.view_func, '__name__'):
            return self.view_func.__name__
        
        # Handle class-based views
        if hasattr(self.view_func, 'cls'):
            return self.view_func.cls.__name__
        
        if hasattr(self.view_func, 'view_class'):
            return self.view_func.view_class.__name__
        
        # Fallback to a generic name
        return f"view_{id(self.view_func)}"
    
    def _extract_doc(self) -> Optional[str]:
        """
        Extract documentation from the view function or class.
        
        Returns:
            The documentation string, or None if not available.
        """
        # Check for method-specific docs for class-based views
        if hasattr(self.view_func, 'cls') and hasattr(self.view_func, 'actions'):
            for method, action in self.view_func.actions.items():
                if hasattr(self.view_func.cls, action):
                    method_handler = getattr(self.view_func.cls, action)
                    if method_handler.__doc__:
                        return method_handler.__doc__.strip()
        
        # Check for view class methods
        for method in self.methods:
            method_name = method.lower()
            if hasattr(self.view_func, 'cls') and hasattr(self.view_func.cls, method_name):
                method_handler = getattr(self.view_func.cls, method_name)
                if method_handler.__doc__:
                    return method_handler.__doc__.strip()
        
        # Check for function docstring
        if self.view_func.__doc__:
            return self.view_func.__doc__.strip()
        
        # Check for class docstring for class-based views
        if hasattr(self.view_func, 'cls') and self.view_func.cls.__doc__:
            return self.view_func.cls.__doc__.strip()
        
        if hasattr(self.view_func, 'view_class') and self.view_func.view_class.__doc__:
            return self.view_func.view_class.__doc__.strip()
        
        return None
    
    def _extract_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract parameter information from the view function.
        
        Returns:
            A dictionary of parameter metadata.
        """
        parameters: Dict[str, Dict[str, Any]] = {}
        
        # Add path parameters
        for param in self.path_params:
            parameters[param] = {
                'type': 'string',
                'in': 'path',
                'required': True,
                'description': f'Path parameter: {param}'
            }
        
        # Extract function signature parameters
        try:
            sig = inspect.signature(self.view_func)
            for param_name, param in sig.parameters.items():
                # Skip self, cls, request, and args/kwargs
                if param_name in ('self', 'cls', 'request', 'args', 'kwargs'):
                    continue
                
                # Skip path parameters already processed
                if param_name in parameters:
                    continue
                
                param_type = 'string'
                if param.annotation != inspect.Parameter.empty:
                    # Get type name from annotation
                    if hasattr(param.annotation, '__name__'):
                        param_type = param.annotation.__name__
                    else:
                        # Handle typing types
                        param_type = str(param.annotation).replace('typing.', '')
                
                # Determine if parameter is required
                required = param.default == inspect.Parameter.empty
                
                parameters[param_name] = {
                    'type': param_type.lower(),
                    'in': 'query',
                    'required': required,
                    'description': f'Query parameter: {param_name}'
                }
                
                # Add default value if available
                if param.default != inspect.Parameter.empty:
                    parameters[param_name]['default'] = param.default
        
        except (ValueError, TypeError):
            # Could not inspect function signature
            pass
        
        return parameters
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert ViewInfo to a dictionary representation.
        
        Returns:
            Dictionary representation of the ViewInfo.
        """
        return {
            'path': self.path,
            'name': self.name,
            'view_name': self.view_name,
            'methods': self.methods,
            'app_name': self.app_name,
            'path_params': self.path_params,
            'doc': self.doc,
            'parameters': self.parameters,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['ViewInfo']:
        """
        Create a ViewInfo object from a dictionary.
        
        Args:
            data: Dictionary data to create ViewInfo from.
            
        Returns:
            A ViewInfo object, or None if creation fails.
        """
        try:
            # Create a dummy view function
            def dummy_view(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
                return HttpResponse()
            
            # Create ViewInfo with required fields
            info = cls(
                view_func=dummy_view,
                path=data.get('path', ''),
                name=data.get('name', ''),
                methods=data.get('methods', ['GET']),
                app_name=data.get('app_name'),
                path_params=data.get('path_params', []),
                doc=data.get('doc'),
                view_name=data.get('view_name'),
                parameters=data.get('parameters', {}),
            )
            
            # Parse created_at if available
            if 'created_at' in data and data['created_at']:
                try:
                    info.created_at = datetime.fromisoformat(data['created_at'])
                except (ValueError, TypeError):
                    info.created_at = timezone.now()
            
            return info
        
        except Exception as e:
            logger.warning(f"Error creating ViewInfo from dict: {e}")
            return None


class ViewRegistry:
    """
    Registry for discovered views.
    
    This class maintains a registry of views discovered by the discovery process,
    providing methods to access and filter the views.
    """

    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize the view registry.
        
        Args:
            max_size: Maximum number of views to store in the registry.
                If exceeded, least recently registered views will be removed.
                Defaults to the value of MCP_MAX_REGISTRY_SIZE setting or 1000.
        """
        self.views: List[ViewInfo] = []
        self._view_cache: Dict[str, ViewInfo] = {}  # Cache views by path
        self._last_discovery_time: Optional[float] = None
        self._last_cleanup_time: Optional[float] = None
        self._registry_stats: Dict[str, Any] = {
            'total_registrations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'cleanups_performed': 0,
            'items_removed': 0,
            'peak_size': 0,
        }
        
        # Set maximum registry size from settings or default
        self.max_size = max_size or getattr(
            settings, 'MCP_MAX_REGISTRY_SIZE', DEFAULT_MAX_REGISTRY_SIZE
        )
    
    def register(self, view_info: ViewInfo) -> None:
        """
        Register a view.
        
        Args:
            view_info: The ViewInfo object to register.
        """
        # Store in main list
        self.views.append(view_info)
        
        # Update cache
        self._view_cache[view_info.path] = view_info
        
        # Update stats
        self._registry_stats['total_registrations'] += 1
        current_size = len(self.views)
        if current_size > self._registry_stats['peak_size']:
            self._registry_stats['peak_size'] = current_size
        
        # Update discovery time
        self._last_discovery_time = time.time()
        
        # Check if we need to clean up
        if self.max_size > 0 and len(self.views) > self.max_size:
            self._cleanup_oldest_views()
    
    def get_views(
        self, app_name: Optional[str] = None, path_pattern: Optional[str] = None
    ) -> List[ViewInfo]:
        """
        Get views matching the filter criteria.
        
        Args:
            app_name: Filter views by app name.
            path_pattern: Filter views by path pattern.
            
        Returns:
            A list of ViewInfo objects matching the filter criteria.
        """
        views = self.views
        
        if app_name:
            views = [view for view in views if view.app_name == app_name]
        
        if path_pattern:
            pattern = re.compile(path_pattern)
            views = [view for view in views if pattern.match(view.path)]
        
        return views
    
    def get_view(self, path: str) -> Optional[ViewInfo]:
        """
        Get a view by path.
        
        Args:
            path: The path of the view to get.
            
        Returns:
            The ViewInfo object for the view, or None if not found.
        """
        view = self._view_cache.get(path)
        if view is not None:
            self._registry_stats['cache_hits'] += 1
        else:
            self._registry_stats['cache_misses'] += 1
        return view
    
    def has_path(self, path: str) -> bool:
        """
        Check if a path is in the registry.
        
        Args:
            path: The path to check.
            
        Returns:
            True if the path is in the registry, False otherwise.
        """
        return path in self._view_cache
    
    def clear(self) -> None:
        """Clear the registry."""
        # Clean up view references to avoid memory leaks
        for view_info in self.views:
            # Remove circular references
            if hasattr(view_info, 'view_func'):
                delattr(view_info, 'view_func')
            if hasattr(view_info, 'original_func'):
                delattr(view_info, 'original_func')
        
        # Clear collections
        self.views = []
        self._view_cache = {}
        self._last_discovery_time = None
        
        # Suggest garbage collection
        gc.collect()
    
    def get_discovery_time(self) -> Optional[float]:
        """
        Get the time of the last discovery operation.
        
        Returns:
            The time of the last discovery operation, or None if no discovery has been performed.
        """
        return self._last_discovery_time
    
    def cache_views(self, cache_timeout: Optional[int] = None) -> None:
        """
        Cache the views in the registry to improve performance.
        
        Args:
            cache_timeout: How long to cache the views, in seconds.
        """
        if not self.views:
            return
        
        # Convert views to a cacheable format
        view_data = [view.to_dict() for view in self.views]
        
        # Cache the views
        timeout = cache_timeout or getattr(settings, 'MCP_VIEW_CACHE_TIMEOUT', VIEW_CACHE_TIMEOUT)
        cache_key = f"{VIEW_CACHE_KEY_PREFIX}all_views"
        cache.set(cache_key, view_data, timeout)
        
        logger.debug(f"Cached {len(view_data)} views")
    
    def load_cached_views(self) -> bool:
        """
        Load views from cache.
        
        Returns:
            True if views were loaded from cache, False otherwise.
        """
        # Check if views are already loaded
        if self.views:
            return False
        
        # Try to get views from cache
        cache_key = f"{VIEW_CACHE_KEY_PREFIX}all_views"
        view_data = cache.get(cache_key)
        
        if not view_data:
            return False
        
        try:
            # Clear existing views
            self.clear()
            
            # Load views from cache
            for view_dict in view_data:
                # Reconstruct view_func from module and qualname (best effort)
                module_name = view_dict.pop('module', None)
                qualname = view_dict.pop('qualname', None)
                
                # Remove the creation time if it exists (will be recreated)
                view_dict.pop('creation_time', None)
                
                view_func = None
                if module_name and qualname:
                    try:
                        module = __import__(module_name, fromlist=['.'])
                        parts = qualname.split('.')
                        view_func = module
                        for part in parts:
                            view_func = getattr(view_func, part, None)
                            if view_func is None:
                                break
                    except (ImportError, AttributeError):
                        logger.warning(f"Could not reconstruct view_func for {module_name}.{qualname}")
                
                if view_func:
                    # Create ViewInfo with reconstructed view_func
                    view_info = ViewInfo(view_func=view_func, **view_dict)
                    self.register(view_info)
            
            logger.debug(f"Loaded {len(self.views)} views from cache")
            return bool(self.views)
        except Exception as e:
            logger.warning(f"Error loading views from cache: {str(e)}")
            self.clear()
            return False
    
    def _cleanup_oldest_views(self) -> None:
        """
        Remove the oldest views from the registry to stay within max_size limit.
        
        This method removes views based on their creation time, keeping the most
        recently registered views.
        """
        if not self.views or len(self.views) <= self.max_size:
            return
        
        # Sort views by creation time (oldest first)
        self.views.sort(key=lambda v: v._creation_time)
        
        # Determine how many views to remove
        num_to_remove = len(self.views) - self.max_size
        views_to_remove = self.views[:num_to_remove]
        
        # Update statistics
        self._registry_stats['cleanups_performed'] += 1
        self._registry_stats['items_removed'] += num_to_remove
        
        # Remove views
        for view in views_to_remove:
            if view.path in self._view_cache:
                del self._view_cache[view.path]
            
            # Remove circular references
            if hasattr(view, 'view_func'):
                delattr(view, 'view_func')
            if hasattr(view, 'original_func'):
                delattr(view, 'original_func')
        
        # Update the main list
        self.views = self.views[num_to_remove:]
        self._last_cleanup_time = time.time()
        
        logger.debug(f"Cleaned up {num_to_remove} old views from registry")
        
        # Suggest garbage collection
        gc.collect()
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Get memory usage statistics for the registry.
        
        Returns:
            Dictionary with memory usage statistics.
        """
        stats = {
            'views_count': len(self.views),
            'cache_count': len(self._view_cache),
            'registry_stats': self._registry_stats.copy(),
            'last_cleanup_time': self._last_cleanup_time,
        }
        
        # Get size information if possible
        try:
            from sys import getsizeof
            
            # Estimate registry size
            registry_size = getsizeof(self.views) + getsizeof(self._view_cache)
            
            # Add sample of view sizes (first 10 to avoid expensive calculation)
            sample_views = self.views[:10]
            if sample_views:
                sample_size = sum(getsizeof(v) for v in sample_views)
                stats['avg_view_size'] = sample_size / len(sample_views)
                stats['estimated_total_size'] = int(stats['avg_view_size'] * len(self.views) + registry_size)
            else:
                stats['estimated_total_size'] = registry_size
            
            stats['registry_size_bytes'] = registry_size
            
        except (ImportError, Exception) as e:
            stats['error_calculating_size'] = str(e)
        
        return stats
    
    def cleanup_unused_references(self) -> int:
        """
        Clean up unused view references to reduce memory usage.
        
        This method removes references to views that are no longer needed,
        focusing on breaking circular references.
        
        Returns:
            Number of views cleaned up.
        """
        cleaned = 0
        
        for view in self.views:
            # Check if the view function has been garbage collected
            view_func = getattr(view, 'view_func', None)
            original_func = getattr(view, 'original_func', None)
            
            if view_func is None:
                continue
                
            # If the view function is already collected, remove our reference
            if isinstance(view_func, weakref.ReferenceType) and view_func() is None:
                delattr(view, 'view_func')
                if hasattr(view, 'original_func'):
                    delattr(view, 'original_func')
                cleaned += 1
        
        # Suggest garbage collection if we cleaned any references
        if cleaned > 0:
            gc.collect()
            logger.debug(f"Cleaned up {cleaned} unused view references")
        
        return cleaned


def discover_views():
    """
    Discover Django REST Framework views and register them as MCP tools.
    
    This function discovers all views exposed by Django REST Framework
    and registers them as MCP tools for use by LLMs.
    """
    try:
        # Import DRF to see if it's installed
        import rest_framework
        
        # Import here to avoid circular imports
        from django_mcp.config import mcp_config
        from django_mcp.discovery import ViewDiscovery
        
        # Get the MCP server instance
        server = mcp_config.get_server()
        
        # Only proceed if server is initialized
        if server is None:
            logger.warning("MCP server is not initialized, skipping view registration")
            return
        
        # Discover DRF views
        discovery = ViewDiscovery()
        
        # Apply path filters if configured
        discovery_settings = mcp_config.get_discovery_settings()
        include_paths = discovery_settings.get('include_paths', [])
        
        if include_paths:
            # Discover views matching specific path patterns
            for path_pattern in include_paths:
                discovery.discover_views_by_pattern(path_pattern)
        else:
            # Discover all views
            discovery.discover_all_views()
        
        # Register discovered views as tools
        discovery.register_views_as_tools(server)
        
    except ImportError:
        # DRF is not installed, skip discovery
        logger.debug("Django REST Framework not installed, skipping DRF view discovery") 