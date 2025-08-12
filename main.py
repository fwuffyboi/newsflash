# Runs all logic for the application

import os
import time
import logging
# Set up logging
logFileTime = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
logFileName = f'newsflash-{logFileTime}.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=logFileName, filemode='w')

logging.info("NewsFlash logger started. Log file created: %s", logFileName)
logging.info("Starting NewsFlash application...")

# import fastapi
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from api.news_bbc import get_headlines_bbc_news
from api.open_weather_map import get_current_weather
from initialization import full_initialization


def lastmainshit():
    # Run the startup process

    # get_weather_forecast("", "", days=3)
    # get_current_air_quality("", "")
    # get_current_weather_warnings_UKONLY() # fix this. todo/test/fix


    while True:
        # Function logic and vars here
        uk_headlines = get_headlines_bbc_news("UK")
        world_headlines = get_headlines_bbc_news("WORLD")

        # weather_alerts = get_current_weather_warnings_UKONLY() # todo/test/fix

        # Get the current weather forecast
        current_weather_forecast = None  # Initialize to None
        if not LOCATION or not OPEN_WEATHER_API_KEY:
            show_message("warn",
                         "Please set the LOCATION and OPEN_WEATHER_API_KEY in the .env file. "
                         "If you have, check its location. If that does not work, please report the error.",
                         timeout=10)
        else:
            current_weather_forecast = get_current_weather(OPEN_WEATHER_API_KEY, LOCATION)
            # If we have a weather forecast, show it with the time and date
            cwc = current_weather_forecast
            print(cwc)
            current_weather_screen(timeout=10,
                                    current_weather_conditions=cwc['weather'][0]['description'],
                                    current_temperature_celsius=float(cwc['main']['temp']),
                                    current_humidity_percentage=int(cwc['main']['humidity']),
                                    UV_index=4,  # todo/fix
                                    users_name=USERS_NAME
                                    )

# Load environment variables from .env file
load_dotenv()

# Take variables from the .env file and set them here
LOCATION = os.getenv("LOCATION", "London, UK")  # Default to London, UK if not set
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "uk" if not set


if __name__ == "__main__":
    # Start the fastapi web server
    app = FastAPI()


    # First, run the full initialization
    full_initialization(logging)

    # Set environment variables for the FastAPI app
    logging.info("Loading environment variables from .env file...")
    load_dotenv()

    # Take variables from the .env file and set them here
    LOCATION = os.getenv("LOCATION", "London, UK")  # Default to London, UK if not set
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
    NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "uk" if not set

    # Log the loaded environment variables
    logging.info("Loaded the environment variables!")


    logging.info("Starting the FastAPI server!")

    # Then, add all the routes
    @app.get("/")
    async def root():
        return HTMLResponse("<h1><i>The NewsFlash API is up and running!!</i></h1>")
    
    @app.get("/ping")
    async def ping():
        return {"ping": "pong!"}
    
    @app.get("/news/bbc")
    async def get_bbc_news():
        return get_headlines_bbc_news(NEWS_REGION)

    @app.get("/weather/current")
    async def get_current_weather():
        if not LOCATION or not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the LOCATION and OPEN_WEATHER_API_KEY in the .env file."}
        return get_current_weather(OPEN_WEATHER_API_KEY, LOCATION)
    
    @app.get("/weather/forecast")
    async def get_weather_forecast(days: int = 3):
        if not LOCATION or not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the LOCATION and OPEN_WEATHER_API_KEY in the .env file."}
        return get_weather_forecast(OPEN_WEATHER_API_KEY, LOCATION, days=days)
    