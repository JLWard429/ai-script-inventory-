#!/usr/bin/env python3
"""
Local Intent Recognition Module for Superhuman AI Terminal

This module provides privacy-friendly, local-only intent recognition using
keyword and pattern-based logic. It maps natural language user requests
to structured intents for easy dispatch to action handlers.

No cloud LLM required - all processing happens locally.
"""

import re
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


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
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """Represents a recognized intent with its parameters."""
    type: IntentType
    confidence: float
    target: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    original_input: str = ""


class IntentRecognizer:
    """Local intent recognition using keyword and pattern matching."""
    
    def __init__(self):
        """Initialize the intent recognizer with patterns and keywords."""
        self.intent_patterns = self._build_intent_patterns()
        self.file_extensions = {'.py', '.sh', '.md', '.txt', '.pdf', '.doc', '.docx'}
        
    def _build_intent_patterns(self) -> Dict[IntentType, List[Dict[str, Any]]]:
        """Build pattern dictionaries for each intent type."""
        return {
            IntentType.HELP: [
                {'keywords': ['help', 'usage', 'how', 'what', 'commands'], 'weight': 1.0},
                {'patterns': [r'\bhelp\b', r'\bhow to\b', r'\bwhat.*do\b'], 'weight': 0.9},
            ],
            
            IntentType.EXIT: [
                {'keywords': ['exit', 'quit', 'bye', 'goodbye'], 'weight': 1.0},
                {'patterns': [r'\bexit\b', r'\bquit\b', r'\bbye\b'], 'weight': 1.0},
            ],
            
            IntentType.SUMMARIZE: [
                {'keywords': ['summarize', 'summary', 'brief', 'overview'], 'weight': 1.0},
                {'patterns': [r'\bsummarize\b', r'\bgive.*summary\b', r'\bbrief.*overview\b'], 'weight': 0.9},
                {'context_keywords': ['meeting', 'notes', 'document', 'file', 'text'], 'weight': 0.3},
            ],
            
            IntentType.RUN_SCRIPT: [
                {'keywords': ['run', 'execute', 'start', 'launch'], 'weight': 0.8},
                {'patterns': [r'\brun\s+\w+', r'\bexecute\s+\w+', r'\bstart\s+\w+'], 'weight': 0.9},
                {'context_keywords': ['script', 'python', 'shell', '.py', '.sh'], 'weight': 0.4},
            ],
            
            IntentType.LIST: [
                {'keywords': ['list', 'show', 'display'], 'weight': 0.7},
                {'patterns': [r'\blist\s+.*files?\b', r'\bshow\s+.*files?\b', r'\bls\b'], 'weight': 0.9},
                {'context_keywords': ['files', 'scripts', 'documents', 'all', 'directory'], 'weight': 0.4},
            ],
            
            IntentType.SHOW: [
                {'keywords': ['show', 'display', 'view', 'open'], 'weight': 0.7},
                {'patterns': [r'\bshow\s+\w+', r'\bview\s+\w+', r'\bopen\s+\w+'], 'weight': 0.8},
                {'context_keywords': ['file', 'document', 'content'], 'weight': 0.3},
            ],
            
            IntentType.PREVIEW: [
                {'keywords': ['preview', 'peek', 'glimpse'], 'weight': 1.0},
                {'patterns': [r'\bpreview\s+\w+', r'\bpeek\s+at\s+\w+'], 'weight': 0.9},
            ],
            
            IntentType.SEARCH: [
                {'keywords': ['search', 'find', 'look', 'grep'], 'weight': 0.9},
                {'patterns': [r'\bfind\s+\w+', r'\bsearch\s+for\s+\w+', r'\blook\s+for\s+\w+'], 'weight': 0.9},
                {'context_keywords': ['file', 'files', 'in', 'containing'], 'weight': 0.3},
            ],
            
            IntentType.RENAME: [
                {'keywords': ['rename', 'move', 'mv'], 'weight': 1.0},
                {'patterns': [r'\brename\s+\w+', r'\bmove\s+\w+.*to\s+\w+'], 'weight': 0.9},
            ],
        }
    
    def recognize(self, user_input: str) -> Intent:
        """
        Recognize intent from user input using pattern matching.
        
        Args:
            user_input: The user's natural language input
            
        Returns:
            Intent object with recognized type, confidence, and parameters
        """
        if not user_input or not user_input.strip():
            return Intent(IntentType.UNKNOWN, 0.0, original_input=user_input)
        
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
            original_input=user_input
        )
    
    def _calculate_intent_score(
        self, 
        normalized_input: str, 
        patterns: List[Dict[str, Any]], 
        original_input: str
    ) -> Tuple[float, Optional[str], Optional[Dict[str, Any]]]:
        """Calculate the score for a specific intent type."""
        total_score = 0.0
        target = None
        parameters = {}
        
        for pattern_dict in patterns:
            # Check keywords
            if 'keywords' in pattern_dict:
                keyword_score = self._score_keywords(
                    normalized_input, pattern_dict['keywords']
                ) * pattern_dict['weight']
                total_score += keyword_score
            
            # Check regex patterns
            if 'patterns' in pattern_dict:
                pattern_score, extracted_target = self._score_patterns(
                    normalized_input, pattern_dict['patterns']
                )
                total_score += pattern_score * pattern_dict['weight']
                if extracted_target and not target:
                    target = extracted_target
            
            # Check context keywords (bonus points)
            if 'context_keywords' in pattern_dict:
                context_score = self._score_keywords(
                    normalized_input, pattern_dict['context_keywords']
                ) * pattern_dict['weight']
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
    
    def _score_patterns(self, text: str, patterns: List[str]) -> Tuple[float, Optional[str]]:
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
        words = user_input.split()
        
        # Look for words that might be filenames
        for word in words:
            # Clean up the word
            clean_word = word.strip('.,!?;:"\'')
            
            # Check if it has a file extension
            if any(clean_word.endswith(ext) for ext in self.file_extensions):
                return clean_word
            
            # Check if it's a likely filename (contains underscore, no spaces)
            if '_' in clean_word or '-' in clean_word:
                return clean_word
        
        # Look for quoted strings (potential filenames with spaces)
        quoted_pattern = r'["\']([^"\']+)["\']'
        quoted_matches = re.findall(quoted_pattern, user_input)
        if quoted_matches:
            return quoted_matches[0]
        
        return None
    
    def _extract_parameters(self, user_input: str, target: Optional[str]) -> Dict[str, Any]:
        """Extract additional parameters from user input."""
        params = {}
        
        # Look for file type specifications
        if 'pdf' in user_input.lower():
            params['file_type'] = 'pdf'
        elif 'python' in user_input.lower() or '.py' in user_input.lower():
            params['file_type'] = 'python'
        elif 'shell' in user_input.lower() or '.sh' in user_input.lower():
            params['file_type'] = 'shell'
        elif 'markdown' in user_input.lower() or '.md' in user_input.lower():
            params['file_type'] = 'markdown'
        
        # Look for quantity indicators
        if 'all' in user_input.lower():
            params['scope'] = 'all'
        elif 'recent' in user_input.lower():
            params['scope'] = 'recent'
        
        # Look for directory specifications
        words = user_input.split()
        for i, word in enumerate(words):
            if word.lower() in ['in', 'from', 'under'] and i + 1 < len(words):
                params['directory'] = words[i + 1]
                break
        
        return params


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