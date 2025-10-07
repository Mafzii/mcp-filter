# GitHub MCP Server Issue - Authentication Required

## Problem Summary

The `mcp_filter.py` script fails when trying to connect to the GitHub MCP server with the error:

```
Error connecting to MCP server: Expecting value: line 1 column 1 (char 0)
```

## Root Cause

The GitHub MCP server endpoint `https://api.githubcopilot.com/mcp` requires authentication and returns **HTTP 401 (Unauthorized)** when accessed without proper credentials.

## Technical Details

### What's Happening

1. The script tries to connect to: `npx -y mcp-remote https://api.githubcopilot.com/mcp`
2. The server responds with HTTP 401 (Unauthorized)
3. Instead of valid JSON-RPC response, the script receives an authentication error
4. JSON parsing fails: "Expecting value: line 1 column 1 (char 0)"

### Why Notion Works But GitHub Doesn't

- **Notion MCP:** `https://mcp.notion.com/mcp` - Public endpoint, no auth required
- **GitHub MCP:** `https://api.githubcopilot.com/mcp` - Requires GitHub Copilot subscription + auth

## Solutions

### Option 1: Authenticate with GitHub Copilot

Requirements:
1. Active GitHub Copilot subscription
2. GitHub CLI installed
3. Authenticated session

Steps:
```bash
# Install GitHub CLI if not already installed
brew install gh

# Authenticate
gh auth login

# Try the test script again
./tests/test_github.sh
```

### Option 2: Use a Different MCP Server

The Notion server works without authentication:

```bash
./tests/test_notion.sh
```

### Option 3: Update the mcp_filter.py Script

To support authenticated servers, the script would need to:

1. Pass authentication headers/tokens to `mcp-remote`
2. Support OAuth flow or token-based auth
3. Handle different authentication methods per server

**Example enhancement needed in `mcp_filter.py:17-23`:**

```python
# Current code:
process = subprocess.Popen(
    mcp_command.split(),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Would need to add:
# - Environment variables for auth tokens
# - Support for authentication headers
# - OAuth token refresh logic
```

## Testing

Run the diagnostic test script:

```bash
./tests/test_github.sh
```

This will show:
- ✓ npx installation status
- ✗ HTTP 401 authentication error
- Detailed diagnostics
- Suggested solutions

## Workaround

Until authentication is implemented, use MCP servers that don't require auth:

1. **Notion** - `npx -y mcp-remote https://mcp.notion.com/mcp`
2. **Other public MCP servers** - Check https://github.com/modelcontextprotocol/servers

## Related Files

- `/tests/test_github.sh` - GitHub MCP diagnostic test
- `/tests/test_notion.sh` - Working Notion MCP test
- `/tests/README.md` - Test documentation
- `/default_servers.json` - Server configurations

## Next Steps

To fully support GitHub MCP:

1. Research GitHub Copilot MCP authentication requirements
2. Add authentication token support to `mcp_filter.py`
3. Update `default_servers.json` with auth config
4. Test with valid GitHub Copilot credentials
