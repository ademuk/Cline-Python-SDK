"""Tests for agent module."""

import pytest
from cline_sdk import Agent


def test_agent_creation():
    """Test basic agent creation."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="Test",
    )
    assert agent.config.provider_id == "anthropic"
    assert agent.config.model_id == "claude-opus-4-7"
    assert agent.has_run is False


def test_agent_run():
    """Test agent run."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="Test",
    )
    result = agent.run("Hello")
    assert result.text is not None
    assert result.iterations >= 0
    assert agent.has_run is True


@pytest.mark.asyncio
async def test_agent_run_async():
    """Test async agent run."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="Test",
    )
    result = await agent.run_async("Hello")
    assert result.text is not None
