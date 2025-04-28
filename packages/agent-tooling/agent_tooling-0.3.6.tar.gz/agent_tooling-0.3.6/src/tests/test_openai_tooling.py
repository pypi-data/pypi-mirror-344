from agent_tooling import tool, get_tool_schemas


def test_tool_registration_basic():
    @tool(tags=["test"])
    def simple_tool(x: int) -> str:
        """Simple test tool."""
        return f"Got {x}"

    schemas = get_tool_schemas(tags=["test"])

    # We expect at least one tool with "test" tag
    assert any(schema["name"] == "simple_tool" for schema in schemas)