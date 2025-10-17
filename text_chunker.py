# text_chunker.py
import re, spacy
from typing import List
nlp = spacy.load("en_core_web_sm")
def _split_long_paragraph(text: str, max_size: int) -> List[str]:
    doc = nlp(text)
    sub_chunks, current_chunk = [], ""
    for sent in doc.sents:
        sentence_text = sent.text.strip()
        if len(current_chunk) + len(sentence_text) + 1 > max_size:
            if current_chunk: sub_chunks.append(current_chunk)
            current_chunk = sentence_text
        else:
            current_chunk = (current_chunk + " " + sentence_text) if current_chunk else sentence_text
    if current_chunk: sub_chunks.append(current_chunk)
    return sub_chunks
def hierarchical_chunker(text: str, max_chunk_size: int) -> List[str]:
    if not text: return []
    initial_paragraphs = re.split(r'\n\s*\n', text)
    final_chunks = []
    for p in initial_paragraphs:
        p = p.strip()
        if not p: continue
        if len(p) <= max_chunk_size: final_chunks.append(p)
        else: final_chunks.extend(_split_long_paragraph(p, max_chunk_size))
    return final_chunks
