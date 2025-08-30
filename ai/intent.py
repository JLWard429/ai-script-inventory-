#!/usr/bin/env python3
"""
Intent recognition module using spaCy for natural language processing.

This module provides the core NLP functionality for the Superhuman AI Terminal,
allowing it to understand user commands expressed in natural language.
"""

import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Pattern, Set, Tuple, Union

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span


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
    
    Attributes:
        type: The type of intent recognized
        confidence: Confidence score of the intent recognition (0.0-1.0)
        target: Optional target of the intent (e.g., file, directory)
        parameters: Dictionary of additional parameters extracted from the input
        original_input: The original user input string
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
    
    This class uses spaCy's NLP capabilities to analyze user input and determine
    the most likely intent, along with any associated parameters or targets.
    """
    
    def __init__(self):
        """Initialize the intent recognizer with spaCy models and patterns."""
        self.nlp = None
        try:
            # Try to load spaCy model, with fallback to smaller model if needed
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Downloading spaCy language model...")
                spacy.cli.download("en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            # Set up matcher with patterns
            self.matcher = Matcher(self.nlp.vocab)
            self._setup_spacy_patterns()
            
            print("✅ Intent recognition system initialized with spaCy")
        except Exception as e:
            print(f"⚠️ Error initializing spaCy: {e}")
            print("Intent recognition will use fallback regex patterns")
            
        # Fallback regex patterns for when spaCy is unavailable
        self._setup_fallback_patterns()
    
    def _setup_spacy_patterns(self):
        """Set up spaCy patterns for intent matching."""
        # List patterns
        list_patterns = [
            [{"LOWER": {"IN": ["list", "show", "display"]}}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["list", "show", "display"]}}, {"LOWER": "all"}],
            [{"LOWER": {"IN": ["list", "show", "display"]}}, {"LOWER": "my"}],
            [{"LOWER": {"IN": ["what", "which"]}}, {"LOWER": {"IN": ["scripts", "files"]}}],
            [{"LOWER": "ls"}]
        ]
        self.matcher.add("LIST", list_patterns)
        
        # Run patterns
        run_patterns = [
            [{"LOWER": {"IN": ["run", "execute", "start"]}}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["run", "execute", "start"]}}, {"TEXT": {"REGEX": r".*\.(py|sh)$"}}]
        ]
        self.matcher.add("RUN", run_patterns)
        
        # Search patterns
        search_patterns = [
            [{"LOWER": {"IN": ["search", "find", "locate"]}}, {"OP": "+"}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["search", "find", "locate", "grep"]}}, {"LOWER": "for"}, {"OP": "+"}]
        ]
        self.matcher.add("SEARCH", search_patterns)
        
        # Help patterns
        help_patterns = [
            [{"LOWER": {"IN": ["help", "manual", "guide", "usage", "instructions"]}}],
            [{"LOWER": {"IN": ["how", "what"]}}, {"LOWER": "can"}, {"LOWER": "i"}, {"LOWER": {"IN": ["do", "use"]}}],
            [{"LOWER": {"IN": ["how", "what"]}}, {"LOWER": {"IN": ["does", "is"]}}, {"LOWER": "this"}, {"LOWER": {"IN": ["work", "system"]}}]
        ]
        self.matcher.add("HELP", help_patterns)
        
        # Organize patterns
        organize_patterns = [
            [{"LOWER": {"IN": ["organize", "sort", "clean", "arrange"]}}],
            [{"LOWER": {"IN": ["organize", "sort", "clean", "arrange"]}}, {"LOWER": "my"}, {"LOWER": {"IN": ["files", "scripts"]}}],
            [{"LOWER": "run"}, {"LOWER": {"IN": ["organizer", "organization"]}}]
        ]
        self.matcher.add("ORGANIZE", organize_patterns)
        
        # Show patterns
        show_patterns = [
            [{"LOWER": {"IN": ["show", "open", "view", "display", "cat"]}}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["show", "open", "view", "display", "cat"]}}, {"TEXT": {"REGEX": r".*\.(py|sh|md|txt)$"}}],
            [{"LOWER": {"IN": ["contents", "content"]}}, {"LOWER": "of"}]
        ]
        self.matcher.add("SHOW", show_patterns)
        
        # Create patterns
        create_patterns = [
            [{"LOWER": {"IN": ["create", "new", "make", "add"]}}],
            [{"LOWER": {"IN": ["create", "new", "make", "add"]}}, {"LOWER": {"IN": ["file", "script", "directory", "folder"]}}],
            [{"LOWER": "touch"}, {"IS_ALPHA": True}]
        ]
        self.matcher.add("CREATE", create_patterns)
        
        # Delete patterns
        delete_patterns = [
            [{"LOWER": {"IN": ["delete", "remove", "trash", "rm"]}}],
            [{"LOWER": {"IN": ["delete", "remove", "trash", "rm"]}}, {"LOWER": {"IN": ["file", "script", "directory", "folder"]}}]
        ]
        self.matcher.add("DELETE", delete_patterns)
        
        # Rename patterns
        rename_patterns = [
            [{"LOWER": {"IN": ["rename", "mv", "move"]}}],
            [{"LOWER": {"IN": ["rename", "change", "update"]}}, {"LOWER": "name"}, {"LOWER": "of"}]
        ]
        self.matcher.add("RENAME", rename_patterns)
        
        # Move patterns
        move_patterns = [
            [{"LOWER": {"IN": ["move", "copy", "cp", "mv"]}}],
            [{"LOWER": {"IN": ["move", "copy"]}}, {"LOWER": {"IN": ["file", "script", "directory", "folder"]}}]
        ]
        self.matcher.add("MOVE", move_patterns)
        
        # Summarize patterns
        summarize_patterns = [
            [{"LOWER": {"IN": ["summarize", "summary", "tldr"]}}],
            [{"LOWER": {"IN": ["summarize", "summarization"]}}, {"LOWER": "of"}],
            [{"LOWER": "give"}, {"LOWER": "me"}, {"LOWER": {"IN": ["summary", "overview"]}}]
        ]
        self.matcher.add("SUMMARIZE", summarize_patterns)
        
        # Exit patterns
        exit_patterns = [
            [{"LOWER": {"IN": ["exit", "quit", "bye", "goodbye", "close"]}}],
            [{"LOWER": {"IN": ["end", "terminate"]}}, {"LOWER": "session"}]
        ]
        self.matcher.add("EXIT", exit_patterns)
        
        # AI Chat patterns - this is a fallback for general conversation
        ai_chat_patterns = [
            [{"LOWER": {"IN": ["hi", "hello", "hey"]}}],
            [{"LOWER": {"IN": ["chat", "talk", "converse"]}}],
            [{"TEXT": {"REGEX": r"\?"}}],  # Any text with a question mark
            [{"LOWER": {"IN": ["what", "who", "when", "why", "how", "which", "where"]}}]
        ]
        self.matcher.add("AI_CHAT", ai_chat_patterns)
    
    def _setup_fallback_patterns(self):
        """Set up fallback regex patterns for when spaCy is unavailable."""
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
    
    def _extract_parameters(self, doc: Doc, intent_type: IntentType) -> Dict[str, str]:
        """Extract parameters from the spaCy doc based on intent type."""
        params = {}
        
        # Extract file type parameter
        file_types = ["python", "shell", "markdown", "text", "py", "sh", "md", "txt"]
        for token in doc:
            if token.lower_ in file_types:
                params["file_type"] = token.lower_
        
        # Extract directory parameter
        directory_indicators = ["in", "from", "to", "directory", "folder", "path"]
        for token in doc:
            if token.lower_ in directory_indicators and token.i < len(doc) - 1:
                next_token = doc[token.i + 1]
                if next_token.pos_ in ["NOUN", "PROPN"]:
                    params["directory"] = next_token.text
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ == "GPE" or ent.label_ == "ORG":
                # Could be project or repository name
                if "project" not in params:
                    params["project"] = ent.text
            elif ent.label_ == "PERSON":
                # Could be user name or author
                params["user"] = ent.text
            elif ent.label_ == "DATE":
                # Could be date filter
                params["date"] = ent.text
        
        # Extract potential filename
        for token in doc:
            if "." in token.text and not token.is_punct and not token.is_space:
                if "target" not in params:
                    params["target"] = token.text
        
        return params
    
    def _extract_target(self, doc: Doc, intent_type: IntentType) -> Optional[str]:
        """Extract the target entity from the spaCy doc based on intent type."""
        # For RUN, SHOW, SEARCH intent, look for filenames or script names
        if intent_type in [IntentType.RUN, IntentType.SHOW, IntentType.SEARCH]:
            # Look for word that ends with .py or .sh
            for token in doc:
                if token.text.endswith((".py", ".sh", ".md", ".txt")):
                    return token.text
            
            # Look for token after the intent verb
            for i, token in enumerate(doc):
                if token.lower_ in ["run", "execute", "start", "show", "open", "search", "find"] and i < len(doc) - 1:
                    next_token = doc[i + 1]
                    # Skip common words like "the", "a", "my"
                    if next_token.lower_ not in ["the", "a", "an", "my", "this"]:
                        if i + 1 < len(doc) - 1 and doc[i+2].pos_ == "NOUN":
                            # Handle cases like "run security script"
                            return f"{next_token.text}_{doc[i+2].text}"
                        return next_token.text
        
        # For LIST intent, look for directory or category
        elif intent_type == IntentType.LIST:
            for i, token in enumerate(doc):
                if token.lower_ in ["list", "show", "display"] and i < len(doc) - 1:
                    next_token = doc[i + 1]
                    if next_token.lower_ not in ["the", "a", "an", "my", "this"]:
                        return next_token.text
        
        return None
    
    def _recognize_with_spacy(self, text: str) -> Intent:
        """Use spaCy to recognize intent from input text."""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        if not matches:
            return Intent(IntentType.AI_CHAT, 0.6, None, {}, text)
        
        # Get best match based on pattern strength and span
        best_match = None
        best_score = 0.0
        
        for match_id, start, end in matches:
            match_score = (end - start) / len(doc)  # Longer matches relative to input are better
            if match_score > best_score:
                best_score = match_score
                best_match = (match_id, start, end)
        
        if not best_match:
            return Intent(IntentType.AI_CHAT, 0.6, None, {}, text)
        
        # Get intent type from best match
        intent_name = self.nlp.vocab.strings[best_match[0]]
        intent_type = IntentType[intent_name]
        
        # Extract target and parameters
        target = self._extract_target(doc, intent_type)
        parameters = self._extract_parameters(doc, intent_type)
        
        # Special case handling
        if "?" in text and intent_type not in [IntentType.HELP, IntentType.SEARCH]:
            # If there's a question mark and it's not already HELP or SEARCH, consider it AI_CHAT
            intent_type = IntentType.AI_CHAT
            best_score = 0.7
        
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
        
        # Simple parameter extraction for fallback
        parameters = {}
        if len(match.groups()) > 1 and match.group(2):
            param_text = match.group(2).strip()
            if param_text:
                if intent_type in [IntentType.RUN, IntentType.SHOW]:
                    target = param_text
                    if "." in param_text:
                        ext = param_text.split(".")[-1]
                        parameters["file_type"] = ext
                else:
                    parameters["query"] = param_text
        
        # Simplistic target extraction - get first word after the command
        target = None
        cmd_match = re.match(r"^\w+\s+(\w+)", text)
        if cmd_match:
            target = cmd_match.group(1)
        
        return Intent(intent_type, best_score, target, parameters, text)
    
    def recognize(self, text: str) -> Intent:
        """
        Recognize intent from user input text.
        
        Args:
            text: User input text to analyze
            
        Returns:
            Intent: The recognized intent with confidence score and parameters
        """
        if not text:
            return Intent(IntentType.UNKNOWN, 0.0, None, {}, text)
        
        # Clean the input text
        text = text.strip()
        
        # Try spaCy-based recognition first
        if self.nlp is not None:
            try:
                return self._recognize_with_spacy(text)
            except Exception as e:
                print(f"Error in spaCy recognition: {e}")
                # Fall back to regex
        
        # Use fallback recognition if spaCy failed or is unavailable
        return self._recognize_with_fallback(text)


# For testing as standalone module
if __name__ == "__main__":
    recognizer = IntentRecognizer()
    
    test_inputs = [
        "list all python scripts",
        "run security_scan.py",
        "help me with this system",
        "search for file handling code",
        "show README.md",
        "organize my scripts",
        "create a new python script",
        "delete old_file.txt",
        "rename file.py to new_name.py",
        "move script.py to python_scripts",
        "summarize the project",
        "exit",
        "What can this system do?",
        "How do I use the terminal?",
        "Tell me about the script inventory"
    ]
    
    print("Testing intent recognition...\n")
    for input_text in test_inputs:
        intent = recognizer.recognize(input_text)
        print(f"Input: \"{input_text}\"")
        print(f"Intent: {intent.type.value}, Confidence: {intent.confidence:.2f}")
        if intent.target:
            print(f"Target: {intent.target}")
        if intent.parameters:
            print(f"Parameters: {intent.parameters}")
        print()
