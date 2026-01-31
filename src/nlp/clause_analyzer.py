import openai
from typing import Dict, Any, List
from src.config import OPENAI_API_KEY, LLM_MODEL

class ClauseAnalyzer:
    """Analyzes individual clauses for rights, obligations, and prohibitions."""
    
    def __init__(self):
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY

    def analyze_clause(self, clause_text: str) -> Dict[str, Any]:
        """Analyzes a clause to determine if it's an obligation, right, or prohibition."""
        if not OPENAI_API_KEY:
            return self._analyze_heuristic(clause_text)

        prompt = f"""
        Analyze the following legal clause and categorize it as 'Obligation', 'Right', or 'Prohibition'.
        Also provide a brief plain-language explanation and a risk level (Low, Medium, High).
        
        Clause:
        {clause_text}
        
        Provide result in JSON format with keys: 'category', 'explanation', 'risk_level'.
        """

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal expert analyzer. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"LLM Clause Analysis error: {e}")
            return self._analyze_heuristic(clause_text)

    def _analyze_heuristic(self, text: str) -> Dict[str, Any]:
        """Simple heuristic-based analysis fallback."""
        text_lower = text.lower()
        category = "Obligation"
        risk_level = "Low"
        
        if any(w in text_lower for w in ["shall", "must", "agrees to", "undertakes"]):
            category = "Obligation"
        elif any(w in text_lower for w in ["may", "has the right", "is entitled to"]):
            category = "Right"
        elif any(w in text_lower for w in ["shall not", "must not", "prohibited", "will not"]):
            category = "Prohibition"
            
        if any(w in text_lower for w in ["indemnify", "penalty", "liable", "terminate"]):
            risk_level = "Medium"
        
        return {
            "category": category,
            "explanation": "Summarization requires LLM access.",
            "risk_level": risk_level
        }
