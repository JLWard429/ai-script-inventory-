#!/bin/bash
set -e

echo "🔄 AI Orchestra - Repository Merger"
echo "=================================="

# Configure git if needed
git config --global user.name "JLWard429" || true
git config --global user.email "your-email@example.com" || true

# Add all files to git
git add .

# Commit changes
git commit -m "🚀 Implement Superhuman AI Terminal with intent recognition

- Created AI module with intent recognition
- Implemented Superhuman Terminal interface
- Set up directory structure for script organization
- Added comprehensive documentation
- Fixed issue #1"

echo "✅ Repository changes committed successfully!"
echo ""
echo "To push to your repository:"
echo "  git push origin main"
echo ""
echo "To merge with AI-Orchestra-Setup repository:"
echo "  git remote add orchestra https://github.com/JLWard429/AI-Orchestra-Setup.git"
echo "  git fetch orchestra"
echo "  git merge orchestra/main --allow-unrelated-histories"
echo "  git push orchestra main"
