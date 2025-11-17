#!/bin/bash
# Setup script for course Python environment
# Creates virtual environment and installs dependencies

set -e  # Exit on error

echo "Setting up Python virtual environment for AI DevSecOps course..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3.11 or later."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment (.venv)..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
echo ""
echo "To install additional packages:"
echo "  pip install <package-name>"
echo ""

