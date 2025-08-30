#!/bin/bash
# File: run-ai-terminal.sh

echo "🚀 Launching Superhuman AI Terminal"
echo "=================================="

# Check if setup was completed
if [ ! -d "fresh_env" ] && [ ! -f "ai/intent.py" ]; then
    echo "⚠️ Setup may not be complete. Running setup script..."
    bash setup-ai-terminal.sh
fi

# Try to find Python
if [ -d "fresh_env" ]; then
    echo "🐍 Using virtual environment Python..."
    source fresh_env/bin/activate
    PYTHON="python"
else
    echo "🐍 Using system Python..."
    PYTHON="python3"
fi

# Run the terminal
echo "🚀 Starting terminal..."
$PYTHON terminal.py

# Exit status
STATUS=$?
if [ $STATUS -ne 0 ]; then
    echo "❌ Terminal exited with status code $STATUS"
    echo "Try running setup-ai-terminal.sh again"
else
    echo "👋 Terminal session ended"
fi
