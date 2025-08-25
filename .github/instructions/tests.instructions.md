---
applyTo: "tests/**/*.py"
---

# Test Files Instructions

When writing tests in the `tests/` directory, follow these guidelines for comprehensive and maintainable test coverage:

## Testing Framework and Structure

1. **Use pytest**
   - All tests should be compatible with pytest
   - Use pytest fixtures for setup and teardown
   - Leverage pytest's powerful assertion features
   - Use parametrize for testing multiple scenarios

2. **File Organization**
   - Name test files with `test_` prefix (e.g., `test_module_name.py`)
   - Mirror the structure of the code being tested
   - Group related tests in the same file
   - Use descriptive test function names that explain what's being tested

## Test Quality Standards

1. **Test Coverage**
   - Aim for comprehensive coverage of new functionality
   - Test both successful execution and error conditions
   - Include edge cases and boundary conditions
   - Test integration points and dependencies

2. **Test Independence**
   - Each test should be independent and able to run in isolation
   - Use fixtures or setup/teardown for test data
   - Avoid dependencies between test functions
   - Clean up any created files or resources

## Specific Testing Patterns

1. **Script Testing**
   - Test Python scripts for syntax validity using `compile()`
   - Test command-line interfaces and argument parsing
   - Verify script outputs and return codes
   - Test script behavior with invalid inputs

2. **File Operation Testing**
   - Use temporary directories for file operation tests
   - Test file creation, modification, and deletion
   - Verify file permissions and ownership when relevant
   - Test behavior with missing or inaccessible files

3. **Configuration Testing**
   - Validate YAML/JSON configuration files
   - Test configuration parsing and validation
   - Verify default values and required fields
   - Test configuration error handling

## Example Test Patterns

```python
"""
Test module for example_script.py functionality.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from python_scripts.example_script import main_function, validate_input


class TestMainFunction:
    """Test cases for main_function."""
    
    def test_successful_execution(self, tmp_path):
        """Test successful execution with valid inputs."""
        input_file = tmp_path / "input.txt"
        input_file.write_text("test content")
        output_file = tmp_path / "output.txt"
        
        result = main_function(input_file, output_file)
        
        assert result is True
        assert output_file.exists()
    
    def test_missing_input_file(self, tmp_path):
        """Test behavior when input file doesn't exist."""
        nonexistent_file = tmp_path / "missing.txt"
        
        with pytest.raises(FileNotFoundError):
            main_function(nonexistent_file)
    
    @pytest.mark.parametrize("invalid_input", [
        "",
        "   ",
        None,
    ])
    def test_invalid_input_handling(self, invalid_input, tmp_path):
        """Test handling of various invalid inputs."""
        input_file = tmp_path / "input.txt"
        input_file.write_text(invalid_input or "")
        
        with pytest.raises(ValueError):
            main_function(input_file)


class TestValidateInput:
    """Test cases for input validation."""
    
    def test_valid_input(self):
        """Test validation of valid input."""
        result = validate_input("valid content")
        assert result is True
    
    def test_empty_input(self):
        """Test validation rejects empty input."""
        result = validate_input("")
        assert result is False


# Integration tests
class TestScriptIntegration:
    """Integration tests for script execution."""
    
    def test_script_syntax_valid(self):
        """Test that the script has valid Python syntax."""
        script_path = Path("python_scripts/example_script.py")
        
        with open(script_path) as f:
            compile(f.read(), script_path, 'exec')
    
    def test_command_line_interface(self, tmp_path):
        """Test command-line interface functionality."""
        input_file = tmp_path / "test_input.txt"
        input_file.write_text("test content")
        
        # Test using subprocess or direct function call
        # depending on script structure
        pass


# Fixtures for common test setup
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "valid_content": "This is valid test content",
        "invalid_content": "",
        "special_chars": "Content with special chars: !@#$%^&*()",
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace for file operations."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace
```

## Security Testing

1. **Input Sanitization**
   - Test with malicious inputs (path traversal, injection attempts)
   - Verify proper sanitization of user inputs
   - Test handling of special characters and encoding

2. **File Security**
   - Test file permission handling
   - Verify no sensitive data leaks in test outputs
   - Test behavior with restricted file access

## Performance Testing

1. **Resource Usage**
   - Test memory usage for large files or datasets
   - Verify reasonable execution times
   - Test behavior under resource constraints

2. **Scalability**
   - Test with varying input sizes
   - Verify graceful handling of large datasets
   - Test concurrent execution if applicable

## Continuous Integration Compatibility

1. **Environment Independence**
   - Tests should work across different Python versions
   - Avoid platform-specific assumptions
   - Use appropriate skips for platform-specific tests

2. **Resource Cleanup**
   - Always clean up temporary files and resources
   - Use context managers for file operations
   - Avoid leaving test artifacts in the repository

## Error Testing Guidelines

1. **Exception Handling**
   - Test that appropriate exceptions are raised
   - Verify exception messages are helpful
   - Test exception handling in different scenarios

2. **Logging Validation**
   - Verify appropriate log messages are generated
   - Test log levels and formatting
   - Ensure no sensitive data in logs