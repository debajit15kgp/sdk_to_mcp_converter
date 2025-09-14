"""
Integration tests for the MCP server.
"""

import pytest
import asyncio
from mcp.client import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class TestIntegration:
    """Integration tests for the MCP server."""
    
    @pytest.mark.asyncio
    async def test_server_connection(self):
        """Test connecting to the MCP server."""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test basic functionality
                tools = await session.list_tools()
                assert tools is not None
                
                resources = await session.list_resources()
                assert resources is not None

if __name__ == "__main__":
    pytest.main([__file__])
