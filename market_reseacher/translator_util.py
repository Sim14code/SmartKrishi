# translator_util.py

from googletrans import Translator

class TranslatorUtil:
    def __init__(self):
        self.translator = Translator()

    def to_hindi(self, text):
        return self.translator.translate(text, src='en', dest='hi').text

    def to_english(self, text):
        return self.translator.translate(text, src='hi', dest='en').text
