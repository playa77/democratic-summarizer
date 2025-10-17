# config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root.
load_dotenv()

# --- OpenRouter API Configuration ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- Language Model Configuration ---
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/llama-3.3-70b-instruct:free")

try:
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
except (ValueError, TypeError):
    print("Warning: Invalid LLM_TEMPERATURE. Using default value of 0.1")
    LLM_TEMPERATURE = 0.1

# --- Text Processing Configuration ---
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "4000"))

# --- API Pacing Configuration ---
try:
    DELAY_BETWEEN_CHUNKS = int(os.getenv("DELAY_BETWEEN_CHUNKS", "2"))
except (ValueError, TypeError):
    print("Warning: Invalid DELAY_BETWEEN_CHUNKS. Using default value of 2 seconds.")
    DELAY_BETWEEN_CHUNKS = 2

try:
    DELAY_BETWEEN_RATIOS = int(os.getenv("DELAY_BETWEEN_RATIOS", "5"))
except (ValueError, TypeError):
    print("Warning: Invalid DELAY_BETWEEN_RATIOS. Using default value of 5 seconds.")
    DELAY_BETWEEN_RATIOS = 5

def validate_config():
    """Checks that essential configuration (like the API key) is present."""
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "Configuration Error: OPENROUTER_API_KEY is not set.\n"
            "Please create a .env file and add your key."
        )
    print("Configuration loaded successfully.")
    print(f"  -> Using Model: {LLM_MODEL_NAME}")
    print(f"  -> Model Temperature: {LLM_TEMPERATURE}")
    print(f"  -> Delay Between Chunks: {DELAY_BETWEEN_CHUNKS}s")
    print(f"  -> Delay Between Ratios: {DELAY_BETWEEN_RATIOS}s")
