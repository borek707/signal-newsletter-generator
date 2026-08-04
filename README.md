# SIGNAL Newsletter Generator

Monthly B2B newsletter for CTOs, VP Engineering, and Chief Architects running distributed systems at scale.

**Philosophy:** Don't aggregate news. Aggregate lessons.

## Quick Start

```bash
# Start a new issue
cp -R template issues/2026-06

# Fill the brief
open issues/2026-06/stages/00_brief/output/brief.md

# Run stages in order
open issues/2026-06/stages/01_research/CONTEXT.md
```

## Repository Layout

```
signal-newsletter-generator/
├── _config/              # Stable reference material
├── template/             # Reusable issue pipeline
├── issues/               # One folder per published issue
│   ├── 2026-03/
│   ├── 2026-04/
│   └── 2026-05/
├── signals/              # Raw signal snippets (optional)
├── SKILL.md              # Original skill reference
└── mcp-client.js         # Chrome MCP client for research
```

## Issue Structure

1. **Intro** — `Welcome back.` + hook.
2. **Today** — 6-8 linked bullets.
3. **The Architecture Debate** — one controversy, both sides, Scalac angle.
4. **Notes from the Trenches** — one production problem + solution, Scalac angle.
5. **Signal Over Noise** — exactly 3 critical changes.
6. **Community Voice** — optional, real article synthesis.
7. **In the Know** — 3-5 short sourced items.
8. **Top Resources** — repo + article + paper.
9. **Footer + References** — fixed closing block and source list.

## Pipeline

Each issue runs through seven stages:

| Stage | Job |
|-------|-----|
| 00_brief | Frame the issue |
| 01_research | Check sources and collect signals |
| 02_select | Pick Debate, Trenches, 3 Signals |
| 03_draft | Write full newsletter |
| 04_review | Fact-check, tone-check, link-check |
| 05_publish | Final markdown + frontmatter |
| 06_post_publish | Social snippets and follow-ups |

## Configuration

All stable rules live in `_config/`:

- `newsletter-structure.md` — section definitions.
- `voice.md` — The Code format and forbidden language.
- `sources.md` — required sources and fetch methods.
- `fact-check-rules.md` — verification rules.
- `newsletter-types.md` — standard and special editions.
- `research-brief-template.md` — research skeleton.

## Research Tools

- `mcp-client.js` — headless Chrome MCP client for fetching paywalled/JS-rendered sources.
- Chrome MCP tools: `navigate_page`, `take_snapshot`, `evaluate_script`, `get_web_content`.

## Published Issues

- `issues/2026-03/output/SIGNAL_March_2026.md` — Issue #1
- `issues/2026-04/output/SIGNAL_April_2026.md` — Issue #2
- `issues/2026-05/output/SIGNAL_May_2026.md` — Issue #3
