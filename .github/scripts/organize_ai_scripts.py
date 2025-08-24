import os
import shutil

# Define where files should go by extension
DESTINATIONS = {
    '.py': 'python_scripts',
    '.md': 'docs',
    '.sh': 'shell_scripts',
    '.txt': 'text_files',
}

# Required template files and their default content
REQUIRED_FILES = {
    'README.md': '# AI Script Inventory\n\nThis repository contains a collection of AI-related scripts.\n'
}

def move_file(filename, ext):
    dest_dir = DESTINATIONS.get(ext)
    if not dest_dir:
        return False  # Unknown extension, do not move
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    shutil.move(filename, os.path.join(dest_dir, filename))
    print(f"Moved {filename} to {dest_dir}/")
    return True

def check_and_create_templates():
    for fname, content in REQUIRED_FILES.items():
        if not os.path.exists(fname):
            with open(fname, 'w') as f:
                f.write(content)
            print(f"Created missing template: {fname}")

def main():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if f.startswith('.') or f in REQUIRED_FILES:
            continue  # Ignore hidden and required template files
        name, ext = os.path.splitext(f)
        moved = move_file(f, ext)
        if not moved:
            print(f"No rule for {f} (extension: {ext}), left in place.")

    check_and_create_templates()

if __name__ == "__main__":
    main()
