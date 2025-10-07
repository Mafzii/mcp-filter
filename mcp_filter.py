#!/usr/bin/env python3
"""
MCP Tool Filter - Filter tools from existing MCP servers
"""
import json
import subprocess
import sys
import os
from typing import Dict, List, Any, Tuple
from pathlib import Path


def get_mcp_tools(mcp_command: str) -> Dict[str, Any]:
    """Connect to an MCP server and retrieve all available tools."""
    try:
        # Run the MCP command and communicate via stdio
        process = subprocess.Popen(
            mcp_command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "mcp-filter",
                    "version": "1.0.0"
                }
            }
        }

        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response
        response_line = process.stdout.readline()
        init_response = json.loads(response_line)

        # Send initialized notification
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        process.stdin.write(json.dumps(initialized) + "\n")
        process.stdin.flush()

        # Request tools list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()

        # Read tools response
        tools_response_line = process.stdout.readline()
        tools_response = json.loads(tools_response_line)

        process.terminate()

        return tools_response.get("result", {}).get("tools", [])

    except Exception as e:
        print(f"Error connecting to MCP server: {e}", file=sys.stderr)
        return []


def load_mcp_servers() -> Dict[str, str]:
    """Load MCP servers from config file."""
    config_file = Path.home() / ".config" / "mcp-filter" / "servers.json"

    # If no user config exists, check for default servers file
    if not config_file.exists():
        default_file = Path(__file__).parent / "default_servers.json"
        if default_file.exists():
            try:
                with open(default_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def save_mcp_servers(servers: Dict[str, str]) -> None:
    """Save MCP servers to config file."""
    config_dir = Path.home() / ".config" / "mcp-filter"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "servers.json"

    with open(config_file, 'w') as f:
        json.dump(servers, indent=2, fp=f)


def display_servers(servers: Dict[str, str]) -> List[str]:
    """Display available MCP servers and return list of names."""
    if not servers:
        print("\nNo MCP servers configured.")
        print("Add servers using: --add-server <name> <command>")
        return []

    print("\nAvailable MCP Servers:")
    server_names = list(servers.keys())
    for idx, name in enumerate(server_names, 1):
        print(f"{idx}. {name}")
    return server_names


def select_server(server_names: List[str], servers: Dict[str, str]) -> Tuple[str, str]:
    """Allow user to select an MCP server by number."""
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


def display_tools(tools: List[Dict[str, Any]]) -> None:
    """Display available tools in a readable format."""
    print("\nAvailable Tools:")
    for idx, tool in enumerate(tools, 1):
        print(f"{idx}. {tool.get('name', 'Unknown')}")
    print()


def display_tools_detailed(tools: List[Dict[str, Any]], selected_names: List[str]) -> None:
    """Display detailed information about selected tools."""
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


def select_tools(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Allow user to select which tools to include."""
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


def generate_filtered_mcp(server_commands: Dict[str, str], selected_tools: List[Dict[str, Any]], output_file: str) -> None:
    """Generate a wrapper script that filters MCP servers to only expose selected tools.

    Args:
        server_commands: Dict mapping server names to their commands
        selected_tools: List of tool dicts with 'name' and 'server' keys
        output_file: Path to output file
    """
    tool_names = [tool['name'] for tool in selected_tools]

    # Group tools by server
    tools_by_server = {}
    for tool in selected_tools:
        server = tool.get('server', 'unknown')
        if server not in tools_by_server:
            tools_by_server[server] = []
        tools_by_server[server].append(tool['name'])

    wrapper_code = f'''#!/usr/bin/env python3
"""
Filtered MCP Server Wrapper
Auto-generated by mcp-filter
Combines tools from multiple MCP servers
"""
import json
import subprocess
import sys
from typing import Dict, List

ALLOWED_TOOLS = {json.dumps(tool_names, indent=4)}

# Server configurations
SERVERS = {json.dumps(server_commands, indent=4)}

# Tools grouped by server
TOOLS_BY_SERVER = {json.dumps(tools_by_server, indent=4)}

class MultiServerProxy:
    def __init__(self):
        self.processes = {{}}
        self.request_id = 0

    def start_servers(self):
        """Start all required MCP servers."""
        for server_name, command in SERVERS.items():
            if server_name in TOOLS_BY_SERVER:
                try:
                    process = subprocess.Popen(
                        command.split(),
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=sys.stderr,
                        text=True,
                        bufsize=1
                    )

                    # Initialize the server
                    init_request = {{
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "initialize",
                        "params": {{
                            "protocolVersion": "2024-11-05",
                            "capabilities": {{}},
                            "clientInfo": {{"name": "mcp-filter", "version": "1.0.0"}}
                        }}
                    }}
                    process.stdin.write(json.dumps(init_request) + "\\n")
                    process.stdin.flush()
                    process.stdout.readline()  # Read init response

                    # Send initialized notification
                    initialized = {{"jsonrpc": "2.0", "method": "notifications/initialized"}}
                    process.stdin.write(json.dumps(initialized) + "\\n")
                    process.stdin.flush()

                    self.processes[server_name] = process
                except Exception as e:
                    print(f"Failed to start {{server_name}}: {{e}}", file=sys.stderr)

    def get_all_tools(self):
        """Retrieve all allowed tools from all servers."""
        all_tools = []
        for server_name, process in self.processes.items():
            try:
                tools_request = {{
                    "jsonrpc": "2.0",
                    "id": self.request_id,
                    "method": "tools/list",
                    "params": {{}}
                }}
                self.request_id += 1

                process.stdin.write(json.dumps(tools_request) + "\\n")
                process.stdin.flush()

                response_line = process.stdout.readline()
                response = json.loads(response_line)

                if "result" in response and "tools" in response["result"]:
                    server_tools = [
                        tool for tool in response["result"]["tools"]
                        if tool["name"] in TOOLS_BY_SERVER.get(server_name, [])
                    ]
                    all_tools.extend(server_tools)
            except Exception as e:
                print(f"Error getting tools from {{server_name}}: {{e}}", file=sys.stderr)

        return all_tools

    def route_request(self, request):
        """Route a tool call request to the appropriate server."""
        if request.get("method") == "tools/call":
            tool_name = request.get("params", {{}}).get("name")

            # Find which server has this tool
            for server_name, tool_list in TOOLS_BY_SERVER.items():
                if tool_name in tool_list and server_name in self.processes:
                    process = self.processes[server_name]
                    process.stdin.write(json.dumps(request) + "\\n")
                    process.stdin.flush()
                    response_line = process.stdout.readline()
                    return json.loads(response_line)

            return {{
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {{"code": -32601, "message": f"Tool {{tool_name}} not found"}}
            }}

        return None

    def shutdown(self):
        """Terminate all server processes."""
        for process in self.processes.values():
            process.terminate()

def main():
    proxy = MultiServerProxy()
    proxy.start_servers()

    try:
        for line in sys.stdin:
            request = json.loads(line)

            # Handle initialize request
            if request.get("method") == "initialize":
                response = {{
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {{
                        "protocolVersion": "2024-11-05",
                        "capabilities": {{}},
                        "serverInfo": {{"name": "mcp-filter-multi", "version": "1.0.0"}}
                    }}
                }}
                sys.stdout.write(json.dumps(response) + "\\n")
                sys.stdout.flush()

            # Handle initialized notification
            elif request.get("method") == "notifications/initialized":
                pass  # No response needed

            # Handle tools/list request
            elif request.get("method") == "tools/list":
                all_tools = proxy.get_all_tools()
                response = {{
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {{"tools": all_tools}}
                }}
                sys.stdout.write(json.dumps(response) + "\\n")
                sys.stdout.flush()

            # Handle tool calls
            elif request.get("method") == "tools/call":
                response = proxy.route_request(request)
                if response:
                    sys.stdout.write(json.dumps(response) + "\\n")
                    sys.stdout.flush()

            # Forward other requests to first available server
            else:
                if proxy.processes:
                    first_server = list(proxy.processes.values())[0]
                    first_server.stdin.write(line)
                    first_server.stdin.flush()
                    response_line = first_server.stdout.readline()
                    sys.stdout.write(response_line)
                    sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        proxy.shutdown()

if __name__ == "__main__":
    main()
'''

    with open(output_file, 'w') as f:
        f.write(wrapper_code)

    # Make executable
    import os
    os.chmod(output_file, 0o755)

    print(f"\nFiltered MCP server created: {output_file}")
    print(f"Included tools: {', '.join(tool_names)}")
    print(f"Servers used: {', '.join(tools_by_server.keys())}")


def select_multiple_servers(server_names: List[str]) -> List[str]:
    """Allow user to select multiple servers."""
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


def collect_tools_from_servers(selected_server_names: List[str], servers: Dict[str, str]) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """Collect tools from multiple servers and let user select which ones to include."""
    all_tools = []
    server_commands = {}

    for server_name in selected_server_names:
        print(f"\n{'='*60}")
        print(f"Connecting to {server_name}...")
        print(f"{'='*60}")

        tools = get_mcp_tools(servers[server_name])

        if not tools:
            print(f"⚠️  No tools found or unable to connect to {server_name}.")
            continue

        server_commands[server_name] = servers[server_name]

        # Tag tools with their server
        for tool in tools:
            tool['server'] = server_name

        print(f"\nAvailable tools from {server_name}:")
        for idx, tool in enumerate(tools, 1):
            print(f"  {idx}. {tool.get('name', 'Unknown')}")

        print(f"\nSelect tools from {server_name} (comma-separated numbers, 'all', or 'none'):")
        selection = input("> ").strip()

        if selection.lower() == 'none':
            continue
        elif selection.lower() == 'all':
            all_tools.extend(tools)
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                selected = [tools[i] for i in indices if 0 <= i < len(tools)]
                all_tools.extend(selected)
            except (ValueError, IndexError):
                print("Invalid selection. Skipping this server.")

    return all_tools, server_commands


def interactive_session(servers: Dict[str, str], output_dir: str = "output"):
    """Run an interactive session allowing multiple filter creations."""
    while True:
        print("\n" + "="*60)
        print("MCP FILTER - Interactive Session")
        print("="*60)

        server_names = display_servers(servers)
        if not server_names:
            print("\nNo servers available. Exiting.")
            break

        # Select servers
        selected_server_names = select_multiple_servers(server_names)
        print(f"\n✓ Selected servers: {', '.join(selected_server_names)}")

        # Collect tools from all selected servers
        all_selected_tools, server_commands = collect_tools_from_servers(selected_server_names, servers)

        if not all_selected_tools:
            print("\n⚠️  No tools selected from any server.")
            retry = input("\nTry again? (y/n): ").strip().lower()
            if retry != 'y':
                break
            continue

        # Display summary
        print("\n" + "="*60)
        print("SELECTED TOOLS SUMMARY")
        print("="*60)
        for tool in all_selected_tools:
            print(f"  • {tool['name']} (from {tool['server']})")

        # Generate output filename
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"filtered_server_{timestamp}.py"
        print(f"\nOutput filename (default: {default_filename}):")
        filename = input("> ").strip()
        if not filename:
            filename = default_filename
        if not filename.endswith('.py'):
            filename += '.py'

        output_path = os.path.join(output_dir, filename)

        # Generate the filtered server
        generate_filtered_mcp(server_commands, all_selected_tools, output_path)
        print(f"\n✅ Filtered server created: {output_path}")
        print(f"Run with: python3 {output_path}")

        # Ask if user wants to create another
        print("\n" + "="*60)
        another = input("\nCreate another filtered server? (y/n): ").strip().lower()
        if another != 'y':
            print("\n👋 Thanks for using MCP Filter!")
            break


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Filter tools from existing MCP servers"
    )
    parser.add_argument(
        "--add-server",
        nargs=2,
        metavar=('NAME', 'COMMAND'),
        help="Add an MCP server configuration"
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

    args = parser.parse_args()
    servers = load_mcp_servers()

    # Handle add server command
    if args.add_server:
        name, command = args.add_server
        servers[name] = command
        save_mcp_servers(servers)
        print(f"Added server '{name}': {command}")
        return

    # Handle list servers command
    if args.list_servers:
        display_servers(servers)
        return

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Main flow: select servers, show tools, filter (in a loop)
    if not servers:
        print("\nNo MCP servers configured.")
        print("Add a server first: python mcp_filter.py --add-server <name> <command>")
        print("\nExample:")
        print("  python mcp_filter.py --add-server notion 'npx -y @modelcontextprotocol/server-notion'")
        sys.exit(1)

    # Run interactive session
    interactive_session(servers, args.output_dir)


if __name__ == "__main__":
    main()
