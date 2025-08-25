---
applyTo: "tests/**/*.py"
---

# Test File Instructions

When working with test files in this repository, follow these specific guidelines:

## Test Structure and Naming

1. **File Naming**: Use `test_*.py` pattern for all test files
2. **Function Naming**: Test functions should be descriptive and start with `test_`
3. **Class Naming**: Test classes should start with `Test` and describe what they test

## Testing Framework

Use pytest with the following conventions:

### Basic Test Structure
```python
"""Tests for [module/functionality description]."""

import pytest
from pathlib import Path
# Other imports...

def test_specific_functionality():
    """Test that [specific functionality] works as expected."""
    # Arrange
    test_input = "sample data"
    
    # Act
    result = function_under_test(test_input)
    
    # Assert
    assert result == expected_output
```

### Error Testing
```python
def test_error_handling():
    """Test that function handles errors gracefully."""
    with pytest.raises(ValueError, match="expected error message"):
        function_under_test(invalid_input)
```

### File and Path Testing
```python
def test_file_operations():
    """Test file operations."""
    # Use Path objects for file paths
    test_file = Path("path/to/test/file")
    assert test_file.exists()
    assert test_file.stat().st_size > 0
```

## Test Categories

### Unit Tests
- Test individual functions and methods
- Use mocking for external dependencies
- Keep tests fast and isolated

### Integration Tests
- Test interactions between components
- Use real files and directories when appropriate
- Test the development tools integration

### Syntax and Configuration Tests
- Test that Python files have valid syntax
- Test that YAML/JSON configurations are valid
- Test that required files exist

## Test Data and Fixtures

### Temporary Files
```python
import tempfile

def test_with_temp_file():
    """Test using temporary files."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as temp_file:
        temp_file.write("test content")
        temp_file.flush()
        # Test operations on temp_file.name
```

### pytest Fixtures
```python
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using pytest fixture."""
    assert sample_data["key"] == "value"
```

## Repository-Specific Test Requirements

### Development Tools Testing
- Test that `dev_tools.py` commands work correctly
- Test help text and argument parsing
- Test that all required development dependencies are available

### Directory Structure Testing
- Verify expected directories exist
- Check that README files are present in main directories
- Validate directory organization

### Configuration Testing
- Test `pyproject.toml` syntax and required sections
- Test `.pre-commit-config.yaml` validity
- Test workflow YAML files

### Code Quality Testing
- Test that all Python files have valid syntax
- Test that all files follow project standards
- Test that security scans pass

## Performance Considerations

- Keep tests fast (< 1 second per test when possible)
- Use appropriate test isolation
- Mock external dependencies and network calls
- Use parametrized tests for multiple similar test cases

## Documentation

- Include docstrings for all test functions
- Explain complex test setup or assertions
- Document any test-specific requirements or assumptions

## Error Messages

- Use descriptive assertion messages
- Include context about what was expected vs actual
- Use pytest's built-in assertion introspection when possible

Example:
```python
assert result == expected, f"Expected {expected}, got {result}"
```