import os
import sys
import subprocess

TOOLBOX_KEYWORDS = ["ai", "llm", "ml", "agent", "openai"]
TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def is_tool_script(filename):
    lower = filename.lower()
    return (
        filename.endswith(".py")
        and filename != os.path.basename(__file__)
        and any(k in lower for k in TOOLBOX_KEYWORDS)
    )

def find_tools():
    return sorted([f for f in os.listdir(TOOL_DIR) if is_tool_script(f)])

def get_docstring(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        in_doc = False
        doc = []
        for line in lines:
            line = line.strip()
            if (line.startswith('"""') or line.startswith("'''")) and not in_doc:
                in_doc = True
                if len(line) > 3:
                    doc.append(line[3:].strip())
                continue
            if in_doc:
                if line.endswith('"""') or line.endswith("'''"):
                    doc.append(line[:-3].strip())
                    break
                doc.append(line)
        return " ".join(doc).strip() if doc else None
    except Exception:
        return None

def show_tools(tools):
    print("\nAvailable AI Tools:\n")
    for tool in tools:
        desc = get_docstring(os.path.join(TOOL_DIR, tool))
        print(f"  {tool}")
        if desc:
            print(f"    → {desc}")
    print("\nUsage:")
    print("  python ai_toolbox.py <toolname.py> [args...]")
    print("  python ai_toolbox.py list   # List tools again")
    print("  python ai_toolbox.py help   # Show this message\n")

def main():
    tools = find_tools()
    if len(sys.argv) < 2 or sys.argv[1] in ("list", "help", "--help", "-h"):
        show_tools(tools)
        sys.exit(0)

    tool = sys.argv[1]
    if tool not in tools:
        print(f"Tool '{tool}' not found.\n")
        show_tools(tools)
        sys.exit(1)
    tool_path = os.path.join(TOOL_DIR, tool)
    args = sys.argv[2:]
    print(f"Running: {tool} {' '.join(args)}\n")
    subprocess.run([sys.executable, tool_path] + args)

if __name__ == "__main__":
    main()
