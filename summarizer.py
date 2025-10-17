# summarizer.py

import os
from typing import List
from tqdm import tqdm
import config

# VERIFIED: Import the correct class 'OpenRouterLLM' from the correct file,
# as confirmed by the inspector script.
from langchain_openrouter.openrouter import OpenRouterLLM

# VERIFIED: Use the simpler 'PromptTemplate' because we are using an 'LLM' class,
# not a 'ChatModel' class.
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def summarize_chunks(chunks: List[str]) -> List[str]:
    """Summarizes text chunks using the correct OpenRouterLLM class."""
    if not chunks:
        return []

    # Use a standard PromptTemplate suitable for an LLM.
    prompt_template = """
    Analyze the following text from a legislative or political document. Your task is to provide a concise, neutral, and factual summary.
    Follow these rules strictly:
    1. Focus only on the key information, regulations, and stated outcomes.
    2. Do not add any interpretation, opinion, or external information.
    3. Present the summary as a clear, factual statement.
    4. The output must be in plain text, not markdown.
    5. Summarize in the same language the Source Text uses.
    Source Text:
    "{text}"
    Factual Summary:
    """
    prompt = PromptTemplate.from_template(prompt_template)
    
    # Instantiate the OpenRouterLLM class.
    # We must pass the parameters exactly as they are defined in the class
    # source code we inspected: 'api_key', 'model', and 'temperature'.
    llm = OpenRouterLLM(
        api_key=config.OPENROUTER_API_KEY,
        model=config.LLM_MODEL_NAME, 
        temperature=config.LLM_TEMPERATURE
    )
    
    output_parser = StrOutputParser()
    
    # The chain works correctly with the LLM-compatible components.
    chain = prompt | llm | output_parser
    
    summaries = []
    for chunk in tqdm(chunks, desc="Generating Summaries", unit="chunk"):
        try:
            summary = chain.invoke({"text": chunk})
            summaries.append(summary)
        except Exception as e:
            print(f"\nAn error occurred while summarizing a chunk: {e}")
            summaries.append("[Error during summarization]")
            
    return summaries
