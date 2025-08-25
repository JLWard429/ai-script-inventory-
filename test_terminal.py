#!/usr/bin/env python3
"""
Basic tests for the Superhuman AI Terminal components.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai.intent import create_intent_recognizer, IntentType


def test_intent_recognition():
    """Test basic intent recognition functionality."""
    print("🧪 Testing Intent Recognition...")
    
    recognizer = create_intent_recognizer()
    
    test_cases = [
        ("help", IntentType.HELP),
        ("exit", IntentType.EXIT),
        ("run test_script.py", IntentType.RUN_SCRIPT),
        ("list all files", IntentType.LIST),
        ("show README.md", IntentType.SHOW),
        ("search for python", IntentType.SEARCH),
        ("summarize document", IntentType.SUMMARIZE),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for input_text, expected_intent in test_cases:
        intent = recognizer.recognize(input_text)
        if intent.type == expected_intent:
            print(f"  ✅ '{input_text}' -> {intent.type.value} (confidence: {intent.confidence:.2f})")
            passed += 1
        else:
            print(f"  ❌ '{input_text}' -> {intent.type.value} (expected: {expected_intent.value})")
    
    print(f"\n📊 Test Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
    return passed == total


def test_file_operations():
    """Test file operation functions."""
    print("\n🧪 Testing File Operations...")
    
    # Test file existence
    test_files = ["README.md", "ai/intent.py", "superhuman_terminal.py"]
    passed = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"  ✅ Found: {test_file}")
            passed += 1
        else:
            print(f"  ❌ Missing: {test_file}")
    
    print(f"\n📊 File Operations: {passed}/{len(test_files)} files found")
    return passed == len(test_files)


def main():
    """Run all tests."""
    print("🚀 Running Superhuman AI Terminal Tests")
    print("=" * 50)
    
    intent_test_passed = test_intent_recognition()
    file_test_passed = test_file_operations()
    
    print("\n" + "=" * 50)
    if intent_test_passed and file_test_passed:
        print("🎉 All tests passed! The Superhuman AI Terminal is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())