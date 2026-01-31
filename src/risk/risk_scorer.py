from typing import List, Dict, Any
from src.config import RISK_LEVELS

class RiskScorer:
    """Calculates risk scores for individual clauses and the entire contract."""

    def calculate_clause_score(self, category: str, detected_risks: List[str], ambiguity_count: int) -> Dict[str, Any]:
        """Calculates a score from 0-10 for a single clause."""
        score = 0
        
        # Base score based on category
        category_weights = {
            "Obligation": 3,
            "Prohibition": 4,
            "Right": 1
        }
        score += category_weights.get(category, 0)
        
        # Risk factor weights
        risk_weights = {
            "Penalty Clauses": 8,
            "Indemnity Clauses": 9,
            "Unilateral Termination": 7,
            "Arbitration & Jurisdiction": 4,
            "Auto-Renewal": 3,
            "Non-Compete": 6,
            "IP Transfer": 7,
            "Limitation of Liability": 5
        }
        
        max_risk_weight = 0
        for risk in detected_risks:
            max_risk_weight = max(max_risk_weight, risk_weights.get(risk, 2))
        
        score += max_risk_weight
        
        # Ambiguity penalty
        score += min(ambiguity_count * 1, 3)
        
        # Normalize to 1-10
        final_score = min(max(round(score / 2), 1), 10)
        
        # Determine label
        label = "LOW"
        if final_score >= 8:
            label = "HIGH"
        elif final_score >= 4:
            label = "MEDIUM"
            
        return {
            "score": final_score,
            "label": label,
            "color": RISK_LEVELS[label]["color"]
        }

    def calculate_contract_score(self, clause_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates a composite score for the entire contract."""
        if not clause_results:
            return {"score": 0, "label": "N/A", "color": "grey"}
            
        total_score = sum(c["risk_score"] for c in clause_results)
        avg_score = round(total_score / len(clause_results), 1)
        
        # Find highest risk clause
        max_clause_score = max(c["risk_score"] for c in clause_results)
        
        # If any HIGH risk clause exists, bump up the contract score
        composite_score = (avg_score * 0.6) + (max_clause_score * 0.4)
        composite_score = round(min(composite_score, 10), 1)
        
        label = "LOW"
        if composite_score >= 7:
            label = "HIGH"
        elif composite_score >= 4:
            label = "MEDIUM"
            
        return {
            "score": composite_score,
            "label": label,
            "color": RISK_LEVELS[label]["color"],
            "clause_count": len(clause_results),
            "high_risk_count": sum(1 for c in clause_results if c["risk_label"] == "HIGH")
        }
