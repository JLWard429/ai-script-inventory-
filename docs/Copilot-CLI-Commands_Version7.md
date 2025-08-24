# Copilot-CLI: Full Commands & Features Reference

This is your quick reference for using the Copilot-CLI AI assistant in your terminal!

---

## 🚀 General Commands

| Command       | Description                                     |
|---------------|-------------------------------------------------|
| `help`        | Show help, usage tips, and nano shortcuts       |
| `exit`/`quit` | Quit the assistant gracefully                   |

---

## 💬 Chat & Conversation

- Ask any question (general, code, explanations, etc.)
- Multi-turn conversation: references to previous answers are supported
- Persistent chat: All chat is saved in `.ai_assistant_history.json` and reloaded on startup

---

## 🖥️ Shell Command Suggestions

- Ask for shell help, e.g.:
  - `How do I list files in this directory?`
  - `Show me how to create a virtual environment.`
- The assistant will suggest shell commands and **prompt you for confirmation** before running.

---

## ⚙️ Configuration

- **Config file**: `.ai_assistant_cli_config`
  - Example:
    ```
    model=gpt-4
    temperature=0.5
    ```
- **Environment variables**:
  - `export OPENAI_API_KEY="sk-..."`
  - `export OPENAI_MODEL="gpt-4"`
  - `export OPENAI_TEMPERATURE="0.5"`

---

## 🛠️ Special Queries

| What to Type                                    | What It Does                                      |
|-------------------------------------------------|---------------------------------------------------|
| `Which model and temperature are you using right now?` | Shows the current model and temperature (if enabled in script) |
| `model?`                                        | Shows the current model (if enabled)               |
| `temperature?`                                  | Shows the current temperature (if enabled)         |
| `settings?` or `config?`                        | Shows current config (if enabled)                  |

---

## 💡 Nano Shortcuts

| Shortcut   | Action        |
|------------|--------------|
| `Ctrl+K`   | Cut line     |
| `Ctrl+U`   | Paste line   |
| `Ctrl+O`   | Save file    |
| `Ctrl+X`   | Exit nano    |
| `Ctrl+W`   | Search       |
| `Ctrl+_`   | Go to line   |

---

## 🛡️ Error Handling

- All errors are logged in `ai_assistant_cli_errors.log` for troubleshooting.

---

## 📝 Example Usage

```
$ github
🤖 Welcome to Copilot-CLI! Type your question, or 'exit' to quit.
Type 'help' to see tips and commands.
You: help
You: How do I list all Python files?
(Copilot suggests: ls *.py — asks to confirm)
You: model?
(Copilot: I am using model: gpt-4 with temperature: 0.5)
You: exit
```

---

Enjoy your Copilot-CLI!  
For more features or suggestions, just ask the assistant.