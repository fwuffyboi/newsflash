# this file has all google api integrations in it.

import requests


def get_current_weather(api_key, location):
    """
    Fetches the current weather for a given location using the Open Weather Map API.

    :param api_key: Open Weather Map API key.
    :param location: The location for which to fetch the weather. String or dict with 'latitude' and 'longitude'.
    :return: A dictionary containing the current weather data.
    """

    if not api_key:  # if no api key
        raise ValueError("API key is required to fetch weather data.")

    if not location:  # if no location given
        raise ValueError("Location is required to fetch weather data.")

    # Convert location to latitude and longitude if it's a string
    if isinstance(location, str): # if location is a string
        # lookup the location to get latitude and longitude
        geocode_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=3&appid={api_key}"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            location_data = response.json()
            print("LOCATION_DATA: ", location_data) # todo/debug
            try:
                lat = location_data[0]['lat']
                lon = location_data[0]['lon']
            except (IndexError, KeyError):
                raise ValueError("Location not found or invalid response from geocoding API.")

        else:
            raise Exception(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")
    else:
        raise ValueError("Location must be a string.")

    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())  # todo/debug
        return response.json()
    else:
        raise Exception(f"Error fetching weather data. Status: {response.status_code} --- Response: {response.text}")


def get_weather_forecast(api_key, location, days=3):
    """
    Fetches the weather forecast for a given location using the Google Weather API.

    :param api_key: Google API key.
    :param location: The location for which to fetch the weather forecast. String or dict with 'latitude' and 'longitude'.
    :param days: Number of days to fetch the forecast for (default is 7).
    :return: A dictionary containing the weather forecast data.
    """

    if not api_key:
        raise ValueError("API key is required to fetch weather forecast data.")
    if not location:
        raise ValueError("Location is required to fetch weather forecast data.")

    # Convert location to latitude and longitude if it's a string
    if isinstance(location, str):
        # lookup the location to get latitude and longitude
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            location_data = response.json()
            if location_data['results']:
                lat = location_data['results'][0]['geometry']['location']['lat']
                lon = location_data['results'][0]['geometry']['location']['lng']
                location = {'latitude': lat, 'longitude': lon}
            else:
                raise ValueError("Location not found.")
        else:
            raise Exception(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")

    url = f"https://weather.googleapis.com/v1/forecast/days:lookup?key={api_key}&location.latitude={lat}&location.longitude={lon}&days={days}"
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json())  # todo
        return response.json()
    else:
        raise Exception(
            f"Error fetching weather forecast data. Status: {response.status_code} --- Response: {response.text}")


def get_current_air_quality(api_key, location):
    """
    Fetches the current air quality for a given location using the Google Air Quality API.

    :param api_key: Google API key.
    :param location: The location for which to fetch the air quality. String or dict with 'latitude' and 'longitude'.
    :return: A dictionary containing the current air quality data.
    """

    if not api_key:
        raise ValueError("API key is required to fetch air quality data.")
    if not location:
        raise ValueError("Location is required to fetch air quality data.")

    # Convert location to latitude and longitude if it's a string
    if isinstance(location, str):
        # lookup the location to get latitude and longitude
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            location_data = response.json()
            if location_data['results']:
                lat = location_data['results'][0]['geometry']['location']['lat']
                lon = location_data['results'][0]['geometry']['location']['lng']
                location = {'latitude': lat, 'longitude': lon}
            else:
                raise ValueError("Location not found.")
        else:
            raise Exception(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")

    url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
    response = requests.post(url, json={"location": {"latitude": lat, "longitude": lon}})

    if response.status_code == 200:
        print(response.json())  # todo
        return response.json()
    else:
        raise Exception(
            f"Error fetching air quality data. Status: {response.status_code} --- Response: {response.text}")
