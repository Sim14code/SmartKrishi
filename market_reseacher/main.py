from agent import MarketResearcherAgent

if __name__ == "__main__":
    product = input("Enter crop name (e.g., Wheat): ")
    agent = MarketResearcherAgent()
    result = agent.analyze_product(product)
    print("\n--- Analysis Result ---")
    print(result)
