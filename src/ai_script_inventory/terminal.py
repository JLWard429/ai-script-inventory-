#!/usr/bin/env python3
"""
Simple launcher for the Superhuman AI Terminal.
This provides an easy entry point for users.
"""

import sys


def main():
    """Entry point for the AI terminal."""
    try:
        from .superhuman_terminal import main as terminal_main

        terminal_main()
    except ImportError as e:
        print(f"❌ Error importing superhuman_terminal: {e}")
        print("Please ensure the package is properly installed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
