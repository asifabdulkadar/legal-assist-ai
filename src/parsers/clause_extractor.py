import re
from typing import List, Dict, Any

class ClauseExtractor:
    """Extracts clauses and sections from contract text."""
    
    # Common clause headers/patterns
    CLAUSE_PATTERNS = [
        r'^\s*(?:Article|Section|Clause)\s+\d+(?:\.\d+)*[:\s.]',  # Article 1, Section 1.1, Clause 2
        r'^\s*\d+(?:\.\d+)*\.',                                     # 1., 1.1., 1.1.1.
        r'^\s*[A-Z][\w\s]{2,50}:$',                               # TERMINATION:, LIABILITY:
        r'^\s*(?:[IVXLCDM]+)\.',                                   # I., II., III.
        r'^\s*\([a-z\d]+\)',                                      # (a), (1), (i)
    ]

    def __init__(self):
        self.regex = re.compile('|'.join(self.CLAUSE_PATTERNS), re.MULTILINE | re.IGNORECASE)

    def extract_clauses(self, text: str) -> List[Dict[str, Any]]:
        """Splits text into a list of clauses with metadata."""
        lines = text.split('\n')
        clauses = []
        current_clause = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line matches a clause header pattern
            if self.regex.match(line):
                if current_clause:
                    clauses.append(current_clause)
                
                # Start a new clause
                current_clause = {
                    "header": line,
                    "content": "",
                    "level": self._determine_level(line)
                }
            else:
                if current_clause:
                    current_clause["content"] += line + " "
                else:
                    # Content before any clause (introduction/preamble)
                    current_clause = {
                        "header": "Preamble/Introduction",
                        "content": line + " ",
                        "level": 0
                    }
        
        if current_clause:
            clauses.append(current_clause)
            
        # Refine content
        for clause in clauses:
            clause["content"] = clause["content"].strip()
            
        return clauses

    def _determine_level(self, header: str) -> int:
        """Heuristic to determine clause nesting level."""
        if re.match(r'^\s*(?:Article|Section)\s+\d+', header, re.I):
            return 1
        if re.match(r'^\s*\d+\.\s', header):
            return 1
        if re.match(r'^\s*\d+\.\d+', header):
            return 2
        if re.match(r'^\s*\([a-z\d]+\)', header):
            return 3
        return 1
