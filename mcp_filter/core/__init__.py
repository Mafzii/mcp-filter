"""
Core functionality for MCP Filter

Contains MCP client communication, configuration management,
and code generation.
"""

from mcp_filter.core.mcp_client import MCPClient
from mcp_filter.core.config import ConfigManager
from mcp_filter.core.generator import CodeGenerator

__all__ = ["MCPClient", "ConfigManager", "CodeGenerator"]
