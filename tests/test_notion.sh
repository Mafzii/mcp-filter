#!/bin/bash
# Test script for Notion + Vercel Multi-MCP Server

echo "=========================================="
echo "Testing Notion + Vercel Multi-MCP Server"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Change to project root directory
cd "$(dirname "$0")/.."

# Test 1: Check if npx is available
echo "Test 1: Checking if npx is installed..."
if command -v npx &> /dev/null; then
    echo -e "${GREEN}✓ npx is installed${NC}"
else
    echo -e "${RED}✗ npx not found. Please install Node.js${NC}"
    exit 1
fi
echo ""

# Test 2: List servers
echo "Test 2: Listing available servers..."
python3 -m mcp_filter --list-servers
echo ""

# Test 3: Test connection and select tools from both servers
echo "Test 3: Creating multi-MCP with Notion + Vercel..."
echo "Selecting Notion (1) and Vercel (4) servers..."
echo "Selecting tools from both servers..."
echo ""

# Input:
# - Select servers: 1,4 (Notion and Vercel)
# - For Notion: select first 3 tools (1,2,3)
# - For Vercel: select first 2 tools (1,2)
echo -e "1,4\n1,2,3\n1,2\n" | python3 -m mcp_filter -o output 2>&1

echo ""
echo "======================================"
echo "Test Results Summary"
echo "======================================"
echo ""

# Check for generated file (it will have a timestamp in the name)
GENERATED_FILE=$(ls -t output/filtered_server_*.py 2>/dev/null | head -1)

if [ -n "$GENERATED_FILE" ] && [ -f "$GENERATED_FILE" ]; then
    echo -e "${GREEN}✓ Multi-MCP server created successfully${NC}"
    echo "  Location: $GENERATED_FILE"
    echo ""
    echo "Selected tools:"
    grep "ALLOWED_TOOLS = " "$GENERATED_FILE" | head -1
    echo ""
    echo "Server configuration:"
    grep -A 5 "SERVERS = {" "$GENERATED_FILE" | head -6
    echo ""
    echo "You can now use this filtered server by running:"
    echo "  python3 $GENERATED_FILE"
else
    echo -e "${RED}✗ Failed to create multi-MCP server${NC}"
    echo ""
    echo "Possible issues:"
    echo "  1. Server connection failed (check auth for Vercel)"
    echo "  2. Network issues"
    echo "  3. Invalid tool selection"
    echo ""
    echo "Try testing with Notion only first:"
    echo "  echo -e '1\\n1,2,3\\n' | python3 -m mcp_filter -o output"
fi
