"""Unit tests for OpenAI backend implementation."""

import json
import os
from unittest.mock import AsyncMock, Mock, patch

import pytest
from mcp.types import Tool as MCPTool
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from agentical.llm.openai.openai_chat import OpenAIBackend


@pytest.fixture
def mock_openai_client():
    """Fixture providing a mock OpenAI client."""
    with patch("agentical.llm.openai.openai_chat.openai.AsyncOpenAI") as mock:
        yield mock


@pytest.fixture
def mock_env_vars():
    """Fixture to set and cleanup environment variables."""
    original_env = dict(os.environ)
    os.environ["OPENAI_API_KEY"] = "test_key"
    os.environ["OPENAI_MODEL"] = "test_model"
    yield
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_mcp_tools():
    """Fixture providing mock MCP tools."""
    return [
        MCPTool(
            name="tool1",
            description="Test tool 1",
            parameters={"type": "object", "properties": {"param1": {"type": "string"}}},
            inputSchema={
                "type": "object",
                "properties": {"param1": {"type": "string"}},
            },
        ),
        MCPTool(
            name="tool2",
            description="Test tool 2",
            parameters={
                "type": "object",
                "properties": {"param2": {"type": "integer"}},
            },
            inputSchema={
                "type": "object",
                "properties": {"param2": {"type": "integer"}},
            },
        ),
    ]


def test_init_with_api_key():
    """Test initialization with explicit API key."""
    backend = OpenAIBackend(api_key="test_key")
    assert backend.model == OpenAIBackend.DEFAULT_MODEL


def test_init_with_env_vars(mock_env_vars):
    """Test initialization with environment variables."""
    backend = OpenAIBackend()
    assert backend.model == "test_model"


def test_init_without_api_key():
    """Test initialization fails without API key."""
    # Clear any existing API key in environment
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    with pytest.raises(ValueError, match="OPENAI_API_KEY not found"):
        OpenAIBackend()


def test_convert_tools(mock_env_vars, mock_mcp_tools):
    """Test tool formatting for OpenAI."""
    backend = OpenAIBackend()
    formatted = backend.convert_tools(mock_mcp_tools)

    assert len(formatted) == 2
    assert formatted[0]["type"] == "function"
    assert formatted[0]["function"]["name"] == "tool1"
    assert formatted[0]["function"]["description"] == "Test tool 1"
    assert (
        formatted[0]["function"]["parameters"]["properties"]["param1"]["type"]
        == "string"
    )

    assert formatted[1]["type"] == "function"
    assert formatted[1]["function"]["name"] == "tool2"
    assert (
        formatted[1]["function"]["parameters"]["properties"]["param2"]["type"]
        == "integer"
    )


def test_convert_tools_handles_missing_parameters(mock_env_vars):
    """Test tool formatting handles tools without parameters."""
    tools = [MCPTool(name="test", description="test", parameters={}, inputSchema={})]
    backend = OpenAIBackend()
    formatted = backend.convert_tools(tools)

    assert len(formatted) == 1
    assert formatted[0]["function"]["parameters"] == {}


@pytest.mark.asyncio
async def test_process_query_without_tool_calls(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test processing a query that doesn't require tool calls."""
    # Setup mock response
    mock_message = ChatCompletionMessage(
        content="Test response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion = ChatCompletion(
        id="test",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_openai_client.return_value = mock_client

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=AsyncMock(),
        context=None,
    )

    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_process_query_with_tool_calls(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test processing a query that requires tool calls."""
    # Setup mock responses
    tool_call = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": json.dumps({"param1": "test"})},
    }

    # First response with tool call
    mock_message1 = ChatCompletionMessage(
        content=None, role="assistant", tool_calls=[tool_call], function_call=None
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Mock tool execution
    mock_execute_tool = AsyncMock(return_value="Tool result")

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=mock_execute_tool,
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2
    mock_execute_tool.assert_called_once_with("tool1", {"param1": "test"})


@pytest.mark.asyncio
async def test_process_query_with_context(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test processing a query with conversation context."""
    # Setup mock response
    mock_message = ChatCompletionMessage(
        content="Test response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion = ChatCompletion(
        id="test",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_openai_client.return_value = mock_client

    # Execute test with context
    backend = OpenAIBackend()
    context = [{"role": "user", "content": "previous message"}]
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=AsyncMock(),
        context=context,
    )

    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_process_query_handles_tool_error(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test handling of tool execution errors."""
    # Setup mock responses
    tool_call = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": json.dumps({"param1": "test"})},
    }

    # First response with tool call
    mock_message1 = ChatCompletionMessage(
        content=None, role="assistant", tool_calls=[tool_call], function_call=None
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Mock tool execution to raise an error
    mock_execute_tool = AsyncMock(side_effect=Exception("Tool error"))

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=mock_execute_tool,
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2
    mock_execute_tool.assert_called_once_with("tool1", {"param1": "test"})


@pytest.mark.asyncio
async def test_process_query_handles_invalid_tool_args(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test handling of invalid tool arguments."""
    # Setup mock responses
    tool_call = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": "invalid json"},
    }

    # First response with tool call
    mock_message1 = ChatCompletionMessage(
        content=None, role="assistant", tool_calls=[tool_call], function_call=None
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=AsyncMock(),
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2


def test_init_with_custom_model(mock_env_vars):
    """Test initialization with custom model from environment."""
    os.environ["OPENAI_MODEL"] = "custom-model"
    backend = OpenAIBackend()
    assert backend.model == "custom-model"


def test_init_with_invalid_api_key():
    """Test initialization with invalid API key."""
    with patch(
        "agentical.llm.openai.openai_chat.openai.AsyncOpenAI",
        side_effect=Exception("Invalid API key"),
    ):
        with pytest.raises(
            ValueError, match="Failed to initialize OpenAI client: Invalid API key"
        ):
            OpenAIBackend(api_key="invalid_key")


@pytest.mark.asyncio
async def test_process_query_with_multiple_tool_calls(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test processing a query that requires multiple tool calls."""
    # Setup mock responses
    tool_call1 = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": json.dumps({"param1": "test1"})},
    }
    tool_call2 = {
        "id": "call2",
        "type": "function",
        "function": {"name": "tool2", "arguments": json.dumps({"param2": 42})},
    }

    # First response with tool calls
    mock_message1 = ChatCompletionMessage(
        content=None,
        role="assistant",
        tool_calls=[tool_call1, tool_call2],
        function_call=None,
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Mock tool execution
    mock_execute_tool = AsyncMock(return_value="Tool result")

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=mock_execute_tool,
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2
    assert mock_execute_tool.call_count == 2
    mock_execute_tool.assert_any_call("tool1", {"param1": "test1"})
    mock_execute_tool.assert_any_call("tool2", {"param2": 42})


@pytest.mark.asyncio
async def test_process_query_with_invalid_json_tool_args(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test handling of invalid JSON in tool arguments."""
    # Setup mock responses
    tool_call = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": "invalid json"},
    }

    # First response with tool call
    mock_message1 = ChatCompletionMessage(
        content=None, role="assistant", tool_calls=[tool_call], function_call=None
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=AsyncMock(),
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2


@pytest.mark.asyncio
async def test_process_query_with_conversation_context(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test processing a query with conversation context."""
    # Setup mock response
    mock_message = ChatCompletionMessage(
        content="Test response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion = ChatCompletion(
        id="test",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    mock_openai_client.return_value = mock_client

    # Execute test with context
    backend = OpenAIBackend()
    context = [{"role": "user", "content": "previous message"}]
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=AsyncMock(),
        context=context,
    )

    assert response == "Test response"
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
async def test_process_query_with_tool_execution_error(
    mock_env_vars, mock_openai_client, mock_mcp_tools
):
    """Test handling of tool execution errors."""
    # Setup mock responses
    tool_call = {
        "id": "call1",
        "type": "function",
        "function": {"name": "tool1", "arguments": json.dumps({"param1": "test"})},
    }

    # First response with tool call
    mock_message1 = ChatCompletionMessage(
        content=None, role="assistant", tool_calls=[tool_call], function_call=None
    )
    mock_completion1 = ChatCompletion(
        id="test1",
        choices=[{"finish_reason": "tool_calls", "index": 0, "message": mock_message1}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Second response with final answer
    mock_message2 = ChatCompletionMessage(
        content="Final response", role="assistant", tool_calls=None, function_call=None
    )
    mock_completion2 = ChatCompletion(
        id="test2",
        choices=[{"finish_reason": "stop", "index": 0, "message": mock_message2}],
        created=123,
        model="test",
        object="chat.completion",
    )

    # Configure mock client
    mock_client = Mock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=[mock_completion1, mock_completion2]
    )
    mock_openai_client.return_value = mock_client

    # Mock tool execution to raise an error
    mock_execute_tool = AsyncMock(side_effect=Exception("Tool error"))

    # Execute test
    backend = OpenAIBackend()
    response = await backend.process_query(
        query="test query",
        tools=mock_mcp_tools,
        resources=[],
        prompts=[],
        execute_tool=mock_execute_tool,
    )

    assert response == "Final response"
    assert mock_client.chat.completions.create.call_count == 2
    mock_execute_tool.assert_called_once_with("tool1", {"param1": "test"})
