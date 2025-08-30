import os
import re

# List of modules you just renamed (match with _mod suffix)
renamed_modules = [
    "http", "warnings", "re", "faulthandler", "hashlib", "unittest", "xml", "doctest", "glob", "array",
    "hmac", "traceback", "copy", "logging", "statistics", "subprocess", "secrets", "pathlib", "types",
    "pickle", "platform", "stat", "string", "gzip", "ast", "abc", "collections", "profile", "functools",
    "math", "json", "ctypes", "asyncio", "html", "venv", "pprint", "io", "typing", "numbers", "token", "enum"
]

# Map old name to new name
rename_map = {m: f"{m}_mod" for m in renamed_modules}

def update_imports_in_file(filepath, rename_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Patterns to match import statements
    # import modulename
    pattern1 = re.compile(r'(^|\n)\s*import\s+([a-zA-Z0-9_]+)(\s|$|,|\n)')
    # from modulename import ...
    pattern2 = re.compile(r'(^|\n)\s*from\s+([a-zA-Z0-9_]+)\s+import\s')

    # Replace import modulename
    def repl1(match):
        prefix, modname, suffix = match.groups()
        if modname in rename_map:
            return f"{prefix}import {rename_map[modname]}{suffix}"
        else:
            return match.group(0)

    # Replace from modulename import ...
    def repl2(match):
        prefix, modname = match.groups()
        if modname in rename_map:
            return f"{prefix}from {rename_map[modname]} import "
        else:
            return match.group(0)

    content = pattern1.sub(repl1, content)
    content = pattern2.sub(repl2, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated imports in {filepath}")

def update_all_py_files(rootdir, rename_map):
    for dirpath, dirnames, filenames in os.walk(rootdir):
        for fname in filenames:
            if fname.endswith('.py'):
                update_imports_in_file(os.path.join(dirpath, fname), rename_map)

if __name__ == "__main__":
    # Update all .py files in ai_related/ (and subfolders)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    rootdir = this_dir
    update_all_py_files(rootdir, rename_map)
    print("All imports updated. Please review your code and test your scripts!")
