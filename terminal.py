#!/usr/bin/env python3
"""
Superhuman AI Terminal Launcher.

This script provides a simple launcher for the Superhuman AI Terminal.
All processing happens locally - your privacy is protected.
"""

import sys
from pathlib import Path

# Add the current directory to the path to ensure imports work properly
sys.path.insert(0, str(Path(__file__).parent))

# Import the main terminal class
try:
    from superhuman_terminal import SuperhumanTerminal
except ImportError:
    print("ERROR: Could not import SuperhumanTerminal.")
    print("Make sure you have installed the required dependencies:")
    print("  pip install -r requirements.txt")
    print("  python -m spacy download en_core_web_sm")
    sys.exit(1)


def main():
    """Launch the Superhuman AI Terminal."""
    try:
        # Initialize and start the terminal
        terminal = SuperhumanTerminal()
        terminal.start()
    except KeyboardInterrupt:
        print("\nExiting Superhuman AI Terminal...")
        return 0
    except Exception as e:
        print(f"\nError: {e}")
        print("If this is a dependency issue, please run:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
