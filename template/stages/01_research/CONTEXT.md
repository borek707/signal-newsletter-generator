## Inputs

- `../00_brief/output/brief.md`
- `../../_config/sources.md` — required and secondary sources.
- `../../_config/newsletter-structure.md` — section definitions.
- `../../_config/research-brief-template.md` — skeleton.

## Process

1. Check every required source listed in `sources.md` (this now includes the Supplementary Research Tools section — `/last30days` and `agent-reach` — not just the newsletter/blog list).
2. Use Chrome MCP (or WebFetch directly first — try it before assuming a Chrome MCP is needed) for Substack, Medium, and JS-rendered pages.
3. Run `/last30days` on 1-2 candidate topics early, as a triage signal for what's actually getting engagement (see `sources.md` § Supplementary Research Tools) — don't wait until the deep-dive to discover a topic is dead or alive.
4. Run `agent-reach doctor --json` once per session; if OpenCLI/X is connected, search X and LinkedIn (via Exa) for each strong candidate from steps 1-3 — real engagement numbers are strong evidence for or against a Debate/Trenches pick.
5. Extract candidate signals: migrations, postmortems, debates, cost reductions, breaking changes, AI integration.
6. Fill `research-brief-template.md` sections §1–§11.
7. Propose at least one Debate candidate, one Trenches candidate, and at least 5 Signal candidates.
8. List skipped sources and rejected signals with reasons.
9. Flag any claims needing fact-check verification.
10. **Competitor check:** before featuring any third-party tool/repo/article by name, cross-check it against the full competitor list in `scalac-tone-of-voice.md` (SoftwareMill, VirtusLab, Typelevel) — not just whichever competitor was flagged in a previous issue's brief. Grep past issues for the exact tool/company name before treating a find as "new" — several July candidates turned out to be duplicates of stories already used in earlier issues.

## Search strategy: five tracks, three query shapes each

Work the tracks in parallel rather than sweeping source-by-source. For each track run at least three searches, and treat the third as non-optional — it is the one that produces the tension the Debate and Trenches sections need.

Tracks:
1. **JVM semantics and runtime** — value objects, Valhalla, Loom, Panama, Leyden, GC, JIT, AOT, native interop, memory model.
2. **Scala / Kotlin / concurrency** — language design, compiler, effects, typed concurrency, build tooling, ecosystem migration.
3. **Kafka and data systems** — KIPs, KRaft, consumers, Streams, state stores, cross-cluster replication, Flink, event-driven patterns.
4. **Distributed correctness** — consensus, replication, transactions, formal methods, verification, public failure analyses.
5. **Agentic production systems** — tool use, durable state, queues, evaluation, MCP/A2A, observability, security, deployment.

Query shapes, per track:
- **Month-bounded:** the topic plus the issue's month and year.
- **Artefact-bounded:** the topic plus `JEP` / `KIP` / `RFC` / `release` / `benchmark` / `paper` / `postmortem`.
- **Conflict-bounded:** the topic plus `trade-off` / `limitation` / `fails` / `incident` / `regression` / `discussion` / `issue`. **Do not skip this one.** Capability news is easy to find and makes a boring issue; the constraint, the cost, and the argument are what the audience actually pays attention for.

Split queries into single entities and single hypotheses. One long multi-clause query returns worse results than three narrow ones. Do not assume version numbers or project names that earlier results did not produce.

## Outputs

- `output/research-brief.md` — full research brief.
- `output/candidate-debate.md` — extracted debate candidate.
- `output/candidate-trenches.md` — extracted trenches candidate.
- `output/candidate-signals.md` — extracted signal candidates.
- `output/skipped.md` — rejected signals and why.

## Review gate

Human checks source coverage and candidate quality before selection.
