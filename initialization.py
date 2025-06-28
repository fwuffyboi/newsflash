# This file checks if the required packages are installed, if APIs are working, etc.
from eink_display import show_message


def check_packages():
    """
    Checks if the required packages are installed. Part 1 of the initialization process.
    :return:
    """
    try:
        import PIL
        import requests
        import bs4
        from PIL import Image, ImageDraw, ImageFont
        import qrcode
        import eink_display  # Assuming this is the module for E-Ink display handling
        from apis.google import get_current_weather, get_weather_forecast, get_current_air_quality
        from apis.met_office import get_current_weather_warnings_UKONLY
        from apis.news_bbc import get_headlines_bbc_news
        from screens.screen_bbc_news import bbc_news_screen_UKONLY

        print("All required packages are installed.")

    except ImportError as e:
        print(f"Missing package: {e.name}. Please install it using pip.")

        # Show on the E-Ink display if possible
        try:
            from eink_display import show_message
            show_message("fatal", f"Missing package: {e.name}. Please install it using pip.")
        except ImportError:
            print("E-Ink display not available to show the message.")

        raise e


def full_initialization():
    """
    Runs the full initialization process, including package checks and API checks.
    :return:
    """
    show_message("info", "Initializing...")

    check_packages()  # make sure all required packages are installed
