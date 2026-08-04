# Issue Routing

## Inputs

- `stages/00_brief/output/brief.md` — issue brief.
- `../../_config/` — global newsletter structure, voice, sources, fact-check rules.

## Stage Sequence

Run in order. Do not skip stages. Human review at each boundary.

1. `00_brief` — define month, issue number, candidate themes.
2. `01_research` — check required sources, fill research brief.
3. `02_select` — choose Debate, Trenches, 3 Signals, In the Know, Top Resources.
4. `03_draft` — write full newsletter.
5. `04_review` — fact-check, tone-check, link-check, slop removal.
6. `05_publish` — final markdown with frontmatter and images.
7. `06_post_publish` — social snippets and follow-up tracking.

## Decision Rules

- If brief is missing or incomplete: stay at `00_brief`.
- If research is thin or sources are weak: return to `01_research`.
- If selection duplicates stories or lacks controversy: revise at `02_select`.
- If review finds major issues: return to `03_draft`.
- If review finds minor issues: fix in `04_review` output.
