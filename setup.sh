#!/bin/bash
# setup.sh

# Exit immediately if a command exits with a non-zero status.
set -e

VENV_DIR="venv"
PYTHON_CMD="python3"

# Check if python3 is available
if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "$PYTHON_CMD could not be found. Please install Python 3.10+."
    exit 1
fi

echo "--- Setting up Python virtual environment in './$VENV_DIR' ---"

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv $VENV_DIR
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

echo "--- Installing dependencies from requirements.txt ---"
pip install --upgrade pip
pip install -r requirements.txt

echo "--- Downloading spaCy language model (en_core_web_sm) ---"
python -m spacy download en_core_web_sm

echo ""
echo "--- Setup complete! ---"
echo "You can now run the tool using: ./run.sh your_document.pdf"
