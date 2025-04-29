import json
import os

import pytest
from mcp import ClientSession, StdioServerParameters, stdio_client

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="openweather-mcp",
    env={"OPENWEATHER_API_KEY": os.getenv("OPENWEATHER_API_KEY")},
)


@pytest.mark.asyncio
async def test_list_tools():
    """Test listing tools."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert isinstance(tools.tools, list)
            assert len(tools.tools) > 0
            assert [tool.name for tool in tools.tools] == [
                "get_current_weather",
                "get_weather_forecast",
            ]


@pytest.mark.asyncio
async def test_current_weather():
    """Test current weather tool."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_current_weather", arguments={"city": "London"}
            )
            resp = json.loads(result.content[0].text)
            assert resp["main"]["temp"] is not None


@pytest.mark.asyncio
async def test_weather_forecast():
    """Test weather forecast tool."""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_weather_forecast", arguments={"city": "London"}
            )
            print(result)
            resp = json.loads(result.content[0].text)
            assert len(resp["list"]) > 0
