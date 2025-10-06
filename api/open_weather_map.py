# this file has all google api integrations in it.
import logging
from datetime import datetime
from io import BytesIO

import requests
from PIL import Image

from api.geocoding import geocodeLocation


def get_current_weather(api_key, location, language, logger):
    """
    Fetches the current weather for a given location using the Open CurrentWeather Map API.

    :param api_key: Open CurrentWeather Map API key.
    :param location: The location for which to fetch the weather. String or dict with 'latitude' and 'longitude'.
    :param language: The language for the weather description.
    :param logger:
    :return: A dictionary containing the current weather data.
    """

    lat, lon, location_data = geocodeLocation(api_key, location, logger)

    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lang={language}&lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:  # yippee! it works :3
        # # Add a "native_name" field to the response; this is the name of the location in the local language
        # native_name = None # default to None
        # country_code = response.json()['sys']['country']
        # country_code = country_code.lower()  # convert to lowercase

        # try:
        #     native_name = location_data[0]['local_names'][country_code]        
        # except (IndexError, KeyError):
        #     # If the native name is not found, set it to the English name
        #     native_name = location_data[0]['name'] if 'name' in location_data[0] else None

        weather_data = response.json()

        return {
            "location": {
                "latitude": lat,
                "longitude": lon,
                "name": location_data[0]['name'],
                # "native_name": native_name,  # add the native name
                "country_code": location_data[0]['country'].upper()
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
    else:
        logging.error(f"Error fetching weather data. Status: {response.status_code} --- Response: {response.text}")
        return {
            "error": f"Error fetching weather data. Status: {response.status_code} --- Response: {response.text}"
        }


def get_weather_forecast(api_key, location, language, logger):
    """
    Fetches the weather forecast for a given location using the Google CurrentWeather API.

    :param api_key: OpenWeatherMap API key.
    :param location: The location for which to fetch the weather forecast. String or dict with 'latitude' and 'longitude'.
    :param language: The language for the weather description.
    :param logger:
    :return: A dictionary containing the weather forecast data.
    """

    lat, lon, location_data = geocodeLocation(api_key, location, logger)

    url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&lang={language}&lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        # Add a "native_name" field to the response; this is the name of the location in the local language
        # native_name = None  # default to None
        # country_code = location_data[0]['country']
        # country_code = country_code.lower()  # convert to lowercase
        # try:
        #     native_name = location_data['results'][0]['local_names'][country_code]
        # except (IndexError, KeyError):
        #     # If the native name is not found, set it to the English name
        #     native_name = location_data['results'][0]['formatted_address'] if 'formatted_address' in location_data['results'][0] else None
        # response_data = response.json()
        # response_data['location']['native_name'] = native_name  # add the native name to the response

        return response.json()
    else:
        raise Exception(
            f"Error fetching weather forecast data. Status: {response.status_code} --- Response: {response.text}")


def get_current_air_quality(api_key, location, logger):
    """
    Fetches the current air quality for a given location using the Google Air Quality API.

    :param api_key: OpenWeatherMap API key.
    :param location: The location for which to fetch the air quality. String or dict with 'latitude' and 'longitude'.
    :param logger:
    :return: A dictionary containing the current air quality data.
    """

    lat, lon, location_data = geocodeLocation(api_key, location, logger)

    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:

        # figure out the healthiness of the air
        rating, aqi = rate_air_quality(response.json(), logger)
        return {
            "error": "",
            "data": {
                "aqi_rating": rating,
                "aqi": aqi,
                "location": location,
                "raw_data": response.json()
            }
        }

    else:
        logger.error(f"Error retrieving air quality. Error: {response.status_code} - {response.text}.")
        return {
            "error": f"{response.status_code} - {response.text}",
            "data": {
                "aqi_rating": 5,
                "aqi": 5,
                "location": location,
                "raw_data": response.json()
            }

        }


def rate_air_quality(air_response, logger):
    """Returns a worded rating based on the aqi value (e.g(s): Great!, Good, Moderate, Unhealthy, Hazardous"""

    aqi_no = air_response['list'][0]['main']['aqi']

    # Calculate the average aqi value
    if not aqi_no:
        logger.warning("No air quality data available.")
        return {"error": "No air quality data available.", "rating": "error"}, 500

    # Determine the air quality rating based on the average aqi value
    if 0 < aqi_no <= 1:  # if aqi is between 0 and 1
        caq_rating = "Great!"
    elif 1 < aqi_no <= 2:  # if aqi is between 1 and 2
        caq_rating = "Good"
    elif 2 < aqi_no <= 3:  # if aqi is between 2 and 3
        caq_rating = "Moderate"
    elif 3 < aqi_no <= 4:  # if aqi is between 3 and 4
        caq_rating = "Unhealthy"
    elif 4 < aqi_no <= 5:  # if aqi is between 4 and 5
        caq_rating = "Hazardous"
    else:  # if aqi is greater than 5
        logger.error(f"Air quality index is too high (over 5). This is likely an API error. AQI: {aqi_no}.")
        return {
            "error": f"Air quality index is too high (over 5). This is likely an API error. AQI: {aqi_no}.",
            "rating": "error"
        }

    return {"error": "", "rating": caq_rating}
