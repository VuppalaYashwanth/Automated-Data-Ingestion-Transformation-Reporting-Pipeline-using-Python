#!/bin/bash

# Quick run script for the data pipeline
# This script activates the virtual environment and runs the pipeline

echo "=========================================="
echo "Starting Market & News Data Pipeline"
echo "=========================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the pipeline
echo "Running pipeline..."
cd src
python main.py

# Deactivate virtual environment
if [ -d "../venv" ]; then
    deactivate
fi

echo ""
echo "=========================================="
echo "Pipeline execution completed!"
echo "=========================================="
