#!/usr/bin/env python3
"""
Empty Folder Cleanup Script

This script scans the repository for empty folders and directories that contain
only .gitkeep or .gitignore files, then removes them from the repository.
It ensures that only truly empty directories are removed and that no necessary
placeholders remain unless explicitly intended.

Usage:
    python cleanup_empty_folders.py [--dry-run] [--verbose]

Example:
    python cleanup_empty_folders.py --dry-run --verbose
"""

import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import List, Set


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the script."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def is_safe_to_remove(directory: Path) -> bool:
    """
    Check if a directory is safe to remove.

    Args:
        directory: Path to the directory to check

    Returns:
        True if the directory is safe to remove, False otherwise
    """
    # Never remove .git or any path containing .git
    if ".git" in str(directory) or directory.name == ".git":
        return False

    # Don't remove essential repository directories
    essential_dirs = {
        "src",
        "tests",
        "docs",
        "python_scripts",
        "shell_scripts",
        "text_files",
        ".github",
        ".vscode",
        ".idea",
    }

    if directory.name in essential_dirs:
        return False

    # Don't remove directories that are immediate children of essential dirs
    # unless they are truly empty (no .gitkeep files needed)
    parent_name = directory.parent.name
    if parent_name in essential_dirs:
        # Be extra careful with subdirectories of essential dirs
        logging.debug(f"Checking subdirectory of essential dir: {directory}")

    return True


def find_empty_directories(
    root_path: Path, exclude_patterns: Set[str] = None
) -> List[Path]:
    """
    Find directories that are empty or contain only .gitkeep/.gitignore files.

    Args:
        root_path: Root path to start scanning from
        exclude_patterns: Set of patterns to exclude from scanning

    Returns:
        List of Path objects representing empty directories
    """
    if exclude_patterns is None:
        exclude_patterns = {".git", "__pycache__", ".pytest_cache", "node_modules"}

    empty_directories = []


        # Modify dirnames in-place to prevent descending into excluded directories
        dirnames[:] = [d for d in dirnames if not any(pattern in os.path.join(dirpath, d) for pattern in exclude_patterns)]
        # Skip excluded directories
        if current_dir.name in exclude_patterns:
            continue

        # Skip if not safe to remove
        if not is_safe_to_remove(current_dir):
            continue

        # Check if directory is empty or contains only .gitkeep/.gitignore
        if not filenames and not dirnames:
            # Completely empty directory
            empty_directories.append(current_dir)
            logging.debug(f"Found empty directory: {current_dir}")
        elif filenames and not dirnames:
            # Directory with files but no subdirectories
            # Check if it only contains .gitkeep or .gitignore files
            placeholder_files = {".gitkeep", ".gitignore"}
            if all(filename in placeholder_files for filename in filenames):
                empty_directories.append(current_dir)
                logging.debug(
                    f"Found placeholder-only directory: {current_dir} (contains: {filenames})"
                )

    # Sort by depth (deepest first) to avoid removing parent before child
    empty_directories.sort(key=lambda p: len(p.parts), reverse=True)

    return empty_directories


def remove_empty_directories(directories: List[Path], dry_run: bool = True) -> int:
    """
    Remove the specified empty directories.

    Args:
        directories: List of directories to remove
        dry_run: If True, only simulate the removal

    Returns:
        Number of directories that were (or would be) removed
    """
    removed_count = 0

    for directory in directories:
        try:
            if dry_run:
                logging.info(f"[DRY RUN] Would remove: {directory}")
            else:
                logging.info(f"Removing empty directory: {directory}")
                shutil.rmtree(directory)
            removed_count += 1
        except OSError as e:
            logging.error(f"Failed to remove {directory}: {e}")

    return removed_count


def main() -> None:
    """Entry point for command-line usage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually removing anything",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Root directory to scan (default: current directory)",
    )

    args = parser.parse_args()

    setup_logging(args.verbose)

    if not args.root.exists():
        logging.error(f"Root directory does not exist: {args.root}")
        exit(1)

    if not args.root.is_dir():
        logging.error(f"Root path is not a directory: {args.root}")
        exit(1)

    logging.info(f"Scanning for empty directories in: {args.root.absolute()}")

    try:
        empty_dirs = find_empty_directories(args.root)

        if not empty_dirs:
            logging.info("No empty directories found.")
            return

        logging.info(
            f"Found {len(empty_dirs)} empty director{'y' if len(empty_dirs) == 1 else 'ies'}:"
        )
        for directory in empty_dirs:
            logging.info(f"  - {directory}")

        if args.dry_run:
            logging.info(
                "Running in dry-run mode. Use without --dry-run to actually remove directories."
            )

        removed_count = remove_empty_directories(empty_dirs, dry_run=args.dry_run)

        if args.dry_run:
            logging.info(
                f"Dry run complete. {removed_count} director{'y' if removed_count == 1 else 'ies'} would be removed."
            )
        else:
            logging.info(
                f"Cleanup complete. {removed_count} director{'y' if removed_count == 1 else 'ies'} removed."
            )



if __name__ == "__main__":
    main()
