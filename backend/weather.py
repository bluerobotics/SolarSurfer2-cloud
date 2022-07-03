import requests
import json
from utils import temporary_cache
import os

@temporary_cache(timeout_seconds=300) # we can only query the api 1000 times a day, and weather doesnt change that fast
def get_weather_data(lat, lon):
    try:
        token = os.environ["VISUALCROSSINGTOKEN"]
        print("getting new weather data...")
        request = requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat}%2C{lon}/today?unitGroup=metric&include=current&key={token}&contentType=json")
        return request.json()
    except KeyError:
        print("Visual Crossing Weather API not found, please set the environment variable VISUALCROSSINGTOKEN")
    except Exception as e:
        return json.dumps({"error: ": str(e)})