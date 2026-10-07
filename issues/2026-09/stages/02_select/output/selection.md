# Selection — SIGNAL Issue #7, September 2026

Approved by Piotr on 2026-10-07: the research lineup, then one swap — typed decision models move up to Debate, compact object headers move down to Signals, and the Graal/JVMCI correction moves to In the Know.

## Theme

**The damage went down the path that was supposed to protect you.** A Kafka broker deleted fresh data on a clean shutdown. A UK flight-data link "recovered" and spread corruption for two and a half hours. Firebase's kill switch, the mechanism meant to undo bad releases, carried a bad flag to every iOS app at once. JDK 27 made a new object layout the default while Oracle's own regression ticket is still open.

Three legs: AI on the JVM (Debate), data durability (Trenches), upgrades that change defaults under you (Signals).

## Lineup

| Slot | Item | Freshness | Score | Why |
|---|---|---|---|---|
| Debate | Typed decision models vs LLM-as-judge (LangChain4j `DecisionModel`, Jev, OpenAI Decisions API) | `NEW_THIS_MONTH` | 26 | Highest engagement of the month, JVM-native (LangChain4j core), an independent evaluation gives both sides P0 evidence. |
| Trenches | KAFKA-20979: a clean shutdown deleted recent data | `MATERIAL_UPDATE` (fixes merged 10 and 15 Sep) | 27 | Production report from a PMC member, code-level root cause, published fix, an operator check readers can run today. Not covered anywhere else. |
| Signal 1 | Kafka 4.4.0 is a month late; the PMC never promised a date | `NEW_THIS_MONTH` | 27 | CVE remediation planned around an unreleased minor. KIP-909 DNS change is the upgrade note. Codec supply-chain thread explains part of the delay. |
| Signal 2 | Scala 3.9 LTS: the Unsafe warning comes from a jar you didn't compile | `NEW_THIS_MONTH` | 26 | Reproduced on JDK 27 GA. Spark on the 3.8+ stdlib waits for Spark 4.3.0. |
| Signal 3 | JDK 27 turns compact object headers on by default, with an open regression ticket | `NEW_THIS_MONTH` | 28 | Every service's object layout changes on upgrade. Oracle lists the regressions itself; the opt-out flag is on a deprecation path. |
| In the Know | No Graal JIT on JDK 27, and a correction to Issue #3 | `MATERIAL_UPDATE` | 24 | We told readers "JDK 29 at the earliest". It shipped in 27. |
| In the Know | G1 is the default in every environment (JEP 523) | `NEW_THIS_MONTH` | 24 | Small pods and CLIs without a GC flag now get G1; no published G1-vs-Serial numbers. |
| In the Know | JEP 544 AOT code compilation targeted to JDK 28 | `NEW_THIS_MONTH` | 24 | Native code from the AOT cache is used only if training and production match CPU features and GC. |
| In the Know | Agent state is a deserialization sink (langchain4j-agentic, a2a-java advisories) | `NEW_THIS_MONTH` | 26 | Durable agents persist state; persisted state is input. |
| In the Know | KIP-1279 Cluster Mirroring accepted, not shipped | `MATERIAL_UPDATE` | 23 | State change on a story from Issue #5. |
| Repo to watch | [lampepfl/tacit](https://github.com/lampepfl/tacit) | `BACKGROUND_ONLY` — must be labelled as July work, not September news | 17 | Odersky's group: the agent writes Scala 3, and capture checking decides what that code may touch (classified data only reachable by pure functions). Paper reports 100% security at 90–99% task utility in its own experiments. Boundary from the paper itself: external processes escape the safe-mode boundary, side channels aren't covered, the JVM is trusted, so a sandbox is still needed. Re-added 2026-10-07 at Piotr's request. |
| Article to read | [Tigris: "We used a database as a message queue. Now we use Kafka"](https://www.tigrisdata.com/blog/quick-fdb-kafka/) | `NEW_THIS_MONTH` (22 Sep) | 21 | When a transactional queue inside your primary store starts eating its write budget. Pairs with the Trenches. |
| Report to read (Paper slot) | [NATS preliminary investigation report, NAS incident of 8 Sep 2026](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf) | `NEW_THIS_MONTH` (issued 16 Sep) | 27 | 18 pages, minute-by-minute: a ~1 ms race on shared state, an auto-recovery that hid the corruption, and the cost of reconciling two stores after a partition. The longer read behind the intro. Preliminary: no code or config; final report due ~early November (follow-up for #8). |

Changed 2026-10-07 at Piotr's request:
- **Dropped the CapScope paper.** It belonged to the rejected "type system as agent sandbox" Debate, and it has no JVM angle. Replaced by the NATS report.
- **Kept the TACIT repo.** It's dropped once, then re-added. It's July work (BACKGROUND_ONLY), so the copy must say so, but it's the most Scala-native agent-safety work available.

Main items: 5 of a maximum 6. No Community Voice this month.

## Intro, Today and Top Resources only (not separate sections)

- **NATS, 8 Sep** — auto-recovering link hid flight-data corruption. Intro anchor for the theme, and the report to read.
- **Firebase, 28 Sep** — kill-switch config shipped globally; dashboards stayed green. Intro anchor for the theme.

Neither gets a body section, so neither may be repeated in In the Know.

## Deduplication check

- Decision models appear only in the Debate. The arXiv 2609.37647 Jev evaluation is a Debate source, not the Paper to read.
- Kafka: the Trenches is a durability bug; Signal 1 is release process. No KAFKA-20979 detail in Signal 1, no release-schedule detail in the Trenches.
- JDK 27: Signal 3 is compact headers only. JVMCI, G1 and JEP 544 are separate In the Know lines. The ScalaKmeans −20% number appears in Signal 3 only, with both disputed causes named.

## Sources

**Debate**
- primary: [LangChain4j 1.21.0 release](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0)
- primary: [PR #6469](https://github.com/langchain4j/langchain4j/pull/6469)
- primary: [issue #6468, naming discussion](https://github.com/langchain4j/langchain4j/issues/6468)
- primary: [TypeSafe, Introducing System One models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- primary: [OpenAI Decisions guide](https://developers.openai.com/api/docs/guides/decisions)
- verification: [arXiv 2609.37647, independent Jev evaluation](https://arxiv.org/abs/2609.37647)
- community: [HN 49717558](https://news.ycombinator.com/item?id=49717558) (1,989 / 520)
- community: [JVM Weekly vol. 193](https://www.jvm-weekly.com/p/thinking-fast-and-typed-java-and) — opinion, P1

**Trenches**
- primary: [KAFKA-20979](https://issues.apache.org/jira/browse/KAFKA-20979)
- primary: [PR #23316](https://github.com/apache/kafka/pull/23316), [PR #23258](https://github.com/apache/kafka/pull/23258)
- primary: [KAFKA-21000](https://issues.apache.org/jira/browse/KAFKA-21000), [PR #23303](https://github.com/apache/kafka/pull/23303)

**Signal 1**
- primary: [Release Plan 4.4.0](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/429064575/Release+Plan+4.4.0)
- primary: [users@ release-date thread](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)
- primary: [RC4 vote](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222)
- primary: [codec dev@ thread](https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8), [KAFKA-21178](https://issues.apache.org/jira/browse/KAFKA-21178)
- primary: [KAFKA-20939](https://issues.apache.org/jira/browse/KAFKA-20939) (KIP-909 DNS change)

**Signal 2**
- primary: [Scala 3.9 announcement](https://www.scala-lang.org/news/3.9/)
- primary: [JEP 471](https://openjdk.org/jeps/471)
- primary: [scala3#25896](https://github.com/scala/scala3/issues/25896), [SPARK-57548](https://issues.apache.org/jira/browse/SPARK-57548), [SPARK-57549](https://issues.apache.org/jira/browse/SPARK-57549)
- verification: local reproduction on JDK 27+35 (track-notes/track2, C1 and C2)

**Signal 3**
- primary: [JEP 534](https://openjdk.org/jeps/534)
- primary: [JDK-8386990](https://bugs.openjdk.org/browse/JDK-8386990), [JDK-8392511](https://bugs.openjdk.org/browse/JDK-8392511), [PR #32984](https://github.com/openjdk/jdk/pull/32984)
- primary: [JDK 27 release notes](https://jdk.java.net/27/release-notes)
- verification: [Inside.java, Performance Improvements in JDK 27](https://inside.java/2026/09/28/performance-update-jdk27/)

**In the Know**
- primary: [JDK-8382582](https://bugs.openjdk.org/browse/JDK-8382582), [GraalVM release calendar](https://www.graalvm.org/release-calendar/)
- primary: [JEP 523](https://openjdk.org/jeps/523); verification: [Open Liberty 26.0.0.10 beta](https://openliberty.io/blog/2026/09/22/26.0.0.10-beta.html)
- primary: [JEP 544](https://openjdk.org/jeps/544)
- primary: [GHSA-gmwr-7wmf-mrjm](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm), [a2a-java advisories](https://github.com/a2aproject/a2a-java/security/advisories)
- primary: [KIP-1279](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring), [vote result](https://lists.apache.org/thread/15rddlqk42tqsjh5rw2r6so5cgns122f)

**Intro**
- primary: [NATS preliminary report](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf)
- primary: [Firebase post-mortem](https://firebase.blog/posts/2026/10/firebase-analytics-outage)

## Rejected

| Item | Reason |
|---|---|
| Odersky / TACIT as Debate | Published 27 Jul; no credible opposing voice in September. Repo kept as Repo to watch, labelled as July work. |
| Compact headers as Debate | The argument is real but lives in a bug tracker; no reader-facing tension. Moved to Signal 3. |
| Graal / JVMCI as Signal | Correction to #3 is mandatory but doesn't need a full slot. Moved to In the Know. |
| Arrays.fill 265× on G1 as Trenches | JDK 25 problem; JDK 26 fixed it. |
| NATS as Trenches | No code or config published; final report due ~early November. Intro anchor instead, and a candidate for a later issue. |
| Firebase as Trenches | iOS SDK, not JVM; widely covered already. Intro anchor instead. |
| AWS me-south-1 data unrecoverable | Strong stakes (HN 530), but the cause is physical destruction from military strikes; the lesson ("multi-AZ is not region-level durability") fits one line and the story pulls toward geopolitics. Excluded; human can overrule. |
| Telstra NTP | Outage in July; report in September. Good concept, weak freshness. |
| Kafgres / Postgres-as-Kafka Debate | Low engagement, no rebuttal, repeats #5's DBOS debate. Tigris kept as Article. |
| MCP obsolete vs governed | MCP in ~20 past issue files. |
| JobRunr 9 durable steps | `runStepOnce` is from v8. |
| Netflix Conductor, DoorDash gateway, ByteByteGo payments | Background (Aug, Jul, Mar). |
| Salesforce 16 Sep | No RCA yet. |
| Box Gradle monorepo | Overlaps #6's monorepo lead. |
| sbt 2.1, Pre-SIP `T ? E`, Scala 3.10 | Under the six-item cap; low CTO stakes this month. |
| Competitor items | Sloth, tulip, VSS, Besom (VirtusLab); Northguard post, diskless, Iggy (SoftwareMill); Typelevel Traverses Europe. |

## Must clear before drafting

1. **Open — Kafka 4.4.0 RC4 vote result** (closes 12 Oct). Signal 1 changes wording either way. Draft both versions; pick after 12 Oct.

2. **Cleared 2026-10-07 — Kafka 4.2.2 does not contain the KAFKA-20979 fix.**
   - Not in the [4.2.2 release notes](https://downloads.apache.org/kafka/4.2.2/RELEASE_NOTES.html) (33 issues, neither KAFKA-20979 nor KAFKA-21000).
   - No backport commit on the `4.2` branch between 20 Aug and 7 Oct.
   - Jira fix versions are 4.3.2 and 4.4.0 only. Affects-versions list 4.1.0 and 4.3.0; 4.2 isn't listed, but nothing says it's unaffected.
   - Wording for the Trenches: "no 4.2.x release carries the fix". Don't claim 4.2 is affected; don't claim it's safe.

   **Two claim boundaries found while checking, both required in the Trenches prose:**
   - The mechanism is the reporter's analysis ("I think this behavior could be caused by invalid time index truncation"). The fix was merged on that basis; no one published a standalone reproduction.
   - Per the Jira description, data is lost "if the broker restarts before the OS flushes the file metadata". The trigger is a clean shutdown *followed by* a restart that beats the metadata flush, not every clean shutdown.

3. **Cleared, then dropped — CapScope (arXiv 2609.08371, 8 Sep 2026).** Bouras, Dai, Mechtaev.
   - Abstract results, on the Pi coding agent across 300 runs: the injected effect executed in 33–47 of 75 runs under the baselines and in 3 of 75 under CapScope. Repairs completed: 68 of 75, against 68–72 for the baselines.
   - Boundary: a small evaluation (five Python tasks).
   - Removed from Top Resources: no link to this issue's Debate or theme. Replaced by the NATS report.

4. **Cleared — JEP 523 threshold vs cgroup limit.**
   - At `jdk-27-ga`, `GCConfig::select_gc_ergonomically()` sets G1 unconditionally when G1 is built in.
   - The old path in `os::is_server_class_machine()` needed at least 2 active processors and `os::physical_memory() >= 2 GB − 256 MB` (= 1792 MB).
   - At `jdk-26-ga`, the Linux `os::physical_memory()` returns the container memory limit when one is set (`OSContainer::memory_limit_in_bytes`).
   - So the wording "pods with a memory limit under 1792 MB or fewer than 2 CPUs, started without a GC flag, move from Serial to G1" is correct for Linux containers.
   - Source: openjdk/jdk `src/hotspot/share/gc/shared/gcConfig.cpp` and `src/hotspot/share/runtime/os.cpp` at `jdk-27-ga`; `src/hotspot/os/linux/os_linux.cpp` at `jdk-26-ga`.

## Open editorial question

**Publish date.** Before Scala Days (12–13 Oct) means drafting before the Kafka RC4 vote closes, so Signal 1 would describe an unfinished vote. Week of 19 Oct lets Signal 1 state the outcome. Recommendation: week of 19 Oct.
