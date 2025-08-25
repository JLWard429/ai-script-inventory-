---
applyTo: "python_scripts/**/*.py"
---

# Python Scripts Instructions

When working with Python scripts in the `python_scripts/` directory, follow these specific guidelines:

## Code Quality Standards

1. **Formatting and Style**
   - Use Black formatting with line length 88
   - Follow PEP 8 style guidelines
   - Use isort for import organization with Black profile
   - Add type hints for function parameters and return values

2. **Documentation Requirements**
   - Include module-level docstring at the top of each file
   - Add docstrings for all public functions and classes
   - Use Google-style or NumPy-style docstring format
   - Include usage examples in docstrings for complex functions

3. **Error Handling**
   - Use specific exception types rather than bare `except:`
   - Add appropriate logging for errors and important operations
   - Validate input parameters and provide meaningful error messages

## Security Considerations

1. **Input Validation**
   - Sanitize all user inputs and file paths
   - Use pathlib.Path for file operations to prevent path traversal
   - Validate data types and ranges for numeric inputs

2. **Sensitive Data**
   - Never hardcode API keys, passwords, or sensitive information
   - Use environment variables or configuration files for secrets
   - Add appropriate bandit security annotations if needed

## Script Organization

1. **File Structure**
   - Use clear, descriptive filenames that indicate functionality
   - Keep scripts focused on a single responsibility
   - Use helper functions to break down complex operations

2. **Dependencies**
   - Import only necessary modules
   - Prefer standard library modules when possible
   - Document any external dependencies in docstrings

## Testing Requirements

1. **Unit Tests**
   - Create corresponding test files in `tests/` directory
   - Test both successful execution and error conditions
   - Use descriptive test function names that explain what's being tested

2. **Integration**
   - Ensure scripts work with the automation system
   - Test compatibility with the organization script
   - Verify scripts can be executed from different working directories

## AI Terminal Integration

When creating scripts for the Superhuman AI Terminal:

1. **Command Interface**
   - Support command-line arguments for automation
   - Provide help text and usage information
   - Return appropriate exit codes

2. **Privacy Protection**
   - Ensure all processing happens locally
   - Avoid any cloud API calls or external data transmission
   - Log only necessary information locally

## Example Template

```python
#!/usr/bin/env python3
"""
Module description here.

This script does X, Y, and Z. It can be used for...

Usage:
    python script_name.py [options]

Example:
    python script_name.py --input file.txt --output result.txt
"""

import argparse
import logging
from pathlib import Path
from typing import Optional, Union


def setup_logging() -> None:
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main_function(input_path: Path, output_path: Optional[Path] = None) -> bool:
    """
    Main function description.
    
    Args:
        input_path: Path to input file
        output_path: Optional path to output file
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input data is invalid
    """
    # Implementation here
    pass


def main() -> None:
    """Entry point for command-line usage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Input file path')
    parser.add_argument('--output', type=Path, help='Output file path')
    
    args = parser.parse_args()
    
    setup_logging()
    
    try:
        success = main_function(args.input, args.output)
        exit(0 if success else 1)
    except Exception as e:
        logging.error(f"Script failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
```