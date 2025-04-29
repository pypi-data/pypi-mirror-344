class MCPError(Exception):
    """Base class for all exceptions raised by the openweather_mcp package."""

    pass


class OpenWeatherError(MCPError):
    """Base class for all exceptions raised by the OpenWeather API."""
