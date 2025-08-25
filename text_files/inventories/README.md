# Text Files Inventories

This directory contains current file inventories and catalogs that document the repository contents and system state.

## Contents

### current_filetree.txt
- **Purpose**: Complete directory tree listing from the user's file system
- **Size**: ~3.0MB (38,731 lines)
- **Usage**: System documentation and reference
- **Note**: Contains comprehensive file system structure information

### current_script_list.txt  
- **Purpose**: Comprehensive catalog of AI scripts and project files
- **Size**: ~1.8MB (21,183 lines)
- **Usage**: Project documentation and script discovery
- **Note**: Contains extensive AI script listings and project information

## Guidelines

### File Management
- Keep only current versions of inventory files in this directory
- Archive timestamped versions in the `../archives/` directory
- Implement size limits (target: <1MB per file for new inventories)
- Consider compression for very large inventory files

### Content Updates
- Update inventories when significant repository changes occur
- Use descriptive naming for new inventory files
- Document the purpose and update frequency of each inventory
- Remove obsolete or redundant inventory files

### Automation
- Use automated tools to generate inventories when possible
- Implement deduplication to prevent duplicate inventory files
- Set up regular cleanup of outdated inventory content
- Create scripts to summarize large inventory files

## Related Files
- See `../archives/` for historical versions of inventory files
- See `../generated/` for auto-generated inventory content
- See repository root for organization scripts and tools