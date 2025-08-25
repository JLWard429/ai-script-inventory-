# 🧭 Copilot Coding Agent Instructions for AI Script Inventory

This is an enterprise-grade repository for organizing and managing AI-related scripts with comprehensive automation, security analysis, and quality controls. The repository features a **Superhuman AI Terminal** that provides a privacy-friendly, local-only AI interface for script management.

## 🥅 End Goal

Build and maintain an advanced, privacy-respecting, local AI-powered script management terminal. This system must:
- Allow users to control, organize, and run scripts and automation tasks using natural language
- Use spaCy for advanced intent and entity recognition, making the system accessible with simple general statements
- Integrate smoothly with all repository resources (scripts, file management, summarization, etc.)
- Provide an AI chat experience that guides users, assists discovery, and minimizes the need to remember command syntax

## 🛠️ Core Development Focus

When working on this repository, prioritize these key areas:

### spaCy-Powered Intent Recognition
- **Primary System**: `ai/intent.py` uses spaCy for advanced natural language processing
- **Refactor and extend** the intent recognition to make spaCy the leader for understanding user requests
- **Route intents and entities** to the correct script or function in the codebase
- **Support new commands, actions, and conversational flows** as the repository grows

### Superhuman Terminal Enhancement
- **Main Interface**: `superhuman_terminal.py` provides the user interaction layer
- **AI Chat Handler**: Extend `handle_ai_chat()` for conversational assistance
- **Action Handlers**: Add new intent handlers following the existing pattern
- **Natural Language Processing**: Leverage spaCy for entity extraction and parameter parsing

## ✅ Best Practices for AI Terminal Development

### Code Quality & Architecture
- **Prefer Python 3.9+ syntax** and typing where possible
- **Ensure all changes are modular, testable, and well-documented**
- **Write code that is easy to reason about and extend** — avoid hard-coded paths or one-off hacks
- **Use descriptive commit messages** and pull request titles focused on terminal functionality
- **Write and update tests** for new or changed terminal functionality

### spaCy Integration Guidelines  
- **Always double-check** that spaCy entity extraction robustly handles script names, file names, directories, and user intent
- **Leverage spaCy's linguistic features**: named entity recognition, dependency parsing, part-of-speech tagging
- **Implement fallback mechanisms** for when spaCy is not available or fails
- **Test with complex, natural language queries** to ensure robust understanding

### Privacy-First Development
- **Maintain local-only processing** — no cloud dependencies or external API calls
- **Respect user privacy** in all data handling and processing
- **Document privacy protections** clearly for users
- **Test offline functionality** to ensure complete local operation

## 💬 AI Chat and Conversational Guidance

### Intent Handling Strategy
- **When user intent is ambiguous**, prompt for clarification rather than failing
- **When user asks general questions** (not matching a concrete command), provide helpful, context-aware advice or examples
- **Reference the README and terminal help docs** to suggest available features and commands
- **Provide discovery assistance** to help users understand repository capabilities

### Conversational Flow Design
- **Build context-aware responses** that consider the user's current workflow
- **Offer proactive suggestions** for next steps or related actions
- **Handle edge cases gracefully** with helpful error messages
- **Maintain conversational memory** within a session when appropriate

## 📂 Repository Integration Best Practices

### Existing Function Reuse
- **Always use existing script runners**, file search, summarization, and management functions
- **Do not duplicate logic** — extend existing functionality instead
- **Make sure new features and handlers are discoverable** via the terminal's help output
- **Follow the established patterns** in action handlers and intent routing

### File Organization Awareness
- **Respect the auto-organization system** (`organize_ai_scripts.py`)
- **Understand the directory structure**: 
  - `python_scripts/` → Python scripts and AI tools
  - `shell_scripts/` → Shell scripts and CLI utilities  
  - `docs/` → Documentation and guides
  - `text_files/` → Configuration files, logs, and data
  - `ai/` → Intent recognition and AI modules

## 🚦 Example Prompts & Expected Terminal Behavior

Understanding these examples will help you develop features that meet user expectations:

### Natural Language Script Execution
```
User: "Run the security scan on all Python files in shell_scripts"
Expected Action: 
- Intent: run_script
- Target: security scan script  
- Parameters: {scope: all, file_type: python, directory: shell_scripts}
- Execution: Run security analysis with specified parameters
```

### Intelligent File Operations
```
User: "Summarize the latest README" 
Expected Action:
- Intent: summarize
- Target: README file (auto-detect most recent)
- Parameters: {scope: latest}
- Execution: Find most recent README and provide content summary
```

### Conversational Assistance
```
User: "How do I use this system?"
Expected Action:
- Intent: ai_chat
- Response: Helpful AI chat answer referencing main features and onboarding steps
- Include: Available commands, best practices, getting started guidance
```

### Advanced Natural Language Queries
```
User: "Show me the contents of my AI scripts"
Expected Action:
- Intent: show/list (context-dependent)
- Target: AI-related scripts
- Parameters: {file_type: ai, scope: contents}
- Execution: Display or list AI script contents
```

## 🔧 Extending the Terminal System

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
    [{"LOWER": "action"}, {"TEXT": {"REGEX": r".*\\.(py|sh)$"}}]
]
self.matcher.add("NEW_INTENT", new_intent_patterns)
```

3. **Implement Handler** in `superhuman_terminal.py`:
```python
def handle_new_intent(self, intent: Intent):
    \"\"\"Handle new intent requests.\"\"\"
    # Implementation here
    pass
```

4. **Register Handler** in `__init__`:
```python
self.action_handlers[IntentType.NEW_INTENT] = self.handle_new_intent
```

### Enhancing AI Chat Capabilities

- **Add contextual response patterns** in `handle_ai_chat()`
- **Leverage user input analysis** to provide relevant suggestions
- **Reference repository documentation** and capabilities dynamically
- **Maintain conversation flow** with appropriate follow-up questions

## 🧪 Testing AI Terminal Features

### Intent Recognition Testing
```python
# Test new intent patterns
def test_new_intent_recognition():
    recognizer = create_intent_recognizer()
    intent = recognizer.recognize("your test input")
    assert intent.type == IntentType.EXPECTED_INTENT
    assert intent.confidence > 0.5
```

### Terminal Integration Testing  
```python
# Test terminal handlers
def test_terminal_handler():
    terminal = SuperhumanTerminal()
    intent = Intent(type=IntentType.TEST, confidence=0.8)
    # Test handler execution
    terminal.handle_intent(intent)
```

### spaCy Feature Testing
- **Test entity extraction** with various input formats
- **Validate parameter parsing** across different phrasings  
- **Ensure fallback mechanisms** work when spaCy fails
- **Test with edge cases** and ambiguous inputs

## 📚 Key Resources & Documentation

### Terminal Documentation
- **[TERMINAL_GUIDE.md](TERMINAL_GUIDE.md)**: Comprehensive developer guide for the AI terminal
- **[README.md](README.md)**: User-facing documentation and quick start guide
- **[ai/intent.py](ai/intent.py)**: Core intent recognition implementation
- **[superhuman_terminal.py](superhuman_terminal.py)**: Main terminal interface

### External Resources
- **[spaCy Documentation](https://spacy.io/usage)**: NLP library documentation
- **[GitHub Copilot Coding Agent Tips](https://gh.io/copilot-coding-agent-tips)**: General development guidance

### Repository-Specific Instructions
- **[.github/instructions/](../instructions/)**: Detailed instructions for different file types
- **[python-scripts.instructions.md](../instructions/python-scripts.instructions.md)**: Python development guidelines
- **[tests.instructions.md](../instructions/tests.instructions.md)**: Testing requirements and patterns

## 🔄 Development Workflow for Terminal Features

### Pre-Development Setup
```bash
# Install dependencies including spaCy
pip install -r requirements-dev.txt

# Download spaCy model (required for intent recognition)
python -m spacy download en_core_web_sm

# Install pre-commit hooks
pre-commit install
```

### Testing & Validation
```bash
# Run all tests including terminal tests
pytest tests/ -v

# Test terminal functionality directly
python terminal.py

# Run specific terminal tests
pytest tests/test_terminal.py -v

# Test intent recognition
python ai/intent.py
```

### Code Quality for Terminal Code
```bash
# Format code (especially important for terminal modules)
black ai/ superhuman_terminal.py terminal.py

# Sort imports
isort ai/ superhuman_terminal.py terminal.py

# Type checking for terminal modules
mypy ai/ superhuman_terminal.py

# Security scanning
bandit -r ai/ superhuman_terminal.py
```

## 📝 How to Update Terminal Documentation

### Synchronize Documentation
- **When new terminal features are added**, update `TERMINAL_GUIDE.md` with technical details
- **Update these Copilot instructions** to reflect new capabilities and patterns
- **Keep the terminal's help output** in sync with actual functionality
- **Update README.md examples** to showcase new natural language capabilities

### Documentation Consistency
- **Maintain alignment** between user docs, developer docs, and code comments
- **Update AI chat responses** to reference current system capabilities
- **Keep example prompts current** with the latest intent recognition features
- **Document privacy protections** whenever touching data handling code

## Repository Structure (Terminal-Focused View)

```
ai-script-inventory/
├── ai/                          # 🧠 Core AI and NLP modules
│   ├── intent.py               # Main intent recognition with spaCy
│   └── __init__.py             # AI module initialization
├── superhuman_terminal.py      # 🚀 Main terminal interface & handlers
├── terminal.py                 # 🎯 Simple terminal launcher
├── TERMINAL_GUIDE.md           # 📖 Developer guide for terminal
├── tests/                      # 🧪 Test suite (focus on terminal tests)
│   ├── test_terminal.py        # Terminal functionality tests
│   └── test_basic.py           # Basic validation including terminal
├── python_scripts/             # 🐍 Python scripts managed by terminal
├── shell_scripts/              # 🐚 Shell scripts managed by terminal  
├── docs/                       # 📚 Documentation managed by terminal
├── text_files/                 # 📄 Configuration/data managed by terminal
├── .github/                    # ⚙️ Automation and instructions
│   ├── copilot-instructions.md # This file - terminal development guide
│   └── instructions/           # Detailed file-type specific instructions
├── requirements-dev.txt        # 📦 Includes spaCy and terminal dependencies
└── pyproject.toml             # ⚙️ Project configuration
```

## Common Terminal Development Tasks

### Adding Natural Language Command Support
1. **Identify the user intent pattern** from real usage examples  
2. **Add spaCy patterns** in `_setup_spacy_patterns()` to recognize the intent
3. **Create or extend the intent handler** in `SuperhumanTerminal`
4. **Test with various phrasings** to ensure robust recognition
5. **Update documentation** and help text

### Enhancing AI Chat Responses
1. **Analyze user question patterns** in `handle_ai_chat()`
2. **Add contextual response logic** for new question types
3. **Reference current repository capabilities** dynamically  
4. **Test conversational flow** for natural interaction
5. **Update AI chat examples** in documentation

### Improving Intent Recognition Accuracy
1. **Analyze missed or misclassified intents** in testing
2. **Enhance spaCy patterns** or add new pattern types
3. **Improve entity extraction** for parameters and targets
4. **Add confidence scoring refinements** 
5. **Test across different input styles** and edge cases

## Troubleshooting Terminal Development

### Common Intent Recognition Issues
- **spaCy model not found**: Run `python -m spacy download en_core_web_sm`
- **Low confidence scores**: Check pattern matching and entity extraction logic
- **Parameter extraction failures**: Validate regex patterns and spaCy entity recognition
- **Fallback activation**: Ensure spaCy is properly initialized and available

### Terminal Integration Problems  
- **Handler not found**: Verify intent type is registered in `action_handlers`
- **Import errors**: Check that all terminal dependencies are installed
- **Context issues**: Ensure working directory and path resolution work correctly

This repository exemplifies a "superhuman AI workflow system" where natural language understanding, privacy protection, and intelligent automation converge. All contributions should enhance the AI terminal experience while maintaining these principles.