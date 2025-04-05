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
