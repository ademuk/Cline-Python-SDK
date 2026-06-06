"""Hooks and events example."""

import os
from cline_sdk import Agent
from cline_sdk.shared.types import EventType


def handle_event(event):
    """Handle agent events."""
    if event.type == EventType.CONTENT_UPDATE:
        if event.content_type == "text":
            print(event.text, end="", flush=True)
    elif event.type == EventType.CONTENT_START:
        if event.content_type == "tool":
            print(f"\n[Calling {event.tool_name}]")
    elif event.type == EventType.USAGE:
        print(
            f"\n[Tokens: {event.input_tokens} in, {event.output_tokens} out]",
            flush=True,
        )
    elif event.type == EventType.AGENT_DONE:
        print("\n[Agent completed]")


def main():
    """Run agent with event streaming."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="You are a helpful assistant.",
        tools=[],
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        on_event=handle_event,
    )

    print("Streaming agent response...\n")
    result = agent.run("Tell me a short story about a robot learning to paint.")
    print(f"\n\nFinal result:\n{result.text}")


if __name__ == "__main__":
    main()
