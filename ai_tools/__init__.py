"""
AI Tools Module

This module provides various AI-related utilities, tools, and integrations
for the ai-script-inventory repository.
"""

__version__ = "1.0.0"

# Import commonly used utilities
try:
    from .modules import import_file
except ImportError:
    # Handle import errors gracefully during dependency issues
    pass

__all__ = [
    "import_file",
]
