---
applyTo: "shell_scripts/**/*.sh"
---

# Shell Scripts Instructions

When working with shell scripts in the `shell_scripts/` directory, follow these guidelines for reliable, secure, and maintainable bash scripts:

## Script Standards and Best Practices

1. **Script Headers and Metadata**
   - Always start with appropriate shebang: `#!/bin/bash`
   - Include script description and usage information in comments
   - Add author, date, and version information when relevant
   - Document any dependencies or requirements

2. **Error Handling and Safety**
   - Use `set -e` to exit on any error
   - Use `set -u` to treat unset variables as errors
   - Use `set -o pipefail` to catch errors in pipelines
   - Implement proper error messages and cleanup

3. **Code Style and Formatting**
   - Use consistent indentation (2 or 4 spaces)
   - Follow consistent naming conventions for variables and functions
   - Use meaningful variable and function names
   - Quote variables to prevent word splitting and globbing

## Security Considerations

1. **Input Validation**
   - Validate all user inputs and command-line arguments
   - Sanitize file paths and prevent path traversal attacks
   - Use `read -r` to prevent backslash interpretation
   - Avoid using `eval` or executing user-provided commands

2. **File Operations**
   - Use absolute paths or validate relative paths
   - Check file permissions before operations
   - Use `mktemp` for temporary files
   - Clean up temporary files on exit

3. **Privilege Management**
   - Run with minimal required privileges
   - Avoid running as root unless absolutely necessary
   - Use `sudo` judiciously and with specific commands

## Script Structure Template

```bash
#!/bin/bash

# Script Name: example_script.sh
# Description: Brief description of what this script does
# Author: Script author
# Version: 1.0
# Usage: ./example_script.sh [options] <arguments>

# Exit on any error, undefined variables, and pipe failures
set -euo pipefail

# Global variables
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Default values
DEFAULT_OUTPUT_DIR="/tmp"
VERBOSE=false
DRY_RUN=false

# Function definitions
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS] <input_file>

Description:
    Brief description of what this script does.

Options:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -n, --dry-run       Show what would be done without executing
    -o, --output DIR    Output directory (default: $DEFAULT_OUTPUT_DIR)

Examples:
    $SCRIPT_NAME input.txt
    $SCRIPT_NAME -v -o /path/to/output input.txt
    $SCRIPT_NAME --dry-run input.txt

EOF
}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

error() {
    log "ERROR: $*"
    exit 1
}

validate_file() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        error "File does not exist: $file"
    fi
    
    if [[ ! -r "$file" ]]; then
        error "File is not readable: $file"
    fi
}

cleanup() {
    # Cleanup function called on script exit
    log "Cleaning up..."
    # Remove temporary files, etc.
}

main() {
    local input_file="$1"
    local output_dir="${2:-$DEFAULT_OUTPUT_DIR}"
    
    # Validate inputs
    validate_file "$input_file"
    
    if [[ ! -d "$output_dir" ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
            log "Would create directory: $output_dir"
        else
            mkdir -p "$output_dir" || error "Failed to create output directory: $output_dir"
        fi
    fi
    
    # Main script logic here
    if [[ "$VERBOSE" == "true" ]]; then
        log "Processing file: $input_file"
        log "Output directory: $output_dir"
    fi
    
    # Example processing
    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would process $input_file to $output_dir"
    else
        # Actual processing commands
        log "Processing completed successfully"
    fi
}

# Trap for cleanup on exit
trap cleanup EXIT

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -n|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -o|--output)
            if [[ -n "${2:-}" ]]; then
                DEFAULT_OUTPUT_DIR="$2"
                shift 2
            else
                error "Option $1 requires an argument"
            fi
            ;;
        -*)
            error "Unknown option: $1"
            ;;
        *)
            # Positional argument
            if [[ -z "${INPUT_FILE:-}" ]]; then
                INPUT_FILE="$1"
            else
                error "Too many arguments"
            fi
            shift
            ;;
    esac
done

# Validate required arguments
if [[ -z "${INPUT_FILE:-}" ]]; then
    error "Input file is required"
fi

# Call main function
main "$INPUT_FILE"
```

## Testing and Validation

1. **ShellCheck Integration**
   - All scripts must pass ShellCheck validation
   - Address warnings and errors systematically
   - Use ShellCheck directives for intentional exceptions
   - Run ShellCheck in CI/CD pipeline

2. **Testing Strategies**
   - Test scripts with various input scenarios
   - Test error conditions and edge cases
   - Use dry-run modes for testing without side effects
   - Test on different systems and shell versions

3. **Documentation Testing**
   - Ensure help text is accurate and complete
   - Test all documented options and examples
   - Verify script behavior matches documentation

## Integration with Repository

1. **File Organization**
   - Scripts should work with the auto-organization system
   - Use consistent naming conventions
   - Include appropriate file extensions (.sh)
   - Make scripts executable (`chmod +x`)

2. **CI/CD Integration**
   - Scripts should be testable in automated environments
   - Include proper exit codes for success/failure
   - Support non-interactive execution
   - Handle missing dependencies gracefully

3. **Logging and Monitoring**
   - Use consistent logging formats
   - Include appropriate verbosity levels
   - Log important operations and errors
   - Support structured logging when beneficial

## Performance and Efficiency

1. **Resource Usage**
   - Avoid unnecessary file operations
   - Use efficient algorithms and data structures
   - Consider memory usage for large files
   - Optimize for common use cases

2. **Portable Code**
   - Use POSIX-compliant commands when possible
   - Avoid bash-specific features unless necessary
   - Test on different platforms and distributions
   - Document any platform-specific requirements

## Maintenance and Updates

1. **Version Control**
   - Include version information in scripts
   - Document changes and compatibility notes
   - Use semantic versioning for significant changes
   - Maintain backward compatibility when possible

2. **Dependency Management**
   - Document all external dependencies
   - Check for required commands and tools
   - Provide helpful error messages for missing dependencies
   - Consider providing installation instructions

## Common Patterns and Anti-patterns

### Good Practices
```bash
# Good: Quoted variables
cp "$source_file" "$destination_file"

# Good: Proper error checking
if ! command -v git >/dev/null 2>&1; then
    error "Git is required but not installed"
fi

# Good: Safe temporary file creation
temp_file=$(mktemp) || error "Failed to create temporary file"

# Good: Array usage for multiple items
files=("file1.txt" "file2.txt" "file3.txt")
for file in "${files[@]}"; do
    process_file "$file"
done
```

### Anti-patterns to Avoid
```bash
# Bad: Unquoted variables
cp $source_file $destination_file

# Bad: Ignoring errors
command_that_might_fail

# Bad: Unsafe parsing
for file in $(ls); do
    process_file $file
done

# Bad: Using ls output
files=$(ls *.txt)
```