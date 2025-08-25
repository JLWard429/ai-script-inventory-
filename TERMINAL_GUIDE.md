# Superhuman AI Terminal - Developer Guide

## Overview

The Superhuman AI Terminal provides a natural language interface to interact with the AI Script Inventory repository. It now uses **spaCy** for advanced natural language processing and intent recognition, offering enhanced understanding of user requests without requiring cloud services.

## Architecture

### Components

1. **Enhanced Intent Recognition** (`ai/intent.py`)
   - **Primary**: Uses spaCy NLP library for advanced linguistic analysis
   - **Fallback**: Keyword and pattern matching for compatibility
   - **Features**: Named entity recognition, dependency parsing, linguistic analysis
   - **Privacy**: Local-only processing (no cloud dependencies)

2. **Terminal Interface** (`superhuman_terminal.py`)
   - Main terminal loop and user interaction
   - Action handlers for each intent type
   - **NEW**: AI Chat handler for conversational assistance
   - File operations and script execution

3. **Launcher** (`terminal.py`)
   - Simple entry point for users

## New Features with spaCy Integration

### Enhanced Intent Recognition
- **Better Natural Language Understanding**: Can handle more complex, conversational inputs
- **Entity Extraction**: Automatically identifies files, directories, and parameters
- **Confidence Scoring**: Improved accuracy in intent detection
- **Linguistic Analysis**: Uses parts of speech, dependency parsing, and semantic understanding

### AI Chat Capability
- **Conversational Interface**: Answer general questions about the repository
- **Contextual Help**: Provide guidance on best practices and workflows
- **Discovery Assistance**: Help users understand available features and tools
- **Repository Information**: Explain project structure and capabilities

### Advanced Query Support
Examples of enhanced natural language queries:
- `"Summarize the latest README"`
- `"Run security scan on all Python files in shell_scripts"`
- `"Show me the contents of my AI scripts"`
- `"What are the best practices for organizing scripts?"`
- `"How do I get started with this repository?"`

## Adding New Intents

To add a new intent type with spaCy integration:

### 1. Define the Intent Type

Add to `IntentType` enum in `ai/intent.py`:

```python
class IntentType(Enum):
    # ... existing intents
    NEW_INTENT = "new_intent"
    AI_CHAT = "ai_chat"  # NEW: For conversational assistance
```

### 2. Add spaCy Pattern Recognition

Add patterns to `_setup_spacy_patterns()` in `IntentRecognizer`:

```python
# New intent patterns for spaCy matcher
new_intent_patterns = [
    [{"LOWER": {"IN": ["keyword1", "keyword2"]}}, {"IS_ALPHA": True}],
    [{"LOWER": "action"}, {"TEXT": {"REGEX": r".*\.(py|sh)$"}}],
    [{"POS": "VERB"}, {"LOWER": "something"}]
]
self.matcher.add("NEW_INTENT", new_intent_patterns)
```

### 3. Add Fallback Pattern Recognition

Add patterns to `_build_intent_patterns()` for fallback compatibility:

```python
IntentType.NEW_INTENT: [
    {'keywords': ['keyword1', 'keyword2'], 'weight': 1.0},
    {'patterns': [r'\bpattern\s+\w+'], 'weight': 0.9},
    {'context_keywords': ['context1', 'context2'], 'weight': 0.3},
],
```

### 4. Update Intent Mapping

Add to `_map_spacy_intent()` method:

```python
mapping = {
    # ... existing mappings
    "NEW_INTENT": IntentType.NEW_INTENT,
}
```

### 5. Implement Handler

Add handler method to `SuperhumanTerminal`:

```python
def handle_new_intent(self, intent: Intent):
    """Handle new intent requests."""
    # Implementation here
    pass

def handle_ai_chat(self, intent: Intent):
    """Handle conversational AI chat requests."""
    # Provide contextual assistance
    pass
```

### 6. Register Handler

Add to `action_handlers` dict in `__init__`:

```python
self.action_handlers = {
    # ... existing handlers
    IntentType.NEW_INTENT: self.handle_new_intent,
    IntentType.AI_CHAT: self.handle_ai_chat,
}
```

## Intent Recognition Details

### spaCy-Enhanced Recognition

1. **Linguistic Patterns**: Uses parts of speech, dependency parsing
2. **Named Entity Recognition**: Automatically extracts entities
3. **Token Matching**: Advanced pattern matching with linguistic features
4. **Contextual Analysis**: Understands sentence structure and meaning

### Fallback Pattern Types

1. **Keywords**: Exact word matches
2. **Regex Patterns**: Regular expression matching  
3. **Context Keywords**: Bonus scoring for related terms

### Confidence Scoring

- **spaCy Primary**: Enhanced scoring using linguistic analysis
- **Pattern Matches**: Weighted combination of pattern types
- **Entity Bonuses**: Additional confidence for recognized entities
- **Fallback**: Traditional keyword/regex scoring when spaCy unavailable

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
🤖 > summarize the latest README   # Enhanced natural language
```

### AI Chat and Conversational Assistance

```
🤖 > what can you do?                    # Get capability overview
🤖 > how do I get started?              # Getting started guidance
🤖 > what is this repository about?     # Repository information
🤖 > what are the best practices?       # Best practices advice
🤖 > tell me about spaCy integration    # Technical information
```

## AI Chat Feature

The terminal now includes an AI Chat capability that provides conversational assistance:

### Types of Questions Supported

1. **Repository Information**
   - "What is this repository about?"
   - "What can you do?"
   - "How is this repository organized?"

2. **Getting Started**
   - "How do I get started?"
   - "What should I do first?"
   - "Show me the first steps"

3. **Best Practices**
   - "What are the best practices for organizing scripts?"
   - "How should I manage my files?"
   - "What's the recommended workflow?"

4. **Technical Information**
   - "Tell me about spaCy integration"
   - "How does the natural language processing work?"
   - "What are the privacy features?"

### How to Use AI Chat

Simply ask questions in natural language. The system will:
- Recognize conversational patterns
- Provide contextual, helpful responses
- Guide you to relevant features and documentation
- Offer actionable advice and tips

Examples:
- Questions starting with "what", "how", "why"
- Requests for advice or recommendations
- General inquiries about the system

## spaCy Integration Features

### Enhanced Natural Language Understanding

- **Entity Recognition**: Automatically identifies files, directories, parameters
- **Dependency Parsing**: Understands sentence structure and relationships  
- **Part-of-Speech Analysis**: Uses grammatical information for better recognition
- **Confidence Scoring**: More accurate intent classification

### Advanced Query Examples

```bash
# Complex parameter extraction
"Run security scan on all Python files in shell_scripts"
→ Intent: run_script, Target: shell_scripts, Params: {scope: all, file_type: python, directory: shell_scripts}

# Contextual summarization
"Summarize the latest README"  
→ Intent: summarize, Target: None, Params: {scope: latest}

# Natural file operations
"Show me the contents of my AI scripts"
→ Intent: show, Target: None, Params: {}
```

### Privacy and Performance

- **Local Processing**: All spaCy operations happen locally
- **No Cloud Dependencies**: No data sent to external services
- **Fallback Support**: Automatically falls back to keyword matching if spaCy unavailable
- **Fast Response**: Efficient processing with cached models

## Extension Ideas

- Add git operation intents (commit, status, diff)
- Integrate with external tools (linters, formatters)
- Add batch operations (run multiple scripts)
- Support for more file types
- Advanced search with regex
- File modification intents (edit, create)
- **NEW**: Enhanced conversational AI with domain-specific knowledge
- **NEW**: Multi-language support for spaCy models
- **NEW**: Custom entity recognition for project-specific terms

## Safety Features

- Read-only operations by default
- Confirmation for destructive actions
- Sandboxed script execution
- No network dependencies
- Local-only processing