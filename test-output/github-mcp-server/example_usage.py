#!/usr/bin/env python3
"""
Example usage of the github MCP server.
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    """Example client usage."""
    print("🚀 Connecting to github MCP server...")
    
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
            print(f"Available tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Example tool calls
            print(f"\nExecuting: authentication")
            result = await session.call_tool("authentication", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            print(f"\nExecuting: mask_authentication")
            result = await session.call_tool("mask_authentication", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            print(f"\nExecuting: withRequester")
            result = await session.call_tool("withRequester", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")

            
            # List resources
            resources = await session.list_resources()
            print(f"\nAvailable resources: {len(resources.resources)}")


async def call_authentication(session):
    """Call authentication tool."""
    try:
        result = await session.call_tool("authentication", {})
        print(f"✅ authentication: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ authentication failed: {e}")
        return None

async def call_mask_authentication(session):
    """Call mask_authentication tool."""
    try:
        result = await session.call_tool("mask_authentication", {})
        print(f"✅ mask_authentication: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ mask_authentication failed: {e}")
        return None

async def call_withRequester(session):
    """Call withRequester tool."""
    try:
        result = await session.call_tool("withRequester", {})
        print(f"✅ withRequester: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ withRequester failed: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(main())
