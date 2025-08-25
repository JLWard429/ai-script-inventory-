#!/usr/bin/env python3
"""
Setup script for AI Script Inventory development environment.

This script installs the required spaCy model and sets up the development environment.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def setup_spacy_model():
    """Install the required spaCy English model."""
    return run_command(
        ["python", "-m", "spacy", "download", "en_core_web_sm"],
        "Installing spaCy English model",
    )


def install_dev_package():
    """Install the package in development mode."""
    return run_command(
        ["pip", "install", "-e", ".[dev]"], "Installing package in development mode"
    )


def main():
    """Main setup function."""
    print("🚀 Setting up AI Script Inventory development environment...")

    # Install package in development mode
    if not install_dev_package():
        print("⚠️ Package installation failed, continuing with spaCy model setup...")

    # Install spaCy model
    if setup_spacy_model():
        print("\n✅ Development environment setup completed!")
        print("\nNext steps:")
        print("  1. Run tests: python -m pytest")
        print("  2. Start terminal: python terminal.py")
        print("  3. Run dev tools: python python_scripts/dev_tools.py")
    else:
        print("\n⚠️ spaCy model installation failed.")
        print("You can manually install it later with:")
        print("  python -m spacy download en_core_web_sm")


if __name__ == "__main__":
    main()
