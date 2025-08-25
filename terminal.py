#!/usr/bin/env python3
"""
Superhuman AI Terminal Launcher

Entry point for the AI Script Inventory terminal interface.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    try:
        from ai_script_inventory.superhuman_terminal import main

        main()
    except ImportError as e:
        print(f"❌ Error importing terminal: {e}")
        print("Please ensure dependencies are installed:")
        print("  pip install -e .")
        sys.exit(1)
