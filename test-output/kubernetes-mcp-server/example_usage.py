#!/usr/bin/env python3
"""
Example usage of the kubernetes MCP server.
"""

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    """Example client usage."""
    print("🚀 Connecting to kubernetes MCP server...")
    
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
            print(f"\nExecuting: get_api_group")
            result = await session.call_tool("get_api_group", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            print(f"\nExecuting: get_api_group_with_http_info")
            result = await session.call_tool("get_api_group_with_http_info", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            print(f"\nExecuting: create_mutating_webhook_configuration")
            result = await session.call_tool("create_mutating_webhook_configuration", {
                "body": "example webhook configuration"
            })
            print(f"Result: {result.content[0].text if result.content else 'No content'}")

            
            # List resources
            resources = await session.list_resources()
            print(f"\nAvailable resources: {len(resources.resources)}")


async def call_get_api_group(session):
    """Call get_api_group tool."""
    try:
        result = await session.call_tool("get_api_group", {})
        print(f"✅ get_api_group: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ get_api_group failed: {e}")
        return None

async def call_get_api_group_with_http_info(session):
    """Call get_api_group_with_http_info tool."""
    try:
        result = await session.call_tool("get_api_group_with_http_info", {})
        print(f"✅ get_api_group_with_http_info: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ get_api_group_with_http_info failed: {e}")
        return None

async def call_create_mutating_webhook_configuration(session):
    """Call create_mutating_webhook_configuration tool."""
    try:
        result = await session.call_tool("create_mutating_webhook_configuration", {})
        print(f"✅ create_mutating_webhook_configuration: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ create_mutating_webhook_configuration failed: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(main())
