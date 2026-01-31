import json
import os
from datetime import datetime
from typing import Any, Dict
from src.config import LOG_FILE

class AuditLogger:
    """Logs contract analysis activities for audit trails."""
    
    def __init__(self):
        self.log_file = LOG_FILE
        if not os.path.exists(os.path.dirname(self.log_file)):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_analysis(self, filename: str, contract_type: str, risk_score: float, details: Dict[str, Any]):
        """Logs a single analysis event."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "filename": filename,
            "contract_type": contract_type,
            "risk_score": risk_score,
            "high_risk_clauses": details.get("high_risk_count", 0),
            "total_clauses": details.get("clause_count", 0)
        }
        
        try:
            with open(self.log_file, 'r+') as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs, f, indent=4)
        except Exception as e:
            print(f"Audit logging error: {e}")

    def get_logs(self):
        """Retrieves all logs."""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except:
            return []
