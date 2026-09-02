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

## Research routing

- Use `agent-reach` for every external lookup, URL and platform query.
- If its reader cannot retrieve a public page because of rendering or a simple bot
  block, use Scrapling as a fallback. Never use it to bypass authentication,
  paywalls, CAPTCHA challenges or access controls.
- Use `last30days` as a small discovery pass after the source sweep: Scala/JVM,
  Kafka/distributed systems, agentic AI in production, and one timely combined
  query. Treat social output as leads, then verify selected claims against primary
  sources.
- Give every candidate a freshness tag: `NEW_THIS_MONTH`, `MATERIAL_UPDATE` or
  `BACKGROUND_ONLY`. Only the first two can lead Debate, Trenches or Signal Over
  Noise.

## Illustration prompts

In `03_draft`, create `output/images.md` with prompts for Architecture Debate and
Notes from the Trenches. Add a cover only when one idea unifies the issue. Match
the existing Scalac diagram-comic style: warm off-white background, rough black
linework, black sticky figures, red as the only accent and short hand-lettered text
when it clarifies the lesson. The image explains one system relationship, failure
mode or decision at a glance. Exclude vendor logos, gradients, photorealism, dense
dashboards and generic robots.
