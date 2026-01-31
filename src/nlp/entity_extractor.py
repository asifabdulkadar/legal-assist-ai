import spacy
import re
from typing import Dict, List, Any
from src.config import OPENAI_API_KEY, LLM_MODEL
import openai

class EntityExtractor:
    """Extracts key legal entities from contract text."""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_lg")
        except:
            # Fallback if model not downloaded
            import os
            os.system("python -m spacy download en_core_web_lg")
            self.nlp = spacy.load("en_core_web_lg")

    def extract_entities_spacy(self, text: str) -> Dict[str, List[str]]:
        """Extracts organizations, dates, and amounts using spaCy."""
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
        if not OPENAI_API_KEY:
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
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a legal assistant that extracts structured data from contracts. Output ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"LLM Entity Extraction error: {e}")
            return self.extract_entities_spacy(text)

    def extract(self, text: str) -> Dict[str, Any]:
        """Main extraction method."""
        spacy_ents = self.extract_entities_spacy(text)
        llm_ents = self.extract_entities_llm(text)
        
        # Merge results - prefer LLM for structure
        return {
            "spacy_entities": spacy_ents,
            "structured_data": llm_ents
        }
