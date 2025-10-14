# MCP Filter Tests

Test scripts for validating MCP server connections and filtered server generation.

## Available Tests

### `test_github_create_issue.sh`

Tests the generation of a filtered GitHub MCP server with only the `create_issue` capability.

**Features:**
- Validates GitHub server configuration
- Checks for `GITHUB_TOKEN` in environment or `.env` file
- Attempts to connect to GitHub Copilot MCP server
- Falls back to demo mode if authentication fails
- Generates a filtered server with only issue creation capability

**Usage:**
```bash
./tests/test_github_create_issue.sh
```

**Requirements:**
- `GITHUB_TOKEN` in `~/.config/mcp-filter/.env` or environment
- For live mode: Active GitHub Copilot subscription

**Output:**
- `tests/test_github_create_issue_only.py` - Filtered MCP server

**Demo Mode:**
If GitHub authentication fails (expected without Copilot subscription), the test runs in demo mode using a mock `create_issue` tool to demonstrate the filtering functionality.

### `test_notion.sh`

Tests connection to the Notion MCP server (no authentication required).

**Usage:**
```bash
./tests/test_notion.sh
```

**Features:**
- Validates Notion MCP server connection
- No authentication required
- Good for testing basic MCP connectivity

## Running All Tests

```bash
# GitHub test (may run in demo mode)
./tests/test_github_create_issue.sh

# Notion test (should always work)
./tests/test_notion.sh
```

## Adding New Tests

To create a new test:

1. Create a shell script in `tests/`
2. Use the Python API to interact with MCP servers:

```python
from mcp_filter.core.mcp_client import MCPClient
from mcp_filter.core.config import ConfigManager
from mcp_filter.core.env_manager import EnvManager
from mcp_filter.core.generator import CodeGenerator

# Load server config
config_manager = ConfigManager()
servers = config_manager.load_servers()
server_config = servers.get('server_name')

# Check authentication
env_manager = EnvManager()
token = env_manager.get('TOKEN_NAME')

# Connect and get tools
client = MCPClient(server_config['command'])
tools = client.get_all_tools()

# Generate filtered server
CodeGenerator.generate_filtered_mcp(
    server_commands={'server_name': server_config['command']},
    selected_tools=[{'name': 'tool_name', 'server': 'server_name'}],
    output_file='output/filtered_server.py'
)
```

3. Make the script executable: `chmod +x tests/your_test.sh`

## Authentication Testing

Tests automatically check for required authentication:

1. Checks system environment variables
2. Falls back to `~/.config/mcp-filter/.env`
3. Provides clear error messages if auth is missing
4. Some tests support demo mode for testing without real credentials

## Expected Test Results

| Test | Without Auth | With Auth |
|------|-------------|-----------|
| `test_github_create_issue.sh` | Demo mode (mock tool) | Live mode (real GitHub MCP) |
| `test_notion.sh` | Works | Works |

## Troubleshooting

**Test fails with "GITHUB_TOKEN not found":**
```bash
cp .env.example ~/.config/mcp-filter/.env
# Edit ~/.config/mcp-filter/.env and add your GITHUB_TOKEN
```

**Test fails with "HTTP 401":**
- GitHub requires an active Copilot subscription
- Token may need additional scopes
- Test will automatically fall back to demo mode

**Generated server doesn't work:**
- Check that environment variables are set in Claude Code config
- Verify the MCP server URL is accessible
- Check `stderr` output for detailed error messages
