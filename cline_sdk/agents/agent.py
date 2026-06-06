"""Agent implementation."""

import asyncio
from typing import Callable, List, Optional

from cline_sdk.shared.types import AgentConfig, AgentEvent, AgentResult, Tool


class Agent:
    """AI Agent that can execute tools."""

    def __init__(self, config: Optional[AgentConfig] = None, **kwargs) -> None:
        """Initialize agent.

        Args:
            config: Agent configuration
            **kwargs: Alternative config parameters
        """
        if config is None:
            config = AgentConfig(
                provider_id=kwargs.get("provider_id", "anthropic"),
                model_id=kwargs.get("model_id", "claude-opus-4-7"),
                system_prompt=kwargs.get("system_prompt", ""),
                tools=kwargs.get("tools", []),
                max_iterations=kwargs.get("max_iterations", 100),
                temperature=kwargs.get("temperature"),
                top_p=kwargs.get("top_p"),
                api_key=kwargs.get("api_key"),
                on_event=kwargs.get("on_event"),
                on_error=kwargs.get("on_error"),
            )

        self.config = config
        self.has_run = False
        self._history: List[dict] = []

    def run(self, prompt: str) -> AgentResult:
        """Run agent synchronously.

        Args:
            prompt: User prompt

        Returns:
            AgentResult
        """
        return asyncio.run(self.run_async(prompt))

    async def run_async(self, prompt: str) -> AgentResult:
        """Run agent asynchronously.

        Args:
            prompt: User prompt

        Returns:
            AgentResult
        """
        # This is a placeholder - actual implementation would:
        # 1. Call LLM provider
        # 2. Handle tool calls
        # 3. Emit events
        # 4. Return result

        self._emit_event(
            AgentEvent(
                type="agent_done",
                text=f"Mock response to: {prompt}",
            )
        )

        self.has_run = True
        return AgentResult(
            text=f"Mock response to: {prompt}",
            iterations=1,
        )

    def continue_conversation(self, prompt: str) -> AgentResult:
        """Continue conversation.

        Args:
            prompt: User message

        Returns:
            AgentResult
        """
        return self.run(prompt)

    async def continue_conversation_async(self, prompt: str) -> AgentResult:
        """Continue conversation asynchronously.

        Args:
            prompt: User message

        Returns:
            AgentResult
        """
        return await self.run_async(prompt)

    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent.

        Args:
            tool: Tool to add
        """
        if tool not in self.config.tools:
            self.config.tools.append(tool)

    def _emit_event(self, event: AgentEvent) -> None:
        """Emit an event.

        Args:
            event: Event to emit
        """
        if self.config.on_event:
            self.config.on_event(event)
