# import python_weather
# import asyncio
# import os

# async def getweather() -> None:
#   # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
#   async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
#     # fetch a weather forecast from a city
#     weather = await client.get('College Station')
#     print("weather = ", weather)
#     # returns the current day's forecast temperature (int)
#     print("Today's temperature => ", weather.temperature)
    
#     # get the weather forecast for a few days
#     for daily in weather:
#       print(daily)
      
#       # hourly forecasts
#       for hourly in daily:
#         print(f' --> {hourly!r}')

# if __name__ == '__main__':
#   # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
#   # for more details
#   if os.name == 'nt':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
#   asyncio.run(getweather())

# trial 2 
# import python_weather
# import asyncio
# import os


# async def get_weather():
#     """
#     Fetch the weather data for the given location.
#     Returns a list of daily weather data with available attributes.
#     """
#     weather_data = []
#     async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
#         # Fetch a weather forecast for College Station
#         weather = await client.get('College Station')

#         # Extract daily forecasts (directly iterate over the Forecast object)
#         for daily in weather:
#             weather_data.append({
#                 "date": daily.date.strftime('%Y-%m-%d'),  # Format date to a readable string
#                 "temperature": f"{daily.temperature}°F" if daily.temperature is not None else "N/A",  # Include temperature
#             })

#     return weather_data


# def fetch_weather():
#     """
#     Run the asynchronous weather fetching function and return results.
#     """
#     if os.name == 'nt':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     return asyncio.run(get_weather())

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
