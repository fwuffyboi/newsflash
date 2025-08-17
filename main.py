import os, sys
import time
import logging

# Set up logging
rootLogger = logging.getLogger()

# set log file details, these will probably become .env variables someday, sooo... TODO
logFileTime = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
logFileName = f'newsflash-{logFileTime}.log'
logFilePath = "."

# Configure the logging format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

# Make it so logs can be printed to the console (helpful for debugging)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout)) # this is annoying and messes with the console logging

# So logs can also go to a file
fileHandler = logging.FileHandler("{0}/{1}".format(logFilePath, logFileName))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

# Initiate everything else after we have done logging
logging.info("NewsFlash logger started. Log file created: %s", logFileName)
logging.info("Starting NewsFlash application...")

from dotenv import load_dotenv
from flask import Flask, request, send_from_directory

from api.news_bbc import get_headlines_bbc_news
from api.open_weather_map import get_current_weather, get_weather_forecast, get_current_air_quality

from initialization import full_initialization


# Load environment variables from .env file
load_dotenv()

# Take variables from the .env file and set them here
LOCATION = os.getenv("LOCATION", "Krakow, Poland")  # Default to Kraków if not set
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "world" if not set
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_ACCESS_SECRET = os.getenv("SPOTIFY_ACCESS_SECRET")
SPOTIFY_LANGUAGE = os.getenv("SPOTIFY_LANGUAGE", "en-US")  # Default to "en-US" if not set


if __name__ == "__main__":
    # Start the fastapi web server
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Make JSON responses pretty
    app.config['JSON_SORT_KEYS'] = False  # Do not sort keys in JSON responses
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Automatically reload templates on change

    logging.info("Starting the NewsFlash web server...")

    # First, run the full initialization
    full_initialization(logging)

    # Set environment variables for the FastAPI app
    logging.info("Loading environment variables from .env file...")
    load_dotenv()

    # Take variables from the .env file and set them here
    LOCATION = os.getenv("LOCATION", "Krakow, Poland")  # Default to London, UK if not set
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
    NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "world" if not set

    # Log the loaded environment variables
    logging.info("Loaded the environment variables!")


    logging.info("Starting the Flask server!")

    # Then, add all the routes

    @app.errorhandler(404)
    def not_found_error_flask(error):
        if request.path.startswith('/api/'):
            logging.error(error)
            return {"message": "Resource not found"}, 404
        else:
            try:
                return send_from_directory('./web', '404.html'), 404
            except Exception as e:
                logging.error("404.html not found in the web directory: %s", e)
                return {"message": "Error.", "error": "404 error, however the server could not find 404.html to serve."}, 500
    @app.route("/")
    async def root():
        return f"put docs here for api" # This is in HTML somehow

    @app.route("/web/")
    async def web_index():
        # Serve the index.html file from the web directory
        try:
            return send_from_directory('web', 'index.html')
        except Exception as e:
            if "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." in str(
                    e):
                logging.error(f"Index page not found.")
                return send_from_directory('web', '404.html'), 404
            else:
                logging.error(f"Error serving index page: {e}")
                return {"message": "Error serving index page."}, 500

    @app.route("/web/<path:subpath>/")
    async def web(subpath):
        # Serve other web pages based on the subpath
        try:
            return send_from_directory('web', subpath)
        except Exception as e:
            if "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." in str(e):
                logging.error(f"Web page {subpath} not found.")
                return send_from_directory('web', '404.html'), 404
            else:
                logging.error(f"Error serving web page {subpath}: {e}")
                return {"message": "Error serving web page."}, 500

    @app.route("/api/v1/spotify/now-playing/")
    async def get_current_track_spotify():
        """
        Endpoint to get the current track from Spotify.
        Requires the access token to be set in the environment variable SPOTIFY_ACCESS_TOKEN.
        Returns the current track information in JSON format and a 200 status code.
        If the user is not listening to anything, returns a message indicating that and a 204 status code.
        """
        from api.spotify import get_current_track_spotify

        if not SPOTIFY_ACCESS_TOKEN:
            return {"message": "Please set the SPOTIFY_ACCESS_TOKEN in the .env file."}, 403

        current_track_info = get_current_track_spotify(SPOTIFY_ACCESS_TOKEN, SPOTIFY_ACCESS_SECRET,
                                                       SPOTIFY_LANGUAGE, logging)
        if not current_track_info:
            return {"message": "Could not retrieve current track from Spotify."}, 204

        return current_track_info, 200


    @app.route("/ping/")
    async def ping():
        # logRequest(request) # do NOT log pings, waste of electricity
        return {"message": "pong!"}

    # logging routes
    @app.route("/logs/")
    async def get_logs():
        # Find all log files in the current directory
        log_files = [f for f in os.listdir('.') if f.startswith('newsflash-') and f.endswith('.log')]
        if not log_files:
            logging.error("No log files found.")
            return {"message": "No log files found."}, 500
        # Sort log files by modification time, oldest first
        log_files.sort(key=lambda x: os.path.getmtime(x))
        # Return the list of log files as JSON
        return {"log_files": log_files}, 200
    
    @app.route("/logs/<log_file_name>/")
    async def get_log_file(log_file_name):

        # Check if the requested log file exists
        if not os.path.exists(log_file_name):
            logging.error(f"Log file {log_file_name} not found.")
            return {"message": f"Log file {log_file_name} not found."}, 404

        # Open the requested log file and return its contents as plain text
        try:
            return send_from_directory('.', log_file_name, mimetype='text/plain'), 200
        except Exception as e:
            logging.error(f"Error reading log file {log_file_name}: {e}")
            return {"message": f"Error reading log file {log_file_name}"}, 500
    
    @app.route("/logs/latest/")
    async def get_latest_logs():

        # Open the latest log file and return the last 1000 lines as plain text
        try:
            with open(logFileName, 'r') as file:
                logs = file.readlines()
            return logs[-2000:]  # Return the last 2000 lines of the log file as plain text
        except FileNotFoundError:
            logging.error("Latest log file not found.")
            return {"message": "Log file not found."}, 500
    
    @app.route("/api/v1/news/bbc/")
    async def get_bbc_news():
        """
        Endpoint to get the latest BBC news headlines.
        :return : JSON response with the latest headlines and a 200 status code.
        """
        # todo/implement fully
        return get_headlines_bbc_news(NEWS_REGION), 200

    @app.route("/api/v1/weather/current/")
    async def get_current_weather_flask():

        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403
    
        return get_current_weather(OPEN_WEATHER_API_KEY, LOCATION, logging)
    
    @app.route("/api/v1/weather/forecast/")
    async def get_weather_forecast_flask():

        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}, 403
       
        return get_weather_forecast(OPEN_WEATHER_API_KEY, LOCATION, logging)

    @app.route("/api/v1/air-quality/current/")
    async def get_current_air_quality_flask():
        if not LOCATION or not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the LOCATION and OPEN_WEATHER_API_KEY in the .env file."}, 403
        
        return get_current_air_quality(OPEN_WEATHER_API_KEY, LOCATION, logging)

    HOST = "0.0.0.0"
    PORT = 8080

    logging.info(f"Running NewsFlash Server on {HOST}:{PORT}...")

    Flask.run(app, HOST, PORT, debug=True)
