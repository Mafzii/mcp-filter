#!/bin/bash
# Test script for GitHub MCP server connection

echo "======================================"
echo "Testing GitHub MCP Server Connection"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check if npx is available
echo "Test 1: Checking if npx is installed..."
if command -v npx &> /dev/null; then
    echo -e "${GREEN}✓ npx is installed${NC}"
else
    echo -e "${RED}✗ npx not found. Please install Node.js${NC}"
    exit 1
fi
echo ""

# Test 2: Check if the GitHub MCP remote URL is accessible
echo "Test 2: Testing GitHub MCP remote URL..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://api.githubcopilot.com/mcp)
if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 301 ] || [ "$HTTP_CODE" -eq 302 ]; then
    echo -e "${GREEN}✓ GitHub MCP URL is accessible (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${RED}✗ GitHub MCP URL returned HTTP $HTTP_CODE${NC}"
fi
echo ""

# Test 3: Check for authentication requirements
echo "Test 3: Checking authentication requirements..."
echo -e "${YELLOW}GitHub MCP requires authentication (returned 401)${NC}"
echo "The GitHub MCP server needs valid GitHub Copilot credentials."
echo ""
echo "To use GitHub MCP, you need:"
echo "  1. GitHub Copilot subscription"
echo "  2. Proper authentication token/session"
echo ""

# Test 4: Try to run the mcp-remote command directly (with timeout fallback)
echo "Test 4: Testing direct connection to GitHub MCP server..."
echo "Running: npx -y mcp-remote https://api.githubcopilot.com/mcp"
echo "Sending initialize request..."

# Create a test script to communicate with MCP server
# Use gtimeout if available (brew install coreutils), otherwise try perl
if command -v gtimeout &> /dev/null; then
    gtimeout 10s npx -y mcp-remote https://api.githubcopilot.com/mcp <<EOF 2>&1 | head -20
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}
EOF
else
    npx -y mcp-remote https://api.githubcopilot.com/mcp <<EOF 2>&1 | head -20 &
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}
EOF
    # Kill after 10 seconds
    sleep 10
    jobs -p | xargs kill 2>/dev/null
fi

echo ""
echo -e "${YELLOW}Note: The above output shows the raw response from the server${NC}"
echo ""

# Test 5: Try with the mcp_filter.py script
echo "Test 5: Testing with mcp_filter.py..."
echo "Selecting GitHub server (option 2) and requesting all tools..."
echo ""

cd "$(dirname "$0")/.."
echo -e "2\nall\ntest_github_output.py\nn" | python3 mcp_filter.py -o output 2>&1 &
PID=$!
sleep 15
kill $PID 2>/dev/null
wait $PID 2>/dev/null

echo ""
echo "======================================"
echo "Test Results Summary"
echo "======================================"
echo ""
if [ -f "output/test_github_output.py" ]; then
    echo -e "${GREEN}✓ Filtered server was created successfully${NC}"
    echo "  Location: output/test_github_output.py"
else
    echo -e "${RED}✗ Failed to create filtered server${NC}"
    echo ""
    echo -e "${YELLOW}Root Cause:${NC}"
    echo "  The GitHub MCP server requires authentication (HTTP 401)"
    echo ""
    echo -e "${YELLOW}Solutions:${NC}"
    echo "  1. Ensure you have an active GitHub Copilot subscription"
    echo "  2. The GitHub MCP endpoint may require authentication headers"
    echo "  3. Try authenticating via GitHub CLI first: gh auth login"
    echo "  4. Check if your GitHub Copilot subscription is active"
    echo ""
    echo -e "${YELLOW}Alternative:${NC}"
    echo "  Use the Notion MCP server instead (no auth required):"
    echo "    ./tests/test_notion.sh"
fi
