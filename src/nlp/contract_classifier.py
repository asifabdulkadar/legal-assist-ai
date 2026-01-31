import re
import openai
from typing import Optional
from src.config import CONTRACT_TYPES, OPENAI_API_KEY, LLM_MODEL

class ContractClassifier:
    """Classifies the type of contract from its text."""
    
    # Keyword-based heuristics for quick classification
    KEYWORDS = {
        "Employment Agreement": ["employment", "employee", "employer", "salary", "bonus", "role", "position"],
        "Vendor Contract": ["vendor", "supplier", "goods", "delivery", "purchase order", "invoice"],
        "Lease Agreement": ["lease", "tenant", "landlord", "rent", "premises", "security deposit", "eviction"],
        "Partnership Deed": ["partnership", "partners", "profit sharing", "capital contribution", "joint venture"],
        "Service Contract": ["service", "client", "deliverables", "milestones", "statement of work", "consultancy"]
    }

    def __init__(self):
        if OPENAI_API_KEY:
            openai.api_key = OPENAI_API_KEY

    def classify_heuristic(self, text: str) -> Optional[str]:
        """Classifies contract using keyword matching."""
        text_lower = text.lower()
        scores = {ct: 0 for ct in CONTRACT_TYPES}
        
        for ct, keywords in self.KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[ct] += 1
        
        best_match = max(scores, key=scores.get)
        if scores[best_match] > 0:
            return best_match
        return None

    def classify_llm(self, text: str) -> str:
        """Classifies contract using LLM for higher accuracy."""
        if not OPENAI_API_KEY:
            return self.classify_heuristic(text) or "General Agreement"

        # Use only first 2000 chars for classification to save tokens
        sample_text = text[:2000]
        
        prompt = f"""
        Classify the following contract snippet into one of these categories:
        {', '.join(CONTRACT_TYPES)}
        If none match, return 'General Agreement'.
        
        Contract Content:
        {sample_text}
        
        Result:"""

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal assistant specializing in contract classification."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=20,
                temperature=0
            )
            result = response.choices[0].message.content.strip()
            # Clean response
            for ct in CONTRACT_TYPES:
                if ct.lower() in result.lower():
                    return ct
            return "General Agreement"
        except Exception as e:
            print(f"LLM Classification error: {e}")
            return self.classify_heuristic(text) or "General Agreement"

    def classify(self, text: str) -> str:
        """Main classification logic combining heuristics and LLM."""
        return self.classify_llm(text)
