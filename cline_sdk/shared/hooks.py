"""Hook system for lifecycle events."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol


class HookType(str, Enum):
    """Types of hooks."""

    BEFORE_RUN = "before_run"
    AFTER_RUN = "after_run"
    BEFORE_TOOL = "before_tool"
    AFTER_TOOL = "after_tool"
    ON_ERROR = "on_error"


class Hook(Protocol):
    """Hook protocol for lifecycle events."""

    def __call__(self, **kwargs: Any) -> Any:
        """Execute the hook."""
        ...


@dataclass
class HookContext:
    """Context passed to hooks."""

    hook_type: HookType
    agent: Optional[Any] = None
    tool_call: Optional[Any] = None
    tool_result: Optional[Any] = None
    result: Optional[Any] = None
    error: Optional[Exception] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class HookEngine:
    """Manages hooks and their execution."""

    def __init__(self) -> None:
        self._hooks: Dict[HookType, List[Hook]] = {}
        for hook_type in HookType:
            self._hooks[hook_type] = []

    def register(self, hook_type: HookType, hook: Hook) -> None:
        """Register a hook."""
        self._hooks[hook_type].append(hook)

    def unregister(self, hook_type: HookType, hook: Hook) -> None:
        """Unregister a hook."""
        if hook in self._hooks[hook_type]:
            self._hooks[hook_type].remove(hook)

    async def emit(self, context: HookContext) -> None:
        """Emit a hook event."""
        hooks = self._hooks.get(context.hook_type, [])
        for hook in hooks:
            try:
                if callable(hook):
                    result = hook(context)
                    # Handle async hooks
                    if hasattr(result, "__await__"):
                        await result
            except Exception as e:
                # Hooks should not raise - log and continue
                print(f"Error in {context.hook_type} hook: {e}")
