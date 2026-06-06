"""Core types and schemas for the Cline SDK."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime


class EventType(str, Enum):
    """Types of events emitted by the agent."""

    CONTENT_START = "content_start"
    CONTENT_UPDATE = "content_update"
    CONTENT_DONE = "content_done"
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"
    TOOL_ERROR = "tool_error"
    USAGE = "usage"
    AGENT_DONE = "agent_done"
    ERROR = "error"


class ContentType(str, Enum):
    """Types of content in events."""

    TEXT = "text"
    REASONING = "reasoning"
    TOOL = "tool"


@dataclass
class ToolInput:
    """Input to a tool."""

    name: str
    schema: Dict[str, Any]


@dataclass
class Tool:
    """Tool definition."""

    name: str
    description: str
    input_schema: Dict[str, Any]
    execute: Callable[[Dict[str, Any]], Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolCall:
    """A tool call made by the agent."""

    tool_name: str
    tool_input: Dict[str, Any]
    id: Optional[str] = None


@dataclass
class ToolResult:
    """Result of a tool call."""

    tool_name: str
    output: Union[str, Dict[str, Any]]
    error: Optional[str] = None
    is_error: bool = False


@dataclass
class Usage:
    """Token usage information."""

    input_tokens: int
    output_tokens: int
    total_tokens: Optional[int] = None


@dataclass
class AgentEvent:
    """Event emitted during agent execution."""

    type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    content_type: Optional[ContentType] = None
    text: Optional[str] = None
    reasoning: Optional[str] = None
    tool_name: Optional[str] = None
    tool_call: Optional[ToolCall] = None
    tool_result: Optional[ToolResult] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """Result of agent execution."""

    text: str
    iterations: int
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)
    usage: Optional[Usage] = None
    stopped_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContentEvent:
    """Content event with text or reasoning."""

    type: EventType
    content_type: ContentType
    text: Optional[str] = None
    reasoning: Optional[str] = None


@dataclass
class Message:
    """Message in conversation history."""

    role: str  # "user", "assistant", "system"
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AgentConfig:
    """Configuration for creating an agent."""

    provider_id: str
    model_id: str
    system_prompt: str
    tools: List[Tool] = field(default_factory=list)
    max_iterations: int = 100
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    on_event: Optional[Callable[["AgentEvent"], None]] = None
    on_error: Optional[Callable[[Exception], None]] = None
    context_window: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
