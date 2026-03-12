# Consulting Site Plan

## Goal

A business website showcasing work as a docs-as-code consultant. Serves two purposes:

1. Attract and inform potential clients (services, about, contact)
2. Demonstrate expertise through real project portfolio and writing

---

## Source Repos

| Repo                         | Description                                                                                        | Location       |
| ---------------------------- | -------------------------------------------------------------------------------------------------- | -------------- |
| `canvas-docs-as-code-public` | Tool for authoring Canvas LMS courses from the command line using Markdown + YAML + Python scripts | Local + GitHub |
| `intervals-icu`              | Python utility for uploading workout plans to Intervals.icu API via CSV                            | Local + GitHub |
| `canvas-api-scripts`         | (To be added) Canvas API scripts                                                                   | GitHub only    |

---

## Tool Decision: MkDocs + Material Theme

**Why MkDocs Material:**

- Python-based (matches existing toolchain)
- Professional, clean look out of the box
- Blog plugin (v9+) for thought leadership articles
- `mkdocs gh-deploy` is itself a docs-as-code workflow — credibility signal to clients
- Free hosting on GitHub Pages with custom domain support
- Upgrade path: [Material Insiders](https://squidfunk.github.io/mkdocs-material/insiders/) (~$15/mo) for social cards, tags, etc.

**Rejected alternatives:**

- Docusaurus — React/JSX overhead, Meta visual identity, overkill for solo consultant
- Jekyll — Ruby ecosystem, aging themes, less docs-native
- Astro — Better for pure business sites, but less docs-as-code credibility

---

## Multi-Repo Content Strategy

MkDocs requires all content under `docs_dir` at build time. Source docs live in separate repos. Bridge with a **Python fetch script**.

### Chosen approach: `fetch_docs.py` + GitHub Actions

A script that runs before `mkdocs build`:

- In local dev: reads from sibling directories on disk
- In CI: clones/pulls from GitHub
- Copies selected files/folders into `docs/samples/`

**Why this over alternatives:**

- `mkdocs-multirepo-plugin` — network-dependent at build time, extra plugin dependency
- Git submodules + symlinks — fiddly, manual update step

### Content layer split

| Layer                 | Location                   | Audience            | Purpose                                     |
| --------------------- | -------------------------- | ------------------- | ------------------------------------------- |
| Case study pages      | Written fresh in site repo | Clients             | Problem → solution → outcome narrative      |
| Documentation samples | Pulled from source repos   | Clients + technical | Authentic evidence of documentation quality |

---

## Site Structure

```
consulting-site/
├── .github/
│   └── workflows/
│       └── deploy.yml             # builds & deploys on push
├── docs/
│   ├── index.md                   # home/landing page + value prop
│   ├── services.md
│   ├── about.md
│   ├── blog/                      # thought leadership on docs-as-code
│   ├── portfolio/
│   │   ├── canvas-docs.md         # case study (client-facing narrative)
│   │   ├── intervals-icu.md
│   │   └── canvas-api-scripts.md
│   └── samples/                   # populated by fetch_docs.py at build time
│       ├── canvas-docs/           # pulled from canvas-docs-as-code-public
│       ├── intervals-icu/         # pulled from intervals-icu
│       └── canvas-api-scripts/    # pulled from GitHub
├── fetch_docs.py                  # glue script — pulls docs from source repos
├── mkdocs.yml
└── requirements.txt
```

---

## Deployment

**Hosting:** GitHub Pages (free) + custom domain (already owned)
**Optional upgrade:** Netlify free tier — easier custom domain setup, branch preview deployments

### CI/CD flow

```
push to source repo  →  webhook (optional)  ┐
push to site repo    ──────────────────────→ GitHub Actions:
                                              1. checkout site repo
                                              2. python fetch_docs.py
                                              3. mkdocs build
                                              4. deploy to gh-pages branch
```

With a webhook on each source repo, any content update automatically triggers a site rebuild.

---

## Implementation Steps (in order)

1. Create `consulting-site` repo on GitHub
2. Initialize MkDocs Material (`pip install mkdocs-material`)
3. Write `fetch_docs.py` to pull docs from source repos
4. Write GitHub Actions workflow (`deploy.yml`)
5. Write stub pages: home, services, about
6. Write case study pages for each project
7. Configure custom domain in GitHub Pages settings
8. (Optional) Set up source repo webhooks for auto-rebuild
9. (Optional) Upgrade to Material Insiders for social cards + tags

---

## Notes

- Case study pages should tell the **client story**: what problem existed, what was built, what it demonstrates about consulting value — not just a copy of the README
- The fetch script + CI pipeline is itself a portfolio piece and talking point with clients
- Blog posts about docs-as-code practice signal active expertise; aim for 1-2 before launch
