# Runs all logic for the application
from apis.met_office import get_current_weather_warnings_UKONLY

if __name__ == "__main__":
    # Run the startup process
    from eink_display import show_message
    from dotenv import load_dotenv
    import os

    from apis.google import get_current_weather
    from apis.news_bbc import get_headlines_bbc_news
    from screens.screen_bbc_news import bbc_news_screen

    # full_initialization() # todo/uncomment

    # get_weather_forecast("", "", days=3)
    # get_current_air_quality("", "")
    # get_current_weather_warnings_UKONLY() # might not work? todo/test/fix

    load_dotenv()

    while True:

        # Take variables from the .env file and set them here
        LOCATION = os.getenv("LOCATION")
        GOOGLE_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")

        # Function logic and vars here
        uk_headlines = get_headlines_bbc_news("UK")
        world_headlines = get_headlines_bbc_news("WORLD")

        weather_alerts = get_current_weather_warnings_UKONLY()

        if not LOCATION or not GOOGLE_API_KEY:
            show_message("warn", "Please set the LOCATION and GOOGLE_CLOUD_API_KEY in the .env file.", timeout=10)
        else:
            current_weather_forecast = get_current_weather(GOOGLE_API_KEY, LOCATION)

        # Repeat 5 times, then refresh data
        for _ in range(5):
            try:
                # Display time and date first
                # todo/screen

                # display the current weather
                # todo/screen

                # Then do BBC News headlines for the world
                if not world_headlines:
                    show_message("warn", "Failed to fetch news headlines. Please verify your connection, if this persists, please report this issue.", timeout=10)
                else:
                    for article in world_headlines:
                        bbc_news_screen("WORLD", article['title'], article['desc'], article['link'])

                # _IF_ there are weather warnings, then display them here
                # if weather_alerts:
                    # todo/screen

                # Then air quality
                # todo/screen

                # Display the BBC News headlines for UK
                if not uk_headlines:
                    show_message("warn",
                                 "Failed to fetch news headlines. Please verify your connection, if this persists, please report this issue.",
                                 timeout=10)

                else:
                    for article in uk_headlines:
                        bbc_news_screen("UK", article['title'], article['desc'], article['link'])

                # Then the calendar for today
                # todo/feature


            except Exception as e:
                print(f"An error occurred: {e}")
                show_message("fatal", f"An error occurred: {e}. Please check the logs for more details.", timeout=-1)
                break
