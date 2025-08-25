---
applyTo: "docs/**/*.md"
---

# Documentation Instructions

When working with documentation files in the `docs/` directory, follow these guidelines for clear, comprehensive, and maintainable documentation:

## Documentation Standards

1. **Structure and Organization**
   - Use clear, hierarchical heading structure (H1, H2, H3)
   - Include table of contents for longer documents
   - Use consistent formatting and style
   - Organize related content logically

2. **Content Quality**
   - Write clear, concise, and actionable content
   - Use active voice and present tense
   - Include practical examples and code snippets
   - Provide step-by-step instructions for procedures

3. **Markdown Best Practices**
   - Use proper markdown syntax for formatting
   - Include code fences with language specification
   - Use relative links for internal references
   - Optimize images and include alt text

## Required Documentation Sections

1. **README Files**
   - Clear project description and purpose
   - Installation and setup instructions
   - Usage examples and common workflows
   - Links to additional documentation
   - Contributing guidelines and contact information

2. **Technical Documentation**
   - API reference and function documentation
   - Configuration options and parameters
   - Troubleshooting guides and FAQ
   - Architecture and design decisions

3. **User Guides**
   - Getting started tutorials
   - Feature explanations with examples
   - Best practices and tips
   - Common use cases and workflows

## Superhuman AI Terminal Documentation

When documenting the AI Terminal features:

1. **Privacy Emphasis**
   - Clearly explain local-only processing
   - Document data handling and storage
   - Emphasize security and privacy features
   - Explain offline capabilities

2. **Usage Examples**
   - Provide realistic command examples
   - Show expected outputs and responses
   - Document error handling and edge cases
   - Include troubleshooting information

## Integration with Repository

1. **Cross-References**
   - Link to relevant code files and scripts
   - Reference CI/CD workflows and automation
   - Connect to related documentation
   - Include links to external resources

2. **Automation Integration**
   - Document automated processes and workflows
   - Explain file organization system
   - Describe quality checks and validation
   - Include maintenance procedures

## Documentation Templates

### Feature Documentation Template
```markdown
# Feature Name

Brief description of what this feature does and why it's useful.

## Overview

Detailed explanation of the feature, its purpose, and how it fits into the overall system.

## Installation/Setup

Step-by-step instructions for setting up or enabling the feature.

```bash
# Example commands
command --option value
```

## Usage

### Basic Usage

Simple examples for getting started:

```bash
# Basic example
example_command input.txt
```

### Advanced Usage

More complex scenarios and options:

```bash
# Advanced example with multiple options
example_command --verbose --output /path/to/output input.txt
```

## Configuration

Description of configuration options and how to set them.

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `option1` | Description of option 1 | `default_value` | `example_value` |

## Examples

Real-world usage examples with expected outputs.

## Troubleshooting

Common issues and their solutions:

### Issue: Common Problem
**Symptoms:** Description of what users might see
**Cause:** Why this happens
**Solution:** How to fix it

## See Also

- [Related Documentation](link)
- [External Resources](link)
```

### API Documentation Template
```markdown
# API Reference

## Function Name

Brief description of what the function does.

### Syntax

```python
function_name(parameter1, parameter2, optional_param=None)
```

### Parameters

- `parameter1` (type): Description of parameter 1
- `parameter2` (type): Description of parameter 2  
- `optional_param` (type, optional): Description of optional parameter. Defaults to None.

### Returns

- `return_type`: Description of return value

### Raises

- `ExceptionType`: When this exception is raised

### Example

```python
# Example usage
result = function_name("value1", "value2")
print(result)
```

### Notes

Additional notes, warnings, or important information.
```

## Quality Assurance

1. **Review Process**
   - Peer review for accuracy and clarity
   - Test all code examples and procedures
   - Validate external links and references
   - Check grammar and spelling

2. **Maintenance**
   - Keep documentation current with code changes
   - Update examples and screenshots regularly
   - Remove outdated information promptly
   - Monitor for broken links and references

3. **Accessibility**
   - Use clear, simple language
   - Provide alternative text for images
   - Ensure good contrast and readability
   - Support screen readers with proper markup

## Style Guidelines

1. **Writing Style**
   - Use clear, professional tone
   - Avoid jargon and technical slang
   - Write for your intended audience
   - Be concise but comprehensive

2. **Formatting Consistency**
   - Use consistent heading styles
   - Apply uniform code formatting
   - Maintain consistent link styles
   - Use standard table formatting

3. **Code Examples**
   - Include complete, runnable examples
   - Show expected outputs when helpful
   - Use realistic data and scenarios
   - Comment complex code appropriately

## Integration Testing

Documentation should be tested as part of the CI/CD process:

1. **Link Validation**
   - Check all internal and external links
   - Validate relative path references
   - Ensure images and assets are accessible

2. **Code Example Testing**
   - Verify that code examples are current
   - Test installation and setup procedures
   - Validate command-line examples

3. **Consistency Checks**
   - Ensure documentation matches current features
   - Verify version numbers and compatibility
   - Check for outdated screenshots or examples