# SIGNAL September 2026 — Research Brief (Issue #7)

Researched 2026-10-07. Window 1–30 Sep 2026; 1–7 Oct used only where it completes a September story. Five tracks worked in parallel; full evidence, verbatim quotes and URL logs live in `track-notes/track1…5-*.md`. This file is the summary register — when a number here and a number in a track note disagree, the track note wins and this file is wrong.

## §1 Issue Metadata

- **Issue number:** #7
- **Month / Year:** September 2026
- **Target publish date:** still open (brief §1: before Scala Days 12 Oct, or week of 19 Oct). Note: Kafka 4.4.0 RC4 vote closes 12 Oct, which changes one Signal either way.
- **Main theme or hook — research changed it.** The brief's "the upgrade is the incident" survives, but a sharper throughline came out of four tracks independently:

  **The safe path was the failure path.** A Kafka broker lost data on a *clean* shutdown (KAFKA-20979). NATS's flight-data link auto-recovered and was logged "recovered and stable" while corruption spread for 2.5 hours. Firebase's kill-switch mechanism — built to undo bad releases — shipped a bad flag to every iOS app at once. JDK 27 made compact object headers the *default* while Oracle's own regression ticket is still open. In each case the mechanism meant to protect you was where the damage travelled.

  Recommendation: use this as the spine. It covers JVM, Kafka and distributed correctness with P0 evidence, and it is not the #5 frame ("settled infrastructure renegotiated").

## §2 Source Coverage

| Source | Checked | Notable stories |
|--------|---------|-----------------|
| JVM Weekly | Yes (vol. 190–194) | JDK 27 GA; Arrays.fill on G1; Jev/TypeSafe; Scala 3.9 + Unsafe lazy vals. Author works at VirtusLab → discovery only. |
| This Week in Scala | Yes (7 Sep – 5 Oct) | Scala 3.9 LTS; sbt 2.1 milestones; Box Gradle monorepo; Pre-SIP `T ? E`; Odersky capabilities post |
| InfoQ Architects' Newsletter | Partial — landing page only (Oct items); InfoQ **Java roundups** 7/14/21/28 Sep read in full | JEP 544 status changes; LangChain4j 1.21 DecisionModel; Open Liberty G1 warning; JobRunr 9; Open Liberty MCP GA |
| ByteByteGo | Yes (feed + DoorDash/payments posts) | Both September agent posts are rewrites of older material (DoorDash 30 Jul; MPP March) → background |
| Pragmatic Engineer | Yes (feed, free previews only) | Firebase outage (paywalled → chased Google's own post-mortem); OpenAI software factory (no P0 sources) |
| Get Kafka-Nated | Yes | No September issue |
| Kafka primary (dev@/users@, Jira, KIP wiki, GitHub tags) | Yes — 520 dev@ messages for Sept via API | 4.4.0 slip; KAFKA-20979; KIP-1279 accepted; codec supply chain |
| r/scala | Partial — one thread via opencli; Reddit API blocked | "AI in Scala" (off-topic for Debate) |
| r/apachekafka / r/java | Via `/last30days` listing only (titles + dates) | Kafgres; Aiven KRaft; JEP 543 PTT |
| Hacker News | Yes — Algolia API, window 1788220800–1791417600 | Jev launch 1,989 pts; AWS me-south-1 530 pts; MCP debate 686/335 pts; TLA+ 246 pts |
| X / LinkedIn | **No** — agent-reach has no X credentials this session; LinkedIn not attempted | Only one X post used (Gergely Orosz on Firebase, via fxtwitter API) |
| `/last30days` | Yes, 1 run (`jdk-27-scala-3-9-jvm-upgrade-raw-v3.md`) | Ranked clusters were noise (Polymarket football); the raw item list surfaced the Kafka-on-Postgres and KRaft leads |

**Correction logged:** the coordinator's first agent prompts used a 2025 HN epoch. All tracks re-ran or date-checked; no 2025 item survives in this register.

## §3 Candidate Register

Scores: Freshness / Relevance / Evidence / Stakes / Tension / Originality. Full fields for every row are in the track note named in the ID.

| ID | Working title | Track | Freshness | Event date | Claim (one line) | Primary source | Score | Decision |
|----|---|---|---|---|---|---|---|---|
| T3-C1 | A clean shutdown could delete recent Kafka data | Kafka | MATERIAL_UPDATE (fixes merged 10 & 15 Sep) | 2026-09-15 | On 4.1.0 an un-fsynced time-index truncation reads as `timestamp=0` after a clean restart; retention deletes valid segments. Fixed in 4.3.2 / 4.4.0. | [KAFKA-20979](https://issues.apache.org/jira/browse/KAFKA-20979), PR #23316 | 4/5/5/5/3/5 = **27** | **SELECT — Trenches (recommended)** |
| T4-C1 | NATS: a ~1 ms race corrupted UK flight data; auto-recovery hid it | correctness | NEW_THIS_MONTH | 2026-09-08 | A preempted mid-write in squawk allocation corrupted NAS data; the link "recovered" at 10:02 and the failure surfaced at 12:32. 2,000+ flights hit. | [NATS preliminary report PDF](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf) | 5/5/5/5/3/4 = **27** | **SELECT — Trenches alternate / intro anchor** |
| T1-C1 | JDK 27 ships compact object headers by default with an open regression ticket | JVM | NEW_THIS_MONTH | 2026-09-15 | JDK-8386990 is Open (P4, fix "tbd"): crypto −1…−4%, ScalaKmeans −15…−20%, String micros to −50%; HotSpot engineers argue it in the ticket. | [JEP 534](https://openjdk.org/jeps/534), [JDK-8386990](https://bugs.openjdk.org/browse/JDK-8386990), [JDK-8392511](https://bugs.openjdk.org/browse/JDK-8392511) | 4/5/5/4/5/5 = **28** | **SELECT — Debate (recommended)** |
| T5-C1 | Typed decision models arrive on the JVM (LangChain4j `DecisionModel`, Jev, OpenAI Decisions) | agentic | NEW_THIS_MONTH | 15 Sep (Jev) / 29 Sep (PR merge, OpenAI) / 2 Oct (1.21.0) | LangChain4j 1.21.0 adds experimental `DecisionModel`; an independent eval finds Jev beats Qwen3.8-27B on 27/37 datasets but needs per-task thresholds. | [1.21.0 release](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0), [arXiv 2609.37647](https://arxiv.org/abs/2609.37647) | 5/5/4/4/4/4 = **26** | **SELECT — Debate alternate, or Signal** |
| T3-C2 | Kafka 4.4.0 slipped a month; PMC: "we don't have committed release dates" | Kafka | NEW_THIS_MONTH | RC0–RC3 failed 21 Aug–5 Oct; RC4 vote to 12 Oct | Ericsson planned CVE fixes around a release that has not shipped; 4.5.0 proposed for ~Mar 2027. KIP-909 DNS behaviour change is an upgrade note. | [users@ thread](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf), [RC4 vote](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222) | 5/5/5/4/4/4 = **27** | **SELECT — Signal** |
| T2-C1 | Scala 3.9 LTS: the Unsafe warning comes from a jar you never compiled | Scala | NEW_THIS_MONTH | 2026-09-03 | On JDK 27 GA, 3.0–3.7 lazy vals warn and run; they fail under `--sun-misc-unsafe-memory-access=deny`. Reproduced locally by the research agent. | [Scala 3.9 announcement](https://www.scala-lang.org/news/3.9/), [JEP 471](https://openjdk.org/jeps/471) | 5/5/5/4/3/4 = **26** | **SELECT — Signal (fold T2-C2 in)** |
| T2-C2 | Spark vs scala-reflect on the 3.8+ stdlib | Scala | MATERIAL_UPDATE | fixes merged 23 Aug, unreleased (Spark 4.3.0) | scala-reflect throws `FatalError: class Array does not have a member apply` on 3.9.0; released Spark initialises that universe. | [scala3#25896](https://github.com/scala/scala3/issues/25896), [SPARK-57548](https://issues.apache.org/jira/browse/SPARK-57548) | 3/4/5/4/4/5 = **25** | CONTEXT — inside T2-C1 |
| T5-C2 | Agent state and A2A trust are a new JVM attack surface | agentic | NEW_THIS_MONTH | 28 Aug–25 Sep | langchain4j-agentic state serializer allowed Jackson polymorphic deserialization (needs a gadget); a2a-java default task store did no read authorization (CVSS 7.5). | [GHSA-gmwr-7wmf-mrjm](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm), [a2a-java advisories](https://github.com/a2aproject/a2a-java/security/advisories) | 4/5/5/4/3/5 = **26** | **SELECT — Signal candidate** |
| T3-C4 | Kafka's codecs depend on unmaintained / single-maintainer libraries | Kafka | NEW_THIS_MONTH | 2026-09-29 | Three snappy-java CVEs can't be fixed by a bump (disputed); LZ4 rests on a one-person fork; KAFKA-21178 proposes disabling codecs on write. | [dev@ thread](https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8), [KAFKA-21178](https://issues.apache.org/jira/browse/KAFKA-21178) | 5/4/4/4/4/5 = **26** | CONTEXT — fold into T3-C2 or Today |
| T4-C2 | Firebase: a 2-line flag cleanup crashed iOS apps globally; dashboards stayed green | correctness | NEW_THIS_MONTH | 28 Sep PDT (post-mortem 2 Oct) | Kill-switch config is released globally; served 2 h 11 min; Google admits dashboards "remained green". | [Google post-mortem](https://firebase.blog/posts/2026/10/firebase-analytics-outage) | 5/4/5/4/4/3 = **25** | CONTEXT — Today or intro example |
| T4-C4 | AWS declares me-south-1 data unrecoverable | correctness | MATERIAL_UPDATE | 2026-09-15 | Damage "exceeded what our regional and multi-AZ services are designed to withstand". No service breakdown. | [AWS Health RSS](https://status.aws.amazon.com/rss/multipleservices-me-south-1.rss) | 4/5/4/5/4/3 = **25** | CONTEXT — Today; framing must stay technical (failure domains, residency vs DR), not geopolitical |
| T4-C3 | Telstra: a GPS card reset to 2006 and the NTP majority agreed | correctness | MATERIAL_UPDATE (report 2 Sep, outage 8 Jul) | 2026-09-02 | Peering loops plus an ad-hoc stratum-1 card let a wrong time win quorum. | [TAP findings PDF](https://www.telstra.com.au/content/dam/tcom/dynamic-media-projects/exchange/TAPFindingsforTelstraOutage.pdf) | 4/5/5/5/3/3 = **25** | CONTEXT — In the Know |
| T1-C2 | JVMCI is gone in GA; GraalVM's calendar stays on JDK 25 — and #3 was wrong | JVM | MATERIAL_UPDATE | 15 Sep / 22 Sep | No Graal JIT on JDK 27 on any published GraalVM roadmap through Feb 2027. #3 said "earliest JDK 29". | [JDK-8382582](https://bugs.openjdk.org/browse/JDK-8382582), [GraalVM calendar](https://www.graalvm.org/release-calendar/) | 3/4/5/4/4/4 = **24** | **SELECT — Signal (carries a correction)** |
| T1-C4 | JEP 544 AOT code compilation targeted to JDK 28 | JVM | NEW_THIS_MONTH | Candidate 10 Sep → Targeted 28 Sep | Cached native code is used only if training and production match CPU features and GC; otherwise silent JIT fallback. | [JEP 544](https://openjdk.org/jeps/544) | 5/5/4/3/3/4 = **24** | **SELECT — Signal candidate** |
| T1-C3 | G1 everywhere: who is newly affected | JVM | NEW_THIS_MONTH | 2026-09-15 | JVMs with no GC flag on 1 CPU or <1792 MB now get G1; no published G1-vs-Serial numbers; small-heap tickets open at GA. | [JEP 523](https://openjdk.org/jeps/523) | 4/5/4/3/4/4 = **24** | CONTEXT — In the Know (Arrays.fill 265× is a JDK 25 problem, fixed in 26) |
| T3-C5 | Postgres-as-Kafka vs leaving the database queue | Kafka | NEW_THIS_MONTH | 7–28 Sep | Kafgres ~700 MB/s single node with relaxed durability; Tigris left FDB for Kafka over write amplification. | [Kafgres](https://rynr.dev/blog/700mbskafgres/), [Tigris](https://www.tigrisdata.com/blog/quick-fdb-kafka/) | 5/4/3/3/5/4 = **24** | REJECT as Debate (HN 4–21 pts, no rebuttal, echoes #5's DBOS debate) → Top Resources |
| T5-C5 | MCP: obsolete overhead vs governed default | agentic | NEW_THIS_MONTH | 14–29 Sep | Earendil's Pi reversed its no-MCP stance (HN 686); Open Liberty `mcp-1.0` GA. | [earendil.com](https://earendil.com/posts/you-said-no-mcp/) | 4/4/4/3/5/3 = **23** | CONTEXT — MCP in ~20 past issue files; only as a line |
| T3-C3 | KIP-1279 Cluster Mirroring accepted | Kafka | MATERIAL_UPDATE | 2026-09-18 | Accepted, not merged or released. | [KIP-1279](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring) | 4/5/5/4/2/3 = **23** | CONTEXT — Today (state change on a #5 story) |
| T3-C6 | KRaft quorum loss has no stock recovery path | Kafka | NEW_THIS_MONTH | 2026-09-29 | Aiven: lost dynamic-quorum majority cannot be fixed with upstream tools. Vendor post. | [Aiven](https://aiven.io/blog/kafka-never-lose-quorum) | 5/4/3/4/3/4 = **23** | CONTEXT — Today |
| T5-C3 | JobRunr 9: durable steps made visible | agentic | NEW_THIS_MONTH (v9) / BACKGROUND (`runStepOnce` is v8) | 2026-09-30 | OSS can re-run a finished step after a hard crash; Pro saves immediately. | [v9.0.0](https://github.com/jobrunr/jobrunr/releases/tag/v9.0.0) | 4/5/4/3/4/3 = **23** | CONTEXT — In the Know |
| T2-C4 | sbt 2.1 milestones: plugin binary split, Ivy removed | Scala | NEW_THIS_MONTH | 13–28 Sep | Plugins built with 2.1 do not run on 2.0.x. | [sbt 2.1.0-M1](https://github.com/sbt/sbt/releases/tag/v2.1.0-M1) | 5/4/5/3/2/3 = **22** | CONTEXT — In the Know |
| T2-C5 | Box: 360+ module Scala monorepo, sbt → Gradle | Scala | NEW_THIS_MONTH (published 16 Sep) | 2026-09-16 | Remote cache is "the largest single reason" PR validation takes ~12 min. | [blog.box.com](https://blog.box.com/gradle-scala-monorepo-box-experience-360-modules) | 4/4/3/3/4/4 = **22** | CONTEXT — Top Resources (overlaps #6 monorepo lead) |
| T4-C6 | Antithesis × Datadog: a durability bug on the ordinary path of a JVM pipeline | correctness | NEW_THIS_MONTH | 2026-09-29 | Found without fault injection. Vendor case study, no bug counts. | [antithesis.com](https://antithesis.com/blog/2026/datadog/) | 5/5/3/3/2/4 = **22** | CONTEXT — In the Know |
| T2-C7 | Odersky / TACIT: tracked capabilities for agents | Scala | **BACKGROUND_ONLY** (post 27 Jul) | — | — | [Substack](https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents) | **17** | REJECT as Debate (stale, no opposing voice) |

## §4 Debate Candidate

Recommended: **T1-C1, compact object headers on by default.** Alternate: **T5-C1, typed decision model vs LLM-as-judge.** Full dossiers in `candidate-debate.md`.

- **Topic:** Should a JVM default trade double-digit heap savings for known single-to-double-digit CPU regressions in array-heavy code?
- **Side A:** Shipilev in JDK-8386990 — "it would be unwise to be spooked by single-digit-% regressions on microbenchmarks, when the real world footprint improvements … are double-digit-%". JEP 534's own numbers: SPECjbb2015 22% less heap, 8% less CPU.
- **Side B:** Kuksenko's regression list in the same ticket; Kozlov: fixing alignment in crypto intrinsics "may cause more regression than improvement"; JDK-8392511 (16 Sep) SERT LU −9%; ticket still Open, fix "tbd".
- **Why it matters for CTOs:** a JDK upgrade now changes object layout by default. The action is a measured rollout with `-XX:-UseCompactObjectHeaders` as the comparison arm, before the flag is deprecated.
- **Scalac angle (first draft):** Renaissance-ScalaKmeans is the one named macro workload in the regression list — Scala collections are array-heavy. Benchmark your own hot paths before you accept the default; don't read a microbenchmark as a verdict either way.

## §5 Trenches Candidate

Recommended: **T3-C1, KAFKA-20979.** Alternate: **T4-C1, NATS.** Full dossiers in `candidate-trenches.md`.

- **Problem:** Kafka brokers on 4.1.0 deleted recent, valid segments after a clean restart. Reporter (Mickael Maison, PMC): "This has happened multiple times in the past few weeks."
- **Context:** the time index is pre-allocated (10 MB default, zero-filled), truncated at close, and the truncation was never fsynced. After restart the zero tail reads as `largestRecordTimestamp=0`, which breaches any time-based retention.
- **Solution:** fixes merged 10 and 15 Sep, shipping in 4.3.2 (RC0 tagged 28 Sep) and 4.4.0. Interim operator check: grep broker logs for `largestRecordTimestamp=0` deletions after restarts. Sibling KAFKA-21000 covers `.log` files with preallocation.
- **Lesson:** a metadata change is not durable until it is fsynced; "clean shutdown" is a code path, and it needs the same durability review as a crash.
- **Scalac angle (first draft):** most teams test crash recovery and treat graceful shutdown as safe. This bug lived in the graceful path.

## §6 Signal Over Noise Candidates

Pick 3. Recommended order:

1. **Kafka 4.4.0 is late, and the project says it never promised a date** (T3-C2, with T3-C4 codec supply chain as the "why"). Re-check RC4 after 12 Oct.
2. **Scala 3.9 LTS: the dependency you didn't compile** (T2-C1 + T2-C2). Run tests with `--sun-misc-unsafe-memory-access=deny`; Spark on 3.8+ waits for Spark 4.3.0.
3. **No Graal JIT on JDK 27** (T1-C2), with an explicit correction to #3.

Bench: JEP 544 (T1-C4), agent-state deserialization on the JVM (T5-C2), typed decision models (T5-C1 if not the Debate).

## §7 In the Know Candidates

- G1 now the default everywhere (T1-C3) — who is affected, and why the Arrays.fill 265× post is a JDK 25 problem.
- KIP-1279 accepted, not shipped (T3-C3).
- sbt 2.1 plugin binary split (T2-C4).
- JDK 27 TLS: third-party JCE providers can fail TLS 1.3 handshakes (JDK-8377550), workaround `-Djdk.tls.t13KeyDerivationAlgorithm=TlsPremasterSecret`.
- JobRunr 9 OSS vs Pro step durability (T5-C3).

## §8 Top Resources

- **Repo to watch:** langchain4j `dev.langchain4j.model.decision` (if Decision models aren't the Debate) — or NATS final report (due early Nov) as a follow-up flag.
- **Article to read:** Box, "Gradle for Scala monorepo" (16 Sep); Tigris, "We used a database as a message queue. Now we use Kafka" (22 Sep); Hillel Wayne, "What TLA+ can and can't check" (30 Sep).
- **Paper to read:** arXiv 2609.37647, independent Jev evaluation (29 Sep).

## §9 Skipped Sources / Rejected Signals

See `skipped.md`.

## §10 Image List

Not drawn yet (03_draft writes `images.md`). Candidates that explain one relationship at a glance:
- **Trenches (Kafka):** a 10 MB index file, the tail zero-filled, a shutdown truncation arrow with no fsync, restart reads `timestamp=0`, retention scissors cut a fresh segment.
- **Debate (COH):** an object header shrinking from 12/16 to 8 bytes, the array's first element sliding from offset 16 to 12, a misaligned vector load.
- **Cover (if the spine holds):** three "safety" devices — a shutdown switch, an auto-reconnect plug, a kill switch — each with the damage flowing through it.

## §11 Open Questions / Fact-Check Needs

Blocking for draft:
1. **Kafka 4.4.0 RC4** — vote closes 12 Oct. GA or RC5 changes Signal 1.
2. **KAFKA-20979 in 4.2.2?** Jira lists fix versions 4.3.2 and 4.4.0 only; check 4.2.2 release notes. If not, 4.2.x users stay exposed.
3. **ScalaKmeans −20% attribution** — blamed on COH (JDK-8386990) *and* JVMCI removal (JDK-8386450). Never print a single cause.
4. **JEP 523 1792 MB threshold vs cgroup limit** — verify in HotSpot source before writing "K8s pods under 1792 MB".
5. **Shipilev's "70% smaller memory"** — no named project. Quote as his claim or drop.

Non-blocking:
6. snappy-java maintenance status (disputed on dev@); NVD severities not checked.
7. Unsafe phase 3 (deny by default) — no JDK named; check for a JDK 28 JEP draft.
8. Scala 3.10.0 — artifacts on Central 4 Oct, not announced. Don't call it released.
9. NATS final report due ~early Nov; supplier unnamed (HN "IBM" claim is speculation).
10. OpenAI Decisions API price — single community post only.
11. **JVM Weekly vol. 193 does exist** (track 5 could not find it): https://www.jvm-weekly.com/p/thinking-fast-and-typed-java-and — contains "be careful when a Jev demo looks too good". P1, quotable as opinion.
12. X/Twitter and LinkedIn not searched (no credentials) — engagement evidence is HN-only.

**Competitor flags this month:** VirtusLab — Sloth, tulip, VSS, Besom, WASM post, tanishiking's capture-checking intro, and the 7 Oct "VirtusLab assumes responsibility for Scala 2 maintenance" (touches the scala-reflect story; do not feature). SoftwareMill — Northguard/Xinfra post, diskless and Iggy posts. None featured.
