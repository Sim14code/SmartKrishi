# advisor/weather.py
import requests

API_KEY = "API_KEY"

def get_weather(city="Delhi"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        print("⚠️ Failed to fetch weather data.")
        return None

    data = response.json()

    temperature = data["main"]["temp"]
    rainfall = data.get("rain", {}).get("1h", 0)  # Rainfall in mm (last 1 hour)
    humidity = data["main"]["humidity"]
    
    return {
        "Temperature_C": temperature,
        "Rainfall_mm": rainfall,
        "Humidity": humidity
    }
