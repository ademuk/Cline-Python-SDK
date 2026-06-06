# Cline Python SDK Architecture

This document describes how the Cline Python SDK is organized, how components interact, and the design principles that guide development.

## Layered Model

The SDK is organized as a layered runtime stack:

```
cline_shared          (types, schemas, hooks, path resolution)
    ^
    |
cline_llms            (provider gateway, model catalogs, handlers)
    ^
    |
cline_agents          (agent loop, tool execution, streaming)
    ^
    |
cline_core            (orchestration, sessions, persistence, RPC)
    ^
    |
Host Applications     (CLI, Slack bots, web services, etc.)
```

## Package Responsibilities

### `cline_shared`

Owns reusable low-level contracts and infrastructure:

- Shared types and schemas
- Path resolution and storage helpers
- Hook contracts and engine
- Extension registry contracts
- Prompt and parsing helpers
- Basic logger interface
- Telemetry primitives

**Design rule:** Should not depend on higher-level runtime packages.

### `cline_llms`

Owns model/provider runtime concerns:

- Provider settings and config resolution
- Model catalogs and manifests
- Provider gateway contracts
- Handler creation and provider execution code
- Support for Anthropic, OpenAI, Google, AWS Bedrock, Mistral, etc.

**Design rule:** Provider-specific behavior should be isolated here.

### `cline_agents`

Owns the stateless runtime loop:

- Agent iteration loop
- Tool orchestration and execution
- Runtime event emission
- Hook/extension execution
- Turn preparation before provider calls
- In-memory team/runtime primitives

**Design rule:** Should not own persistent storage or host lifecycle concerns.

### `cline_core`

Owns stateful orchestration:

- Runtime composition
- Session lifecycle and management
- Storage and persistence (SQLite)
- Config watching/loading
- Settings listing and mutation
- Default host tool assembly
- Plugin discovery and loading
- Context compaction policy
- Telemetry integration
- RPC runtime services

**Design rules:**

- Is the app-facing orchestration layer over `agents`
- Handles all persistence concerns
- Manages plugin lifecycle
- Exposes high-level session APIs

## Runtime Flows

### Local In-Process Runtime

1. Host constructs an `Agent` through `cline_sdk`
2. `cline_agents` runs the loop using `cline_llms` handlers
3. Events stream back to the host through callbacks

### Session-Based Runtime (ClineCore)

1. Host creates `ClineCore` instance
2. `ClineCore` manages session lifecycle
3. Persists sessions to SQLite
4. Discovers config from `.cline/` directories
5. Supports resumable sessions and RPC communication

## Design Seams

### 1. Config Watchers

Core uses file-based discovery and watchers for:
- Rules
- Workflows
- Skills
- Agents
- Hooks
- Plugins

### 2. Runtime Builder

`DefaultRuntimeBuilder` composes a runtime from:
- Tools
- Hooks
- Extensions
- User instructions
- Telemetry

### 3. Plugin System

Plugins register:
- Tools
- Hooks (before_run, after_run, before_tool, after_tool)
- Automation events
- Custom behavior

### 4. Tool Execution

Tools are defined with:
- Name and description
- JSON Schema for inputs
- Async execute function
- Optional metadata

### 5. Event Streaming

All runtime events are observable:
- `content_start` / `content_update` / `content_done`
- `tool_start` / `tool_result` / `tool_error`
- `usage` (token counts)
- `agent_done`

## File Structure

```
cline_sdk/
├── __init__.py                 # Public API exports
├── shared/
│   ├── types.py               # Core types and schemas
│   ├── hooks.py               # Hook engine and contracts
│   ├── extensions.py          # Extension registry
│   ├── logger.py              # Basic logger interface
│   └── utils.py               # Utility functions
├── llms/
│   ├── provider.py            # Provider base class
│   ├── models.py              # Model catalogs
│   ├── handlers/              # Provider-specific handlers
│   │   ├── anthropic.py
│   │   ├── openai.py
│   │   ├── google.py
│   │   └── bedrock.py
│   └── config.py              # Provider configuration
├── agents/
│   ├── agent.py               # Agent class and loop
│   ├── tool_execution.py      # Tool call handling
│   ├── events.py              # Event types and emission
│   ├── runtime.py             # Runtime state and management
│   └── teams.py               # Multi-agent support
└── core/
    ├── cline_core.py          # Main orchestrator
    ├── session.py             # Session management
    ├── runtime_host.py        # Runtime host abstraction
    ├── persistence/           # Storage adapters
    │   ├── sqlite.py
    │   └── schemas.py
    ├── config/                # Configuration discovery
    │   ├── discovery.py
    │   └── watchers.py
    ├── extensions/            # Extension loading
    │   ├── plugin.py
    │   └── tools.py
    └── tools/                 # Built-in tools
        ├── bash.py
        ├── editor.py
        ├── read_files.py
        └── fetch_web.py
```

## Key Types

- **`Agent`** (`cline_agents.agent.Agent`) - The agent loop
- **`ClineCore`** (`cline_core.cline_core.ClineCore`) - Main orchestrator
- **`Tool`** (`cline_shared.types.Tool`) - Tool definition
- **`AgentEvent`** (`cline_shared.types.AgentEvent`) - Runtime events
- **`AgentPlugin`** (`cline_shared.extensions.AgentPlugin`) - Plugin base class
- **`Hook`** (`cline_shared.hooks.Hook`) - Hook definition

## Architectural Constraints

### Keep `agents` Stateless

Do not move these into `cline_agents`:
- Session persistence
- Provider settings storage
- RPC lifecycle
- Host-specific approvals
- Config caching

### Keep `core` Generic

Do not make `cline_core` organization- or provider-specific.

### Use One-Way Dependency Flow

Higher layers can depend on lower layers, but not vice versa:
- `cline_core` → `cline_agents` → `cline_llms` → `cline_shared`

## Testing Strategy

- **Unit tests**: Test individual components (tools, hooks, handlers)
- **Integration tests**: Test agent loop with mocked LLMs
- **E2E tests**: Test full workflows with real providers (optional, requires API keys)

## Development Workflow

1. Add types to `cline_shared`
2. Implement provider handlers in `cline_llms`
3. Implement runtime behavior in `cline_agents`
4. Add orchestration in `cline_core`
5. Export public API from `__init__.py`
6. Add tests and examples
