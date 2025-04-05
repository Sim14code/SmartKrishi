from data_handler import DataHandler
from model_predictor import MissingValuePredictor
from llm_module import LLMAnalyzer

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
