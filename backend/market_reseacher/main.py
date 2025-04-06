
from googletrans import Translator

class TranslatorUtil:
    def __init__(self):
        self.translator = Translator()

    def to_hindi(self, text):
        return self.translator.translate(text, src='en', dest='hi').text

    def to_english(self, text):
        return self.translator.translate(text, src='hi', dest='en').text
    
import pandas as pd

class DataHandler:
    def __init__(self, path):
        self.df = pd.read_csv(path)

    def get_product_data(self, product_name):
        row = self.df[self.df['Product'].str.lower() == product_name.lower()]
        return row.iloc[0].to_dict() if not row.empty else {}
    
    def get_training_data(self):
        return self.df.dropna()


from sklearn.ensemble import RandomForestRegressor
import pandas as pd



class MissingValuePredictor:
    def __init__(self, df):
        self.df = df
        self.models = {}
        self.train_models()

    def train_models(self):
        ignore = ['Product', 'Market_ID']
        features = [col for col in self.df.columns if col not in ignore]

        for target in features:
            temp_df = self.df.dropna(subset=[target])  # Ensure target is not NaN
            X = temp_df.drop(columns=[target] + ignore)
            y = temp_df[target]

        # Keep only numeric features
            X = X.select_dtypes(include=['int64', 'float64'])

            if not X.empty and y.dtype in ['int64', 'float64']:
                try:
                    model = RandomForestRegressor(n_estimators=100)
                    model.fit(X, y)
                    self.models[target] = model
                except Exception as e:
                    print(f"⚠️ Skipping model for {target}: {e}")

    def fill_missing(self, row):
        filled = row.copy()
        base_features = {k: v for k, v in row.items() if isinstance(v, (int, float))}

        for param, model in self.models.items():
            if param not in filled or pd.isna(filled[param]):
                try:
                    df_input = pd.DataFrame([base_features]).select_dtypes(include=['int64', 'float64'])

                    filled[param] = model.predict(df_input)[0]
                except Exception as e:
                    print(f"⚠️ Could not predict {param}: {e}")
        return filled
        

import requests

class LLMAnalyzer:
    def __init__(self, model_name="tinyllama"):
        self.model = model_name
        self.api_url = "http://localhost:11434/api/generate"
    

    def format_prompt(self, data):
        prompt = (
            "You are a smart and fast agriculture advisor AI. Based on the following product's market parameters, "
            "analyze and provide:\n"
            "1. Crop Name\n2. Expected Yield\n3. Market Price\n4. Profitability Index\n5. Additional Notes\n"
            "All indexes should be given in percentage and aligned with Indian agricultural standards.\n\n"
        )
        for key, val in data.items():
            prompt += f"{key}: {val}\n"
        
        prompt += (
            "\nAnalyze the data and suggest the top 3 most profitable crops to plant in the region, "
            "with expected market prices in INR and the percentage of overall market demand.\n"
            "Do not include additional information or Market ID in the suggestions.\n\n"
            "Your response should be structured and should only analyze the given product data "
            "(not the suggested crops).\n\n"
            "Keep the response concise and informative."
        )
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

class MarketResearcherAgent:
    def __init__(self):
        self.data_handler = DataHandler("data/market_researcher_dataset.csv")
        self.df = self.data_handler.get_training_data()
        self.predictor = MissingValuePredictor(self.df)
        self.llm = LLMAnalyzer()

    def analyze_product(self, product_name):
        print(f"\n🔍 Product: {product_name}")
        product_data = self.data_handler.get_product_data(product_name)

        if not product_data:
            return "❌ Product not found in dataset."

        filled = self.predictor.fill_missing(product_data)
        result = self.llm.get_recommendation(filled)
        return result

if __name__ == "__main__":
    translator = TranslatorUtil()

    # Input in English
    product = input("Enter crop name (e.g., Wheat): ")

    # Language selection
    print("\nSelect output language:")
    print("1. English")
    print("2. Hindi")
    lang_choice = input("Enter choice (1 or 2): ")

    # Run analysis
    agent = MarketResearcherAgent()
    result = agent.analyze_product(product)

    # Handle output
    if lang_choice == "2":
        result = translator.to_hindi(result)
        print("\n--- विश्लेषण परिणाम ---")
    else:
        print("\n--- Analysis Result ---")

    print(result)
