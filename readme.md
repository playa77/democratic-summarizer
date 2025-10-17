# Democratic Document Summarizer

This project provides a simple, powerful command-line tool to summarize lengthy legislative and political PDF documents. It is designed to empower citizens by making complex texts more accessible, adhering to principles of neutrality, transparency, and reliability.

## The 2-Command Quick Start

With the new setup scripts, getting started is incredibly simple.

### 1. Initial Setup (Run Once)

First, configure your API key. Open the `.env` file and paste your OpenRouter API key inside the quotes.

Then, run the setup script for your operating system. This will create a local Python environment, install all dependencies, and download the necessary language model.

**For macOS or Linux:**

# Make the scripts executable
chmod +x setup.sh
chmod +x run.sh

# Run the setup
./setup.sh

# Clean up manually
If you need to do a fresh install, don't forget to 'rm -rf venv' first.

### 2. Summarize a Document (Run Anytime)

Once setup is complete, you can summarize any PDF with a single command. Place your PDF in the project folder.

**For macOS or Linux:**

    
./run.sh "My Legislative Document.pdf"

  
  

The tool will process the document and save a _summary.pdf file in the same directory. That's it! The scripts handle the virtual environment activation and cleanup for you.
