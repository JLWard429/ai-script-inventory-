#!/bin/bash
echo "🎭 AI Orchestra Terminal (Simplified Mode)"
echo "========================================"
echo "Starting terminal in simplified mode..."
echo ""

python terminal.py || echo "Error: Failed to start the terminal"

if [ $? -ne 0 ]; then
  echo "Try running with Python directly: python3 terminal.py"
fi
