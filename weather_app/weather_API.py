# weather_api.py
import requests
from utils import kelvin_to_celsius
import os
from dotenv import load_dotenv

try:
    from dotenv import load_dotenv
    load_dotenv()  # load .env only if it exists
except ModuleNotFoundError:
    pass  # on Streamlit Cloud, dotenv is not installed

# Get API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY") 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather(city: str) -> dict:
    """
    get the current weather using OpenWeather API
    """
    params = {
        "q": city,
        "appid": API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        result = {
            "city": data["name"],
            "temperature_celsius": kelvin_to_celsius(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"]
        }
        return result
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

