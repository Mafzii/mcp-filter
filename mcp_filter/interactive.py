"""
Interactive Session - Handle interactive user workflows

This module provides the InteractiveSession class for managing the complete
interactive workflow of selecting servers, tools, and generating filtered wrappers.
"""

import os
import datetime
from typing import Dict, List, Any, Tuple

from mcp_filter.core.mcp_client import MCPClient
from mcp_filter.core.config import ConfigManager
from mcp_filter.core.generator import CodeGenerator
from mcp_filter.core.env_manager import EnvManager
from mcp_filter.cli.display import (
    display_servers,
    display_server_tools,
    display_summary,
    display_separator,
    display_warning,
)
from mcp_filter.cli.selection import (
    select_multiple_servers,
    select_tools_from_server,
    get_yes_no_input,
    get_output_filename,
)
from mcp_filter.integrations import prompt_add_to_claude


class InteractiveSession:
    """Manages interactive sessions for creating filtered MCP servers."""

    def __init__(self, config_manager: ConfigManager, output_dir: str = "output"):
        """
        Initialize interactive session.

        Args:
            config_manager: ConfigManager instance for accessing server configs
            output_dir: Directory where filtered servers will be saved
        """
        self.config_manager = config_manager
        self.output_dir = output_dir
        self.servers = config_manager.load_servers()
        self.env_manager = EnvManager()

    def collect_tools_from_servers(
        self,
        selected_server_names: List[str]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, str], Dict[str, Dict[str, str]]]:
        """
        Collect tools from multiple servers and let user select which ones to include.

        Args:
            selected_server_names: List of server names to collect tools from

        Returns:
            Tuple of (selected_tools, server_commands, server_envs)
        """
        all_tools = []
        server_commands = {}
        server_envs = {}

        for server_name in selected_server_names:
            display_separator(f"Connecting to {server_name}...")

            server_config = self.servers[server_name]
            server_command = server_config["command"]

            # Auto-detect required environment variables from command template
            required_env_keys = self.env_manager.extract_variables(server_command)

            # Prompt for any missing environment variables
            env_values = {}
            if required_env_keys:
                env_values = self.env_manager.prompt_for_missing(required_env_keys)

            # Replace <VARIABLE> placeholders in command with actual values
            final_command = server_command
            for env_key, env_value in env_values.items():
                final_command = final_command.replace(f"<{env_key}>", env_value)

            client = MCPClient(final_command)
            tools = client.get_all_tools()

            if not tools:
                display_warning(f"No tools found or unable to connect to {server_name}.")
                continue

            server_commands[server_name] = server_command
            server_envs[server_name] = env_values

            # Tag tools with their server
            for tool in tools:
                tool['server'] = server_name

            display_server_tools(server_name, tools)
            selected = select_tools_from_server(server_name, tools)
            all_tools.extend(selected)

        return all_tools, server_commands, server_envs

    def create_filtered_server(self) -> bool:
        """
        Run the workflow to create a single filtered server.

        Returns:
            True if successful, False if user wants to quit
        """
        display_separator("MCP FILTER - Interactive Session")

        server_names = display_servers(self.servers)
        if not server_names:
            print("\nNo servers available.")
            return False

        # Select servers
        selected_server_names = select_multiple_servers(server_names)
        print(f"\n✓ Selected servers: {', '.join(selected_server_names)}")

        # Collect tools from all selected servers
        all_selected_tools, server_commands, server_envs = self.collect_tools_from_servers(
            selected_server_names
        )

        if not all_selected_tools:
            display_warning("No tools selected from any server.")
            return get_yes_no_input("Try again?")

        # Display summary
        display_summary(all_selected_tools)

        # Get output filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"filtered_server_{timestamp}.py"
        filename = get_output_filename(default_filename)
        output_path = os.path.join(self.output_dir, filename)

        # Generate the filtered server
        CodeGenerator.generate_filtered_mcp(
            server_commands,
            all_selected_tools,
            output_path
        )
        print(f"\n✅ Filtered server created: {output_path}")
        print(f"Run with: python3 {output_path}")

        # Collect all environment variables needed across all servers
        all_env_vars = {}
        for server_name in selected_server_names:
            if server_name in server_envs:
                all_env_vars.update(server_envs[server_name])

        # Prompt to add to Claude Code config
        server_name = os.path.splitext(filename)[0]  # Use filename without .py extension
        prompt_add_to_claude(server_name, output_path, all_env_vars)

        return True

    def run(self) -> None:
        """
        Run an interactive session allowing multiple filter creations.

        Continues in a loop until user chooses to exit.
        """
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        if not self.servers:
            print("\nNo servers available.")
            return

        while True:
            if not self.create_filtered_server():
                break

            display_separator()
            if not get_yes_no_input("Create another filtered server?"):
                print("\n👋 Thanks for using MCP Filter!")
                break
