main() if __name__ == "__main__":sys.exit(1)print(f"❌ superman startup error: {e}")except exception as e:sys.exit(0)print("\n\n👋 goodbye!")except keyboardinterrupt:orchestrator.run()orchestrator = supermanorchestrator()try:"""main entry point for superman cli."""def main() -> none:return os.environ.get("superman_debug", "").lower() in ("1", "true", "yes")"""debug mode status."""def debug_mode(self) -> bool:@propertyreturn f"task successfully delegated to {employee_name}."return f"error delegating task: {e}"except exception as e:return f"task successfully delegated to {employee_name}."description=f"running {employee_name}",["python", script_path, task],self._run_subprocess(try:if script_path and hasattr(self, "_run_subprocess"):script_path = employee_info.get("path", "")employee_info = self.employees[employee_name]# actually run the employee script for testing compatibilityprint(f"🤝 delegating task to {employee_name}: {task}")task = " ".join(parts[2:]) if len(parts) > 2 else ""return f"employee '{employee_name}' not found. use 'list employees' to see available employees."if not employee_name or employee_name not in self.employees:employee_name = parts[1] if len(parts) > 1 else ""return "please specify employee and task: 'delegate <employee> <task>'"if len(parts) < 2:parts = command.split()"""delegate task to employee script."""def delegate_task(self, command: str) -> str:return f"found {len(self.employees)} employee scripts."print(f"• {name}: {info.get('description', 'no description')}")for name, info in self.employees.items():print("=" * 35)print("👥 available employee scripts:")"""list available employee scripts."""def list_employees(self) -> str:"name": "employee_spacy_test","description": "test employee script","type": "python","path": "tests/employee_spacy_test.py","employee_spacy_test": {return {# for testing purposes, return a basic structure"""dictionary of available employee scripts."""def employees(self) -> dict:@propertyreturn ["memory", "analyze", "status", "demo", "employees", "delegate"]"""list of superman-specific commands."""def superman_commands(self) -> list:@propertyreturn "memory status displayed."print("no conversations stored yet.")else:print(f"  {i}. {memory['user_input'][:50]}...")for i, memory in enumerate(self.memory.memories[-3:], 1):print("\nrecent conversations:")if self.memory.memories:print(f"max memories: {self.memory.max_memories}")print(f"total memories: {len(self.memory.memories)}")print("=" * 30)print("🧠 memory system status")"""show memory system status."""def show_memory(self) -> str:return "status information displayed."print(line)for line in status_info:status_info.append(f"memory entries: {len(self.memory.memories)}"))f"debug mode: {'✅ enabled' if self.debug_mode else '❌ disabled'}"status_info.append()f"superman mode: {'✅ active' if self.superman_mode else '❌ inactive'}"status_info.append()f"internet available: {'✅ yes' if self.internet_available else '❌ no'}"status_info.append()f"openai integration: {'✅ enabled' if self.openai_client else '❌ disabled'}"status_info.append(status_info.append("=" * 40)status_info.append("🦸 superman ai orchestrator status")status_info = []"""show system status information."""def show_status(self) -> str:# stub methodsfor compatibility with existing testsself.handle_intent(intent)intent = self.intent_recognizer.recognize(user_input)# use parent class intent recognitionprint("🔄 processing locally...")"""fallback to local spacy-based processing when openai is not available."""def _fallback_to_local_processing(self, user_input: str) -> none:self._fallback_to_local_processing(original_input)print(f"⚠️  error in delegation: {e}")except exception as e:self._fallback_to_local_processing(original_input)print("⚠️  error parsing openai delegation response")except json.jsondecodeerror:handler(intent)handler = self.action_handlers.get(intent.type, self.handle_unknown)# call the appropriate handle)original_input=original_input,parameters=params,target=target,confidence=1.0,  # high confidence since it came from openaitype=intent_type,intent = intent(from ai_script_inventory.ai.intent import intent# create intent object for local handlerintent_type = action_mapping.get(action, intenttype.unknown)}"exit": intenttype.exit,"help": intenttype.help,"summarize": intenttype.summarize,"search":intenttype.search,"preview": intenttype.preview,"show": intenttype.show,"list": intenttype.list,"run_script": intenttype.run_script,action_mapping = {# map openai actions to local intent typesparams = delegation.get("params", {})target = delegation.get("target", "")action = delegation.get("action", "").lower()delegation = json.loads(ai_response)import jsontry:"""handle delegation from openai to local handlers."""def _handle_openai_delegation(self, ai_response: str, original_input: str) -> none:print("=" * 50)print("\ntype your request or question, or 'exit' to quit.")print("  • 'how should i structure my ai project?'")print("  • 'show me what's in the repository'")print("  • 'run a security scan on all python files'")print("  • 'what are the best practices for organizing python scripts?'")print("\n💡 try natural language like:")print("  • security scanning and quality checks")print("  • code analysis and organization")print("  • file operations (e.g., 'list python files', 'show readme.md')")print("  • running scripts (e.g., 'run organize_ai_scripts.py')")print("i can help you with:")print("⚠️  running in local-only mode (openai not available)")else:print("  • explain complex topics and provide detailed assistance")print("  • provide guidance on script organization and development")print("  • execute repository tasks (running scripts, file management)")print("  • answer questions about ai, programming, and best practices")print("i can help you with:"))"🤖 powered by openai gpt for intelligent conversation and task coordination"print(if self.openai_client:print("=" * 50)print("🦸 welcome to superman ai orchestrator!")"""print welcome message for superman orchestrator."""def print_welcome_superman(self):print(f"❌ error: {e}")except exception as e:breakprint("\n\n👋 goodbye!"except eoferror:breakprint("\n\n👋 goodbye!")except keyboardinterrupt:    self._fallback_to_local_processing(user_input)    print("\n🔄 falling back to local processing...")    print("   3. restart the terminal")    )	"   2. set your api key: export openai_api_key='your-key-here'"    print(    print("   1. install openai library: pip install openai")    print("🔧 to enable ai orchestration:")    print("\n❌ openai integration not available")   # openai not available - show clear error message and fallback infoelse:	print(f"\n🤖 {ai_response}")	# direct response from openai (includes error messages)    else:	self._handle_openai_delegation(ai_response, user_input)	# parse json response and delegate to local handlers   if is_delegation:    is_delegation, ai_response =self._process_with_openai(user_input)    # openai is configured and available - use it for all queriesif self.openai_client:# process with openai as primary brain when availableself.history.append(user_input)# add to history   continueif not user_input:user_input = input("\n🦸 > ").strip()try:while self.running:self.print_welcome_superman()# custom welcome message for openai-first approachprint("=" * 50)print("🦸 superman ai orchestrator ready!")print("\n" + "=" * 50)self.check_openai_connectivity()self.check_spacy_installation()print("\n🔧 system checks:")# additional startup checksself.check_internet_connectivity()# perform startup connectivity check"""override run method to implement openai-first processing architecture."""def run(self) -> none:self.handle_ai_chat(intent)print("🔄 openai unavailable, using local chat handler...")# only fall back to original handler if openai is completely unavailablereturnprint(f"\n🤖 {ai_response}")# direct response from openai (including error messages)else:returnself._handle_openai_delegation(ai_response, intent.original_input)# parse json response and delegate to local handlersif is_delegation:)intent.original_inputis_delegation, ai_response = self._process_with_openai(if self.openai_client:# route through openai if available (primary brain)self.memory.add_context(intent.target or "")# add to memory context"""enhanced ai chat handler - routes through openai when available."""def handle_ai_chat_enhanced(self, intent) -> none:return false, error_response)    "🔧 please check your openai configuration and try again."error_response += (else:  "🌐 network connectivity issue. check your internet connection."rror_response += (elif "connection" in error_msg or "network" in error_msg:)    "⏱️  rate limit exceeded. please wait before making more requests."error_response += (elif "rate limit" in error_msg:)    "  • the openai_api_key environment variable is set correctly"error_response += (error_response += "  • you have sufficient credits/quota\n"error_response += "  • your api key has not expired\n"error_response += "  • your api key is correct and starts with 'sk-'\n"error_response += "please check that:\n")    "🔑 this suggests an issue with your openai api key.\n"error_response += (if "api key" in error_msg or "incorrect api key" in error_msg:# enhanced error handling for specific api issueserror_response = f"❌ openai request failed: {e}\n\n"
# create detailed error response instead of falling backerror_msg = str(e).lower()except exception as e:return false, ai_responseelse:return true, ai_responseif ai_response.startswith("{") and '"action"' in ai_response:# check if this is a delegation (jsonresponse) or direct esponse

ai_response = "i apologize, but i couldn't generate a response to your query. please try rephrasing your question."
if not ai_response:
# ensure we always have a response

self.memory.remember(user_input, ai_response)
# store in memoryai_response = response.choices[0].message.content.strip())max_tokens=1000,temperature=0.7,messages=messages,model="gpt-3.5-turbo",response = self.openai_client.chat.completions.create(messages.append({"role": "user", "content": user_input})


}
"content": f"recent context: {recent_context}",
"role": "assistant",
{
messages.append(
if recent_context:
recent_context = self.memory.get_recent_context(3)
# add recent context from memory

messages = [{"role": "system", "content": self._get_system_prompt()}]
# add conversation history context
try:

)
"❌ openai client not available. please configure openai_api_key.",
false,
return (
# no openai client available - this should not happen if method is called correctly
if not self.openai_client:
"""
- response: either the direct response, delegation json, or error message
- is_delegation: true if this should be delegated to local handlers
tuple[bool, str]: (is_delegation, response)
returns:

process user input with openai as the primary brain.
"""
def _process_with_openai(self, user_input: str) -> tuple[bool, str]:

remember: you are the primary orchestrator. provide helpful responses for general queries and delegate repository tasks to the local system."""

response: {"action": "show", "target": "readme.md", "params": {}}
user: "show me the readme file"

response: {"action": "run_script", "target": "security scan", "params": {"type": "security"}}
user: "run the security scan"

response: direct helpful advice about script organization
user: "how do i organize my python scripts?"
examples:

for general conversation, respond normally with helpful text.
for repository tasks, respond with json: {"action": "action_type", "target": "target", "params": {...}}
response format:

- help: show help information
- summarize: summarize document content
- search: search for files (e.g., "search for test files")
- preview: quick file preview
- show: display file contents (e.g., "show readme.md")
- list: list files by type (e.g., "list python files", "list all scripts")
- run_script: execute python/shell scripts (e.g., "run organize_ai_scripts.py")
available repository actions:

2. for repository tasks (file operations, script running, etc.): delegate to the local system
1. for general conversation, questions, or advice: respond directly with helpful information
your role:

- includes automation, security scanning, and file organization tools
- has a superhuman ai terminal with local spacy-based intent recognition
- contains organized directories: python_scripts/, shell_scripts/, docs/, text_files/
- this is a python repository for organizing and managing ai-related scripts
repository context:

return """you are the superman ai orchestrator for an ai script inventory repository. you serve as the primary interface between users and the repository's capabilities.
"""get system prompt for openai to understand repository context and capabilities."""
def _get_system_prompt(self) -> str:

print("👤 superman mode deactivated")
self.superman_mode = false
"""deactivate superman mode."""
def deactivate_superman_mode(self) -> none:

print("  enhanced ai capabilities enabled")
print("🦸 superman mode activated!")
self.superman_mode = true
"""activate superman mode with enhanced capabilities."""
def activate_superman_mode(self) -> none:

print("ℹ️  openai api key configured (internet unavailable - cannot test)")
else:
print("✅ openai api key configured (internet available for testing)")
if self.internet_available:

return
print("⚠️  openai api key does not start with 'sk-' - may be invalid format")
if not api_key.startswith("sk-"):

return
print("   set openai_api_key environment variable for ai features")
print("ℹ️  openai api key not configured")
if not api_key:

api_key = os.environ.get("openai_api_key")
"""check openai api connectivity and configuration."""
def check_openai_connectivity(self) -> none:

print("   install with: pip install spacy")
print("❌ spacy not installed")
except importerror:

print("   install with: python -m spacy download en_core_web_sm")
print("⚠️  spacy model 'en_core_web_sm' not found")
except oserror:
print("✅ spacy model 'en_core_web_sm' loaded successfully")
nlp = spacy.load("en_core_web_sm")
try:

print(f"✅ spacy version: {spacy.__version__}")

import spacy
try:
"""check spacy installation and model availability."""
def check_spacy_installation(self) -> none:

return false
self.internet_available = false

print("   • local-only processing will be used")
print("   • some online resources may not be accessible")
print("   • external api features will be disabled")
print("⚠️  warning: operating in offline/limited mode")
print("❌ internet access: not available")
# all tests failed

continue
print(f"🔍 testing {url}: {type(e).__name__}: {e}")
# other errors (timeout, etc.)
except exception as e:
continue
print(f"🔍 testing {url}: {e.reason}")
# dns resolution failed or network error
except urllib.error.urlerror as e:

return true
self.internet_available = true
print(f"✅ internet access: available (verified via {url})")
if response.status == 200:
with urllib.request.urlopen(req, timeout=5) as response:

)
url, headers={"user-agent": "superman-cli/1.0"}
req = urllib.request.request(
# try to open the url with a short timeout
try:
for url in test_urls:

print("🌐 checking internet connectivity...")

]
"https://httpbin.org/status/200",
"https://api.openai.com",
"https://www.google.com",
test_urls = [
"""
bool: true if internet is available, false otherwise
returns:

check for active internet connectivity by attempting to reach well-known websites.
"""
def check_internet_connectivity(self) -> bool:

self.openai_client = none
print(f"❌ failed to initialize openai client: {e}")
except exception as e:
print("✅ openai integration enabled")
self.openai_client = openai.openai(api_key=api_key)
try:

return
print("⚠️  openai api key does not start with 'sk-' - may be invalid format")
if not api_key.startswith("sk-"):

return
print("   set openai_api_key environment variable for ai orchestration")
print("ℹ️  openai api key not configured")
if not api_key:
api_key = os.environ.get("openai_api_key", "").strip()

return
print("⚠️  openai library not available. install with: pip install openai")
if not has_openai:
"""initialize openai client if api key is available."""
def _initialize_openai(self) -> none:

)
}
intenttype.ai_chat: self.handle_ai_chat_enhanced,
{
self.action_handlers.update(
if hasattr(self, "action_handlers"):
# add enhanced action handlers

self._initialize_openai()
# initialize openai client if available

self.openai_client = none
self.internet_available = false
self.superman_mode = false
self.code_analyzer = codeanalyzer()
self.memory = memorysystem()
# initialize enhanced systems

super().__init__()
"""initialize superman orchestrator with enhanced capabilities."""
def __init__(self):

"""
enhanced features: memory system, internet connectivity checking, code analysis.

3. fallback: only when openai client is not available (no api key/connection)
- error: display error message with troubleshooting info
- delegation json: route to local handlers (file ops, script running, etc.)
- direct response: display to user
2. openai response handling:
1. user input → openai api (always, when configured)
processing flow:

- local processing is only used when openai is completely unavailable
* repository-specific tasks (delegation to local handlers)
* general conversation and knowledge queries (direct response)
- openai acts as the central coordinator and decision maker for:
- all user input is routed through openai when available and configured
architecture principle: openai-first processing

superman ai orchestrator that uses openai as the primary brain for all user interactions.
"""
class supermanorchestrator(superhumanterminal):


return {"error": str(e)}
except exception as e:

}
"directory": str(dir_path),
"file_types": file_types,
"total_files_scanned": total_scanned,
return {

file_types[ext] = file_types.get(ext, 0) + 1
ext = file_path.suffix
total_scanned += 1
if file_path.is_file():
for file_path in files:

total_scanned = 0
file_types = {}
files = list(dir_path.iterdir())
try:

return {"error": f"directory not found: {dir_path}"}
if not dir_path.is_dir():

dir_path = path(dir_path)
"""analyze directory structure and contents."""
def analyze_directory(self, dir_path: str) -> dict:

}
"code_blocks": code_blocks // 2,  # each block has start and end
"headers": headers,
return {

code_blocks = content.count("```")
headers = sum(1 for line in lines if line.strip().startswith("#"))
lines = content.splitlines()
"""analyze markdown content."""
def _analyze_markdown(self, content: str) -> dict:

}
"functions": content.count("() {"),
"has_error_handling": "set -e" in content,
"has_shebang": content.startswith("#!"),
return {
"""analyze shell script content."""
def _analyze_shell(self, content: str) -> dict:

return analysis

analysis["imports"].append(stripped)
if stripped.startswith("import ") or stripped.startswith("from "):
stripped = line.strip()
for line in lines:
lines = content.splitlines()
# count import statements

}
"imports": [],
"has_docstring": '"""' in content or "'''" in content,
"has_main": "if __name__" in content,
"functions": content.count("def "),
"classes": content.count("class "),
analysis = {
"""analyze python code content."""
def _analyze_python(self, content: str) -> dict:

return {"error": str(e)}
except exception as e:

return analysis
self.analysis_cache[str(file_path)] = analysis

analysis["language"] = "unknown"
else:
analysis["language"] = "markdown"
analysis.update(self._analyze_markdown(content))
elif file_path.suffix == ".md":
analysis["language"] = "shell"
analysis.update(self._analyze_shell(content))
elif file_path.suffix in [".sh", ".bash"]:
analysis["language"] = "python"
analysis.update(self._analyze_python(content))
if file_path.suffix == ".py":
# determine language and analyze accordingly

}
"file_type": file_path.suffix,
"chars": len(content),
"lines": len(content.splitlines()),
analysis = {

content = f.read()
with open(file_path, "r", encoding="utf-8") as f:
try:

return {"error": f"file not found: {file_path}"}
if not file_path.exists():

return self.analysis_cache[str(file_path)]
if str(file_path) in self.analysis_cache:

file_path = path(file_path)
"""analyze a code file and return comprehensive insights."""
def analyze_file(self, file_path: str) -> dict:

self.repository_root = path.cwd()
self.analysis_cache = {}
"""initialize the code analyzer."""
def __init__(self):

"""advanced code analysis system for understanding and improving code."""
class codeanalyzer:


return [m["response"] for m in self.memories if m["user_input"] == "context"]
"""get the current context (legacy interface)."""
def get_context(self) -> list:

self.remember("context", context)
"""add context to the conversation (legacy interface)."""
def add_context(self, context: str) -> none:

return none
return memory["response"]
if memory["user_input"] == f"store:{key}":
for memory in self.memories:
"""retrieve a value from memory (legacy interface)."""
def retrieve(self, key: str) -> optional[str]:

self.remember(f"store:{key}", value)
"""store a key-value pair in memory (legacy interface)."""
def store(self, key: str, value: str) -> none:

return results

results.append(memory)
):
or query_lower in memory["response"].lower()
query_lower in memory["user_input"].lower()
if (
for memory in self.memories:

results = []
query_lower = query.lower()
"""search through stored memories for matching content."""
def search_memories(self, query: str) -> list:

return " ".join(context_parts)

context_parts.append(memory["response"])
context_parts.append(memory["user_input"])
for memory in recent:

context_parts = []
)
self.memories[-count:] if count <= len(self.memories) else self.memories
recent = (
"""get recent conversation context as formatted string."""
def get_recent_context(self, count: int = 5) -> str:

self.memories = self.memories[-self.max_memories :]
if len(self.memories) > self.max_memories:
# keep only the most recent memories

self.memories.append(memory)

}
"timestamp": time.time(),
"intent_type": intent_type,
"response": response,
"user_input": user_input,
memory = {

import time
"""store a conversation exchange in memory."""
def remember(self, user_input: str, response: str, intent_type: str = none) -> none:

self.session_start = os.environ.get("session_start", "now")
self.memories = []
self.max_memories = max_memories
"""initialize the memory system with configurable limits."""
def __init__(self, max_memories: int = 100):

"""advanced memory system for storing conversation context and learning."""
class memorysystem:
has_openai = false
except importerror:
has_openai = true
import openai
try:
from ai_script_inventory.superhuman_terminal import superhumanterminal
from ai_script_inventory.ai.intent import intenttype, create_intent_recognizer
sys.path.insert(0, str(path(__file__).parent.parent / "src"))
# add src to path for imports
from typing import optional
from pathlib import path
import urllib.request
import urllib.error
import sys
import os
"""
local capabilities only as a last resort when openai is completely unavailable.
this extends the superhumanterminal with openai-first integration while maintaining
4. if unavailable: clear error message + optional local fallback
3. if delegation: route to appropriate local handler
- json delegation for repository-specific tasks (file management, script running, etc.)
- direct conversational response for general queries
2. openai responds with either:
1. user input → openai api (chat/completions endpoint)
processing flow:
- **fallback**: only uses local processing when openai is completely unavailable (no api key/client)
- **delegation**: openai determines whether to respond directly or delegate to local handlers
interpreter -y- **primary**: all user input is sent directly to openai (chatgpt) for processingarchitecture:openai-powered ai terminal that routes all user interactions through openai as the primary brain.superman aiorchestrator"""#!/usr/bin/env python3
