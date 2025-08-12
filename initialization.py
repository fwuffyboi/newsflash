# This file checks if the required packages are installed, if APIs are working, etc.
def check_packages(logger):
    """
    Checks if the required packages are installed. Part 1 of the initialization process.
    :return:
    """
    try:
        # import logging - This is not needed here, as it is already imported in main.py
        import fastapi
        import requests
        import PIL
        import bs4
        import PIL
        import qrcode
        from dotenv import load_dotenv

        import os

        from api.open_weather_map import get_current_weather, get_weather_forecast, get_current_air_quality
        from api.met_office import get_current_weather_warnings_UKONLY
        from api.news_bbc import get_headlines_bbc_news

        logger.info("All required packages are installed!")

    except ImportError as e:
        logger.error(f"Missing package: {e.name}. Please install it using pip.")
        print(f"Missing package: {e}. Please run \"pip3/pip install requirements.txt\". If you are using a virtual environment, make sure it is activated.")
        raise e


def full_initialization(logger):
    """
    Runs the full initialization process, including package checks and API checks.
    :return:
    """
    check_packages(logger)  # make sure all required packages are installed
    logger.info("Completed with the NewsFlash initialization process!")        

