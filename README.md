[![Code Quality & Security](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/code-quality.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/code-quality.yml)
[![CI Passing](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions)
[![CodeQL Security Analysis](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/codeql.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/security/code-scanning)
[![Security Scanning](https://github.com/JLWard429/ai-script-inventory-/actions/workflows/dependency-scan.yml/badge.svg)](https://github.com/JLWard429/ai-script-inventory-/actions)
[![Powered by Copilot](https://img.shields.io/badge/powered%20by-copilot-blue?logo=github)](https://github.com/features/copilot)

# 🤖 AI Script Inventory

A professional, enterprise-grade repository for organizing and managing AI-related scripts with comprehensive automation, security analysis, and quality controls.

This repository contains a collection of AI-related scripts and features the **Superhuman AI Terminal** — a privacy-friendly, local-only AI terminal interface powered by spaCy for advanced natural language understanding.

---

## 🚀 Superhuman AI Terminal

The Superhuman AI Terminal provides a natural language interface to interact with your AI script inventory. It uses spaCy for advanced intent recognition and entity extraction (no cloud LLMs required) to understand and execute your requests with high precision.

### Quick Start

```bash
# Launch the terminal
python terminal.py
# or
python superhuman_terminal.py
```

### Features

- **🧠 spaCy-Powered NLP**: Advanced natural language understanding with entity extraction
- **🎯 Precise Intent Recognition**: Maps complex natural language to specific actions
- **🛡️ Privacy-First**: All processing happens locally — no cloud dependencies
- **🔍 Smart Entity Extraction**: Automatically detects files, directories, scopes, and parameters
- **💬 Context-Aware AI Chat**: Provides guidance, best practices, and repository help
- **🚀 Script Execution**: Run Python and shell scripts with natural commands
- **📁 Intelligent File Management**: List, search, preview, and summarize files
- **🔧 Repository Integration**: Seamless access to all repository features and tools

### Example Commands

```
🤖 > help                                    # Show available commands
🤖 > run security scan on Python files       # Execute security analysis  
🤖 > I need to run the security analysis on all my Python files  # Natural request
🤖 > list all Python files                   # List files by type
🤖 > show README.md                          # Display file contents
🤖 > preview the main configuration files    # Quick preview
🤖 > summarize the latest README             # Auto-find and summarize latest docs
🤖 > search for test files                   # Search for files containing text
🤖 > what can you do?                        # Get AI assistance and guidance
🤖 > how do I get started?                   # Onboarding help
🤖 > Can you help me organize my scripts better?  # Get organization advice
🤖 > What are the security features?         # Learn about security capabilities
```

### Advanced Natural Language Support

The terminal uses spaCy to understand complex, conversational queries:

**Intent Recognition:**
- **Commands**: "run", "execute", "list", "show", "search", "summarize", "preview"
- **Conversational**: "I need to...", "Can you help...", "What are...", "How do I..."
- **Context-Aware**: Understands file types, directories, scopes, and modifiers

**Entity Extraction:**
- **File Types**: python, shell, markdown, configuration, etc.
- **Scopes**: all, latest, recent, main, specific directories
- **Directories**: python_scripts, shell_scripts, docs, text_files
- **Action Modifiers**: security, development, testing, organization

**Smart Parameter Detection:**
- Automatically extracts file names, directories, and scope from natural language
- Handles complex queries like "run security scan on all Python files in shell_scripts"
- Provides confidence scoring and clarification when needed

### AI Chat Assistant

The built-in AI chat provides contextual help and guidance:

- **Repository Navigation**: Learn about available scripts and tools
- **Best Practices**: Get advice on script organization and development workflow
- **Security Guidance**: Understand security features and best practices  
- **Development Help**: Learn about the development tools and CI/CD pipeline
- **Onboarding**: Step-by-step guidance for new users

---

## 🔐 Security & Quality

This repository implements enterprise-grade security and quality controls:

- **🔍 Professional CodeQL Analysis**: Multi-language security scanning with advanced configuration

---

## 🧠 Adding New Intents and Entities

The Superhuman Terminal is designed to be easily extensible. Here's how to add new functionality:

### Adding New Intent Types

1. **Define the Intent** in `ai/intent.py`:
```python
class IntentType(Enum):
    NEW_INTENT = "new_intent"
```

2. **Add spaCy Patterns** in `_setup_spacy_patterns()`:
```python
new_intent_patterns = [
    [{"LOWER": {"IN": ["keyword1", "keyword2"]}}, {"IS_ALPHA": True}],
    [{"LOWER": "action"}, {"TEXT": {"REGEX": r".*\\.(py|sh)$"}}],
]
self.matcher.add("NEW_INTENT", new_intent_patterns)
```

3. **Update Pattern Mapping** in `_map_spacy_intent()`:
```python
mapping = {
    # ... existing mappings
    "NEW_INTENT": IntentType.NEW_INTENT,
}
```

4. **Implement Handler** in `superhuman_terminal.py`:
```python
def handle_new_intent(self, intent: Intent):
    """Handle new intent requests."""
    # Implementation here
    pass
```

5. **Register Handler** in `__init__`:
```python
self.action_handlers[IntentType.NEW_INTENT] = self.handle_new_intent
```

### Enhancing Entity Extraction

Add new entity types in `_extract_entities_with_spacy()`:

```python
# Add new file type mappings
file_type_mapping = {
    "new_type": "new_type",
    # ... existing mappings
}

# Add new scope indicators
scope_indicators = {
    "custom_scope": ["custom", "specific", "targeted"],
    # ... existing scopes
}

# Add new action modifiers
action_modifiers = {
    "new_action": ["new", "custom", "specific"],
    # ... existing modifiers
}
```

### Extending AI Chat Responses

Add new response patterns in `handle_ai_chat()`:

```python
elif any(phrase in user_input for phrase in ["new", "topic", "keywords"]):
    print("""
    🔥 **New Feature Information:**
    
    • Description of new capabilities
    • Usage examples and commands
    • Best practices and tips
    """)
```

### Testing Your Extensions

Add tests in `tests/test_superhuman_terminal.py`:

```python
def test_new_intent_recognition(self):
    """Test new intent recognition."""
    intent = self.recognizer.recognize("new command example")
    assert intent.type == IntentType.NEW_INTENT
    assert intent.confidence >= 0.7
```

---

## 🔧 Technical Architecture

**spaCy Integration:**
- English language model (`en_core_web_sm`) for NLP processing
- Pattern matching with `spacy.matcher.Matcher` for intent recognition
- Named Entity Recognition (NER) for parameter extraction
- Dependency parsing for complex query understanding
- Linguistic analysis for confidence scoring

**Intent Recognition Pipeline:**
1. spaCy processes input for linguistic features
2. Pattern matcher identifies potential intents
3. Entity extraction finds parameters and targets
4. Confidence scoring with linguistic enhancement
5. Route to appropriate action handler

**Privacy Protection:**
- All processing happens locally using spaCy
- No cloud APIs or external data transmission
- Complete offline functionality
- User data never leaves the local machine