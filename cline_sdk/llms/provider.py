"""Provider base class and interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from cline_sdk.shared.types import Message, Usage


class Provider(ABC):
    """Base class for LLM providers."""

    def __init__(self, api_key: Optional[str] = None, api_base: Optional[str] = None):
        self.api_key = api_key
        self.api_base = api_base

    @abstractmethod
    async def create_message(
        self,
        model: str,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a message using the provider.

        Args:
            model: Model ID
            messages: Message history
            system_prompt: System prompt
            tools: Available tools
            temperature: Sampling temperature
            top_p: Top-p sampling
            max_tokens: Max tokens in response

        Returns:
            Response dict with 'content', 'usage', 'stop_reason'
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        pass
