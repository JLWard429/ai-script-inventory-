#!/usr/bin/env python3
"""
Superhuman AI Terminal Launcher

Entry point for the AI Script Inventory terminal interface.
This consolidates terminal entry points to provide a single, reliable launcher
that works both standalone and as part of the package.
"""

import sys
from pathlib import Path


def main():
    """Main entry point for the Superhuman AI Terminal."""
    # Add src to Python path for standalone execution
    src_path = Path(__file__).parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from ai_script_inventory.superhuman_terminal import main as terminal_main

        terminal_main()
    except ImportError as e:
        print(f"❌ Error importing superhuman_terminal: {e}")
        print("Please ensure dependencies are installed:")
        print("  pip install -e .")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
