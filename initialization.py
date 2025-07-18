# This file checks if the required packages are installed, if APIs are working, etc.
def check_packages():
    """
    Checks if the required packages are installed. Part 1 of the initialization process.
    :return:
    """
    try:
        import kivy
        print(kivy.__version__)  # Print Kivy version for debugging
        import kivy_deps
        print("Kivy dependencies are installed.")
        import requests
        import PIL
        import bs4
        from PIL import Image, ImageDraw, ImageFont
        import qrcode
        from dotenv import load_dotenv

        import os

        from apis.open_weather_map import get_current_weather, get_weather_forecast, get_current_air_quality
        from apis.met_office import get_current_weather_warnings_UKONLY
        from apis.news_bbc import get_headlines_bbc_news
        from screens.bbc_news import bbc_news_screen

        print("All required packages are installed.")

    except ImportError as e:
        print(f"Missing package: {e.name}. Please install it using pip.")

        # Show on the E-Ink display if possible
        try:
            from screens.message import show_message
            show_message("fatal", f"Missing package: {e.name}. Please install it using pip.")
        except ImportError:
            print("E-Ink display not available to show the message.")

        raise e


def full_initialization():
    """
    Runs the full initialization process, including package checks and API checks.
    :return:
    """
    check_packages()  # make sure all required packages are installed
