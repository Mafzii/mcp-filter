"""
Selection Functions - User input and selection utilities

This module provides functions for interactive user selection of servers,
tools, and other options.
"""

from typing import Dict, List, Any, Tuple


def select_server(server_names: List[str], servers: Dict[str, str]) -> Tuple[str, str]:
    """
    Allow user to select an MCP server by number.

    Args:
        server_names: List of server names in display order
        servers: Dictionary mapping server names to their commands

    Returns:
        Tuple of (server_name, server_command)
    """
    print("\nSelect server (number):")
    selection = input("> ").strip()

    try:
        idx = int(selection) - 1
        if 0 <= idx < len(server_names):
            name = server_names[idx]
            return name, servers[name]
        else:
            print("Invalid number. Please try again.")
            return select_server(server_names, servers)
    except ValueError:
        print("Please enter a valid number.")
        return select_server(server_names, servers)


def select_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Allow user to select which tools to include.

    Args:
        tools: List of available tool dictionaries

    Returns:
        List of selected tool dictionaries
    """
    print("Select tools to include (comma-separated numbers, or 'all' for all tools):")
    selection = input("> ").strip()

    if selection.lower() == 'all':
        return tools

    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected = [tools[i] for i in indices if 0 <= i < len(tools)]

        if not selected:
            print("No valid tools selected. Please try again.")
            return select_tools(tools)

        return selected
    except (ValueError, IndexError):
        print("Invalid selection. Please enter valid numbers.")
        return select_tools(tools)


def select_multiple_servers(server_names: List[str]) -> List[str]:
    """
    Allow user to select multiple servers.

    Args:
        server_names: List of available server names

    Returns:
        List of selected server names
    """
    print("\nSelect servers (comma-separated numbers, or 'all' for all servers):")
    selection = input("> ").strip()

    if selection.lower() == 'all':
        return server_names

    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected = [server_names[i] for i in indices if 0 <= i < len(server_names)]

        if not selected:
            print("No valid servers selected. Please try again.")
            return select_multiple_servers(server_names)

        return selected
    except (ValueError, IndexError):
        print("Invalid selection. Please enter valid numbers.")
        return select_multiple_servers(server_names)


def select_tools_from_server(
    server_name: str,
    tools: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Allow user to select tools from a specific server.

    Args:
        server_name: Name of the server
        tools: List of available tools from this server

    Returns:
        List of selected tool dictionaries
    """
    print(f"\nSelect tools from {server_name} (comma-separated numbers, 'all', or 'none'):")
    selection = input("> ").strip()

    if selection.lower() == 'none':
        return []
    elif selection.lower() == 'all':
        return tools
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected = [tools[i] for i in indices if 0 <= i < len(tools)]
            return selected
        except (ValueError, IndexError):
            print("Invalid selection. Skipping this server.")
            return []


def get_yes_no_input(prompt: str, default: bool = False) -> bool:
    """
    Get yes/no input from user.

    Args:
        prompt: Question to ask the user
        default: Default value if user just presses Enter

    Returns:
        True for yes, False for no
    """
    default_str = "Y/n" if default else "y/N"
    print(f"\n{prompt} ({default_str}): ", end="")
    response = input().strip().lower()

    if not response:
        return default

    return response in ['y', 'yes']


def get_output_filename(default: str) -> str:
    """
    Get output filename from user.

    Args:
        default: Default filename to suggest

    Returns:
        Chosen filename with .py extension
    """
    print(f"\nOutput filename (default: {default}):")
    filename = input("> ").strip()

    if not filename:
        filename = default

    if not filename.endswith('.py'):
        filename += '.py'

    return filename
