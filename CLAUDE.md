# SIGNAL Newsletter Generator

This is an ICM (Interpretable Context Methodology) workspace for producing the monthly **SIGNAL** newsletter for Scalac.

## What this workspace is

A folder-based newsletter production system. Each issue is a separate ICM workspace under `issues/YYYY-MM/`. The `template/` folder holds the reusable issue pipeline. The `_config/` folder holds stable reference material: newsletter structure, voice, sources, fact-check rules.

The original skill reference remains in `SKILL.md` at the root.

## Target

- **Publication:** SIGNAL newsletter (email + blog).
- **Reader:** CTO / VP Engineering / Chief Architect.
- **Goal:** monthly filter for what matters in distributed systems, not news aggregation.
- **Voice:** independent engineering perspective, short and punchy, metric-driven.

## How to use it

1. To start a new issue, copy `template/` into `issues/YYYY-MM/`.
2. Fill the brief in `stages/00_brief/output/brief.md`.
3. Run stages in order: `01_research` → `02_select` → `03_draft` → `04_review` → `05_publish` → `06_post_publish`.
4. At each stage, read the stage `CONTEXT.md`, load the required inputs, and write the required outputs.
5. Human reviews output at each stage before proceeding.

## Folder map

- `_config/` — Layer 3 reference files (structure, voice, sources, fact-check rules).
- `template/` — Layer 0–2 template for any new issue.
- `issues/` — Layer 0–2 instances, one folder per issue.
- `signals/` — optional raw signal snippets between issues.
- `SKILL.md` — original skill reference.

## Rules

- One stage, one job.
- Plain markdown files only.
- Every output is an edit surface.
- Configure the factory (`_config/`), not the product (`output/`).
- No AI-slop language. No throat-clearers, emphasis crutches, or business jargon.
