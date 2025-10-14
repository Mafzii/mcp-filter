"""
Configuration Manager - Handle MCP server configurations

This module provides the ConfigManager class for loading, saving, and managing
MCP server configurations.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Any, List


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

    def load_servers(self) -> Dict[str, Dict[str, Any]]:
        """
        Load MCP server configurations.

        First tries to load from user config, then falls back to default servers.

        Returns:
            Dictionary mapping server names to config objects with 'command' and 'env' fields
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

    def save_servers(self, servers: Dict[str, Dict[str, Any]]) -> None:
        """
        Save MCP server configurations to user config.

        Args:
            servers: Dictionary mapping server names to config objects
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w') as f:
            json.dump(servers, f, indent=2)

    def add_server(self, name: str, command: str, env: Optional[List[str]] = None) -> None:
        """
        Add a new MCP server configuration.

        Args:
            name: Server name
            command: Command to start the server
            env: Optional list of environment variable names required by the server
        """
        servers = self.load_servers()
        servers[name] = {
            "command": command,
            "env": env or []
        }
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

    def get_server(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get the configuration for a specific server.

        Args:
            name: Server name

        Returns:
            Server config object (with 'command' and 'env') or None if not found
        """
        servers = self.load_servers()
        return servers.get(name)

    def list_servers(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all configured servers.

        Returns:
            Dictionary mapping server names to their config objects
        """
        return self.load_servers()

    def has_servers(self) -> bool:
        """
        Check if any servers are configured.

        Returns:
            True if at least one server is configured, False otherwise
        """
        return bool(self.load_servers())
