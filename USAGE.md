# MCP Filter - Usage Guide

## 🚀 Quick Start

### Interactive Mode (Recommended)

Simply run:
```bash
python3 mcp_filter.py
```

This starts an **interactive session** where you can:
- ✅ Select multiple servers
- ✅ Mix and match tools from different servers
- ✅ Create multiple filtered servers in one session
- ✅ All outputs go to the `output/` directory

---

## 📖 Step-by-Step Walkthrough

### Example: Combining Tools from Notion and Vercel

```bash
$ python3 mcp_filter.py

============================================================
MCP FILTER - Interactive Session
============================================================

Available MCP Servers:
1. notion
2. github
3. canva
4. vercel
5. atlassian
6. asana
7. zapier

Select servers (comma-separated numbers, or 'all' for all servers):
> 1,4

✓ Selected servers: notion, vercel

============================================================
Connecting to notion...
============================================================

Available tools from notion:
  1. search_pages
  2. create_page
  3. update_page
  4. get_database
  5. query_database

Select tools from notion (comma-separated numbers, 'all', or 'none'):
> 1,2,5

============================================================
Connecting to vercel...
============================================================

Available tools from vercel:
  1. deploy_project
  2. list_deployments
  3. get_deployment_logs

Select tools from vercel (comma-separated numbers, 'all', or 'none'):
> 1,2

============================================================
SELECTED TOOLS SUMMARY
============================================================
  • search_pages (from notion)
  • create_page (from notion)
  • query_database (from notion)
  • deploy_project (from vercel)
  • list_deployments (from vercel)

Output filename (default: filtered_server_20251007_213045.py):
> my_custom_server.py

✅ Filtered server created: output/my_custom_server.py
Run with: python3 output/my_custom_server.py

============================================================
Create another filtered server? (y/n): n

👋 Thanks for using MCP Filter!
```

---

## 🎯 Common Use Cases

### 1. Single Server, Specific Tools

```bash
python3 mcp_filter.py
# Select: 1 (notion)
# Select tools: 1,3,5
# Filename: notion_search_tools.py
# Continue: n
```

**Output:** `output/notion_search_tools.py` with only selected Notion tools

---

### 2. Multiple Servers, All Tools

```bash
python3 mcp_filter.py
# Select: 1,4,6 (notion, vercel, asana)
# For each server: all
# Filename: [press enter for timestamp]
# Continue: n
```

**Output:** `output/filtered_server_TIMESTAMP.py` with all tools from 3 servers

---

### 3. Mix and Match from Multiple Servers

```bash
python3 mcp_filter.py
# Select: 1,2,4,7 (notion, github, vercel, zapier)
# notion: 1,2,3
# github: none (skip if auth fails)
# vercel: all
# zapier: 2,4,6
# Filename: my_workflow.py
# Continue: n
```

**Output:** `output/my_workflow.py` combining selected tools from multiple servers

---

### 4. Create Multiple Filtered Servers

```bash
python3 mcp_filter.py
# First server:
#   Select: 1
#   Tools: 1,2
#   Filename: notion_basic.py
#   Continue: y
#
# Second server:
#   Select: 4,7
#   vercel: all
#   zapier: 1,3,5
#   Filename: deploy_automation.py
#   Continue: n
```

**Output:**
- `output/notion_basic.py`
- `output/deploy_automation.py`

---

## ⚙️ Command Line Options

### List Available Servers

```bash
python3 mcp_filter.py --list-servers
```

### Add a New Server

```bash
python3 mcp_filter.py --add-server <name> <command>
```

**Example:**
```bash
python3 mcp_filter.py --add-server slack "npx -y mcp-remote https://mcp.slack.com/api/mcp"
```

### Change Output Directory

```bash
python3 mcp_filter.py -o my_custom_output_dir
```

---

## 📂 Output Structure

All generated servers are saved to the `output/` directory:

```
mcp-filter/
├── output/
│   ├── filtered_server_20251007_213045.py
│   ├── my_custom_server.py
│   ├── notion_basic.py
│   └── deploy_automation.py
└── ...
```

---

## 🔧 Using Generated Servers

Once you've created a filtered server, run it like any MCP server:

```bash
# Run the filtered server
python3 output/my_custom_server.py
```

Then send JSON-RPC requests via stdin:

```bash
# Initialize
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | python3 output/my_custom_server.py
```

Or use it in your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "my-filtered-server": {
      "command": "python3",
      "args": ["/path/to/mcp-filter/output/my_custom_server.py"]
    }
  }
}
```

---

## 🛠️ Tips & Tricks

### Skip a Server During Selection

If a server requires authentication or you don't want tools from it:

```
Select tools from github (comma-separated numbers, 'all', or 'none'):
> none
```

### Use Default Filenames

Just press Enter when prompted for filename to use timestamped names:

```
Output filename (default: filtered_server_20251007_213045.py):
> [press Enter]
```

### Select All Servers Quickly

```
Select servers (comma-separated numbers, or 'all' for all servers):
> all
```

### Exit Interactive Mode

Type `n` when asked to create another filtered server:

```
Create another filtered server? (y/n): n
```

Or press `Ctrl+C` anytime to exit.

---

## 🐛 Troubleshooting

### Server Returns No Tools

**Symptom:**
```
⚠️  No tools found or unable to connect to github.
```

**Solution:** Server likely requires authentication. Type `none` to skip it, or see authentication guides in `GITHUB_ISSUE.md`.

---

### Invalid Selection

**Symptom:**
```
Invalid selection. Please enter valid numbers.
```

**Solution:** Enter comma-separated numbers matching the displayed options:
- ✅ Good: `1,2,3` or `1, 2, 3` or `all`
- ❌ Bad: `1-3` or `1 2 3` or `one,two`

---

### Wrong Output Directory

**Symptom:** Can't find generated files

**Solution:** Check the `output/` directory (default) or the directory specified with `-o`:

```bash
ls -la output/
```

---

## 📋 Full Example Session

```bash
$ python3 mcp_filter.py

============================================================
MCP FILTER - Interactive Session
============================================================

Available MCP Servers:
1. notion
2. github
3. canva
4. vercel
5. atlassian
6. asana
7. zapier

Select servers (comma-separated numbers, or 'all' for all servers):
> 1,7

✓ Selected servers: notion, zapier

============================================================
Connecting to notion...
============================================================

Available tools from notion:
  1. search_pages
  2. create_page
  3. update_page

Select tools from notion (comma-separated numbers, 'all', or 'none'):
> all

============================================================
Connecting to zapier...
============================================================

Available tools from zapier:
  1. trigger_zap
  2. list_zaps
  3. create_zap

Select tools from zapier (comma-separated numbers, 'all', or 'none'):
> 1

============================================================
SELECTED TOOLS SUMMARY
============================================================
  • search_pages (from notion)
  • create_page (from notion)
  • update_page (from notion)
  • trigger_zap (from zapier)

Output filename (default: filtered_server_20251007_214530.py):
> automation_server.py

✅ Filtered server created: output/automation_server.py
Run with: python3 output/automation_server.py

============================================================
Create another filtered server? (y/n): y

============================================================
MCP FILTER - Interactive Session
============================================================

Available MCP Servers:
1. notion
2. github
3. canva
4. vercel
5. atlassian
6. asana
7. zapier

Select servers (comma-separated numbers, or 'all' for all servers):
> 4

✓ Selected servers: vercel

============================================================
Connecting to vercel...
============================================================

Available tools from vercel:
  1. deploy_project
  2. list_deployments

Select tools from vercel (comma-separated numbers, 'all', or 'none'):
> all

============================================================
SELECTED TOOLS SUMMARY
============================================================
  • deploy_project (from vercel)
  • list_deployments (from vercel)

Output filename (default: filtered_server_20251007_214601.py):
> vercel_tools.py

✅ Filtered server created: output/vercel_tools.py
Run with: python3 output/vercel_tools.py

============================================================
Create another filtered server? (y/n): n

👋 Thanks for using MCP Filter!
```

**Results:**
- Created `output/automation_server.py` (Notion + Zapier tools)
- Created `output/vercel_tools.py` (All Vercel tools)

---

## 🎓 Advanced Usage

### Multi-Server Proxy Architecture

The generated filtered servers use a **multi-server proxy** architecture:

1. **Start Phase:** Initializes all required MCP servers
2. **Tool Discovery:** Aggregates tools from all servers
3. **Request Routing:** Routes tool calls to the correct server
4. **Response Handling:** Returns responses to client

This allows seamless mixing of tools from different servers!

---

## 📚 Related Documentation

- **Main README:** [`README.md`](./README.md)
- **GitHub Auth Issues:** [`GITHUB_ISSUE.md`](./GITHUB_ISSUE.md)
- **Claude Code Notes:** [`CLAUDE.md`](./CLAUDE.md)
- **Test Scripts:** [`tests/README.md`](./tests/README.md)

---

**Happy filtering! 🎉**
