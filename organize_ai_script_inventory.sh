#!/bin/bash

# Set project root
ROOT="ai-script-inventory-"
NO_EXT="$ROOT/no_extension"
PYTHON_FILES="$ROOT/python_files"
LOST_FOUND="$ROOT/lost+found"
PROJECT_ROOT="$ROOT/ai_orchestra_project"

# Ensure directories exist
mkdir -p "$PYTHON_FILES" "$LOST_FOUND" "$PROJECT_ROOT"

echo "=== Moving LICENSE and AUTHORS to project root ==="
[ -f "$NO_EXT/LICENSE" ] && mv -v "$NO_EXT/LICENSE" "$PROJECT_ROOT/"
[ -f "$NO_EXT/Author:" ] && mv -v "$NO_EXT/Author:" "$PROJECT_ROOT/AUTHORS"

echo "=== Moving large/data/code files to python_files ==="
for file in hello jwt pkg_resources requests timedelta yes; do
    [ -f "$NO_EXT/$file" ] && mv -v "$NO_EXT/$file" "$PYTHON_FILES/"
done

echo "=== Moving zero-byte/stray files to lost+found ==="
# List zero-byte and odd files
files_to_move=(
    Automated Callback Forensic Full The To You
    "[" ai_orchestra_organized complete i no "“The"
)
for file in "${files_to_move[@]}"; do
    [ -f "$NO_EXT/$file" ] && mv -v "$NO_EXT/$file" "$LOST_FOUND/"
done

echo "=== Clean-up Complete! ==="
echo "Review '$PROJECT_ROOT', '$PYTHON_FILES', and '$LOST_FOUND' to confirm organization."
