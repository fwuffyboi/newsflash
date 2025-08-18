import requests


def geocodeLocation(api_key, location, logger):
    if not api_key:  # if no api key
        logger.error("API key is required to geocode a location.")
        raise ValueError("API key is required to geocode a location.")

    if not location:  # if no location given
        logger.error("Location is required to geocode a location.")
        raise ValueError("Location is required to geocode a location.")

    # Convert location to latitude and longitude if it's a string
    if isinstance(location, str):  # if location is a string
        # lookup the location to get latitude and longitude
        geocode_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        response = requests.get(geocode_url)
        if response.status_code == 200:
            location_data = response.json()

            try:
                lat = location_data[0]['lat']
                lon = location_data[0]['lon']

                return lat, lon, location_data

            except (IndexError, KeyError):
                logger.error("Unable to fetch weather data for location {}".format(location))
                raise ValueError("Location not found or invalid response from geocoding API.")

        else:
            logger.error(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")
            raise Exception(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")
    else:
        logger.error("Location must be a string.")
        raise ValueError("Location must be a string.")