########################################################################################################################
# credit to: https://learnpython.com/blog/working-with-icalendar-with-python/
########################################################################################################################

import requests
import icalendar
import recurring_ical_events
from datetime import datetime, timezone, time, timedelta


def get_calendar_events_google(cal_url, logger):
    # Parse the URL

    cal_req = requests.get(cal_url)
    if cal_req.status_code != 200:
        logger.error("Error getting calendar events from Google Calendar: {} - {}.".format(cal_req.status_code, cal_req.text[:40]))
        return None

    cal = icalendar.Calendar.from_ical(cal_req.text)

    try:
        local_tz = datetime.now().astimezone().tzinfo
        today = datetime.now().date()
        start_of_today = datetime.combine(today, time.min, tzinfo=local_tz)
        end_of_today = datetime.combine(today, time.max, tzinfo=local_tz)

        query = recurring_ical_events.of(cal)
        all_events = query.between(start_of_today,
                                   end_of_today + timedelta(seconds=1))  # include events ending at 23:59:59

        next_events = []
        for event in all_events:
            if str(event["DTEND"].dt - event["DTSTART"].dt) == "1 day, 0:00:00":
                duration = "All day"
            else:
                duration = str(event["DTEND"].dt - event["DTSTART"].dt)

            next_events.append(
                {
                    "title": str(event.get("SUMMARY", "")),
                    "desc":  str(event.get("DESCRIPTION", "")),
                    "start": str(event["DTSTART"].dt),
                    "end":   str(event["DTEND"].dt),
                    "location": event.get("LOCATION", ""),
                    "duration": duration,
                }
            )

        return next_events
    except Exception as e:
        logger.error("There was an error in get_calendar_events_google. Error: {}.".format(e))
        return None