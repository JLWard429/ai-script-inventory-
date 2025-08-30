#!/usr/bin/env python3
"""
Tests for Superman AI Orchestrator functionality.
"""

import sys
import tempfile
import unittest.mock as mock
import urllib.error
import os
from pathlib_mod_custom import Path

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
from pathlib_mod_custom import Path

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
        expected_commands = [
            "memory",
            "analyze",
            "status",
            "demo",
            "employees",
            "delegate",
        ]

        for command in expected_commands:
            assert command in self.orchestrator.superman_commands

    def test_employee_discovery(self):
        """Test that employee scripts are discovered and registered."""
        # The orchestrator should have discovered some employees during initialization
        assert hasattr(self.orchestrator, "employees")
        assert isinstance(self.orchestrator.employees, dict)
        # Should have at least the example employee script we created
        employee_names = list(self.orchestrator.employees.keys())
        assert len(employee_names) > 0
        assert "employee_spacy_test" in employee_names

    def test_list_employees_command(self):
        """Test the list employees command."""
        with mock.patch("builtins.print") as mock_print:
            result = self.orchestrator.list_employees()

            # Should return a success message
            assert "employee scripts" in result.lower()
            # Should have printed employee information
            mock_print.assert_called()

    def test_delegate_task_no_args(self):
        """Test delegation with no arguments."""
        result = self.orchestrator.delegate_task("delegate")
        assert "Please specify employee" in result

    def test_delegate_task_unknown_employee(self):
        """Test delegation to unknown employee."""
        result = self.orchestrator.delegate_task("delegate unknown_employee some_task")
        assert "not found" in result.lower()

    @mock.patch("superman.SupermanOrchestrator._run_subprocess")
    def test_delegate_task_success(self, mock_subprocess):
        """Test successful task delegation."""
        # Mock subprocess result
        mock_result = mock.MagicMock()
        mock_result.stdout = "Test output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result

        # Ensure we have at least one employee
        if not self.orchestrator.employees:
            self.orchestrator.employees["test_employee"] = {
                "path": "/test/path.py",
                "type": "python",
                "description": "Test employee",
                "name": "test_employee",
            }

        employee_name = list(self.orchestrator.employees.keys())[0]
        result = self.orchestrator.delegate_task(f"delegate {employee_name} test_task")

        assert "successfully" in result.lower()
        mock_subprocess.assert_called_once()

    def test_spacy_installation_check(self):
        """Test that spaCy installation check runs without error."""
        with mock.patch("builtins.print") as mock_print:
            self.orchestrator.check_spacy_installation()
            # Should have printed some spaCy status
            mock_print.assert_called()

    def test_openai_connectivity_check(self):
        """Test that OpenAI connectivity check runs without error."""
        with mock.patch("builtins.print") as mock_print:
            self.orchestrator.check_openai_connectivity()
            # Should have printed some OpenAI status
            mock_print.assert_called()

    def test_internet_connectivity_check_available(self):
        """Test internet connectivity check when internet is available."""
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            # Mock successful connection
            mock_response = mock.MagicMock()
            mock_response.status = 200
            mock_urlopen.return_value.__enter__.return_value = mock_response

            with mock.patch("builtins.print") as mock_print:
                result = self.orchestrator.check_internet_connectivity()

                # Should return True for available internet
                assert result is True
                assert self.orchestrator.internet_available is True

                # Should print availability message
                print_calls = [str(call) for call in mock_print.call_args_list]
                availability_found = any(
                    "Internet access: AVAILABLE" in call for call in print_calls
                )
                assert availability_found

    def test_internet_connectivity_check_unavailable(self):
        """Test internet connectivity check when internet is not available."""
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            # Mock network error
            mock_urlopen.side_effect = urllib.error.URLError("Network unreachable")

            with mock.patch("builtins.print") as mock_print:
                result = self.orchestrator.check_internet_connectivity()

                # Should return False for unavailable internet
                assert result is False
                assert self.orchestrator.internet_available is False

                # Should print unavailability and warning messages
                print_calls = [str(call) for call in mock_print.call_args_list]
                unavailable_found = any(
                    "Internet access: NOT AVAILABLE" in call for call in print_calls
                )
                warning_found = any(
                    "Operating in offline/limited mode" in call for call in print_calls
                )
                assert unavailable_found
                assert warning_found

    def test_internet_connectivity_check_dns_error(self):
        """Test internet connectivity check with DNS resolution errors."""
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            # Mock DNS error
            mock_urlopen.side_effect = urllib.error.URLError(
                "[Errno -5] No address associated with hostname"
            )

            with mock.patch("builtins.print") as mock_print:
                result = self.orchestrator.check_internet_connectivity()

                # Should return False and provide actionable error info
                assert result is False

                # Should show DNS error details
                print_calls = [str(call) for call in mock_print.call_args_list]
                dns_error_found = any(
                    "No address associated with hostname" in call
                    for call in print_calls
                )
                assert dns_error_found


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
                success_found = any(
                    "OpenAI integration enabled" in call for call in print_calls
                )
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
                warning_found = any(
                    "does not start with 'sk-'" in call for call in print_calls
                )
                assert warning_found

    @mock.patch("builtins.print")
    def test_debug_status_display(self, mock_print):
        """Test that debug mode is shown in status display."""
        with mock.patch.dict(
            os.environ, {"OPENAI_API_KEY": "sk-test123", "SUPERMAN_DEBUG": "1"}
        ):
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

        with mock.patch.dict(
            os.environ, {"OPENAI_API_KEY": "sk-test123", "SUPERMAN_DEBUG": "1"}
        ):
            orch = SupermanOrchestrator()
            orch.intent_recognizer = mock.MagicMock()
            orch.running = True
            orch.history = []
            orch.action_handlers = {}
            orch.superman_mode = True

            # Mock OpenAI client to raise API key error
            mock_client = mock.MagicMock()
            orch.openai_client = mock_client
            mock_client.chat.completions.create.side_effect = Exception(
                "Incorrect API key provided"
            )

            test_intent = Intent(
                IntentType.AI_CHAT, confidence=0.9, original_input="test question"
            )

            with mock.patch("builtins.print") as mock_print:
                result = orch.handle_ai_chat_enhanced(test_intent)

                print_calls = [str(call) for call in mock_print.call_args_list]

                # Should provide specific guidance for API key errors
                guidance_found = any(
                    "This suggests an issue with your OpenAI API key" in call
                    for call in print_calls
                )
                assert guidance_found

                # Should provide troubleshooting checklist
                checklist_found = any(
                    "Please check that:" in call for call in print_calls
                )
                assert checklist_found


class TestOpenAIFirstArchitecture:
    """Test suite for validating the OpenAI-first processing architecture."""

    def setup_method(self):
        """Set up test fixtures."""
        with mock.patch(
            "superman.create_intent_recognizer"
        ) as mock_recognizer, mock.patch(
            "superman.SuperhumanTerminal.__init__"
        ) as mock_init:
            mock_init.return_value = None
            self.orchestrator = SupermanOrchestrator()

            # Manually set required attributes
            self.orchestrator.intent_recognizer = mock.MagicMock()
            self.orchestrator.running = True
            self.orchestrator.history = []
            self.orchestrator.action_handlers = {}
            self.orchestrator.memory = MemorySystem()

    @mock.patch("builtins.print")
    def test_openai_unavailable_shows_clear_error_and_setup_instructions(
        self, mock_print
    ):
        """Test that when OpenAI is unavailable, clear setup instructions are shown."""
        # Ensure no OpenAI client
        self.orchestrator.openai_client = None

        # Mock input to simulate user interaction once, then stop
        with mock.patch(
            "builtins.input", side_effect=["test query", KeyboardInterrupt()]
        ):
            try:
                self.orchestrator.run()
            except KeyboardInterrupt:
                pass  # Expected to break out of loop

        # Verify error message and setup instructions were shown
        print_calls = [str(call) for call in mock_print.call_args_list]

        # Should show OpenAI not available error
        error_found = any(
            "OpenAI integration not available" in call for call in print_calls
        )
        assert error_found

        # Should show setup instructions
        setup_found = any("To enable AI orchestration:" in call for call in print_calls)
        assert setup_found

        # Should show pip install instruction
        pip_found = any("pip install openai" in call for call in print_calls)
        assert pip_found

        # Should show API key instruction
        api_key_found = any("export OPENAI_API_KEY" in call for call in print_calls)
        assert api_key_found

    @mock.patch("builtins.print")
    def test_openai_available_always_used_for_all_queries(self, mock_print):
        """Test that when OpenAI is available, ALL queries go through it."""
        # Set up OpenAI client
        mock_client = mock.MagicMock()
        self.orchestrator.openai_client = mock_client

        # Mock OpenAI response (direct response, not delegation)
        mock_response = mock.MagicMock()
        mock_response.choices = [mock.MagicMock()]
        mock_response.choices[0].message.content = (
            "This is OpenAI's response to your query."
        )
        mock_client.chat.completions.create.return_value = mock_response

        # Mock input to simulate user interaction once, then stop
        with mock.patch(
            "builtins.input", side_effect=["what is the weather?", KeyboardInterrupt()]
        ):
            try:
                self.orchestrator.run()
            except KeyboardInterrupt:
                pass  # Expected to break out of loop

        # Verify OpenAI was called
        mock_client.chat.completions.create.assert_called_once()

        # Verify OpenAI response was displayed
        print_calls = [str(call) for call in mock_print.call_args_list]
        response_found = any(
            "🤖 This is OpenAI's response" in call for call in print_calls
        )
        assert response_found

    def test_process_with_openai_no_fallback_on_errors(self):
        """Test that _process_with_openai provides error messages instead of falling back."""
        # Set up OpenAI client that will fail
        mock_client = mock.MagicMock()
        self.orchestrator.openai_client = mock_client

        # Mock API key error
        mock_client.chat.completions.create.side_effect = Exception(
            "Incorrect API key provided"
        )

        is_delegation, response = self.orchestrator._process_with_openai("test query")

        # Should not be delegation
        assert is_delegation is False

        # Should provide detailed error message instead of empty string
        assert response.startswith("❌ OpenAI request failed:")
        assert "This suggests an issue with your OpenAI API key" in response
        assert "Please check that:" in response

    def test_process_with_openai_handles_empty_responses(self):
        """Test that empty OpenAI responses are handled gracefully."""
        # Set up OpenAI client
        mock_client = mock.MagicMock()
        self.orchestrator.openai_client = mock_client

        # Mock empty response
        mock_response = mock.MagicMock()
        mock_response.choices = [mock.MagicMock()]
        mock_response.choices[0].message.content = ""  # Empty response
        mock_client.chat.completions.create.return_value = mock_response

        is_delegation, response = self.orchestrator._process_with_openai("test query")

        # Should not be delegation
        assert is_delegation is False

        # Should provide a helpful fallback message
        assert "I apologize, but I couldn't generate a response" in response
        assert "Please try rephrasing" in response

    def test_enhanced_ai_chat_handler_openai_first(self):
        """Test that enhanced AI chat handler uses OpenAI first when available."""
        from ai_script_inventory.ai.intent import Intent, IntentType

        # Set up OpenAI client
        mock_client = mock.MagicMock()
        self.orchestrator.openai_client = mock_client

        # Mock OpenAI response
        mock_response = mock.MagicMock()
        mock_response.choices = [mock.MagicMock()]
        mock_response.choices[0].message.content = "OpenAI handled this query."
        mock_client.chat.completions.create.return_value = mock_response

        # Create test intent
        test_intent = Intent(
            IntentType.AI_CHAT, confidence=0.9, original_input="test question"
        )

        with mock.patch("builtins.print") as mock_print:
            self.orchestrator.handle_ai_chat_enhanced(test_intent)

        # Verify OpenAI was called
        mock_client.chat.completions.create.assert_called_once()

        # Verify OpenAI response was displayed
        print_calls = [str(call) for call in mock_print.call_args_list]
        response_found = any(
            "🤖 OpenAI handled this query" in call for call in print_calls
        )
        assert response_found

    @mock.patch("builtins.print")
    def test_enhanced_ai_chat_handler_fallback_only_when_no_openai(self, mock_print):
        """Test that enhanced AI chat handler only falls back when OpenAI is completely unavailable."""
        from ai_script_inventory.ai.intent import Intent, IntentType

        # Ensure no OpenAI client
        self.orchestrator.openai_client = None

        # Mock the parent handle_ai_chat method
        self.orchestrator.handle_ai_chat = mock.MagicMock()

        # Create test intent
        test_intent = Intent(
            IntentType.AI_CHAT, confidence=0.9, original_input="test question"
        )

        self.orchestrator.handle_ai_chat_enhanced(test_intent)

        # Should show fallback message
        print_calls = [str(call) for call in mock_print.call_args_list]
        fallback_found = any(
            "OpenAI unavailable, using local chat handler" in call
            for call in print_calls
        )
        assert fallback_found

        # Should call parent handler
        self.orchestrator.handle_ai_chat.assert_called_once_with(test_intent)


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
