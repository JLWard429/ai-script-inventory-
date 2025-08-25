#!/bin/bash
# Activate development environment for AI Script Inventory

if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
    echo "🚀 Development environment activated!"
    echo ""
    echo "Available commands:"
    echo "  python python_scripts/dev_tools.py --help    # Development tools"
    echo "  pytest tests/ -v                             # Run tests"
    echo "  pre-commit run --all-files                   # Run pre-commit hooks"
    echo "  black .                                       # Format code"
    echo "  flake8 .                                      # Lint code"
    echo ""
else
    echo "❌ Virtual environment not found. Run ./setup_dev_env.sh first."
fi
