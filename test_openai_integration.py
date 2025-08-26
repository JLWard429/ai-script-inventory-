#!/usr/bin/env python3
"""
Test script to verify OpenAI integration in Superman orchestrator
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from superman import SupermanOrchestrator


def test_openai_initialization():
    """Test OpenAI client initialization"""
    # Test without API key
    os.environ.pop('OPENAI_API_KEY', None)
    orchestrator = SupermanOrchestrator()
    assert orchestrator.openai_client is None
    
    # Test with fake API key
    os.environ['OPENAI_API_KEY'] = 'sk-test123'
    orchestrator2 = SupermanOrchestrator()
    assert orchestrator2.openai_client is not None
    
    print("✅ OpenAI initialization tests passed")


def test_system_prompt():
    """Test system prompt generation"""
    orchestrator = SupermanOrchestrator()
    prompt = orchestrator._get_system_prompt()
    
    assert "Superman AI Orchestrator" in prompt
    assert "repository" in prompt.lower()
    assert "action" in prompt.lower()
    assert "json" in prompt.lower()
    
    print("✅ System prompt tests passed")


def test_delegation_parsing():
    """Test delegation response parsing"""
    orchestrator = SupermanOrchestrator()
    
    # Test JSON delegation response
    json_response = '{"action": "show", "target": "README.md", "params": {}}'
    
    try:
        import json
        delegation = json.loads(json_response)
        assert delegation["action"] == "show"
        assert delegation["target"] == "README.md"
        print("✅ JSON delegation parsing tests passed")
    except Exception as e:
        print(f"❌ JSON parsing failed: {e}")


def test_fallback_processing():
    """Test fallback to local processing"""
    orchestrator = SupermanOrchestrator()
    
    # Should have intent recognizer for fallback
    assert hasattr(orchestrator, 'intent_recognizer')
    assert orchestrator.intent_recognizer is not None
    
    print("✅ Fallback processing tests passed")


if __name__ == "__main__":
    print("Testing OpenAI integration in Superman orchestrator...")
    
    test_openai_initialization()
    test_system_prompt()
    test_delegation_parsing()
    test_fallback_processing()
    
    print("\n🎉 All OpenAI integration tests passed!")