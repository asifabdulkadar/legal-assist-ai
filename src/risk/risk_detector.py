import re
from typing import List, Dict, Any

class RiskDetector:
    """Detects specific high-risk legal clauses."""
    
    RISK_PATTERNS = {
        "Penalty Clauses": r'\b(penalty|liquidated damages|forfeit|compensation for delay)\b',
        "Indemnity Clauses": r'\b(indemnify|indemification|hold harmless|defend)\b',
        "Unilateral Termination": r'\b(terminate at any time|terminate without cause|absolute discretion to terminate)\b',
        "Arbitration & Jurisdiction": r'\b(arbitration|jurisdiction|governing law|courts of)\b',
        "Auto-Renewal": r'\b(automatically renew|auto-renewal|evergreen clause)\b',
        "Non-Compete": r'\b(non-compete|restrictive covenant|restraint of trade|non-solicitation)\b',
        "IP Transfer": r'\b(intellectual property|assignment of ip|work for hire|ownership of deliverables)\b',
        "Limitation of Liability": r'\b(limitation of liability|maximum liability|aggregate liability)\b'
    }

    def detect_risks(self, clause_text: str) -> List[str]:
        """Identifies which risk categories a clause belongs to."""
        text_lower = clause_text.lower()
        found_risks = []
        
        for risk_name, pattern in self.RISK_PATTERNS.items():
            if re.search(pattern, text_lower):
                found_risks.append(risk_name)
        
        return found_risks

    def get_risk_description(self, risk_name: str) -> str:
        """Returns a predefined description of why a category is risky."""
        descriptions = {
            "Penalty Clauses": "May impose heavy financial burdens for minor delays or breaches.",
            "Indemnity Clauses": "Could make you liable for 3rd party claims or costs beyond your control.",
            "Unilateral Termination": "Allows the other party to end the contract without a specific reason, creating business instability.",
            "Arbitration & Jurisdiction": "Specifies where and how disputes are settled; expensive or far-away locations increase risk.",
            "Auto-Renewal": "The contract might continue indefinitely unless you manually opt out.",
            "Non-Compete": "Restricts your ability to work for competitors or start a similar business after termination.",
            "IP Transfer": "Might result in loss of ownership over work you've created.",
            "Limitation of Liability": "May unfairly limit the other party's financial responsibility if they cause you loss."
        }
        return descriptions.get(risk_name, "Potential legal commitment requiring review.")
