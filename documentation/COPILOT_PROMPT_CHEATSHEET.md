<<<<
# 🤖 GitHub Copilot Prompt Cheat Sheet for Browser Use

A comprehensive guide to effective GitHub Copilot prompts for Chat, Workspace, and Pull Requests to maximize your AI-powered development workflow.

[![Powered by Copilot](https://img.shields.io/badge/powered%20by-copilot-blue?logo=github)](https://github.com/features/copilot)

---

## 🗂️ Table of Contents

1. [GitHub Copilot Chat](#-github-copilot-chat)
2. [GitHub Copilot Workspace](#-github-copilot-workspace)
3. [GitHub Copilot Pull Requests](#-github-copilot-pull-requests)
4. [Pro Tips & Best Practices](#-pro-tips--best-practices)
5. [Slash Commands Reference](#-slash-commands-reference)
6. [Official Documentation](#-official-documentation)

---

## 💬 GitHub Copilot Chat

### Code Generation & Refactoring

```markdown
# Function/Method Creation
"Create a Python function that validates email addresses using regex"
"Generate a TypeScript interface for a user profile with validation"
"Write a React component for a responsive navigation bar"

# Code Refactoring
"Refactor this function to use async/await instead of callbacks"
"Convert this class-based component to a functional component with hooks"
"Optimize this SQL query for better performance"
"Add error handling to this function"

# Code Analysis
"Explain what this code does step by step"
"Find potential bugs or issues in this code"
"Suggest improvements for code readability"
"Check for security vulnerabilities in this function"
```

### Documentation & Comments

```markdown
# Documentation Generation
"Generate JSDoc comments for this function"
"Create a comprehensive README for this project"
"Write docstrings for all methods in this Python class"
"Generate API documentation for these endpoints"

# Code Comments
"Add inline comments explaining this complex algorithm"
"Create a header comment for this file explaining its purpose"
"Generate TODO comments for missing functionality"
```

### Testing & Quality Assurance

```markdown
# Test Generation
"Create unit tests for this function using Jest"
"Generate pytest test cases for this Python class"
"Write integration tests for this API endpoint"
"Create mock data for testing this component"

# Code Quality
"Review this code for best practices"
"Check this code against SOLID principles"
"Suggest performance optimizations"
"Identify code smells and suggest fixes"
```

### Debugging & Troubleshooting

```markdown
# Bug Analysis
"Help me debug this error: [paste error message]"
"Why is this function returning undefined?"
"Explain why this CSS isn't working as expected"
"Help me understand this stack trace"

# Performance Issues
"Why is this query running slowly?"
"How can I optimize this algorithm?"
"Find memory leaks in this code"
"Suggest caching strategies for this function"
```

### Architecture & Design Patterns

```markdown
# System Design
"Design a microservices architecture for an e-commerce platform"
"Suggest a database schema for a social media app"
"Recommend design patterns for this use case"
"Help me structure this large React application"

# Code Organization
"How should I organize these utility functions?"
"Suggest a folder structure for this project"
"Recommend naming conventions for this codebase"
```

---

## 🏗️ GitHub Copilot Workspace

### Project Planning & Architecture

```markdown
# Initial Project Setup
"Create a modern React app with TypeScript, Tailwind CSS, and testing setup"
"Set up a Node.js REST API with Express, MongoDB, and authentication"
"Initialize a Python web scraper project with proper error handling"
"Design a microservices architecture for a task management system"

# File Structure Planning
"Plan the folder structure for a full-stack MERN application"
"Organize files for a Python machine learning project"
"Structure a component library with Storybook integration"
"Design directory layout for a multi-tenant SaaS application"
```

### Feature Implementation

```markdown
# Complete Features
"Build a complete user authentication system with JWT tokens"
"Implement a shopping cart with local storage persistence"
"Create a real-time chat feature using WebSockets"
"Build a file upload system with progress tracking"

# Complex Functionality
"Implement pagination for large datasets with search and filtering"
"Create a drag-and-drop task board like Trello"
"Build a data visualization dashboard with charts"
"Implement role-based access control (RBAC) system"
```

### Configuration & Setup

```markdown
# Development Environment
"Set up ESLint, Prettier, and Husky for code quality"
"Configure Webpack for a React TypeScript project"
"Set up GitHub Actions for CI/CD pipeline"
"Configure Docker for local development environment"

# Tool Integration
"Integrate Stripe payment processing"
"Set up Sentry for error monitoring"
"Configure Redis for caching"
"Set up automated database migrations"
```

### Code Quality & Standards

```markdown
# Code Standards
"Establish coding conventions for a team of 5 developers"
"Create TypeScript strict configuration"
"Set up comprehensive testing strategy"
"Implement automated code review guidelines"

# Documentation Standards
"Create contributing guidelines for open source project"
"Set up automated API documentation"
"Establish code comment standards"
"Create troubleshooting guides"
```

---

## 🔍 GitHub Copilot Pull Requests

### Pull Request Analysis

```markdown
# Code Review
"Review this pull request for potential issues"
"Check for breaking changes in this PR"
"Analyze the impact of these changes on performance"
"Verify that proper error handling is implemented"

# Security Review
"Check this PR for security vulnerabilities"
"Review authentication and authorization changes"
"Validate input sanitization in these changes"
"Check for potential data leaks"
```

### Pull Request Enhancement

```markdown
# Code Improvement Suggestions
"Suggest improvements for code readability in this PR"
"Recommend performance optimizations"
"Identify opportunities for code reuse"
"Suggest better variable and function names"

# Testing Enhancement
"Identify missing test cases for this PR"
"Suggest additional edge cases to test"
"Recommend integration tests for these changes"
"Check test coverage for new functionality"
```

### Documentation & Communication

```markdown
# PR Description Enhancement
"Generate a comprehensive description for this pull request"
"Create a changelog entry for these changes"
"List the breaking changes in this PR"
"Generate migration guide for API changes"

# Review Comments
"Explain why this approach might cause issues"
"Suggest alternative implementation strategies"
"Provide examples of better error handling"
"Explain the benefits of this refactoring"
```

### Merge & Deployment Readiness

```markdown
# Pre-merge Checklist
"Create a checklist for merging this PR safely"
"Identify dependencies that need to be updated"
"Check backward compatibility of these changes"
"Verify all CI/CD checks are passing"

# Deployment Planning
"Create deployment steps for these database changes"
"Identify rollback procedures for this feature"
"Plan feature flag strategy for gradual rollout"
"Document monitoring and alerting requirements"
```

---

## ⚡ Pro Tips & Best Practices

### Writing Effective Prompts

#### 🎯 Be Specific and Contextual
```markdown
❌ "Fix this code"
✅ "Fix the memory leak in this React component by properly cleaning up event listeners in useEffect"

❌ "Make this better"
✅ "Refactor this function to follow SOLID principles and improve testability"
```

#### 🗂️ Provide Context
```markdown
# Always include relevant context
"I'm building a Next.js e-commerce site. Create a product search component with filtering by category, price range, and ratings."

# Mention your tech stack
"Using React 18 with TypeScript, create a custom hook for managing form state with validation."
```

#### 📋 Break Down Complex Tasks
```markdown
# Instead of one large request
❌ "Build a complete authentication system"

# Break it down
✅ "Create a login form component with email and password validation"
✅ "Implement JWT token storage and refresh logic"
✅ "Add protected route wrapper component"
```

### Advanced Prompting Techniques

#### 🔄 Iterative Refinement
```markdown
1. "Create a basic user profile component"
2. "Add form validation to the user profile component"
3. "Add photo upload functionality to the profile component"
4. "Add social media links section to the profile"
```

#### 🎭 Role-Based Prompting
```markdown
"As a senior React developer, review this component for best practices"
"From a security expert perspective, audit this authentication function"
"As a UX designer, suggest improvements to this form interface"
```

#### 📊 Constraint-Based Prompting
```markdown
"Create a function that must handle 10,000+ concurrent users"
"Build a component that works without JavaScript enabled"
"Design an API that must respond within 100ms"
"Write code that passes all ESLint strict rules"
```

### Context Optimization

#### 📎 Use @mentions Effectively
```markdown
# Reference specific files
"@workspace Look at the user model and create matching validation schema"

# Reference docs
"@github Create integration tests based on the API documentation"

# Reference current selection
"@selection Optimize this database query for better performance"
```

#### 🔍 Leverage Code Context
```markdown
# Reference surrounding code
"Following the pattern used in other components in this file, create a similar component for products"

# Reference project conventions
"Using the same error handling pattern as other API routes, create an endpoint for user preferences"
```

---

## 🛠️ Slash Commands Reference

### Essential Slash Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `/explain` | Explain selected code | `/explain How does this authentication middleware work?` |
| `/fix` | Fix bugs or issues | `/fix the memory leak in this component` |
| `/doc` | Generate documentation | `/doc Create JSDoc comments for this function` |
| `/tests` | Generate test cases | `/tests Create unit tests for this utility function` |
| `/optimize` | Improve performance | `/optimize this database query for better speed` |

### Advanced Slash Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `/simplify` | Reduce complexity | `/simplify this nested conditional logic` |
| `/secure` | Add security measures | `/secure this user input validation` |
| `/api` | API-related tasks | `/api Create REST endpoints for user management` |
| `/terminal` | Command line help | `/terminal Help me write a bash script for deployment` |

---

## 📚 Official Documentation

### GitHub Copilot Resources

- **[GitHub Copilot Documentation](https://docs.github.com/en/copilot)** - Complete official documentation
- **[GitHub Copilot Chat](https://docs.github.com/en/copilot/github-copilot-chat)** - Chat-specific features and usage
- **[GitHub Copilot Workspace](https://githubnext.com/projects/copilot-workspace)** - Workspace features and capabilities
- **[Copilot in Pull Requests](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-your-ide)** - PR integration guide

### Best Practices Guides

- **[Prompt Engineering Guide](https://github.com/microsoft/prompt-engineering-guide)** - Advanced prompting techniques
- **[AI-Assisted Development](https://github.blog/category/ai/)** - GitHub Blog AI content
- **[Copilot Patterns](https://github.com/microsoft/copilot-productivity-patterns)** - Productivity patterns and examples

### Community Resources

- **[Awesome Copilot](https://github.com/topics/github-copilot)** - Community projects and resources
- **[Copilot Discussions](https://github.com/community/community/discussions/categories/copilot)** - Community discussions and tips
- **[VS Code Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)** - IDE integration

---

## 🎨 Quick Reference Card

### 🚀 Power User Shortcuts

```markdown
# Quick Code Generation
"func + [description]" → Function generation
"comp + [description]" → Component creation  
"test + [description]" → Test case generation
"fix + [error]" → Bug fixing

# Quick Documentation
"doc this" → Add documentation
"explain this" → Code explanation
"comment this" → Add inline comments
"readme for this" → Generate README
```

### 🎯 Context Patterns

```markdown
# File-level context
"In this [file type], create a [specific component]"
"Following this file's pattern, add [new functionality]"

# Project-level context  
"For this [project type], implement [feature]"
"Using this project's architecture, add [component]"

# Code-level context
"Based on this function, create a similar one that [variation]"
"Refactor this code to follow the same pattern as [reference]"
```

---

**💡 Remember**: GitHub Copilot learns from context, so the more specific and detailed your prompts, the better the results. Always review and test AI-generated code before using it in production!

---

*This cheat sheet is maintained by the AI Script Inventory project. For updates and contributions, visit our [GitHub repository](https://github.com/JLWard429/ai-script-inventory-).*
=======
# 🤖 GitHub Copilot Prompt Cheat Sheet (For Browser Use)

Use these prompts and commands with GitHub Copilot Chat, Copilot Workspace, and Copilot for Pull Requests right in your browser to accelerate and automate your repo management and code review.

---

## 📝 General Prompts (Type in Copilot Chat or Copilot Workspace)

- "Audit my repository for common issues."
- "Clean up unused code and files in this repository."
- "Tidy up all workflows and configuration files."
- "Fix all lint and formatting errors project-wide."
- "Summarize all open pull requests and highlight conflicts."
- "Suggest improvements for this codebase."
- "Optimize dependencies and update outdated packages."
- "Identify and suggest fixes for security vulnerabilities."
- "Generate or update documentation for this project."
- "What are the biggest risks or code smells in this repo?"

---

## 🚀 Copilot for Pull Requests (Type in PR comments or Copilot side panel)

- /copilot summarize
  - Summarizes the pull request changes.
- /copilot fix this
  - Suggests a fix for code or workflow issues in the PR.
- /copilot resolve conflicts
  - Proposes a way to resolve merge conflicts.
- /copilot document
  - Generates or updates documentation for changes in the PR.
- /copilot test
  - Suggests or creates tests related to the PR.
- /copilot review
  - Provides a general code review or improvement suggestions.

---

## 🧠 Copilot Workspace & Chat (Describe Your Task)

- "Refactor and modernize this entire repo."
- "Automate dependency updates and workflow optimizations."
- "Find and fix all potential bugs and errors."
- "Streamline project structure and remove redundant files."
- "Prepare this repo for production deployment."
- "Help me merge all passing pull requests and delete merged branches."

---

## ⚡ Pro Tips

- You can often combine instructions:  
  "Summarize open PRs, suggest merges, and clean up merged branches."
- For large tasks, Copilot may respond with a plan and ask for approval before making changes.
- Always review Copilot’s suggestions before applying changes, especially for critical code or configurations.
- Not all commands may be available in every Copilot panel—feature availability depends on your GitHub Copilot and repo settings.

---

## 📚 References

- [Copilot for Pull Requests](https://docs.github.com/en/copilot/github-copilot-for-pull-requests)
- [Copilot Chat](https://docs.github.com/en/copilot/github-copilot-chat)
- [Copilot Workspace](https://docs.github.com/en/copilot/copilot-workspace)
- [Copilot Prompts Examples](https://docs.github.com/en/copilot/using-github-copilot-in-your-repository#prompt-examples)

