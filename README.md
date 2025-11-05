# MCP Tool Filter

Combine specific tools from multiple MCP servers into one custom server.

## Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# (Optional) Set up authentication for servers that require it
cp .env.example ~/.config/mcp-filter/.env
# Edit ~/.config/mcp-filter/.env and add your API keys

# Run interactive mode
python -m mcp_filter

# Or list available servers (🔑 indicates auth required)
python -m mcp_filter --list-servers
```

## What It Does

Select specific tools from multiple MCP servers and combine them into a single filtered server.

**Example**: Create a server with only:
- `create_page` from Notion
- `get_deployments` from Vercel

## Interactive Mode

```bash
python -m mcp_filter
```

1. Select servers (e.g., `1,3` for Notion + Vercel)
2. If a server requires authentication (shown with 🔑), you'll be prompted to enter API keys
3. Pick tools from each server
4. Get a combined filtered server in `output/`
5. Optionally add to Claude Code config automatically

## Programmatic Usage

```python
from mcp_filter import CodeGenerator

selected_tools = [
    {"name": "create_page", "server": "notion"},
    {"name": "get_deployments", "server": "vercel"},
]

server_commands = {
    "notion": "npx -y mcp-remote https://mcp.notion.com/mcp",
    "vercel": "npx -y mcp-remote https://mcp.vercel.com/mcp",
}

CodeGenerator.generate_filtered_mcp(
    server_commands=server_commands,
    selected_tools=selected_tools,
    output_file="my_server.py"
)
```

## Managing Servers

```bash
# Add server
python -m mcp_filter --add-server myserver "command to start server"

# Remove server
python -m mcp_filter --remove-server myserver

# List servers
python -m mcp_filter --list-servers
```

## Using Generated Servers

### In Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-filtered-server": {
      "command": "python3",
      "args": ["/absolute/path/to/output/filtered_server.py"]
    }
  }
}
```

### Standalone

```bash
python3 output/filtered_server.py
```

## Default Servers

- **notion** - https://mcp.notion.com/mcp
- **github** 🔑 - Official GitHub MCP (requires Docker + `GITHUB_PERSONAL_ACCESS_TOKEN`)
- **vercel** - https://mcp.vercel.com/mcp

## Requirements

- Python 3.6+
- npx (Node.js)
- Docker (required for GitHub MCP server)
- Internet connection

## Authentication

Some MCP servers require API keys or tokens (indicated with 🔑).

### Setup

1. Copy the example environment file:
```bash
cp .env.example ~/.config/mcp-filter/.env
```

2. Edit `~/.config/mcp-filter/.env` and add your credentials:
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

3. When you run `python -m mcp_filter`, the tool will:
   - Automatically use credentials from the `.env` file
   - Prompt you to enter any missing credentials
   - Save new credentials to `.env` for future use
   - Include credentials in the Claude Code config

### Where to get credentials

- **GitHub Personal Access Token**:
  - Create at https://github.com/settings/tokens
  - Required scopes: `repo`, `read:packages`, `read:org`
  - Requires Docker to be installed and running

## Troubleshooting

**Server won't connect:**
- Servers marked with 🔑 require authentication - check your `.env` file
- Try Notion first (no auth required)

**No servers listed:**
```bash
python -m mcp_filter --add-server notion "npx -y mcp-remote https://mcp.notion.com/mcp"
```

## Project Structure

```
mcp_filter/
├── core/           # MCP client, config, code generation
├── cli/            # Display and input handling
└── interactive.py  # Main workflow
```

## Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Servers List](https://github.com/modelcontextprotocol/servers)
- [Claude Desktop](https://claude.ai/download)
