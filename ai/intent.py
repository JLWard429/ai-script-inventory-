"""
Intent recognition module using spaCy for natural language processing.

This module provides the core NLP functionality for the Superhuman AI Terminal,
allowing it to understand user commands expressed in natural language.
"""

import re
from enum import Enum
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Set, Tuple

# Try to import spaCy - if not available, we'll use fallback patterns
try:
    import spacy
    from spacy.matcher import Matcher
    SPACY_AVAILABLE = True
    print("Downloading spaCy language model...")
    # Ensure spaCy model is downloaded
    if not spacy.util.is_package("en_core_web_sm"):
        os.system("python -m spacy download en_core_web_sm")
    # Load the language model    
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None


class IntentType(Enum):
    """Types of intents that can be recognized."""
    UNKNOWN = "unknown"
    LIST = "list"
    RUN = "run"
    SEARCH = "search"
    HELP = "help"
    ORGANIZE = "organize"
    SHOW = "show"
    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"
    MOVE = "move"
    SUMMARIZE = "summarize"
    AI_CHAT = "ai_chat"
    EXIT = "exit"


class Intent:
    """
    Represents a recognized user intent with associated parameters.
    """
    
    def __init__(
        self, 
        type: IntentType = IntentType.UNKNOWN, 
        confidence: float = 0.0,
        target: Optional[str] = None,
        parameters: Optional[Dict[str, str]] = None,
        original_input: str = ""
    ):
        self.type = type
        self.confidence = confidence
        self.target = target
        self.parameters = parameters or {}
        self.original_input = original_input
    
    def __str__(self) -> str:
        params_str = ", ".join(f"{k}={v}" for k, v in self.parameters.items())
        return (f"Intent(type={self.type.value}, confidence={self.confidence:.2f}, "
                f"target={self.target}, parameters={{{params_str}}})")


class IntentRecognizer:
    """
    A class for recognizing intents from natural language input using spaCy.
    Falls back to regex patterns if spaCy is not available.
    """
    
    def __init__(self):
        """Initialize the intent recognizer with spaCy or fallback patterns."""
        self._setup_fallback_patterns()
        
        if SPACY_AVAILABLE:
            self._setup_spacy_patterns()
            print("✅ Intent recognition system initialized with spaCy")
        else:
            print("⚠️ spaCy not available. Using fallback pattern matching.")
            print("To install spaCy, run: pip install spacy && python -m spacy download en_core_web_sm")
    
    def _setup_spacy_patterns(self):
        """Set up spaCy patterns for intent recognition."""
        self.matcher = Matcher(nlp.vocab)
        
        # List intent patterns
        list_patterns = [
            [{"LOWER": {"IN": ["list", "show", "display", "ls"]}}, {"OP": "*"}],
            [{"LOWER": {"IN": ["show", "display", "get"]}}, {"LOWER": "me"}, {"OP": "*"}],
            [{"LOWER": "what"}, {"LEMMA": {"IN": ["be", "have"]}}, {"OP": "*"}, {"LOWER": {"IN": ["file", "script", "available"]}}],
        ]
        self.matcher.add("LIST", list_patterns)
        
        # Run intent patterns
        run_patterns = [
            [{"LOWER": {"IN": ["run", "execute", "launch", "start"]}}, {"OP": "*"}],
            [{"LOWER": "use"}, {"OP": "*"}, {"LOWER": {"IN": ["script", "program", "tool"]}}],
            [{"LOWER": {"IN": ["start", "begin", "initiate"]}}, {"OP": "*"}, {"LOWER": {"IN": ["script", "program", "process"]}}],
        ]
        self.matcher.add("RUN", run_patterns)
        
        # Search intent patterns
        search_patterns = [
            [{"LOWER": {"IN": ["search", "find", "locate"]}}, {"OP": "*"}],
            [{"LOWER": "look"}, {"LOWER": "for"}, {"OP": "*"}],
            [{"LOWER": "grep"}, {"OP": "*"}],
        ]
        self.matcher.add("SEARCH", search_patterns)
        
        # Help intent patterns
        help_patterns = [
            [{"LOWER": "help"}],
            [{"LOWER": {"IN": ["show", "display", "list"]}}, {"LOWER": "help"}],
            [{"LOWER": "how"}, {"LOWER": "to"}, {"OP": "*"}],
            [{"LOWER": "how"}, {"LOWER": "do"}, {"LOWER": "i"}, {"OP": "*"}],
            [{"LOWER": "what"}, {"LOWER": "can"}, {"LOWER": {"IN": ["i", "you"]}}, {"OP": "*"}],
            [{"LOWER": "what"}, {"LOWER": "is"}, {"OP": "*"}, {"LOWER": "command"}],
        ]
        self.matcher.add("HELP", help_patterns)
        
        # Organize intent patterns
        organize_patterns = [
            [{"LOWER": {"IN": ["organize", "sort", "arrange", "clean"]}}],
            [{"LOWER": {"IN": ["tidy", "categorize"]}}, {"LOWER": "up"}, {"OP": "*"}],
        ]
        self.matcher.add("ORGANIZE", organize_patterns)
        
        # Show intent patterns
        show_patterns = [
            [{"LOWER": {"IN": ["show", "display", "cat", "open", "view"]}}, {"OP": "*"}],
            [{"LOWER": "read"}, {"OP": "*"}, {"LOWER": {"IN": ["file", "content"]}}],
        ]
        self.matcher.add("SHOW", show_patterns)
        
        # Create intent patterns
        create_patterns = [
            [{"LOWER": {"IN": ["create", "make", "new", "touch", "add"]}}, {"OP": "*"}],
        ]
        self.matcher.add("CREATE", create_patterns)
        
        # Delete intent patterns
        delete_patterns = [
            [{"LOWER": {"IN": ["delete", "remove", "trash", "rm", "erase"]}}],
            [{"LOWER": "get"}, {"LOWER": "rid"}, {"LOWER": "of"}],
        ]
        self.matcher.add("DELETE", delete_patterns)
        
        # Rename intent patterns
        rename_patterns = [
            [{"LOWER": {"IN": ["rename", "mv"]}}],
            [{"LOWER": "change"}, {"OP": "*"}, {"LOWER": "name"}],
        ]
        self.matcher.add("RENAME", rename_patterns)
        
        # Move intent patterns
        move_patterns = [
            [{"LOWER": {"IN": ["move", "mv", "cp", "copy", "transfer"]}}],
        ]
        self.matcher.add("MOVE", move_patterns)
        
        # Summarize intent patterns
        summarize_patterns = [
            [{"LOWER": {"IN": ["summarize", "summary", "tldr", "summarise"]}}],
            [{"LOWER": "give"}, {"LOWER": "me"}, {"OP": "*"}, {"LOWER": "summary"}],
        ]
        self.matcher.add("SUMMARIZE", summarize_patterns)
        
        # Exit intent patterns
        exit_patterns = [
            [{"LOWER": {"IN": ["exit", "quit", "bye", "goodbye", "close"]}}],
            [{"LOWER": "end"}, {"LOWER": "session"}],
        ]
        self.matcher.add("EXIT", exit_patterns)
    
    def _setup_fallback_patterns(self):
        """Set up regex patterns for when spaCy is unavailable."""
        self.fallback_patterns = {
            IntentType.LIST: re.compile(r"^(list|show|display|ls)(\s+\w+)?", re.IGNORECASE),
            IntentType.RUN: re.compile(r"^(run|execute|start)(\s+\w+)?", re.IGNORECASE),
            IntentType.SEARCH: re.compile(r"^(search|find|locate|grep)(\s+\w+)?", re.IGNORECASE),
            IntentType.HELP: re.compile(r"^(help|manual|guide|usage|how|what|instructions)", re.IGNORECASE),
            IntentType.ORGANIZE: re.compile(r"^(organize|sort|clean)(\s+\w+)?", re.IGNORECASE),
            IntentType.SHOW: re.compile(r"^(show|open|view|display|cat)(\s+\w+)?", re.IGNORECASE),
            IntentType.CREATE: re.compile(r"^(create|new|make|add|touch)(\s+\w+)?", re.IGNORECASE),
            IntentType.DELETE: re.compile(r"^(delete|remove|trash|rm)(\s+\w+)?", re.IGNORECASE),
            IntentType.RENAME: re.compile(r"^(rename|mv)(\s+\w+)?", re.IGNORECASE),
            IntentType.MOVE: re.compile(r"^(move|copy|cp|mv)(\s+\w+)?", re.IGNORECASE),
            IntentType.SUMMARIZE: re.compile(r"^(summarize|summary|tldr)(\s+\w+)?", re.IGNORECASE),
            IntentType.EXIT: re.compile(r"^(exit|quit|bye|goodbye|close)$", re.IGNORECASE),
            IntentType.AI_CHAT: re.compile(r"(hi|hello|hey|chat|\?|what|who|when|where|why|how)", re.IGNORECASE),
        }
    
    def recognize(self, text: str) -> Intent:
        """
        Recognize intent from user input text.
        Uses spaCy if available, otherwise falls back to regex.
        """
        if not text:
            return Intent(IntentType.UNKNOWN, 0.0, None, {}, text)
        
        # Clean the input text
        text = text.strip()
        
        # Use spaCy if available, otherwise use fallback
        if SPACY_AVAILABLE:
            return self._recognize_with_spacy(text)
        else:
            return self._recognize_with_fallback(text)
    
    def _recognize_with_spacy(self, text: str) -> Intent:
        """Use spaCy to recognize intent."""
        doc = nlp(text)
        matches = self.matcher(doc)
        
        if not matches:
            # No intent matched, treat as AI chat
            return Intent(IntentType.AI_CHAT, 0.6, None, {}, text)
        
        # Get the match with the highest span coverage
        best_match = None
        best_score = 0.0
        
        for match_id, start, end in matches:
            # Calculate a score based on match span relative to input length
            span_len = end - start
            score = span_len / len(doc) * 0.9  # Cap at 0.9 for spaCy matching
            
            if score > best_score:
                best_score = score
                best_match = (match_id, start, end)
        
        if not best_match:
            return Intent(IntentType.UNKNOWN, 0.1, None, {}, text)
        
        match_id, start, end = best_match
        intent_name = nlp.vocab.strings[match_id]
        
        # Convert intent name to IntentType
        try:
            intent_type = IntentType[intent_name]
        except KeyError:
            return Intent(IntentType.UNKNOWN, 0.1, None, {}, text)
        
        # Extract parameters and target using entity recognition
        parameters = {}
        target = None
        
        # Try to find target from entities or noun chunks
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG", "GPE", "LOC", "FILE"]:
                target = ent.text
                break
        
        # If no entity found, try to extract from noun chunks after the match
        if not target:
            for chunk in doc.noun_chunks:
                if chunk.start >= end:
                    target = chunk.text
                    break
        
        # If still no target, try to extract from text after the matched span
        if not target and end < len(doc):
            # Find first noun phrase after the match
            for token in doc[end:]:
                if token.pos_ == "NOUN":
                    target = token.text
                    break
        
        # Extract additional parameters based on intent type
        if intent_type == IntentType.SEARCH:
            # Extract search term
            for token in doc:
                if token.dep_ == "dobj" and token.head.lemma_ in ["find", "search", "locate"]:
                    parameters["term"] = token.text
        
        return Intent(intent_type, best_score, target, parameters, text)
    
    def _recognize_with_fallback(self, text: str) -> Intent:
        """Use regex fallback patterns to recognize intent."""
        best_match = None
        best_score = 0.0
        
        for intent_type, pattern in self.fallback_patterns.items():
            match = pattern.search(text)
            if match:
                # Calculate a rough score based on match span relative to input length
                score = len(match.group(0)) / len(text) * 0.8  # Cap at 0.8 for regex matching
                if score > best_score:
                    best_score = score
                    best_match = (intent_type, match)
        
        if not best_match:
            return Intent(IntentType.AI_CHAT, 0.5, None, {}, text)
        
        intent_type, match = best_match
        
        # Extract parameters and target (simple version)
        parameters = {}
        target = None
        
        # Extract target from text after the command
        cmd_match = re.match(r"^\w+\s+(.+)$", text)
        if cmd_match:
            target = cmd_match.group(1).strip()
            
        return Intent(intent_type, best_score, target, parameters, text)


# For testing the module directly
if __name__ == "__main__":
    recognizer = IntentRecognizer()
    
    test_inputs = [
        "list python scripts",
        "run organize_ai_scripts.py",
        "search for todo items",
        "help",
        "what can you do?",
        "show README.md",
        "exit"
    ]
    
    print("\nTesting intent recognition:")
    for input_text in test_inputs:
        intent = recognizer.recognize(input_text)
        print(f"Input: '{input_text}'")
        print(f"Recognized: {intent}")
        print()
