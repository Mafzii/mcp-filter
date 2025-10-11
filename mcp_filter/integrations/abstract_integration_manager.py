"""
Abstract Integration Manager

Abstract base class for managing MCP server integrations across different AI tools.
"""

from abc import ABC, abstractmethod
from typing import Dict


class AbstractIntegrationManager(ABC):
    """
    Abstract base class for tool-specific integration managers.

    Each AI tool (Claude Code, Claude Desktop, GitHub Copilot, etc.)
    should implement this interface to provide consistent integration management.
    """

    @abstractmethod
    def get_tool_name(self) -> str:
        """
        Get the human-readable name of the tool.

        Returns:
            Tool name (e.g., "Claude Code", "Claude Desktop", "GitHub Copilot")
        """
        pass

    @abstractmethod
    def config_exists(self) -> bool:
        """
        Check if the tool's configuration directory/file exists.

        Returns:
            True if config exists, False otherwise
        """
        pass

    @abstractmethod
    def get_config_path(self) -> str:
        """
        Get the absolute path to the configuration file.

        Returns:
            Absolute path as string
        """
        pass

    @abstractmethod
    def load_config(self) -> Dict:
        """
        Load existing MCP servers configuration.

        Returns:
            Configuration dictionary (tool-specific format)
        """
        pass

    @abstractmethod
    def save_config(self, config: Dict) -> bool:
        """
        Save MCP servers configuration.

        Args:
            config: Configuration dictionary to save

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def add_server(
        self,
        name: str,
        script_path: str,
        overwrite: bool = False
    ) -> bool:
        """
        Add a generated MCP server to the tool's configuration.

        Args:
            name: Server name/identifier
            script_path: Absolute path to the generated Python script
            overwrite: If True, overwrite existing server with same name

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def remove_server(self, name: str) -> bool:
        """
        Remove a server from the tool's configuration.

        Args:
            name: Server name to remove

        Returns:
            True if removed, False if not found or error
        """
        pass

    @abstractmethod
    def list_servers(self) -> Dict[str, Dict]:
        """
        Get all configured MCP servers.

        Returns:
            Dictionary of server configurations (tool-specific format)
        """
        pass

    def is_available(self) -> bool:
        """
        Check if this tool is available/installed on the system.

        Default implementation checks if config exists.
        Can be overridden for more sophisticated detection.

        Returns:
            True if tool is available, False otherwise
        """
        return self.config_exists()
