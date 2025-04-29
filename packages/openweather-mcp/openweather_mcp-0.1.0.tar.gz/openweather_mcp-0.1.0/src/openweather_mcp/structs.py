from __future__ import annotations

from datetime import datetime
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, Field


class Coordinate(NamedTuple):
    lat: float
    lon: float


class APIModel(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)


class WeatherCondition(APIModel):
    main: str = Field(
        ..., description="Group of weather parameters (Rain, Snow, Clouds etc.)"
    )
    description: str = Field(..., description="Weather condition within the group")


class WeatherMain(APIModel):
    temp: float = Field(
        ...,
        description="Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit",
    )
    feels_like: float = Field(
        ...,
        description="Temperature. This temperature parameter accounts for the human perception of weather",
    )
    temp_min: float = Field(
        ...,
        description="Minimum temperature at the moment. This is minimal currently observed temperature (within large megalopolises and urban areas) in Kelvin units",
    )
    temp_max: float = Field(
        ...,
        description="Maximum temperature at the moment. This is maximal currently observed temperature (within large megalopolises and urban areas) in Kelvin units",
    )
    pressure: int = Field(
        ...,
        description="Atmospheric pressure (on the sea level, if there is no sea level or ground level data), hPa",
    )
    humidity: int = Field(..., description="Humidity, %")


class WeatherWind(APIModel):
    speed: float = Field(
        ...,
        description="Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour",
    )
    deg: int = Field(..., description="Wind direction, degrees (meteorological)")
    gust: float = Field(
        ..., description="Wind gust. Unit Default: meter/sec, Metric: meter/sec"
    )


class WeatherResponse(APIModel):
    weather: list[WeatherCondition] = Field(
        ..., description="Weather condition information"
    )
    main: WeatherMain = Field(..., description="Main weather information")
    visibility: int = Field(
        ...,
        description="Visibility, meter. The maximum value of the visibility is 10 km",
    )
    wind: WeatherWind = Field(..., description="Wind information")
    dt: datetime = Field(..., description="Time of data calculation, unix, UTC")


class ForecastResponse(APIModel):
    list_: list[WeatherResponse] = Field(
        ..., description="List of weather forecasts for the next 5 days", alias="list"
    )
