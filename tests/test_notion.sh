#!/bin/bash
# Test script for Notion MCP server connection

echo "======================================"
echo "Testing Notion MCP Server Connection"
echo "======================================"
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
python3 mcp_filter.py --list-servers
echo ""

# Test 3: Test connection and select tools
echo "Test 3: Testing connection and selecting tools 1,2,3..."
echo "Selecting Notion server (option 1) and tools 1,2,3..."
echo ""

echo -e "1\n1,2,3\ntest_filtered_notion.py\nn" | python3 mcp_filter.py -o output 2>&1

echo ""
echo "======================================"
echo "Test Results Summary"
echo "======================================"
echo ""

if [ -f "output/test_filtered_notion.py" ]; then
    echo -e "${GREEN}✓ Filtered Notion server created successfully${NC}"
    echo "  Location: output/test_filtered_notion.py"
    echo ""
    echo "You can now use this filtered server by running:"
    echo "  python3 output/test_filtered_notion.py"
else
    echo -e "${RED}✗ Failed to create filtered server${NC}"
    echo ""
    echo "Possible issues:"
    echo "  1. Notion MCP server connection failed"
    echo "  2. Network issues"
    echo "  3. The server response format may have changed"
fi
