# this file has all OpenWeatherMap API integrations in it.
import logging
from datetime import datetime

import requests


def get_current_weather(api_key, location, language, logger):
    """
    Fetches the current weather for a given location using the Open CurrentWeather Map API.

    :param api_key: Open CurrentWeather Map API key.
    :param location: The location for which to fetch the weather. String or dict with 'latitude' and 'longitude'.
    :param language: The language for the weather description.
    :param logger:
    :return: A dictionary containing the current weather data.
    """

    ld = location

    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lang={language}&lat={ld['coords'][0]}&lon={ld['coords'][1]}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:  # yippee! it works :3
        weather_data = response.json()

        return {
            "error": "",
            "data": {
                "location": {
                    "latitude": ld['coords'][0],
                    "longitude": ld['coords'][1],
                    "name": ld['data'][0]['name'],
                    "country_code": ld['data'][0]['country'].upper()
                },
                "day": datetime.now().strftime("%A"),
                "time": datetime.now().strftime("%I:%M"),
                "format": 'metric',
                "weather": {
                    "description": weather_data['weather'][0]['description'],
                    "temperature": weather_data['main']['temp'],
                    "humidity": weather_data['main']['humidity'],
                    "wind_speed": weather_data['wind']['speed'],
                    "pressure": weather_data['main']['pressure'],
                    "sunrise": weather_data['sys']['sunrise'],
                    "sunset": weather_data['sys']['sunset'],
                    "icon_url": f"https://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png",
                    "icon": weather_data['weather'][0]['icon']
                }
            }
        }

    else:
        logging.error(f"Error fetching weather data. Status: {response.status_code} --- Response: {response.text}")
        return {
            "error": f"Error fetching weather data. Status: {response.status_code} --- Response: {response.text}",
            "data": {}
        }


def get_weather_forecast(api_key, location, language, logger):
    """
    Fetches the weather forecast for a given location using the OpenWeatherMap API.

    :param api_key: OpenWeatherMap API key.
    :param location: The location for which to fetch the weather forecast. String or dict with 'latitude' and 'longitude'.
    :param language: The language for the weather description.
    :param logger:
    :return: A dictionary containing the weather forecast data.
    """

    ld = location

    url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&lang={language}&lat={ld['coords'][0]}&lon={ld['coords'][1]}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return {"error": "", "data": response.json()}
    else:
        logger.error(f"Error fetching weather forecast data. Status: {response.status_code} --- Response: {response.text}")
        return {"error": f"Error fetching weather forecast data. Status: {response.status_code} --- Response: {response.text}",
                "data": {}
        }


# def get_weather_forecast_simple(api_key, location, language, logger):
#     """
#     Fetches the weather forecast for a given location using the OpenWeatherMap API.
#
#     :param api_key: OpenWeatherMap API key.
#     :param location: The location for which to fetch the weather forecast. String or dict with 'latitude' and 'longitude'.
#     :param language: The language for the weather description.
#     :param logger:
#     :return: A dictionary containing the weather forecast data.
#     """
#
#     try:
#         ld = location
#
#         url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&lang={language}&lat={ld['coords'][0]}&lon={ld['coords'][1]}&appid={api_key}"
#
#         response = requests.get(url)
#         if response.status_code == 200:
#
#             # Take response and format it to show the average from 0600 to 2100
#             data = response.json()
#
#             forecast_data = data["list"]
#
#
#
#             outlook = {}
#             ol = []
#
#             for i in range(3):
#
#                 # Determine the cutoff time for each day
#                 now = datetime.now(timezone.utc)
#                 day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
#                 day_end = day_start + timedelta(days=i+1)
#
#                 relevant_data = []
#                 for forecast in forecast_data:
#                     forecast_time = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc)
#                     if day_start <= forecast_time < day_end:
#                         relevant_data.append(forecast)
#
#                 if not relevant_data:
#                     print("No relevant forecast data found for today.")
#                     return {"error": "No relevant forecast data found for today.", "data": {}}
#
#                 # Calculate averages here for each day
#                 avg_temp =     int(sum(d['main']['temp']     for d in relevant_data) / len(relevant_data))
#                 avg_humidity = int(sum(d['main']['humidity'] for d in relevant_data) / len(relevant_data))
#                 avg_wind =     str(sum(d['wind']['speed']    for d in relevant_data) / len(relevant_data))[:4]
#
#                 ol.append({f"muh":{
#                     "avg_temperature": avg_temp,
#                     "avg_humidity": avg_humidity,
#                     "avg_wind": avg_wind
#                 }})
#
#             # compile ol into outlook
#             for thing in ol:
#                 print(thing)
#                 # outlook[thing] = thing
#
#             return {"error": "", "data": outlook}
#
#         else:
#             logger.error(
#                 f"Error fetching simple weather forecast data. Status: {response.status_code} --- Response: {response.text}")
#             return {
#                 "error": f"Error fetching simple weather forecast data. Status: {response.status_code} --- Response: {response.text}",
#                 "data": {}
#             }
#
#     except requests.exceptions.RequestException as e:
#         print(f"Request Error: {e}")
#         return {"error": e, "data": {}}
#     except (KeyError, TypeError) as e:
#         print(f"Data Parsing Error: {e}")
#         return {"error": e, "data": {}}


def get_current_air_quality(api_key, location, logger):
    """
    Fetches the current air quality for a given location using the OpenWeatherMap Air Quality API.

    :param api_key: OpenWeatherMap API key.
    :param location: The location for which to fetch the air quality. String or dict with 'latitude' and 'longitude'.
    :param logger:
    :return: A dictionary containing the current air quality data.
    """

    ld = location

    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={ld['coords'][0]}&lon={ld['coords'][1]}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:

        # figure out the healthiness of the air
        # rating, aqi = rate_air_quality(response.json(), logger)

        return {
            "error": "",
            "data": {
                # "aqi_rating": rating,
                "aqi": response.json()['list'][0]['main']['aqi'],
                "location": location,
                "raw_data": response.json()
            }
        }

    else:
        logger.error(f"Error retrieving air quality. Error: {response.status_code} - {response.text}.")
        return {
            "error": f"{response.status_code} - {response.text}",
            "data": {}

        }


# def rate_air_quality(air_response, logger):
#     """Returns a worded rating based on the aqi value (e.g(s): Great!, Good, Moderate, Unhealthy, Hazardous"""
#
#     aqi_no = air_response['list'][0]['main']['aqi']
#
#     # Calculate the average aqi value
#     if not aqi_no:
#         logger.warning("No air quality data available.")
#         return {"error": "No air quality data available.", "rating": "error"}, 500
#
#     # Determine the air quality rating based on the average aqi value
#     if 0 < aqi_no <= 1:  # if aqi is between 0 and 1
#         caq_rating = "Great!"
#     elif 1 < aqi_no <= 2:  # if aqi is between 1 and 2
#         caq_rating = "Good"
#     elif 2 < aqi_no <= 3:  # if aqi is between 2 and 3
#         caq_rating = "Moderate"
#     elif 3 < aqi_no <= 4:  # if aqi is between 3 and 4
#         caq_rating = "Unhealthy"
#     elif 4 < aqi_no <= 5:  # if aqi is between 4 and 5
#         caq_rating = "Hazardous"
#     else:  # if aqi is greater than 5
#         logger.error(f"Air quality index is too high (over 5). This is likely an API error. AQI: {aqi_no}.")
#         return {
#             "error": f"Air quality index is too high (over 5). This is likely an API error. AQI: {aqi_no}.",
#             "rating": "error"
#         }
#
#     return {"error": "", "rating": caq_rating}
