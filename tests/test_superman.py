#!/usr/bin/env python3
"""
Tests for Superman AI Orchestrator functionality.
"""

import sys
import tempfile
import unittest.mock as mock
import os
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import superman module
superman_path = Path(__file__).parent.parent / "superman.py"
sys.path.insert(0, str(superman_path.parent))

try:
    import superman
    from superman import CodeAnalyzer, MemorySystem, SupermanOrchestrator
except ImportError as e:
    pytest.skip(f"Superman module not available: {e}", allow_module_level=True)


class TestMemorySystem:
    """Test suite for the MemorySystem functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.memory = MemorySystem(max_memories=5)

    def test_memory_initialization(self):
        """Test that memory system initializes correctly."""
        assert len(self.memory.memories) == 0
        assert self.memory.max_memories == 5
        assert self.memory.session_start is not None

    def test_remember_conversation(self):
        """Test storing conversation exchanges."""
        self.memory.remember("test input", "test response", "test_intent")

        assert len(self.memory.memories) == 1
        memory = self.memory.memories[0]
        assert memory["user_input"] == "test input"
        assert memory["response"] == "test response"
        assert memory["intent_type"] == "test_intent"
        assert "timestamp" in memory

    def test_memory_limit(self):
        """Test that memory system respects size limits."""
        # Add more memories than the limit
        for i in range(10):
            self.memory.remember(f"input {i}", f"response {i}")

        # Should only keep the last 5
        assert len(self.memory.memories) == 5
        assert self.memory.memories[0]["user_input"] == "input 5"
        assert self.memory.memories[-1]["user_input"] == "input 9"

    def test_get_recent_context(self):
        """Test retrieving recent conversation context."""
        self.memory.remember("hello", "hi there")
        self.memory.remember("how are you", "I'm doing well")

        context = self.memory.get_recent_context(2)
        assert "hello" in context
        assert "hi there" in context
        assert "how are you" in context
        assert "I'm doing well" in context

    def test_search_memories(self):
        """Test searching through conversation history."""
        self.memory.remember("python code", "Here's some Python code")
        self.memory.remember("javascript info", "Here's some JS info")
        self.memory.remember("more python", "More Python details")

        results = self.memory.search_memories("python")
        assert len(results) == 2
        assert any("python code" in r["user_input"] for r in results)
        assert any("more python" in r["user_input"] for r in results)


class TestCodeAnalyzer:
    """Test suite for the CodeAnalyzer functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()

    def test_analyzer_initialization(self):
        """Test that code analyzer initializes correctly."""
        assert self.analyzer.repository_root is not None

    def test_analyze_python_file(self, tmp_path):
        """Test analyzing a Python file."""
        # Create a test Python file
        test_file = tmp_path / "test.py"
        test_file.write_text(
            '''#!/usr/bin/env python3
"""Test module."""

import os
from pathlib import Path

class TestClass:
    def test_method(self):
        pass

def test_function():
    pass

if __name__ == "__main__":
    print("Hello")
'''
        )

        analysis = self.analyzer.analyze_file(test_file)

        assert "error" not in analysis
        assert analysis["language"] == "python"
        assert analysis["classes"] == 1
        assert analysis["functions"] == 2  # test_method and test_function
        assert analysis["has_main"] is True
        assert analysis["has_docstring"] is True
        assert len(analysis["imports"]) >= 2

    def test_analyze_shell_file(self, tmp_path):
        """Test analyzing a shell script file."""
        test_file = tmp_path / "test.sh"
        test_file.write_text(
            """#!/bin/bash
set -e

test_function() {
    echo "test"
}

echo "Hello World"
"""
        )

        analysis = self.analyzer.analyze_file(test_file)

        assert "error" not in analysis
        assert analysis["language"] == "shell"
        assert analysis["has_shebang"] is True
        assert analysis["has_error_handling"] is True
        assert analysis["functions"] == 1

    def test_analyze_markdown_file(self, tmp_path):
        """Test analyzing a markdown file."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """# Main Title

## Section 1

Some content here.

```python
print("code block")
```

### Subsection

More content.
"""
        )

        analysis = self.analyzer.analyze_file(test_file)

        assert "error" not in analysis
        assert analysis["language"] == "markdown"
        assert analysis["headers"] == 3
        assert analysis["code_blocks"] == 1

    def test_analyze_nonexistent_file(self):
        """Test analyzing a file that doesn't exist."""
        analysis = self.analyzer.analyze_file("/nonexistent/file.py")
        assert "error" in analysis
        assert "not found" in analysis["error"].lower()

    def test_analyze_directory(self, tmp_path):
        """Test analyzing a directory structure."""
        # Create test files
        (tmp_path / "test.py").write_text("print('hello')")
        (tmp_path / "test.sh").write_text("echo 'hello'")
        (tmp_path / "README.md").write_text("# Test")

        analysis = self.analyzer.analyze_directory(tmp_path)

        assert "error" not in analysis
        assert analysis["total_files_scanned"] == 3
        assert ".py" in analysis["file_types"]
        assert ".sh" in analysis["file_types"]
        assert ".md" in analysis["file_types"]


class TestSupermanOrchestrator:
    """Test suite for the SupermanOrchestrator functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock to avoid needing full terminal setup
        with mock.patch(
            "superman.create_intent_recognizer"
        ) as mock_recognizer, mock.patch(
            "superman.SuperhumanTerminal.__init__"
        ) as mock_init:

            mock_init.return_value = None  # __init__ returns None
            self.orchestrator = SupermanOrchestrator()

            # Manually set required attributes that would be set by parent __init__
            self.orchestrator.intent_recognizer = mock.MagicMock()
            self.orchestrator.running = True
            self.orchestrator.history = []
            self.orchestrator.action_handlers = {}

            # Re-run the action_handlers update now that it exists
            from superman import IntentType

            if hasattr(self.orchestrator, "action_handlers"):
                self.orchestrator.action_handlers.update(
                    {
                        IntentType.AI_CHAT: self.orchestrator.handle_ai_chat_enhanced,
                    }
                )

    def test_orchestrator_initialization(self):
        """Test that Superman orchestrator initializes correctly."""
        assert hasattr(self.orchestrator, "memory")
        assert hasattr(self.orchestrator, "code_analyzer")
        assert hasattr(self.orchestrator, "superman_mode")
        assert self.orchestrator.superman_mode is False

    def test_superman_mode_activation(self):
        """Test activating Superman mode."""
        with mock.patch("builtins.print"):
            self.orchestrator.activate_superman_mode()

        assert self.orchestrator.superman_mode is True

    def test_superman_mode_deactivation(self):
        """Test deactivating Superman mode."""
        self.orchestrator.superman_mode = True

        with mock.patch("builtins.print"):
            self.orchestrator.deactivate_superman_mode()

        assert self.orchestrator.superman_mode is False

    def test_memory_integration(self):
        """Test that memory system is properly integrated."""
        assert isinstance(self.orchestrator.memory, MemorySystem)

        # Test that memory can store interactions
        self.orchestrator.memory.remember("test", "response")
        assert len(self.orchestrator.memory.memories) == 1

    def test_code_analyzer_integration(self):
        """Test that code analyzer is properly integrated."""
        assert isinstance(self.orchestrator.code_analyzer, CodeAnalyzer)

    @mock.patch("builtins.print")
    def test_show_status(self, mock_print):
        """Test the status command."""
        result = self.orchestrator.show_status()

        # Check that print was called (status was displayed)
        mock_print.assert_called()
        assert result == "Status information displayed."

    @mock.patch("builtins.print")
    def test_show_memory(self, mock_print):
        """Test the memory command."""
        # Add some memory first
        self.orchestrator.memory.remember("test input", "test response")

        result = self.orchestrator.show_memory()

        # Check that print was called (memory was displayed)
        mock_print.assert_called()
        assert result == "Memory status displayed."

    def test_superman_commands_registration(self):
        """Test that Superman-specific commands are registered."""
        expected_commands = ["memory", "analyze", "status", "demo"]

        for command in expected_commands:
            assert command in self.orchestrator.superman_commands


class TestSupermanOpenAIIntegration:
    """Test suite for Superman's OpenAI integration improvements."""

    def setup_method(self):
        """Set up test fixtures."""
        # Mock to avoid needing full terminal setup
        with mock.patch(
            "superman.create_intent_recognizer"
        ) as mock_recognizer, mock.patch(
            "superman.SuperhumanTerminal.__init__"
        ) as mock_init:

            mock_init.return_value = None  # __init__ returns None
            self.orchestrator = SupermanOrchestrator()

            # Manually set required attributes that would be set by parent __init__
            self.orchestrator.intent_recognizer = mock.MagicMock()
            self.orchestrator.running = True
            self.orchestrator.history = []
            self.orchestrator.action_handlers = {}

    def test_debug_mode_initialization(self):
        """Test that debug mode can be enabled via environment variable."""
        with mock.patch.dict(os.environ, {"SUPERMAN_DEBUG": "1"}):
            with mock.patch("builtins.print"):
                orch = SupermanOrchestrator()
                orch.intent_recognizer = mock.MagicMock()
                orch.running = True
                orch.history = []
                orch.action_handlers = {}
                
                assert orch.debug_mode is True

    def test_api_key_whitespace_handling(self):
        """Test that API keys with whitespace are properly handled."""
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "  sk-test123  "}):
            with mock.patch("builtins.print") as mock_print:
                orch = SupermanOrchestrator()
                orch.intent_recognizer = mock.MagicMock()
                orch.running = True
                orch.history = []
                orch.action_handlers = {}
                
                # Should still initialize successfully
                print_calls = [str(call) for call in mock_print.call_args_list]
                success_found = any("OpenAI integration enabled" in call for call in print_calls)
                assert success_found

    def test_invalid_api_key_format_warning(self):
        """Test that invalid API key formats trigger warnings."""
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key-format"}):
            with mock.patch("builtins.print") as mock_print:
                orch = SupermanOrchestrator()
                orch.intent_recognizer = mock.MagicMock()
                orch.running = True
                orch.history = []
                orch.action_handlers = {}
                
                # Should warn about invalid format
                print_calls = [str(call) for call in mock_print.call_args_list]
                warning_found = any("does not start with 'sk-'" in call for call in print_calls)
                assert warning_found

    @mock.patch("builtins.print")
    def test_debug_status_display(self, mock_print):
        """Test that debug mode is shown in status display."""
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123", "SUPERMAN_DEBUG": "1"}):
            orch = SupermanOrchestrator()
            orch.intent_recognizer = mock.MagicMock()
            orch.running = True
            orch.history = []
            orch.action_handlers = {}
            
            # Call status method
            orch.show_status()
            
            # Should show debug mode is enabled
            print_calls = [str(call) for call in mock_print.call_args_list]
            debug_status_found = any("Debug mode: ✅" in call for call in print_calls)
            assert debug_status_found

    def test_enhanced_error_handling(self):
        """Test enhanced error handling for API key errors."""
        from ai_script_inventory.ai.intent import Intent, IntentType
        
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test123", "SUPERMAN_DEBUG": "1"}):
            orch = SupermanOrchestrator()
            orch.intent_recognizer = mock.MagicMock()
            orch.running = True
            orch.history = []
            orch.action_handlers = {}
            orch.superman_mode = True
            
            # Mock OpenAI client to raise API key error
            mock_client = mock.MagicMock()
            orch.openai_client = mock_client
            mock_client.chat.completions.create.side_effect = Exception("Incorrect API key provided")
            
            test_intent = Intent(IntentType.AI_CHAT, confidence=0.9, original_input="test question")
            
            with mock.patch("builtins.print") as mock_print:
                result = orch.handle_ai_chat_enhanced(test_intent)
                
                print_calls = [str(call) for call in mock_print.call_args_list]
                
                # Should provide specific guidance for API key errors
                guidance_found = any("This suggests an issue with your OpenAI API key" in call for call in print_calls)
                assert guidance_found
                
                # Should provide troubleshooting checklist
                checklist_found = any("Please check that:" in call for call in print_calls)
                assert checklist_found


class TestSupermanScript:
    """Test suite for the overall Superman script functionality."""

    def test_imports_work(self):
        """Test that all required imports work correctly."""
        # Test should pass if we got this far without import errors
        assert superman is not None
        assert MemorySystem is not None
        assert CodeAnalyzer is not None
        assert SupermanOrchestrator is not None

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        assert hasattr(superman, "main")
        assert callable(superman.main)

    @mock.patch("superman.SupermanOrchestrator")
    def test_main_function_creates_orchestrator(self, mock_orchestrator_class):
        """Test that main function creates and runs orchestrator."""
        mock_orchestrator = mock.MagicMock()
        mock_orchestrator_class.return_value = mock_orchestrator

        with mock.patch("builtins.print"):  # Suppress any print statements
            try:
                superman.main()
            except SystemExit:
                pass  # Expected if orchestrator.run() raises SystemExit

        # Verify orchestrator was created and run was called
        mock_orchestrator_class.assert_called_once()
        mock_orchestrator.run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
