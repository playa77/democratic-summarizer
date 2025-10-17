# main.py
import os, argparse, sys, config, pdf_processor, text_chunker, summarizer, output_generator
def main():
    parser = argparse.ArgumentParser(description="Summarize legislative PDF documents.")
    parser.add_argument("pdf_path", type=str, help="Path to the input PDF file.")
    args = parser.parse_args()
    pdf_path = args.pdf_path
    if not os.path.exists(pdf_path): sys.exit(f"Error: File '{pdf_path}' not found.")
    print("-" * 60)
    print("Starting Democratic Document Summarizer")
    try: config.validate_config()
    except ValueError as e: sys.exit(e)
    print(f"Input file: {os.path.basename(pdf_path)}")
    print("-" * 60)
    print("\n[STAGE 1/4] Extracting text...")
    full_text = pdf_processor.extract_text_from_pdf(pdf_path)
    if not full_text: sys.exit("Text extraction failed.")
    print("\n[STAGE 2/4] Chunking text...")
    chunks = text_chunker.hierarchical_chunker(full_text, config.MAX_CHUNK_SIZE)
    if not chunks: sys.exit("Text chunking failed.")
    print("\n[STAGE 3/4] Generating summary...")
    summaries = summarizer.summarize_chunks(chunks)
    if not summaries: sys.exit("Summarization failed.")
    final_summary = "\n\n".join(summaries)
    print("\n[STAGE 4/4] Creating summary PDF...")
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_filename = f"{base_name}_summary.pdf"
    output_generator.create_summary_pdf(os.path.basename(pdf_path), final_summary, output_filename)
    print("-" * 60)
    print(f"Success! Summary saved to: {output_filename}")
    print("-" * 60)
if __name__ == "__main__":
    main()
