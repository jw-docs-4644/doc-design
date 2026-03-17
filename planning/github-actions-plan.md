# Plan: Automate Publishing with GitHub Actions

## Goal

Replace the manual build-and-deploy steps with GitHub Actions so that pushing to `canvas-docs-as-code-public` automatically triggers a site rebuild and deploy on `doc-design`.

## Current manual workflow

1. Edit content in private `canvas-docs-as-code` repo
2. Run `publish.sh` → pushes curated content to `canvas-docs-as-code-public`
3. In `doc-design`: run `python scripts/pull_portfolio_docs.py`
4. Run `mkdocs build`
5. Run `mkdocs gh-deploy`

Steps 3–5 are what the action automates.

## What to build

### 1. Deploy action in `doc-design`

File: `.github/workflows/deploy.yml`

Triggers:
- Push to `main` (handles changes to site content like case-study.md)
- `repository_dispatch` event of type `portfolio-updated` (handles upstream portfolio changes)

Steps:
1. Checkout repo
2. Set up Python
3. Install mkdocs (`pip install mkdocs`)
4. Run `python scripts/pull_portfolio_docs.py`
5. Run `mkdocs gh-deploy --force`

### 2. Notify action in `canvas-docs-as-code-public`

File: `.github/workflows/notify.yml`

Triggers:
- Push to `main`

Steps:
1. Use `actions/github-script` to send a `repository_dispatch` event to `doc-design`
2. Requires a Personal Access Token stored as a secret (`DOC_DESIGN_TOKEN`)

## Setup steps

1. Create a GitHub Personal Access Token (classic) with `repo` scope
2. Add it as a secret named `DOC_DESIGN_TOKEN` in the `canvas-docs-as-code-public` repo settings
3. Add `.github/workflows/deploy.yml` to `doc-design`
4. Add `.github/workflows/notify.yml` to `canvas-docs-as-code-public`
5. Push both and verify the chain fires end-to-end

## Notes

- The `pull_portfolio_docs.py` script clones from GitHub over HTTPS — no extra credentials needed in the action since the repo is public
- `mkdocs gh-deploy` pushes to the `gh-pages` branch; the action runner needs write access to `doc-design`, which is automatic for actions running within that repo
- Once this is working, the full trigger chain is: edit private repo → `publish.sh` → push. Nothing else manual.
- Having a working `deploy.yml` in the public repo is itself a portfolio signal — it shows the full CI/CD pattern, not just the docs tooling
