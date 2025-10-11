"""
MCP Filter - Filter tools from existing MCP servers

A modular tool for connecting to Model Context Protocol servers,
retrieving available tools, and generating filtered wrapper scripts.
"""

__version__ = "1.0.0"

from mcp_filter.core.mcp_client import MCPClient
from mcp_filter.core.config import ConfigManager
from mcp_filter.core.generator import CodeGenerator
from mcp_filter.interactive import InteractiveSession

__all__ = [
    "MCPClient",
    "ConfigManager",
    "CodeGenerator",
    "InteractiveSession",
]
