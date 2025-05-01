"""
OpenAI Image Generation MCP Server entry module.

This module serves as the entry point for the OpenAI Image Generation MCP server.
"""

from openai_gpt_image_1 import mcp
import openai_gpt_image_1.tools

def main():
    """Run the OpenAI Image Generation MCP server."""
    print("Starting OpenAI Image Generation MCP server...")
    print("Press Ctrl+C to stop.")
    mcp.run()

if __name__ == "__main__":
    main()