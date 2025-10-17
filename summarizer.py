# summarizer.py

import os
from typing import List
from tqdm import tqdm
import config
import sys

# VERIFIED: Import the correct class 'OpenRouterLLM' from the correct file.
from langchain_openrouter.openrouter import OpenRouterLLM

# VERIFIED: Use the simpler 'PromptTemplate' because we are using an 'LLM' class.
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def load_prompt_from_file(ratio: str) -> str:
    """Loads a prompt template from the corresponding file in the 'prompts' directory."""
    prompt_path = os.path.join("prompts", f"ratio_{ratio}.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at '{prompt_path}'.")
        print("Please ensure a prompt file exists for the specified ratio.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading prompt file '{prompt_path}': {e}")
        sys.exit(1)

def summarize_chunks(chunks: List[str], ratio: str) -> List[str]:
    """
    Summarizes text chunks using a dynamically loaded prompt based on the specified ratio.
    """
    if not chunks:
        return []

    # Dynamically load the prompt template from an external file.
    prompt_template_str = load_prompt_from_file(ratio)
    prompt = PromptTemplate.from_template(prompt_template_str)
    
    # Instantiate the OpenRouterLLM class.
    llm = OpenRouterLLM(
        api_key=config.OPENROUTER_API_KEY,
        model=config.LLM_MODEL_NAME, 
        temperature=config.LLM_TEMPERATURE
    )
    
    output_parser = StrOutputParser()
    
    # The chain works correctly with the LLM-compatible components.
    chain = prompt | llm | output_parser
    
    summaries = []
    for chunk in tqdm(chunks, desc=f"Generating Summaries (1:{ratio} ratio)", unit="chunk"):
        try:
            summary = chain.invoke({"text": chunk})
            summaries.append(summary)
        except Exception as e:
            print(f"\nAn error occurred while summarizing a chunk: {e}")
            summaries.append("[Error during summarization]")
            
    return summaries
