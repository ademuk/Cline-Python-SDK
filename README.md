# Cline Python SDK

<div align="center">
<table>
<tbody>
<td align="center">
<a href="https://discord.gg/cline" target="_blank"><strong>Discord</strong></a>
</td>
<td align="center">
<a href="https://www.reddit.com/r/cline/" target="_blank"><strong>r/cline</strong></a>
</td>
<td align="center">
<a href="https://docs.cline.bot/sdk" target="_blank"><strong>Documentation</strong></a>
</td>
</tbody>
</table>
</div>

A Python framework for building AI agents that can edit files, run shell commands, browse the web, call APIs, and use any custom tool you give them.

## Quick Start

```python
from cline_sdk import Agent

agent = Agent(
    provider_id="anthropic",
    model_id="claude-opus-4-7",
    system_prompt="You are a helpful coding assistant.",
    tools=[],
)

result = agent.run("Create a REST API with FastAPI and Python")
print(result.text)
```

## Installation

```bash
pip install cline-sdk
```

## What You Can Build

- Coding agents
- Slack bots
- Scheduled automations
- Code review pipelines
- Multi-agent teams
- IDE integrations
- Anything that benefits from an LLM that can take actions

## Custom Tools

Tools are how agents interact with the world. Define a tool with a name, description, input schema, and execute function:

```python
from cline_sdk import create_tool

deploy = create_tool(
    name="deploy",
    description="Deploy the app to staging or production.",
    input_schema={
        "type": "object",
        "properties": {
            "environment": {"type": "string", "enum": ["staging", "production"]}
        },
        "required": ["environment"],
    },
    execute=async lambda input: {"url": "...", "status": "success"},
)

agent = Agent(
    provider_id="anthropic",
    model_id="claude-opus-4-7",
    system_prompt="You are a deployment assistant.",
    tools=[deploy],
)
```

## Streaming Events

Every event during execution is observable in real time:

```python
from cline_sdk import Agent

def handle_event(event):
    if event.type == "content_update" and event.content_type == "text":
        print(event.text, end="", flush=True)
    elif event.type == "content_start" and event.content_type == "tool":
        print(f"\n[{event.tool_name}]")
    elif event.type == "usage":
        print(f"\nTokens: {event.input_tokens} in, {event.output_tokens} out")

agent = Agent(
    provider_id="anthropic",
    model_id="claude-opus-4-7",
    system_prompt="You are a helpful assistant.",
    tools=[],
    on_event=handle_event,
)
```

## Plugins

Package reusable capabilities as extensions. A plugin can register tools, observe lifecycle events, and modify agent behavior:

```python
from cline_sdk import AgentPlugin

class MetricsPlugin(AgentPlugin):
    name = "metrics"
    capabilities = ["tools", "hooks"]
    
    def setup(self, api):
        api.register_tool(my_custom_tool)
    
    def before_run(self):
        print("Starting agent...")
    
    def before_tool(self, tool_call):
        print(f"Calling tool: {tool_call.tool_name}")
    
    def after_run(self, result):
        print(f"Agent completed: {result.iterations} iterations, {result.usage.output_tokens} tokens")
```

## ClineCore: Full Runtime

When you need session persistence, built-in tools, config discovery, and multi-process support, use `ClineCore`:

```python
from cline_sdk import ClineCore

async def main():
    cline = await ClineCore.create(client_name="my-app")
    
    session = await cline.start(
        prompt="Set up CI with GitHub Actions",
        config={
            "provider_id": "anthropic",
            "model_id": "claude-sonnet-4-6",
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "cwd": "/path/to/project",
            "enable_tools": True,
        },
    )
    
    print(session.result.text if session.result else "No result")
```

`ClineCore` gives the agent built-in tools (`bash`, `editor`, `read_files`, `apply_patch`, `search`, `fetch_web`), persists sessions to SQLite, discovers config from `.cline/` directories, and supports RPC communication.

## Packages

The SDK is a layered stack. Use as much or as little as you need:

| Package | What it does |
|---------|-------------|
| `cline-sdk` | Everything you need -- install this one |
| `cline-core` | Sessions, persistence, built-in tools, config discovery, RPC |
| `cline-agents` | Stateless agent loop with tool execution and streaming |
| `cline-llms` | LLM provider gateway (Anthropic, OpenAI, Google, Bedrock, Mistral, etc.) |
| `cline-shared` | Types, tool creation helpers, hook engine |

## Providers

Works with every major LLM provider out of the box:

| Provider | Models |
|----------|--------|
| Anthropic | Claude Opus 4.7, Sonnet 4.6, Haiku 4.5 |
| OpenAI | GPT-5.5, GPT-5.3 Codex |
| Google | Gemini 3.1 Pro Preview, Gemini 3 Flash Preview |
| AWS Bedrock | Claude, Llama |
| Mistral | Mistral Large, Codestral |
| Any OpenAI-compatible | vLLM, Together, Fireworks, Groq, etc. |

## Documentation

Full documentation at [docs.cline.bot/sdk](https://docs.cline.bot/sdk/overview):

- [Quickstart](https://docs.cline.bot/sdk/quickstart) -- zero to running agent in 5 minutes
- [Core Concepts](https://docs.cline.bot/sdk/agents) -- agents, sessions, tools, events, extensions, hooks
- [Guides](https://docs.cline.bot/sdk/guides/building-an-agent) -- end-to-end tutorials for common patterns
- [Architecture](ARCHITECTURE.md) -- how the SDK is structured and why

## Examples

Explore full working examples in the `examples/` directory:

- [Basic Agent](examples/basic_agent.py) -- Simple agent setup
- [Custom Tools](examples/custom_tools.py) -- Building custom tools
- [Plugins](examples/plugins.py) -- Extensible plugin architecture
- [Hooks](examples/hooks.py) -- Lifecycle hooks and automation

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and contribution process.

## License

[Apache 2.0 © 2026 Cline Bot Inc.](./LICENSE)
