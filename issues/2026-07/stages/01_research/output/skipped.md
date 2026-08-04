# Skipped Sources / Rejected Signals — July 2026

## Rejected as duplicates (confirmed by grepping published/drafted issues before including)

- **Kotlin's Koog reaches 1.0.** Already the lead Kotlin story in [Issue #3, May 2026](../../../2026-05/output/SIGNAL_May_2026.md) ("JetBrains ships Koog 1.0" at KotlinConf, featured in Today bullets, In the Know, and References). The framework's actual 1.0 announcement was May 2026 (KotlinConf keynote); anything reading "Koog 1.0" as a July story is working from a stale/misdated source.
- **Apache Kafka KIP-1150 / diskless topics.** Was the flagship Trenches story in [Issue #1, March 2026](../../../2026-03/output/SIGNAL_March_2026.md) (KIP-1150 approval, WarpStream comparison, "Scalac angle" already written). No new July-specific implementation movement found this pass — still "approved March 2026, production readiness unlikely before 2027." Skip unless a genuine new development (e.g. a merged sub-KIP, a production deployment) surfaces in a future pass.

## Rejected as explainer/tutorial content (no production-incident or breaking-change angle)

- ByteByteGo: "MCP vs A2A vs ACP: How AI Agents Actually Talk to Each Other," "Best Practices for Building AI Agents That Work in Production," "How ChatGPT Optimizes its Agent Loop" — real content, but explainer-shaped, not incident-driven. Per `sources.md` skip criteria.
- ByteByteGo: "A Guide to Multi-Tenancy," "How NVIDIA Builds Open Models," "Why DoorDash, Instacart, and Uber Eats Integrated LLMs Into Search," "Inside Roblox's Bet on World Models," "AI Customer Support at Scale" — off-theme for a JVM/distributed-systems audience or tutorial-shaped.

## Rejected as off-theme for SIGNAL (real, but belongs elsewhere)

- Pragmatic Engineer: "How building software is changing at Anthropic" (Jul 28) — engineering-culture piece, not JVM/distributed-systems specific.
- Pragmatic Engineer: "The Pulse: What can we learn from Bun's rapid Rust rewrite with AI?" (Jul 9) — interesting (Rust rewrite via AI tooling) but off-theme; better fit for a general engineering-practices piece.
- Pragmatic Engineer: "The Pulse: Quitting Spotify Podcasts over reliability," "Pushing software engineering limits with 'napkin math'," "Context engineering with Dex Horthy," "What is 'loop engineering?'," "Tech jobs market in 2026 part 3," "How Kent Beck shapes the software engineering industry," "The Pragmatic Engineer AMA" — reviewed, none carry a JVM/distributed-systems architecture angle strong enough for this issue.

## Rejected as minor/routine (no architectural impact)

- This Week in Scala, all four July issues: Sage 0.2.0 (Redis/Valkey client), Hearth 0.4.0, muntabot 1.0.0, tapir-cloudflare-worker, Jar Jar Abrams 1.17.0 + sbt-assembly 2.4.0, declinio, h4sbl, Uni ("Refined for Scala 3"), vibe-types, Scalapptainer, dbos4s (a thin Scala wrapper over DBOS's Java library — noted for interest given the Debate topic, but not signal-worthy on its own), Kyo v1.0.0-RC5, Scala.js 1.22.0, Mill 1.2.0-RC1.
- WildFly 41 GA, Open Liberty 26.0.0.7, Quarkus 3.37, Payara Server 7.2.0, TornadoVM 5.1.0, GPULlama3.java 1.0.0, Flyway 13.0.0, Micronaut 5.1.0 — routine framework point releases; real but not headline-worthy individually. Candidates for a one-line In the Know mention if space allows, not full Signal items.
- Oracle's July 21 Critical Patch Update across Java 8-26 — routine security patching, no migration story.

## Real, relevant, but wrong month or already-superseded

- **Definity embeds AI agents inside Spark pipelines** (VentureBeat, Kerner) — genuinely excellent "AI meets distributed systems" story (JVM agent inside the Spark/DBT execution layer, real customer metrics from Nexxen). **Dated April 29, 2026** — confirmed via grep not to have been covered in Issue #2 (April) or since, so not a duplicate, just outside July's window. Flagged in `candidate-signals.md` for a human recency-vs-relevance call rather than silently dropped.
- **Apache Spark multi-agent RL self-tuning** (InfoQ) — dated January 30, 2026. Interesting technique (hybrid RL + AQE, up to 69% faster on skewed groupBy) but stale for July; not checked against earlier issues since it's clearly out of any recent window.
- **Kai Waehner's "Kafka as event broker for Agentic AI (A2A + MCP)" writing** — real and well-regarded (Confluent), but his cited pieces are dated 2025-05 and 2026-04; no July-specific update found. Good evergreen Top Resources candidate, not a July Signal.
- **"Ox for Scala" direct-style effects, SoftwareMill** (X, @baldram) — Apr 26, 2026, too old for July.
- **"Orca" (Adam Warski / SoftwareMill, deterministic AI-driven dev flow scripts)** — found on X (May 31, 2026), too old for July. **Do not confuse with "Orca (VirtusLab)"**, a different, unrelated project already dropped in June's brief as a competitor product — this SoftwareMill one is a different tool with the same name and is not a competitor issue, just a stale date.

## Unverified — parked, not included

- **Project Detroit** (OpenJDK effort to ease Java/Python/JS interop) — surfaced only via secondary WebSearch summaries, never traced to a primary openjdk.org source. Do not use until verified.
- **QuePaxa's original paper** (SOSP 2023, Tennage & Băsescu et al.) — real, referenced by multiple sources discussing Meerkat, but exact arXiv/ACM link not yet located. Needs a direct lookup before citing as Top Resources.
- **GitHub "All-Stars" from JVM Weekly** (BossConsole, libargus.cc, JAIPilot-CLI) and other repo candidates (KotlinLLM, GPULlama3.java) — interesting but star counts/production traction not verified this pass; deferred to `02_select` for a quick check rather than committed now.

## Verified against a late tip-off, rejected on date or evidence

These came in as suggested July stories near the end of research. Each was checked against a primary source; four did not survive.

- **ScarfBench** (IBM Research benchmark for agentic Java framework migration: Spring ↔ Jakarta EE ↔ Quarkus). **The numbers are real and excellent** — 34 applications, 102 variants, ~151K LOC, 204 directed migration tasks, best agent scoring only 15.3% test pass on focused-layer and 12.2% on whole-application migrations, with exactly 1 of 204 tasks reaching full behavioural equivalence. Confirmed on [arXiv](https://arxiv.org/abs/2605.06754), [GitHub](https://github.com/scarfbench/benchmark), [IBM's announcement](https://www.ibm.com/new/announcements/scarfbench-a-public-benchmark-for-java-framework-migration), and [HuggingFace](https://huggingface.co/blog/ibm-research/scarfbench). **But the dates do not work:** benchmark introduced March 2026, arXiv paper May, blog posts June 30. No July distribution wave could be found. Freshness tag: `BACKGROUND_ONLY`. Thematically this is close to ideal for Scalac (enterprise JVM modernization plus honest evidence that agents generate code but do not preserve behaviour) — **worth its own scalac.io article or a future issue's Trenches, not a July Signal.**
- **Scala 3.3.8 LTS as a July release** — real release, wrong month: [shipped June 10, 2026](https://www.scala-lang.org/news/3.3.8/). Exactly the publication-date-vs-event-date trap `fact-check-rules.md` now covers.
- **"Nine new KIPs in July" and "configurable segment interval for Kafka Streams"** — could not be confirmed against the KIP index or Red Hat's digest. The July 8 KIP freeze and the September release slip *were* confirmed; these two specifics were not. Dropped rather than hedged.
- **Kafka CVE-2026-33557 (CVSS 9.1, OAUTHBEARER JWT signature bypass) and CVE-2026-35554 (producer buffer-pool race, silent misrouting to wrong topics)** — both genuinely severe and squarely on-topic, both published April 2026, neither with any confirmed real-world exploitation. `BACKGROUND_ONLY`. Grepped past issues: never covered, so available for a future security-themed issue.

## Reviewed from newer sources (Get Kafka-Nated, Data Engineering Digest, Kai Waehner), not used

- **Databricks raises $188B valuation** — real, dated July 2026, but pure business/funding news with no architecture angle; off-theme for SIGNAL.
- **Apache Ossie (semantic layer standardization)** — real Apache Incubator acceptance, interesting governance story, but a BI/analytics-metrics-layer topic rather than JVM/distributed-systems core; parked as a possible future item if the theme ever fits.
- **Trino as a data-warehouse alternative** — real community discussion, but a "roundup of tradeoffs" piece without a specific production incident; thin for this issue.
- **Meta's DEmate (AI-assisted data engineering)** — genuinely good AI+data-engineering story (3,500 weekly users, 80% code-acceptance) but Meta-specific and somewhat off the JVM/Scala/distributed-systems core; candidate for In the Know if space allows, not a lead item.
- **GKN Dispatches fireside chat (HelloFresh/OSO CTOs, Current London)** — real and on-theme (Kafka ops at scale) but video-only; WebFetch couldn't retrieve a transcript. Noted for awareness, not usable as a sourced quote without watching/transcribing it.
- **Kai Waehner: "When to Use AMQP, JMS, Kafka, or MQTT"** and **"Kafka vs Flink vs Spark: Do You Really Need Real-Time?"** — real July posts, not read in full this pass; flagged in case `02_select` wants a Top Resources architecture-reference pick.

## Not checked this session (access gaps, not editorial rejections)

- **r/apachekafka, r/dataengineering** — no working direct-Reddit access this session (`agent-reach` Reddit backend is off; WebFetch cannot reach reddit.com directly). If either community had a real July architecture debate or postmortem, this pass didn't catch it.
- ~~X/Twitter~~ — **Resolved mid-session**: OpenCLI browser extension connected, X search now works (`opencli twitter search/thread`). Found strong real engagement for the Meerkat/QuePaxa item (Cloudflare's own tweet + @arpit_bhayani's explainer thread — see `candidate-signals.md`). Searched specifically for JDK-8377715 and the DBOS/Postgres-vs-Temporal debate: **nothing relevant came back for either** — not a gap in access, just no real X discussion of those two specific stories yet.

## Event announcements

- None surfaced this pass requiring a Scalendar flag (no Devoxx/JavaOne/MCP Dev Summit-type items found in the July sweep).
