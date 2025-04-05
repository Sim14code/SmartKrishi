import requests

class LLMAnalyzer:
    def __init__(self, model_name="tinyllama"):
        self.model = model_name
        self.api_url = "http://localhost:11434/api/generate"

    def format_prompt(self, data):
        prompt = "You are a smart and fast agriculture advisor AI. Based on this product's market parameters:\n\n"
        for key, val in data.items():
            prompt += f"{key}: {val}\n"
        prompt += "\nAnalyze the data and suggest the top 3 most profitable crops to plant in the region with market price in rupee and with the percentage of overall market demand.Also no need to give Market ID"  
        prompt += "\n\nPlease provide the analysis in a structured format:\n"
        prompt += "1. Crop Name\n2. Expected Yield\n3. Market Price\n4. Profitability Index\n5. Additional Notes\n and give all these indexes in percentage and in indian standards"
        prompt += "\n\nYour response should be concise and informative."
        
        return prompt

    def get_recommendation(self, filled_data):
        prompt = self.format_prompt(filled_data)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"❌ Error {response.status_code}: {response.text}"
