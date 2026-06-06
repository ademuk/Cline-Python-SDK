"""Cline Python SDK - Build AI agents that can take actions."""

__version__ = "0.1.0"

# Core exports
from cline_sdk.agents.agent import Agent
from cline_sdk.core.cline_core import ClineCore
from cline_sdk.shared.extensions import AgentPlugin
from cline_sdk.shared.hooks import Hook
from cline_sdk.shared.types import (
    AgentConfig,
    AgentEvent,
    AgentResult,
    ContentEvent,
    Tool,
    ToolCall,
    ToolResult,
)
from cline_sdk.shared.utils import create_tool

__all__ = [
    # Main classes
    "Agent",
    "ClineCore",
    # Types
    "AgentConfig",
    "AgentEvent",
    "AgentResult",
    "ContentEvent",
    "Tool",
    "ToolCall",
    "ToolResult",
    # Plugins and extensions
    "AgentPlugin",
    "Hook",
    # Utilities
    "create_tool",
]
