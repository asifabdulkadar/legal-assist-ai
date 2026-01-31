from deep_translator import GoogleTranslator
from typing import List, Union

class ContractTranslator:
    """Translates Hindi contracts to English for easier NLP processing."""
    
    def __init__(self):
        # We initialize the translator with source 'hi' and target 'en'
        # deep-translator instances are specific to source-target pairs usually, 
        # or we can pass it in translate() but defining it here is cleaner if fixed.
        # However, to match previous flexibility, we can just instantiate it.
        # deep_translator's GoogleTranslator takes source and target in constructor.
        self.translator = GoogleTranslator(source='hi', target='en')

    def translate_to_english(self, text: str) -> str:
        """Translates Hindi text to English."""
        try:
            # deep-translator handles limits better, but explicit chunking is still safe for massive texts.
            # 5000 chars is Google's limit usually.
            if len(text) > 4500:
                chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
                translated_chunks = []
                for chunk in chunks:
                    # translate method returns a string directly
                    result = self.translator.translate(chunk)
                    translated_chunks.append(result)
                return " ".join(translated_chunks)
            else:
                return self.translator.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return text # Fallback to original text

    def translate_list(self, items: List[str]) -> List[str]:
        """Translates a list of strings."""
        try:
            # deep-translator has translate_batch
            return self.translator.translate_batch(items)
        except Exception as e:
            print(f"List translation error: {e}")
            return items
