# pdf_processor.py
import pdfplumber
def extract_text_from_pdf(pdf_path: str) -> str:
    full_text = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error processing PDF file '{pdf_path}': {e}")
        return ""
