# Runs all logic for the application

import os
import threading
import time

from dotenv import load_dotenv
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager

from apis.news_bbc import get_headlines_bbc_news
from apis.open_weather_map import get_current_weather
from initialization import full_initialization
from screens.message import show_message
from screens.bbc_news import BBCNewsScreen
from screens.taskbar import Taskbar
from screens.weather import current_weather_screen


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



# Make sure all is good to go before starting the app
full_initialization()

# Load environment variables from .env file
load_dotenv()

# Take variables from the .env file and set them here
LOCATION = os.getenv("LOCATION", "London, UK")  # Default to London, UK if not set
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "uk" if not set

# Global variable to store news
news_data = []

def fetch_news_periodically():
    from apis.news_bbc import get_headlines_bbc_news
    while True:
        news_data["uk"] = get_headlines_bbc_news("UK")
        news_data["world"] = get_headlines_bbc_news("WORLD")
        time.sleep(300)  # Fetch every 5 minutes

# Start the background thread
threading.Thread(target=fetch_news_periodically(newsRegion), daemon=True).start()


# Build the layout of the app here
class NewsFlashApp(App):
    def build(self):
        Window.fullscreen = True
        root = BoxLayout(orientation="horizontal")
        info_bar = Taskbar(size_hint_y=0.1)
        sm = ScreenManager()
        sm.add_widget(BBCNewsScreen(name="BBC News", newsRegion=BBCNewsRegion,
                                    articleTitle=BBCNewsArticleTitle,
                                    articleDescription=BBCNewsArticleDescription,
                                    articleURL=BBCNewsArticleURL))
        sm.add_widget(CurrentWeatherScreen(name="second"))
        root.add_widget(info_bar)
        root.add_widget(sm)
        return root


if __name__ == "__main__":
    NewsFlashApp().run()
