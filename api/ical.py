########################################################################################################################
# credit to: https://learnpython.com/blog/working-with-icalendar-with-python/
########################################################################################################################

import requests
import icalendar
import recurring_ical_events
from datetime import datetime, time, timedelta


def get_calendar_events(cal_url, logger):

    cal_req = requests.get(cal_url)
    if cal_req.status_code != 200:
        logger.error("Error getting calendar events from ICalendar URL: {} - {}.".format(cal_req.status_code, cal_req.text[:40]))
        return {"error": f"Status code not 200. status code: {cal_req.status_code}", "next_events": None}

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

            # calculate hasEnded (thank you chatgpt)
            has_ended = (event["DTEND"].dt
                         if isinstance(event["DTEND"].dt, datetime)  # timed event
                         else datetime.combine(event["DTEND"].dt, time.min, tzinfo=local_tz)) <= datetime.now(tz=local_tz)

            next_events.append(
                {
                    "title": str(event.get("SUMMARY", "")),
                    "desc":  str(event.get("DESCRIPTION", "")),
                    "start": str(event["DTSTART"].dt)[11:16],
                    "end":   str(event["DTEND"].dt)[11:16],
                    "location": event.get("LOCATION", ""),
                    "duration": duration,
                    "hasEnded": has_ended,
                }
            )

        return {"error": "", "next_events": sorted(next_events, key=lambda x: x["start"])} # return, sorted by start time
    except Exception as e:
        logger.error(f"There was an error in get_calendar_events. Error: {e}.")
        return {"error": e, "next_events": None}