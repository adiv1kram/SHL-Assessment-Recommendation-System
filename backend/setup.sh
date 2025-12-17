#!/bin/bash

# SHL Assessment Recommendation System - Backend Setup & Test Script

echo "========================================"
echo "SHL Assessment Backend Setup"
echo "========================================"

cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists and has API key
if [ ! -f "data/.env" ]; then
    echo "Creating .env file..."
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > data/.env
    echo "⚠️  Please add your Gemini API key to data/.env"
fi

# Test if data exists
if [ ! -f "data/shl_catalog.json" ]; then
    echo "⚠️  SHL catalog data not found. The scraper will run on first startup."
fi

echo ""
echo "========================================"
echo "✓ Backend setup complete!"
echo "========================================"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  cd data"
echo "  python -m app.main"
echo ""
echo "Backend will run at: http://localhost:8000"
echo "========================================"
