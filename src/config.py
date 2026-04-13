import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_API_KEY = OPENROUTER_API_KEY or OPENAI_API_KEY
OPENROUTER_API_BASE = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/v1") if OPENROUTER_API_KEY else None

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini" if OPENROUTER_API_KEY else "gpt-4")


def get_llm_client():
    """Return a configured OpenAI/OpenRouter client or None if no API key is set."""
    if not LLM_API_KEY:
        return None

    client_kwargs = {"api_key": LLM_API_KEY}
    if OPENROUTER_API_BASE:
        client_kwargs["api_base"] = OPENROUTER_API_BASE
    return openai.OpenAI(**client_kwargs)

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
