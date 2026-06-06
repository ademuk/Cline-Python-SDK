# Contributing to Cline Python SDK

We'd love your help! Here's how to get started.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -e ".[dev]"`

## Development

- Run tests: `pytest`
- Run tests with coverage: `pytest --cov`
- Format code: `black .`
- Lint: `flake8`
- Type check: `mypy cline_sdk`

## Code Style

- Use type hints for all functions
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use `black` for formatting
- Keep lines under 100 characters

## Architecture Guidelines

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information on:
- Package responsibilities
- Layering rules
- Design patterns
- File structure

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Add tests for new functionality
4. Update documentation as needed
5. Run tests and linting
6. Push your branch and open a PR

## Pull Request Process

1. Update the CHANGELOG
2. Ensure all tests pass
3. Update documentation if adding features
4. Request review from maintainers
5. Address feedback
6. Squash and merge when approved

## Testing

All new features should include tests:

```python
import pytest
from cline_sdk import Agent, create_tool

@pytest.mark.asyncio
async def test_custom_tool():
    tool = create_tool(
        name="test",
        description="Test tool",
        input_schema={...},
        execute=async lambda input: {...},
    )
    assert tool.name == "test"
```

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add docstrings to all public APIs
- Include type hints

## Questions?

Join our [Discord](https://discord.gg/cline) to chat with other contributors!
