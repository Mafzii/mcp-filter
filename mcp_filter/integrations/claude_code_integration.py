"""
Claude Code Integration

Integration module for adding generated MCP servers to Claude Code's user config.
Manages ~/.claude/mcp_servers.json (user scope only).
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from .abstract_integration_manager import AbstractIntegrationManager


class ClaudeCodeIntegration(AbstractIntegrationManager):
    """Manages Claude Code MCP server integration at user scope."""

    def __init__(self):
        """Initialize with default Claude Code config path."""
        self.config_path = Path.home() / ".claude.json"

    def get_tool_name(self) -> str:
        """Get the human-readable name of the tool."""
        return "Claude Code"

    def config_exists(self) -> bool:
        """Check if Claude Code config directory exists."""
        return self.config_path.parent.exists()

    def load_config(self) -> Dict:
        """
        Load existing MCP servers configuration.

        Returns:
            Dict with 'mcpServers' key, or empty structure if file doesn't exist.
        """
        if not self.config_path.exists():
            return {"mcpServers": {}}

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                # Ensure mcpServers key exists
                if "mcpServers" not in config:
                    config["mcpServers"] = {}
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read config file: {e}")
            return {"mcpServers": {}}

    def save_config(self, config: Dict) -> bool:
        """
        Save MCP servers configuration.

        Args:
            config: Configuration dictionary with 'mcpServers' key

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            # Write with pretty formatting
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            return True
        except IOError as e:
            print(f"Error: Could not write config file: {e}")
            return False

    def add_server(
        self,
        name: str,
        script_path: str,
        overwrite: bool = False
    ) -> bool:
        """
        Add a generated MCP server to Claude Code configuration.

        Args:
            name: Server name/identifier
            script_path: Absolute path to the generated Python script
            overwrite: If True, overwrite existing server with same name

        Returns:
            True if successful, False otherwise
        """
        # Load existing config
        config = self.load_config()

        # Check if server already exists
        if name in config["mcpServers"] and not overwrite:
            print(f"Warning: Server '{name}' already exists in config")
            return False

        # Add new server configuration
        config["mcpServers"][name] = {
            "type": "stdio",
            "command": "python3",
            "args": [os.path.abspath(script_path)],
            "env": {}
        }

        # Save updated config
        return self.save_config(config)

    def remove_server(self, name: str) -> bool:
        """
        Remove a server from Claude Code configuration.

        Args:
            name: Server name to remove

        Returns:
            True if removed, False if not found or error
        """
        config = self.load_config()

        if name not in config["mcpServers"]:
            print(f"Server '{name}' not found in config")
            return False

        del config["mcpServers"][name]
        return self.save_config(config)

    def list_servers(self) -> Dict[str, Dict]:
        """
        Get all configured MCP servers.

        Returns:
            Dictionary of server configurations
        """
        config = self.load_config()
        return config.get("mcpServers", {})

    def get_config_path(self) -> str:
        """Get the absolute path to the config file."""
        return str(self.config_path)


def prompt_add_to_claude(
    server_name: str,
    script_path: str
) -> Optional[bool]:
    """
    Prompt user to add generated server to Claude Code config.

    Args:
        server_name: Name for the server
        script_path: Path to generated script

    Returns:
        True if added successfully, False if declined/error, None if Claude Code not detected
    """
    manager = ClaudeCodeIntegration()

    # Check if Claude Code is installed
    if not manager.config_exists():
        return None

    # Prompt user
    print(f"\n🤖 Claude Code detected!")
    try:
        response = input(f"Add '{server_name}' to Claude Code config? [Y/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipped (non-interactive mode).")
        return False

    if response in ['', 'y', 'yes']:
        # Check if server already exists
        existing = manager.load_config()
        if server_name in existing.get("mcpServers", {}):
            overwrite = input(f"Server '{server_name}' already exists. Overwrite? [y/N]: ").strip().lower()
            if overwrite not in ['y', 'yes']:
                print("Skipped.")
                return False

            success = manager.add_server(server_name, script_path, overwrite=True)
        else:
            success = manager.add_server(server_name, script_path)

        if success:
            print(f"✓ Added to Claude Code config: {manager.get_config_path()}")
            print(f"  Restart Claude Code to load the new server.")
            return True
        else:
            print("✗ Failed to add to config")
            return False
    else:
        print("Skipped.")
        return False
