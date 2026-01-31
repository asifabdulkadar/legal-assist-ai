import openai
from typing import List, Dict, Any
from src.config import OPENAI_API_KEY, LLM_MODEL

class ComplianceChecker:
    """Checks contract compliance with general Indian business law principles."""
    
    def __init__(self):
        pass

    def check_compliance(self, contract_type: str, text: str) -> List[Dict[str, Any]]:
        """Identifies potential compliance issues based on common Indian laws."""
        if not OPENAI_API_KEY:
            return self._heuristic_check(contract_type, text)

        prompt = f"""
        Identify potential legal compliance issues in this {contract_type} according to Indian laws (e.g., Contract Act, Companies Act, IT Act, Labour Laws).
        Focus on SMEs.
        
        Contract Content (Sample):
        {text[:5000]}
        
        Provide result in JSON format as a list of issues with: 'issue', 'law', 'risk', 'recommendation'.
        """

        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are an Indian legal compliance expert for SMEs. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            data = json.loads(response.choices[0].message.content)
            return data.get("issues", data if isinstance(data, list) else [])
        except Exception as e:
            print(f"Compliance Check error: {e}")
            return self._heuristic_check(contract_type, text)

    def _heuristic_check(self, contract_type: str, text: str) -> List[Dict[str, Any]]:
        """Basic heuristic-based compliance checks."""
        issues = []
        text_lower = text.lower()
        
        if "stamp duty" not in text_lower:
            issues.append({
                "issue": "Stamp Duty Mention Missing",
                "law": "Indian Stamp Act, 1899",
                "risk": "Contract may be inadmissible as evidence in court.",
                "recommendation": "Ensure appropriate stamp duty is paid and mentioned."
            })
            
        if contract_type == "Employment Agreement" and "gratuity" not in text_lower:
            issues.append({
                "issue": "Gratuity Policy Not Specified",
                "law": "Payment of Gratuity Act, 1972",
                "risk": "Potential non-compliance if employee completes 5 years.",
                "recommendation": "Include terms regarding gratuity eligibility."
            })
            
        return issues
