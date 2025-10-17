import os
from dotenv import load_dotenv

# Load environment variables from .env file.
# This allows for secure and flexible configuration without modifying the code.
load_dotenv()

# --- Core LLM Configuration ---

# Load the API key from the environment. This is mandatory for the app to run.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load the model name from .env, providing a powerful, tested model as a fallback.
# The value in your .env file will always take precedence.
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "meta-llama/llama-3.3-70b-instruct:free")

# Load the model temperature from .env, with a default for consistent output.
try:
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
except (ValueError, TypeError):
    LLM_TEMPERATURE = 0.1

# Load the max chunk size from .env. The default is set to a higher value
# based on research into the new model's capabilities. Your .env value will be used.
try:
    MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "16000"))
except (ValueError, TypeError):
    MAX_CHUNK_SIZE = 16000

# --- Load External Prompt Template ---
try:
    # The prompt is externalized to keep it separate from application logic.
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        PROMPT_TEMPLATE = f.read()
except FileNotFoundError:
    # If the prompt is missing, the application cannot function.
    raise RuntimeError("Fatal Error: The 'prompt.txt' file was not found in the project directory.")

def validate_config():
    """Validates that essential configuration variables are set and prints the active configuration."""
    if not OPENROUTER_API_KEY:
        raise ValueError("Config Error: OPENROUTER_API_KEY is not set in the .env file.")
    
    print("Configuration loaded successfully from .env (with defaults for missing values):")
    print(f"  -> Using Model: {LLM_MODEL_NAME}")
    print(f"  -> Model Temperature: {LLM_TEMPERATURE}")
    print(f"  -> Max Chunk Size: {MAX_CHUNK_SIZE} characters")
