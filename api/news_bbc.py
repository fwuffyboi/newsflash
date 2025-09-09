# this file has BBC news integrations
def get_headlines_bbc_news(region: str):
    """
    Fetches the latest UK headlines from BBC News.

    :return: A list of dictionaries containing the headline and URL.
    """

    try:
        # take the rss feed url from the BBC News UK section and parse it to get the headlines
        import requests
        from bs4 import BeautifulSoup

        region = region.lower().split(",")

        # To check all provided regions are acceptable/valid
        for area in region:
            if area not in ["uk", "usc", "world"]:
                raise ValueError("Invalid region. Currently, only 'UK', 'USC', or 'WORLD' is accepted.")

        headlines = []

        for area in region:
            if area == "uk":
                url = "https://feeds.bbci.co.uk/news/uk/rss.xml"  # BBC News UK RSS feed URL
            elif area == "usc":
                url = "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
            elif area == "world":
                url = "https://feeds.bbci.co.uk/news/world/rss.xml"
            else:
                raise ValueError("Invalid region. Currently, only 'UK', 'USC', or 'WORLD' is accepted.")

            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(
                    f"Failed to fetch data from BBC News. Status: {response.status_code} --- Response: {response.text}")

            soup = BeautifulSoup(response.content, 'xml')  # Parse the XML content

            # My personal word blocklist, shit I don't care about or want to see on the daily
            blocklist = []

            # set up a temporary list to house the headlines of just this area, then late on add it all together
            temp_lines = []
            item_count = 0

            for item in soup.find_all('item'):

                # Add 1 to the item counter so we know what article we're on
                item_count += 1

                title = item.title.text.strip()
                description = item.description.text.strip()
                link = item.link.text.strip()

                # Check if the title or description contains any blocked words
                if any(blocked_word.lower() in title.lower() for blocked_word in blocklist):
                    title = f"This headline contains one or more of your chosen blocked words."  # If the title contains a blocked word, modify it

                if any(blocked_word.lower() in description.lower() for blocked_word in blocklist):
                    description = f"..."

                temp_lines.append({'title': title, 'desc': description, 'link': link})

            if len(temp_lines) > 6:
                temp_lines = temp_lines[:5]

            # Add the region as well as the temp_lines
            temp_lines = {area: temp_lines}
            headlines.append(temp_lines)

        # after going through every provided region, provide the final result of all headlines.
        return headlines

    except Exception as e:
        raise Exception(f"Error fetching BBC News headlines: {str(e)}")