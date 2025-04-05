from agent import MarketResearcherAgent
from translator_util import TranslatorUtil

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
