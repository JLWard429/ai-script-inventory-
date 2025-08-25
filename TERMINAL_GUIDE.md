# Superhuman AI Terminal - Developer Guide

## Overview

The Superhuman AI Terminal provides a natural language interface to interact with the AI Script Inventory repository. It uses local intent recognition to map user requests to actions without requiring cloud services.

## Architecture

### Components

1. **Intent Recognition** (`ai/intent.py`)
   - Maps natural language to structured intents
   - Uses keyword and pattern matching
   - Local-only processing (no cloud dependencies)

2. **Terminal Interface** (`superhuman_terminal.py`)
   - Main terminal loop and user interaction
   - Action handlers for each intent type
   - File operations and script execution

3. **Launcher** (`terminal.py`)
   - Simple entry point for users

## Adding New Intents

To add a new intent type:

### 1. Define the Intent Type

Add to `IntentType` enum in `ai/intent.py`:

```python
class IntentType(Enum):
    # ... existing intents
    NEW_INTENT = "new_intent"
```

### 2. Add Pattern Recognition

Add patterns to `_build_intent_patterns()` in `IntentRecognizer`:

```python
IntentType.NEW_INTENT: [
    {'keywords': ['keyword1', 'keyword2'], 'weight': 1.0},
    {'patterns': [r'\bpattern\s+\w+'], 'weight': 0.9},
    {'context_keywords': ['context1', 'context2'], 'weight': 0.3},
],
```

### 3. Implement Handler

Add handler method to `SuperhumanTerminal`:

```python
def handle_new_intent(self, intent: Intent):
    """Handle new intent requests."""
    # Implementation here
    pass
```

### 4. Register Handler

Add to `action_handlers` dict in `__init__`:

```python
self.action_handlers = {
    # ... existing handlers
    IntentType.NEW_INTENT: self.handle_new_intent,
}
```

## Intent Recognition Details

### Pattern Types

1. **Keywords**: Exact word matches
2. **Regex Patterns**: Regular expression matching
3. **Context Keywords**: Bonus scoring for related terms

### Confidence Scoring

- Patterns are weighted and combined
- Final confidence is clamped to [0.0, 1.0]
- Minimum confidence threshold: 0.3
- Confirmation threshold: 0.5

### Parameter Extraction

The system automatically extracts:
- File targets (with extensions)
- File types (python, shell, markdown, etc.)
- Scope indicators (all, recent)
- Directory specifications

## File Operations

### Supported File Types

- Python scripts (`.py`)
- Shell scripts (`.sh`)
- Markdown documents (`.md`)
- Text files (`.txt`)
- PDF documents (`.pdf`)

### Search Directories

- Root directory (`.`)
- `python_scripts/`
- `shell_scripts/`
- `docs/`
- `text_files/`
- `.github/scripts/`

## Testing

Run the test suite:

```bash
python test_terminal.py
```

Test specific functionality interactively:

```bash
python terminal.py
```

## Examples

### Basic Commands

```
🤖 > help                          # Show help
🤖 > exit                          # Exit terminal
```

### Script Execution

```
🤖 > run test_script.py             # Run Python script
🤖 > run organize_ai_scripts        # Run organization script
```

### File Operations

```
🤖 > list all Python files         # List by type
🤖 > show README.md                # Display content
🤖 > preview document.md           # Quick preview
🤖 > search for test               # Search content
```

### Document Analysis

```
🤖 > summarize CONTRIBUTING.md     # Create summary
```

## Extension Ideas

- Add git operation intents (commit, status, diff)
- Integrate with external tools (linters, formatters)
- Add batch operations (run multiple scripts)
- Support for more file types
- Advanced search with regex
- File modification intents (edit, create)

## Safety Features

- Read-only operations by default
- Confirmation for destructive actions
- Sandboxed script execution
- No network dependencies
- Local-only processing