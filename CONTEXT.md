# SIGNAL Newsletter Generator — Workspace Routing

For human instructions see `README.md`.

## Available Issues

- `issues/2026-03/` — Issue #1, March 2026.
- `issues/2026-04/` — Issue #2, April 2026.
- `issues/2026-05/` — Issue #3, May 2026.

## How to Start a New Issue

1. Copy `template/` to `issues/YYYY-MM/`.
2. Write `stages/00_brief/output/brief.md`.
3. Move to `01_research`.

## Stage Sequence

Run in order. Do not skip stages. Human review at each boundary.

1. `00_brief` — define month, issue number, candidate themes.
2. `01_research` — check required sources, fill research brief.
3. `02_select` — choose Debate, Trenches, 3 Signals, In the Know, Top Resources.
4. `03_draft` — write full newsletter.
5. `04_review` — fact-check, tone-check, link-check, slop removal.
6. `05_publish` — final markdown with frontmatter and images.
7. `06_post_publish` — social snippets and follow-up tracking.

## Global Reference (Layer 3)

Load from `_config/` when a stage needs it:

- `newsletter-structure.md` — section definitions and selection criteria.
- `voice.md` — The Code format, banned words, link and metric rules.
- `sources.md` — required and secondary sources, fetch methods.
- `fact-check-rules.md` — verification rules from past issues.
- `newsletter-types.md` — standard and special edition formats.
- `research-brief-template.md` — research brief skeleton.
