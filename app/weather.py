# weather.py
import requests
from app.config import API_KEY, API_URL_WEATHER, API_URL_FORECAST
from requests.exceptions import RequestException

def get_weather(city):  
    current_weather_url= f"{API_URL_WEATHER}?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"{API_URL_FORECAST}?q={city}&appid={API_KEY}&units=metric"

    try:
        # Get current weather
        current_response = requests.get(current_weather_url, timeout=10)
        current_data = current_response.json()
        
        if current_data['cod'] != 200:
            return None, "City not found!"

        # Extract current weather information
        weather_desc = current_data['weather'][0]['description'].capitalize()
        temperature = current_data['main']['temp']
        humidity = current_data['main']['humidity']
        
        # Get forecast weather
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_data = forecast_response.json()

        if forecast_data['cod'] != "200":
            return None, "City not found!"

        # Extract forecast for the next few hours (3-hour intervals)
        forecast_list = forecast_data['list'][:5]  # Get next few intervals (3-hour intervals)
        forecast_info = []

        for forecast in forecast_list:
            time = forecast['dt_txt']
            forecast_desc = forecast['weather'][0]['description'].capitalize()
            temp = forecast['main']['temp']
            forecast_info.append((time, forecast_desc, temp))

        return (weather_desc, temperature, humidity), forecast_info
    
    except RequestException as e:
        return None, f"Error: {str(e)}"
