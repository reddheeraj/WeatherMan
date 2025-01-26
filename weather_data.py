import python_weather
import asyncio
import os

async def get_weather(location: str):
    """
    Fetch the weather data for the given location.
    :param location: The name of the city or country for which the weather is requested.
    :return: A dictionary containing weather attributes and daily forecasts.
    """
    weather_data = {
        "current": {},  # Store general weather data
        "daily": []     # Store daily forecasts
    }
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        try:
            # Fetch the weather forecast for the given location
            weather = await client.get(location)
            print(f"Fetched weather data for {location}: {weather}")

            # Extract general weather data from the main weather object
            weather_data["current"] = {
                "date": weather.datetime.strftime('%Y-%m-%d %H:%M'),
                "temperature": f"{weather.temperature}°F" if weather.temperature is not None else "N/A",
                "humidity": f"{weather.humidity}%" if weather.humidity is not None else "N/A",
                "precipitation": f"{weather.precipitation} in" if weather.precipitation is not None else "N/A",
                "wind_speed": f"{weather.wind_speed} mph" if weather.wind_speed is not None else "N/A",
                "wind_direction": weather.wind_direction.name if weather.wind_direction is not None else "N/A",
            }

            # Extract daily forecasts from daily_forecasts
            for daily in weather.daily_forecasts:
                weather_data["daily"].append({
                    "date": daily.date.strftime('%Y-%m-%d'),
                    "temperature": f"{daily.temperature}°F" if daily.temperature is not None else "N/A",
                })

        except Exception as e:
            print(f"Error fetching weather data for {location}: {e}")

    return weather_data


def fetch_weather(location: str):
    """
    Run the asynchronous weather fetching function and return results.
    :param location: The name of the city or country for which the weather is requested.
    """
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.run(get_weather(location))
