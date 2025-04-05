# advisor/analyzer.py
import joblib
import pandas as pd
from advisor.weather import get_weather

yield_model = joblib.load('models/yield_model.pkl')
fertilizer_model = joblib.load('models/fertilizer_model.pkl')
pesticide_model = joblib.load('models/pesticide_model.pkl')

CROP_MAP = {
    'Wheat': 0,
    'Rice': 1,
    'Maize': 2,
    'Barley': 3,
    # add more as needed
}

def analyze_farm(crop, land_size, city="Delhi"):
    crop_code = CROP_MAP.get(crop.capitalize())
    if crop_code is None:
        return None

    weather = get_weather(city)
    if not weather:
        return None

    input_data = pd.DataFrame([{
        'Soil_pH': 6.5,  # could also be a sensor or user input
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
