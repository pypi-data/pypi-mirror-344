import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from httpx import AsyncClient
from mcp.server import Server
from mcp.server.fastmcp import Context, FastMCP

from .errors import OpenWeatherError
from .structs import Coordinate, ForecastResponse, WeatherResponse


@asynccontextmanager
async def lifespan(server: Server[AsyncClient]) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://api.openweathermap.org") as client:
        yield client


server = FastMCP("openweather_mcp", lifespan=lifespan)
API_KEY = os.getenv("OPENWEATHER_API_KEY")


async def get_location(ctx: Context, query: str) -> Coordinate:
    client = ctx.request_context.lifespan_context

    resp = await client.get(
        "/geo/1.0/direct", params={"q": query, "limit": 1, "appid": API_KEY}
    )
    if not resp.is_success:
        raise OpenWeatherError(
            f"Failed to call OpenWeather API: {resp.status_code} {resp.text}"
        )
    data = resp.json()
    if not data:
        raise OpenWeatherError(f"Can't find location for {query}, it may be invalid.")
    return Coordinate(lat=data[0]["lat"], lon=data[0]["lon"])


# Add your mcp tools and resources here
@server.tool()
async def get_current_weather(
    city: str | None = None, coordinate: Coordinate | None = None, *, ctx: Context
) -> WeatherResponse:
    """Get current weather for a given city or location.

    Args:
        city (str): The name of the city to get the weather for, can be omitted if coordinate is provided.
        coordinate (Coordinate): The coordinates of the location to get the weather for, can be omitted if city is provided.
    """
    client = ctx.request_context.lifespan_context

    if coordinate is None:
        if city is None:
            raise OpenWeatherError("Either city or coordinate must be provided.")
        coordinate = await get_location(ctx, city)
    resp = await client.get(
        "/data/2.5/weather",
        params={
            "lat": coordinate.lat,
            "lon": coordinate.lon,
            "appid": API_KEY,
            "units": "metric",
        },
    )
    if not resp.is_success:
        raise OpenWeatherError(
            f"Failed to call OpenWeather API: {resp.status_code} {resp.text}"
        )
    return WeatherResponse.model_validate(resp.json())


@server.tool()
async def get_weather_forecast(
    city: str | None = None, coordinate: Coordinate | None = None, *, ctx: Context
) -> ForecastResponse:
    """Get weather forecast for a given city for the next 5 days.

    Args:
        city (str): The name of the city to get the weather for, can be omitted if coordinate is provided.
        coordinate (Coordinate): The coordinates of the location to get the weather for, can be omitted if city is provided.
    """
    client = ctx.request_context.lifespan_context

    if coordinate is None:
        if city is None:
            raise OpenWeatherError("Either city or coordinate must be provided.")
        coordinate = await get_location(ctx, city)
    resp = await client.get(
        "/data/2.5/forecast",
        params={"lat": coordinate.lat, "lon": coordinate.lon, "appid": API_KEY},
    )
    if not resp.is_success:
        raise OpenWeatherError(
            f"Failed to call OpenWeather API: {resp.status_code} {resp.text}"
        )
    return ForecastResponse.model_validate(resp.json())


def main():
    server.run("stdio")
