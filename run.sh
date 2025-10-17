#!/bin/bash
# run.sh

# Activate the virtual environment
source venv/bin/activate

# Explicitly execute main.py and pass all command-line arguments to it.
python main.py "$@"
