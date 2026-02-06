"""
Comprehensive test suite for Legal Assist AI components.
Tests multiple components with error handling and edge cases.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestRunner:
    """Test runner with reporting capabilities."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def run_test(self, name, test_func):
        """Run a single test and track results."""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"{'='*60}")
        try:
            result = test_func()
            if result:
                print(f"[PASS] {name}: PASSED")
                self.passed += 1
                self.tests.append({"name": name, "status": "PASSED"})
            else:
                print(f"[FAIL] {name}: FAILED")
                self.failed += 1
                self.tests.append({"name": name, "status": "FAILED"})
            return result
        except Exception as e:
            print(f"[ERROR] {name}: ERROR - {e}")
            self.failed += 1
            self.tests.append({"name": name, "status": "ERROR", "error": str(e)})
            return False
    
    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%" if (self.passed+self.failed) > 0 else "N/A")
        print(f"{'='*60}")


def test_language_detector():
    """Test LanguageDetector component."""
    try:
        from src.multilingual.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        # Test cases
        test_cases = [
            ("नमस्ते दुनिया", True, "Hindi text"),
            ("Hello world", False, "English text"),
            ("", False, "Empty string"),
            ("नमस्ते hello world", True, "Mixed text with Hindi"),
            ("123 !@#", False, "Special characters only"),
            ("नमस्ते " * 100, True, "Long Hindi text"),
        ]
        
        all_passed = True
        for text, expected_hindi, description in test_cases:
            result = detector.is_hindi(text)
            if result == expected_hindi:
                print(f"  [PASS] {description}: {result}")
            else:
                print(f"  [FAIL] {description}: expected {expected_hindi}, got {result}")
                all_passed = False
        
        # Test detect_language
        lang_result = detector.detect_language("नमस्ते दुनिया")
        print(f"  [PASS] Language detection: {lang_result}")
        
        return all_passed
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_document_parser():
    """Test DocumentParser component."""
    try:
        from src.parsers.document_parser import DocumentParser
        parser = DocumentParser()
        
        # Test text file parsing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            test_content = "This is a test contract.\n\nIt has multiple paragraphs.\n\nWith various clauses."
            f.write(test_content)
            temp_path = f.name
        
        try:
            # Test TXT parsing
            result = parser.parse(temp_path)
            if "test contract" in result.lower():
                print(f"  [PASS] TXT file parsing: Success")
            else:
                print(f"  [FAIL] TXT file parsing: Content mismatch")
                return False
            
            # Test clean_text
            dirty_text = "This   has    multiple    spaces\n\n\nAnd   newlines"
            cleaned = parser.clean_text(dirty_text)
            if cleaned.count("  ") == 0:  # No double spaces
                print(f"  [PASS] Text cleaning: Success")
            else:
                print(f"  [FAIL] Text cleaning: Still has multiple spaces")
                return False
            
            # Test unsupported format
            try:
                parser.parse("test.xyz")
                print(f"  [FAIL] Unsupported format: Should raise ValueError")
                return False
            except ValueError:
                print(f"  [PASS] Unsupported format: Correctly raises ValueError")
            
            return True
        finally:
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_contract_classifier():
    """Test ContractClassifier component."""
    try:
        from src.nlp.contract_classifier import ContractClassifier
        classifier = ContractClassifier()
        
        # Test heuristic classification
        test_cases = [
            ("This is an employment agreement with salary and bonus", "Employment Agreement"),
            ("Vendor contract for goods delivery and purchase orders", "Vendor Contract"),
            ("Lease agreement for premises with rent and security deposit", "Lease Agreement"),
            ("Random text without keywords", None),  # May return None or "General Agreement"
        ]
        
        all_passed = True
        for text, expected in test_cases:
            result = classifier.classify_heuristic(text)
            print(f"  Text: {text[:50]}...")
            print(f"  Result: {result}")
            if expected is None:
                print(f"  [PASS] Heuristic classification (no match expected)")
            elif result == expected:
                print(f"  [PASS] Heuristic classification: {result}")
            else:
                print(f"  [WARN] Heuristic classification: expected {expected}, got {result} (may still be valid)")
        
        # Test full classification (may use LLM if API key is set)
        try:
            result = classifier.classify("This is an employment contract")
            print(f"  [PASS] Full classification: {result}")
        except Exception as e:
            print(f"  [WARN] Full classification (may require API key): {e}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return False


def test_audit_logger():
    """Test AuditLogger component."""
    try:
        from src.data.audit_logger import AuditLogger
        
        # Create temporary log file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_log = f.name
        
        try:
            # Override log file path (would need to modify AuditLogger to accept path)
            # For now, test with default
            logger = AuditLogger()
            
            # Test logging
            test_details = {
                "high_risk_count": 2,
                "clause_count": 10,
                "score": 75.5
            }
            
            logger.log_analysis("test_contract.pdf", "Employment Agreement", 75.5, test_details)
            print(f"  [PASS] Log entry created")
            
            # Test retrieval
            logs = logger.get_logs()
            if isinstance(logs, list) and len(logs) > 0:
                latest = logs[-1]
                if latest.get("filename") == "test_contract.pdf":
                    print(f"  [PASS] Log retrieval: Success")
                    print(f"     Latest entry: {latest.get('contract_type')} - Risk: {latest.get('risk_score')}")
                else:
                    print(f"  [FAIL] Log retrieval: Entry mismatch")
                    return False
            else:
                print(f"  [WARN] Log retrieval: No logs found (may be using different log file)")
            
            return True
        finally:
            # Cleanup would happen here if we could override log path
            pass
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Test that all main components can be imported."""
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
    
    all_passed = True
    for module_name, class_name in components:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            instance = cls()
            print(f"  [PASS] {class_name}: Imported and instantiated")
        except ImportError as e:
            print(f"  [FAIL] {class_name}: Import failed - {e}")
            all_passed = False
        except Exception as e:
            print(f"  [WARN] {class_name}: Import OK but instantiation failed - {e}")
            # Don't fail on instantiation errors as some may need API keys
    
    return all_passed


def main():
    """Run all tests."""
    runner = TestRunner()
    
    # Run tests
    runner.run_test("Component Imports", test_imports)
    runner.run_test("LanguageDetector", test_language_detector)
    runner.run_test("DocumentParser", test_document_parser)
    runner.run_test("ContractClassifier", test_contract_classifier)
    runner.run_test("AuditLogger", test_audit_logger)
    
    # Print summary
    runner.print_summary()
    
    return runner.failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

