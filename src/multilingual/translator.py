from googletrans import Translator as GoogleTranslator
from typing import List, Union

class ContractTranslator:
    """Translates Hindi contracts to English for easier NLP processing."""
    
    def __init__(self):
        self.translator = GoogleTranslator()

    def translate_to_english(self, text: str) -> str:
        """Translates Hindi text to English."""
        try:
            # googletrans handles long strings by chunking internally, 
            # but for very long contracts we might need manual chunking.
            if len(text) > 4500:
                chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
                translated_chunks = []
                for chunk in chunks:
                    result = self.translator.translate(chunk, src='hi', dest='en')
                    translated_chunks.append(result.text)
                return " ".join(translated_chunks)
            else:
                result = self.translator.translate(text, src='hi', dest='en')
                return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text # Fallback to original text

    def translate_list(self, items: List[str]) -> List[str]:
        """Translates a list of strings."""
        try:
            results = self.translator.translate(items, src='hi', dest='en')
            return [r.text for r in results]
        except Exception as e:
            print(f"List translation error: {e}")
            return items
