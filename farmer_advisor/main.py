# main.py

import os
from datetime import datetime
import requests
import joblib
import pandas as pd
import sqlite3

# === Load Models ===
yield_model = joblib.load('models/yield_model.pkl')
fertilizer_model = joblib.load('models/fertilizer_model.pkl')
pesticide_model = joblib.load('models/pesticide_model.pkl')

# === Crop Mapping ===
CROP_MAP = {
    'Wheat': 0,
    'Rice': 1,
    'Soybean': 2,
    'Corn': 3,
}

# === Real-Time Weather Fetch ===
API_KEY = "API-KEY"  # Replace with your OpenWeatherMap API key

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

# === Farm Analyzer ===
def analyze_farm(crop, land_size, city="Delhi"):
    crop_code = CROP_MAP.get(crop.capitalize())
    if crop_code is None:
        return None

    weather = get_weather(city)
    if not weather:
        return None

    input_data = pd.DataFrame([{
        'Soil_pH': 6.5,
        'Soil_Moisture': 30,
        'Temperature_C': weather['Temperature_C'],
        'Rainfall_mm': weather['Rainfall_mm'],
        'Crop_Type': crop_code,
        'Land_Size': land_size
    }])

    expected_yield = yield_model.predict(input_data)[0] * land_size
    fertilizer_needed = fertilizer_model.predict(input_data)[0] * land_size
    pesticide_needed = pesticide_model.predict(input_data)[0] * land_size

    return {
        'expected_yield': expected_yield,
        'fertilizer_needed': fertilizer_needed,
        'pesticide_needed': pesticide_needed,
        'sustainability': 7.5,
        'weather_used': weather
    }

# === Prompt Builder ===
def build_prompt(user_input, analysis):
    weather = analysis.get('weather_used', {})
    
    return f"""
You are an expert farmer advisor AI.

The following are the details provided by the farmer and data gathered:

📍 **Farmer Input:**
- Land Size: {user_input['land_size']} acres
- Crop Preference: {user_input['crop']}
- Financial Goal: ₹{user_input['goal']}
- Location: {user_input.get('city', 'Not specified')}

🌦️ **Weather Data (Real-Time):**
- Temperature: {weather.get('Temperature_C', 'N/A')}°C
- Rainfall: {weather.get('Rainfall_mm', 0)} mm
- Humidity: {weather.get('Humidity', 'N/A')}%

📊 **Predicted Farm Insights (via ML):**
- Expected Crop Yield: {analysis['expected_yield']:.2f} tons
- Fertilizer Needed: {analysis['fertilizer_needed']:.1f} kg
- Pesticide Needed: {analysis['pesticide_needed']:.1f} kg
- Sustainability Score: {analysis['sustainability']} / 10

🧠 Based on the above data, generate a detailed farming plan:
- Suggest best practices for this crop
- Recommend how to meet the financial goal
- Include tips to improve sustainability and profit
- Make it localized to the weather and crop type
"""

# === Query Local LLM (TinyLlama) ===
def query_llm(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return "Error: Unable to generate AI response at the moment."

# === Translation (Google Translate) ===
from googletrans import Translator

def translate_to_hindi(text):
    translator = Translator()
    try:
        translated = translator.translate(text, src='en', dest='hi')
        return translated.text
    except Exception as e:
        print(f"⚠️ Translation failed: {e}")
        return "Translation failed. Please try again."


# === Save Output to File ===
def save_output_to_file(text, language):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/farmer_output_{language}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"✅ Output saved to {filename}")

# === SQLite DB Logic ===
DB_NAME = "db.sqlite3"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crop TEXT,
                land_size REAL,
                goal REAL,
                city TEXT,
                language TEXT,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_log(data):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (crop, land_size, goal, city, language, response)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get("crop"),
            data.get("land_size"),
            data.get("goal"),
            data.get("city"),
            data.get("language"),
            data.get("response")
        ))
        conn.commit()

# === Run Advisor ===
def run_advisor(user_input):
    init_db()

    analysis = analyze_farm(
        user_input['crop'],
        user_input['land_size'],
        user_input.get('city', 'Delhi')
    )
    if not analysis:
        return "Sorry, I couldn't find data for that crop or location."

    prompt = build_prompt(user_input, analysis)
    english_response = query_llm(prompt)

    final_response = english_response
    if user_input.get("language", "").lower() == "hindi":
        translated_response = translate_to_hindi(english_response)
        final_response = translated_response
        save_output_to_file(translated_response, "hindi")
    else:
        save_output_to_file(english_response, "english")

    log_data = {
        "crop": user_input.get("crop"),
        "land_size": user_input.get("land_size"),
        "goal": user_input.get("goal"),
        "city": user_input.get("city", "Delhi"),
        "language": user_input.get("language", "english"),
        "response": final_response
    }
    save_log(log_data)

    return final_response

# === Main Execution ===
if __name__ == "__main__":
    user_input = {
        'land_size': 7,
        'crop': 'Rice',
        'goal': 90000,
        'language': 'hindi',
        'city': 'Pune'
    }

    result = run_advisor(user_input)
    print("\nFarming Plan:\n")
    print(result)
