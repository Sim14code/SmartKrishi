import os
from datetime import datetime
from advisor.analyzer import analyze_farm
from advisor.prompt_builder import build_prompt
from ollama_integration.llama_api import query_llm
from advisor.translator import translate_to_hindi
from database import init_db, save_log  # ✅ NEW

# ✅ File logging
def save_output_to_file(text, language):
    if not os.path.exists("logs"):
        os.makedirs("logs")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/farmer_output_{language}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"✅ Output saved to {filename}")

# ✅ Advisor logic
def run_advisor(user_input):
    init_db()  # Make sure DB is initialized (can move elsewhere if needed)

    analysis = analyze_farm(
        user_input['crop'],
        user_input['land_size'],
        user_input.get('city', 'Delhi')  # default if not provided
    )
    if not analysis:
        return "Sorry, I couldn't find data for that crop."

    prompt = build_prompt(user_input, analysis)
    english_response = query_llm(prompt)

    final_response = english_response

    if user_input.get("language", "").lower() == "hindi":
        translated_response = translate_to_hindi(english_response)
        final_response = translated_response
        save_output_to_file(translated_response, "hindi")
    else:
        save_output_to_file(english_response, "english")

    # ✅ Save to SQLite
    log_data = {
        "crop": user_input.get("crop"),
        "land_size": user_input.get("land_size"),
        "goal": user_input.get("goal"),
        "city": user_input.get("city", "Delhi"),
        "language": user_input.get("language", "english"),
        "response": final_response
    }
    save_log(log_data)

    return final_response
