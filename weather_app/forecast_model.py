import requests
import os
from dotenv import load_dotenv
from utils import kelvin_to_celsius

load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_forecast(city: str) -> dict:
    """
    Fetch 5-day weather forecast (every 3 hours) for a given city.
    Returns simplified forecast data as a dictionary.
    """
    params = {
        "q": city,
        "appid": API_KEY
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        # Simplify forecast data: city + list of forecasts
        forecasts = []
        for item in data["list"]:
            forecast_entry = {
                "datetime": item["dt_txt"],
                "temperature_celsius": kelvin_to_celsius(item["main"]["temp"]),
                "humidity": item["main"]["humidity"],
                "condition": item["weather"][0]["description"]
            }
            forecasts.append(forecast_entry)

        result = {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": forecasts
        }

        return result
    else:
        return {"error": f"Failed to fetch forecast: {response.status_code}"}