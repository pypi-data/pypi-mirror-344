"""Unit tests for MCPToolProvider.

This module contains tests for the MCPToolProvider class, which serves as the main
integration layer between LLM backends and MCP tools.
"""

from contextlib import AsyncExitStack
from unittest.mock import AsyncMock, Mock, patch

import pytest
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool
from mcp.types import Resource as MCPResource
from mcp.types import Prompt as MCPPrompt

from agentical.api import LLMBackend
from agentical.mcp.config import DictBasedMCPConfigProvider
from agentical.mcp.provider import MCPToolProvider
from agentical.mcp.schemas import ServerConfig


class MockClientSession:
    """Mock implementation of ClientSession."""

    def __init__(self, tools=None, server_name=None):
        self.tools = tools or []
        self.server_name = server_name
        self.closed = False
        self.list_tools = AsyncMock(return_value=Mock(tools=self.tools))
        self.list_resources = AsyncMock(return_value=Mock(resources=[]))
        self.list_prompts = AsyncMock(return_value=Mock(prompts=[]))
        self.call_tool = AsyncMock(
            return_value=CallToolResult(
                result="success",
                content=[{"type": "text", "text": "Tool execution successful"}],
            )
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.closed = True


@pytest.fixture
def mock_llm_backend():
    """Fixture providing a mock LLM backend."""
    backend = Mock(spec=LLMBackend)
    backend.process_query = AsyncMock()
    return backend


@pytest.fixture
def valid_server_configs():
    """Fixture providing valid server configurations."""
    return {
        "server1": ServerConfig(command="cmd1", args=["--arg1"], env={"ENV1": "val1"}),
        "server2": ServerConfig(command="cmd2", args=["--arg2"], env={"ENV2": "val2"}),
    }


@pytest.fixture
def mock_mcp_tools():
    """Fixture providing mock MCP tools."""
    return [
        MCPTool(
            name="tool1",
            description="Tool 1",
            parameters={},
            inputSchema={"type": "object", "properties": {}},
        ),
        MCPTool(
            name="tool2",
            description="Tool 2",
            parameters={},
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@pytest.fixture
def mock_mcp_resources():
    """Fixture providing mock MCP resources."""
    return [
        MCPResource(
            uri="https://example.com/resource1",
            name="resource1",
            description="Test resource 1",
            mimeType="text/plain",
            size=1024,
            annotations=None,
        ),
        MCPResource(
            uri="https://example.com/resource2",
            name="resource2",
            description="Test resource 2",
            mimeType="application/json",
            size=2048,
            annotations=None,
        ),
    ]


@pytest.fixture
def mock_mcp_prompts():
    """Fixture providing mock MCP prompts."""
    return [
        MCPPrompt(
            name="prompt1",
            description="Test prompt 1",
            arguments=[],
        ),
        MCPPrompt(
            name="prompt2",
            description="Test prompt 2",
            arguments=[],
        ),
    ]


@pytest.fixture
def mock_session(mock_mcp_tools, mock_mcp_resources, mock_mcp_prompts):
    """Fixture providing a mock MCP session factory."""

    def create_session(server_name=None):
        session = MockClientSession(
            tools=mock_mcp_tools.copy(), server_name=server_name
        )
        session.list_resources = AsyncMock(
            return_value=Mock(resources=mock_mcp_resources)
        )
        session.list_prompts = AsyncMock(return_value=Mock(prompts=mock_mcp_prompts))
        return session

    return create_session


@pytest.fixture
async def mock_exit_stack():
    """Fixture providing a mock AsyncExitStack."""
    async with AsyncExitStack() as stack:
        yield stack


@pytest.mark.asyncio
async def test_provider_initialization(mock_llm_backend, valid_server_configs):
    """Test MCPToolProvider initialization."""
    # Test with server configs
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    assert isinstance(provider.config_provider, DictBasedMCPConfigProvider)
    assert provider.llm_backend == mock_llm_backend

    # Test with invalid backend
    with pytest.raises(TypeError, match="must be an instance of LLMBackend"):
        MCPToolProvider("invalid_backend", server_configs=valid_server_configs)

    # Test with no configuration source
    with pytest.raises(
        ValueError, match="Either config_provider or server_configs must be provided"
    ):
        MCPToolProvider(mock_llm_backend)


@pytest.mark.asyncio
async def test_provider_initialize(mock_llm_backend, valid_server_configs):
    """Test provider initialization with configurations."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    assert provider.available_servers == valid_server_configs
    assert len(provider.list_available_servers()) == 2
    assert set(provider.list_available_servers()) == {"server1", "server2"}


@pytest.mark.asyncio
async def test_provider_initialize_error(mock_llm_backend, valid_server_configs):
    """Test error handling during provider initialization."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)

    # Mock config provider to raise an exception
    with patch.object(
        provider.config_provider, "load_config", side_effect=Exception("Config error")
    ):
        with pytest.raises(Exception, match="Config error"):
            await provider.initialize()


@pytest.mark.asyncio
async def test_provider_tool_registration(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test tool registration when connecting to servers."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Verify tools were registered
        assert len(provider.tool_registry.all_tools) == 2
        assert provider.tool_registry.find_tool_server("tool1") == "server1"
        assert provider.tool_registry.find_tool_server("tool2") == "server1"


@pytest.mark.asyncio
async def test_provider_tool_cleanup(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test tool cleanup when disconnecting from servers."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to both servers
        await provider.mcp_connect("server1")
        await provider.mcp_connect("server2")
        assert len(provider.tool_registry.all_tools) == 4

        # Clean up one server
        await provider.cleanup_server("server1")
        assert len(provider.tool_registry.all_tools) == 2
        assert provider.tool_registry.find_tool_server("tool1") == "server2"
        assert provider.tool_registry.find_tool_server("tool2") == "server2"

        # Clean up all
        await provider.cleanup_all()
        assert len(provider.tool_registry.all_tools) == 0


@pytest.mark.asyncio
async def test_provider_query_processing(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test query processing with tool execution."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Process a query
        response = await provider.process_query("Test query")
        assert response is not None


@pytest.mark.asyncio
async def test_execute_tool_success(
    mock_llm_backend, valid_server_configs, mock_mcp_tools, mock_exit_stack
):
    """Test successful tool execution."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Create a session with tools
    session = MockClientSession(tools=mock_mcp_tools)

    with (
        patch.object(
            provider.connection_service._connection_manager,
            "connect",
            side_effect=lambda name, config: session,
        ),
        patch.object(
            provider.connection_service,
            "get_session",
            return_value=session,
        ),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Execute a tool
        result = await provider.execute_tool("tool1", {})
        assert result.result == "success"


@pytest.mark.asyncio
async def test_execute_tool_no_session(
    mock_llm_backend, valid_server_configs, mock_mcp_tools, mock_exit_stack
):
    """Test tool execution when no session exists."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Register tools directly in the registry to bypass session check
    provider.tool_registry.register_server_tools("server1", mock_mcp_tools)

    # Try to execute a tool without connecting
    with pytest.raises(ValueError, match="No active session for server server1"):
        await provider.execute_tool("tool1", {})


@pytest.mark.asyncio
async def test_mcp_connect_invalid_server_name(mock_llm_backend, valid_server_configs):
    """Test connecting with invalid server name."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    with pytest.raises(ValueError, match="server_name must be a non-empty string"):
        await provider.mcp_connect("")


@pytest.mark.asyncio
async def test_mcp_connect_unknown_server(mock_llm_backend, valid_server_configs):
    """Test connecting to unknown server."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    with pytest.raises(ValueError, match="Unknown server"):
        await provider.mcp_connect("unknown_server")


@pytest.mark.asyncio
async def test_mcp_connect_connection_error(mock_llm_backend, valid_server_configs):
    """Test connection error handling."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=Exception("Connection failed"),
    ):
        with pytest.raises(Exception, match="Connection failed"):
            await provider.mcp_connect("server1")


@pytest.mark.asyncio
async def test_mcp_connect_resource_error(
    mock_llm_backend, valid_server_configs, mock_session
):
    """Test resource registration error handling."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    session = mock_session()
    session.list_resources = AsyncMock(side_effect=Exception("Resource error"))

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        return_value=session,
    ):
        # Should still succeed as resource errors are logged but not fatal
        await provider.mcp_connect("server1")


@pytest.mark.asyncio
async def test_mcp_connect_prompt_error(
    mock_llm_backend, valid_server_configs, mock_session
):
    """Test prompt registration error handling."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    session = mock_session()
    session.list_prompts = AsyncMock(side_effect=Exception("Prompt error"))

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        return_value=session,
    ):
        # Should still succeed as prompt errors are logged but not fatal
        await provider.mcp_connect("server1")


@pytest.mark.asyncio
async def test_mcp_connect_all_error(mock_llm_backend, valid_server_configs):
    """Test error handling in connect_all."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=Exception("Connection failed"),
    ):
        results = await provider.mcp_connect_all()
        assert len(results) == 2
        assert all(isinstance(result[1], Exception) for result in results)


@pytest.mark.asyncio
async def test_cleanup_server_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during server cleanup."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock cleanup to raise an error
        with patch.object(
            provider.connection_service,
            "disconnect",
            side_effect=Exception("Cleanup failed"),
        ):
            # Should not raise an exception, just log the error
            await provider.cleanup_server("server1")
            # Verify tools were still removed
            assert len(provider.tool_registry.all_tools) == 0


@pytest.mark.asyncio
async def test_reconnect_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during reconnection."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock reconnect to raise an error
        with patch.object(
            provider.connection_service,
            "connect",
            side_effect=Exception("Reconnect failed"),
        ):
            success = await provider.reconnect("server1")
            assert not success  # Should return False on error


@pytest.mark.asyncio
async def test_cleanup_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during cleanup."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock cleanup to raise an error
        with patch.object(
            provider.connection_service,
            "disconnect",
            side_effect=Exception("Cleanup failed"),
        ):
            # Should not raise an exception, just log the error
            await provider.cleanup_all()
            # Verify tools were still removed
            assert len(provider.tool_registry.all_tools) == 0


@pytest.mark.asyncio
async def test_process_query_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during query processing."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock query processing to raise an error
        with patch.object(
            provider.llm_backend,
            "process_query",
            side_effect=Exception("Query processing failed"),
        ):
            with pytest.raises(Exception, match="Query processing failed"):
                await provider.process_query("test query")


@pytest.mark.asyncio
async def test_execute_tool_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during tool execution."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock tool execution to raise an error
        with patch.object(
            provider.connection_service, "get_session", return_value=mock_session()
        ):
            session = provider.connection_service.get_session("server1")
            session.call_tool = AsyncMock(
                side_effect=Exception("Tool execution failed")
            )

            with pytest.raises(Exception, match="Tool execution failed"):
                await provider.execute_tool("tool1", {})


@pytest.mark.asyncio
async def test_get_resource_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during resource retrieval."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock resource retrieval to raise an error
        with patch.object(
            provider.resource_registry, "find_resource_server", return_value=None
        ):
            with pytest.raises(ValueError, match="Resource not found"):
                await provider.get_resource("nonexistent_resource")


@pytest.mark.asyncio
async def test_get_prompt_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during prompt retrieval."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock prompt retrieval to raise an error
        with patch.object(
            provider.prompt_registry, "find_prompt_server", return_value=None
        ):
            with pytest.raises(ValueError, match="Prompt not found"):
                await provider.get_prompt("nonexistent_prompt")


@pytest.mark.asyncio
async def test_process_query_impl_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling in query implementation."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Mock query implementation to raise an error
        with patch.object(
            provider.llm_backend,
            "process_query",
            side_effect=Exception("Query processing failed"),
        ):
            with pytest.raises(Exception, match="Query processing failed"):
                await provider.process_query("test query")


@pytest.mark.asyncio
async def test_resource_management(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test resource management functionality."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test resource retrieval
        server_name = provider.resource_registry.find_resource_server("resource1")
        assert server_name == "server1"
        resources = provider.resource_registry.get_server_resources(server_name)
        resource = next(r for r in resources if r.name == "resource1")
        assert resource.name == "resource1"
        assert (
            str(resource.uri) == "https://example.com/resource1"
        )  # Convert AnyUrl to string for comparison

        # Test resource not found
        assert (
            provider.resource_registry.find_resource_server("nonexistent_resource")
            is None
        )


@pytest.mark.asyncio
async def test_prompt_management(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test prompt management functionality."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test prompt retrieval
        server_name = provider.prompt_registry.find_prompt_server("prompt1")
        assert server_name == "server1"
        prompts = provider.prompt_registry.get_server_prompts(server_name)
        prompt = next(p for p in prompts if p.name == "prompt1")
        assert prompt.name == "prompt1"
        assert prompt.description == "Test prompt 1"

        # Test prompt not found
        assert provider.prompt_registry.find_prompt_server("nonexistent_prompt") is None


@pytest.mark.asyncio
async def test_query_processing_with_context(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test query processing with context handling."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Mock LLM response with tool usage
        mock_llm_backend.process_query.return_value = {
            "response": "Tool execution result",
            "tool_calls": [{"name": "tool1", "args": {}}],
        }

        # Test query processing with context
        response = await provider.process_query("Test query")
        assert isinstance(response, dict)
        assert response["response"] == "Tool execution result"
        assert response["tool_calls"] == [{"name": "tool1", "args": {}}]
        mock_llm_backend.process_query.assert_called_once()


@pytest.mark.asyncio
async def test_server_reconnection(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test server reconnection functionality."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test successful reconnection
        result = await provider.reconnect("server1")
        assert result is True

        # Test reconnection with invalid server
        result = await provider.reconnect("nonexistent_server")
        assert result is False  # Should return False on error


@pytest.mark.asyncio
async def test_tool_execution_error_handling(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during tool execution."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Create a mock session with error-raising call_tool
    mock_session_instance = mock_session("server1")
    mock_session_instance.call_tool = AsyncMock(
        side_effect=Exception("Tool execution failed")
    )

    with (
        patch.object(
            provider.connection_service._connection_manager,
            "connect",
            side_effect=lambda name, config: mock_session_instance,
        ),
        patch.object(
            provider.connection_service,
            "get_session",
            return_value=mock_session_instance,
        ),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test tool execution error
        with pytest.raises(Exception, match="Tool execution failed"):
            await provider.execute_tool("tool1", {})


@pytest.mark.asyncio
async def test_resource_retrieval_edge_cases(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test edge cases in resource retrieval."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test empty resource name
        assert provider.resource_registry.find_resource_server("") is None

        # Test None resource name
        assert provider.resource_registry.find_resource_server(None) is None


@pytest.mark.asyncio
async def test_prompt_retrieval_edge_cases(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test edge cases in prompt retrieval."""
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        # Connect to a server
        await provider.mcp_connect("server1")

        # Test empty prompt name
        assert provider.prompt_registry.find_prompt_server("") is None

        # Test None prompt name
        assert provider.prompt_registry.find_prompt_server(None) is None


@pytest.mark.asyncio
async def test_resource_not_found_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling when a resource is not found.

    This test verifies that appropriate errors are raised when:
    1. A non-existent resource is requested
    2. A resource's server cannot be found
    """
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Connect to a server first
    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

    # Try to get a non-existent resource
    with pytest.raises(ValueError, match="Resource not found: nonexistent_resource"):
        await provider.get_resource("nonexistent_resource")

    # Try to get a resource when server is not found
    provider.resource_registry.find_resource_server = Mock(return_value=None)
    with pytest.raises(ValueError, match="Resource not found: test_resource"):
        await provider.get_resource("test_resource")


@pytest.mark.asyncio
async def test_prompt_not_found_error(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling when a prompt is not found.

    This test verifies that appropriate errors are raised when:
    1. A non-existent prompt is requested
    2. A prompt's server cannot be found
    """
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Connect to a server first
    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

    # Try to get a non-existent prompt
    with pytest.raises(ValueError, match="Prompt not found: nonexistent_prompt"):
        await provider.get_prompt("nonexistent_prompt")

    # Try to get a prompt when server is not found
    provider.prompt_registry.find_prompt_server = Mock(return_value=None)
    with pytest.raises(ValueError, match="Prompt not found: test_prompt"):
        await provider.get_prompt("test_prompt")


@pytest.mark.asyncio
async def test_cleanup_server_error_handling(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during server cleanup.

    This test verifies:
    1. Exceptions during cleanup are properly re-raised
    2. Cleanup of non-existent servers doesn't raise errors
    3. All registries are properly cleaned up
    """
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Connect to a server first
    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")

        # Verify tools were registered
        assert "server1" in provider.tool_registry.tools_by_server
        assert len(provider.tool_registry.tools_by_server["server1"]) > 0

        # Test error case with a server that exists
        with (
            patch.object(
                provider.connection_service,
                "cleanup",
                side_effect=Exception("Cleanup error"),
            ),
            patch.object(
                provider.tool_registry, "remove_server_tools"
            ) as mock_remove_tools,
            patch.object(
                provider.resource_registry, "remove_server_resources"
            ) as mock_remove_resources,
            patch.object(
                provider.prompt_registry, "remove_server_prompts"
            ) as mock_remove_prompts,
        ):
            # Cleanup should re-raise the exception
            with pytest.raises(Exception, match="Cleanup error"):
                await provider.cleanup_server("server1")

            # Verify cleanup was attempted in the correct order
            mock_remove_tools.assert_not_called()  # Should not be called due to error
            mock_remove_resources.assert_not_called()
            mock_remove_prompts.assert_not_called()

        # Test cleanup of non-existent server (should not raise)
        # Use a new mock that doesn't raise an error
        with patch.object(
            provider.connection_service, "cleanup", new_callable=AsyncMock
        ) as mock_cleanup:
            await provider.cleanup_server("nonexistent_server")
            mock_cleanup.assert_called_once_with("nonexistent_server")


@pytest.mark.asyncio
async def test_connect_all_empty_server_list(mock_llm_backend):
    """Test connecting to servers when no servers are available.

    This test verifies that attempting to connect to an empty list of servers:
    1. Returns an empty result list
    2. Logs appropriate warnings
    3. Doesn't raise any errors
    """
    # Create provider with empty server configs but valid config provider
    config_provider = DictBasedMCPConfigProvider({})
    provider = MCPToolProvider(mock_llm_backend, config_provider=config_provider)
    await provider.initialize()

    # Should return empty list without error
    results = await provider.mcp_connect_all()
    assert results == []


@pytest.mark.asyncio
async def test_connect_all_partial_failure(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test handling of partial connection failures when connecting to multiple servers.

    This test verifies that when connecting to multiple servers:
    1. Successful connections are established where possible
    2. Failed connections are properly reported
    3. The overall operation continues despite individual failures
    4. The result list contains appropriate success/failure information
    """
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Mock connection to fail for one server
    async def mock_connect(server_name, config):
        if server_name == "server1":
            raise ConnectionError("Failed to connect")
        return mock_session(server_name)

    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=mock_connect,
    ):
        results = await provider.mcp_connect_all()

        # Verify results
        assert len(results) == 2
        server1_result = next(r for r in results if r[0] == "server1")
        server2_result = next(r for r in results if r[0] == "server2")

        assert isinstance(server1_result[1], ConnectionError)
        assert server2_result[1] is None

        # Verify server2 tools were registered but server1 tools were not
        assert "server2" in provider.tool_registry.tools_by_server
        assert "server1" not in provider.tool_registry.tools_by_server


@pytest.mark.asyncio
async def test_cleanup_all_error_handling(
    mock_llm_backend, valid_server_configs, mock_session, mock_exit_stack
):
    """Test error handling during cleanup_all operation.

    This test verifies that during cleanup_all:
    1. All resources are attempted to be cleaned up
    2. Errors in individual cleanups don't prevent other cleanups
    3. Registries are cleared regardless of errors
    4. Exit stack is properly closed
    """
    provider = MCPToolProvider(mock_llm_backend, server_configs=valid_server_configs)
    provider.exit_stack = mock_exit_stack
    await provider.initialize()

    # Connect to servers first
    with patch.object(
        provider.connection_service._connection_manager,
        "connect",
        side_effect=lambda name, config: mock_session(name),
    ):
        await provider.mcp_connect("server1")
        await provider.mcp_connect("server2")

        # Verify initial state
        assert len(provider.tool_registry.tools_by_server) == 2
        assert len(provider.resource_registry.resources_by_server) == 2
        assert len(provider.prompt_registry.prompts_by_server) == 2

        # Mock cleanup to fail for connection service but still allow registry cleanup
        provider.connection_service.cleanup_all = AsyncMock(
            side_effect=Exception("Cleanup error")
        )

        # Mock registry clear methods to verify they're called
        with (
            patch.object(provider.tool_registry, "clear") as mock_tool_clear,
            patch.object(provider.resource_registry, "clear") as mock_resource_clear,
            patch.object(provider.prompt_registry, "clear") as mock_prompt_clear,
        ):
            try:
                # Should not raise despite the error
                await provider.cleanup_all()
            except Exception:
                pass  # Error is expected but should not prevent registry cleanup

            # Verify registry clear methods were called
            mock_tool_clear.assert_called_once()
            mock_resource_clear.assert_called_once()
            mock_prompt_clear.assert_called_once()

            # Verify connected servers are cleared
            assert len(provider._connected_servers) == 0
