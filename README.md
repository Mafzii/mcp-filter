# MCP Tool Filter

A simple Python CLI tool that connects to existing MCP (Model Context Protocol) servers, displays all available tools, and creates a filtered MCP server with only the tools you select.

## Installation

No installation required - uses only Python standard library.

```bash
chmod +x mcp_filter.py
```

## Usage

### 1. Using Predefined Servers

The tool comes with predefined popular MCP servers. Just run:

```bash
python mcp_filter.py
```

### 2. Add Custom Servers (Optional)

You can add your own MCP servers:

```bash
python mcp_filter.py --add-server myserver "command to run server"
```

### 3. List Configured Servers

```bash
python mcp_filter.py --list-servers
```

### Example Session

```bash
$ python mcp_filter.py

Available MCP Servers:
1. notion

Select server (number):
> 1

Connecting to notion...

Available Tools:
1. notion_search
2. notion_get_page
3. notion_create_page

Select tools to include (comma-separated numbers, or 'all' for all tools):
> 1, 2

Selected Tools (detailed):
================================================================================

• notion_search
  Description: Search Notion pages
  Parameters: query, limit

• notion_get_page
  Description: Get a specific Notion page
  Parameters: page_id

================================================================================

Filtered server created: filtered_mcp_server.py
Run with: python filtered_mcp_server.py
```

### Specify Output File

```bash
python mcp_filter.py -o my_custom_server.py
```

## How It Works

1. Loads predefined servers from `default_servers.json` or user config from `~/.config/mcp-filter/servers.json`
2. Displays available servers as numbered list
3. Connects to the selected server and retrieves all available tools
4. Shows tools as numbered list
5. Prompts you to select tools by number
6. Displays detailed information about selected tools
7. Generates a wrapper script that filters the original server to only expose selected tools

## Predefined Servers

The tool includes these remote MCP servers by default:
- **notion** - Notion's hosted MCP server at https://mcp.notion.com/mcp

You can add custom servers using `--add-server`, which will be saved to your user config.

## Requirements

- Python 3.6+
- The MCP servers you want to filter must be installed and accessible

## Notes

The generated filtered server acts as a proxy, forwarding requests to the original MCP server but only exposing the tools you selected.
