# 🤖 Claude Code - MCP Filter Project

> **AI-Powered Development Notes** — Generated with Claude Code

---

## 📋 Project Overview

**MCP Filter** is a Python tool that connects to Model Context Protocol (MCP) servers, retrieves available tools, and generates filtered wrapper scripts that expose only selected tools.

### Key Features

- 🔌 Connect to any MCP server via stdio
- 🔍 Discover and list available tools
- ✂️ Filter and select specific tools
- 🎁 Generate standalone filtered server wrappers
- 💾 Manage multiple server configurations

---

## 🚨 Current Issues

### GitHub MCP Authentication Problem

**Status:** 🔴 **Not Working**

The GitHub MCP server requires authentication:

```bash
❌ Error: Expecting value: line 1 column 1 (char 0)
```

**Root Cause:**
- GitHub endpoint returns `HTTP 401 (Unauthorized)`
- Requires active GitHub Copilot subscription
- Needs authentication token/session

**Test it yourself:**
```bash
./tests/test_github.sh
```

---

### Notion MCP Server

**Status:** 🟢 **Working**

The Notion server works without authentication:

```bash
./tests/test_notion.sh
```

---

### Canva MCP Server

**Status:** 🔴 **Not Working**

The Canva server also requires authentication:

```bash
❌ HTTP 401 (Unauthorized)
```

**Test it yourself:**
```bash
./tests/test_canva.sh
```

---

## 🧪 Testing Infrastructure

### Available Test Scripts

| Script | Purpose | Status | Requirements |
|--------|---------|--------|--------------|
| `tests/test_github.sh` | Diagnose GitHub MCP auth issues | ⚠️ Auth Required | GitHub Copilot subscription |
| `tests/test_notion.sh` | Test Notion MCP connection | ✅ Working | Internet connection only |
| `tests/test_canva.sh` | Diagnose Canva MCP auth issues | ⚠️ Auth Required | Canva account/API key |

### Running Tests

```bash
# Test GitHub (shows auth diagnostics)
./tests/test_github.sh

# Test Notion (working example)
./tests/test_notion.sh
```

---

## 📁 Project Structure

```
mcp-filter/
├── mcp_filter.py              # Main script
├── default_servers.json       # Default MCP server configs
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
├── GITHUB_ISSUE.md           # Detailed auth issue analysis
├── CLAUDE.md                 # This file! 👋
│
├── tests/                    # Test suite
│   ├── README.md            # Test documentation
│   ├── test_github.sh       # GitHub MCP diagnostics
│   ├── test_canva.sh        # Canva MCP diagnostics
│   └── test_notion.sh       # Notion MCP test (working!)
│
└── test_filtered_notion.py  # Example filtered server output
```

---

## 🔧 How It Works

### 1. Server Configuration

Servers are stored in `default_servers.json`:

```json
{
  "notion": "npx -y mcp-remote https://mcp.notion.com/mcp",
  "github": "npx -y mcp-remote https://api.githubcopilot.com/mcp",
  "canva": "npx -y mcp-remote https://mcp.canva.com/mcp"
}
```

### 2. Tool Discovery Process

```python
# 1. Initialize MCP connection
initialize_request → MCP Server

# 2. Send initialized notification
initialized_notification → MCP Server

# 3. Request available tools
tools/list → MCP Server

# 4. Receive tools list
← tools_response (JSON)
```

### 3. Filter Generation

The script generates a Python wrapper that:
- Forwards all JSON-RPC requests to the original server
- Intercepts `tools/list` responses
- Filters out non-selected tools
- Returns filtered response to client

---

## 🎯 Use Cases

### Example 1: Notion Database Tools Only

```bash
# Run the filter tool
python3 mcp_filter.py

# Select Notion server (1)
# Choose specific database tools (e.g., 1,3,5)
# Output: filtered_mcp_server.py

# Use the filtered server
python3 filtered_mcp_server.py
```

### Example 2: GitHub Code Search Only

```bash
# First, authenticate with GitHub
gh auth login

# Run the filter tool
python3 mcp_filter.py

# Select GitHub server (2)
# Choose only search tools
# Output: filtered_github.py
```

---

## 🐛 Known Issues & Solutions

### Issue 1: GitHub Authentication

**Problem:**
```
Error connecting to MCP server: Expecting value: line 1 column 1 (char 0)
```

**Solutions:**

1. **Authenticate with GitHub CLI**
   ```bash
   gh auth login
   ```

2. **Verify Copilot Subscription**
   - Check: https://github.com/settings/copilot
   - Ensure subscription is active

3. **Use Alternative Server**
   ```bash
   # Use Notion instead (no auth required)
   ./tests/test_notion.sh
   ```

### Issue 2: macOS `timeout` Command

**Problem:** `timeout: command not found`

**Solution:** Test scripts now handle this automatically. Optionally:
```bash
brew install coreutils  # Provides gtimeout
```

---

## 🚀 Quick Start Guide

### Installation

```bash
# Clone or navigate to project
cd /path/to/mcp-filter

# Install dependencies
pip3 install -r requirements.txt

# Verify setup
python3 mcp_filter.py --list-servers
```

### Basic Usage

```bash
# Add a new server
python3 mcp_filter.py --add-server myserver "npx -y @mcp/server-name"

# List available servers
python3 mcp_filter.py --list-servers

# Create filtered server (interactive)
python3 mcp_filter.py -o my_filtered_server.py
```

---

## 📊 Test Results

### Latest Test Run

```bash
./tests/test_github.sh
```

**Output:**
```
======================================
Testing GitHub MCP Server Connection
======================================

✓ npx is installed
✗ GitHub MCP URL returned HTTP 401

Root Cause:
  The GitHub MCP server requires authentication (HTTP 401)

Solutions:
  1. Ensure you have an active GitHub Copilot subscription
  2. The GitHub MCP endpoint may require authentication headers
  3. Try authenticating via GitHub CLI first: gh auth login
  4. Check if your GitHub Copilot subscription is active
```

---

## 🔮 Future Enhancements

### Planned Features

- [ ] **OAuth/Token Authentication Support**
  - Add auth token handling to `mcp_filter.py`
  - Support GitHub Copilot authentication
  - Environment variable for credentials

- [ ] **Configuration Improvements**
  - YAML config file support
  - Per-server authentication settings
  - Server aliases and tags

- [ ] **Testing Enhancements**
  - Automated CI/CD tests
  - Mock MCP server for testing
  - Integration tests for each server type

- [ ] **CLI Improvements**
  - Better error messages
  - Progress indicators
  - Dry-run mode

---

## 💡 Tips & Tricks

### For Developers

**Debugging MCP Communication:**
```bash
# See raw JSON-RPC messages
python3 mcp_filter.py 2>&1 | grep -A5 "jsonrpc"
```

**Test a server manually:**
```bash
npx -y mcp-remote https://mcp.notion.com/mcp
# Then send:
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}
```

### For Users

**Quick filter creation:**
```bash
# Select all tools from Notion
echo -e "1\nall" | python3 mcp_filter.py -o notion_all.py
```

**Check generated wrapper:**
```bash
cat filtered_mcp_server.py | grep ALLOWED_TOOLS
```

---

## 📚 Resources

### MCP Documentation
- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP Servers List](https://github.com/modelcontextprotocol/servers)

### Related Files
- **Main Docs:** [`README.md`](./README.md)
- **GitHub Issue:** [`GITHUB_ISSUE.md`](./GITHUB_ISSUE.md)
- **Test Docs:** [`tests/README.md`](./tests/README.md)

### Getting Help

1. **Run diagnostics:** `./tests/test_github.sh` or `./tests/test_notion.sh`
2. **Check logs:** Look for JSON parse errors in stderr
3. **Verify auth:** `gh auth status` for GitHub
4. **Test connectivity:** `curl https://mcp.notion.com/mcp`

---

## 🎨 Code Highlights

### Key Functions

**`get_mcp_tools(mcp_command)` — `mcp_filter.py:13-76`**
- Connects to MCP server via subprocess
- Sends JSON-RPC initialize request
- Retrieves tools list
- Returns parsed tool definitions

**`generate_filtered_mcp(...)` — `mcp_filter.py:188-259`**
- Creates filtered wrapper script
- Embeds allowed tools list
- Generates forwarding proxy logic
- Makes output executable

**`select_tools(tools)` — `mcp_filter.py:166-185`**
- Interactive tool selection
- Supports comma-separated indices
- "all" keyword for bulk selection
- Input validation and retry logic

---

## 🏆 Success Metrics

| Metric | Status | Notes |
|--------|--------|-------|
| Notion Connection | ✅ | Works without auth |
| GitHub Connection | ⚠️ | Requires auth implementation |
| Canva Connection | ⚠️ | Requires auth implementation |
| Tool Discovery | ✅ | JSON-RPC flow working |
| Filter Generation | ✅ | Creates valid Python wrappers |
| Test Coverage | 🟡 | 3 servers, all documented |

---

## 🤝 Contributing

### Adding a New MCP Server

1. **Add to config:**
   ```bash
   python3 mcp_filter.py --add-server myserver "npx -y @scope/server"
   ```

2. **Create test script:**
   ```bash
   cp tests/test_notion.sh tests/test_myserver.sh
   # Edit and customize
   chmod +x tests/test_myserver.sh
   ```

3. **Update documentation:**
   - Add to `tests/README.md`
   - Document any auth requirements
   - Note in `CLAUDE.md` (this file)

---

## 📝 Notes from Development

### What Worked Well
- ✅ Simple stdio-based MCP communication
- ✅ Clean JSON-RPC request/response handling
- ✅ Wrapper script generation approach
- ✅ Test script diagnostics

### What Needs Improvement
- ⚠️ No authentication support (blocks GitHub)
- ⚠️ Limited error handling for edge cases
- ⚠️ No async/concurrent server testing
- ⚠️ Manual configuration management

### Lessons Learned
1. **Auth is critical** — Many MCP servers require it
2. **Diagnostics matter** — Test scripts reveal real issues
3. **Documentation helps** — Clear error messages save time
4. **Start simple** — Notion works great for prototyping

---

## 🎬 Quick Demo

```bash
# 1. Test the working server
./tests/test_notion.sh

# Expected output:
# ✓ npx is installed
# ✓ Filtered Notion server created successfully
#   Location: tests/test_filtered_notion.py

# 2. Examine the filtered server
head -30 tests/test_filtered_notion.py

# 3. (Optional) Run the filtered server
python3 tests/test_filtered_notion.py
# Send JSON-RPC requests via stdin
```

---

## 📅 Timeline

| Date | Event | Status |
|------|-------|--------|
| Initial | Project created | ✅ |
| Oct 5 | Notion integration working | ✅ |
| Oct 6 | GitHub auth issue discovered | 🔴 |
| Oct 7 | Test suite created | ✅ |
| Oct 7 | Documentation added | ✅ |
| Future | Auth implementation | ⏳ |

---

<div align="center">

**Built with ❤️ using Claude Code**

*Last updated: 2025-10-07*

[Report an Issue](./GITHUB_ISSUE.md) • [View Tests](./tests/README.md) • [Main README](./README.md)

</div>
