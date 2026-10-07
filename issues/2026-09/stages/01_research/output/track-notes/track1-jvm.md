# SIGNAL #7 (September 2026) — Track 1: JVM semantics and runtime

Researched 2026-10-07. Window: 1–30 Sep 2026. P0 = openjdk.org JEPs, jdk.java.net release notes, bugs.openjdk.org (REST API), github.com/openjdk/jdk. P1 = discovery only. P2 = reaction only.

**Three corrections to the leads, up front:**

1. **The RC was not late.** Tag `jdk-27+35` (= `jdk-27-ga`) sits on commit 815ff4dc32, dated 2026-08-19. The schedule said "Release Candidate Build 2026/08/20". The real story is a **P1 silent-data-corruption bug in C2 found 18 Aug and backed out on 19 Aug, the day before the RC** (see C6). Builds +33 and +34 are the same commit (8106099da0, 29 Jul), which is probably where the "two weeks" reading came from.
2. **JEP 528 left JDK 27 in May, not September.** The owner moved it back to Candidate on 2026-05-21. In September it was **retargeted to JDK 28** (29 Sep) (see C7).
3. **SIGNAL #3 (May) and the May–June LinkedIn edition said "Earliest removal is JDK 29" for JVMCI. That was wrong.** JVMCI was removed in JDK 27: the PR was integrated 2026-05-26 and shipped in GA on 15 Sep. #7 should carry a correction (see C2).

**Past-issue overlap check** (grep over `issues/`): JEP 523, 534 and 528 appear only in the unpublished June draft. The May–June LinkedIn edition mentioned "compact object headers cutting heap use 22%" and "G1 becoming the default everywhere" as feature-freeze news. JVMCI was #3's lead debate. TornadoVM (Llama3 on Maven) was in #5. JEP 541 Intel Mac was in #6. Leyden agent rules (JDK-8387190) were in #5. Valhalla/JEP 401 was in #5. None of the angles below repeat those, except C2, which is deliberately a follow-up to #3.

---

## 1. Candidate register

### C1. Compact object headers shipped as the default with an open regression ticket the vendor accepts
- **Freshness:** NEW_THIS_MONTH. GA on 15 Sep. JDK-8392511 filed 16 Sep. Alignment patch PR #32984 opened 21 Sep. JDK-8386990 last updated 22 Sep.
- **Event date:** 2026-09-15 (GA). Underlying ticket opened 2026-06-19.
- **Source publication dates:** JEP 534 page updated 2026/08/11. JDK-8386990 updated 2026-09-22. Inside.java perf post 2026-09-28.
- **Falsifiable claim:** JDK 27 turns compact object headers on by default while JDK-8386990 is still Open (fix version "tbd", priority P4). That ticket says the 12-byte array base offset under COH causes measurable regressions: crypto benchmarks −1% to −4%, Renaissance-ScalaKmeans −15% to −20%, String micros up to −50%, ArrayCopy micros up to −35%.
- **Primary sources:**
  - https://openjdk.org/jeps/534 (JEP, P0)
  - https://bugs.openjdk.org/browse/JDK-8386990 (JBS, P0)
  - https://bugs.openjdk.org/browse/JDK-8392511 (JBS, P0)
  - https://github.com/openjdk/jdk/pull/32984 (PR, P0)
- **Verification:**
  - Release notes (jdk.java.net/27/release-notes, "Compact Object Headers Are Enabled by Default (JDK-8360700)") confirm the default and that `-XX:-UseCompactObjectHeaders` "is planned for deprecation and removal in a future release".
  - JBS issue links confirm 8386990 "Causes: JDK-8360700" (the JEP 534 implementation).
- **Hard evidence:**
  - JEP 534 benefits (Oracle's own numbers): SPECjbb2015 "22% less heap space and 8% less CPU time"; "reduced by 15%" GC count; JSON parser "10% less time". Amazon runs "hundreds of services in production" with COH (mostly backports to 17/21). SapMachine already defaults to COH.
  - JDK-8386990 (Sergey Kuksenko, Oracle, 19 Jun): the regression list above. Root cause: the first array element is at offset 12, not 16. Roman Kennke (23 Jun): byte/char/short/int/float/Object[] (with coops) start at offset 12 and are 4-byte aligned; long[]/double[] start at 16.
  - Vladimir Kozlov (26 Jun): hand-written crypto intrinsics use unaligned AVX-512 loads, and fixing alignment there "may cause more regression than improvement. -1%..-4% seems more acceptable".
  - Emanuel Peter (1 Jul) questions whether the ScalaKmeans number is statistically significant: "results were already multi-modal in about the same range since JDK26, maybe even JDK25".
  - Tobias Hartmann triaged it P4 on 2 Jul ("disable COH" is the workaround). On 21 Sep he opened PR #32984 "AlignArrayElements": an opt-in flag, false by default, "to diagnose JDK-8386990". The PR is open and WIP.
  - JDK-8392511 (16 Sep): COH costs "~9% score drop" on SERT::LU (2-D double arrays) on a Xeon 8280L. Measured: b23 347690.761 vs 379266.565 without the JEP 534 commit, using `-XX:+UseSerialGC`. Workaround suggested: `ObjectAlignmentInBytes=32`. Kuksenko could not reproduce it on SPECjvm2008 lu on a Xeon 8358.
  - JDK-8385590 (MessageDigest −19%): closed Won't Fix because it appeared only on Apple M1.
- **Trade-off:** Real-world heap footprint wins in the double digits against single-digit (sometimes larger, workload-specific) CPU regressions in array-heavy, vectorised, crypto and string code. Inside.java (28 Sep) only hedges: results "depend heavily on object-size distribution and alignment; an application dominated by large primitive arrays will benefit less." It does not mention the open ticket.
- **Community reaction:**
  - The sharpest exchange is P0 (it happened in JBS). Aleksey Shipilev (26 Jun): "it would be unwise to be spooked by single-digit-% regressions on microbenchmarks, when the real world footprint improvements from COH … are double-digit-%… We have seen projects reporting 70% … smaller memory usage". That 70% is his claim, not verified. On the other side: Kozlov, Kuksenko and Doug Lea, who saw ForkJoinPool regressions after default COH (23 Jun, 23 Jul).
  - Side conflict worth a line: Kozlov (25 Jun) told Kennke that Oracle "never agreed to integrate" 4-byte headers (Lilliput 2) into OpenJDK.
  - HN: nothing specific to compact headers found.
- **Scores:** Freshness 4 / Relevance 5 / Evidence 5 / Stakes 4 / Tension 5 / Originality 5 = **28/30**
- **Slot:** **Debate.** "Default-on with a known regression list": footprint versus array-heavy CPU, argued in public by HotSpot engineers. The reader's action is to benchmark crypto, string and array-heavy paths with `-XX:-UseCompactObjectHeaders` before rollout. Scalac angle: Renaissance-ScalaKmeans is the one named macro workload.

### C2. JVMCI is gone in GA, and GraalVM's published roadmap stays on JDK 25 (plus a correction to #3)
- **Freshness:** MATERIAL_UPDATE. The removal was integrated in May. New in September: it shipped in GA on 15 Sep, and GraalVM 25.4 (22 Sep) is still JDK 25-based, with a calendar of 25.x releases through Feb 2027.
- **Event date:** 2026-09-15 (GA) / 2026-09-22 (GraalVM 25.4).
- **Source publication dates:** CSR JDK-8385105 approved 2026-05-22. PR #30834 integrated 2026-05-26. GraalVM 25.4 release notes 2026-09-22.
- **Falsifiable claim:** JDK 27 contains no JVMCI, no `jdk.graal.compiler` module and no `-XX:+UseGraalJIT`. Every GraalVM release scheduled through 23 Feb 2027 (25.5–25.8) is numbered on the JDK 25 baseline. So a team that depends on the Graal JIT can't upgrade to JDK 27 by swapping in a Graal build from Oracle's published calendar.
- **Primary sources:**
  - https://jdk.java.net/27/release-notes ("Removal of the JVM Compiler Interface (JVMCI) (JDK-8382582)", P0)
  - https://bugs.openjdk.org/browse/JDK-8382582
  - https://bugs.openjdk.org/browse/JDK-8385105 (CSR)
  - https://github.com/openjdk/jdk/pull/30834
  - https://www.graalvm.org/release-notes/25.4/
  - https://www.graalvm.org/release-calendar/
- **Verification:**
  - GitHub graalvm/graalvm-ce-builds release `graal-25.4.4.1.1` (2026-09-22) is titled "GraalVM Community 25 Innovation 4 (graal 25.4.4.1.1, jdk 25.0.4.1.1)".
  - Release notes: "an innovation release, based on OpenJDK 25.0.4.1".
- **Hard evidence:**
  - CSR rationale: "After dissolving Galahad, Graal and Metropolis projects there are no consumers of JVMCI experimental API left in OpenJDK… This is an experiment that has outlived its usefulness."
  - Alan Bateman: "~25 XX options removed but they are all EXPERIMENTAL".
  - JDK-8386450 "Renaissance-ScalaKmeans shows a 20% performance regression with JDK 27-b24 on Linux x64": closed Won't Fix on 10 Jun. Kuksenko: "Removal of JVMCI causes -20% regression on Linux x64. At the same time… +12% on Linux aarch64 and +15% on MacOSX aarch64."
  - Downstream cost, P0 on GitHub: TornadoVM PR #894 (merged 14 Aug) replaced JVMCI with reflection, ASM and Unsafe. PR #1192 (opened 5 Oct) vendors "the 104 JVMCI API files that Graal and TornadoVM use … from OpenJDK jdk-21.0.2+13", renamed to `tornado.meta.*`. TornadoVM 7.0.0 (22 Sep) ships JDK 21/25/26/27 archives.
- **Trade-off:** OpenJDK maintenance velocity against downstream projects that now have to carry the interface themselves (TornadoVM did it; Graal JIT users are pinned to JDK 25). Native Image users are unaffected at build level: GraalVM ships its own JDK.
- **Community reaction:**
  - HN item 48350832 (JBS link, 31 May): 4 points, 2 comments. Thin.
  - No objection from Amazon or Red Hat in the PR #30834 comments (27 issue comments, 39 review comments, all procedural). The "Amazon objects" framing in #3 came from JVM Weekly (P1) and is not visible in the PR.
- **Scores:** Freshness 3 / Relevance 4 / Evidence 5 / Stakes 4 / Tension 4 / Originality 4 = **24/30**
- **Slot:** **Signal** (with an explicit correction line to #3). Reason: our own readers were told "JDK 29 at the earliest". The actionable fact now is "JDK 27 + Graal JIT does not exist on any published roadmap."

### C3. G1 everywhere (JEP 523): who is newly affected, what else moved, and why the "265× slower" post doesn't transfer
- **Freshness:** NEW_THIS_MONTH (GA 15 Sep; Open Liberty beta warning 22 Sep). The Ślusarski article (19 Aug) is BACKGROUND_ONLY, but its HN discussion (1 Sep) is in the window.
- **Event date:** 2026-09-15.
- **Source publication dates:** JEP 523 updated 2026/08/19. Schatzl blog 2026-08-10. Open Liberty blog 2026-09-22. Ślusarski 2026-08-19.
- **Falsifiable claim:** On JDK 27, a JVM started without a GC flag on a machine with **a single CPU or less than 1792 MB of physical memory** now runs G1 instead of Serial (JEP 523 text). Separately, G1's `MinHeapFreeRatio`/`MaxHeapFreeRatio` defaults changed from 40/70 to 0/100, so G1 no longer shrinks or expands the heap after a Full GC based on those ratios.
- **Primary sources:**
  - https://openjdk.org/jeps/523 (P0)
  - https://jdk.java.net/27/release-notes (JDK-8238686 MinHeapFreeRatio; JDK-8227106 IHOP rename)
  - https://bugs.openjdk.org/browse/JDK-8359802 (P0)
- **Verification:**
  - Open Liberty 26.0.0.10 beta (https://openliberty.io/blog/2026/09/22/26.0.0.10-beta.html): "G1 is now the default garbage collector in all environments, including those previously using Serial or Parallel GC, for example, single-CPU or low-memory environme[nts]".
  - InfoQ quotes the same blog: "users running Open Liberty in a constrained environment may experience a different garbage collection behavior".
- **Hard evidence:**
  - The JEP's stated goal is that the metrics "should not degrade significantly". **The JEP publishes no numbers.** Schatzl's blog publishes none either; the fetch summary found no measured G1-vs-Serial comparison.
  - JBS links on JDK-8359802 show small-heap ergonomics work **still Open** at GA: JDK-8367238 "G1: Improve heap region size ergonomics for small heaps", JDK-8367241 "G1: Improve thread sizing ergonomics for small heaps", JDK-8367992 "Card table clearing during commit significantly slows down VM startup", JDK-8368082, JDK-8368083. JMC-8408 "Update Rules to account for G1 being default" is New.
  - `AlwaysActAsServerClassMachine`/`NeverActAsServerClassMachine` obsoleted (JDK-8379665).
  - Inside.java (28 Sep): "This is primarily a consistency change, not a claim that G1 suits every workload."
  - Ślusarski: G1 139,019.174 µs/op vs ParallelGC 525.537 µs/op (265×) on **JDK 25.0.3** Corretto, M4 Max, humongous 1M-element Object[]. On **JDK 26** (JEP 522's second card table removes the fence), G1 humongous is 1,121 ms/op, down from 108,811.
- **Trade-off / the honest hook:** The teams newly put on G1 by JEP 523 get it **on JDK 27, which already has JEP 522**, so they don't inherit the 265× pathology. The 265× number is a **JDK ≤25 LTS** problem for anyone already on G1 (≥2 CPUs and ≥1792 MB). Newly affected small containers trade Serial's simplicity for G1's barrier and native-memory overhead. No public numbers say how much.
- **Community reaction:**
  - **HN 49517958 "Why is Arrays.fill 265 times slower on G1GC?" (posted 2026-09-01, in the window): 31 points, 27 comments.** This is where JEP 523 gets argued directly:
    - cogman10: "I don't really understand why G1 is being pushed so hard… Even the serial collector isn't bad for things like a containerized environment, yet G1 replaces it by default now". Also says G1's sweet spot is large heaps and that below 2–10 GB Parallel does better.
    - pron (Ron Pressler, Oracle) replies: "Are you talking about G1 in JDK 25, JDK 26, or JDK 27?… G1 has been made the default even for small machines in JDK 27 because of some very recent changes". His practical lessons: upgrade the JDK, and don't pool objects.
    - Side argument: several commenters say the post reads AI-written (hyperpape, zbentley); others disagree. The author's page itself says one table was AI-generated.
  - This thread gives the Ślusarski piece a September reaction hook. The engagement numbers are from the Algolia API on 2026-10-07.
  - HN 49289101 (Schatzl blog, 13 Aug): 68 points, 35 comments. One commenter (hylaride) raised serverless/Lambda pause-between-invocations memory creep. pron pointed to automatic heap sizing coming (JEP 546 link).
  - HN 49712041 ("Java 27", 15 Sep): 351 points, 439 comments. Mostly cadence and "upgrade is painless with Spring" talk; one joke about OOM after the switch. No concrete regression report.
- **Scores:** Freshness 4 / Relevance 5 / Evidence 4 / Stakes 3 / Tension 4 / Originality 4 = **24/30** (Tension raised from 3 after the HN 49517958 G1-vs-Serial/Parallel exchange)
- **Slot:** **Notes from the Trenches**, framed as "check sidecars, CLIs, batch jobs and K8s pods with <2 vCPU or <1792 MB; pin `-XX:+UseSerialGC` if you measured Serial better; and the 265× post is your JDK 25 problem, not your JDK 27 one." Ślusarski is independent (not a competitor) and can go in Top Resources.

### C4. JEP 544 "Ahead-of-Time Code Compilation" targeted to JDK 28: Leyden's answer to Native Image, with two silent-fallback traps
- **Freshness:** NEW_THIS_MONTH. Candidate 10 Sep → Proposed to Target 18 Sep → Targeted 28 Sep.
- **Event date:** 2026-09-28 (Targeted).
- **Source publication dates:** JEP 544 updated 2026/09/29. HN thread 2026-09-10.
- **Falsifiable claim:** In JDK 28 the existing AOT cache workflow (`-XX:AOTCacheOutput` / `-XX:AOTCache`) will also store C1/C2-compiled native code by default. That code is used **only if training and production run on the same CPU architecture and features and the same GC**. Otherwise HotSpot warns and silently falls back to JIT, keeping only classes and profiles.
- **Primary sources:**
  - https://openjdk.org/jeps/544 (P0)
  - https://bugs.openjdk.org/browse/JDK-8335368 (status history, P0)
- **Verification:** JBS changelog: `mr` Submitted→Candidate 2026-09-10; `jrose` Candidate→Proposed to Target, fix version 28, 2026-09-18; `mr` →Targeted 2026-09-28. InfoQ roundups (P1) agree.
- **Hard evidence:**
  - JEP figures, measured on a JDK 28 EA build on a 2-core Linux/x64 box: AOT cache without AOT code cuts startup "around 50% to 70%"; with AOT code "around 65% to 80%".
  - javac benchmark: about 30% from the cache alone, plus about 45% more from AOT code, "for a total of about 75%".
  - Non-goals: no AOT-only mode, no cross-compilation. AArch64 and x64 only.
  - Example given in the JEP: code built on an AVX-512 machine won't run on a CPU without it.
- **Trade-off:** Keeps JIT agility and full dynamic-Java compatibility, unlike Native Image's closed world, but needs representative training runs. CI and production must also match on CPU features and GC. Original angle: JEP 523 removes one source of GC mismatch (a small CI runner used to get Serial while production got G1). The CPU-feature mismatch remains.
- **Community reaction:**
  - HN 49647404: 105 points, 74 comments. cogman10: training runs are "a pretty hard burden to setup. The tooling for doing these sorts of training runs doesn't really exist." java-man wants an AOT-only/native mode. rerdavies asks why not compile at install time.
  - Separate data point on the "Java 27" thread (p2detar): a team moving to containers hasn't tried Leyden because of the warm-up and training requirement.
- **Scores:** Freshness 5 / Relevance 5 / Evidence 4 / Stakes 3 / Tension 3 / Originality 4 = **24/30**
- **Slot:** **Signal**, or the second half of a Debate on "JIT plus AOT cache vs Native Image now that Graal is off the JDK train" (pairs with C2). Reason: it's a September status change with a concrete operational constraint (CPU features and GC parity between CI and production).

### C5. Post-quantum hybrid TLS on by default (JEP 527), and the less-noticed TLS changes in the same release
- **Freshness:** NEW_THIS_MONTH (GA 15 Sep).
- **Event date:** 2026-09-15.
- **Source publication dates:** JEP 527 updated 2026/08/17. Release notes.
- **Falsifiable claim:**
  - JDK 27 TLS 1.3 clients put `X25519MLKEM768` first and send **two key shares (X25519MLKEM768 + x25519)** in ClientHello with no code change.
  - Separately, TLS 1.3 key agreement now asks the provider for a `Generic` key algorithm, so **third-party JCE providers that don't support Generic keys fail with SSLHandshakeException "Could not generate secret"**. The workaround is `-Djdk.tls.t13KeyDerivationAlgorithm=TlsPremasterSecret`.
- **Primary sources:**
  - https://openjdk.org/jeps/527 (P0)
  - https://jdk.java.net/27/release-notes (JDK-8314323, JDK-8377550, JDK-8373426, JDK-8372526, JDK-8044609)
- **Verification:** The release notes repeat the JEP's default list and the opt-out (`jdk.tls.namedGroups`). Classmethod tested PQ TLS on Corretto 27 GA (dev.classmethod.jp, P1; not fetched).
- **Hard evidence:**
  - Default groups: X25519MLKEM768, x25519, secp256r1, secp384r1, secp521r1, x448, ffdhe2048/3072/4096. ffdhe6144 and ffdhe8192 were removed from the defaults (JDK-8373426).
  - zlib certificate compression is on by default (JDK-8372526).
  - `javax.net.debug` invalid combos are now silently ignored (JDK-8044609), so `-Djavax.net.debug=verbose` alone does nothing.
  - Performance: ML-KEM "+46–48%" and ML-DSA "+38–74%" on AVX-512 (release note JDK-8384353). X25519 handshake without resumption +14% (x64) and +17% (AArch64) (JDK-8378893).
- **Trade-off:** Harvest-now-decrypt-later protection against a bigger ClientHello. The JEP itself says nothing about size or middleboxes. The "≈1.2 KB key share, ClientHello spans two segments, middleboxes break" claim comes only from P2/vendor blogs (encryptionconsulting.com, rabinarayanpatra.com).
- **Community reaction:** None found specific to JDK 27. A JBS text search for X25519MLKEM768 / MLKEM / "hybrid key exchange" since 15 Aug returned **0 issues**.
- **Scores:** Freshness 4 / Relevance 4 / Evidence 3 / Stakes 3 / Tension 2 / Originality 3 = **19/30**
- **Slot:** **In the Know.** "PQ is on; if you use an HSM or third-party JCE provider, test TLS 1.3 handshakes (JDK-8377550); if you pin groups behind old middleboxes, `jdk.tls.namedGroups` is the switch." Not a Debate: no documented breakage.

### C6. Four weeks before GA: a C2 bug that silently corrupted copied byte arrays under compact headers, found by a user testing EA builds
- **Freshness:** BACKGROUND_ONLY (18–19 Aug). It is the true version of the "RC delayed by a bug" lead.
- **Event date:** 2026-08-18 (reported) / 2026-08-19 (backout integrated into `jdk27`, tagged `jdk-27+35` = GA).
- **Source publication date:** JBS 2026-08-18.
- **Falsifiable claim:** JDK 27-ea+24 to the pre-RC builds had a P1 C2 bug (regression from JDK-8373591). A C2-compiled caller that inlined `Arrays.copyOfRange` after `StandardCharsets.UTF_8.encode` could leave **bytes 12–15 of the new array as garbage** on x64 Linux. `-XX:-UseCompactObjectHeaders` or `-XX:-ReduceBulkZeroing` avoided it. The change was backed out the day before the RC build and is not in GA.
- **Primary sources:**
  - https://bugs.openjdk.org/browse/JDK-8390546
  - https://bugs.openjdk.org/browse/JDK-8390590 (backout, labels `jdk-rc-fix`, `jdk27-fix-yes`, P1)
  - GitHub `openjdk/jdk` branch `jdk27` commits 2026-08-19
- **Verification:** The commit list on branch `jdk27` shows "8390590: [BACKOUT] C2: Fix the memory around some intrinsics nodes" and "8390591: Add regression test" on 2026-08-19, then the `jdk-27+35` tag on the same SHA. JDK 27.0.1 also lists the backout (JDK-8391188, P1).
- **Hard evidence:** Filed "on behalf of Lorenzo Dematte". His team's integration tests round-tripped strings and saw diffs "on the first 4 bytes". Tobias Hartmann's ILW: "Incorrect result with C2 compiled code, reproducible with simple test" = P1. Hartmann's root cause: memory-alias types pointed at the array header, not the payload, affecting the `_encodeAsciiArray`, `_encodeISOArray` and `_encodeByteISOArray` intrinsics. A redo is JDK-8390617. The reporter's employer is **not verified**; don't name one.
- **Trade-off:** Good evidence for "run your integration tests on EA builds". Also shows that COH changes array layout assumptions in C2 intrinsics, which links to C1.
- **Community reaction:** The original thread is on hotspot-compiler-dev (mail.openjdk.org, not fetched). No HN thread found.
- **Scores:** Freshness 2 / Relevance 4 / Evidence 5 / Stakes 4 / Tension 3 / Originality 4 = **22/30**
- **Slot:** A **sidebar inside C1 (Debate)** or a Trenches mini-case. Not standalone, because it falls outside the window.

### C7. JEP 528 (post-mortem crash analysis with jcmd): pulled from 27 over Attach API design, retargeted to 28 in September
- **Freshness:** MATERIAL_UPDATE. PR reworked 28 Sep; fix version set back to 28 on 29 Sep.
- **Event date:** 2026-09-29.
- **Source publication dates:** JEP page updated 2026/09/29. PR #31011 updated 2026-10-02.
- **Falsifiable claim:** JEP 528 reached Proposed to Target for JDK 27 (label `jdk27-ptt-2026-05-26`), but the owner moved it back to Candidate on 2026-05-21 before the PTT deadline. The PR stalled on Attach API design review: Alan Bateman (19 May) wanted a separate AttachProvider rather than overloading `attach()`. On 28 Sep the owner pushed a version with a separate CoreDumpAttachProvider, and on 29 Sep set the fix version to 28.
- **Primary sources:**
  - https://openjdk.org/jeps/528
  - https://bugs.openjdk.org/browse/JDK-8328351 (changelog)
  - https://github.com/openjdk/jdk/pull/31011
- **Verification:** The JBS changelog shows each transition with author and date. Kevin Walls on the PR (7 Jul): "finalizing the Attach API changes, which is the block here". On 28 Sep: "(1) Separate AttachProvider for core files."
- **Hard evidence:** jcmd has 57 commands for a live JVM, "26 are relevant and available in the post-mortem environment" (JEP). Linux and Windows only. The PR has 32 issue comments and 97 review comments and is still open.
- **Trade-off:** One tool for live and post-mortem diagnostics, instead of the "brittle and dated" Serviceability Agent/jhsdb. The cost is new Attach API surface and an ambiguity: a core file named `123` versus PID 123.
- **Community reaction:** None found on HN.
- **Scores:** Freshness 3 / Relevance 3 / Evidence 5 / Stakes 2 / Tension 2 / Originality 3 = **18/30**
- **Slot:** **In the Know** (one line, folded into the JDK 27 GA item). Useful as a "Proposed to Target ≠ shipped" example.

### C8. JDK 28 shaping in September: ZGC startup and heap sizing (JEPs 545/546), Structured Concurrency final (JEP 543)
- **Freshness:** NEW_THIS_MONTH. 545 and 546 became Candidate on 21 Sep. 543 became Candidate on 8 Sep and Proposed to Target on 1 Oct.
- **Event dates:** 2026-09-08 / 2026-09-21 / 2026-10-01.
- **Falsifiable claim:** JEP 546 "Adaptive Heap Sizing for ZGC" and JEP 545 "Faster Startup and Warmup with ZGC" are Candidates with no release. JEP 543 Structured Concurrency (final) is Proposed to Target for 28 after seven previews.
- **Primary sources:**
  - https://openjdk.org/jeps/543 (P0)
  - https://openjdk.org/jeps/545 (P0)
  - https://openjdk.org/jeps/546 (P0)
  - JBS JDK-8389757 / JDK-8329758 / JDK-8377305 changelogs (P0)
- **Hard evidence:** Status transitions only. JEP bodies were not read in detail.
- **Trade-off:** Not assessed.
- **Community reaction:** HN 49922076 (JEP 545): 1 point, 0 comments.
- **Scores:** Freshness 4 / Relevance 3 / Evidence 3 / Stakes 2 / Tension 1 / Originality 2 = **15/30**
- **Slot:** **In the Know** (one line), or reject if space is tight.

---

## 2. Conflict findings (what breaks or is contested)

1. **COH default vs array alignment (open).** JDK-8386990, Open, fix "tbd". Regression list: crypto −1..−4%, ScalaKmeans −15..−20%, String micros to −50%. Shipilev vs Kozlov/Kuksenko/Lea, all in JBS. JDK-8392511 (16 Sep): SERT LU −9%. PR #32984 (21 Sep): opt-in `AlignArrayElements`, a diagnostic only. Links: https://bugs.openjdk.org/browse/JDK-8386990, https://bugs.openjdk.org/browse/JDK-8392511, https://github.com/openjdk/jdk/pull/32984
2. **COH correctness bugs in neighbouring code.** Generational Shenandoah's remembered-set scan used non-COH-aware size accessors. Two fixes: JDK-8391488 (2 Sep) and JDK-8393229 (30 Sep, "We missed this usage"). Affects version 25. Several JFR OldObject + ZGC + COH test failures were backported to 17/21/25 (JDK-8392266/8392270/8392346). This matters for anyone who backports COH to LTS (Amazon does).
3. **JVMCI removal costs.** ScalaKmeans −20% on Linux x64 was accepted as Won't Fix (JDK-8386450). Caveat: JDK-8386990 attributes a ScalaKmeans −15..−20% to COH as well, both measured around b23/b24, and Emanuel Peter doubts significance. **Do not print a single cause for the ScalaKmeans number.** TornadoVM had to vendor 104 JVMCI API files (PR #1192). There is no Graal JIT on JDK 27 on any published GraalVM calendar.
4. **G1-by-default in small containers.** No published G1-vs-Serial numbers, and small-heap ergonomics tickets still Open at GA (JDK-8367238, 8367241, 8367992). Open Liberty warns of "different garbage collection behavior". Heap-ratio defaults moved to 0/100 (JDK-8238686), which changes post-Full-GC shrink behaviour. **No user-reported breakage found** in JBS (regression + affectsVersion 27 + created Sep: 7 issues, none GC).
5. **TLS.** No JDK 27 PQ breakage found (0 JBS hits). The real compatibility risk in the release notes is JDK-8377550: the Generic key algorithm breaks third-party JCE providers ("Could not generate secret"). Middlebox/ClientHello-size risk exists only in vendor and P2 sources.
6. **Other upgrade breakers in the release notes:**
   - `ThreadPoolExecutor.finalize()` removed: subclasses calling `super.finalize()` may no longer compile.
   - `-noverify` / `-Xverify:none` removed, no replacement. This affects old agent setups that rely on them.
   - HttpServer switched to path-prefix matching (`/foo` no longer matches `/foobar`).
   - JSON thread dump fields changed from strings to numbers.
   - `UseCompressedClassPointers` is obsolete.
   - `-XX:InitiatingHeapOccupancyPercent` renamed to `-XX:G1IHOP` (alias deprecated).
   - VFORK launch mechanism removed.
   - GZIPInputStream read-ahead reverted to pre-23 behaviour.
7. **Loom-adjacent regression (minor):** JDK-8392202 (11 Sep, P3, Open): `ForkJoinPool.shutdownNow()` can fail to stop the pool after JDK-8385830. Affects 27 and 28. Viktor Klang flags a Javadoc conflict.
8. **Official perf messaging vs JBS.** Inside.java's 28 Sep "Performance Improvements in JDK 27" (Minborg, Redestad) mentions alignment only as a hedge and doesn't link JDK-8386990.

## 3. Rejected items and why

- **Ślusarski "Arrays.fill 265× slower on G1" as its own item.** Published 19 Aug, outside the window. The JEP 523 hook doesn't hold, because newly affected JDK 27 users already have JEP 522. It goes into C3 as context and into Top Resources as a JDK 25 LTS warning.
- **Ślusarski "JDK 26 and SIMD operations" (5 Sep).** In the window, independent, solid numbers. But JDK 26 only, with no JDK 27 or COH link. At most Top Resources.
- **GraalVM 25.4 feature list** (PullThroughPhi, Native Image StringBuilder outlining, etc.): routine churn. The only material point (still JDK 25-based) is folded into C2.
- **TornadoVM 7.0 as a release:** routine, and #5 already featured TornadoVM. Its JVMCI-vendoring PRs are used as evidence in C2. Not a competitor (beehive-lab, University of Manchester).
- **Intel Mac builds:** covered in #6 (JEP 541). Verified follow-up only: jdk.java.net/27 lists Linux AArch64/x64, macOS AArch64 and Windows x64; the Adoptium API for 27/mac returns aarch64 only. At most a one-line follow-up.
- **JEP 536 JFR redaction:** delivered, low tension. In the Know one-liner if needed (`jdk.SystemProcess` no longer emits command lines; JDK-8384164).
- **Quarkus 3.39.5 CVE batch:** framework/security track, not JVM runtime. Pass to the relevant track. The "AI discovers a lot of CVEs" quote was not verified on quarkus.io.
- **Phoronix "JDK 8 through OpenJDK 27" benchmarks (24 Sep, HN 4 points):** not fetched, not verified.
- **Valhalla:** #5 covered JEP 401. The September JBS activity is Valhalla C2 crash fixes (lworld), with no status change. Reject.
- **Competitor check:** none of the candidates are VirtusLab, SoftwareMill or Typelevel projects. JVM Weekly (VirtusLab author) was used only for discovery and isn't cited as evidence.

## 4. Open fact-check questions

1. **JEP 523 in containers:** is "less than 1792 MB of physical memory" evaluated against the cgroup memory limit when container support is active? It probably is (HotSpot's `os::physical_memory()` is container-aware), but this was not verified from source. Check `src/hotspot/share/runtime/os.cpp` / `gc/shared/gcConfig.cpp` history around JDK-8383856 before printing "K8s pods under 1792 MB".
2. **ScalaKmeans attribution:** COH (JDK-8386990) or JVMCI removal (JDK-8386450), both about −20%? Ask whether a JDK 27 GA vs 26 ScalaKmeans comparison exists. Until then, say "flagged by Oracle's perf team in two tickets, cause disputed".
3. **Shipilev's "70% smaller memory usage" claim** (JBS comment): no named project. Quote it as his claim or drop it.
4. **X25519MLKEM768 key share size:** the ~1.2 KB figure comes only from P2 blogs. For a P0, cite draft-ietf-tls-ecdhe-mlkem / FIPS 203 (ML-KEM-768 encapsulation key 1184 bytes + X25519 32 bytes). Not fetched.
5. **Does any Oracle GraalVM or GraalVM CE plan include a JDK 27 or 29 base?** The calendar shows 25.x through Feb 2027. Check whether Oracle has said anything about the next base (the 28 Sep 2025 "Detaching GraalVM from the Java Ecosystem Train" blog was not fetched in this pass).
6. **JDK-8390546 reporter:** "Lorenzo Dematte". Employer not verified; don't attribute.
7. **Open Liberty quote wording:** the InfoQ-quoted sentence ("may experience a different garbage collection behavior") was not seen in my direct regex fetch, which cut off mid-sentence. Re-fetch the full paragraph before quoting.
8. **MinHeapFreeRatio 0/100:** does this reduce memory returned to the OS for small-container G1 users, or does periodic or uncommit logic still return it? Schatzl's blog gives no metric. Needs a P0 statement before claiming an effect on RSS.
9. **HN "Java 27" thread engagement** (351 points / 439 comments) was read from the Algolia API on 2026-10-07. Re-check if quoting.

## 5. URLs fetched

**Fetched successfully (curl / WebFetch / gh API):**
- https://openjdk.org/projects/jdk/27/
- https://openjdk.org/jeps/523, /527, /528, /534, /536, /543, /544, /545, /546, /539
- https://jdk.java.net/27/release-notes
- https://jdk.java.net/27/
- https://bugs.openjdk.org/rest/api/2/issue/JDK-8328351 (changelog)
- JBS REST: JDK-8382582, JDK-8359802, JDK-8361187, JDK-8386450, JDK-8385105, JDK-8390590, JDK-8390546, JDK-8386990, JDK-8385590, JDK-8392511, JDK-8391488, JDK-8393229, JDK-8392202, JDK-8335368, JDK-8389757, JDK-8329758, JDK-8377305
- JBS REST JQL searches: regressions affecting 27 created in Sep; COH text search; PQ text search; P1/P2 affecting 27 in Sep; fixVersion 27.0.1 P1/P2
- GitHub API: openjdk/jdk PR #31011 (plus comments), PR #30834 (plus comments), PR #32984; tags jdk-27+32..+35, jdk-27-ga; branch `jdk27` commits since 2026-07-28; search for 8328351 and 8382582
- GitHub API: graalvm/graalvm-ce-builds releases (incl. tag graal-25.4.4.1.1)
- GitHub API: beehive-lab/TornadoVM releases v7.0.0/v7.0.1/v7.1.0/v7.2.0; PRs/issues #894, #1192, #957
- https://www.graalvm.org/release-notes/25.4/
- https://www.graalvm.org/release-calendar/
- https://api.adoptium.net/v3/assets/latest/27/hotspot?os=mac
- https://krzysztofslusarski.github.io/ (index)
- https://krzysztofslusarski.github.io/2026/08/19/g1barrier.html
- https://krzysztofslusarski.github.io/2026/09/05/simd.html
- https://tschatzl.github.io/2026/08/10/jdk27-g1-serial-parallel-gc-changes.html
- https://inside.java/2026/09/28/performance-update-jdk27/
- https://www.infoq.com/news/2026/09/java-news-roundup-sep21-2026/
- https://openliberty.io/blog/2026/09/22/26.0.0.10-beta.html (partial text match)
- HN Algolia search API. First pass used the wrong lower bound (1756684800 = Sep 2025); every hit was then date-checked by `created_at` and 2025 items discarded. **Re-run with `created_at_i>1788220800,created_at_i<1791417600`** for: JDK 27, Java 27, JVMCI, compact object headers, JEP 544, Leyden, GraalVM, G1, post-quantum Java, TornadoVM, Arrays.fill. The re-run surfaced one new in-window item, HN 49517958 (Arrays.fill, 1 Sep, 31 points / 27 comments). JVMCI, compact object headers and post-quantum Java: 0 in-window stories.
- HN Algolia items 49712041, 49647404, 49289101 (Aug, background), 49517958
- Local: ~/Documents/signal-newsletter-generator/issues/ (grep, read-only)
- WebSearch (results lists only, pages not opened): JDK 27 PQ TLS middlebox; JDK 27 regression COH/G1; GraalVM 25.4 JVMCI; Open Liberty beta; Quarkus 3.39.5

**Failed or not attempted:**
- github.com/openjdk/jdk27: 404 (no separate stabilization repo; the branch `jdk27` in openjdk/jdk was used instead)
- mail.openjdk.org: not attempted (known 403); the hotspot-compiler-dev thread for JDK-8390546 is unread
- infoq.com sep07 and sep28 roundups: not fetched (coordinator-supplied; JEP statuses verified via JBS instead)
- quarkus.io/blog/quarkus-3-39-5-released: not fetched
- dev.classmethod.jp Corretto 27 PQ article, encryptionconsulting.com, rabinarayanpatra.com: search snippets only
- blogs.oracle.com "Detaching GraalVM from the Java Ecosystem Train": not fetched
- phoronix.com JDK 8–27 benchmark: not fetched
