"""
SDK to MCP Converter

A Python library that automatically converts Python SDKs into MCP (Model Context Protocol) servers.
This enables AI assistants to interact with any Python SDK through a standardized MCP interface.
"""

__version__ = "0.1.0"
__author__ = "SDK to MCP Converter"

from .converter import SDKToMCPConverter
from .introspector import SDKIntrospector
from .generator import MCPGenerator

__all__ = ["SDKToMCPConverter", "SDKIntrospector", "MCPGenerator"]
