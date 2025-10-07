# Changelog

## [2.0.0] - 2025-10-07

### 🎉 Major Features

#### Multi-Server Support
- **Mix and match tools** from multiple MCP servers in a single filtered server
- Select tools from Notion, GitHub, Canva, Vercel, Atlassian, Asana, and Zapier
- Generated servers automatically route requests to the correct upstream server

#### Interactive Loop Mode
- Continuous interactive session for creating multiple filtered servers
- No need to restart the script for each filter
- User-friendly prompts and selections

#### Organized Output
- All generated servers now saved to `output/` directory
- Automatic timestamp-based filenames
- Custom filename support

### ✨ New Servers Added
- Vercel (`https://mcp.vercel.com/`)
- Atlassian (`https://mcp.atlassian.com/v1/sse`)
- Asana (`https://mcp.asana.com/sse`)
- Zapier (`https://mcp.zapier.com/api/mcp/mcp`)
- Canva (`https://mcp.canva.com/mcp`)

### 🔧 Improvements

#### Enhanced Server Selection
- Select multiple servers with comma-separated numbers
- `all` keyword to select all servers
- `none` keyword to skip a server during tool selection

#### Better Tool Selection
- View tools grouped by server
- Select specific tools from each server
- Clear summary of all selected tools before generation

#### Improved User Experience
- Color-coded output (✅ ❌ ⚠️)
- Clear section separators
- Detailed progress indicators
- Friendly prompts and error messages

### 📁 Project Structure Changes
- Created `output/` directory for all generated servers
- Added `.gitignore` to exclude output and cache files
- Updated test scripts to use new output directory

### 📚 Documentation
- New `USAGE.md` with comprehensive examples
- Updated `CLAUDE.md` with latest features
- Enhanced `tests/README.md` with new server info
- Added `CHANGELOG.md` (this file!)

### 🧪 Testing
- Updated all test scripts for new output directory
- Test scripts now properly handle interactive prompts
- Better diagnostics for authentication failures

---

## [1.0.0] - 2025-10-05

### Initial Release

#### Core Features
- Connect to MCP servers via stdio
- Discover available tools
- Filter and select specific tools
- Generate wrapper scripts

#### Initial Servers
- Notion (`https://mcp.notion.com/mcp`)
- GitHub (`https://api.githubcopilot.com/mcp`)

#### Basic Functionality
- Single server, single filter creation
- Command-line server management
- Basic tool filtering

---

## Upcoming Features

### Planned for v2.1.0
- [ ] Authentication support for GitHub, Canva, etc.
- [ ] Configuration file for server credentials
- [ ] Batch mode for automated filter creation
- [ ] Server health checks before selection
- [ ] Tool dependency detection

### Future Considerations
- [ ] Web UI for visual server/tool selection
- [ ] Export/import filter configurations
- [ ] Tool usage analytics
- [ ] Server plugin system
- [ ] Docker containerization

---

## Migration Guide

### From v1.0.0 to v2.0.0

**Old behavior:**
```bash
python3 mcp_filter.py -o my_server.py
# Select one server, create one filter, exit
```

**New behavior:**
```bash
python3 mcp_filter.py -o output
# Select multiple servers, select tools from each
# Create multiple filters in a loop
# All outputs saved to output/ directory
```

**Breaking Changes:**
- `-o` now specifies output **directory**, not file
- Script now runs in interactive loop mode
- Must specify filename during session (or accept default)

**To maintain old behavior:**
Simply answer `n` when asked to create another server:
```
Create another filtered server? (y/n): n
```

---

## Contributors

- Claude Code (AI Assistant)
- Mustafa Afzal (Developer)

---

**Last Updated:** 2025-10-07
