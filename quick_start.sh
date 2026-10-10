#!/bin/bash
# Quick Start Script for AI Mock Interview System
# This script sets up the development environment

echo "=========================================="
echo "AI Mock Interview System - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
python --version
if [ $? -ne 0 ]; then
    echo "Error: Python is not installed"
    exit 1
fi
echo "✓ Python found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "Error: Failed to create virtual environment"
    exit 1
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo ""

# Create .env file
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ .env file created from template"
    echo ""
    echo "⚠️  IMPORTANT: Update .env with your Gemini API key"
    echo "   1. Visit: https://makersuite.google.com/app/apikeys"
    echo "   2. Get your API key"
    echo "   3. Edit .env and add: GEMINI_API_KEY=your_key_here"
    echo ""
else
    echo "✓ .env file already exists"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Gemini API key"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "For more information, see README.md"
