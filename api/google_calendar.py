########################################################################################################################
# credit to: https://learnpython.com/blog/working-with-icalendar-with-python/
########################################################################################################################

import requests
from ics import Calendar
from datetime import datetime, timezone

def get_calendar_events_google(cal_url, logger):
    # Parse the URL

    cal_req = requests.get(cal_url)
    if cal_req.status_code != 200:
        logger.error("Error getting calendar events from Google Calendar: {} - {}.".format(cal_req.status_code, cal_req.text[:40]))
        return None

    cal = Calendar(cal_req.text)

    try:
        now = datetime.now(timezone.utc)
        # Filter events that end after now
        upcoming_events = [event for event in cal.events if event.end.datetime > now]
        # Sort by start time ascending
        upcoming_events = sorted(upcoming_events, key=lambda e: e.begin)

        # Make the next 10 events into json manually so it is possible to return without errors :3c
        next_10_events = []
        for event in upcoming_events[:10]:
            next_10_events.append(
                {
                    "title": str(event.name),
                    "desc": str(event.description),
                    "start": str(event.begin.datetime),
                    "end": str(event.end.datetime),
                    "location": str(event.location),
                    "duration": str(event.duration)
                }
            )

        return next_10_events
    except Exception as e:
        logger.error("There was an issue with get_calendar_events_google. Error: {}.".format(e))
        return None