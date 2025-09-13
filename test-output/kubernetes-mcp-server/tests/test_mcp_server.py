"""
Tests for the MCP server.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from mcp_server import MCPServer

class TestMCPServer:
    """Test cases for the MCP server."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.server = MCPServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test server initialization."""
        assert self.server is not None
        assert self.server.server is not None
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test listing available tools."""
        tools = await self.server.server.list_tools()
        assert tools is not None
        assert isinstance(tools, list)
    
    @pytest.mark.asyncio
    async def test_list_resources(self):
        """Test listing available resources."""
        resources = await self.server.server.list_resources()
        assert resources is not None
        assert isinstance(resources, list)

if __name__ == "__main__":
    pytest.main([__file__])
