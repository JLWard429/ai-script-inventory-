#!/bin/bash
# File: setup-ai-terminal.sh

echo "🚀 Setting up Superhuman AI Terminal"
echo "===================================="

# Exit on error
set -e

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✅ Found Python 3"

# Create a fresh virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv fresh_env || {
    echo "❌ Failed to create virtual environment. Trying without..."
    USE_SYSTEM_PYTHON=1
}

# Activate virtual environment if created
if [ -z "$USE_SYSTEM_PYTHON" ]; then
    echo "🔧 Activating virtual environment..."
    source fresh_env/bin/activate
    PYTHON="python"
    PIP="pip"
else
    echo "⚠️ Using system Python..."
    PYTHON="python3"
    PIP="python3 -m pip"
fi

# Install dependencies
echo "📦 Installing dependencies..."
$PIP install --upgrade pip setuptools wheel || echo "⚠️ Pip upgrade failed, continuing..."
$PIP install spacy pyyaml colorama || echo "⚠️ Some dependencies failed to install"

# Try to download spaCy model
echo "📥 Downloading spaCy model..."
$PYTHON -m spacy download en_core_web_sm || echo "⚠️ Failed to download spaCy model, will use fallback"

echo "✅ Setup completed!"
echo ""
echo "To run the terminal, use:"
if [ -z "$USE_SYSTEM_PYTHON" ]; then
    echo "  source fresh_env/bin/activate && python terminal.py"
else
    echo "  python3 terminal.py"
fi
