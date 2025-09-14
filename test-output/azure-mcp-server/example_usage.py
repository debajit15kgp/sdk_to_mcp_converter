#!/usr/bin/env python3
"""
Example usage of the azure MCP server.

Before running this example, make sure you have:
1. Azure CLI installed and logged in: `az login`
2. Or set the following environment variables:
   - AZURE_SUBSCRIPTION_ID
   - AZURE_CLIENT_ID (for service principal)
   - AZURE_CLIENT_SECRET (for service principal)
   - AZURE_TENANT_ID (for service principal)
3. Or update the config.json file with your Azure credentials
"""

import asyncio
import os
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    """Example client usage."""
    print("🚀 Connecting to azure MCP server...")
    
    # Check if Azure credentials are available
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        print("⚠️  Warning: AZURE_SUBSCRIPTION_ID not found in environment variables.")
        print("   Please either:")
        print("   1. Set AZURE_SUBSCRIPTION_ID environment variable")
        print("   2. Update config.json with your subscription_id")
        print("   3. Run 'az login' if using Azure CLI authentication")
        print()
    
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
            print(f"\nExecuting: close")
            result = await session.call_tool("close", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            
            print(f"\nExecuting: list_operations")
            result = await session.call_tool("list_operations", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")
            
            print(f"\nExecuting: close")
            result = await session.call_tool("close", {})
            print(f"Result: {result.content[0].text if result.content else 'No content'}")

            
            # List resources
            resources = await session.list_resources()
            print(f"\nAvailable resources: {len(resources.resources)}")


async def call_close(session):
    """Call close tool."""
    try:
        result = await session.call_tool("close", {})
        print(f"✅ close: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ close failed: {e}")
        return None

async def call_list_operations(session):
    """Call list_operations tool."""
    try:
        result = await session.call_tool("list_operations", {})
        print(f"✅ list_operations: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ list_operations failed: {e}")
        return None

async def call_close(session):
    """Call close tool."""
    try:
        result = await session.call_tool("close", {})
        print(f"✅ close: {result.content[0].text if result.content else 'Success'}")
        return result
    except Exception as e:
        print(f"❌ close failed: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(main())
