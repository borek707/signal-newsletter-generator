# Candidate Signals — September 2026

Seven candidates for three slots. Recommended three first. Every item is NEW_THIS_MONTH or MATERIAL_UPDATE; nothing BACKGROUND_ONLY is here.

---

## Recommended

### S1. Kafka 4.4.0 is a month late, and the project says it never promised a date

- **What changed:** The release plan said "no earlier than September 9 2026". RC0 (21 Aug), RC1 (22 Sep) and RC3 (29 Sep) failed; RC4 was tagged 6 Oct and its vote closes **12 Oct**. Ericsson engineers on users@ had planned their own end-of-September release around 4.4.0's vulnerability fixes. PMC replies: "As an open source project, we don't have committed release dates" (Matthias J. Sax); "have you considered packaging Kafka 4.3.2 or 4.2.2 instead" (Chia-Ping Tsai); "We had too many must-have changes in 4.4.0 … CVEs are common these days" (Tsai, 29 Sep). A proposal moves 4.5.0 to ~17 Mar 2027 (two +1s, not formally adopted).
- **Why it matters:** if your CVE remediation depends on an unreleased OSS minor, you hold the schedule risk. Patch lines are the hedge: 4.2.2 shipped 29 Sep; 4.3.2 RC0 tagged 28 Sep.
- **Migration note:** KAFKA-20939 (an RC blocker, resolved 10 Sep): KIP-909 changed client DNS-failure behaviour — producers with an unresolvable bootstrap now get a non-retriable `BootstrapResolutionException` from `send()` instead of `ConfigException` in the constructor. Streams and Connect had async DNS disabled to cope.
- **Fold-in option:** Kafka's codec supply chain (dev@, 29 Sep): Luke Chen says three snappy-java CVEs can't be fixed with a version bump; LZ4 depends on a one-person fork; old codecs can't be removed because historical logs must stay readable, so KAFKA-21178 proposes disabling codecs on write. **The snappy "unmaintained" claim is disputed** (Martin Andersson, 5 Oct); the lz4 point stands.
- **Sources (P0):** [Release plan 4.4.0](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/429064575/Release+Plan+4.4.0) · [users@ release-date thread](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf) · [RC4 vote](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222) · [dev@ time-based releases](https://lists.apache.org/thread/o1d5p48t7br2bbh0rwl65rybd331pn7d) · [codec thread](https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8) · [KAFKA-21178](https://issues.apache.org/jira/browse/KAFKA-21178)
- **Re-check before draft:** RC4 result. If GA lands, reframe as "4.4.0 shipped five weeks late — check KIP-909 DNS behaviour".
- **Score:** 27/30 (+ codec item 26/30).

### S2. Scala 3.9 LTS: the Unsafe warning comes from a jar you never compiled

- **What changed:** Scala 3.9.0 LTS announced 3 Sep. 3.3 LTS gets one more year (~Sep 2027); 3.9 at least three. SIP-71 `into` is stable.
- **Why it matters:** lazy vals compiled with Scala 3.0–3.7 still call `sun.misc.Unsafe`. On JDK 27 GA they warn and run; under `--sun-misc-unsafe-memory-access=deny` they fail (reproduced locally on build 27+35). Recompiling your code with 3.8+ doesn't fix a dependency built earlier. Separately, scala-reflect 2.13 runtime reflection throws on the 3.8+ stdlib (`FatalError: class Array does not have a member apply`, reproduced); released Spark initialises it, and the Spark fixes target the unreleased 4.3.0. The Scala team says fix it in Spark; Spark users say Spark releases too slowly ([scala3#25896](https://github.com/scala/scala3/issues/25896)).
- **Migration path:** run the test suite with `--sun-misc-unsafe-memory-access=deny` now; upgrade dependencies to releases built with 3.8+; use `=allow` only as a bridge (JEP 471: once deny becomes default, `allow` stops working). Spark teams: stay on 3.7.x or wait for Spark 4.3.0. Next: 3.10 stops finding implicits in inaccessible companions (~20 community-build projects break) and 3.10.0 artifacts were on Maven Central 4 Oct, unannounced.
- **Sources (P0):** [Scala 3.9 announcement](https://www.scala-lang.org/news/3.9/) · [JEP 471](https://openjdk.org/jeps/471) · [SPARK-57548](https://issues.apache.org/jira/browse/SPARK-57548) · [SPARK-57549](https://issues.apache.org/jira/browse/SPARK-57549)
- **Competitor:** the 3.9 announcement is by a VirtusLab engineer — fine to cover as a scala-lang release, don't credit. The bundled bytecode rewriter (Sloth) is VirtusLab's — mention generically or not at all.
- **Score:** 26/30.

### S3. There is no Graal JIT on JDK 27 — and we told you JDK 29

- **What changed:** JDK 27 GA (15 Sep) ships without JVMCI, the `jdk.graal.compiler` module or `-XX:+UseGraalJIT` ([JDK-8382582](https://bugs.openjdk.org/browse/JDK-8382582), no JEP; CSR rationale: "an experiment that has outlived its usefulness"). GraalVM 25.4 (22 Sep) is still JDK 25-based, and every GraalVM release on the published calendar through 23 Feb 2027 (25.5–25.8) is on the JDK 25 baseline.
- **Correction owed:** SIGNAL #3 (May) and the May–June LinkedIn edition said "Earliest removal is JDK 29". The removal was integrated 26 May and shipped in JDK 27.
- **Why it matters:** teams running the Graal JIT can't move to JDK 27 by swapping in a GraalVM build. Native Image users are unaffected at build level (GraalVM ships its own JDK). Downstream cost: TornadoVM vendored 104 JVMCI API files ([PR #1192](https://github.com/beehive-lab/TornadoVM/pull/1192)).
- **Caveat:** JDK-8386450 ties a −20% ScalaKmeans regression on Linux x64 to the removal (Won't Fix; +12–15% on aarch64). The same number is also blamed on compact headers. Don't print a single cause.
- **Sources (P0):** [JDK 27 release notes](https://jdk.java.net/27/release-notes) · [JDK-8385105 CSR](https://bugs.openjdk.org/browse/JDK-8385105) · [GraalVM 25.4 notes](https://www.graalvm.org/release-notes/25.4/) · [GraalVM release calendar](https://www.graalvm.org/release-calendar/)
- **Score:** 24/30. The correction is the reason it earns a slot.

---

## Bench

### S4. JEP 544: AOT code compilation is targeted to JDK 28, with a silent-fallback trap

- **What changed:** Candidate 10 Sep → Proposed to Target 18 Sep → Targeted 28 Sep.
- **Claim:** the AOT cache will also store compiled native code. JEP figures (JDK 28 EA, 2-core x64): startup −50…70% with the cache alone, −65…80% with AOT code. The code is used only if training and production share CPU features and GC; otherwise HotSpot warns and falls back to JIT.
- **Angle:** JEP 523 (G1 everywhere) removes one CI-vs-prod GC mismatch; CPU-feature mismatch remains. HN [49647404](https://news.ycombinator.com/item?id=49647404) (105 / 74): "The tooling for doing these sorts of training runs doesn't really exist."
- **Source:** [JEP 544](https://openjdk.org/jeps/544). Score 24/30. Pairs well with S3 (JIT + AOT cache vs Native Image).

### S5. Agent state is a deserialization sink, and A2A defaults fail open (JVM)

- **What changed:** [GHSA-gmwr-7wmf-mrjm](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm) (10 Sep): langchain4j-agentic's `AgenticScopeSerializer` enabled Jackson default typing over persisted agent state (CVSS 6.6; needs a gadget class and attacker-controlled state). a2a-java ≤1.2.0.Final: default `InMemoryTaskStore` did no read authorization (CVSS 7.5); credentials survived cross-origin redirects; an Android fix was undone and re-fixed 9 Sep ([advisories](https://github.com/a2aproject/a2a-java/security/advisories)).
- **Angle:** durable agents need persisted state; persisted state is input. Don't overstate — the langchain4j bug needs a gadget.
- Score 26/30. Strong if the issue wants an agentic Signal.

### S6. Typed decision models (if not the Debate)

See `candidate-debate.md` D2. LangChain4j 1.21.0 `DecisionModel` (2 Oct), Jev (15 Sep), OpenAI Decisions API (29 Sep), independent eval [arXiv 2609.37647](https://arxiv.org/abs/2609.37647). Score 26/30.

### S7. AWS declares me-south-1 data unrecoverable

- **What changed:** 15 Sep, AWS Health Dashboard: damage "spanned multiple Availability Zones and exceeded what our regional and multi-AZ services are designed to withstand"; data "hosted exclusively in this Region" unrecoverable; same for one UAE AZ.
- **Angle:** multi-AZ is a design for independent failures; residency mandates and DR pull against each other. HN 530 / 452.
- **Caution:** the cause is physical destruction from military strikes. Keep the framing technical; no service-level data-loss breakdown exists.
- **Source:** [AWS Health RSS](https://status.aws.amazon.com/rss/multipleservices-me-south-1.rss). Score 25/30. Better as a Today bullet than a Signal.
