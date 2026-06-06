"""Basic agent example."""

import os
from cline_sdk import Agent


def main():
    """Run a basic agent."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="You are a helpful coding assistant.",
        tools=[],
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    result = agent.run("What is the capital of France?")
    print(result.text)


if __name__ == "__main__":
    main()
