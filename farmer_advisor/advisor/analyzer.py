# advisor/analyzer.py
import joblib
import pandas as pd

# Load models
yield_model = joblib.load('models/yield_model.pkl')
fertilizer_model = joblib.load('models/fertilizer_model.pkl')
pesticide_model = joblib.load('models/pesticide_model.pkl')

# Hardcoded crop code map (match what was used in training)
CROP_MAP = {
    'Wheat': 0,
    'Rice': 1,
    'Maize': 2,
    'Barley': 3,
    # Add your crop types here based on your dataset
}

# Simulated environment values for now
DEFAULT_ENV = {
    'Soil_pH': 6.5,
    'Soil_Moisture': 30,
    'Temperature_C': 25,
    'Rainfall_mm': 200
}

def analyze_farm(crop, land_size):
    crop_code = CROP_MAP.get(crop.capitalize())
    if crop_code is None:
        return None

    input_data = pd.DataFrame([{
        **DEFAULT_ENV,
        'Crop_Type': crop_code,
        'Land_Size': land_size
    }])

    expected_yield = yield_model.predict(input_data)[0] * land_size
    fertilizer_needed = fertilizer_model.predict(input_data)[0] * land_size
    pesticide_needed = pesticide_model.predict(input_data)[0] * land_size

    # Return results
    return {
        'expected_yield': expected_yield,
        'fertilizer_needed': fertilizer_needed,
        'pesticide_needed': pesticide_needed,
        'sustainability': 7.5  #  can also predict this if needed
    }
