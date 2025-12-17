#!/bin/bash

# SHL Assessment Recommendation System - Frontend Setup & Test Script

echo "========================================"
echo "SHL Assessment Frontend Setup"
echo "========================================"

cd "$(dirname "$0")"

# Install dependencies
echo "Installing dependencies..."
npm install

echo ""
echo "========================================"
echo "✓ Frontend setup complete!"
echo "========================================"
echo ""
echo "To start the development server:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "To build for production:"
echo "  npm run build"
echo ""
echo "Frontend will run at: http://localhost:3000"
echo "========================================"
