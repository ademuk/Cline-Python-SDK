"""Tests for tool system."""

import pytest
from cline_sdk import create_tool


def test_create_tool():
    """Test tool creation."""
    tool = create_tool(
        name="test_tool",
        description="A test tool",
        input_schema={"type": "object"},
        execute=lambda x: {"result": "success"},
    )

    assert tool.name == "test_tool"
    assert tool.description == "A test tool"
    assert callable(tool.execute)


def test_tool_execution():
    """Test tool execution."""
    def add(input_data):
        return {"result": input_data.get("a", 0) + input_data.get("b", 0)}

    tool = create_tool(
        name="add",
        description="Add two numbers",
        input_schema={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
        },
        execute=add,
    )

    result = tool.execute({"a": 5, "b": 3})
    assert result["result"] == 8
