import os

# List of common stdlib module names (not exhaustive, but covers the problem ones)
stdlib_modules = [
    "abc", "argparse", "array", "ast", "asyncio", "base64", "binascii", "bisect", "builtins",
    "calendar", "cmath", "collections", "concurrent", "contextlib", "copy", "csv", "ctypes",
    "datetime", "decimal", "difflib", "dis", "doctest", "enum", "errno", "faulthandler", "fnmatch",
    "fractions", "functools", "gc", "getopt", "getpass", "gettext", "glob", "gzip", "hashlib",
    "heapq", "hmac", "html", "http", "imaplib", "importlib", "inspect", "io", "ipaddress",
    "itertools", "json", "keyword", "linecache", "locale", "logging", "lzma", "math", "mmap",
    "multiprocessing", "numbers", "operator", "os", "pathlib", "pickle", "pkgutil", "platform",
    "plistlib", "pprint", "profile", "pstats", "queue", "random", "re", "reprlib", "sched",
    "secrets", "select", "selectors", "shlex", "shutil", "signal", "site", "socket", "sqlite3",
    "ssl", "stat", "statistics", "string", "struct", "subprocess", "sys", "tempfile", "termios",
    "textwrap", "threading", "time", "timeit", "tkinter", "token", "traceback", "types", "typing",
    "unicodedata", "unittest", "urllib", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "xml", "zipfile", "zoneinfo"
]

def find_conflicts(directory):
    conflicts = []
    for fname in os.listdir(directory):
        base, ext = os.path.splitext(fname)
        if ext == ".py" and base in stdlib_modules:
            conflicts.append(fname)
    return conflicts

def auto_rename(directory, conflicts):
    for fname in conflicts:
        base, ext = os.path.splitext(fname)
        new_name = base + "_mod" + ext
        old_path = os.path.join(directory, fname)
        new_path = os.path.join(directory, new_name)
        print(f"Renaming {fname} -> {new_name}")
        os.rename(old_path, new_path)

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    found = find_conflicts(here)
    if found:
        print("WARNING: The following files in ai_related/ shadow standard library modules and should be renamed:")
        for f in found:
            print(f"  - {f}")
        choice = input("\nType 'y' to auto-rename these files by appending '_mod.py', or anything else to just exit: ").strip().lower()
        if choice == 'y':
            auto_rename(here, found)
            print("Files renamed! Remember to update any imports in your code.")
        else:
            print("No files renamed. Please rename them manually to avoid import issues.")
    else:
        print("No standard library shadowing modules found in ai_related/.")
