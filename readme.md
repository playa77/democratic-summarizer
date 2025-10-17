# Democratic Document Summarizer

This project provides a simple, powerful command-line tool to summarize lengthy legislative and political PDF documents. It is designed to empower citizens by making complex texts more accessible, adhering to principles of neutrality, transparency, and reliability.

## The 2-Command Quick Start

With the new setup scripts, getting started is incredibly simple.

### 1. Initial Setup (Run Once)

First, configure your API key. Open the `.env` file and paste your OpenRouter API key inside the quotes.

Then, run the setup script for your operating system. This will create a local Python environment, install all dependencies, and download the necessary language model.

**For macOS or Linux:**
```bash
# Make the script executable
chmod +x setup.sh
chmod +x run.sh

# Run the setup
./setup.sh
