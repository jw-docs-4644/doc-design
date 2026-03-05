#!/bin/bash
set -e

echo "🔄 Building consulting site with portfolio sync..."

# Pull latest portfolio docs from external repos
python3 scripts/pull_portfolio_docs.py

# Build the mkdocs site
mkdocs build

echo "✅ Site built successfully!"
