# this file has BBC news integrations
def get_headlines_bbc_news(region: str, logger):
    """
    Fetches the latest UK headlines from BBC News.

    :return: A list of dictionaries containing the headline and URL.
    """

    try:
        # take the rss feed url from the BBC News UK section and parse it to get the headlines
        import feedparser

        # lowercase and split all regions in "region" var
        region = region.lower().split(",")

        # To check all provided regions are acceptable/valid
        for area in region:
            if area not in ["uk", "usc", "world"]:
                raise ValueError("Invalid region. Currently, only 'UK', 'USC', or 'WORLD' is accepted.")

        headlines = {}
        ahs = []

        for area in region:
            if area == "uk":
                url = "https://feeds.bbci.co.uk/news/uk/rss.xml"  # BBC News UK RSS feed URL
            elif area == "usc":
                url = "https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
            elif area == "world":
                url = "https://feeds.bbci.co.uk/news/world/rss.xml"
            else:
                raise ValueError("Invalid region. Currently, only 'UK', 'USC', or 'WORLD' is accepted.")

            try:
                feed = feedparser.parse(url)
            except Exception as e:
                logger.error(f"Failed to fetch data from BBC News. Error: feedparser can't parse url --- e: {e.__traceback__}")
                raise Exception(
                    f"Failed to fetch data from BBC News. Error: feedparser can't parse url --- e: {e.__traceback__}")

            # set up a temporary list to house the headlines of just this area, then late on add it all together
            rh = []

            for entry in feed.entries:

                title = entry.title.strip()
                desc  = entry.description.strip()
                link  = entry.link.strip()
                media = entry.media_thumbnail
                pubDate = entry.published.strip()

                # # Check if the title or description contains any blocked words todo
                # if any(blocked_word.lower() in title.lower() for blocked_word in blocklist):
                #     title = f"This headline contains one or more of your chosen blocked words."  # If the title contains a blocked word, modify it
                #
                # if any(blocked_word.lower() in description.lower() for blocked_word in blocklist):
                #     description = f"..."

                rh.append({'title': title, 'desc': desc, 'link': link, 'media': media, 'pubDate': pubDate})

            if len(rh) > 6:
                rh = rh[:6]

            # Add the region as well as the temp_lines
            ahs.append({area: rh})

        # after getting all news for all regions
        headlines = ahs

        # after going through every provided region, provide the final result of all headlines.
        return headlines

    except Exception as e:
        raise Exception(f"Error fetching BBC News headlines: {str(e)}")