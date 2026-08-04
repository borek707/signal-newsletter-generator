# Candidate Trenches — July 2026

Two candidates found. **Recommend Candidate B as primary** given Candidate A's sourcing gap; keep A as backup if the loom-dev/JBS thread gets independently verified before drafting.

## Candidate A: JVM virtual-thread SIGSEGV regression (needs verification — see caveat)

**The Problem:** JVM crashes with SIGSEGV during G1 heap scanning when virtual threads are in use.

**Context (scale, constraints):** BellSoft Liberica 24.0.2+12, Spring Boot 3.4, Kotlin. Per JVM Weekly's account, root cause is JIT deoptimizations erroneously undone when processing exception subclasses via `HandshakeAllThreads`.

**Solution:** Revert to platform threads until a backported fix is available.

**Lesson:** Virtual threads + G1 + certain JIT deopt paths are not yet a fully safe combination on this JDK line. Canary before a blanket virtual-thread rollout.

**Scalac angle (first draft):** Teams mid-migration to virtual threads should canary on a JDK/G1 combination close to production before a full rollout, and track this specific JBS ticket before upgrading.

**⚠️ Verification caveat (do not skip at review):** This is currently single-sourced — JVM Weekly Vol. 186 plus a link to the OpenJDK loom-dev mailing list that returned HTTP 403 on direct fetch. An attempt to independently corroborate via [GitHub `adoptium/adoptium-support#1127`](https://github.com/adoptium/adoptium-support/issues/1127) surfaced a **different, unrelated, older, stale-and-closed** issue (JDK 21.0.1, CentOS 7.9, no linked JBS bug) that happens to share the surface-level description "virtual thread SIGSEGV." **Do not cite #1127 as corroborating JDK-8377715** — they are not the same bug. Before using Candidate A, get a working fetch of the real loom-dev thread or the JBS ticket itself.

---

## Candidate B: Batch-to-micro-batch streaming migration (recommended primary)

**The Problem:** An ads/campaign delta-index pipeline suffered from scheduling-induced staleness, not processing inefficiency. Jobs were externally scheduled on a fixed interval, so incremental data arriving shortly after a run had to wait nearly a full interval before being processed. Any failure required re-running the entire window, even when only part of the data was incomplete.

**Context (scale, constraints):**
- Several million documents; delta index tens of gigabytes.
- New data arrived every 5-7 minutes.
- Full index rebuild took 2-3 hours plus validation and deployment.
- Source data lived as time-partitioned files in object storage (S3-style).

**Solution (with mechanism detail):**
- Migrated to Spark Structured Streaming with a fixed 30-second trigger interval.
- Time-driven execution comparing the latest available partition against a watermark.
- "Freshness-first" logic: skip intermediate partitions, always process the latest.
- Deterministic progress without relying on fragile completion markers.
- Planned 24-hour restarts as a routine operational mechanism, managed by an external watchdog for job liveness.

**Lesson:** "The best streaming design is the one that works reliably in production, not the one that looks the most elegant in theory." Record-level streaming would have added operational risk this system didn't actually need — the real bottleneck was scheduling cadence, not per-record latency.

**Result:** End-to-end latency dropped roughly 50%; worst-case freshness lag fell from ~10 minutes to 30 seconds.

**Scalac angle (first draft):** Before reaching for record-level streaming, check whether the actual problem is processing latency or scheduling latency — this team's fix was a trigger-interval and watermark change, not a rewrite to per-record semantics.

**Source:** [InfoQ: "From Batch to Micro-Batch Streaming: Lessons Learned the Hard Way in a Delta Index Pipeline"](https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/) — also independently listed in InfoQ Architects' Newsletter #108 (July 2026) as a Case Study, so it's getting real editorial attention this month, not just a standalone blog post.
