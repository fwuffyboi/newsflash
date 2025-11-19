# this file has all met office integrations in it.
import feedparser

def GetCurrentWeatherWarningsMetOffice(uk_region, logger):
    """
    Scrapes potential weather warnings from the Met Office RSS list.

    :return: A dictionary containing weather warning data.
    """

    url = f"https://weather.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{uk_region}"
    # url = f"http://localhost:5173/UK" # TESTING URL
    try:
        feed = feedparser.parse(url)
    #     todo: add caching
    except Exception as e:
        logger.error(f"Attempt to get weather warnings failed. Error: feedparser e:{e.__traceback__}")
        return ['!!!COULD NOT PARSE RSS FEED FOR MET OFFICE!!!',
                '!!!COULD NOT PARSE RSS FEED FOR MET OFFICE!!!',
                '!!!COULD NOT PARSE RSS FEED FOR MET OFFICE!!!'
        ]

    warnings = []

    try:
        # Get the link to more details
        for entry in feed.entries:
            title = entry.title
            description = entry.description
            link = entry.link
            if 'red warning' in str(title).lower():
                warn_level = 'Red'
            elif 'amber warning' in str(title).lower():
                warn_level = 'Amber'
            elif 'yellow warning' in str(title).lower():
                warn_level = 'Yellow'
            else:
                warn_level = 'Unknown'

            warnings.append({'level': warn_level, 'title': title, 'desc': description, 'link': link})

            logger.info(
                f"!!!WEATHER WARNING FOUND!!!: Title: {title}, Description: {description}, "
                f"Level: {warn_level}, Link: {link}")

        logger.info(f"Found {len(warnings)} weather warnings from the Met Office for region \"{uk_region}\".")

        return {"error": "", "warnings": warnings}
    except Exception as e:
        logger.error(f"Error parsing Met Office weather warnings: {e}")
        return {"error": e, "warnings": []}
