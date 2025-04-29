"""Tests for the MCP (Model Context Protocol) server implementation."""

from pathlib import Path

import pytest
from dirty_equals import IsInstance
from inline_snapshot import snapshot

from pydantic_ai.agent import Agent
from pydantic_ai.exceptions import UserError
from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, ToolCallPart, ToolReturnPart, UserPromptPart

from .conftest import IsDatetime, try_import

with try_import() as imports_successful:
    from mcp.types import CallToolResult, TextContent

    from pydantic_ai.mcp import MCPServerHTTP, MCPServerStdio
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider


pytestmark = [
    pytest.mark.skipif(not imports_successful(), reason='mcp and openai not installed'),
    pytest.mark.anyio,
    pytest.mark.vcr,
]


async def test_stdio_server():
    server = MCPServerStdio('python', ['-m', 'tests.mcp_server'])
    async with server:
        tools = await server.list_tools()
        assert len(tools) == 2
        assert tools[0].name == 'celsius_to_fahrenheit'
        assert tools[0].description.startswith('Convert Celsius to Fahrenheit.')

        # Test calling the temperature conversion tool
        result = await server.call_tool('celsius_to_fahrenheit', {'celsius': 0})
        assert result.content == snapshot([TextContent(type='text', text='32.0')])


async def test_stdio_server_with_cwd():
    test_dir = Path(__file__).parent
    server = MCPServerStdio('python', ['mcp_server.py'], cwd=test_dir)
    async with server:
        tools = await server.list_tools()
        assert len(tools) == 2


def test_sse_server():
    sse_server = MCPServerHTTP(url='http://localhost:8000/sse')
    assert sse_server.url == 'http://localhost:8000/sse'
    assert sse_server._get_log_level() is None  # pyright: ignore[reportPrivateUsage]


def test_sse_server_with_header_and_timeout():
    sse_server = MCPServerHTTP(
        url='http://localhost:8000/sse',
        headers={'my-custom-header': 'my-header-value'},
        timeout=10,
        sse_read_timeout=100,
        log_level='info',
    )
    assert sse_server.url == 'http://localhost:8000/sse'
    assert sse_server.headers is not None and sse_server.headers['my-custom-header'] == 'my-header-value'
    assert sse_server.timeout == 10
    assert sse_server.sse_read_timeout == 100
    assert sse_server._get_log_level() == 'info'  # pyright: ignore[reportPrivateUsage]


async def test_agent_with_stdio_server(allow_model_requests: None, openai_api_key: str):
    server = MCPServerStdio('python', ['-m', 'tests.mcp_server'])
    model = OpenAIModel('gpt-4o', provider=OpenAIProvider(api_key=openai_api_key))
    agent = Agent(model, mcp_servers=[server])
    async with agent.run_mcp_servers():
        result = await agent.run('What is 0 degrees Celsius in Fahrenheit?')
        assert result.output == snapshot('0 degrees Celsius is 32.0 degrees Fahrenheit.')
        assert result.all_messages() == snapshot(
            [
                ModelRequest(
                    parts=[UserPromptPart(content='What is 0 degrees Celsius in Fahrenheit?', timestamp=IsDatetime())]
                ),
                ModelResponse(
                    parts=[
                        ToolCallPart(
                            tool_name='celsius_to_fahrenheit',
                            args='{"celsius":0}',
                            tool_call_id='call_UNesABTXfwIkYdh3HzXWw2wD',
                        )
                    ],
                    model_name='gpt-4o-2024-08-06',
                    timestamp=IsDatetime(),
                ),
                ModelRequest(
                    parts=[
                        ToolReturnPart(
                            tool_name='celsius_to_fahrenheit',
                            content=IsInstance(CallToolResult),
                            tool_call_id='call_UNesABTXfwIkYdh3HzXWw2wD',
                            timestamp=IsDatetime(),
                        )
                    ]
                ),
                ModelResponse(
                    parts=[TextPart(content='0 degrees Celsius is 32.0 degrees Fahrenheit.')],
                    model_name='gpt-4o-2024-08-06',
                    timestamp=IsDatetime(),
                ),
            ]
        )


async def test_agent_with_server_not_running(openai_api_key: str):
    server = MCPServerStdio('python', ['-m', 'tests.mcp_server'])
    model = OpenAIModel('gpt-4o', provider=OpenAIProvider(api_key=openai_api_key))
    agent = Agent(model, mcp_servers=[server])
    with pytest.raises(UserError, match='MCP server is not running'):
        await agent.run('What is 0 degrees Celsius in Fahrenheit?')


async def test_log_level_unset():
    server = MCPServerStdio('python', ['-m', 'tests.mcp_server'])
    assert server._get_log_level() is None  # pyright: ignore[reportPrivateUsage]
    async with server:
        tools = await server.list_tools()
        assert len(tools) == 2
        assert tools[1].name == 'get_log_level'

        result = await server.call_tool('get_log_level', {})
        assert result.content == snapshot([TextContent(type='text', text='unset')])


async def test_log_level_set():
    server = MCPServerStdio('python', ['-m', 'tests.mcp_server'], log_level='info')
    assert server._get_log_level() == 'info'  # pyright: ignore[reportPrivateUsage]
    async with server:
        result = await server.call_tool('get_log_level', {})
        assert result.content == snapshot([TextContent(type='text', text='info')])
