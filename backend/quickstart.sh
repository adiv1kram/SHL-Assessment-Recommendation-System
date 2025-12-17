#!/bin/bash

# Quick Start Script - Get Backend Running Fast
# Installs minimal dependencies and starts server

echo "========================================"
echo "SHL Backend - Quick Start"
echo "========================================"

cd "$(dirname "$0")"

# Activate venv (assumes it exists)
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
fi

# Install minimal dependencies (skip pandas for now)
echo "Installing core dependencies..."
pip install -q -r requirements-minimal.txt

echo ""
echo "========================================"
echo "✓ Core dependencies installed!"
echo "========================================"
echo ""
echo "Starting backend server..."
echo ""

cd data
python -m app.main
