# Create ai directory if it doesn't exist
mkdir -p ai

# Create ai/__init__.py
cat > ai/__init__.py << 'EOF'
"""
AI module for Superhuman AI Terminal.

This module provides intent recognition and NLP capabilities
for the terminal interface.
"""

from .intent import IntentRecognizer, Intent, IntentType

__all__ = ['IntentRecognizer', 'Intent', 'IntentType']
EOF

# Create ai/intent.py
cat > ai/intent.py << 'EOF'
#!/usr/bin/env python3
"""
Intent recognition module using spaCy for natural language understanding.

This module provides a robust intent recognition system for the Superhuman AI Terminal,
with fallback pattern matching when spaCy is unavailable.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any


class IntentType(Enum):
    """Types of intents recognized by the system."""
    RUN = "run"
    LIST = "list"
    SEARCH = "search"
    HELP = "help"
    EXIT = "exit"
    CREATE = "create"
    DELETE = "delete"
    ORGANIZE = "organize"
    UNKNOWN = "unknown"
    AI_CHAT = "ai_chat"


@dataclass
class Intent:
    """Represents a recognized intent with its parameters."""
    type: IntentType
    confidence: float
    params: Dict[str, Any] = None
    original_text: str = ""

    def __post_init__(self):
        if self.params is None:
            self.params = {}


class IntentRecognizer:
    """
    Intent recognition using spaCy with fallback to pattern matching.
    
    Uses natural language processing to identify user intent from
    text input. Falls back to regex patterns when spaCy is unavailable.
    """
    
    def __init__(self):
        """Initialize the intent recognizer with spaCy if available."""
        self.nlp = None
        self.matcher = None
        self.spacy_available = False
        
        # Try to initialize spaCy
        try:
            import spacy
            from spacy.matcher import Matcher
            
            # Load the English model
            try:
                self.nlp = spacy.load("en_core_web_sm")
                self.matcher = Matcher(self.nlp.vocab)
                self._setup_spacy_patterns()
                self.spacy_available = True
                print("✅ spaCy initialized successfully")
            except OSError:
                print("⚠️ spaCy model not found. Please install it with:")
                print("   python -m spacy download en_core_web_sm")
                self.spacy_available = False
        except ImportError:
            print("⚠️ spaCy not available. Using fallback pattern recognition.")
            self.spacy_available = False
        
        # Set up fallback patterns
        self._setup_fallback_patterns()

    def _setup_spacy_patterns(self):
        """Set up spaCy patterns for intent recognition."""
        if not self.spacy_available:
            return
        
        # Run patterns
        run_patterns = [
            [{"LOWER": "run"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "execute"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "start"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": {"IN": ["python", "py"]}}, {"TEXT": {"REGEX": r".*\.py$"}}]
        ]
        self.matcher.add("RUN", run_patterns)
        
        # List patterns
        list_patterns = [
            [{"LOWER": "list"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "show"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "display"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": {"IN": ["ls", "dir"]}}, {"OP": "?"}, {"OP": "*"}]
        ]
        self.matcher.add("LIST", list_patterns)
        
        # Search patterns
        search_patterns = [
            [{"LOWER": "search"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "find"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "locate"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": {"IN": ["grep", "filter"]}}, {"OP": "?"}, {"OP": "*"}]
        ]
        self.matcher.add("SEARCH", search_patterns)
        
        # Help patterns
        help_patterns = [
            [{"LOWER": "help"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": {"IN": ["man", "manual", "guide"]}}, {"OP": "?"}, {"OP": "*"}],
            [{"TEXT": "--help"}]
        ]
        self.matcher.add("HELP", help_patterns)
        
        # Exit patterns
        exit_patterns = [
            [{"LOWER": {"IN": ["exit", "quit", "bye", "goodbye"]}}],
            [{"LOWER": "close"}, {"LOWER": "terminal"}]
        ]
        self.matcher.add("EXIT", exit_patterns)
        
        # Create patterns
        create_patterns = [
            [{"LOWER": {"IN": ["create", "make", "new"]}}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "add"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "touch"}, {"OP": "?"}, {"OP": "*"}]
        ]
        self.matcher.add("CREATE", create_patterns)
        
        # Delete patterns
        delete_patterns = [
            [{"LOWER": {"IN": ["delete", "remove", "rm"]}}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "trash"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "erase"}, {"OP": "?"}, {"OP": "*"}]
        ]
        self.matcher.add("DELETE", delete_patterns)
        
        # Organize patterns
        organize_patterns = [
            [{"LOWER": {"IN": ["organize", "sort", "categorize"]}}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "clean"}, {"LOWER": "up"}, {"OP": "?"}, {"OP": "*"}],
            [{"LOWER": "arrange"}, {"OP": "?"}, {"OP": "*"}]
        ]
        self.matcher.add("ORGANIZE", organize_patterns)

    def _setup_fallback_patterns(self):
        """Set up fallback regex patterns when spaCy is unavailable."""
        self.fallback_patterns = {
            IntentType.RUN: [
                r"^(?:run|execute|start)\s+(.+)$",
                r"^python\s+(\S+\.py)(?:\s+(.+))?$",
                r"^\.\/(\S+\.sh)(?:\s+(.+))?$"
            ],
            IntentType.LIST: [
                r"^(?:list|show|display|ls|dir)\s*(.*?)$"
            ],
            IntentType.SEARCH: [
                r"^(?:search|find|locate|grep)\s+(.+)$"
            ],
            IntentType.HELP: [
                r"^(?:help|--help|man|manual|guide)(?:\s+(.+))?$",
                r"^(?:how\s+to|what\s+is|how\s+do\s+i)\s+(.+)$"
            ],
            IntentType.EXIT: [
                r"^(?:exit|quit|bye|goodbye)$",
                r"^close\s+terminal$"
            ],
            IntentType.CREATE: [
                r"^(?:create|make|new|add|touch)\s+(.+)$"
            ],
            IntentType.DELETE: [
                r"^(?:delete|remove|rm|trash|erase)\s+(.+)$"
            ],
            IntentType.ORGANIZE: [
                r"^(?:organize|sort|categorize|clean\s+up|arrange)\s*(.*?)$"
            ],
            IntentType.AI_CHAT: [
                r"^(?!run|list|search|help|exit|create|delete|organize|ls|dir|python|find|grep).*\?$",
                r"^(?:tell\s+me|explain|describe|what|how|who|when|why|where)\s+(.+)$",
                r"^(?:can\s+you|could\s+you|would\s+you)\s+(.+)$"
            ]
        }

    def _extract_entities_from_doc(self, doc):
        """Extract entities and parameters from a spaCy doc."""
        params = {}
        
        # Extract script name or files
        for token in doc:
            if token.text.endswith('.py') or token.text.endswith('.sh'):
                params['script_name'] = token.text
                break
        
        # Extract directory paths
        for token in doc:
            if token.text.startswith('./') or token.text.startswith('/'):
                params['path'] = token.text
                break
        
        # Extract specific file types
        file_types = ['python', 'shell', 'text', 'markdown', 'md', 'py', 'sh', 'txt']
        for token in doc:
            if token.text.lower() in file_types:
                params['file_type'] = token.text.lower()
                break
        
        return params

    def _extract_params_from_text(self, intent_type: IntentType, text: str) -> Dict[str, Any]:
        """Extract parameters from text based on the intent type."""
        params = {}
        
        if intent_type == IntentType.RUN:
            # Extract script name
            match = re.search(r'(\S+\.(py|sh))', text)
            if match:
                params['script_name'] = match.group(0)
            
            # Extract arguments
            if 'script_name' in params:
                args_text = text.split(params['script_name'], 1)
                if len(args_text) > 1:
                    args = args_text[1].strip()
                    if args:
                        params['args'] = args
        
        elif intent_type == IntentType.LIST:
            # Extract path or filter
            words = text.split()[1:] if len(text.split()) > 1 else []
            if words:
                path_or_filter = ' '.join(words)
                if '/' in path_or_filter:
                    params['path'] = path_or_filter
                else:
                    params['filter'] = path_or_filter
        
        elif intent_type == IntentType.SEARCH:
            # Extract search query
            words = text.split()[1:] if len(text.split()) > 1 else []
            if words:
                params['query'] = ' '.join(words)
        
        return params

    def recognize(self, text: str) -> Intent:
        """
        Recognize intent from text input.
        
        Args:
            text: User input text
            
        Returns:
            Intent object with recognized intent type and parameters
        """
        text = text.strip()
        
        # Handle empty input
        if not text:
            return Intent(type=IntentType.UNKNOWN, confidence=0.0, original_text=text)
        
        # Try spaCy recognition first if available
        if self.spacy_available:
            try:
                intent = self._recognize_with_spacy(text)
                if intent.type != IntentType.UNKNOWN:
                    return intent
            except Exception as e:
                print(f"spaCy recognition failed: {e}")
                print("Falling back to pattern matching...")
        
        # Fall back to pattern matching
        return self._recognize_with_patterns(text)

    def _recognize_with_spacy(self, text: str) -> Intent:
        """Use spaCy to recognize intent."""
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        if not matches:
            # Check for question pattern that might indicate AI chat
            if text.endswith('?') or any(token.text.lower() in ["what", "how", "who", "when", "why", "where", "can", "could", "would"] for token in doc):
                return Intent(type=IntentType.AI_CHAT, confidence=0.7, original_text=text)
            return Intent(type=IntentType.UNKNOWN, confidence=0.0, original_text=text)
        
        # Get the match with the highest score
        match_id, start, end = max(matches, key=lambda x: x[1])
        span = doc[start:end]
        
        intent_label = self.nlp.vocab.strings[match_id]
        confidence = 0.8  # Base confidence for matched patterns
        
        try:
            intent_type = IntentType[intent_label]
        except KeyError:
            intent_type = IntentType.UNKNOWN
            confidence = 0.3
        
        # Extract parameters based on the recognized intent
        params = self._extract_entities_from_doc(doc)
        additional_params = self._extract_params_from_text(intent_type, text)
        params.update(additional_params)
        
        return Intent(type=intent_type, confidence=confidence, params=params, original_text=text)

    def _recognize_with_patterns(self, text: str) -> Intent:
        """Use regex patterns to recognize intent when spaCy is unavailable."""
        for intent_type, patterns in self.fallback_patterns.items():
            for pattern in patterns:
                match = re.match(pattern, text, re.IGNORECASE)
                if match:
                    params = {}
                    
                    # Extract parameters from the regex groups
                    if match.groups():
                        if intent_type == IntentType.RUN:
                            params['script_name'] = match.group(1)
                            if len(match.groups()) > 1 and match.group(2):
                                params['args'] = match.group(2)
                        elif intent_type == IntentType.LIST:
                            if match.group(1):
                                path_or_filter = match.group(1)
                                if '/' in path_or_filter:
                                    params['path'] = path_or_filter
                                else:
                                    params['filter'] = path_or_filter
                        elif intent_type == IntentType.SEARCH:
                            params['query'] = match.group(1)
                        elif intent_type == IntentType.HELP:
                            if len(match.groups()) > 0 and match.group(1):
                                params['topic'] = match.group(1)
                        elif intent_type == IntentType.CREATE:
                            params['name'] = match.group(1)
                        elif intent_type == IntentType.DELETE:
                            params['name'] = match.group(1)
                        elif intent_type == IntentType.AI_CHAT:
                            if len(match.groups()) > 0 and match.group(1):
                                params['query'] = match.group(1)
                    
                    return Intent(
                        type=intent_type,
                        confidence=0.6,  # Lower confidence for fallback patterns
                        params=params,
                        original_text=text
                    )
        
        # Default to AI chat for unrecognized queries that might be questions
        if '?' in text or text.lower().startswith(('what', 'how', 'why', 'when', 'where', 'who', 'can', 'could')):
            return Intent(
                type=IntentType.AI_CHAT,
                confidence=0.5,
                params={'query': text},
                original_text=text
            )
        
        return Intent(type=IntentType.UNKNOWN, confidence=0.0, original_text=text)


if __name__ == "__main__":
    # Simple test for the intent recognizer
    recognizer = IntentRecognizer()
    
    test_queries = [
        "run security_scan.py",
        "list python scripts",
        "search for password utilities",
        "help with script organization",
        "exit",
        "How do I use this terminal?",
        "What scripts are available?",
        "create a new Python script called test.py",
        "delete old_script.py",
        "organize my scripts"
    ]
    
    print("\n=== Testing Intent Recognition ===\n")
    for query in test_queries:
        intent = recognizer.recognize(query)
        print(f"Query: '{query}'")
        print(f"Intent: {intent.type.value} (confidence: {intent.confidence:.2f})")
        if intent.params:
            print(f"Parameters: {intent.params}")
        print()
EOF
