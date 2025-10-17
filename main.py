# main.py

import os
import argparse
import sys
import time
import config
import pdf_processor
import text_chunker
import summarizer
import output_generator

def get_unique_filename(path: str) -> str:
    """
    Checks if a file exists at the given path. If it does, it appends a
    counter to the filename until a unique filename is found.
    
    Example:
      If "summary.pdf" exists, it will return "summary (1).pdf".
    """
    if not os.path.exists(path):
        return path
    
    base_name, extension = os.path.splitext(path)
    counter = 1
    new_path = f"{base_name} ({counter}){extension}"
    
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base_name} ({counter}){extension}"
        
    print(f"Warning: Output file '{os.path.basename(path)}' already exists.")
    print(f"  -> Saving to '{os.path.basename(new_path)}' instead.")
    return new_path

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
    
    summaries_dict = {}
    
    if args.ratio == 'all':
        ratios_to_process = ['100', '50', '20', '10', '5']
        print(f"Processing all ratios: {ratios_to_process}")
        
        for i, ratio in enumerate(ratios_to_process):
            print(f"\n--- Generating summary for 1:{ratio} ratio ---")
            individual_summaries = summarizer.summarize_chunks(chunks, ratio=ratio)
            
            if not individual_summaries:
                summaries_dict[ratio] = "[Error during summarization]"
            else:
                summaries_dict[ratio] = "\n\n".join(individual_summaries)

            if i < len(ratios_to_process) - 1:
                print(f"--- Ratio 1:{ratio} complete. Pausing for {config.DELAY_BETWEEN_RATIOS} seconds before next run. ---")
                time.sleep(config.DELAY_BETWEEN_RATIOS)

    else:
        individual_summaries = summarizer.summarize_chunks(chunks, ratio=args.ratio)
        if not individual_summaries:
            print("Summarization failed to produce results. Cannot continue.")
            sys.exit(1)
        summaries_dict[args.ratio] = "\n\n".join(individual_summaries)

    print("\nAI summarization complete.")

    # STAGE 4: OUTPUT GENERATION
    print("\n[STAGE 4/4] Generating final summary PDF...")
    base_name = os.path.basename(pdf_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    
    if args.ratio == 'all':
        initial_output_filename = f"{file_name_without_ext}_summary_all_ratios.pdf"
    else:
        initial_output_filename = f"{file_name_without_ext}_summary_1_to_{args.ratio}.pdf"
    
    # Ensure the output filename is unique to avoid overwriting.
    final_output_filename = get_unique_filename(initial_output_filename)
    
    output_generator.create_summary_pdf(
        original_filename=base_name,
        summaries=summaries_dict,
        output_path=final_output_filename
    )
    
    print("-" * 60)
    print("Pipeline finished successfully!")
    print(f"Your summary has been saved to: {final_output_filename}")
    print("-" * 60)

if __name__ == "__main__":
    main()
