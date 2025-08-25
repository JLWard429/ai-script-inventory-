#!/usr/bin/env python3
"""
Local Intent Recognition Module for Superhuman AI Terminal

This module provides privacy-friendly, local-only intent recognition using
spaCy NLP library for advanced natural language understanding. It maps
natural language user requests to structured intents for easy dispatch
to action handlers.

No cloud LLM required - all processing happens locally using spaCy.
"""

import re
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

try:
    import spacy
    from spacy.matcher import Matcher

    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False


class IntentType(Enum):
    """Supported intent types for the terminal."""

    SUMMARIZE = "summarize"
    RUN_SCRIPT = "run_script"
    LIST = "list"
    SHOW = "show"
    PREVIEW = "preview"
    RENAME = "rename"
    SEARCH = "search"
    HELP = "help"
    EXIT = "exit"
    AI_CHAT = "ai_chat"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Represents a recognized intent with its parameters."""

    type: IntentType
    confidence: float
    target: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    original_input: str = ""


class IntentRecognizer:
    """Enhanced intent recognition using spaCy NLP for advanced understanding."""

    def __init__(self):
        """Initialize the intent recognizer with spaCy and patterns."""
        self.file_extensions = {".py", ".sh", ".md", ".txt", ".pdf", ".doc", ".docx"}

        # Initialize spaCy components
        if HAS_SPACY:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                self.matcher = Matcher(self.nlp.vocab)
                self._setup_spacy_patterns()
                self.use_spacy = True
                print("🔧 Using spaCy for enhanced intent recognition")
            except Exception as e:
                print(
                    f"⚠️ spaCy initialization failed: {e}. Falling back to keyword matching."
                )
                self.use_spacy = False
                self.intent_patterns = self._build_intent_patterns()
        else:
            print("⚠️ spaCy not available. Using keyword-based intent recognition.")
            self.use_spacy = False
            self.intent_patterns = self._build_intent_patterns()

    def _setup_spacy_patterns(self):
        """Setup spaCy matcher patterns for intent recognition."""
        # Help patterns
        help_patterns = [
            [{"LOWER": {"IN": ["help", "assistance", "guide"]}}],
            [{"LOWER": "how"}, {"LOWER": "to"}],
            [{"LOWER": "what"}, {"LOWER": {"IN": ["can", "do"]}}],
            [{"LOWER": {"IN": ["commands", "usage"]}}],
        ]
        self.matcher.add("HELP", help_patterns)

        # Exit patterns
        exit_patterns = [
            [{"LOWER": {"IN": ["exit", "quit", "bye", "goodbye"]}}],
            [{"LOWER": "see"}, {"LOWER": "you"}],
            [{"LOWER": "get"}, {"LOWER": "out"}],
        ]
        self.matcher.add("EXIT", exit_patterns)

        # Run script patterns
        run_patterns = [
            [
                {"LOWER": {"IN": ["run", "execute", "start", "launch"]}},
                {"TEXT": {"REGEX": r".*\.(py|sh)$"}},
            ],
            [
                {"LOWER": {"IN": ["run", "execute", "start", "launch"]}},
                {"IS_ALPHA": True},
            ],
            [{"LOWER": "python"}, {"TEXT": {"REGEX": r".*\.py$"}}],
            [{"LOWER": "bash"}, {"TEXT": {"REGEX": r".*\.sh$"}}],
            # Security scan patterns
            [{"LOWER": {"IN": ["run", "execute"]}}, {"LOWER": "security"}, {"LOWER": "scan"}],
            [{"LOWER": "security"}, {"LOWER": "scan"}],
            [{"LOWER": {"IN": ["run", "execute"]}}, {"LOWER": "scan"}],
            [{"LOWER": {"IN": ["run", "execute"]}}, {"LOWER": {"IN": ["the", "a"]}}, {"LOWER": "security"}, {"LOWER": "scan"}],
        ]
        self.matcher.add("RUN_SCRIPT", run_patterns)

        # List patterns
        list_patterns = [
            [
                {"LOWER": {"IN": ["list", "show", "display"]}},
                {"LOWER": {"IN": ["all", "files", "scripts"]}},
            ],
            [
                {"LOWER": "list"},
                {"LOWER": {"IN": ["python", "shell", "markdown"]}},
                {"LOWER": "files"},
            ],
            [{"LOWER": {"IN": ["ls", "dir"]}}],
        ]
        self.matcher.add("LIST", list_patterns)

        # Show/View patterns
        show_patterns = [
            [
                {"LOWER": {"IN": ["show", "view", "display", "open"]}},
                {"TEXT": {"REGEX": r".*\.(py|sh|md|txt)$"}},
            ],
            [
                {"LOWER": {"IN": ["show", "view", "display", "open"]}},
                {"IS_ALPHA": True},
            ],
            [{"LOWER": "contents"}, {"LOWER": "of"}],
        ]
        self.matcher.add("SHOW", show_patterns)

        # Search patterns
        search_patterns = [
            [{"LOWER": {"IN": ["search", "find", "look", "grep"]}}, {"LOWER": "for"}],
            [{"LOWER": {"IN": ["search", "find", "look"]}}, {"IS_ALPHA": True}],
            [{"LOWER": "find"}, {"LOWER": "files"}, {"LOWER": "containing"}],
        ]
        self.matcher.add("SEARCH", search_patterns)

        # Summarize patterns
        summarize_patterns = [
            [
                {"LOWER": {"IN": ["summarize", "summary", "brief"]}},
                {"TEXT": {"REGEX": r".*\.(md|txt|pdf)$"}},
            ],
            [
                {"LOWER": "summarize"},
                {"LOWER": {"IN": ["the", "this", "document", "file"]}},
            ],
            [{"LOWER": "summarize"}, {"IS_ALPHA": True}],
            [{"LOWER": {"IN": ["give", "provide"]}}, {"LOWER": "summary"}],
            [{"LOWER": "brief"}, {"LOWER": "overview"}],
            # Latest/recent patterns for summarization
            [{"LOWER": "summarize"}, {"LOWER": {"IN": ["the", "a"]}}, {"LOWER": {"IN": ["latest", "recent"]}}],
            [{"LOWER": "summarize"}, {"LOWER": {"IN": ["latest", "recent"]}}],
            [{"LOWER": {"IN": ["show", "get"]}}, {"LOWER": "summary"}, {"LOWER": "of"}, {"LOWER": {"IN": ["latest", "recent"]}}],
        ]
        self.matcher.add("SUMMARIZE", summarize_patterns)

        # Rename patterns
        rename_patterns = [
            [
                {"LOWER": {"IN": ["rename", "move"]}},
                {"IS_ALPHA": True},
                {"LOWER": "to"},
            ],
            [{"LOWER": "mv"}, {"IS_ALPHA": True}],
        ]
        self.matcher.add("RENAME", rename_patterns)

        # AI Chat patterns (questions, general queries)
        ai_chat_patterns = [
            [{"LOWER": {"IN": ["why", "how", "when", "where", "who", "what"]}}],
            [{"LOWER": {"IN": ["can", "could", "would", "should"]}}, {"LOWER": "you"}],
            [{"LOWER": {"IN": ["tell", "explain", "describe"]}}],
            [{"LOWER": "i"}, {"LOWER": {"IN": ["need", "want", "would", "like"]}}],
            [{"POS": "PRON"}, {"LOWER": {"IN": ["is", "are", "was", "were"]}}],
            [
                {
                    "LOWER": {
                        "IN": [
                            "advice",
                            "tip",
                            "tips",
                            "help",
                            "suggestion",
                            "recommend",
                        ]
                    }
                }
            ],
        ]
        self.matcher.add("AI_CHAT", ai_chat_patterns)

    def _build_intent_patterns(self) -> Dict[IntentType, List[Dict[str, Any]]]:
        """Build pattern dictionaries for each intent type (fallback method)."""
        return {
            IntentType.HELP: [
                {
                    "keywords": ["help", "usage", "how", "what", "commands"],
                    "weight": 1.0,
                },
                {
                    "patterns": [r"\bhelp\b", r"\bhow to\b", r"\bwhat.*do\b"],
                    "weight": 0.9,
                },
            ],
            IntentType.EXIT: [
                {"keywords": ["exit", "quit", "bye", "goodbye"], "weight": 1.0},
                {"patterns": [r"\bexit\b", r"\bquit\b", r"\bbye\b"], "weight": 1.0},
            ],
            IntentType.SUMMARIZE: [
                {
                    "keywords": ["summarize", "summary", "brief", "overview"],
                    "weight": 1.0,
                },
                {
                    "patterns": [
                        r"\bsummarize\b",
                        r"\bgive.*summary\b",
                        r"\bbrief.*overview\b",
                    ],
                    "weight": 0.9,
                },
                {
                    "context_keywords": [
                        "meeting",
                        "notes",
                        "document",
                        "file",
                        "text",
                    ],
                    "weight": 0.3,
                },
            ],
            IntentType.RUN_SCRIPT: [
                {"keywords": ["run", "execute", "start", "launch"], "weight": 0.8},
                {
                    "patterns": [r"\brun\s+\w+", r"\bexecute\s+\w+", r"\bstart\s+\w+"],
                    "weight": 0.9,
                },
                {
                    "context_keywords": ["script", "python", "shell", ".py", ".sh"],
                    "weight": 0.4,
                },
            ],
            IntentType.LIST: [
                {"keywords": ["list", "show", "display"], "weight": 0.7},
                {
                    "patterns": [
                        r"\blist\s+.*files?\b",
                        r"\bshow\s+.*files?\b",
                        r"\bls\b",
                    ],
                    "weight": 0.9,
                },
                {
                    "context_keywords": [
                        "files",
                        "scripts",
                        "documents",
                        "all",
                        "directory",
                    ],
                    "weight": 0.4,
                },
            ],
            IntentType.SHOW: [
                {"keywords": ["show", "display", "view", "open"], "weight": 0.7},
                {
                    "patterns": [r"\bshow\s+\w+", r"\bview\s+\w+", r"\bopen\s+\w+"],
                    "weight": 0.8,
                },
                {"context_keywords": ["file", "document", "content"], "weight": 0.3},
            ],
            IntentType.PREVIEW: [
                {"keywords": ["preview", "peek", "glimpse"], "weight": 1.0},
                {"patterns": [r"\bpreview\s+\w+", r"\bpeek\s+at\s+\w+"], "weight": 0.9},
            ],
            IntentType.SEARCH: [
                {"keywords": ["search", "find", "look", "grep"], "weight": 0.9},
                {
                    "patterns": [
                        r"\bfind\s+\w+",
                        r"\bsearch\s+for\s+\w+",
                        r"\blook\s+for\s+\w+",
                    ],
                    "weight": 0.9,
                },
                {
                    "context_keywords": ["file", "files", "in", "containing"],
                    "weight": 0.3,
                },
            ],
            IntentType.RENAME: [
                {"keywords": ["rename", "move", "mv"], "weight": 1.0},
                {
                    "patterns": [r"\brename\s+\w+", r"\bmove\s+\w+.*to\s+\w+"],
                    "weight": 0.9,
                },
            ],
            IntentType.AI_CHAT: [
                {
                    "keywords": [
                        "why",
                        "how",
                        "when",
                        "where",
                        "who",
                        "what",
                        "advice",
                        "tip",
                        "recommend",
                    ],
                    "weight": 0.7,
                },
                {
                    "patterns": [
                        r"\bwhy\s+",
                        r"\bhow\s+",
                        r"\bwhat\s+is\b",
                        r"\bcan\s+you\b",
                        r"\btell\s+me\b",
                    ],
                    "weight": 0.8,
                },
                {
                    "context_keywords": [
                        "explain",
                        "help",
                        "understand",
                        "know",
                        "learn",
                    ],
                    "weight": 0.3,
                },
            ],
        }

    def _extract_file_target_regex(self, user_input: str) -> Optional[str]:
        """Extract potential file targets from user input using regex (fallback method)."""
        words = user_input.split()

        # Look for words that might be filenames
        for word in words:
            # Clean up the word
            clean_word = word.strip(".,!?;:\"'")

            # Check if it has a file extension
            if any(clean_word.endswith(ext) for ext in self.file_extensions):
                return clean_word

            # Check if it's a likely filename (contains underscore, no spaces)
            if "_" in clean_word or "-" in clean_word:
                return clean_word

        # Look for quoted strings (potential filenames with spaces)
        quoted_pattern = r'["\']([^"\']+)["\']'
        quoted_matches = re.findall(quoted_pattern, user_input)
        if quoted_matches:
            return quoted_matches[0]

        return None

    def _extract_parameters_regex(
        self, user_input: str, target: Optional[str]
    ) -> Dict[str, Any]:
        """Extract additional parameters from user input using regex (fallback method)."""
        params = {}

        # Look for file type specifications
        if "pdf" in user_input.lower():
            params["file_type"] = "pdf"
        elif "python" in user_input.lower() or ".py" in user_input.lower():
            params["file_type"] = "python"
        elif "shell" in user_input.lower() or ".sh" in user_input.lower():
            params["file_type"] = "shell"
        elif "markdown" in user_input.lower() or ".md" in user_input.lower():
            params["file_type"] = "markdown"

        # Look for quantity indicators
        if "all" in user_input.lower():
            params["scope"] = "all"
        elif "recent" in user_input.lower() or "latest" in user_input.lower():
            params["scope"] = "recent"

        # Look for directory specifications
        words = user_input.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "from", "under"] and i + 1 < len(words):
                params["directory"] = words[i + 1]
                break

        return params

    def recognize(self, user_input: str) -> Intent:
        """
        Recognize intent from user input using spaCy NLP or fallback pattern matching.

        Args:
            user_input: The user's natural language input

        Returns:
            Intent object with recognized type, confidence, and parameters
        """
        if not user_input or not user_input.strip():
            return Intent(IntentType.UNKNOWN, 0.0, original_input=user_input)

        if self.use_spacy:
            return self._recognize_with_spacy(user_input)
        else:
            return self._recognize_with_patterns(user_input)

    def _recognize_with_spacy(self, user_input: str) -> Intent:
        """Use spaCy for advanced intent recognition."""
        doc = self.nlp(user_input)

        # Use spaCy matcher to find intent patterns
        matches = self.matcher(doc)
        intent_scores = {}

        # Score based on pattern matches
        for match_id, start, end in matches:
            intent_name = self.nlp.vocab.strings[match_id]
            intent_type = self._map_spacy_intent(intent_name)
            if intent_type in intent_scores:
                intent_scores[intent_type] += 0.8
            else:
                intent_scores[intent_type] = 0.8

        # Enhanced scoring using spaCy's linguistic features
        self._enhance_scores_with_linguistics(doc, intent_scores, user_input)

        # Extract entities and parameters using spaCy
        target, parameters = self._extract_entities_with_spacy(doc, user_input)

        # Determine best intent
        if intent_scores:
            best_intent = max(intent_scores.keys(), key=lambda k: intent_scores[k])
            confidence = min(intent_scores[best_intent], 1.0)
        else:
            # No pattern matches - analyze for AI chat or unknown
            best_intent, confidence = self._analyze_for_ai_chat(doc, user_input)

        # If confidence is too low, classify as unknown
        if confidence < 0.3:
            return Intent(IntentType.UNKNOWN, confidence, original_input=user_input)

        return Intent(
            type=best_intent,
            confidence=confidence,
            target=target,
            parameters=parameters,
            original_input=user_input,
        )

    def _map_spacy_intent(self, spacy_intent_name: str) -> IntentType:
        """Map spaCy pattern names to IntentType enum values."""
        mapping = {
            "HELP": IntentType.HELP,
            "EXIT": IntentType.EXIT,
            "RUN_SCRIPT": IntentType.RUN_SCRIPT,
            "LIST": IntentType.LIST,
            "SHOW": IntentType.SHOW,
            "SEARCH": IntentType.SEARCH,
            "SUMMARIZE": IntentType.SUMMARIZE,
            "RENAME": IntentType.RENAME,
            "AI_CHAT": IntentType.AI_CHAT,
        }
        return mapping.get(spacy_intent_name, IntentType.UNKNOWN)

    def _enhance_scores_with_linguistics(
        self, doc, intent_scores: Dict[IntentType, float], user_input: str
    ):
        """Enhance intent scores using spaCy's linguistic analysis."""
        # Check for interrogative words (questions) - lean toward AI_CHAT
        question_words = ["what", "why", "how", "when", "where", "who", "which"]
        if any(token.text.lower() in question_words for token in doc):
            intent_scores[IntentType.AI_CHAT] = (
                intent_scores.get(IntentType.AI_CHAT, 0) + 0.4
            )

        # Check for imperative mood (commands) - lean toward action intents
        has_imperative = any(token.tag_ == "VB" for token in doc)
        if has_imperative:
            for intent_type in [
                IntentType.RUN_SCRIPT,
                IntentType.LIST,
                IntentType.SHOW,
                IntentType.SEARCH,
            ]:
                if intent_type in intent_scores:
                    intent_scores[intent_type] += 0.2

        # Check for file-related entities
        file_entities = self._find_file_entities(doc)
        if file_entities:
            for intent_type in [
                IntentType.RUN_SCRIPT,
                IntentType.SHOW,
                IntentType.SUMMARIZE,
            ]:
                if intent_type in intent_scores:
                    intent_scores[intent_type] += 0.3

        # Check for request/help indicators
        help_indicators = ["please", "can you", "could you", "help me", "i need"]
        if any(phrase in user_input.lower() for phrase in help_indicators):
            intent_scores[IntentType.AI_CHAT] = (
                intent_scores.get(IntentType.AI_CHAT, 0) + 0.3
            )

    def _analyze_for_ai_chat(self, doc, user_input: str) -> Tuple[IntentType, float]:
        """Analyze input to determine if it should be handled as AI chat."""
        # Check for conversational patterns
        conversational_patterns = [
            r"\bi\s+(am|was|have|need|want|would|like)",
            r"\bcan\s+you",
            r"\bwhat\s+(is|are|do|does)",
            r"\bhow\s+(do|can|should)",
            r"\btell\s+me",
            r"\bexplain",
            r"\badvice",
            r"\btip",
            r"\bhelp\s+with",
        ]

        conversational_score = 0.0
        for pattern in conversational_patterns:
            if re.search(pattern, user_input.lower()):
                conversational_score += 0.2

        # Check for question structure
        if user_input.strip().endswith("?"):
            conversational_score += 0.3

        # Check for uncertainty indicators
        uncertainty_words = ["maybe", "perhaps", "possibly", "might", "could", "unsure"]
        if any(word in user_input.lower() for word in uncertainty_words):
            conversational_score += 0.2

        if conversational_score >= 0.4:
            return IntentType.AI_CHAT, min(conversational_score, 0.9)
        else:
            return IntentType.UNKNOWN, conversational_score

    def _extract_entities_with_spacy(
        self, doc, user_input: str
    ) -> Tuple[Optional[str], Dict[str, Any]]:
        """Extract entities and parameters using spaCy's NER and linguistic analysis."""
        target = None
        parameters = {}

        # Extract file entities
        file_entities = self._find_file_entities(doc)
        if file_entities:
            target = file_entities[0]  # Use first file found as target

        # Extract file types using spaCy entities and patterns
        file_type_mapping = {
            "python": "python",
            "shell": "shell",
            "markdown": "markdown",
            "pdf": "pdf",
            "text": "text",
        }

        for entity in doc.ents:
            if (
                entity.label_ in ["ORG", "PRODUCT"]
                and entity.text.lower() in file_type_mapping
            ):
                parameters["file_type"] = file_type_mapping[entity.text.lower()]

        # Look for scope indicators
        scope_words = ["all", "every", "recent", "latest", "new"]
        for token in doc:
            if token.text.lower() in scope_words:
                parameters["scope"] = token.text.lower()
                break

        # Extract directory mentions using dependency parsing
        for token in doc:
            if token.dep_ in ["prep", "pobj"] and token.head.text.lower() in [
                "in",
                "from",
                "under",
            ]:
                parameters["directory"] = token.text

        # Fallback to regex-based extraction for file targets
        if not target:
            target = self._extract_file_target_regex(user_input)

        # Fallback parameter extraction
        fallback_params = self._extract_parameters_regex(user_input, target)
        for key, value in fallback_params.items():
            if key not in parameters:
                parameters[key] = value

        return target, parameters

    def _find_file_entities(self, doc) -> List[str]:
        """Find file-related entities in the spaCy doc."""
        file_entities = []

        # Look for tokens that match file patterns
        for token in doc:
            # Check for file extensions
            if any(token.text.endswith(ext) for ext in self.file_extensions):
                file_entities.append(token.text)
            # Check for file-like patterns (word with underscore/dash)
            elif re.match(r"^[a-zA-Z_-]+[a-zA-Z0-9_-]*$", token.text) and (
                "_" in token.text or "-" in token.text
            ):
                file_entities.append(token.text)

        return file_entities

    def _recognize_with_patterns(self, user_input: str) -> Intent:
        """Fallback to original keyword/pattern-based recognition."""
        # Normalize input
        normalized_input = user_input.lower().strip()

        # Calculate scores for each intent type
        intent_scores = {}
        intent_targets = {}
        intent_params = {}

        for intent_type, patterns in self.intent_patterns.items():
            score, target, params = self._calculate_intent_score(
                normalized_input, patterns, user_input
            )
            intent_scores[intent_type] = score
            intent_targets[intent_type] = target
            intent_params[intent_type] = params

        # Find the highest scoring intent
        best_intent = max(intent_scores.keys(), key=lambda k: intent_scores[k])
        best_score = intent_scores[best_intent]

        # If score is too low, classify as unknown
        if best_score < 0.3:
            return Intent(IntentType.UNKNOWN, best_score, original_input=user_input)

        return Intent(
            type=best_intent,
            confidence=best_score,
            target=intent_targets[best_intent],
            parameters=intent_params[best_intent],
            original_input=user_input,
        )

    def _calculate_intent_score(
        self, normalized_input: str, patterns: List[Dict[str, Any]], original_input: str
    ) -> Tuple[float, Optional[str], Optional[Dict[str, Any]]]:
        """Calculate the score for a specific intent type."""
        total_score = 0.0
        target = None
        parameters = {}

        for pattern_dict in patterns:
            # Check keywords
            if "keywords" in pattern_dict:
                keyword_score = (
                    self._score_keywords(normalized_input, pattern_dict["keywords"])
                    * pattern_dict["weight"]
                )
                total_score += keyword_score

            # Check regex patterns
            if "patterns" in pattern_dict:
                pattern_score, extracted_target = self._score_patterns(
                    normalized_input, pattern_dict["patterns"]
                )
                total_score += pattern_score * pattern_dict["weight"]
                if extracted_target and not target:
                    target = extracted_target

            # Check context keywords (bonus points)
            if "context_keywords" in pattern_dict:
                context_score = (
                    self._score_keywords(
                        normalized_input, pattern_dict["context_keywords"]
                    )
                    * pattern_dict["weight"]
                )
                total_score += context_score

        # Extract file targets and parameters
        if not target:
            target = self._extract_file_target(original_input)

        parameters = self._extract_parameters(original_input, target)

        return min(total_score, 1.0), target, parameters

    def _score_keywords(self, text: str, keywords: List[str]) -> float:
        """Score based on keyword presence."""
        matches = sum(1 for keyword in keywords if keyword in text)
        return matches / len(keywords) if keywords else 0.0

    def _score_patterns(
        self, text: str, patterns: List[str]
    ) -> Tuple[float, Optional[str]]:
        """Score based on regex pattern matches."""
        total_matches = 0
        target = None

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                total_matches += 1
                # Try to extract target from the pattern
                if not target:
                    groups = match.groups()
                    if groups:
                        target = groups[0]
                    elif len(match.group().split()) > 1:
                        # Extract the word after the command
                        words = match.group().split()
                        if len(words) > 1:
                            target = words[1]

        return total_matches / len(patterns) if patterns else 0.0, target

    def _extract_file_target(self, user_input: str) -> Optional[str]:
        """Extract potential file targets from user input."""
        return self._extract_file_target_regex(user_input)

    def _extract_parameters(
        self, user_input: str, target: Optional[str]
    ) -> Dict[str, Any]:
        """Extract additional parameters from user input."""
        return self._extract_parameters_regex(user_input, target)


def create_intent_recognizer() -> IntentRecognizer:
    """Factory function to create an intent recognizer instance."""
    return IntentRecognizer()


# Example usage and testing
if __name__ == "__main__":
    recognizer = create_intent_recognizer()

    # Test examples
    test_inputs = [
        "help me with commands",
        "run data_cleaner.py",
        "list all PDF files",
        "summarize meeting notes",
        "show test_script.py",
        "search for python files",
        "exit",
        "rename old_file.txt to new_file.txt",
        "preview document.md",
        "what can you do?",
        "how do I get started?",
        "tell me about this repository",
        "what is the best way to organize scripts?",
    ]

    print("Intent Recognition Test Results:")
    print("=" * 50)

    for test_input in test_inputs:
        intent = recognizer.recognize(test_input)
        print(f"Input: '{test_input}'")
        print(f"  Intent: {intent.type.value}")
        print(f"  Confidence: {intent.confidence:.2f}")
        print(f"  Target: {intent.target}")
        print(f"  Parameters: {intent.parameters}")
        print()
