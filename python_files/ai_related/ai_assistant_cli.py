"""
Copilot-CLI: Terminal AI Assistant

Quick Commands:
  exit              Quit the assistant
  help              Show this quick help

Nano Shortcuts:
  Ctrl+K            Cut line
  Ctrl+U            Paste line
  Ctrl+O            Save file
  Ctrl+X            Exit nano

Features:
  - Persistent chat history in .ai_assistant_history.json
  - Command suggestions with confirmation and safe execution
  - Configurable model/temperature via env or .ai_assistant_cli_config
  - Colorful CLI output for clarity
  - Error logging to ai_assistant_cli_errors.log

Set your OpenAI API key before running:
  export OPENAI_API_KEY="sk-..."

Enjoy your Copilot-CLI!
"""

import os
import sys
import json
import openai
import traceback
from datetime import datetime

# --- CONFIGURABLES ---
HISTORY_FILE = ".ai_assistant_history.json"
ERROR_LOG = "ai_assistant_cli_errors.log"
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.2
CONFIG_FILE = ".ai_assistant_cli_config"

# --- COLOR FUNCTIONS ---
def color(text, code): return f"\033[{code}m{text}\033[0m"
def cyan(text): return color(text, "36")
def green(text): return color(text, "32")
def yellow(text): return color(text, "33")
def red(text): return color(text, "31")
def bold(text): return color(text, "1")
def magenta(text): return color(text, "35")

# --- ERROR LOGGING ---
def log_error(msg):
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

# --- CONFIG LOADING ---
def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        config[k.strip()] = v.strip()
        except Exception as e:
            log_error(f"Failed to load config: {e}")
    return config

# --- HISTORY HANDLING ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            log_error(f"Failed to load history: {e}")
    # Start new history
    return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        log_error(f"Failed to save history: {e}")

# --- API KEY, MODEL, TEMP ---
def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(red("❗ ERROR: OPENAI_API_KEY environment variable not set."))
        print("   Please set it with:")
        print(yellow("   export OPENAI_API_KEY='sk-...your-key...'"))
        sys.exit(1)
    return api_key

def get_model_and_temp():
    config = load_config()
    model = os.getenv("OPENAI_MODEL", config.get("model", DEFAULT_MODEL))
    try:
        temp = float(os.getenv("OPENAI_TEMPERATURE", config.get("temperature", DEFAULT_TEMPERATURE)))
    except Exception:
        temp = DEFAULT_TEMPERATURE
    return model, temp

def print_welcome():
    print(cyan("🤖 Welcome to Copilot-CLI! Type your question, or 'exit' to quit.\n"))
    print(magenta("Type 'help' to see tips and commands."))

def print_goodbye():
    print(green("\n👋 Goodbye! Have a great day."))

def print_help():
    print(bold("\nCopilot-CLI Quick Help"))
    print(f"{yellow('exit')}: Quit the assistant")
    print(f"{yellow('help')}: Show this help")
    print("Nano shortcuts: Ctrl+K (cut), Ctrl+U (paste), Ctrl+O (save), Ctrl+X (exit)\n")
    print("Configurable via .ai_assistant_cli_config (model=..., temperature=...)\n")
    print("Persistent chat history in .ai_assistant_history.json")
    print("Command suggestions will prompt for confirmation before running.\n")

# --- OPENAI CALL ---
def ask_openai(client, messages, model, temperature):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        err_msg = f"OpenAI API error: {e}\n{traceback.format_exc()}"
        print(red("❗ OpenAI API error. See log for details."))
        log_error(err_msg)
        return None

# --- COMMAND SUGGESTION LOGIC ---
def extract_command(text):
    # Very simple heuristic: look for lines like $ ... or code blocks with shell commands
    lines = text.splitlines()
    for line in lines:
        if line.strip().startswith("$ "):
            return line.strip()[2:]
        if line.strip().startswith("```sh") or line.strip().startswith("```bash"):
            # look for next non-empty, non-``` line
            for l in lines[lines.index(line)+1:]:
                l = l.strip()
                if l and not l.startswith("```"):
                    return l
    # fallback: look for common shell command patterns
    for line in lines:
        if any(line.strip().startswith(cmd) for cmd in ["ls", "cd", "cat", "pip", "python", "git", "rm", "cp", "mv", "./"]):
            return line.strip()
    return None

def prompt_and_run_command(cmd):
    print(yellow(f"\nCopilot suggests you run: {cmd}"))
    confirm = input(yellow("Run this command? (y/n): ")).strip().lower()
    if confirm == "y":
        print(green(f"Running: {cmd}\n"))
        os.system(cmd)
    else:
        print(cyan("Command not run."))

def main():
    api_key = get_api_key()
    model, temperature = get_model_and_temp()
    client = openai.OpenAI(api_key=api_key)

    system_prompt = (
        "You are a helpful AI assistant in the terminal. "
        "Answer clearly, be friendly, and keep explanations simple. "
        "If the user asks to run a command, always ask for confirmation first. "
        "If you don’t know something, say so. "
        "If the user refers to something from earlier, try your best to understand the context. "
        "Hold a casual conversation and help with code, commands, or questions."
    )

    history = load_history()
    if not history or (history and history[0].get("role") != "system"):
        # Start new history with system prompt
        history = [{"role": "system", "content": system_prompt}]
        save_history(history)

    print_welcome()

    while True:
        try:
            user_input = input(bold("You: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print_goodbye()
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print_goodbye()
            break
        if user_input.lower() == "help":
            print_help()
            continue

        history.append({"role": "user", "content": user_input})
        save_history(history)

        print(cyan("Copilot: Thinking..."))
        response = ask_openai(client, history, model, temperature)
        if response:
            print(green(f"Copilot: {response}"))
            history.append({"role": "assistant", "content": response})
            save_history(history)
            # Check for command suggestions
            cmd = extract_command(response)
            if cmd:
                prompt_and_run_command(cmd)
        else:
            print(red("Copilot: Sorry, there was an error. Try again or check your API key/internet connection."))

if __name__ == "__main__":
    main()
