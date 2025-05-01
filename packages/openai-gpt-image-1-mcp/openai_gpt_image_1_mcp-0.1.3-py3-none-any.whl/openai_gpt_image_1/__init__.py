"""
OpenAI Image Generation MCP module.

This module provides MCP tools for OpenAI's image generation capabilities.
"""

# Import MCP server components
from mcp.server.fastmcp import FastMCP, Context

# Create the MCP Server instance
mcp = FastMCP(
    "OpenAIImageGen",  # Internal name
    dependencies=["openai", "httpx"]  # Specify dependencies
)

# Import tool implementations to register them with the MCP
from openai_gpt_image_1.tools import basic_tools

def run():
    """Run the OpenAI Image Generation MCP server."""
    mcp.run()