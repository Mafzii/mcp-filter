"""
MCP Client - Handle communication with MCP servers

This module provides the MCPClient class for connecting to and communicating
with Model Context Protocol servers via stdio.
"""

import json
import subprocess
import sys
from typing import Dict, List, Any, Optional


class MCPClient:
    """Client for communicating with MCP servers via stdio."""

    def __init__(self, command: str):
        """
        Initialize MCP client with a server command.

        Args:
            command: The command to start the MCP server (e.g., "npx -y mcp-remote https://...")
        """
        self.command = command
        self.process: Optional[subprocess.Popen] = None

    def connect(self) -> bool:
        """
        Start the MCP server process.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.process = subprocess.Popen(
                self.command.split(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except Exception as e:
            print(f"Error starting MCP server: {e}", file=sys.stderr)
            return False

    def initialize(self) -> Optional[Dict[str, Any]]:
        """
        Send initialize request to the MCP server.

        Returns:
            Server response dict or None if failed
        """
        if not self.process:
            return None

        try:
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "mcp-filter",
                        "version": "1.0.0"
                    }
                }
            }

            self.process.stdin.write(json.dumps(init_request) + "\n")
            self.process.stdin.flush()

            response_line = self.process.stdout.readline()
            return json.loads(response_line)

        except Exception as e:
            print(f"Error during initialization: {e}", file=sys.stderr)
            return None

    def send_initialized_notification(self) -> bool:
        """
        Send initialized notification to the MCP server.

        Returns:
            True if successful, False otherwise
        """
        if not self.process:
            return False

        try:
            initialized = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            self.process.stdin.write(json.dumps(initialized) + "\n")
            self.process.stdin.flush()
            return True

        except Exception as e:
            print(f"Error sending initialized notification: {e}", file=sys.stderr)
            return False

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Request the list of available tools from the MCP server.

        Returns:
            List of tool dictionaries, or empty list if failed
        """
        if not self.process:
            return []

        try:
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }

            self.process.stdin.write(json.dumps(tools_request) + "\n")
            self.process.stdin.flush()

            tools_response_line = self.process.stdout.readline()
            tools_response = json.loads(tools_response_line)

            return tools_response.get("result", {}).get("tools", [])

        except Exception as e:
            print(f"Error retrieving tools: {e}", file=sys.stderr)
            return []

    def disconnect(self) -> None:
        """Terminate the MCP server process."""
        if self.process:
            self.process.terminate()
            self.process = None

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """
        Connect to server, initialize, and retrieve all tools.

        This is a convenience method that handles the full connection lifecycle.

        Returns:
            List of tool dictionaries, or empty list if any step fails
        """
        try:
            if not self.connect():
                return []

            if not self.initialize():
                self.disconnect()
                return []

            if not self.send_initialized_notification():
                self.disconnect()
                return []

            tools = self.get_tools()
            self.disconnect()

            return tools

        except Exception as e:
            print(f"Error connecting to MCP server: {e}", file=sys.stderr)
            self.disconnect()
            return []

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
