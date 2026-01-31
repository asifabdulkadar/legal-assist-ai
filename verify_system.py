
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_components():
    logger.info("Starting system verification...")
    failures = []

    components = [
        ("src.parsers.document_parser", "DocumentParser"),
        ("src.parsers.clause_extractor", "ClauseExtractor"),
        ("src.nlp.contract_classifier", "ContractClassifier"),
        ("src.nlp.entity_extractor", "EntityExtractor"),
        ("src.nlp.clause_analyzer", "ClauseAnalyzer"),
        ("src.nlp.ambiguity_detector", "AmbiguityDetector"),
        ("src.risk.risk_detector", "RiskDetector"),
        ("src.risk.risk_scorer", "RiskScorer"),
        ("src.risk.compliance_checker", "ComplianceChecker"),
        ("src.legal.alternative_suggester", "AlternativeSuggester"),
        ("src.multilingual.language_detector", "LanguageDetector"),
        ("src.multilingual.translator", "ContractTranslator"),
        ("src.data.audit_logger", "AuditLogger"),
    ]

    for module_name, class_name in components:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            instance = cls()
            logger.info(f"SUCCESS: {class_name} initialized correctly.")
        except ImportError as e:
            logger.error(f"FAILURE: Could not import {class_name} from {module_name}. Error: {e}")
            failures.append(f"{class_name} (ImportError)")
        except Exception as e:
            logger.error(f"FAILURE: Could not instantiate {class_name}. Error: {e}")
            failures.append(f"{class_name} (RuntimeError: {e})")

    # Check UI components (functions)
    try:
        from src.ui.components import render_risk_gauge, render_clause_card, render_entity_summary
        logger.info("SUCCESS: UI components imported correctly.")
    except Exception as e:
        logger.error(f"FAILURE: Could not import UI components. Error: {e}")
        failures.append("UI Components")

    if failures:
        logger.error(f"System verification failed for: {', '.join(failures)}")
        sys.exit(1)
    else:
        logger.info("All system components verified successfully!")
        sys.exit(0)

if __name__ == "__main__":
    verify_components()
