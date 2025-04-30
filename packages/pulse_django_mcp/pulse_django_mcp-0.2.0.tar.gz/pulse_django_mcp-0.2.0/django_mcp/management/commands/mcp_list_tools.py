"""
Django management command to list available MCP tools.

This command displays information about the registered MCP tools,
providing detailed information about their parameters and schemas.
"""
import logging
import json
from typing import Any, Dict

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django_mcp.config import mcp_config
from django_mcp.apps import autodiscover

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Django management command to list available MCP tools.
    
    This command displays information about the registered MCP tools,
    providing detailed information about their parameters and schemas.
    """
    
    help = "Lists all registered MCP tools available through the FastMCP server."
    
    def add_arguments(self, parser):
        """
        Add command-line arguments for the command.
        
        Args:
            parser: The argument parser
        """
        parser.add_argument(
            '--json', 
            action='store_true',
            help='Output the tool list in JSON format.'
        )
        parser.add_argument(
            '--verbose', 
            action='store_true',
            help='Include detailed parameter information in text output.'
        )
    
    def handle(self, *args: Any, **options: Any) -> None:
        """Handle the command execution."""
        # Ensure MCP is enabled
        if not mcp_config.is_enabled():
            self.stderr.write(self.style.ERROR("Django-MCP is disabled in settings (MCP_ENABLED=False)."))
            return

        # Run autodiscovery to ensure all tools are loaded
        # This is important if views are being registered as tools
        self.stdout.write("Running autodiscovery...")
        try:
            autodiscover()
            self.stdout.write(self.style.SUCCESS("Autodiscovery completed."))
        except Exception as e:
            logger.exception("Error during autodiscovery")
            self.stderr.write(self.style.WARNING(f"Warning: Error during autodiscovery: {e}. Proceeding..."))
            # Continue anyway, maybe some tools were registered manually

        # Get the server instance
        self.stdout.write("Fetching MCP server instance...")
        server = mcp_config.get_server()

        if not server:
            self.stderr.write(self.style.ERROR("Failed to retrieve MCP Server instance from config."))
            return
            
        if not hasattr(server, '_official_server') or not hasattr(server._official_server, '_mcp_server'):
            self.stderr.write(self.style.ERROR("Retrieved server instance is not a valid FastMCP wrapper."))
            return

        mcp_server = server._official_server._mcp_server
        if not hasattr(mcp_server, 'tools'):
            self.stderr.write(self.style.ERROR("Internal MCP server object does not have a 'tools' attribute."))
            return

        tools = mcp_server.tools

        if not tools:
            self.stdout.write("No MCP tools registered or found on the server.")
            return

        # Output based on format
        if options['json']:
            self._output_json(tools)
        else:
            self._output_text(tools, verbose=options['verbose'])
    
    def _output_json(self, tools: Dict[str, Any]) -> None:
        """Output tool list as JSON."""
        output_data = []
        for name, tool_obj in tools.items():
            tool_data = {
                "name": name,
                "description": getattr(tool_obj, 'description', 'No description available'),
                "parameters": [],
            }
            # Attempt to extract parameters from the Pydantic model if present
            if hasattr(tool_obj, 'parameters') and hasattr(tool_obj.parameters, 'model_json_schema'):
                 try:
                     schema = tool_obj.parameters.model_json_schema()
                     if 'properties' in schema:
                         for param_name, param_info in schema['properties'].items():
                              tool_data['parameters'].append({
                                  "name": param_name,
                                  "type": param_info.get('type', 'any'),
                                  "description": param_info.get('description', ''),
                                  "required": param_name in schema.get('required', [])
                              })
                 except Exception as e:
                     logger.warning(f"Could not generate JSON schema for parameters of tool '{name}': {e}")
                     tool_data['parameters_error'] = f"Could not extract: {e}"
            else:
                tool_data['parameters_info'] = "Parameter schema not available or not in expected format."
                
            output_data.append(tool_data)
            
        self.stdout.write(json.dumps(output_data, indent=2))

    def _output_text(self, tools: Dict[str, Any], verbose: bool) -> None:
        """Output tool list as formatted text."""
        self.stdout.write(self.style.SUCCESS(f"Registered MCP Tools ({len(tools)}):"))
        for name, tool_obj in sorted(tools.items()):
            description = getattr(tool_obj, 'description', 'No description available')
            self.stdout.write(f"- {self.style.SQL_FIELD(name)}: {description}")
            
            if verbose:
                # Attempt to extract and display parameters
                if hasattr(tool_obj, 'parameters') and hasattr(tool_obj.parameters, 'model_json_schema'):
                    try:
                        schema = tool_obj.parameters.model_json_schema()
                        if 'properties' in schema:
                            self.stdout.write(f"  {self.style.SQL_COLTYPE('Parameters')}:")
                            for param_name, param_info in schema['properties'].items():
                                param_type = param_info.get('type', 'any')
                                param_desc = param_info.get('description', '')
                                required = param_name in schema.get('required', [])
                                req_str = " (required)" if required else ""
                                self.stdout.write(f"    - {param_name} ({param_type}){req_str}: {param_desc}")
                        else:
                            self.stdout.write(f"  {self.style.SQL_COLTYPE('Parameters')}: (No parameters defined in schema)")
                    except Exception as e:
                        logger.warning(f"Could not generate/parse parameter schema for tool '{name}': {e}")
                        self.stdout.write(f"  {self.style.SQL_COLTYPE('Parameters')}: (Error extracting schema: {e})")
                else:
                     self.stdout.write(f"  {self.style.SQL_COLTYPE('Parameters')}: (Parameter schema not available or not in expected format.)")
        self.stdout.write("\n") # Add a newline for better spacing 