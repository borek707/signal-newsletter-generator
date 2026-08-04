# Issue Routing — July 2026 (Issue #5)

## Current state (2026-08-04)

`00_brief`, `01_research`, and `02_select` are complete. **Waiting on human approval of the lineup before `03_draft` starts.**

Theme: the infrastructure layer everyone treated as settled is being renegotiated in one month — what an object is on the JVM (JEP 401) and when it may legally exist (JEP 539), whether consensus needs a leader and timeouts (QuePaxa), what durability costs in write latency across regions (KIP-1360), and whether orchestration belongs in a dedicated engine or the database you already run (the Debate).

**One open editorial question**, in `stages/02_select/output/selection.md` §6: Signal 3 is currently proposed as Kafka KIP-1360, with GPULlama3.java moved down to Top Resources. Piotr had earlier approved GPULlama3.java for the Signal 3 slot. Resolve before drafting.

## How this issue's research was run

Worth reading before the next issue, because the process changed mid-flight and `_config/` now reflects it.

1. Started wrong: a generic `/last30days` pass on "JVM and Distributed Systems" before realising this workspace and its pipeline existed. Not wasted (it surfaced Cloudflare Meerkat and the DBOS/Postgres thread, both of which survived into the issue) but it is triage, not research. `_config/sources.md` now documents it as exactly that.
2. Swept all five required sources properly via direct fetch rather than WebSearch: JVM Weekly vol. 186 (confirmed the newsletter is now monthly despite the name, so one July issue is full coverage), all four July This Week in Scala issues, InfoQ Architects' Newsletter #108 (issue number is derivable: 91 + months since Feb 2025), the ByteByteGo July archive, and the Pragmatic Engineer July archive.
3. Added four sources not previously in `sources.md`, all now documented there: Get Kafka-Nated, Data Engineering Digest, Kai Waehner's blog, Scala Times. Scala Times carries a competitor warning — it is published by SoftwareMill.
4. Set up X access mid-session: OpenCLI browser extension connected, so `opencli twitter search/thread` works against a logged-in session. Found real engagement for Meerkat (Cloudflare's own post at 458 likes / 225K views; @arpit_bhayani's explainer thread at 346 likes) and confirmed the *absence* of X discussion for JDK-8377715 and the DBOS debate. LinkedIn covered via Exa `site:linkedin.com`, which found Cloudflare's post plus Vincent Vauban's JEP 401 walkthrough.
5. Reddit was never reachable this session. r/apachekafka and r/dataengineering remain unchecked — the one real gap against `sources.md`.

## What the verification pass killed

The part worth internalising. Six candidates that looked like July news were not:

- **Kotlin Koog 1.0** — already the lead Kotlin story in Issue #3 (May). Caught by grepping past issues, not by memory.
- **Kafka KIP-1150 / diskless** — already the flagship Trenches story in Issue #1 (March).
- **ScarfBench** — real and excellent (34 apps, 204 tasks, best agent 15.3% test pass, 1/204 behaviourally equivalent), but a March benchmark with June blog posts. Scored 25/30 on everything except freshness. Recommended as its own scalac.io article instead.
- **Scala 3.3.8 LTS** — arrived as a July claim, shipped June 10.
- **Definity's Spark-embedded agents** — strong story, dated April 29.
- **Kafka CVE-2026-33557 / -35554** — severe and on-topic, both April, no confirmed exploitation.

Two rejected on other grounds: **Chimp / sttp-ai** (SoftwareMill, a named competitor — and it was initially recommended because only the one competitor flagged in June's brief got checked, instead of the full list in `scalac-tone-of-voice.md`), and the **OpenAI → Hugging Face agent intrusion** (highest engagement found anywhere in the pass at 405 HN points / 224 comments, rejected by Piotr as off-theme).

Also killed as a Debate candidate: **Prefect acquiring Dagster** looked like drama, then verification showed one founder leaving, ~40 staff joining, an explicit open-source commitment, and no opposing technical camp. Demoted to a context sentence.

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
