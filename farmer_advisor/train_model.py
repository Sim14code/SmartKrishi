# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv('data/farm_dataset.csv')

# Add land size column for training simulation
df['Land_Size'] = 1  # We'll adjust this during predictions

# Encode crop types
df['Crop_Type'] = df['Crop_Type'].astype('category').cat.codes

X = df[['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Crop_Type', 'Land_Size']]
y_yield = df['Crop_Yield_ton']
y_fertilizer = df['Fertilizer_Usage_kg']
y_pesticide = df['Pesticide_Usage_kg']

# Train models
yield_model = RandomForestRegressor()
fertilizer_model = RandomForestRegressor()
pesticide_model = RandomForestRegressor()

yield_model.fit(X, y_yield)
fertilizer_model.fit(X, y_fertilizer)
pesticide_model.fit(X, y_pesticide)

# Save models
joblib.dump(yield_model, 'models/yield_model.pkl')
joblib.dump(fertilizer_model, 'models/fertilizer_model.pkl')
joblib.dump(pesticide_model, 'models/pesticide_model.pkl')
