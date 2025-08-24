#!/usr/bin/env python3
"""
Organize and audit root directory of repository by file type.
Moves files to type-based folders, ensures required templates exist,
and logs all actions. Designed for CI automation and safe local use.
"""

import os
import shutil
import logging
from datetime import datetime

# ================= CONFIGURATION =================

# Mapping of file extensions to destination folders
DESTINATIONS = {
    '.py': 'python_scripts',
    '.md': 'docs',
    '.sh': 'shell_scripts',
    '.txt': 'text_files',
}

# Required template files and their default content
REQUIRED_FILES = {
    'README.md': (
        "# AI Script Inventory\n\n"
        "This repository contains a collection of AI-related scripts.\n"
    ),
    # Add more templates as needed
}

# Files/directories to skip during organization
SKIP = {
    '.git', '.github', '__pycache__', 'organize_ai_scripts.log', os.path.basename(__file__)
}

# Log file name for audit trail
LOGFILE = "organize_ai_scripts.log"

# Set to True for a dry run (no actual moves/writes)
DRY_RUN = False

# =============== LOGGING SETUP ===================

logging.basicConfig(
    filename=LOGFILE,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def log_print(msg, level=logging.INFO):
    logging.log(level, msg)
    if level >= logging.WARNING:
        print(msg)

# =============== ORGANIZATION LOGIC ==============

def ensure_dir(path):
    if not os.path.exists(path):
        if not DRY_RUN:
            os.makedirs(path)
        log_print(f"Created directory: {path}")

def safe_move(src, dst_folder):
    """Move file, avoid overwriting by timestamping colliding files."""
    ensure_dir(dst_folder)
    dst = os.path.join(dst_folder, os.path.basename(src))
    if os.path.exists(dst):
        base, ext = os.path.splitext(os.path.basename(src))
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        dst = os.path.join(dst_folder, f"{base}_{timestamp}{ext}")
        log_print(f"Collision: Renaming {src} -> {os.path.basename(dst)}", logging.WARNING)
    if DRY_RUN:
        log_print(f"[DRY-RUN] Would move {src} to {dst}")
    else:
        shutil.move(src, dst)
        log_print(f"Moved {src} to {dst}")

def organize_files():
    root_files = [
        f for f in os.listdir('.')
        if os.path.isfile(f) and f not in SKIP and not f.startswith('.')
    ]
    for f in root_files:
        _, ext = os.path.splitext(f)
        if ext in DESTINATIONS:
            safe_move(f, DESTINATIONS[ext])
        else:
            log_print(f"No rule for {f} (extension: {ext}), left in place.", logging.WARNING)

def ensure_templates():
    for fname, content in REQUIRED_FILES.items():
        if not os.path.exists(fname):
            if DRY_RUN:
                log_print(f"[DRY-RUN] Would create missing template: {fname}")
            else:
                with open(fname, 'w') as f:
                    f.write(content)
                log_print(f"Created missing template: {fname}")

def summarize():
    log_print("\nDirectory summary after organization:\n" + "="*35)
    for d, _, files in os.walk('.'):
        if any(skip in d for skip in ('.git', '.github', '__pycache__')):
            continue
        if files:
            log_print(f"{d}: {files}")
    log_print("="*35 + "\n")

def main():
    log_print("\n=== organize_ai_scripts.py started ===", logging.INFO)
    if DRY_RUN:
        log_print("DRY RUN MODE: No files will be moved or written!", logging.WARNING)

    organize_files()
    ensure_templates()
    summarize()

    log_print("=== organize_ai_scripts.py complete ===\n", logging.INFO)

if __name__ == "__main__":
    main()
