import spacy
import re
import subprocess
import sys
import logging
from typing import Dict, List, Any
from src.config import LLM_API_KEY, LLM_MODEL, get_llm_client

logger = logging.getLogger(__name__)

# Global cache for spacy model to avoid repeated load attempts
_spacy_model = None
_spacy_load_attempted = False

class EntityExtractor:
    """Extracts key legal entities from contract text."""
    
    def __init__(self):
        global _spacy_model, _spacy_load_attempted
        
        self.nlp = None
        
        # Use cached result if already attempted
        if _spacy_load_attempted:
            self.nlp = _spacy_model
            return
        
        try:
            self.nlp = spacy.load("en_core_web_lg")
            _spacy_model = self.nlp
            _spacy_load_attempted = True
        except OSError:
            logger.warning("en_core_web_lg not found. Attempting to download...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "spacy", "download", "en_core_web_lg"],
                    check=True,
                    capture_output=True,
                    timeout=300
                )
                self.nlp = spacy.load("en_core_web_lg")
                _spacy_model = self.nlp
            except Exception as e:
                logger.error(f"Failed to download/load spacy model: {e}. Using LLM extraction only.")
                self.nlp = None
            finally:
                _spacy_load_attempted = True
                _spacy_model = self.nlp

    def extract_entities_spacy(self, text: str) -> Dict[str, List[str]]:
        """Extracts organizations, dates, and amounts using spaCy."""
        if not self.nlp:
            # Return empty if model unavailable
            return {
                "Parties": [],
                "Dates": [],
                "Monetary Amounts": [],
                "Jurisdictions": []
            }
        
        # Process first 100k chars for performance
        doc = self.nlp(text[:100000])
        
        entities = {
            "Parties": [],
            "Dates": [],
            "Monetary Amounts": [],
            "Jurisdictions": []
        }
        
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PERSON"]:
                entities["Parties"].append(ent.text)
            elif ent.label_ == "DATE":
                entities["Dates"].append(ent.text)
            elif ent.label_ == "MONEY":
                entities["Monetary Amounts"].append(ent.text)
            elif ent.label_ == "GPE":
                entities["Jurisdictions"].append(ent.text)
        
        # Deduplicate
        for k in entities:
            entities[k] = list(set(entities[k]))
            
        return entities

    def extract_entities_llm(self, text: str) -> Dict[str, Any]:
        """Extracts key structured data using LLM for higher precision."""
        if not LLM_API_KEY:
            return self.extract_entities_spacy(text)

        # Use first 3000 chars - usually contains parties and basic terms
        sample_text = text[:3000]
        
        prompt = f"""
        Extract the following information from this contract:
        1. Parties (Names of companies/individuals)
        2. Effective Date
        3. Total Value/Financial Obligations (if mentioned)
        4. Termination Notice Period
        5. Governing Law/Jurisdiction
        
        Contract Content:
        {sample_text}
        
        Provide the result in JSON format.
        """

        try:
            client = get_llm_client()
            if not client:
                logger.warning("LLM client not configured. Falling back to spacy extraction.")
                return self.extract_entities_spacy(text)
            
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal assistant that extracts structured data from contracts. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            result = json.loads(response.choices[0].message.content)
            if not isinstance(result, dict):
                logger.error(f"LLM returned non-dict JSON: {type(result)}")
                return self.extract_entities_spacy(text)
            return result
        except json.JSONDecodeError as e:
            logger.error(f"LLM Entity Extraction - JSON decode error: {e}")
            return self.extract_entities_spacy(text)
        except KeyError as e:
            logger.error(f"LLM Entity Extraction - Key error accessing response: {e}")
            return self.extract_entities_spacy(text)
        except Exception as e:
            logger.error(f"LLM Entity Extraction error: {e}")
            return self.extract_entities_spacy(text)

    def extract(self, text: str) -> Dict[str, Any]:
        """Main extraction method."""
        try:
            spacy_ents = self.extract_entities_spacy(text)
            llm_ents = self.extract_entities_llm(text)
            
            # Ensure llm_ents is a dict
            if not isinstance(llm_ents, dict):
                logger.warning(f"LLM extraction returned non-dict type: {type(llm_ents)}")
                llm_ents = {}
            
            # Merge results - prefer LLM for structure
            return {
                "spacy_entities": spacy_ents,
                "structured_data": llm_ents or {}
            }
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {
                "spacy_entities": {
                    "Parties": [],
                    "Dates": [],
                    "Monetary Amounts": [],
                    "Jurisdictions": []
                },
                "structured_data": {}
            }
