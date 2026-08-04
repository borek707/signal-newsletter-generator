## Inputs

- `../00_brief/output/brief.md`
- `../../_config/sources.md` — required and secondary sources.
- `../../_config/newsletter-structure.md` — section definitions.
- `../../_config/research-brief-template.md` — skeleton.

## Process

1. Check every required source listed in `sources.md`.
2. Use Chrome MCP for Substack, Medium, and JS-rendered pages.
3. Extract candidate signals: migrations, postmortems, debates, cost reductions, breaking changes, AI integration.
4. Fill `research-brief-template.md` sections §1–§11.
5. Propose at least one Debate candidate, one Trenches candidate, and at least 5 Signal candidates.
6. List skipped sources and rejected signals with reasons.
7. Flag any claims needing fact-check verification.

## Outputs

- `output/research-brief.md` — full research brief.
- `output/candidate-debate.md` — extracted debate candidate.
- `output/candidate-trenches.md` — extracted trenches candidate.
- `output/candidate-signals.md` — extracted signal candidates.
- `output/skipped.md` — rejected signals and why.

## Review gate

Human checks source coverage and candidate quality before selection.
