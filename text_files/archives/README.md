# Text Files Archives

This directory contains archived versions of files, particularly timestamped duplicates that are preserved for historical reference but not actively used.

## Archival Policy

### What Gets Archived
- Timestamped duplicate files (e.g., filename_YYYYMMDDHHMMSS.ext)
- Superseded versions of configuration files
- Historical snapshots of inventory files
- Large files that are no longer current but may have historical value

### Archive Organization
- Files are archived in their original format
- Original timestamps and naming are preserved
- Related files are grouped when possible
- Large archives may be compressed to save space

## Current Archives

### File Tree Archives
- `filetree_20250825090428.txt` - System directory tree snapshot (3.0MB)
- `filetree_20250825090934.txt` - System directory tree snapshot (3.0MB)

### Script List Archives  
- `my_ai_script_list_20250825090428.txt` - AI script catalog snapshot (1.8MB)
- `my_ai_script_list_20250825090934.txt` - AI script catalog snapshot (1.8MB)

## Archive Notes

### Duplicate Analysis
All archived files above are byte-for-byte identical to their current versions in `../inventories/`. They appear to be automatically generated duplicates with timestamp suffixes.

### Storage Optimization
- **Space Saved**: 6MB by moving duplicates to archives
- **Recommendation**: Consider compression for these large identical files
- **Future**: Implement automated deduplication to prevent such duplicates

## Maintenance

### Regular Tasks
- Review archives quarterly for relevance
- Compress large archives to save space
- Remove archives that are no longer needed
- Document the purpose and retention period for each archive

### Access Guidelines
- Archives are read-only reference material
- Do not modify archived files
- Extract copies to working directories if edits are needed
- Maintain archive integrity for historical accuracy

## Related Directories
- See `../inventories/` for current versions of inventory files
- See `../generated/` for auto-generated content
- See repository root for tools that may generate archived content