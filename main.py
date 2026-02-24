import os, sys
import time
import logging

from api.face import detect_face
from api.geocoding import geocodeLocation
from api.ical import get_calendar_events
from api.met_office import GetCurrentWeatherWarningsMetOffice
from api.spotify import get_next_4_tracks_spotify

VERSION = "Beta-1.0.0"

# Set up logging
rootLogger = logging.getLogger()

# Set log file details, these will probably become .env variables someday, sooo... TODO
# logFileTime = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
# logFileName = f'newsflash-{logFileTime}.log'
# logFilePath = "logs"

# Configure the logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

# Make it so logs can be printed to the console (helpful for debugging)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)

# So logs can also go to a file
# fileHandler = logging.FileHandler(f"{logFilePath}/{logFileName}")
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

# Initiate everything else after we have done logging
logging.info("NewsFlash logger started.")
# logging.info("Log file created: %s", logFileName)
logging.info("Starting NewsFlash application...")
logging.info(f"NewsFlash. Version {VERSION}")

from dotenv import load_dotenv
from flask import Flask, request, send_from_directory, send_file, redirect, flash, url_for
from flask_cors import CORS

from api.open_weather_map import get_current_weather, get_weather_forecast, get_current_air_quality # , get_weather_forecast_simple
from api.tfl import all_train_status_tfl, get_set_bus_statuses_tfl


if __name__ == "__main__":
    # Start the flask web server
    app = Flask(__name__)
    CORS(app, origins=["*"]) # enable CORS on all routes.
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Make JSON responses pretty
    app.config['JSON_SORT_KEYS'] = False  # Do not sort keys in JSON responses
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Automatically reload templates on change

    logging.info("Starting the NewsFlash web server...")

    # Set environment variables for the Flask app
    logging.info("Loading environment variables from .env file...")
    # Load environment variables from .env file
    load_dotenv()

    # Take variables from the .env file and set them here

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8080")) # convert to int on the fly

    OPEN_WEATHER_ENABLED = os.getenv( "OPEN_WEATHER_ENABLED" , "false")  # Default to true if not set
    OPEN_WEATHER_API_KEY = os.getenv( "OPEN_WEATHER_API_KEY",  "NOTSET")
    OPEN_WEATHER_LANGUAGE = os.getenv("OPEN_WEATHER_LANGUAGE", "en")  # Default to "en" if not set

    LOCATION = os.getenv("LOCATION") # This is only what's in the .env, don't use this for any functions

    MET_OFFICE_WEATHER_WARNING_REGION = os.getenv( "MET_OFFICE_WEATHER_WARNING_REGION", "NOTSET")

    USERS_NAME = os.getenv(           "USERS_NAME", "User")  # Default to "User" if not set

    SPOTIFY_ENABLED = os.getenv(      "SPOTIFY_ENABLED",       "false")  # Default to false if not set
    SPOTIFY_ACCESS_TOKEN = os.getenv( "SPOTIFY_ACCESS_TOKEN",  "NOTSET")
    SPOTIFY_ACCESS_SECRET = os.getenv("SPOTIFY_ACCESS_SECRET", "NOTSET")
    SPOTIFY_LANGUAGE = os.getenv(     "SPOTIFY_LANGUAGE",      "en-GB")  # Default to "en-GB" if not set

    TFL_TRAINS_ENABLED = os.getenv("TFL_TRAINS_ENABLED", "true")
    TFL_BUSES_ENABLED = os.getenv( "TFL_BUSES_ENABLED", "true")
    TFL_BUS_ROUTES = os.getenv(    "TFL_BUS_ROUTES", "18,25,29,140,149,243,207")

    CALENDAR_ICS_URL = os.getenv("CALENDAR_ICS_URL", "")

    # Log the loaded environment variables
    logging.info("Loaded the environment variables!")

    # Geocode users location
    logging.info("Geocoding user's location...")
    if LOCATION == "OPTOUTLOC": # if user wishes to not give a location.
        LOCATION_COORDS = [0, 0]
        OPEN_WEATHER_ENABLED = False

    else: # if user location is not OPTOUTLOC
        LOCATION_COORDS = geocodeLocation(OPEN_WEATHER_API_KEY, LOCATION, logging)
        if LOCATION_COORDS['error'] != "" and LOCATION_COORDS['data'] == {}:
            # This means the coords fucked up, stop the app and tell the user their location is messed.
            logging.warning("Your location is likely not set correctly!!!")
            logging.info("If you would not like to submit a location, please change it to \"OPTOUTLOC\". Weather integrations (excl. weather alerts) will not work.")
            logging.error(f"LOCATION_COORDS ERROR: {LOCATION_COORDS['error']}")
            logging.error(f"LOCATION_COORDS DATA: {LOCATION_COORDS['data']}")
            logging.warning("Newsflash API shutting down NOW!!!")
            sys.exit(1)
        else:
            logging.info(f"Your location \"{LOCATION}\" is set to LAT, LON: {LOCATION_COORDS['coords'][0]}, {LOCATION_COORDS['coords'][1]}")

    logging.info("Starting the Flask server!")

    # Application warnings go here for the user.
    APPLICATION_USER_WARNINGS = []

    if MET_OFFICE_WEATHER_WARNING_REGION == "NOTSET":
        warning_message = ("YOU HAVE NOT SET THE MET OFFICE WEATHER WARNING LOCATION (For UK users only). "
                           "THIS IS WHERE THE APPLICATION WILL CHECK FOR WEATHER WARNINGS IN THE UK."
                           "WHILE NOT REQUIRED, IT MAY BE HELPFUL IN AN EMERGENCY. FOLLOW THE INSTRUCTIONS IN THE .ENV FILE TO SET YOURS. "
                           "ALTERNATIVELY, TO REMOVE THIS WARNING, CHANGE IT TO \"NOTUK\".")
        APPLICATION_USER_WARNINGS.append(warning_message)
        logging.warning(warning_message)


    # Then, add all the routes

    @app.errorhandler(404)
    def not_found_error_flask(error):
        logging.error(error)
        return {"message": "Resource not found"}, 404

    @app.route("/")
    async def root():
        return redirect('/api/v1'), 303

    @app.route("/license")
    async def license_route():
        txt=""
        with open("LICENSE", "r") as f:
            txt=f.read()

        return str(txt), 200

    @app.route("/api/v1/")
    async def api_v1_root():
        return {
            "message": "This is the API endpoint for Newsflash.",
            "copyright": f"(C) MIT Copyright fwuffyboi / Ashley Caramel {time.strftime("%Y")}",
            "routes": [
                "/api/v1/", "/license", "/api/warnings", "/api/config", "/api/v1/spotify/now-playing/",
                "/api/v1/transport/tfl/train-status/", "/api/v1/transport/tfl/bus-status/", "/ping",
                "/api/v1/weather/current/", "/api/v1/weather/forecast/", "/api/v1/weather/warnings/",
                "/api/v1/air-quality/current/", "/api/v1/ical/", "/api/v1/face/"

            ],
        }, 200

    @app.route("/api/warnings/")
    async def api_warnings():
        return APPLICATION_USER_WARNINGS, 200

    @app.route("/api/config/")
    async def api_config():
        try:
            enabled_apis = []
            if OPEN_WEATHER_ENABLED == "true":
                enabled_apis.append("owm")
            if MET_OFFICE_WEATHER_WARNING_REGION not in ["NOTSET", "NOTUK"]:
                enabled_apis.append("met-office-uk")
            if SPOTIFY_ENABLED == "true":
                enabled_apis.append("spotify")
            if TFL_TRAINS_ENABLED == "true":
                enabled_apis.append("tfl-trains")
            if TFL_BUSES_ENABLED == "true":
                enabled_apis.append("tfl-buses")
            if CALENDAR_ICS_URL != "":
                enabled_apis.append("ical")

            return {
                "error": "",
                "user_name": USERS_NAME,
                "api_version": VERSION,
                "enabled_apis": enabled_apis
            }
        except Exception as e:
            return {
                "error": e,
                "user_name": "",
                "enabled_apis": []
            }


    @app.route("/api/v1/spotify/now-playing/")
    async def get_current_track_spotify():
        """
        Endpoint to get the current track from Spotify.
        Requires the access token to be set in the environment variable SPOTIFY_ACCESS_TOKEN.
        Returns the current track information in JSON format and a 200 status code.
        If the user is not listening to anything, returns a message indicating that and a 204 status code.
        """

        if not SPOTIFY_ENABLED:
            return {"error": "", "message": "Spotify integration is disabled."}, 403

        if not SPOTIFY_ACCESS_TOKEN:
            return {"error": "", "message": "Please set the SPOTIFY_ACCESS_TOKEN in the .env file."}, 403

        current_track_info = get_next_4_tracks_spotify(
            SPOTIFY_ACCESS_TOKEN, SPOTIFY_ACCESS_SECRET,
            SPOTIFY_LANGUAGE, logging
        )
        if current_track_info['error'] == "NPIF":
            return {"error": "", "message": "User is not listening to anything."}, 200

        elif current_track_info['error'] != "":
            return {"error": current_track_info['error'], "message": "Unknown error"}, 500

        return current_track_info, 200

    @app.route("/api/v1/transport/tfl/train-status/")
    async def get_tfl_train_status():
        """
        Endpoint to get the status of all TFL (Transport for London) train lines.
        Returns a JSON response with the status of all TFL train lines and a 200 status code.
        """

        if TFL_TRAINS_ENABLED == "false":
            return {"message": "TFL train statuses are disabled."}, 403

        train_status = all_train_status_tfl(logging)
        if train_status['error']:
            return {"error": "No train status data available. Please check the logs for more information.", "data": {}}, 500

        return {"error": "", "data":train_status['data']}, 200


    @app.route("/api/v1/transport/tfl/bus-status/")
    async def get_tfl_bus_status_flask():
        """
        Endpoint to get the status of all TFL bus lines requested by the user in the .env file.
        Returns a JSON response with the status of the chosen TFL bus lines.
        :return:
        """

        if TFL_BUSES_ENABLED == "false":
            return {"message": "TFL train statuses are disabled."}, 403

        resp = get_set_bus_statuses_tfl(TFL_BUS_ROUTES, logging)
        if resp['error']:
            return {"message": "TFL bus statuses are not available."}, 404

        return {"error": "", "data": resp['data']}, 200


    @app.route("/ping/")
    async def ping():
        return {"message": "pong"}

    # logging routes
    @app.route("/logs/")
    async def get_logs():
        return "Not supported.", 501

        # Find all log files in the current directory
        log_files = [f for f in os.listdir('./logs') if f.startswith('newsflash-') and f.endswith('.log')]
        if not log_files:
            logging.error("No log files found.")
            return {"message": "No log files found."}, 500
        # Sort log files by modification time, oldest first
        log_files.sort(key=lambda x: os.path.getmtime(x))
        # Return the list of log files as JSON
        return {"log_files": log_files}, 200
    
    @app.route("/logs/<log_file_name>/")
    async def get_log_file(log_file_name):
        return "Not supported.", 501

        # Check if the requested log file exists
        if not os.path.exists(log_file_name):
            logging.error(f"Log file {log_file_name} not found.")
            return {"message": f"Log file {log_file_name} not found."}, 404

        # Open the requested log file and return its contents as plain text
        try:
            return send_from_directory('./logs', log_file_name, mimetype='text/plain'), 200
        except Exception as e:
            logging.error(f"Error reading log file {log_file_name}: {e}")
            return {"error": f"Error reading log file {log_file_name}"}, 500
    
    @app.route("/logs/latest/")
    async def get_latest_logs():
        return "Not supported.", 501

        # Open the latest log file and return the last 1000 lines as plain text
        try:
            with open(logFileName, 'r') as file:
                logs = file.readlines()
            return logs[-2000:], 200  # Return the last 2000 lines of the log file as plain text
        except FileNotFoundError:
            logging.error("Latest log file not found.")
            return {"error": "Log file not found."}, 500

    @app.route("/api/v1/weather/current/")
    async def get_current_weather_flask():

        if not OPEN_WEATHER_ENABLED:
            return {"error": "The OpenWeatherMap integration is disabled."}, 403

        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403

        resp = get_current_weather(OPEN_WEATHER_API_KEY, LOCATION_COORDS, OPEN_WEATHER_LANGUAGE, logging)

        if resp["error"]:
            return {"error": "Could not get current weather data. Please check the logs.", "data": {}}
        return {"error": "", "data": resp["data"]}
    
    @app.route("/api/v1/weather/forecast/")
    async def get_weather_forecast_flask():

        if not OPEN_WEATHER_ENABLED:
            return {"error": "The OpenWeatherMap integration is disabled."}, 403

        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403

        resp = get_weather_forecast(OPEN_WEATHER_API_KEY, LOCATION_COORDS, OPEN_WEATHER_LANGUAGE, logging)

        if resp["error"]:
            return {"error": "Could not get forecasted weather data. Please check the logs.", "data": {}}
        return {"error": "", "data": resp["data"]}, 200

    # @app.route("/api/v1/weather/tile/")
    # async def get_weather_tile():
    #     return get_tile_img(location=LOCATION_COORDS, api_key=OPEN_WEATHER_API_KEY, logger=logging)

    # @app.route("/api/v1/weather/forecast/simple/")
    # async def get_weather_forecast_simple_flask():
    #
    #     if not OPEN_WEATHER_ENABLED:
    #         return {"error": "The OpenWeatherMap integration is disabled."}, 403
    #
    #     if not OPEN_WEATHER_API_KEY:
    #         return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403
    #
    #     resp = get_weather_forecast_simple(OPEN_WEATHER_API_KEY, LOCATION_COORDS, OPEN_WEATHER_LANGUAGE, logging)
    #
    #     if resp["error"]:
    #         return {"error": "Could not get simple forecasted weather data. Please check the logs.", "data": {}}
    #     return {"error": "", "data": resp["data"]}, 200


    @app.route("/api/v1/weather/warnings/")
    async def get_weather_warnings_flask():

        if MET_OFFICE_WEATHER_WARNING_REGION == "NOTUK":
            return {"message": "This endpoint is disabled."},

        wa = GetCurrentWeatherWarningsMetOffice(MET_OFFICE_WEATHER_WARNING_REGION, logging)

        if wa['error']:
            return {"error": f"Error occurred getting UK weather warnings for region {MET_OFFICE_WEATHER_WARNING_REGION}. Error: {wa['error']}"}, 500

        return wa, 200


    @app.route("/api/v1/air-quality/current/")
    async def get_current_air_quality_flask():
        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403

        if not LOCATION:
            return {"error": "Please provide a location or set one in the .env file."}, 403

        # take the response
        caq = get_current_air_quality(OPEN_WEATHER_API_KEY, LOCATION_COORDS, logging)

        if caq['error']:
            return caq, 200
        return caq, 200


    @app.route("/api/v1/ical/")
    async def get_ical_flask():

        if CALENDAR_ICS_URL == "":
            return {"message": "This endpoint will not work because the CALENDAR_ICS_URL environment variable is empty."}

        cag = get_calendar_events(CALENDAR_ICS_URL, logging)

        if cag['error']:
            return cag, 500
        return cag, 200


    @app.route('/api/v1/face/', methods=['POST'])
    def face_upload_file():

        """
            Accepts a multipart‑encoded image file.
            Returns JSON.
            """
        if "file" not in request.files:
            return {"error": "No file part"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"error": "Empty filename"}, 400

        # Read file into memory
        img_bytes = file.read()
        if not img_bytes:
            return {"error": "Empty file"}, 400

        try:
            result = detect_face(img_bytes, logging)
            # print(result)
            if result["error"] != "":
                return {"error": result["error"]}
            return {'faces': 1, 'error': ''} # TEST/TODO
        except Exception as e:
            return {"error": str(e)}


    # Run the Flask app
    logging.info(f"Running NewsFlash Server on {HOST}:{PORT}...")

    Flask.run(app, HOST, PORT, debug=True)
