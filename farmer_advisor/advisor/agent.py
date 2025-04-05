import os
from datetime import datetime
from advisor.analyzer import analyze_farm
from advisor.prompt_builder import build_prompt
from ollama_integration.llama_api import query_llm
from advisor.translator import translate_to_hindi

def save_output_to_file(text, language):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/farmer_output_{language}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"✅ Output saved to {filename}")

def run_advisor(user_input):
    analysis = analyze_farm(user_input['crop'], user_input['land_size'])
    if not analysis:
        return "Sorry, I couldn't find data for that crop."

    prompt = build_prompt(user_input, analysis)
    english_response = query_llm(prompt)

    if user_input.get("language", "").lower() == "hindi":
        translated_response = translate_to_hindi(english_response)
        save_output_to_file(translated_response, "hindi")
        return translated_response

    save_output_to_file(english_response, "english")
    return english_response
