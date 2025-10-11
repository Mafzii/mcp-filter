"""
Tool Integrations

Simple integrations for adding generated MCP servers to AI tools.
Currently supports: Claude Code (user scope)
"""

from .abstract_integration_manager import AbstractIntegrationManager
from .claude_code_integration import ClaudeCodeIntegration, prompt_add_to_claude

__all__ = [
    'AbstractIntegrationManager',
    'ClaudeCodeIntegration',
    'prompt_add_to_claude',
]
