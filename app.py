import streamlit as st
import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.parsers.document_parser import DocumentParser
from src.parsers.clause_extractor import ClauseExtractor
from src.nlp.contract_classifier import ContractClassifier
from src.nlp.entity_extractor import EntityExtractor
from src.nlp.clause_analyzer import ClauseAnalyzer
from src.nlp.ambiguity_detector import AmbiguityDetector
from src.risk.risk_detector import RiskDetector
from src.risk.risk_scorer import RiskScorer
from src.risk.compliance_checker import ComplianceChecker
from src.legal.alternative_suggester import AlternativeSuggester
from src.multilingual.language_detector import LanguageDetector
from src.multilingual.translator import ContractTranslator
from src.data.audit_logger import AuditLogger
from src.ui.components import render_risk_gauge, render_clause_card, render_entity_summary
from src.legal.templates import TEMPLATES
from src.config import STORAGE_DIR

# Page Config
st.set_page_config(page_title="SME Legal Assistant", layout="wide", page_icon="⚖️")

# Initialize Session State
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def run_analysis(temp_path, filename):
    with st.spinner("Analyzing contract... This may take a minute."):
        parser = DocumentParser()
        raw_text = parser.parse(temp_path)
        clean_text = parser.clean_text(raw_text)
        
        # Language Detection & Translation
        lang_detector = LanguageDetector()
        is_hindi = lang_detector.is_hindi(clean_text)
        
        analysis_text = clean_text
        if is_hindi:
            st.info("Hindi contract detected. Translating for analysis...")
            translator = ContractTranslator()
            analysis_text = translator.translate_to_english(clean_text)
            
        # Classification
        classifier = ContractClassifier()
        contract_type = classifier.classify(analysis_text)
        
        # Entity Extraction
        entity_extractor = EntityExtractor()
        entities = entity_extractor.extract(analysis_text)
        
        # Clause Extraction
        extractor = ClauseExtractor()
        clauses = extractor.extract_clauses(analysis_text)
        
        # Clause Analysis
        analyzer = ClauseAnalyzer()
        ambiguity_detector = AmbiguityDetector()
        risk_detector = RiskDetector()
        risk_scorer = RiskScorer()
        suggester = AlternativeSuggester()
        
        processed_clauses = []
        for i, c in enumerate(clauses):
            # Categorization & Explanation
            analysis = analyzer.analyze_clause(c["content"])
            
            # Risk Detection
            detected_risks = risk_detector.detect_risks(c["content"])
            
            # Ambiguity Detection
            ambiguities = ambiguity_detector.detect_ambiguities_llm(c["content"])
            
            # Scoring
            score_data = risk_scorer.calculate_clause_score(
                analysis["category"], 
                detected_risks, 
                len(ambiguities)
            )
            
            # Alternative Suggestion for High/Medium Risk
            alternative_data = {}
            if score_data["label"] in ["HIGH", "MEDIUM"] and detected_risks:
                alternative_data = suggester.suggest_alternative(c["content"], detected_risks)
            
            processed_clauses.append({
                "header": c["header"],
                "content": c["content"],
                "category": analysis["category"],
                "explanation": analysis["explanation"],
                "detected_risks": detected_risks,
                "ambiguities": ambiguities,
                "risk_score": score_data["score"],
                "risk_label": score_data["label"],
                "risk_color": score_data["color"],
                "alternative": alternative_data.get("alternative"),
                "alternative_explanation": alternative_data.get("explanation")
            })
            
        # Contract Level Score
        contract_risk = risk_scorer.calculate_contract_score(processed_clauses)
        
        # Compliance Check
        compliance_checker = ComplianceChecker()
        compliance_issues = compliance_checker.check_compliance(contract_type, analysis_text)
        
        results = {
            "filename": filename,
            "contract_type": contract_type,
            "entities": entities,
            "clauses": processed_clauses,
            "risk_summary": contract_risk,
            "compliance_issues": compliance_issues,
            "is_hindi": is_hindi
        }
        
        # Audit Log
        logger = AuditLogger()
        logger.log_analysis(filename, contract_type, contract_risk["score"], contract_risk)
        
        return results

# Sidebar
st.sidebar.title("⚖️ Legal Assistant")
st.sidebar.markdown("GenAI-powered contract analysis for Indian SMEs.")

menu = st.sidebar.radio("Navigation", ["Upload & Analyze", "Analysis History", "Templates"])

if menu == "Upload & Analyze":
    st.title("Upload Contract")
    uploaded_file = st.file_uploader("Choose a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        temp_path = os.path.join(STORAGE_DIR, uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        if st.button("Start Analysis"):
            st.session_state.analysis_results = run_analysis(temp_path, uploaded_file.name)
            
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        
        # Dashboard
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            render_risk_gauge(res["risk_summary"]["score"], res["risk_summary"]["label"], res["risk_summary"]["color"])
            
        with col2:
            st.markdown(f"## {res['contract_type']}")
            st.markdown(f"**File:** {res['filename']}")
            if res["is_hindi"]:
                st.caption("Auto-translated from Hindi to English")
                
        with col3:
            st.metric("High Risk Clauses", res["risk_summary"]["high_risk_count"])
            st.metric("Total Clauses", res["risk_summary"]["clause_count"])
            
        st.markdown("---")
        
        # Tabs
        tab_entities, tab_clauses, tab_compliance = st.tabs(["📌 Key Entities", "🔍 Clause Analysis", "📋 Compliance"])
        
        with tab_entities:
            render_entity_summary(res["entities"])
            
        with tab_clauses:
            for idx, clause in enumerate(res["clauses"]):
                render_clause_card(clause, idx + 1)
                
        with tab_compliance:
            st.subheader("Legal Compliance (Indian Law)")
            if res["compliance_issues"]:
                for issue in res["compliance_issues"]:
                    with st.expander(issue["issue"]):
                        st.write(f"**Relevant Law:** {issue['law']}")
                        st.write(f"**Risk:** {issue['risk']}")
                        st.info(f"**Recommendation:** {issue['recommendation']}")
            else:
                st.success("No major compliance issues detected based on preliminary analysis.")

elif menu == "Analysis History":
    st.title("Audit Trail")
    logger = AuditLogger()
    logs = logger.get_logs()
    if logs:
        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)
    else:
        st.info("No analysis history found.")

elif menu == "Templates":
    st.title("SME Contract Templates")
    st.markdown("Download and adapt these SME-friendly templates for your business needs.")
    
    selected_type = st.selectbox("Filter by Contract Type", ["All"] + sorted(list(set(t["type"] for t in TEMPLATES))))
    
    filtered_templates = TEMPLATES
    if selected_type != "All":
        filtered_templates = [t for t in TEMPLATES if t["type"] == selected_type]
        
    for template in filtered_templates:
        with st.expander(f"📄 {template['name']}"):
            st.info(template["description"])
            st.code(template["content"], language="text")
            
            # Simple "Download" button via clipboard or showing full text
            st.button(f"Copy {template['name']} Content", key=template['id'], on_click=lambda t=template: st.write("Content copied to scratchpad! (Demo functionality)"))
            
            # Real download button for .txt format
            st.download_button(
                label="Download as Text File",
                data=template["content"],
                file_name=f"{template['id']}.txt",
                mime="text/plain"
            )
