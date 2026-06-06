"""Plugin system example."""

import os
from cline_sdk import Agent, AgentPlugin, create_tool
from cline_sdk.shared.extensions import PluginAPI, PluginManifest


class MetricsPlugin(AgentPlugin):
    """Example plugin that tracks metrics."""

    name = "metrics"
    manifest = PluginManifest(capabilities=["tools", "hooks"])

    def __init__(self):
        self.iterations = 0
        self.tool_calls = 0

    def setup(self, api: PluginAPI) -> None:
        """Register tools with the agent."""
        # Custom tool could be registered here
        pass

    def before_run(self) -> None:
        """Called before agent runs."""
        self.iterations = 0
        self.tool_calls = 0
        print("Agent starting...")

    def before_tool(self, tool_call) -> None:
        """Called before tool execution."""
        self.tool_calls += 1
        print(f"Calling tool: {tool_call.tool_name}")

    def after_run(self, result) -> None:
        """Called after agent completes."""
        print(f"\nAgent completed:")
        print(f"  Iterations: {result.iterations}")
        print(f"  Tool calls: {self.tool_calls}")
        if result.usage:
            print(f"  Tokens: {result.usage.input_tokens} in, {result.usage.output_tokens} out")


def main():
    """Run agent with plugin."""
    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="You are a helpful assistant.",
        tools=[],
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    # In a full implementation, plugins would be registered like:
    # metrics_plugin = MetricsPlugin()
    # agent.register_plugin(metrics_plugin)

    result = agent.run("What are the top 3 programming languages in 2024?")
    print(result.text)


if __name__ == "__main__":
    main()
