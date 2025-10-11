# MCP Tool Filter

Combine specific tools from multiple MCP servers into one custom server.

## Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run interactive mode
python -m mcp_filter

# Or list available servers
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
2. Pick tools from each server
3. Get a combined filtered server in `output/`

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
- **github** - https://api.githubcopilot.com/mcp (requires auth)
- **vercel** - https://mcp.vercel.com/mcp
- **canva** - https://mcp.canva.com/mcp
- **atlassian** - https://mcp.atlassian.com/mcp
- **asana** - https://mcp.asana.com/mcp
- **zapier** - https://mcp.zapier.com/mcp

## Requirements

- Python 3.6+
- npx (Node.js)
- Internet connection

## Troubleshooting

**Server won't connect:**
- Some servers require authentication (GitHub, Canva)
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
