import requests


def all_train_status_tfl(logger):
    """
    Fetches the status of all TFL (Transport for London) train lines.

    :param logger: Logger instance for logging.
    :return: A dictionary containing the status of all TFL train lines.
    """

    url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"

    response = requests.get(url) # tfl's api isn't a heaping pile of shit so its actually free and easy

    if response.status_code == 200:

        # now, parse all the train routes to get their names and service

        response = response.json()

        train_lines_data = {}

        # for each json line in the response
        for line_no in range(len(response)):
            train_line_name = response[line_no]['name']
            train_line_status = response[line_no]['lineStatuses'][0]['statusSeverity']
            train_line_status_description = response[line_no]['lineStatuses'][0]['statusSeverityDescription']
            train_line_disruption_reason = ""

            if train_line_status != 10:
                train_line_disruption_reason = response[line_no]['lineStatuses'][0]['reason']

            train_lines_data[train_line_name] = {"status_int": train_line_status, "status": train_line_status_description, "status_reason": train_line_disruption_reason}

        return {"error": "", "data": train_lines_data}
    else:
        logger.error(f"Error fetching TFL train status. Status: {response.status_code} --- Response: {response.text}")
        return {"error": f"TFL Train status returned {response.status_code} and text: {response.text}", "data": {}}

def get_set_bus_statuses_tfl(buses, logger):
    if not buses:
        logger.warning(f"No buses provided.")
        return {"error": "", "data": {}}

    url = "https://api.tfl.gov.uk/Line/Mode/bus/Status"

    response = requests.get(url)
    # todo: add caching (5min only)

    bus_statuses_data = []
    buses = buses.split(',')

    if response.status_code == 200:
        response = response.json()
        for line_no in range(len(response)):
            bus_name = response[line_no]['name']

            # check if the bus name matches any of the ones in buses
            for bus in buses: # check each bus in buses
                if bus.lower() == bus_name.lower(): # if bus name is a match to one in buses
                    bus_status_no = response[line_no]['lineStatuses'][0]['statusSeverity']

                    if bus_status_no != 10:
                        bus_status_reason = response[line_no]['lineStatuses'][0]['reason']
                    else:
                        bus_status_reason = "Good status."

                    bus_statuses_data.append({"bus_name": bus_name, "status_int": bus_status_no, "status": bus_status_reason})
                else: # if not a match, skip the loop.
                    continue

        return {"error": "", "data": bus_statuses_data}

    else:
        logger.error("Error fetching TFL bus statuses. Status: {} --- Response: {}".format(response.status_code, response.text))
        return {"error": f"TFL Bus status returned {response.status_code} and text: {response.text}", "data": {}}
