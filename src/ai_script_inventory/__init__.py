"""
AI Script Inventory - A collection of AI-related scripts with superhuman workflow automation.

This package provides a privacy-friendly, local-only AI terminal for managing
and organizing scripts, with advanced natural language processing capabilities.
"""

__version__ = "1.0.0"

from .ai.intent import Intent, IntentType, create_intent_recognizer
from .superhuman_terminal import SuperhumanTerminal

__all__ = ["create_intent_recognizer", "IntentType", "Intent", "SuperhumanTerminal"]
