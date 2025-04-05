# advisor/translator.py
from googletrans import Translator

translator = Translator()

def translate_to_hindi(text):
    try:
        result = translator.translate(text, src='en', dest='hi')
        return result.text
    except Exception as e:
        return f"Translation error: {e}"
