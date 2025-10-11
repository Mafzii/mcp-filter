"""
Main Entry Point - Command-line interface for MCP Filter

This module provides the main entry point for running MCP Filter as a command-line tool.
"""

import sys
import argparse

from mcp_filter.core.config import ConfigManager
from mcp_filter.cli.display import display_servers
from mcp_filter.interactive import InteractiveSession


def main():
    """Main entry point for MCP Filter CLI."""
    parser = argparse.ArgumentParser(
        description="Filter tools from existing MCP servers",
        prog="mcp_filter"
    )
    parser.add_argument(
        "--add-server",
        nargs=2,
        metavar=('NAME', 'COMMAND'),
        help="Add an MCP server configuration"
    )
    parser.add_argument(
        "--remove-server",
        metavar='NAME',
        help="Remove an MCP server configuration"
    )
    parser.add_argument(
        "--list-servers",
        action="store_true",
        help="List all configured MCP servers"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="output",
        help="Output directory for filtered MCP servers (default: output)"
    )
    parser.add_argument(
        "--config-dir",
        help="Custom configuration directory (default: ~/.config/mcp-filter)"
    )

    args = parser.parse_args()

    # Initialize configuration manager
    config_manager = ConfigManager(config_dir=args.config_dir)
    servers = config_manager.load_servers()

    # Handle add server command
    if args.add_server:
        name, command = args.add_server
        config_manager.add_server(name, command)
        print(f"Added server '{name}': {command}")
        return

    # Handle remove server command
    if args.remove_server:
        if config_manager.remove_server(args.remove_server):
            print(f"Removed server '{args.remove_server}'")
        else:
            print(f"Server '{args.remove_server}' not found")
        return

    # Handle list servers command
    if args.list_servers:
        display_servers(servers)
        return

    # Main flow: interactive session
    if not servers:
        print("\nNo MCP servers configured.")
        print("Add a server first: python -m mcp_filter --add-server <name> <command>")
        print("\nExample:")
        print("  python -m mcp_filter --add-server notion 'npx -y @modelcontextprotocol/server-notion'")
        sys.exit(1)

    # Run interactive session
    session = InteractiveSession(config_manager, args.output_dir)
    session.run()


if __name__ == "__main__":
    main()
