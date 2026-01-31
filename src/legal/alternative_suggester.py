import openai
from typing import List, Dict, Any
from src.config import OPENAI_API_KEY, LLM_MODEL

class AlternativeSuggester:
    """Suggests alternative, more favorable wordings for high-risk clauses."""
    
    def __init__(self):
        pass

    def suggest_alternative(self, original_clause: str, risks: List[str]) -> Dict[str, Any]:
        """Generates a more SME-friendly alternative using LLM."""
        if not OPENAI_API_KEY:
            return {
                "alternative": "Suggestion requires LLM access.",
                "explanation": "Consult a legal professional for alternative wording."
            }

        prompt = f"""
        Original Clause (Risk identified: {', '.join(risks)}):
        {original_clause}
        
        Task: Provide a more SME-friendly, balanced alternative to this clause that reduces the identified risks while maintaining the core business purpose.
        
        Provide result in JSON format with 'alternative' and 'explanation'.
        """

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal negotiator for SMEs. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Alternative Suggestion error: {e}")
            return {
                "alternative": "Error generating alternative.",
                "explanation": "Please try again later or consult a lawyer."
            }
