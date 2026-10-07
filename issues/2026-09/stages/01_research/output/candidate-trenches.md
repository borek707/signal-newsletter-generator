# Candidate Trenches — September 2026

The brief had no solid Trenches. Research found four with primary sources. Recommendation: **A (Kafka)** for audience fit and actionability; **B (NATS)** is the stronger story for a general reader and works as the intro anchor if A runs.

The brief's original lead — Arrays.fill 265× slower on G1 — **does not hold**: the pathology is on JDK 25; JDK 26's second card table (JEP 522) removes it, so teams moved to G1 by JDK 27 never see it. It's a JDK 25 LTS warning at most. Details: `track-notes/track1-jvm.md` C3.

---

## A. A clean shutdown could delete recent Kafka data (KAFKA-20979) — recommended

**Freshness:** MATERIAL_UPDATE. Filed 24 Aug; fixes merged 10 Sep (4.4 branch, commit beae700) and 15 Sep (PR #23316); Jira resolved 15 Sep. Ships in 4.3.2 (RC0 tagged 28 Sep) and 4.4.0.

**Problem.** Brokers on Kafka 4.1.0 (affects-version also lists 4.3.0) deleted segments holding recent, valid records after a *clean* restart. Reporter Mickael Maison (PMC): "It's deleting many segments due to the retention limits. This has happened multiple times in the past few weeks." Log line:

```
Deleting segment LogSegment(baseOffset=83454, size=4483, ..., largestRecordTimestamp=0)
due to log retention time 604800000ms breach
```

**Root cause (verbatim from the Jira).** "The flush() fsyncs the time index file at its pre-allocated size (10MB by default, zero-filled). The close() truncates the file … which calls RandomAccessFile.setLength(), but never fsyncs the truncation." After restart, the zero-filled tail reads as `timestamp=0`, so the segment looks seven days old and time-based retention removes it.

**Sibling bug.** [KAFKA-21000](https://issues.apache.org/jira/browse/KAFKA-21000): the same class of bug for `.log` files when preallocation is on (`trim()` without flushing length metadata). That one throws on restart rather than deleting. PR #23303 merged 3 Sep, fix version 4.5.0 only.

**Fix.**
- Upgrade to 4.3.2 or 4.4.0 when released.
- Until then: watch broker logs after restarts for deletions with `largestRecordTimestamp=0`.
- Luke Chen on including it in 4.4.0: "Given this issue will cause data loss for the impacted partitions, I think we should include this fix in v4.4.0." Agreed by Chia-Ping Tsai, 10 Sep.

**Lesson.**
1. A metadata change (file length) is not durable until it's fsynced. This is the same lesson as the filesystem-durability research of 2018–2020, now in a broker everyone runs.
2. "Clean shutdown" is a code path with its own durability bugs. Most teams test crash recovery and treat graceful restarts as safe — rolling upgrades are graceful restarts.
3. The cost of the fix is slower shutdown. That's the right trade.

**Sources (all P0):** [KAFKA-20979](https://issues.apache.org/jira/browse/KAFKA-20979) · [PR #23316](https://github.com/apache/kafka/pull/23316) · [PR #23258](https://github.com/apache/kafka/pull/23258) · [KAFKA-21000](https://issues.apache.org/jira/browse/KAFKA-21000) · [PR #23303](https://github.com/apache/kafka/pull/23303)

**Community reaction:** dev@ and Jira only (6 Jira comments, 33 PR review comments). No HN or Reddit thread. Nobody in the newsletter space has covered it.

**Open before draft:** does 4.2.2 (released 29 Sep) include the fix? Jira lists only 4.3.2 and 4.4.0. If not, say 4.2.x stays exposed.

**Scalac angle (first draft):** If your Kafka upgrade runbook only tests the crash case, it missed this. Add a restart-and-verify step: produce, restart cleanly, check retention didn't fire on fresh segments.

**Score:** 4/5/5/5/3/5 = 27/30.

---

## B. NATS: a ~1 ms race corrupted UK flight data, and auto-recovery hid it — alternate / intro anchor

**Freshness:** NEW_THIS_MONTH. Incident 8 Sep; preliminary report dated 16 Sep.

**Problem.** London Area Control lost automated flight-data exchange with NAS, the core UK flight-data system. UK departures stopped for about 4.5 hours in a 6-hour period. NATS forecast ~8,000 flights and handled 6,094; "more than two thousand flights were delayed, cancelled or diverted."

**Root cause (NATS report).**
- A "legacy and previously unknown" defect in NAS squawk-code allocation.
- A higher-priority message arrived "during that exact millisecond while the original request was part-way through updating a value". When processing resumed, the output was corrupt. Exposure window: "approximately one millisecond".
- 10:02: the LAC↔NAS link dropped and recovered in 45 s. Logged as a standard incident, "recovered and stable".
- From 12:32 the link flapped as reads of the corrupt record timed out. At 13:32 it dropped "and does not recover" — by design, to "protect the integrity of both systems".

**Fix.**
- Controlled NAS restart and reload from LAC (15:17–16:09), then reconciliation until 18:50: duplicate flight plans, code and callsign correlation anomalies, plans filed while disconnected. Restrictions lifted 19:30.
- Supplier software fix in safety testing; interim "additional engineering framework" for link-drop events.
- **No code, config or language detail published.** Final report due within 60 days (~early November).

**Lesson.**
1. A preemptible, non-atomic update to shared state is a race regardless of window size.
2. An auto-recovering timeout can hide data corruption. The 10:02 "recovered" alert was the first symptom. Repeated timeouts on the same record are a poison-message signal.
3. Isolating a failing peer protects integrity and creates divergence. Reconciliation took 2 h 41 min of the recovery.

**Sources:** [NATS preliminary report (PDF, P0)](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf) · [NATS news post](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/) · HN [49754064](https://news.ycombinator.com/item?id=49754064) (59 pts / 27 comments)

**Score:** 5/5/5/5/3/4 = 27/30. Weaker on JVM relevance and on "solution with code".

---

## C. Scala 3.9 LTS and the jar you never compiled — Signal by default, Trenches option

**Freshness:** NEW_THIS_MONTH (3.9.0 announced 3 Sep). Spark side is MATERIAL_UPDATE.

**Problem.** Lazy vals compiled with Scala 3.0–3.7 go through `scala.runtime.LazyVals` on `sun.misc.Unsafe`. Recompiling your own code with 3.8+ doesn't help if a dependency was built with the old compiler. Separately, scala-reflect 2.13 runtime reflection throws on the 3.8+ stdlib, and released Spark initialises it.

**Evidence (reproduced by the research agent on JDK 27 GA, build 27+35).**
- Scala 3.3.6 lazy val, default flags: warning naming `scala.runtime.LazyVals$`, then runs.
- With `--sun-misc-unsafe-memory-access=deny`: `UnsupportedOperationException` from `LazyVals$.getOffsetStatic`.
- Scala 3.9.0, same code, `deny`: runs clean.
- scala-reflect on 3.9.0: `FatalError: class Array does not have a member apply`; 3.7.4 works.
- Secondary sources saying "JDK 26 throws by default" repeat JEP 471's 2024 plan, which has not shipped.

**Fix path (non-competitor).** Test with `=deny` to find affected dependencies; upgrade to library releases built with 3.8+; `=allow` only as a bridge. Spark: fixes merged 23 Aug target Spark 4.3.0 (unreleased); SPARK-57549 (TypeTag encoders) still open. Do **not** present the VirtusLab bytecode rewriter (Sloth) as the answer.

**Sources:** [Scala 3.9 announcement](https://www.scala-lang.org/news/3.9/) · [JEP 471](https://openjdk.org/jeps/471) · [scala3#25896](https://github.com/scala/scala3/issues/25896) · [SPARK-57548](https://issues.apache.org/jira/browse/SPARK-57548) · [SPARK-57549](https://issues.apache.org/jira/browse/SPARK-57549)

**Score:** 26/30 (C1), 25/30 (Spark).

---

## D. Firebase: a 2-line flag cleanup crashed iOS apps globally — Today / intro example

**Freshness:** NEW_THIS_MONTH (28 Sep PDT; Google post-mortem 2 Oct).

**Summary.** A cleanup removed a remote-config flag the GA4F iOS SDK still referenced; the SDK crashed on a nil key. Served for 2 h 11 min. The kill-switch mechanism is "released globally", so it reached everyone at once. Google: dashboards "remained green". One-time crash per user, then fallback — which contradicts the viral "ALL sessions" framing on X. Four commitments, including SDK-side payload validation and phased config rollout.

**Source:** [Google post-mortem (P0)](https://firebase.blog/posts/2026/10/firebase-analytics-outage) · [firebase-ios-sdk#16728](https://github.com/firebase/firebase-ios-sdk/issues/16728)

**Why not Trenches:** iOS SDK, not JVM; already widely covered (PE, 9to5Google, MacRumors).

**Score:** 25/30.
