#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced Superhuman AI Terminal capabilities.

This script tests the key improvements made to make spaCy the primary engine
for intent recognition and entity extraction.
"""

import sys
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.intent import create_intent_recognizer, IntentType


def test_enhanced_terminal():
    """Test the enhanced terminal functionality."""
    print("🚀 Testing Enhanced Superhuman AI Terminal")
    print("=" * 60)
    
    recognizer = create_intent_recognizer()
    
    # Test cases from the problem statement
    test_cases = [
        {
            "description": "Complex security scan command",
            "query": "run security scan on all Python files in shell_scripts",
            "expected_intent": IntentType.RUN_SCRIPT,
            "expected_params": ["scope", "file_type", "directory", "action_modifier"],
        },
        {
            "description": "Latest file summarization",
            "query": "summarize the latest README",
            "expected_intent": IntentType.SUMMARIZE,
            "expected_params": ["scope"],
        },
        {
            "description": "Conversational system query",
            "query": "How do I use this system?",
            "expected_intent": IntentType.AI_CHAT,
            "expected_params": [],
        },
        {
            "description": "Natural language command request",
            "query": "I need to run the security analysis on all my Python files",
            "expected_intent": IntentType.RUN_SCRIPT,
            "expected_params": ["file_type", "scope", "action_modifier", "intent_strength"],
        },
        {
            "description": "Preview configuration files",
            "query": "preview the main configuration files",
            "expected_intent": IntentType.PREVIEW,
            "expected_params": ["file_type", "scope"],
        },
        {
            "description": "Organization advice request",
            "query": "Can you help me organize my scripts better?",
            "expected_intent": IntentType.AI_CHAT,
            "expected_params": ["action_modifier", "intent_strength"],
        },
        {
            "description": "Security features inquiry",
            "query": "What are the security features?",
            "expected_intent": IntentType.AI_CHAT,
            "expected_params": ["action_modifier"],
        },
        {
            "description": "Development tools request",
            "query": "Run dev tools setup for me",
            "expected_intent": IntentType.RUN_SCRIPT,
            "expected_params": ["action_modifier"],
        },
        {
            "description": "File search with parameters",
            "query": "Find all shell scripts that contain the word test",
            "expected_intent": IntentType.SEARCH,
            "expected_params": ["file_type", "scope", "action_modifier"],
        },
        {
            "description": "Python tools summary request",
            "query": "I want to see a summary of all the Python tools available",
            "expected_intent": IntentType.AI_CHAT,
            "expected_params": ["file_type", "scope", "action_modifier", "intent_strength"],
        },
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. {case['description']}")
        print(f"   Query: \"{case['query']}\"")
        
        intent = recognizer.recognize(case["query"])
        
        # Check intent type
        if intent.type == case["expected_intent"]:
            print(f"   ✅ Intent: {intent.type.value} (confidence: {intent.confidence:.2f})")
        else:
            print(f"   ❌ Intent: Expected {case['expected_intent'].value}, got {intent.type.value}")
            continue
        
        # Check parameters
        missing_params = []
        for param in case["expected_params"]:
            if param not in intent.parameters:
                missing_params.append(param)
        
        if not missing_params:
            print(f"   ✅ Parameters: {intent.parameters}")
            passed += 1
        else:
            print(f"   ⚠️  Parameters: {intent.parameters}")
            print(f"      Missing expected: {missing_params}")
    
    print(f"\n" + "=" * 60)
    print(f"🎯 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🏆 All enhanced functionality working perfectly!")
    else:
        print("🔧 Some functionality needs attention.")
    
    return passed == total


def demonstrate_ai_chat():
    """Demonstrate the enhanced AI chat functionality."""
    print("\n\n🤖 Demonstrating Enhanced AI Chat")
    print("=" * 60)
    
    from superhuman_terminal import SuperhumanTerminal
    
    terminal = SuperhumanTerminal()
    recognizer = create_intent_recognizer()
    
    chat_examples = [
        "What are the security features?",
        "Can you help me organize my scripts better?",
        "I want to see a summary of all the Python tools available",
    ]
    
    for example in chat_examples:
        print(f"\n🗨️  User: \"{example}\"")
        print("-" * 40)
        
        intent = recognizer.recognize(example)
        if intent.type == IntentType.AI_CHAT:
            terminal.handle_ai_chat(intent)
        else:
            print(f"Note: Classified as {intent.type.value}")
        
        print("\n" + "=" * 40)


if __name__ == "__main__":
    # Test enhanced functionality
    success = test_enhanced_terminal()
    
    # Demonstrate AI chat
    demonstrate_ai_chat()
    
    if success:
        print("\n🚀 Enhanced Superhuman AI Terminal is ready!")
        print("   Try running: python superhuman_terminal.py")
    else:
        print("\n🔧 Please review the failing tests above.")
        sys.exit(1)