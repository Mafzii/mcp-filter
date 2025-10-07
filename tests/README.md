# MCP Filter Test Scripts

This directory contains test scripts for validating MCP server connections and the mcp-filter tool.

## Available Test Scripts

### 1. test_notion.sh
Tests the Notion MCP server connection.

**Usage:**
```bash
./tests/test_notion.sh
```

**What it tests:**
- npx availability
- Lists configured servers
- Connects to Notion MCP server
- Selects and filters tools (1, 2, 3)
- Generates a filtered server wrapper

**Requirements:**
- Node.js and npx installed
- Internet connection
- No authentication required

---

### 2. test_github.sh
Tests the GitHub MCP server connection and diagnoses authentication issues.

**Usage:**
```bash
./tests/test_github.sh
```

**What it tests:**
- npx availability
- GitHub MCP endpoint accessibility
- Authentication status (HTTP 401 check)
- Direct connection attempt
- Detailed diagnostics

**Requirements:**
- Node.js and npx installed
- GitHub Copilot subscription
- Authenticated GitHub session

**Known Issue:**
The GitHub MCP server requires authentication (returns HTTP 401). You need:
1. Active GitHub Copilot subscription
2. Valid authentication token/session
3. May need to authenticate via `gh auth login`

---

### 3. test_canva.sh
Tests the Canva MCP server connection and diagnoses authentication issues.

**Usage:**
```bash
./tests/test_canva.sh
```

**What it tests:**
- npx availability
- Canva MCP endpoint accessibility
- Authentication status (HTTP 401 check)
- Connection attempt with mcp_filter.py
- Detailed diagnostics

**Requirements:**
- Node.js and npx installed
- Canva account (possibly)
- Canva API credentials or authentication

**Known Issue:**
The Canva MCP server requires authentication (returns HTTP 401). You may need:
1. Active Canva account
2. API key or authentication token
3. Canva developer/enterprise subscription

---

## Common Issues

### GitHub MCP Authentication Error
**Symptom:** `Error connecting to MCP server: Expecting value: line 1 column 1 (char 0)`

**Root Cause:** GitHub MCP endpoint returns HTTP 401 (Unauthorized)

**Solutions:**
1. Ensure you have GitHub Copilot subscription active
2. Authenticate using GitHub CLI: `gh auth login`
3. The server may require additional authentication headers
4. Try using the Notion server instead (no auth required)

### Timeout Command Not Found (macOS)
**Symptom:** `timeout: command not found`

**Solution:** The test scripts now handle this automatically. If needed, install coreutils:
```bash
brew install coreutils
```

---

## Test Output Files

When tests succeed, they create filtered server files:
- `tests/test_filtered_notion.py` - Filtered Notion MCP server
- `tests/test_github_output.py` - Filtered GitHub MCP server (if auth succeeds)

These can be run directly:
```bash
python3 tests/test_filtered_notion.py
```

---

## Adding New Test Scripts

To add a new MCP server test:

1. Create a new script: `tests/test_<server_name>.sh`
2. Make it executable: `chmod +x tests/test_<server_name>.sh`
3. Follow the pattern from existing test scripts
4. Update this README with the new test

---

## Debugging

Enable verbose output by adding `-x` to the bash shebang:
```bash
#!/bin/bash -x
```

Or run with bash -x:
```bash
bash -x tests/test_github.sh
```
