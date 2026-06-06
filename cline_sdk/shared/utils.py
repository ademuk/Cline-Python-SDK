"""Utility functions."""

from typing import Any, Callable, Dict, Optional

from cline_sdk.shared.types import Tool


def create_tool(
    name: str,
    description: str,
    input_schema: Dict[str, Any],
    execute: Callable[[Dict[str, Any]], Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> Tool:
    """Create a tool definition.

    Args:
        name: Tool name
        description: Tool description (shown to the model)
        input_schema: JSON Schema for tool inputs
        execute: Async function to execute the tool
        metadata: Optional metadata

    Returns:
        Tool instance
    """
    if metadata is None:
        metadata = {}

    return Tool(
        name=name,
        description=description,
        input_schema=input_schema,
        execute=execute,
        metadata=metadata,
    )
