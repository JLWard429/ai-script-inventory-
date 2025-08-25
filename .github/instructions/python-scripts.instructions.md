---
applyTo: "python_scripts/**/*.py"
---

# Python Scripts Instructions

When working with Python scripts in the `python_scripts/` directory, follow these specific guidelines:

## Script Structure

### Shebang and Encoding
```python
#!/usr/bin/env python3
"""
Module docstring describing the script's purpose.

Detailed description of what the script does, its main functionality,
and any important usage notes.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
```

### Main Function Pattern
```python
def main() -> None:
    """Main function for the script."""
    parser = argparse.ArgumentParser(
        description="Brief description of the script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python script_name.py --option value    # Example usage
  python script_name.py --help           # Show help
        """,
    )
    
    # Add arguments
    parser.add_argument(
        "positional_arg",
        help="Description of the positional argument"
    )
    
    parser.add_argument(
        "--option", "-o",
        default="default_value",
        help="Description of the option"
    )
    
    args = parser.parse_args()
    
    # Main logic here
    try:
        result = do_work(args)
        if result:
            print("✅ Operation completed successfully")
            sys.exit(0)
        else:
            print("❌ Operation failed")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Development Tools Integration

### Using the Development Tools Pattern
Follow the pattern established in `dev_tools.py`:

```python
def run_command(command: List[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
```

### Progress Indicators
Use emoji and clear messages for user feedback:
- 🔄 for operations in progress
- ✅ for successful operations
- ❌ for failed operations
- 🚀 for starting major operations
- 🎉 for completion

## Code Quality Standards

### Type Hints
```python
from typing import List, Dict, Optional, Union, Any

def process_files(file_paths: List[Path]) -> Dict[str, bool]:
    """Process multiple files and return success status for each."""
    results: Dict[str, bool] = {}
    
    for file_path in file_paths:
        results[str(file_path)] = process_single_file(file_path)
    
    return results

def process_single_file(file_path: Path) -> bool:
    """Process a single file."""
    if not file_path.exists():
        return False
    
    # Processing logic
    return True
```

### Error Handling
```python
def safe_file_operation(file_path: Path) -> Optional[str]:
    """Safely read a file with proper error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except PermissionError:
        print(f"❌ Permission denied: {file_path}")
        return None
    except UnicodeDecodeError:
        print(f"❌ Unable to decode file: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error reading {file_path}: {e}")
        return None
```

### Path Handling
```python
from pathlib import Path

def organize_files(source_dir: Path, target_dir: Path) -> bool:
    """Organize files from source to target directory."""
    # Always use Path objects
    source_dir = Path(source_dir)
    target_dir = Path(target_dir)
    
    # Create directories if they don't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Use glob for file discovery
    for file_path in source_dir.glob("**/*.py"):
        relative_path = file_path.relative_to(source_dir)
        target_path = target_dir / relative_path
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move or copy file
        file_path.rename(target_path)
    
    return True
```

## Documentation Standards

### Docstrings
```python
def complex_function(
    input_data: List[Dict[str, Any]], 
    options: Optional[Dict[str, str]] = None
) -> Dict[str, List[str]]:
    """
    Process complex input data with optional configuration.
    
    Args:
        input_data: List of dictionaries containing data to process.
                   Each dict should have 'name' and 'type' keys.
        options: Optional configuration dict. Supported keys:
                - 'format': Output format ('json' or 'yaml')
                - 'verbose': Enable verbose output ('true' or 'false')
    
    Returns:
        Dictionary mapping categories to lists of processed items.
    
    Raises:
        ValueError: If input_data is empty or contains invalid items.
        TypeError: If input_data items don't have required keys.
    
    Example:
        >>> data = [{'name': 'test', 'type': 'script'}]
        >>> result = complex_function(data)
        >>> print(result)
        {'script': ['test']}
    """
    if not input_data:
        raise ValueError("input_data cannot be empty")
    
    # Implementation here
    return {}
```

## Integration with Repository Automation

### File Organization
- Scripts should be self-contained in the `python_scripts/` directory
- Use relative imports when referencing other modules in the same directory
- Keep configuration and data files separate from scripts

### Testing Integration
- Each script should have corresponding tests in `tests/test_script_name.py`
- Include tests for command-line argument parsing
- Test both success and failure scenarios

### Security Considerations
- Validate all user inputs
- Use subprocess.run() with proper arguments for shell commands
- Never use shell=True unless absolutely necessary
- Sanitize file paths and names

### Performance
- Use generators for large data processing
- Implement progress bars for long-running operations
- Cache expensive computations when appropriate

```python
from tqdm import tqdm

def process_large_dataset(items: List[Any]) -> List[Any]:
    """Process a large dataset with progress indication."""
    results = []
    
    for item in tqdm(items, desc="Processing items"):
        result = expensive_operation(item)
        results.append(result)
    
    return results
```

## Command Line Interface Best Practices

### Argument Groups
```python
parser = argparse.ArgumentParser(description="Script description")

# Required arguments group
required = parser.add_argument_group('required arguments')
required.add_argument('--input', required=True, help='Input file path')

# Optional arguments group
optional = parser.add_argument_group('optional arguments')
optional.add_argument('--output', help='Output file path')
optional.add_argument('--verbose', action='store_true', help='Enable verbose output')
```

### Validation
```python
def validate_args(args: argparse.Namespace) -> bool:
    """Validate command line arguments."""
    if args.input and not Path(args.input).exists():
        print(f"❌ Input file does not exist: {args.input}")
        return False
    
    if args.output and Path(args.output).exists():
        response = input(f"Output file exists: {args.output}. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled")
            return False
    
    return True
```