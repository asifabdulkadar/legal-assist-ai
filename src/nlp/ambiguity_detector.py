import re
from typing import List, Dict, Any
from src.config import OPENAI_API_KEY, LLM_MODEL
import openai

class AmbiguityDetector:
    """Detects vague or ambiguous language in contract clauses."""
    
    # Common vague terms in legal documents
    VAGUE_TERMS = [
        "reasonable", "best efforts", "promptly", "material", "substantial",
        "to the extent possible", "in a timely manner", "appropriate",
        "ordinarily", "generally", "commonly", "fairly"
    ]

    def __init__(self):
        pass

    def detect_ambiguities_heuristic(self, text: str) -> List[str]:
        """Identifies vague terms using keyword matching."""
        found = []
        text_lower = text.lower()
        for term in self.VAGUE_TERMS:
            if re.search(r'\b' + term + r'\b', text_lower):
                found.append(term)
        return found

    def detect_ambiguities_llm(self, text: str) -> List[Dict[str, str]]:
        """Uses LLM to detect more complex semantic ambiguities."""
        if not OPENAI_API_KEY:
            terms = self.detect_ambiguities_heuristic(text)
            return [{"term": t, "reason": "Common vague term used in legal context."} for t in terms]

        prompt = f"""
        Identify ambiguous, vague, or subjective terms in the following clause that could lead to disputes.
        Explain why each term is ambiguous.
        
        Clause:
        {text}
        
        Provide result in JSON format as a list of objects with 'term' and 'reason'.
        """

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal risk analyst. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            data = json.loads(response.choices[0].message.content)
            return data.get("ambiguities", data if isinstance(data, list) else [])
        except Exception as e:
            print(f"LLM Ambiguity Detection error: {e}")
            terms = self.detect_ambiguities_heuristic(text)
            return [{"term": t, "reason": "Common vague term."} for t in terms]
