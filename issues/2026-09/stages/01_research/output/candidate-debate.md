# Candidate Debate — September 2026

Two candidates with substance on both sides. Recommendation: **D1**. D2 is the fallback, or a Signal if D1 runs.

The brief's original Debate candidate — "can the type system be the agent sandbox?" (Odersky / TACIT) — is **rejected**: the post is from 27 Jul (BACKGROUND_ONLY), the repo has had no commits since August, and no credible September voice argues against it. The strongest "types aren't enough" material is in the TACIT paper itself. Details: `track-notes/track2-scala-kotlin.md` §2.

---

## D1. Compact object headers on by default, with an open regression ticket (recommended)

**Topic:** JDK 27 (GA 15 Sep) turns compact object headers on by default (JEP 534). Oracle's own performance team has an Open ticket listing regressions, and the HotSpot engineers argue the trade in the ticket itself. Is the default right?

**Freshness:** NEW_THIS_MONTH — GA 15 Sep; new regression report JDK-8392511 on 16 Sep; diagnostic PR #32984 opened 21 Sep; JDK-8386990 last updated 22 Sep.

### Side A — footprint wins, ship the default

- [JEP 534](https://openjdk.org/jeps/534) (Oracle's numbers): SPECjbb2015 "22% less heap space and 8% less CPU time"; GC count "reduced by 15%"; a JSON parser "10% less time". Amazon runs "hundreds of services in production" with compact headers (mostly backports to 17/21). SapMachine already defaulted to it.
- Aleksey Shipilev in [JDK-8386990](https://bugs.openjdk.org/browse/JDK-8386990) (26 Jun): "it would be unwise to be spooked by single-digit-% regressions on microbenchmarks, when the real world footprint improvements from COH … are double-digit-%". He also says projects reported "70% … smaller memory usage" — **his claim, no project named; quote as such or drop.**
- Release notes: `-XX:-UseCompactObjectHeaders` "is planned for deprecation and removal in a future release". The opt-out is temporary by design.

### Side B — the regressions are known and unresolved

- Sergey Kuksenko (Oracle), JDK-8386990 (19 Jun): crypto −1% to −4%, Renaissance-ScalaKmeans −15% to −20%, String micros up to −50%, ArrayCopy micros up to −35%. Root cause: the first array element now sits at byte offset 12, not 16, so most primitive arrays are only 4-byte aligned.
- Vladimir Kozlov (26 Jun): realigning the hand-written AVX-512 crypto intrinsics "may cause more regression than improvement. -1%..-4% seems more acceptable". Doug Lea reported ForkJoinPool regressions after the default flip.
- Ticket status at GA: **Open, P4, fix version "tbd"**. Tobias Hartmann's PR [#32984](https://github.com/openjdk/jdk/pull/32984) (21 Sep) adds an opt-in `AlignArrayElements` flag "to diagnose JDK-8386990" — a diagnostic, not a fix.
- [JDK-8392511](https://bugs.openjdk.org/browse/JDK-8392511) (16 Sep): ~9% drop on SERT LU (2-D double arrays), Xeon 8280L, `-XX:+UseSerialGC`. Kuksenko couldn't reproduce it on a Xeon 8358.
- Oracle's [Inside.java performance post](https://inside.java/2026/09/28/performance-update-jdk27/) (28 Sep) hedges ("an application dominated by large primitive arrays will benefit less") and does not link the ticket.

### Honest caveats for the write-up

- Emanuel Peter (1 Jul) doubts the ScalaKmeans number is significant ("multi-modal in about the same range since JDK26"). The same −20% is **also** blamed on JVMCI removal in JDK-8386450. **Never print a single cause for ScalaKmeans.**
- Sidebar option: a P1 C2 bug (JDK-8390546) silently corrupted bytes 12–15 of copied arrays under compact headers in EA builds; found by a user on 18 Aug, backed out 19 Aug, the day before the RC. Not in GA. Shows compact headers change layout assumptions in C2 intrinsics. Reporter's employer unverified — don't name one.

### Why it matters for CTOs

Upgrading to JDK 27 changes object layout in every service by default. The decision is not "on or off" in the abstract; it is whether your hot paths are array-, string- or crypto-heavy. The opt-out flag is on a deprecation path, so the window to measure is now.

### Scalac angle (first draft)

The one named macro workload in Oracle's regression list is a Scala benchmark. Scala collections and serialization are array-heavy. Run your own throughput benchmark with `-XX:-UseCompactObjectHeaders` as the control arm before you roll JDK 27 out — and don't let a String microbenchmark or a SPECjbb headline decide it for you.

### Engagement

The argument is P0 (in JBS). HN had nothing specific to compact headers in the window. Evidence and tension are high; social engagement is low. That's acceptable under the rubric — engagement is never the evidence.

---

## D2. Typed decision models vs LLM-as-judge (alternate)

**Topic:** Three things landed within two weeks: TypeSafe's Jev (a model that answers typed questions, not text, 15 Sep), OpenAI's Decisions API (DevDay 29 Sep), and an experimental `DecisionModel` type in LangChain4j core (1.21.0, 2 Oct). Should routing, gating and grading move off general LLMs?

**Freshness:** NEW_THIS_MONTH.

### Side A — dedicated decision models

- Independent evaluation, [arXiv 2609.37647](https://arxiv.org/abs/2609.37647) (29 Sep, Uni Bonn / Lamarr / Fraunhofer IAIS): 37 datasets, 346,009 requests, ~US$9.15. Jev beats Qwen3.8-27B on 27 datasets, loses on 9; 11 of Jev's leads have non-overlapping 95% CIs, none of Qwen's do. Choice calibration ECE 0.028. Mean latency 0.36 s.
- LangChain4j put `DecisionModel` in `langchain4j-core` so routing, guardrails, re-ranking and tool selection share one primitive ([1.21.0 release](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0), [PR #6469](https://github.com/langchain4j/langchain4j/pull/6469): 54 files, +5,832, merged 29 Sep).
- Naming fight in [issue #6468](https://github.com/langchain4j/langchain4j/issues/6468) (21–25 Sep): JudgeModel → StructuredDecisionModel → DecisionModel. maxandersen: Jev "is explicitly not an LLM and doesn't reason step by step the way an 'LLM judge' does".
- OpenAI shipping the same shape ([Decisions guide](https://developers.openai.com/api/docs/guides/decisions), public beta) is category validation.

### Side B — general models still win where judgment is fuzzy

- Same paper: all models "degrade on … fine-grained or noisy labels, and rubric-based quality judgments". Binary probabilities "rank well but are poorly placed relative to a fixed 0.5 threshold" — per-task tuning moved UNFAIR-ToS micro-F1 from 0.50 to 0.75. That undercuts the zero-config pitch.
- HN launch thread ([49717558](https://news.ycombinator.com/item?id=49717558), 1,989 pts / 520 comments): the top thread calls the speed comparison "misleading", "apples-to-oranges" against reasoning LLMs.
- JVM Weekly vol. 193 ([link](https://www.jvm-weekly.com/p/thinking-fast-and-typed-java-and), P1 opinion): "be careful when a Jev demo looks too good".
- The API is `@Experimental` and changed shape three times in ten days.

### Why it matters for CTOs

Many agent systems spend most of their LLM budget on short decisions — route this, is this safe, which tool. A cheap, calibrated primitive for those changes cost and latency. The trap is assuming calibration transfers to every task without threshold tuning.

### Scalac angle (first draft)

Split decisions from generation in your agent architecture now, behind one interface — that's what LangChain4j just did. Log where every confidence number came from (native calibrated vs emulated by a chat model). Tune thresholds per task against labelled data before you trust a 0.5 cut.

### Check before using

- Jev is waitlist access, not open. Java/Scala/Kotlin SDKs are community projects (`spring-ai-typesafe` lives in the spring-ai-community org).
- polyvariant/jev4s is not on the competitor list, but check before naming it.
- Overlap: grep "Jev" / "System One" hits only this issue's brief. Not covered before.

---

## Considered and rejected

- **Postgres-as-Kafka vs leaving the DB queue** (Kafgres 700 MB/s vs Tigris FDB → Kafka): real tension, but HN 4–21 points, no published rebuttal, and the "one database vs dedicated system" frame repeats #5's DBOS/Temporal debate. → Top Resources (Tigris).
- **Durable execution: snapshot vs replay** (Trigora prototype vs Temporal's co-founder on HN): fresh axis, but Side A is one research prototype with its own "not a production claim" caveat. JobRunr v9 does not introduce durable steps (`runStepOnce` is v8).
- **MCP: obsolete vs governed default**: high engagement (HN 686 / 335) but MCP appears in ~20 past issue files.
