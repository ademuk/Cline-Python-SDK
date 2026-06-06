"""Extension and plugin system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from cline_sdk.shared.types import Tool


@dataclass
class PluginManifest:
    """Manifest for a plugin."""

    capabilities: List[str] = field(default_factory=list)  # ["tools", "hooks", ...]
    version: str = "1.0.0"
    requires: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentPlugin(ABC):
    """Base class for agent plugins."""

    name: str
    manifest: PluginManifest = PluginManifest()

    @abstractmethod
    def setup(self, api: "PluginAPI") -> None:
        """Called when plugin is loaded."""
        pass

    def before_run(self) -> None:
        """Hook called before agent run."""
        pass

    def after_run(self, result: Any) -> None:
        """Hook called after agent run."""
        pass

    def before_tool(self, tool_call: Any) -> None:
        """Hook called before tool execution."""
        pass

    def after_tool(self, tool_result: Any) -> None:
        """Hook called after tool execution."""
        pass


class PluginAPI:
    """API provided to plugins for registration and interaction."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
        self._hooks: Dict[str, List[Any]] = {}

    def register_tool(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool

    def unregister_tool(self, tool_name: str) -> None:
        """Unregister a tool."""
        if tool_name in self._tools:
            del self._tools[tool_name]

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a registered tool."""
        return self._tools.get(tool_name)

    def get_tools(self) -> Dict[str, Tool]:
        """Get all registered tools."""
        return self._tools.copy()

    def register_hook(self, hook_name: str, hook_fn: Any) -> None:
        """Register a hook."""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(hook_fn)
