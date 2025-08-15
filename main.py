import os
import time
import logging

# Set up logging
logFileTime = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
logFileName = f'newsflash-{logFileTime}.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=logFileName, filemode='w')

logging.info("NewsFlash logger started. Log file created: %s", logFileName)
logging.info("Starting NewsFlash application...")

from dotenv import load_dotenv
from flask import Flask, request

from api.news_bbc import get_headlines_bbc_news
from api.open_weather_map import get_current_weather, get_weather_forecast, get_current_air_quality

from initialization import full_initialization


# Load environment variables from .env file
load_dotenv()

# Take variables from the .env file and set them here
LOCATION = os.getenv("LOCATION", "Krakow, PL")  # Default to Krakow if not set
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "world" if not set


def logRequest(request):
    requested_url = request.url
    if requested_url is None or requested_url == "":
        requested_url = "Unknown URL"
    requesting_ip = request.remote_addr
    if requesting_ip is None or requesting_ip == "":
        requesting_ip = "Unknown IP"
    
    request_method = request.method
    if request_method is None or request_method == "":
        request_method = "Unknown Method"
    user_agent = request.headers.get('User-Agent', 'Unknown User Agent')

    toLog = f"Request received!, method: {request_method}, URL: {requested_url}, IP: {requesting_ip}, User-Agent: {user_agent}, Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"

    logging.info(toLog)


if __name__ == "__main__":
    # Start the fastapi web server
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Make JSON responses pretty
    app.config['JSON_SORT_KEYS'] = False  # Do not sort keys in JSON responses

    logging.info("Starting NewsFlash's Flask API...")


    # First, run the full initialization
    full_initialization(logging)

    # Set environment variables for the FastAPI app
    logging.info("Loading environment variables from .env file...")
    load_dotenv()

    # Take variables from the .env file and set them here
    LOCATION = os.getenv("LOCATION", "London, UK")  # Default to London, UK if not set
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    USERS_NAME = os.getenv("USERS_NAME", "User")  # Default to "User" if not set
    NEWS_REGION = os.getenv("NEWS_REGION", "world")  # Default to "world" if not set

    # Log the loaded environment variables
    logging.info("Loaded the environment variables!")


    logging.info("Starting the Flask server!")

    # Then, add all the routes
    @app.route("/")
    def root():
        logRequest(request)
        return f"Replace this with the svelte web page. oh yh get doxxed: {str(request.remote_addr)}" # This is in HTML... somehow....
    
    @app.route("/ping/")
    async def ping():
        # logRequest(request) # do NOT log pings, literal waste of electricity
        return {"message": "pong!"}
    
    @app.route("/logs/")
    async def get_logs():
        logRequest(request)
        # Find all log files in the current directory
        log_files = [f for f in os.listdir('.') if f.startswith('newsflash-') and f.endswith('.log')]
        if not log_files:
            logging.error("No log files found.")
            return {"message": "No log files found."}
        # Sort log files by modification time, oldest first
        log_files.sort(key=lambda x: os.path.getmtime(x))
        # Return the list of log files as JSON
        return {"log_files": log_files}
    
    @app.route("/logs/<log_file_name>/")
    async def get_log_file(log_file_name):
        logRequest(request)

        # Check if the requested log file exists
        if not os.path.exists(log_file_name):
            logging.error(f"Log file {log_file_name} not found.")
            return {"message": f"Log file {log_file_name} not found."}

        # Open the requested log file and return its contents as plain text
        try:
            with open(log_file_name, 'r') as file:
                logs = file.readlines()
            return logs  # Return the contents of the log file as plain text
        except Exception as e:
            logging.error(f"Error reading log file {log_file_name}: {e}")
            return {"message": f"Error reading log file {log_file_name}: {str(e)}"}
    
    @app.route("/logs/latest/")
    async def get_latest_logs():
        logRequest(request)

        # Open the latest log file and return the last 1000 lines as plain text
        try:
            with open(logFileName, 'r') as file:
                logs = file.readlines()
            return logs[-1000:]  # Return the last 1000 lines of the log file as plain text
        except FileNotFoundError:
            logging.error("Latest log file not found.")
            return {"message": "Log file not found."}
    
    @app.route("/api/v1/news/bbc/")
    async def get_bbc_news():
        logRequest(request)

        if not NEWS_REGION or NEWS_REGION.lower() not in ["uk", "usa", "world"]:
            return get_bbc_news(NEWS_REGION)  # Default to the set NEWS_REGION if no valid region is provided
        
        return get_headlines_bbc_news(NEWS_REGION)

    @app.route("/api/v1/weather/current/")
    async def get_current_weather_flask():
        logRequest(request)
        
        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}
    
        return get_current_weather(OPEN_WEATHER_API_KEY, LOCATION)
    
    @app.route("/api/v1/weather/forecast/")
    async def get_weather_forecast_flask():
        logRequest(request)
       
        if not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the OPEN_WEATHER_API_KEY in the .env file."}
       
        return get_weather_forecast(OPEN_WEATHER_API_KEY, LOCATION)

    @app.route("/api/v1/air-quality/current/")
    async def get_current_air_quality_flask():
        if not LOCATION or not OPEN_WEATHER_API_KEY:
            return {"error": "Please set the LOCATION and OPEN_WEATHER_API_KEY in the .env file."}
        
        return get_current_air_quality(OPEN_WEATHER_API_KEY, LOCATION)

    Flask.run(app, host="0.0.0.0", port=8080, debug=True)