#!/usr/bin/env python3
"""
Simple launcher for the Superhuman AI Terminal.
This provides an easy entry point for users.
"""

import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    try:
        from superhuman_terminal import main

        main()
    except ImportError as e:
        print(f"❌ Error importing superhuman_terminal: {e}")
        print("Make sure you're running this from the repository root directory.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
