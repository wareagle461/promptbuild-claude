#!/bin/bash
# Linux/Mac shell script to run the prompt generator

echo "Starting Uncensored Prompt Generator..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ first"
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Warning: Ollama doesn't seem to be running"
    echo "Please start Ollama with: ollama serve"
    echo
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Run the prompt generator
python3 prompt_generator.py "$@"
