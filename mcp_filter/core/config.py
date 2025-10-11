"""
Configuration Manager - Handle MCP server configurations

This module provides the ConfigManager class for loading, saving, and managing
MCP server configurations.
"""

import json
from pathlib import Path
from typing import Dict, Optional


class ConfigManager:
    """Manages MCP server configurations."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_dir: Custom config directory path. Defaults to ~/.config/mcp-filter
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".config" / "mcp-filter"

        self.config_file = self.config_dir / "servers.json"
        self.default_file = Path(__file__).parent.parent.parent / "default_servers.json"

    def load_servers(self) -> Dict[str, str]:
        """
        Load MCP server configurations.

        First tries to load from user config, then falls back to default servers.

        Returns:
            Dictionary mapping server names to their commands
        """
        # Try user config first
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        # Fall back to default servers
        if self.default_file.exists():
            try:
                with open(self.default_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass

        return {}

    def save_servers(self, servers: Dict[str, str]) -> None:
        """
        Save MCP server configurations to user config.

        Args:
            servers: Dictionary mapping server names to their commands
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w') as f:
            json.dump(servers, f, indent=2)

    def add_server(self, name: str, command: str) -> None:
        """
        Add a new MCP server configuration.

        Args:
            name: Server name
            command: Command to start the server
        """
        servers = self.load_servers()
        servers[name] = command
        self.save_servers(servers)

    def remove_server(self, name: str) -> bool:
        """
        Remove an MCP server configuration.

        Args:
            name: Server name to remove

        Returns:
            True if server was removed, False if not found
        """
        servers = self.load_servers()
        if name in servers:
            del servers[name]
            self.save_servers(servers)
            return True
        return False

    def get_server(self, name: str) -> Optional[str]:
        """
        Get the command for a specific server.

        Args:
            name: Server name

        Returns:
            Server command or None if not found
        """
        servers = self.load_servers()
        return servers.get(name)

    def list_servers(self) -> Dict[str, str]:
        """
        Get all configured servers.

        Returns:
            Dictionary mapping server names to their commands
        """
        return self.load_servers()

    def has_servers(self) -> bool:
        """
        Check if any servers are configured.

        Returns:
            True if at least one server is configured, False otherwise
        """
        return bool(self.load_servers())
