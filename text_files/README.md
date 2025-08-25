# Text Files

This directory contains organized text files, inventories, notes, and miscellaneous documentation for the AI Script Inventory project.

## Directory Structure

### `/inventories/`
Current file inventories and catalogs that document repository contents and system state:
- `current_filetree.txt` - Complete system directory tree (3.0MB)
- `current_script_list.txt` - Comprehensive AI script catalog (1.8MB)

### `/archives/`  
Historical versions and timestamped duplicates preserved for reference:
- Timestamped file tree snapshots
- Historical script list versions
- Superseded configuration files

### `/generated/`
Auto-generated content from tools and automation:
- Automated reports and summaries
- Tool outputs and processing results
- Temporary files from operations

## File Management Guidelines

### Organization Principles
- **Current files** → `inventories/` (active use)
- **Historical files** → `archives/` (reference only)
- **Auto-generated** → `generated/` (tool outputs)

### Best Practices
- Use descriptive naming for new files
- Implement size limits for large inventories (target <1MB)
- Regular cleanup of obsolete content
- Compress large archives when appropriate

## Related Documentation
- See [ORGANIZATION_CHANGELOG.md](../ORGANIZATION_CHANGELOG.md) for details of recent reorganization
- See [REPO_AUDIT_PLAN.md](../REPO_AUDIT_PLAN.md) for future improvement plans
- See individual subdirectory READMEs for specific usage guidelines