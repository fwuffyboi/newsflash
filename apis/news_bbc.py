# this file has BBC news integrations

def get_headlines_bbc_news(region: str):
    """
    Fetches the latest UK headlines from BBC News.

    :return: A list of dictionaries containing the headline and URL.
    """

    # take the rss feed url from the BBC News UK section and parse it to get the headlines
    import requests
    from bs4 import BeautifulSoup

    if region.lower() not in ["uk", "usc", "world"]:
        raise ValueError("Invalid region. Currently, only 'UK', 'USC', or 'WORLD' is accepted.")

    if region.lower() == "uk":
        url = "https://feeds.bbci.co.uk/news/uk/rss.xml"  # BBC News UK RSS feed URL
    elif region.lower() == "usa":
        url = "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
    elif region.lower() == "world":
        url = "https://feeds.bbci.co.uk/news/world/rss.xml"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch data from BBC News. Status: {response.status_code} --- Response: {response.text}")

    soup = BeautifulSoup(response.content, 'xml')  # Parse the XML content
    headlines = []

    # My personal word blocklist, shit i dont care about or wanna see on the daily
    blocklist = ["rape", "abuse", "stab", "stabbing", "prince"]

    for item in soup.find_all('item'):
        title = item.title.text.strip()
        description = item.description.text.strip()
        link = item.link.text.strip()

        # Check if the title or description contains any blocked words
        if any(blocked_word.lower() in title.lower() for blocked_word in blocklist):
            title = f"Headline contains blocked word(s)"  # If the title contains a blocked word, modify it

        if any(blocked_word.lower() in description.lower() for blocked_word in blocklist):
            description = f"Description contains blocked word(s)"

        # Print the title to the console
        # print(title) # todo/debug

        headlines.append({'title': title, 'desc': description, 'link': link})

    # Limit the number of headlines to 5
    if len(headlines) >= 5:
        headlines = headlines[:5]

    # print(headlines) # todo/debug

    return headlines
