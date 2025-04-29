# tests/test_tool_registry.py
import sys
import importlib
import pytest

from agent_tooling import tool, get_tool_schemas, get_tool_function, discover_tools
from agent_tooling.tool import tool_registry

@pytest.fixture(autouse=True)
def clear_registry():
    # reset between tests
    tool_registry.tool_schemas.clear()
    tool_registry.tool_functions.clear()
    yield
    tool_registry.tool_schemas.clear()
    tool_registry.tool_functions.clear()

def test_direct_decorator_registration():
    @tool(tags=["test"])
    def double(x: int) -> int:
        """Double it."""
        return x * 2

    schemas = get_tool_schemas()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "double"
    fn = get_tool_function("double")
    assert fn is not None
    assert fn(3) == 6

def test_dynamic_discovery(tmp_path, monkeypatch):
    # 1) create a fake package
    pkg = tmp_path / "pkg_agents"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "mymod.py").write_text(
        "from agent_tooling import tool\n"
        "@tool\ndef greet(name: str) -> str:\n"
        "    return 'Hello ' + name\n"
    )

    # 2) patch sys.path
    monkeypatch.syspath_prepend(str(tmp_path))

    # 🛠 3) RE-IMPORT agent_tooling fresh under pytest sys.path
    import importlib
    import sys
    if "agent_tooling" in sys.modules:
        del sys.modules["agent_tooling"]
    agent_tooling = importlib.import_module("agent_tooling")

    # 4) force import the dynamic package
    importlib.import_module("pkg_agents")

    # 5) discover tools
    agent_tooling.discover_tools(["pkg_agents"])
    schemas = agent_tooling.get_tool_schemas()
    assert any(s["name"] == "greet" for s in schemas)

def test_openai_client_importable():
    # just ensure module loads under whichever name you choose
    # e.g. openai_client or openai
    import importlib
    try:
        m = importlib.import_module("agent_tooling.openai_client")
    except ModuleNotFoundError:
        m = importlib.import_module("agent_tooling.openai")
    assert hasattr(m, "OpenAITooling")
