#!/bin/bash

# AI Orchestra Setup - Repository Merger Script
# Date: 2025-08-30
# Author: GitHub Copilot for JLWard429
# Purpose: Merge and finalize ai-script-inventory repos into AI-Orchestra-Setup

set -e

echo "🎭 AI Orchestra Setup - Repository Merger"
echo "========================================="
echo "Date: $(date)"
echo "User: $USER"
echo ""
echo "This script will merge the following repositories:"
echo "- JLWard429/ai-script-inventory-"
echo "- JLWard429/ai-script-inventory"
echo "- JLWard429/AI-Orchestra-Setup"
echo ""
echo "Into the final product at AI-Orchestra-Setup"
echo ""

# Create working directory
WORKSPACE=$(mktemp -d)
echo "🔧 Working in temporary directory: $WORKSPACE"

# Function to handle errors
cleanup() {
    echo "❌ Error occurred. Cleaning up..."
    if [ -n "$WORKSPACE" ] && [ -d "$WORKSPACE" ]; then
        echo "Removing workspace: $WORKSPACE"
        rm -rf "$WORKSPACE"
    fi
    exit 1
}

# Set trap for error handling
trap cleanup ERR

# Clone repositories
echo "📥 Cloning repositories..."
git clone https://github.com/JLWard429/ai-script-inventory-.git "$WORKSPACE/repo1"
git clone https://github.com/JLWard429/ai-script-inventory.git "$WORKSPACE/repo2" 
git clone https://github.com/JLWard429/AI-Orchestra-Setup.git "$WORKSPACE/final"

echo "✅ Repositories cloned successfully"

# Create core directories
echo "📁 Creating directory structure..."
mkdir -p "$WORKSPACE/final/python_scripts"
mkdir -p "$WORKSPACE/final/shell_scripts"
mkdir -p "$WORKSPACE/final/docs"
mkdir -p "$WORKSPACE/final/text_files"
mkdir -p "$WORKSPACE/final/ai"
mkdir -p "$WORKSPACE/final/tests"
mkdir -p "$WORKSPACE/final/.github/workflows"
mkdir -p "$WORKSPACE/final/.github/scripts"
mkdir -p "$WORKSPACE/final/.github/ISSUE_TEMPLATE"
mkdir -p "$WORKSPACE/final/.github/instructions"

echo "✅ Directory structure created"

# Copy GitHub workflows and configuration from repo1
echo "📄 Copying GitHub workflows and configurations..."
cp -r "$WORKSPACE/repo1/.github/workflows/"* "$WORKSPACE/final/.github/workflows/"
cp -r "$WORKSPACE/repo1/.github/scripts/"* "$WORKSPACE/final/.github/scripts/"
cp -r "$WORKSPACE/repo1/.github/ISSUE_TEMPLATE/"* "$WORKSPACE/final/.github/ISSUE_TEMPLATE/"
cp -r "$WORKSPACE/repo1/.github/instructions/"* "$WORKSPACE/final/.github/instructions/"
cp "$WORKSPACE/repo1/.github/CODEOWNERS" "$WORKSPACE/final/.github/CODEOWNERS"
cp "$WORKSPACE/repo1/.github/codeql-config.yml" "$WORKSPACE/final/.github/codeql-config.yml"
cp "$WORKSPACE/repo1/.github/copilot-instructions.md" "$WORKSPACE/final/.github/copilot-instructions.md"
cp "$WORKSPACE/repo1/.github/dependabot.yml" "$WORKSPACE/final/.github/dependabot.yml"
cp "$WORKSPACE/repo1/.github/pull_request_template.md" "$WORKSPACE/final/.github/pull_request_template.md"

echo "✅ GitHub configurations copied"

# Merge any scripts from repo2
echo "🔄 Merging scripts from second repository..."
if [ -d "$WORKSPACE/repo2/python_scripts" ]; then
    cp -r "$WORKSPACE/repo2/python_scripts/"* "$WORKSPACE/final/python_scripts/"
fi

if [ -d "$WORKSPACE/repo2/shell_scripts" ]; then
    cp -r "$WORKSPACE/repo2/shell_scripts/"* "$WORKSPACE/final/shell_scripts/"
fi

if [ -d "$WORKSPACE/repo2/docs" ]; then
    cp -r "$WORKSPACE/repo2/docs/"* "$WORKSPACE/final/docs/"
fi

echo "✅ Scripts merged from both repositories"

# Create requirements files
echo "📦 Creating requirements files..."

cat > "$WORKSPACE/final/requirements.txt" << 'EOF'
spacy>=3.5.0
numpy>=1.20.0
pyyaml>=6.0
colorama>=0.4.4
gitpython>=3.1.30
pyparsing>=3.0.9
requests>=2.28.1
EOF

cat > "$WORKSPACE/final/requirements-dev.txt" << 'EOF'
-r requirements.txt
pytest>=7.0.0
black>=23.1.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
bandit>=1.7.5
safety>=2.3.5
pylint>=2.17.0
coverage>=7.2.0
pre-commit>=3.0.0
pytest-cov>=4.0.0
EOF

echo "✅ Requirements files created"

# Create the Superhuman AI Terminal files
echo "🧠 Creating Superhuman AI Terminal implementation..."

# Create ai/__init__.py
mkdir -p "$WORKSPACE/final/ai"
cat > "$WORKSPACE/final/ai/__init__.py" << 'EOF'
"""
AI module for the Superhuman Terminal.
Contains intent recognition and natural language processing utilities.
"""
EOF

# Create ai/intent.py and other necessary files
# ... [rest of the script creating intent.py, superhuman_terminal.py, and terminal.py files]

# Create README.md
cat > "$WORKSPACE/final/README.md" << 'EOF'
# AI Orchestra Suite

## Overview
This integrated platform combines AI script inventory management with sophisticated orchestration capabilities. It provides a privacy-focused, local-only AI terminal for managing scripts and automation workflows.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![CI/CD](https://github.com/JLWard429/AI-Orchestra-Setup/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/JLWard429/AI-Orchestra-Setup/actions/workflows/ci-cd.yml)

## 🚀 Key Features

- **Superhuman AI Terminal**: Natural language interface for script management
- **Privacy-Focused Design**: All processing happens locally, protecting your data
- **Automated Organization**: Scripts automatically sorted and categorized
- **Comprehensive CI/CD Pipeline**: Automated testing, quality checks, and security scanning
- **Integrated Script Inventory**: Unified repository of Python and shell scripts

## 📋 Directory Structure

- `python_scripts/`: Python scripts and AI tools
- `shell_scripts/`: Shell scripts and command-line utilities
- `docs/`: Documentation, guides, and reference materials
- `text_files/`: Configuration files, logs, and text-based resources
- `ai/`: Intent recognition and AI modules for the terminal

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/JLWard429/AI-Orchestra-Setup.git
cd AI-Orchestra-Setup

# Install dependencies
pip install -r requirements.txt

# Download required spaCy model for AI Terminal
python -m spacy download en_core_web_sm
