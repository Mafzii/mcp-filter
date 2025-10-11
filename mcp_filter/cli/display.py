"""
Display Functions - User interface display utilities

This module provides functions for displaying information to users in a
formatted and readable manner.
"""

from typing import Dict, List, Any


def display_servers(servers: Dict[str, str]) -> List[str]:
    """
    Display available MCP servers and return list of names.

    Args:
        servers: Dictionary mapping server names to their commands

    Returns:
        List of server names in display order
    """
    if not servers:
        print("\nNo MCP servers configured.")
        print("Add servers using: --add-server <name> <command>")
        return []

    print("\nAvailable MCP Servers:")
    server_names = list(servers.keys())
    for idx, name in enumerate(server_names, 1):
        print(f"{idx}. {name}")
    return server_names


def display_tools(tools: List[Dict[str, Any]]) -> None:
    """
    Display available tools in a simple list format.

    Args:
        tools: List of tool dictionaries with at least 'name' key
    """
    print("\nAvailable Tools:")
    for idx, tool in enumerate(tools, 1):
        print(f"{idx}. {tool.get('name', 'Unknown')}")
    print()


def display_tools_detailed(tools: List[Dict[str, Any]], selected_names: List[str]) -> None:
    """
    Display detailed information about selected tools.

    Args:
        tools: List of all tool dictionaries
        selected_names: List of tool names to display details for
    """
    print("\nSelected Tools (detailed):")
    print("=" * 80)
    for tool in tools:
        if tool.get('name') in selected_names:
            print(f"\n• {tool.get('name', 'Unknown')}")
            print(f"  Description: {tool.get('description', 'No description')}")
            if 'inputSchema' in tool:
                props = tool['inputSchema'].get('properties', {})
                if props:
                    print(f"  Parameters: {', '.join(props.keys())}")
    print("\n" + "=" * 80)


def display_server_tools(server_name: str, tools: List[Dict[str, Any]]) -> None:
    """
    Display tools available from a specific server.

    Args:
        server_name: Name of the server
        tools: List of tool dictionaries
    """
    print(f"\nAvailable tools from {server_name}:")
    for idx, tool in enumerate(tools, 1):
        print(f"  {idx}. {tool.get('name', 'Unknown')}")


def display_summary(selected_tools: List[Dict[str, Any]]) -> None:
    """
    Display summary of selected tools grouped by server.

    Args:
        selected_tools: List of selected tool dictionaries with 'server' key
    """
    print("\n" + "=" * 60)
    print("SELECTED TOOLS SUMMARY")
    print("=" * 60)
    for tool in selected_tools:
        server = tool.get('server', 'unknown')
        print(f"  • {tool['name']} (from {server})")


def display_separator(title: str = "", width: int = 60) -> None:
    """
    Display a separator line with optional title.

    Args:
        title: Optional title to display in the separator
        width: Width of the separator line
    """
    if title:
        print("\n" + "=" * width)
        print(title)
        print("=" * width)
    else:
        print("\n" + "=" * width)


def display_success(message: str) -> None:
    """
    Display a success message.

    Args:
        message: Success message to display
    """
    print(f"\n✅ {message}")


def display_warning(message: str) -> None:
    """
    Display a warning message.

    Args:
        message: Warning message to display
    """
    print(f"\n⚠️  {message}")


def display_error(message: str) -> None:
    """
    Display an error message.

    Args:
        message: Error message to display
    """
    print(f"\n❌ {message}")
