# Single-Sourcing Portfolio Docs

## Goal

Have an overview page for each portfolio project written in doc-consulting, while pulling sample docs directly from their source repos — so documentation is single-sourced and doesn't need to be manually kept in sync.

## Current State

The `docs/portfolio/canvas-docs-as-code-public/` folder contains **copies** of files from the canvas-docs-as-code repo. These are not single-sourced — updates to the originals require a manual re-copy.

## Options

### Option 1: Symlinks (Recommended)

Replace the copied folder with a symlink pointing to the actual files in the source repo. MkDocs supports symlinks natively. Simple, no extra tooling required.

```bash
rm -rf docs/portfolio/canvas-docs-as-code-public
ln -s /home/josh/Repos/canvas-docs-as-code/docs docs/portfolio/canvas-docs-as-code-public
```

**Pros:** Simple, no plugins needed, works out of the box with MkDocs
**Cons:** Symlinks are machine-specific — won't work on other machines or CI without the same repo layout

### Option 2: mkdocs-monorepo-plugin

A plugin designed for pulling docs from multiple repos into a single MkDocs site. More portable and explicit than symlinks.

**Pros:** Designed for this use case, works in CI
**Cons:** Requires installing and configuring the plugin

## Nav Structure

Regardless of which option is used, the `nav:` in `mkdocs.yml` controls exactly what's displayed. You can mix overview pages written in doc-consulting with sample docs pulled from source repos:

```yaml
- Portfolio:
  - Canvas Docs-as-Code:
    - Overview: portfolio/canvas/overview.md                              # written in doc-consulting
    - README: portfolio/canvas-docs-as-code-public/README_UPDATES.md     # from source repo
    - Multi-Machine Setup: portfolio/canvas-docs-as-code-public/multi_machine_setup.md
```

Files not listed in `nav:` are not published, so you have full control over what appears on the site.
