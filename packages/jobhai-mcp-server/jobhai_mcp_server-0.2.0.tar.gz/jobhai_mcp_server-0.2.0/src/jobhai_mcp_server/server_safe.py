import logging
import os
import importlib
from typing import Any
from pathlib import Path

from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

logger = logging.getLogger(__name__)

async def serve() -> None:
    """Start MCP server"""
    # TODO: Uncomment the following lines to enable environment variable checks
    # required_vars = ["JOBHAI_BASE_URL", "AUTH_TOKEN"]
    # if not all(var in os.environ for var in required_vars):
    #     raise ValueError(f"Missing required environment variables: {required_vars}")

    server = Server("jobhai-mcp-server")

    # Dynamically load resources from the resources directory
    resources_dir = Path(__file__).parent / "resources"
    resources = {}
    for resource_file in resources_dir.glob("*.py"):
        if resource_file.name.startswith("get"):
            continue
        module_name = f"jobhai_mcp_server.resources.{resource_file.stem}"
        module = importlib.import_module(module_name)
        resources[module.RESOURCE] = module

    @server.list_resources()
    async def list_resources() -> list[Tool]:
        try:
            return [
                Tool(name=name, description=module.DESCRIPTION)
                for name, module in resources.items()
            ]
        except Exception as e:
            logger.error("Failed to list resources: %s", e)
            raise

    @server.read_resource()
    async def read_resource(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        try:
            if name not in resources:
                raise ValueError(f"Resource '{name}' not found")
            resource = resources[name]
            return await resource.execute(arguments)
        except Exception as e:
            logger.error("Resource execution failed: %s", e)
            raise

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)