# this file has all met office api integrations in it.
from typing import Any


def get_current_weather_warnings_UKONLY(uk_region, logger) -> list[Any] | None:
    """
    Scrapes potential weather warnings from the Met Office website.

    :return: A dictionary containing weather warning data.
    """
    
    import requests
    from bs4 import BeautifulSoup

    url = f"https://weather.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{uk_region}"
    response = requests.get(url)

    if response.status_code != 200:
        logger.error(f"Request to {url} failed with status code {response.status_code}. Response: {response.text}")
        return None

    soup = BeautifulSoup(response.content, 'xml')

    warnings = []

    try:

        # Find all warning sections
        warning_sections = soup.find_all('div', class_='warning-card')


        if not warning_sections:
            return []

        for section in warning_sections:

            # Extract the warning level from a div with class 'warning-card'. The warning level is in a field on the same div with a value called "data-level".
            warning_level = section.get('data-level',
                                        'No Warning Level')  # Get the warning level from the data-level attribute
            if warning_level == "No Warning Level":
                raise ValueError(
                    "Warning level not found in the section. Please check the HTML structure of the Met Office page.")

            title = section.find('h3').text.strip() if section.find('warning-header') else "No Title"  # todo/fix
            description = section.find('p').text.strip() if section.find('p') else "No Description"

            # Get the warning validity period from 2 sections
            valid_from_period = section.find('div').text.strip() if section.find('div',
                                                                                 class_='valid-from') else "Unknown Valid From Period"
            valid_from_period += section.find('lower date') if section.find('div',
                                                                            class_='valid-from') else "Unknown Valid From Period"

            valid_to_period = section.find('div').text.strip() if section.find('div',
                                                                               class_='valid-TO') else "Unknown Valid From period"

            # Get the link to more details
            link = section.find('a')['href'] if section.find('a') else "No Link"
            warnings.append({'title': title, 'desc': description, 'link': link})

            print(
                f"Title: {title}, Description: {description}, Level: {warning_level}, Valid from-to: {valid_from_period}-{valid_to_period}, Link: {link}")  # todo/debug

        print(f"Found {len(warnings)} weather warnings from the Met Office.")  # todo/debug
        # print(warnings) # todo/debug

        return warnings
    except Exception as e:
        logger.error(f"Error parsing Met Office weather warnings: {e}")
        return None
