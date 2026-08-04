# SIGNAL July 2026 (Issue #5) — Selection

Produced under the `02_select` deliverable contract: candidate register with scores, recommended theme, proposed lineup, rejects with reasons, tagged sources, and one editorial question.

Rubric: Freshness / Relevance / Evidence / Stakes / Tension / Originality, each 0-5, 30 max. Threshold ~20. Hard overrides: a low-evidence item can never headline, and a `BACKGROUND_ONLY` item can never be Debate, Trenches, or a Signal.

## 1. Candidate register

| # | Candidate | Track | Fresh | Score | Decision |
|---|-----------|-------|-------|-------|----------|
| 1 | Postgres-as-orchestrator vs Temporal | workflow | `MATERIAL_UPDATE` | 4/5/5/5/5/4 = **28** | **SELECT** — Debate |
| 2 | Kafka KIP-1360 synchronous mirroring, zero-RPO | kafka | `NEW_THIS_MONTH` | 5/5/4/5/5/5 = **29** | **SELECT** — Signal 3 |
| 3 | Cloudflare Meerkat / QuePaxa | distributed | `NEW_THIS_MONTH` | 5/5/4/3/5/4 = **26** | **SELECT** — Signal 2 |
| 4 | JEP 401 merges + JEP 539 targeted | jvm | `NEW_THIS_MONTH` | 5/5/5/4/3/3 = **25** | **SELECT** — Signal 1 |
| 5 | Batch→micro-batch streaming migration | data | `MATERIAL_UPDATE` | 4/4/5/4/3/4 = **24** | **SELECT** — Trenches |
| 6 | Kafka Share Groups production edge cases (Vanlightly) | kafka | `NEW_THIS_MONTH` | 5/5/4/3/4/4 = **25** | **SELECT** — In the Know (see note) |
| 7 | Scala 3 separation checker | scala | `MATERIAL_UPDATE` | 4/5/4/3/2/4 = **22** | **SELECT** — In the Know |
| 8 | Chrome DevTools MCP v1.5.0 / v1.6.0 | agentic | `NEW_THIS_MONTH` | 5/3/5/2/2/4 = **21** | **SELECT** — In the Know |
| 9 | Databricks LTAP / "lakebase" | data | `NEW_THIS_MONTH` | 5/3/4/3/2/4 = **21** | **CONTEXT** — one line in Debate |
| 10 | Project Leyden AOT Cache | jvm | `NEW_THIS_MONTH` | 4/4/4/3/2/3 = **20** | **SELECT** — In the Know |
| 11 | sbt 2.0 final GA | scala | `MATERIAL_UPDATE` | 4/4/5/3/1/2 = **19** | **SELECT** — In the Know |
| 12 | Prefect acquires Dagster | workflow | `NEW_THIS_MONTH` | 5/3/4/3/1/3 = **19** | **CONTEXT** — one line in Debate |
| 13 | GPULlama3.java | jvm+ai | `MATERIAL_UPDATE` | 3/4/3/2/1/5 = **18** | **SELECT** — Top Resources repo |
| 14 | Vincent Vauban, Valhalla + quantized weights | jvm+ai | `NEW_THIS_MONTH` | rubric n/a (voice, not story) | **SELECT** — Community Voice |
| 15 | ScarfBench, agentic Java migration benchmark | agentic+jvm | `BACKGROUND_ONLY` | 0/5/5/5/5/5 = **25** | **REJECT** this issue — freshness override |
| 16 | OpenAI agent → Hugging Face intrusion | agentic | `NEW_THIS_MONTH` | 5/3/5/4/5/3 = **25** | **REJECT** — human decision, off-theme |
| 17 | Kafka CVE-2026-33557 / -35554 | kafka | `BACKGROUND_ONLY` | 0/5/5/4/3/4 = **21** | **REJECT** this issue — April CVEs |
| 18 | Chimp / sttp-ai MCP for Scala | scala+agentic | `NEW_THIS_MONTH` | n/a | **REJECT** — SoftwareMill, competitor |
| 19 | Definity, agents inside Spark pipelines | data+agentic | `BACKGROUND_ONLY` | 0/5/4/4/3/5 = **21** | **REJECT** this issue — April story |
| 20 | Kotlin 2.4.10 | kotlin | `NEW_THIS_MONTH` | 5/3/5/1/1/1 = **16** | **REJECT** — below threshold, patch release |

**Note on #6:** Share Groups edge cases scored 25, which is Signal-worthy. It lost the slot to KIP-1360 on issue balance, not quality — two Kafka items out of three Signals would skew the issue. If the human prefers it as Signal 3, KIP-1360 swaps down to In the Know cleanly.

**Note on #15:** ScarfBench is the clearest demonstration of why the freshness override exists. It scores 25 on everything except freshness, it is arguably the single most on-brand topic in the whole register (enterprise JVM modernization plus hard evidence that agents generate code without preserving behaviour: 15.3% test pass, 1 of 204 tasks behaviourally equivalent), and it still cannot run as July news because it shipped in March. **Recommend it as a standalone scalac.io article or next issue's Trenches** rather than burying it here.

## 2. Recommended theme

The infrastructure layer everyone treated as settled is being renegotiated, all in one month: what an object *is* on the JVM (JEP 401) and when it may legally exist (JEP 539), whether consensus needs a leader and timeouts at all (QuePaxa), what durability costs in latency across regions (KIP-1360), and whether workflow orchestration belongs in a dedicated engine or in the database you already run (the Debate).

Not "AI is eating everything." The narrower and more defensible line: **the primitives are moving, and each move is a priced trade-off rather than a free upgrade.**

## 3. Proposed lineup

**Intro** — theme in 2-3 sentences, hook on the Debate.

**Today** — see `today-bullets.md`.

**The Architecture Debate: Postgres-as-orchestrator vs a dedicated engine.** Side A: DBOS's argument, checkpoint workflow state in the same Postgres transaction as the work, run as a library, delete a service from the diagram. Side B: the exactly-once guarantee only covers the database write (an external API call that crashes before its checkpoint commits still fires twice), workflow load competes with app load at scale, and Conductor is not open source. Both sides have real practitioners on the record. Market context in one sentence: Prefect acquired Dagster, and Databricks shipped LTAP to push OLTP/OLAP sharing into the storage layer, so pressure is arriving from both directions at once. **Scalac angle:** the deciding question is whether workflow load scales independently of application load; and either way every outbound call still needs its own idempotency key.

**Notes from the Trenches: the pipeline was late, not slow.** Delta index pipeline, several million documents, tens of GB, new data every 5-7 minutes, full rebuild 2-3 hours. The problem was scheduling cadence, not processing throughput. Fix: Spark Structured Streaming on a 30-second trigger, watermark comparison against the latest partition, freshness-first partition skipping, scheduled 24-hour restarts with an external watchdog instead of completion markers. Result: end-to-end latency down ~50%, worst-case freshness from ~10 minutes to 30 seconds. **Scalac angle:** diagnose whether your latency is processing or scheduling before you rewrite anything to per-record semantics.

**Signal 1: the JVM renegotiates two fundamentals at once.** JEP 401 (Value Classes and Objects) merged to OpenJDK mainline after roughly a decade and ~197K lines of code; JEP 539 (Strict Field Initialization) moved Candidate → Proposed to Target → Targeted for JDK 28 across the same month. One removes identity from the object model, the other removes the window where an object exists in a partially-initialized state. Boundary: both preview, both aimed at JDK 28 (March 2027), and Goetz explicitly discourages expecting JEP 401 to exit preview in JDK 29.

**Signal 2: consensus without the tyranny of timeouts.** Cloudflare's Meerkat, built on QuePaxa: any replica can drive consensus, a leader is an optimization rather than a requirement, progress never halts on a timeout. Boundary, stated plainly: not in production, proofs of concept up to 50 replicas, and Cloudflare did not invent QuePaxa (SOSP 2023). Include the pushback, because it is the interesting part: HN readers argued the honest comparison is other Paxos-class leaderless protocols rather than Raft, and flagged a real concern that the retry-and-abandon pattern trades bounded timeout latency for unbounded tail latency.

**Signal 3: Kafka wants to sell you RPO=0.** KIP-1360 proposes synchronous mirroring on top of KIP-1279: a record counts as received only once all ISR on all mirror clusters have it. That buys zero-RPO disaster recovery and charges for it in write latency. Boundary: a proposal built on a proposal, nothing shipped; 4.4.0 KIP freeze was July 8 and the release slipped to September.

**Community Voice** — Vincent Vauban's JEP 401 walkthrough on LinkedIn, specifically the `value record QuantizedWeight(byte value)` example. It is the one community read that connects value types to AI workloads on their own terms rather than ours.

**In the Know** — Share Groups production edge cases (Vanlightly); Chrome DevTools MCP v1.5.0 and v1.6.0; Scala 3's separation checker; sbt 2.0 final GA; Project Leyden AOT Cache tightening agent rules while cutting Quarkus+Postgres startup readiness from 1022.4ms to 380.3ms.

**Top Resources** — Repo: [GPULlama3.java](https://github.com/beehive-lab/GPULlama3.java), GPU-accelerated Llama3 inference in pure Java via TornadoVM, 269 stars and active. Article: [Pragmatic Engineer on formal methods with Hillel Wayne](https://newsletter.pragmaticengineer.com/p/formal-methods-with-hillel-wayne), including the AWS bug whose shortest error trace was 35 steps. Paper: [QuePaxa: Escaping the tyranny of timeouts in consensus](https://dl.acm.org/doi/10.1145/3600006.3613150), SOSP 2023, Tennage, Basescu et al., open access [here](https://bford.info/pub/os/quepaxa/).

## 4. Rejects, one line each

- **ScarfBench** — March benchmark, June blog posts, no July event. Best candidate in the register on every axis except the one that disqualifies it. Recommend as its own article.
- **OpenAI → Hugging Face agent intrusion** — highest engagement found anywhere in this research (405 points, 224 comments), rejected by human decision as off-theme for a JVM/distributed-systems issue.
- **Kafka CVE-2026-33557 (CVSS 9.1 auth bypass) and CVE-2026-35554** — April disclosures, no confirmed exploitation. Never covered in a past issue, so available for a future security-themed issue.
- **Definity, agents inside Spark pipelines** — April 29 story. Strong material, wrong month.
- **Chimp / sttp-ai** — SoftwareMill is a named competitor in `scalac-tone-of-voice.md`. Same treatment VirtusLab got in June.
- **Kotlin Koog 1.0** — already the lead Kotlin story in Issue #3 (May).
- **Kafka KIP-1150 / diskless** — already the flagship Trenches story in Issue #1 (March), no new July movement.
- **Scala 3.3.8 LTS** — June 10 release, arrived as a July claim.
- **"Nine new July KIPs" and configurable Streams segment interval** — could not be confirmed against the KIP index or Red Hat's digest.
- **Kotlin 2.4.10, plus WildFly 41 / Payara 7.2.0 / Quarkus 3.37 / GraalVM 25.2 and the This Week in Scala library churn** — routine releases, below threshold.
- **Databricks $188B valuation, Apache Ossie, Trino-as-warehouse, Meta DEmate** — real July items, off-core for a JVM/distributed-systems audience.

## 5. Sources, tagged

**Primary (P0)**
- [JEP 401](https://openjdk.org/jeps/401), [JEP 539](https://openjdk.org/jeps/539), [openjdk/jdk PR #31120](https://github.com/openjdk/jdk/pull/31120), [jdk-dev candidate announcement](https://mail.openjdk.org/archives/list/jdk-dev@openjdk.org/thread/FGQVFIUNYX4GVJTABNLPFBLBLKDPM55H/)
- [Cloudflare Meerkat announcement](https://blog.cloudflare.com/meerkat-introduction/), [QuePaxa paper, ACM](https://dl.acm.org/doi/10.1145/3600006.3613150) / [open access](https://bford.info/pub/os/quepaxa/)
- [KIP-1279 Cluster Mirroring](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring) and the KIP-1360 discussion
- [Chrome DevTools MCP releases](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases), [GPULlama3.java](https://github.com/beehive-lab/GPULlama3.java)
- [Scala separation checking docs](https://www.scala-lang.org/api/current/docs/experimental/capture-checking/separation-checking.html), [System Capybara paper](https://arxiv.org/abs/2607.09383)
- [Dagster's own acquisition announcement](https://dagster.io/blog/prefect-is-acquiring-dagster)

**Verification (P1)**
- [InfoQ: Compiling Workflows into Databases](https://www.infoq.com/presentations/dbos/), [InfoQ: micro-batch streaming case study](https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/), [InfoQ Architects' Newsletter #108](https://assets.infoq.com/newsletter/architect/en/newsletter_sample/108Architects_NL_July-2026.html)
- [JVM Weekly vol. 186](https://www.jvm-weekly.com/p/the-rest-of-the-story-july-edition), InfoQ Java News Roundups (Jun 29, Jul 20, Jul 27)
- [Get Kafka-Nated, July 2026](https://getkafkanated.substack.com/p/get-kafka-nated-espresso-july-2026), [Red Hat Kafka Monthly Digest](https://developers.redhat.com/blog/2026/07/01/kafka-monthly-digest-june-2026)
- [The Register on Valhalla](https://www.theregister.com/devops/2026/06/15/javas-project-valhalla-finally-lands-a-preview-in-jdk-28/5255557), [dev.to on Postgres durable workflows](https://dev.to/contrite42/durable-workflows-on-postgres-what-you-dont-need-temporal-actually-buys-you-3o0f), [BigGo on DBOS exactly-once skepticism](https://finance.biggo.com/news/202510030712_DBOS_Developer_Skepticism_Exactly_Once_Processing)
- [Pragmatic Engineer, Hillel Wayne](https://newsletter.pragmaticengineer.com/p/formal-methods-with-hillel-wayne) (free preview only, per §8)

**Community (P2)**
- [HN: JEP 401 merged](https://news.ycombinator.com/item?id=49119063), [HN: Meerkat](https://news.ycombinator.com/item?id=48831565), [HN: JEP 539 preview](https://news.ycombinator.com/item?id=48765830), [HN: Postgres durable workflows](https://news.ycombinator.com/item?id=44840693)
- [Cloudflare on X](https://x.com/i/status/2074842199104135561) (458 likes, 225K views), [@arpit_bhayani QuePaxa thread](https://x.com/arpit_bhayani/status/2075218756499071037) (346 likes)
- [Vincent Vauban on LinkedIn](https://www.linkedin.com/posts/vvauban_jep-401-value-classes-and-objects-preview-activity-7483158484075655168-Zp3Q), [Cloudflare on LinkedIn](https://www.linkedin.com/posts/cloudflare_introducing-meerkat-an-experiment-in-global-activity-7480607893894127616-9nVb)

## 6. Editorial question (one)

**Signal 3 slot.** You approved GPULlama3.java as Signal 3 earlier, replacing Project Leyden. Verification then surfaced KIP-1360, which fits the theme far better: it is a priced architectural trade-off (RPO=0 against write latency), where GPULlama3.java is an impressive artefact with no trade-off and no July event behind it.

This lineup therefore moves GPULlama3.java to Top Resources as the repo to watch, which also solves the gap left when Chimp was disqualified as a competitor. Net effect: you keep the item, it stops carrying a Signal slot it does not quite earn, and the issue gains thematic coherence.

Say the word if you'd rather keep GPULlama3.java in Signal 3 and drop KIP-1360 to In the Know.
