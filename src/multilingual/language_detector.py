import re
from typing import Optional

class LanguageDetector:
    """Detects the language of a contract (primarily English vs Hindi)."""
    
    # Range of Hindi characters in Unicode
    HINDI_RANGE = re.compile(r'[\u0900-\u097F]+')

    def detect_language(self, text: str) -> str:
        """Determines if the text is primarily Hindi or English."""
        # Clean text for better detection
        sample = text[:5000]
        hindi_chars = len(self.HINDI_RANGE.findall(sample))
        total_chars = len(sample)
        
        if total_chars == 0:
            return "English"
            
        # If more than 5% characters are Hindi, classify as Hindi
        if (hindi_chars / total_chars) > 0.05:
            return "Hindi"
        
        return "English"

    def is_hindi(self, text: str) -> bool:
        """Checks if there is any Hindi text present."""
        return bool(self.HINDI_RANGE.search(text))
