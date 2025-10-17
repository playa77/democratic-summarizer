# main.py

import os
import argparse
import sys
import config
import pdf_processor
import text_chunker
import summarizer
import output_generator

def main():
    """The main execution function for the document summarization pipeline."""
    parser = argparse.ArgumentParser(
        description="A tool to summarize lengthy legislative and political PDF documents.",
        epilog="Example: python main.py 'path/to/your/document.pdf' --ratio 20"
    )
    parser.add_argument("pdf_path", type=str, help="The full path to the PDF file.")
    parser.add_argument(
        "--ratio",
        type=str,
        required=True,
        choices=['5', '10', '20', '50', '100', 'all'],
        help="The desired summary ratio. Use 'all' to generate all summaries."
    )
    args = parser.parse_args()

    pdf_path = args.pdf_path
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        sys.exit(1)

    print("-" * 60)
    print("Starting Democratic Document Summarizer")
    try:
        config.validate_config()
    except ValueError as e:
        print(e)
        sys.exit(1)
    print(f"Input file: {os.path.basename(pdf_path)}")
    # Add the selected ratio to the initial output for clarity.
    print(f"  -> Summary Ratio: {args.ratio}")
    print("-" * 60)

    # STAGE 1: PDF TEXT EXTRACTION
    print("\n[STAGE 1/4] Extracting text from PDF...")
    full_text = pdf_processor.extract_text_from_pdf(pdf_path)
    if not full_text:
        print("Text extraction failed. Cannot continue.")
        sys.exit(1)
    print("Text extraction complete.")

    # STAGE 2: TEXT CHUNKING
    print("\n[STAGE 2/4] Splitting text using hierarchical chunker...")
    chunks = text_chunker.hierarchical_chunker(full_text, max_chunk_size=config.MAX_CHUNK_SIZE)
    if not chunks:
        print("Text chunking resulted in zero chunks. Cannot continue.")
        sys.exit(1)
    print("Text chunking complete.")

    # STAGE 3: AI SUMMARIZATION
    print("\n[STAGE 3/4] Generating summary with AI model...")
    # The user's selected ratio is now passed to the summarizer.
    # Note: The logic to handle the 'all' case will be built in the next step.
    # For now, this step assumes a single ratio is processed.
    individual_summaries = summarizer.summarize_chunks(chunks, ratio=args.ratio)
    if not individual_summaries:
        print("Summarization failed to produce results. Cannot continue.")
        sys.exit(1)
    final_summary = "\n\n".join(individual_summaries)
    print("AI summarization complete.")

    # STAGE 4: OUTPUT GENERATION
    print("\n[STAGE 4/4] Generating final summary PDF...")
    base_name = os.path.basename(pdf_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{file_name_without_ext}_summary_1_to_{args.ratio}.pdf"
    
    output_generator.create_summary_pdf(
        original_filename=base_name,
        summary_text=final_summary,
        output_path=output_filename
    )
    
    print("-" * 60)
    print("Pipeline finished successfully!")
    print(f"Your summary has been saved to: {output_filename}")
    print("-" * 60)

if __name__ == "__main__":
    main()
