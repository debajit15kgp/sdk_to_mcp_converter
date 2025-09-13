"""
Example usage of the Github MCP Server

This file demonstrates how to interact with the generated MCP server.
"""

import json
import asyncio
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """Example usage of the MCP server."""
    
    # Connect to the MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Example tool calls
            examples = [

# Example: authentication
{
    "tool": "authentication",
    "arguments": {}
},

# Example: mask_authentication
{
    "tool": "mask_authentication",
    "arguments": {}
},

# Example: withRequester
{
    "tool": "withRequester",
    "arguments": {}
}
            ]
            
            for example in examples:
                print(f"\nExecuting: {example['tool']}")
                try:
                    result = await session.call_tool(example["tool"], example["arguments"])
                    print(f"Result: {result.content[0].text}")
                except Exception as e:
                    print(f"Error: {e}")
            
            # List available resources
            resources = await session.list_resources()
            print("\nAvailable resources:")
            for resource in resources.resources:
                print(f"- {resource.name}: {resource.description}")

if __name__ == "__main__":
    asyncio.run(main())
