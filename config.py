# config.py
import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/llama-3.1-8b-instruct")
try:
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
except (ValueError, TypeError):
    LLM_TEMPERATURE = 0.1
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "4000"))
def validate_config():
    if not OPENROUTER_API_KEY:
        raise ValueError("Config Error: OPENROUTER_API_KEY is not set.")
    print("Configuration loaded successfully.")
    print(f"  -> Using Model: {LLM_MODEL_NAME}")
    print(f"  -> Model Temperature: {LLM_TEMPERATURE}")
