#!/usr/bin/env python3
"""
Pull documentation from external repos into the consulting site portfolio.
Runs before mkdocs builds to sync latest docs from source projects.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# Portfolio projects: {folder_name: (github_url, source_docs_path)}
# source_docs_path is relative to repo root
PORTFOLIO_PROJECTS = {
    "canvas-docs-as-code-public": (
        "https://github.com/jw-docs-4644/canvas-docs-as-code-public.git",
        "docs",
    ),
    "intervals-icu": (
        "https://github.com/jw-docs-4644/intervals-icu.git",
        None,  # Special case: build docs from README
    ),
}

DOCS_ROOT = Path(__file__).parent.parent / "docs" / "portfolio"
TEMP_DIR = Path(tempfile.gettempdir()) / "portfolio_sync"


def ensure_portfolio_dir():
    """Create portfolio directory if it doesn't exist."""
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)


def sync_project(project_name: str, repo_url: str, source_path: str) -> None:
    """Clone/pull a repo and copy its docs to portfolio."""
    project_dir = DOCS_ROOT / project_name
    repo_dir = TEMP_DIR / project_name

    print(f"\n📦 Syncing {project_name}...")

    # Clone or update repo
    if repo_dir.exists():
        print(f"  → Updating existing repo...")
        subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=repo_dir,
            check=True,
            capture_output=True,
        )
    else:
        print(f"  → Cloning repo...")
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", repo_url, str(repo_dir)],
            check=True,
            capture_output=True,
        )

    # Handle special case for intervals-icu: build docs from README
    if source_path is None:
        readme = repo_dir / "README.md"
        if not readme.exists():
            print(f"  ⚠️  No README.md found in {project_name}")
            return

        # Create docs folder and copy README as index
        project_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(readme, project_dir / "index.md")
        print(f"  ✓ Synced README to docs/portfolio/{project_name}/index.md")
        return

    # Standard case: copy docs folder
    source_docs = repo_dir / source_path
    if not source_docs.exists():
        print(f"  ⚠️  No {source_path}/ folder found in {project_name}")
        return

    # Remove old portfolio version and copy new one
    if project_dir.exists():
        shutil.rmtree(project_dir)

    shutil.copytree(source_docs, project_dir)
    print(f"  ✓ Synced to docs/portfolio/{project_name}/")


def main():
    """Sync all portfolio projects."""
    print("🚀 Pulling portfolio documentation...")

    ensure_portfolio_dir()

    for project_name, (repo_url, source_path) in PORTFOLIO_PROJECTS.items():
        try:
            sync_project(project_name, repo_url, source_path)
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Error syncing {project_name}: {e}")
            raise
        except Exception as e:
            print(f"  ✗ Unexpected error with {project_name}: {e}")
            raise

    print("\n✅ Portfolio documentation synced successfully!")


if __name__ == "__main__":
    main()
