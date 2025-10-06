import requests


def geocodeLocation(api_key, location, logger):
    if not api_key:  # if no api key
        logger.error("API key is required to geocode a location.")
        return {"error": "API key is required to geocode a location.", "coords": [0,0], "data": {}}

    if not location:  # if no location given
        logger.error("Location is required to geocode a location.")
        return {"error": "Location is required to geocode a location.", "coords": [0,0], "data": {}}

    if not logger:
        print("Logger is required to geocode a location.")
        return {"error": "Logger is required for this function. FUNCTION: geocodeLocation().", "coords": [0,0], "data": {}}

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

                return {"error": "", "coords": [lat, lon], "data": location_data}

            except (IndexError, KeyError):
                logger.error("Unable to geocode the location \"{}\"".format(location))
                return {"error": "Location not found or invalid response from geocoding API.", "coords": [0,0], "data": {}}

        else:
            logger.error(f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}")
            return {"error": f"Error geocoding location. Status: {response.status_code} --- Response: {response.text}", "coords": [0,0], "data": {}}
    else:
        logger.error("Location must be a string.")
        return {"error": "Location must be a string.", "coords": [0,0], "data": {}}