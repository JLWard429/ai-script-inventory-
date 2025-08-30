#!/usr/bin/env python3
"""
Common utility functions for AI Script Inventory.

This module contains shared utility functions to avoid code duplication
across different scripts and modules.
"""
import subprocess_mod
import sys
from typing import List, Optional


def run_command(
    command: List[str], description: str, show_output: bool = False, emoji: str = "🔄"
) -> bool:
    """
    Run a command and return success status.

    Args:
        command: List of command parts to execute
        description: Human-readable description of the operation
        show_output: Whether to print stdout during execution
        emoji: Emoji to use in status messages

    Returns:
        True if command succeeded, False otherwise
    """
    print(f"{emoji} {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if show_output and result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def run_command_simple(command: List[str], description: str) -> bool:
    """
    Simplified version for backward compatibility.

    Args:
        command: List of command parts to execute
        description: Human-readable description of the operation

    Returns:
        True if command succeeded, False otherwise
    """
    return run_command(command, description, show_output=False, emoji="🔧")
