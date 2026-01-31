import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")

# Path Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STORAGE_DIR = os.path.join(DATA_DIR, "storage")
TEMPLATE_DIR = os.path.join(DATA_DIR, "templates")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "audit.json")

# Ensure directories exist
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Risk Thresholds
RISK_LEVELS = {
    "LOW": {"score": 1, "color": "green"},
    "MEDIUM": {"score": 2, "color": "orange"},
    "HIGH": {"score": 3, "color": "red"}
}

# Contract Types
CONTRACT_TYPES = [
    "Employment Agreement",
    "Vendor Contract",
    "Lease Agreement",
    "Partnership Deed",
    "Service Contract"
]
