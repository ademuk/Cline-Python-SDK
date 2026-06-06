"""Custom tools example."""

import os
from cline_sdk import Agent, create_tool


def main():
    """Run agent with custom tools."""

    # Define a custom tool
    calculator = create_tool(
        name="calculate",
        description="Perform mathematical calculations",
        input_schema={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"},
            },
            "required": ["expression"],
        },
        execute=lambda input: {"result": str(eval(input["expression"]))},
    )

    agent = Agent(
        provider_id="anthropic",
        model_id="claude-opus-4-7",
        system_prompt="You are a helpful math tutor. Use the calculator tool to solve problems.",
        tools=[calculator],
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )

    result = agent.run("What is 42 * 7?")
    print(result.text)


if __name__ == "__main__":
    main()
