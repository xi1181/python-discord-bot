import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import time

def get_weather():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 1.2897,
        "longitude": 103.8501,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code"],
        "timezone": "Asia/Singapore"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_weather_code = current.Variables(3).Value()

    current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(current.Time()))

    weather_interpretation_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light intensity",
        53: "Drizzle: Moderate intensity",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light intensity",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight intensity",
        63: "Rain: Moderate intensity",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light intensity",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight intensity",
        73: "Snow fall: Moderate intensity",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight intensity",
        81: "Rain showers: Moderate intensity",
        82: "Rain showers: Violent intensity",
        85: "Snow showers: Slight intensity",
        86: "Snow showers: Heavy intensity",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }



    output_string = (f"Coordinates {response.Latitude()}°N {response.Longitude()}°E\n"
                f"Elevation {response.Elevation()} m asl\n"
                f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}\n"
                f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s\n"
                f"Current time {current_time}\n"
                f"Current temperature_2m {current_temperature_2m}\n"
                f"Current relative_humidity_2m {current_relative_humidity_2m}\n"
                f"Current apparent_temperature {current_apparent_temperature}\n"
                f"Current weather: {weather_interpretation_codes[int(current_weather_code)]}\n")

    return(output_string)

