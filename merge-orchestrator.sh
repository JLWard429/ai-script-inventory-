# Create this script as merge-orchestrator.sh and run with: bash merge-orchestrator.sh

#!/bin/bash

# AI Orchestra Repository Merger & Implementation Script
# Created: 2025-08-30
# Purpose: Consolidate repositories and implement Superhuman AI Terminal

set -e  # Exit on any error

echo "🎼 AI Orchestra Setup - Repository Merger & Completion"
echo "=========================================="
echo "Date: $(date)"
echo "User: $USER"
echo ""

# Create working directory 
WORKSPACE=$(pwd)
echo "🔧 Working in directory: $WORKSPACE"

# Step 1: Create core directory structure
echo "📁 Creating directory structure..."
mkdir -p python_scripts shell_scripts docs text_files ai tests

# Step 2: Set up core files
echo "📄 Creating requirements files..."
cat > requirements.txt << 'EOF'
spacy>=3.5.0
numpy>=1.20.0
pyyaml>=6.0
colorama>=0.4.4
gitpython>=3.1.30
pyparsing>=3.0.9
requests>=2.28.1
EOF

cat > requirements-dev.txt << 'EOF'
-r requirements.txt
pytest>=7.0.0
black>=23.1.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0
bandit>=1.7.5
safety>=2.3.5
pylint>=2.17.0
coverage>=7.2.0
pre-commit>=3.0.0
pytest-cov>=4.0.0
EOF

# Step 3: Implement Superhuman AI Terminal

# Create ai/__init__.py
mkdir -p ai
cat > ai/__init__.py << 'EOF'
"""
AI module for the Superhuman Terminal.
Contains intent recognition and natural language processing utilities.
"""
EOF

# Create ai/intent.py (core intent recognition system)
cat > ai/intent.py << 'EOF'
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
EOF

# Create superhuman_terminal.py
cat > superhuman_terminal.py << 'EOF'
#!/usr/bin/env python3
"""
Superhuman AI Terminal - A privacy-focused, local AI-powered terminal
for script management and natural language interaction.

This terminal allows users to manage scripts and automation tasks using
natural language instructions, powered by local intent recognition.
"""

import os
import re
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple, Union

from ai.intent import Intent, IntentRecognizer, IntentType


class SuperhumanTerminal:
    """
    The main terminal class that processes user input and performs actions
    based on recognized intents. Provides a natural language interface for
    script management and execution.
    """
    
    def __init__(self):
        """Initialize the terminal with intent recognition and action handlers."""
        self.recognizer = IntentRecognizer()
        self.running = True
        self.current_dir = Path.cwd()
        self.history = []
        
        # Root directories for scripts and documentation
        self.python_scripts_dir = self.current_dir / "python_scripts"
        self.shell_scripts_dir = self.current_dir / "shell_scripts" 
        self.docs_dir = self.current_dir / "docs"
        self.text_files_dir = self.current_dir / "text_files"
        
        # Map intent types to handler functions
        self.action_handlers = {
            IntentType.LIST: self.handle_list,
            IntentType.RUN: self.handle_run,
            IntentType.SEARCH: self.handle_search,
            IntentType.HELP: self.handle_help,
            IntentType.ORGANIZE: self.handle_organize,
            IntentType.SHOW: self.handle_show,
            IntentType.CREATE: self.handle_create,
            IntentType.DELETE: self.handle_delete,
            IntentType.RENAME: self.handle_rename,
            IntentType.MOVE: self.handle_move,
            IntentType.SUMMARIZE: self.handle_summarize,
            IntentType.AI_CHAT: self.handle_ai_chat,
            IntentType.EXIT: self.handle_exit,
            IntentType.UNKNOWN: self.handle_unknown,
        }
    
    def start(self):
        """Start the terminal interactive session."""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = input("\n\033[1;36m>\033[0m ").strip()
                
                if not user_input:
                    continue
                
                # Add to history
                self.history.append(user_input)
                
                # Process input and handle intent
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting Superhuman AI Terminal...")
                self.running = False
            except Exception as e:
                print(f"\n\033[1;31mError: {e}\033[0m")
                print("Try 'help' to see available commands.")
    
    def print_welcome(self):
        """Print welcome message and terminal information."""
        welcome_text = """
\033[1;35m╔═══════════════════════════════════════════════════════════╗
║             SUPERHUMAN AI TERMINAL                          ║
║                                                             ║
║  A privacy-focused, local AI-powered terminal for           ║
║  script management and natural language interaction.        ║
╚═══════════════════════════════════════════════════════════╝\033[0m

Type naturally to manage your scripts and automation tasks.
All processing happens locally - your privacy is protected.

Try commands like:
  - "list all python scripts" 
  - "run organize_ai_scripts.py"
  - "show README.md"
  - "help" or "what can I do?"

Type 'exit' to quit.
"""
        print(welcome_text)
    
    def process_input(self, user_input: str):
        """
        Process user input by recognizing intent and handling it appropriately.
        
        Args:
            user_input: The text input from the user
        """
        # Recognize intent from user input
        intent = self.recognizer.recognize(user_input)
        
        # Display debug info if needed
        # print(f"DEBUG: Recognized intent: {intent}")
        
        # Handle the intent
        self.handle_intent(intent)
    
    def handle_intent(self, intent: Intent):
        """
        Handle a recognized intent by dispatching to the appropriate handler.
        
        Args:
            intent: The recognized Intent object
        """
        handler = self.action_handlers.get(intent.type, self.handle_unknown)
        handler(intent)
    
    def handle_unknown(self, intent: Intent):
        """Handle unknown intent."""
        print("\033[1;33mI'm not sure what you want to do.\033[0m")
        print("Try 'help' to see available commands.")
    
    def handle_exit(self, intent: Intent):
        """Handle exit intent to terminate the terminal."""
        print("\nExiting Superhuman AI Terminal...")
        self.running = False
    
    def handle_ai_chat(self, intent: Intent):
        """Handle AI chat intent for natural conversation."""
        input_text = intent.original_input.lower()
        
        # Handle greetings
        if any(word in input_text for word in ["hi", "hello", "hey"]):
            print("\nHello! I'm your Superhuman AI Terminal assistant. How can I help you today?")
            print("Try asking me about available commands or what this system can do.")
        
        # Handle questions about capabilities
        elif "what can" in input_text and ("you" in input_text or "do" in input_text or "system" in input_text):
            print("\n\033[1;34mI can help you with the following:\033[0m")
            print("• Managing and organizing scripts")
            print("• Running scripts and automation tasks")
            print("• Searching for code or content")
            print("• Creating, renaming, moving, and deleting files")
            print("• Summarizing file contents")
            print("\nTry commands like 'list python scripts', 'run organize_ai_scripts.py', or 'help'")
        
        # Handle questions about the system
        elif "what is" in input_text and ("this" in input_text or "terminal" in input_text or "system" in input_text):
            print("\nThis is the Superhuman AI Terminal, a privacy-focused local terminal")
            print("that uses natural language processing to help you manage scripts and automation tasks.")
            print("All processing happens locally - your privacy is protected.")
            print("\nYou can use natural language commands like:")
            print("- 'list all scripts'")
            print("- 'run security_scan.py'")
            print("- 'search for file handling code'")
        
        # Handle questions about privacy
        elif "privacy" in input_text or "data" in input_text or "local" in input_text:
            print("\n\033[1;32mYour privacy is protected!\033[0m")
            print("The Superhuman AI Terminal processes all commands locally on your machine.")
            print("No data is sent to external servers, and all processing happens offline.")
            print("The intent recognition system uses spaCy which runs entirely on your device.")
        
        # Handle questions about usage
        elif "how" in input_text and ("use" in input_text or "work" in input_text):
            print("\n\033[1;34mUsing the Superhuman AI Terminal:\033[0m")
            print("1. Type natural language commands like 'list python scripts' or 'show README.md'")
            print("2. The terminal will recognize your intent and perform the appropriate action")
            print("3. For more specific information, try 'help' or ask about specific features")
            print("\nTry asking: 'How do I organize scripts?' or 'How do I search for files?'")
        
        # Default response
        else:
            print("\nI'm here to help you manage scripts and automation tasks.")
            print("You can ask me about available commands, how to use specific features,")
            print("or try direct commands like 'list scripts', 'run <script_name>', or 'help'.")
    
    def handle_list(self, intent: Intent):
        """Handle list intent to show files of a specific type."""
        target = intent.target or "scripts"
        target = target.lower()
        
        # Determine directory to list based on target
        if "python" in target or target in ["py", "python_scripts"]:
            dir_path = self.python_scripts_dir
            print("\n\033[1;34mPython Scripts:\033[0m")
        elif "shell" in target or target in ["sh", "shell_scripts", "bash"]:
            dir_path = self.shell_scripts_dir
            print("\n\033[1;34mShell Scripts:\033[0m")
        elif "doc" in target or target in ["md", "documentation", "docs"]:
            dir_path = self.docs_dir
            print("\n\033[1;34mDocumentation:\033[0m")
        elif "text" in target or target in ["txt", "text_files"]:
            dir_path = self.text_files_dir
            print("\n\033[1;34mText Files:\033[0m")
        else:
            print("\n\033[1;34mAll Scripts and Files:\033[0m")
            
            # List all script directories
            for dir_path, name in [
                (self.python_scripts_dir, "Python Scripts"),
                (self.shell_scripts_dir, "Shell Scripts"),
                (self.docs_dir, "Documentation"),
                (self.text_files_dir, "Text Files")
            ]:
                if dir_path.exists():
                    files = list(dir_path.glob("*"))
                    if files:
                        print(f"\n\033[1;32m{name}:\033[0m")
                        for f in files:
                            print(f"  {f.name}")
            return
        
        # List files in the selected directory
        if dir_path.exists():
            files = list(dir_path.glob("*"))
            if not files:
                print("  No files found.")
            else:
                for f in files:
                    print(f"  {f.name}")
        else:
            print(f"  Directory {dir_path} does not exist yet.")
            print("  You can create scripts and files with the 'create' command.")
    
    def handle_run(self, intent: Intent):
        """Handle run intent to execute a script."""
        script_name = intent.target
        
        if not script_name:
            print("\033[1;33mWhat script would you like to run?\033[0m")
            print("Try: run <script_name> or specify a python/shell script.")
            return
        
        # Determine script type and location
        if script_name.endswith(".py"):
            script_path = self.python_scripts_dir / script_name
            if not script_path.exists():
                script_path = Path.cwd() / script_name  # Try in current directory
        elif script_name.endswith(".sh"):
            script_path = self.shell_scripts_dir / script_name
            if not script_path.exists():
                script_path = Path.cwd() / script_name  # Try in current directory
        else:
            # Try with extensions
            py_path = self.python_scripts_dir / f"{script_name}.py"
            sh_path = self.shell_scripts_dir / f"{script_name}.sh"
            
            if py_path.exists():
                script_path = py_path
            elif sh_path.exists():
                script_path = sh_path
            else:
                print(f"\033[1;31mScript '{script_name}' not found.\033[0m")
                print("Try 'list scripts' to see available scripts.")
                return
        
        if not script_path.exists():
            print(f"\033[1;31mScript '{script_name}' not found.\033[0m")
            print("Try 'list scripts' to see available scripts.")
            return
        
        # Execute the script
        print(f"\n\033[1;32mRunning script: {script_path}\033[0m\n")
        
        try:
            if script_path.suffix == ".py":
                # Run Python script
                import subprocess
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                if result.stderr:
                    print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            elif script_path.suffix == ".sh":
                # Run shell script
                import subprocess
                # Make sure the script is executable
                script_path.chmod(0o755)
                result = subprocess.run(
                    ["bash", str(script_path)],
                    capture_output=True,
                    text=True
                )
                print(result.stdout)
                if result.stderr:
                    print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            
            print(f"\n\033[1;32mScript execution completed.\033[0m")
            
        except Exception as e:
            print(f"\033[1;31mError executing script: {e}\033[0m")
    
    def handle_search(self, intent: Intent):
        """Handle search intent to find text in files."""
        query = intent.target
        
        if not query and "query" in intent.parameters:
            query = intent.parameters["query"]
        
        if not query:
            print("\033[1;33mWhat would you like to search for?\033[0m")
            print("Try: search for <text> or find <text> in scripts")
            return
        
        print(f"\n\033[1;34mSearching for: '{query}'\033[0m\n")
        
        # Determine directories to search
        search_dirs = []
        if "file_type" in intent.parameters:
            file_type = intent.parameters["file_type"]
            if file_type in ["py", "python"]:
                search_dirs = [self.python_scripts_dir]
            elif file_type in ["sh", "shell", "bash"]:
                search_dirs = [self.shell_scripts_dir]
            elif file_type in ["md", "markdown", "doc"]:
                search_dirs = [self.docs_dir]
            elif file_type in ["txt", "text"]:
                search_dirs = [self.text_files_dir]
        else:
            search_dirs = [
                self.python_scripts_dir,
                self.shell_scripts_dir,
                self.docs_dir,
                self.text_files_dir
            ]
        
        # Search in each directory
        found = False
        for dir_path in search_dirs:
            if dir_path.exists():
                for file_path in dir_path.glob("**/*"):
                    if file_path.is_file():
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                if query.lower() in content.lower():
                                    found = True
                                    print(f"\033[1;32mFound in: {file_path.relative_to(Path.cwd())}\033[0m")
                                    
                                    # Print lines containing the query
                                    lines = content.split("\n")
                                    for i, line in enumerate(lines):
                                        if query.lower() in line.lower():
                                            line_num = i + 1
                                            print(f"  Line {line_num}: {line.strip()}")
                        except Exception:
                            # Skip files that can't be read
                            pass
        
        if not found:
            print("\033[1;33mNo matches found.\033[0m")
    
    def handle_help(self, intent: Intent):
        """Handle help intent to show available commands and usage."""
        help_text = """
\033[1;35m╔═══════════════════════════════════════════════════════════╗
║             SUPERHUMAN AI TERMINAL HELP                      ║
╚═══════════════════════════════════════════════════════════╝\033[0m

You can use natural language to control this terminal. Here are some example commands:

\033[1;32mScript Management\033[0m
  • list all scripts                 - Show all available scripts
  • list python scripts              - Show Python scripts
  • run <script_name>                - Execute a script
  • create a new python script       - Create a new script
  • organize my scripts              - Run the organization script

\033[1;32mFile Operations\033[0m
  • show README.md                   - Display file contents
  • search for <text>                - Search in files
  • create a new file                - Create a new file
  • delete <file_name>               - Delete a file
  • rename <old> to <new>            - Rename a file
  • move <file> to <directory>       - Move a file

\033[1;32mUtilities\033[0m
  • summarize <file>                 - Generate a summary of a file
  • help                             - Show this help message
  • exit                             - Exit the terminal

You can ask general questions about the system and I'll do my best to help.

\033[1;34mAll processing happens locally - your privacy is protected.\033[0m
"""
        print(help_text)
    
    def handle_organize(self, intent: Intent):
        """Handle organize intent to run the organization script."""
        organize_script = Path.cwd() / ".github" / "scripts" / "organize_ai_scripts.py"
        
        if not organize_script.exists():
            print("\033[1;31mOrganization script not found.\033[0m")
            print("Please ensure the script exists at .github/scripts/organize_ai_scripts.py")
            return
        
        print("\n\033[1;32mRunning organization script...\033[0m\n")
        
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(organize_script)],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print(f"\033[1;31mErrors:\033[0m\n{result.stderr}")
            
            print(f"\n\033[1;32mScript organization completed.\033[0m")
            
        except Exception as e:
            print(f"\033[1;31mError running organization script: {e}\033[0m")
    
    def handle_show(self, intent: Intent):
        """Handle show intent to display file contents."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to see?\033[0m")
            print("Try: show <filename> or display contents of <filename>")
            return
        
        # Determine file location based on extension
        file_path = None
        if filename.endswith(".py"):
            file_path = self.python_scripts_dir / filename
        elif filename.endswith(".sh"):
            file_path = self.shell_scripts_dir / filename
        elif filename.endswith(".md"):
            file_path = self.docs_dir / filename
            if not file_path.exists() and filename == "README.md":
                file_path = Path.cwd() / "README.md"
        elif filename.endswith(".txt") or filename.endswith((".json", ".yaml", ".yml")):
            file_path = self.text_files_dir / filename
        
        # If not found by extension, try all directories
        if not file_path or not file_path.exists():
            for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
                test_path = dir_path / filename
                if test_path.exists():
                    file_path = test_path
                    break
        
        if not file_path or not file_path.exists():
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            print("Try 'list scripts' or 'list docs' to see available files.")
            return
        
        # Display the file contents
        print(f"\n\033[1;34mContents of {file_path}:\033[0m\n")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Basic syntax highlighting
                if file_path.suffix == ".py":
                    content = self._highlight_python(content)
                elif file_path.suffix == ".md":
                    content = self._highlight_markdown(content)
                
                print(content)
                
        except Exception as e:
            print(f"\033[1;31mError reading file: {e}\033[0m")
    
    def _highlight_python(self, content: str) -> str:
        """Simple Python syntax highlighting for terminal."""
        # This is a very basic implementation - could be enhanced
        lines = content.split("\n")
        result = []
        
        for line in lines:
            # Comments
            if re.match(r'^\s*#.*$', line):
                line = f"\033[1;32m{line}\033[0m"
            # Function definitions
            elif re.match(r'^\s*def\s+\w+\(.*\):', line):
                line = f"\033[1;34m{line}\033[0m"
            # Class definitions
            elif re.match(r'^\s*class\s+\w+.*:', line):
                line = f"\033[1;35m{line}\033[0m"
            # Strings
            elif '"' in line or "'" in line:
                # Very simple, not accurate for all cases
                line = re.sub(r'(".*?")', r'\033[0;32m\1\033[0m', line)
                line = re.sub(r"('.*?')", r'\033[0;32m\1\033[0m', line)
            
            result.append(line)
        
        return "\n".join(result)
    
    def _highlight_markdown(self, content: str) -> str:
        """Simple Markdown syntax highlighting for terminal."""
        lines = content.split("\n")
        result = []
        
        for line in lines:
            # Headers
            if re.match(r'^#{1,6}\s+.*$', line):
                line = f"\033[1;35m{line}\033[0m"
            # Bold text
            line = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', line)
            # Italic text
            line = re.sub(r'\*(.*?)\*', r'\033[3m\1\033[0m', line)
            # Code blocks
            line = re.sub(r'`(.*?)`', r'\033[0;36m\1\033[0m', line)
            
            result.append(line)
        
        return "\n".join(result)
    
    def handle_create(self, intent: Intent):
        """Handle create intent to create a new file."""
        # Try to extract file type and name from intent
        file_type = None
        file_name = None
        
        if "file_type" in intent.parameters:
            file_type = intent.parameters["file_type"]
        
        if intent.target:
            file_name = intent.target
        
        # If file type or name is not specified, ask for it
        if not file_type:
            print("\033[1;33mWhat type of file would you like to create?\033[0m")
            print("Options: python, shell, markdown, text")
            file_type = input("> ").strip().lower()
            
        if not file_name:
            print("\033[1;33mWhat should the file be named?\033[0m")
            file_name = input("> ").strip()
        
        # Ensure the file has the correct extension
        if file_type in ["python", "py"]:
            if not file_name.endswith(".py"):
                file_name += ".py"
            file_path = self.python_scripts_dir / file_name
            template = """#!/usr/bin/env python3
\"\"\"
{file_name} - Brief description

This script...

Author: {author}
Date: {date}
\"\"\"

def main():
    \"\"\"Main function.\"\"\"
    print("Hello from {file_name}!")

if __name__ == "__main__":
    main()
"""
        elif file_type in ["shell", "sh", "bash"]:
            if not file_name.endswith(".sh"):
                file_name += ".sh"
            file_path = self.shell_scripts_dir / file_name
            template = """#!/bin/bash
#
# {file_name} - Brief description
#
# Author: {author}
# Date: {date}

# Exit on error
set -e

# Script logic here
echo "Hello from {file_name}!"
"""
        elif file_type in ["markdown", "md"]:
            if not file_name.endswith(".md"):
                file_name += ".md"
            file_path = self.docs_dir / file_name
            template = """# {title}

## Overview

Brief description of this document.

## Contents

- Section 1
- Section 2

## Section 1

Content for section 1...

## Section 2

Content for section 2...

---

Created on {date}
"""
        elif file_type in ["text", "txt"]:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            file_path = self.text_files_dir / file_name
            template = """This is a text file named {file_name}.

Created on {date}
"""
        else:
            print(f"\033[1;31mUnknown file type: {file_type}\033[0m")
            print("Supported types: python, shell, markdown, text")
            return
        
        # Create directory if it doesn't exist
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file already exists
        if file_path.exists():
            print(f"\033[1;31mFile '{file_path}' already exists.\033[0m")
            print("Try a different name or use 'show' to view its contents.")
            return
        
        # Create the file from template
        try:
            import getpass
            import datetime
            
            # Format template with appropriate values
            content = template.format(
                file_name=file_name,
                title=file_name.split('.')[0].title(),
                author=getpass.getuser(),
                date=datetime.datetime.now().strftime("%Y-%m-%d")
            )
            
            # Write the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Make shell scripts executable
            if file_path.suffix == ".sh":
                file_path.chmod(0o755)
            
            print(f"\n\033[1;32mCreated file: {file_path}\033[0m")
            print("Would you like to see its contents? (y/n)")
            
            if input("> ").strip().lower() == "y":
                print(f"\n\033[1;34mContents of {file_path}:\033[0m\n")
                print(content)
            
        except Exception as e:
            print(f"\033[1;31mError creating file: {e}\033[0m")
    
    def handle_delete(self, intent: Intent):
        """Handle delete intent to remove a file."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to delete?\033[0m")
            filename = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Confirm deletion
        print(f"\n\033[1;33mAre you sure you want to delete '{file_path}'? (y/n)\033[0m")
        if input("> ").strip().lower() != "y":
            print("Delete operation cancelled.")
            return
        
        # Delete the file
        try:
            file_path.unlink()
            print(f"\033[1;32mDeleted file: {file_path}\033[0m")
        except Exception as e:
            print(f"\033[1;31mError deleting file: {e}\033[0m")
    
    def handle_rename(self, intent: Intent):
        """Handle rename intent to rename a file."""
        old_name = intent.target
        new_name = None
        
        # Try to extract old and new names
        if "to" in intent.original_input.lower():
            parts = intent.original_input.lower().split("to")
            if len(parts) >= 2:
                # Extract old name from first part
                old_part = parts[0].split()
                for word in reversed(old_part):
                    if word not in ["rename", "mv", "move", "the", "file"]:
                        old_name = word
                        break
                
                # Extract new name from second part
                new_part = parts[1].strip().split()
                if new_part:
                    new_name = new_part[0]
        
        # If names are not clear, ask the user
        if not old_name:
            print("\033[1;33mWhat file would you like to rename?\033[0m")
            old_name = input("> ").strip()
        
        if not new_name:
            print(f"\033[1;33mWhat would you like to rename '{old_name}' to?\033[0m")
            new_name = input("> ").strip()
        
        # Find the file in all directories
        old_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / old_name
            if test_path.exists() and test_path.is_file():
                old_path = test_path
                break
        
        if not old_path:
            print(f"\033[1;31mFile '{old_name}' not found.\033[0m")
            return
        
        # Determine new path (same directory as old path)
        new_path = old_path.parent / new_name
        
        # Check if new file already exists
        if new_path.exists():
            print(f"\033[1;31mA file named '{new_name}' already exists in that location.\033[0m")
            return
        
        # Rename the file
        try:
            old_path.rename(new_path)
            print(f"\033[1;32mRenamed '{old_path.name}' to '{new_path.name}'\033[0m")
        except Exception as e:
            print(f"\033[1;31mError renaming file: {e}\033[0m")
    
    def handle_move(self, intent: Intent):
        """Handle move intent to move a file to another directory."""
        filename = intent.target
        dest_dir = None
        
        # Try to extract destination from parameters or input
        if "directory" in intent.parameters:
            dest_dir = intent.parameters["directory"]
        elif "to" in intent.original_input.lower():
            parts = intent.original_input.lower().split("to")
            if len(parts) >= 2:
                dest_part = parts[1].strip().split()
                if dest_part:
                    dest_dir = dest_part[0]
        
        # If filename or destination is not clear, ask the user
        if not filename:
            print("\033[1;33mWhat file would you like to move?\033[0m")
            filename = input("> ").strip()
        
        if not dest_dir:
            print("\033[1;33mWhere would you like to move the file to?\033[0m")
            print("Options: python_scripts, shell_scripts, docs, text_files")
            dest_dir = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Determine destination directory
        dest_path = None
        if dest_dir in ["python", "python_scripts", "py"]:
            dest_path = self.python_scripts_dir / file_path.name
        elif dest_dir in ["shell", "shell_scripts", "sh"]:
            dest_path = self.shell_scripts_dir / file_path.name
        elif dest_dir in ["docs", "documentation", "md"]:
            dest_path = self.docs_dir / file_path.name
        elif dest_dir in ["text", "text_files", "txt"]:
            dest_path = self.text_files_dir / file_path.name
        else:
            print(f"\033[1;31mUnknown destination: {dest_dir}\033[0m")
            print("Supported destinations: python_scripts, shell_scripts, docs, text_files")
            return
        
        # Create destination directory if it doesn't exist
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if destination file already exists
        if dest_path.exists():
            print(f"\033[1;31mA file named '{dest_path.name}' already exists in the destination.\033[0m")
            return
        
        # Move the file
        try:
            import shutil
            shutil.move(str(file_path), str(dest_path))
            print(f"\033[1;32mMoved '{file_path}' to '{dest_path}'\033[0m")
        except Exception as e:
            print(f"\033[1;31mError moving file: {e}\033[0m")
    
    def handle_summarize(self, intent: Intent):
        """Handle summarize intent to summarize file contents."""
        filename = intent.target
        
        if not filename:
            print("\033[1;33mWhat file would you like to summarize?\033[0m")
            filename = input("> ").strip()
        
        # Find the file in all directories
        file_path = None
        for dir_path in [self.python_scripts_dir, self.shell_scripts_dir, self.docs_dir, self.text_files_dir, Path.cwd()]:
            test_path = dir_path / filename
            if test_path.exists() and test_path.is_file():
                file_path = test_path
                break
        
        if not file_path:
            print(f"\033[1;31mFile '{filename}' not found.\033[0m")
            return
        
        # Read file contents
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"\033[1;31mError reading file: {e}\033[0m")
            return
        
        print(f"\n\033[1;34mSummarizing {file_path}...\033[0m\n")
        
        # Generate summary based on file type
        if file_path.suffix == ".py":
            self._summarize_python(file_path, content)
        elif file_path.suffix == ".sh":
            self._summarize_shell(file_path, content)
        elif file_path.suffix == ".md":
            self._summarize_markdown(file_path, content)
        else:
            self._summarize_text(file_path, content)
    
    def _summarize_python(self, file_path: Path, content: str):
        """Summarize a Python file."""
        # Extract docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        description = "No description available."
        if docstring_match:
            description = docstring_match.group(1).strip()
        
        # Count functions and classes
        functions = len(re.findall(r'def\s+\w+\s*\(', content))
        classes = len(re.findall(r'class\s+\w+\s*[:\(]', content))
        
        # Extract imports
        imports = re.findall(r'(?:from\s+\S+\s+)?import\s+\S+', content)
        
        # Check if it's a main script
        has_main = "if __name__ == \"__main__\":" in content
        
        print(f"\033[1;32mSummary of Python file: {file_path.name}\033[0m")
        print(f"\033[1;36mDescription:\033[0m {description}")
        print(f"\033[1;36mStats:\033[0m")
        print(f"  - {functions} function(s)")
        print(f"  - {classes} class(es)")
        print(f"  - {len(imports)} import statement(s)")
        print(f"  - {'Has' if has_main else 'No'} main entry point")
        
        if imports:
            print(f"\033[1;36mKey dependencies:\033[0m")
            for imp in imports[:5]:  # Show only first 5 imports
                print(f"  - {imp}")
            if len(imports) > 5:
                print(f"  - ... and {len(imports)-5} more")
    
    def _summarize_shell(self, file_path: Path, content: str):
        """Summarize a shell script."""
        # Extract description from comments
        description_match = re.search(r'#\s*(.*?)$', content, re.MULTILINE)
        description = "No description available."
        if description_match:
            description = description_match.group(1).strip()
        
        # Check for key shell features
        features = []
        if "set -e" in content:
            features.append("Exits on error")
        if "set -u" in content:
            features.append("Treats unset variables as errors")
        if "set -x" in content:
            features.append("Prints commands before execution")
        if "getopts" in content:
            features.append("Parses command-line options")
        if "trap" in content:
            features.append("Has signal traps")
        
        # Count functions
        functions = len(re.findall(r'function\s+\w+\s*\(\)|^\s*\w+\s*\(\)', content, re.MULTILINE))
        
