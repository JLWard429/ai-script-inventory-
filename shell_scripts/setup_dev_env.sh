#!/bin/bash
# AI Script Inventory - Development Setup Script
#
# This script automates the initial setup of the development environment
# for the AI Script Inventory superhuman workflow system.
#
# Usage: ./setup_dev_env.sh
# Author: AI Script Inventory Team
# Date: 2025-08-24

set -euo pipefail

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️ INFO:${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ SUCCESS:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠️ WARNING:${NC} $1"
}

log_error() {
    echo -e "${RED}❌ ERROR:${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
check_python() {
    log_info "Checking Python installation..."
    
    if ! command_exists python3; then
        log_error "Python 3 is not installed. Please install Python 3.8+ first."
        return 1
    fi
    
    local python_version
    python_version=$(python3 --version | cut -d' ' -f2)
    local major_version
    major_version=$(echo "$python_version" | cut -d'.' -f1)
    local minor_version
    minor_version=$(echo "$python_version" | cut -d'.' -f2)
    
    if [[ $major_version -eq 3 && $minor_version -ge 8 ]]; then
        log_success "Python $python_version detected"
        return 0
    else
        log_error "Python 3.8+ required, but $python_version found"
        return 1
    fi
}

# Check Git installation
check_git() {
    log_info "Checking Git installation..."
    
    if ! command_exists git; then
        log_error "Git is not installed. Please install Git first."
        return 1
    fi
    
    local git_version
    git_version=$(git --version | cut -d' ' -f3)
    log_success "Git $git_version detected"
    return 0
}

# Setup Python virtual environment
setup_venv() {
    log_info "Setting up Python virtual environment..."
    
    if [[ -d "venv" ]]; then
        log_warning "Virtual environment already exists"
        return 0
    fi
    
    python3 -m venv venv
    # shellcheck source=/dev/null
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    
    log_success "Virtual environment created and activated"
    return 0
}

# Install dependencies
install_dependencies() {
    log_info "Installing project dependencies..."
    
    if [[ -f "requirements-dev.txt" ]]; then
        pip install -r requirements-dev.txt
        log_success "Development dependencies installed"
    else
        log_warning "requirements-dev.txt not found, skipping dependency installation"
    fi
    
    return 0
}

# Setup pre-commit hooks
setup_precommit() {
    log_info "Setting up pre-commit hooks..."
    
    if command_exists pre-commit; then
        pre-commit install
        log_success "Pre-commit hooks installed"
    else
        log_warning "pre-commit not available, skipping hook installation"
    fi
    
    return 0
}

# Run initial tests
run_initial_tests() {
    log_info "Running initial tests to verify setup..."
    
    if command_exists pytest && [[ -d "tests" ]]; then
        pytest tests/ -v
        log_success "Initial tests passed"
    else
        log_warning "pytest not available or tests directory not found, skipping tests"
    fi
    
    return 0
}

# Validate GitHub Actions workflows
validate_workflows() {
    log_info "Validating GitHub Actions workflows..."
    
    local workflow_dir=".github/workflows"
    if [[ -d "$workflow_dir" ]]; then
        local yaml_files
        yaml_files=$(find "$workflow_dir" -name "*.yml" -o -name "*.yaml")
        
        if [[ -n "$yaml_files" ]]; then
            for file in $yaml_files; do
                log_info "Found workflow: $(basename "$file")"
            done
            log_success "GitHub Actions workflows found"
        else
            log_warning "No workflow files found in $workflow_dir"
        fi
    else
        log_warning "GitHub workflows directory not found"
    fi
    
    return 0
}

# Create development shortcuts
create_shortcuts() {
    log_info "Creating development shortcuts..."
    
    # Create a simple activation script
    cat > activate_dev.sh << 'EOF'
#!/bin/bash
# Activate development environment for AI Script Inventory

if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
    echo "🚀 Development environment activated!"
    echo ""
    echo "Available commands:"
    echo "  python python_scripts/dev_tools.py --help    # Development tools"
    echo "  pytest tests/ -v                             # Run tests"
    echo "  pre-commit run --all-files                   # Run pre-commit hooks"
    echo "  black .                                       # Format code"
    echo "  flake8 .                                      # Lint code"
    echo ""
else
    echo "❌ Virtual environment not found. Run ./setup_dev_env.sh first."
fi
EOF
    
    chmod +x activate_dev.sh
    log_success "Development shortcuts created (activate_dev.sh)"
    
    return 0
}

# Display helpful information
show_next_steps() {
    echo ""
    echo "🎉 Development environment setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Activate the environment: source venv/bin/activate"
    echo "   Or use the shortcut: ./activate_dev.sh"
    echo ""
    echo "2. Run development tools:"
    echo "   python python_scripts/dev_tools.py --help"
    echo ""
    echo "3. Make your first contribution:"
    echo "   - Create a new branch: git checkout -b feature/your-feature"
    echo "   - Make your changes"
    echo "   - Run quality checks: python python_scripts/dev_tools.py all"
    echo "   - Commit and push: git commit -m 'feat: your changes'"
    echo ""
    echo "4. The superhuman workflow will automatically:"
    echo "   ✅ Format your code"
    echo "   ✅ Run security scans"
    echo "   ✅ Organize files"
    echo "   ✅ Update documentation"
    echo "   ✅ Run comprehensive tests"
    echo ""
    echo "Happy coding! 🚀"
}

# Main setup function
main() {
    echo "🤖 AI Script Inventory - Development Environment Setup"
    echo "======================================================"
    echo ""
    
    # Check prerequisites
    check_python || exit 1
    check_git || exit 1
    
    # Setup environment
    setup_venv || exit 1
    install_dependencies || exit 1
    setup_precommit || exit 1
    
    # Validation and testing
    validate_workflows || exit 1
    run_initial_tests || exit 1
    
    # Final setup
    create_shortcuts || exit 1
    show_next_steps
    
    return 0
}

# Only run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi