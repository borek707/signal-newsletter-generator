# SIGNAL September 2026 — Brief (Issue #7)

## 1. Issue number and publish target

Issue #7. Verified on scalac.io 2026-10-07: the last live issue is #6 (August, post 34091). No September issue exists yet.

Research window: **1–30 September 2026.** Items from 1–7 October can go into Today / In the Know only if they change a September story.

Publish target: **to decide.** Two realistic options:
- **Before Scala Days Berlin (12–13 Oct).** Five working days for the full pipeline. Tight, and only worth it if the issue gets promoted at the event.
- **Week of 19 Oct**, same mid-month rhythm as #6 (14 Sep). Lets the issue reference Scala Days as an upcoming event in October rather than rushing it.

## 2. Main theme / hook

Working hypothesis, to confirm in research. Two candidates:

**A. The upgrade is the incident.** September moved defaults under running systems. JDK 27 (GA 15 Sep) makes G1 the default everywhere, turns compact object headers on by default, enables post-quantum hybrid key exchange in TLS 1.3 with no code change, and removes JVMCI and the Graal JIT from HotSpot. Scala 3.9 LTS (3 Sep) exposes that lazy vals compiled with Scala 3.0–3.7 still call `sun.misc.Unsafe`, and that scala-reflect runtime reflection can fail on the new stdlib (Apache Spark is the known casualty). Neither release is a rewrite. Both break at the boundary nobody owns: the dependency you did not compile, the GC barrier you did not write.

**B. Types as the guardrail for agents.** Odersky's "Tracked Capabilities for Safer Agents" argues for capture checking as the way to limit what agent-written code can touch. TypeSafe AI's Jev (typed questions instead of generated text) reached the JVM through community SDKs and a LangChain4j PR within days, and the naming fight (JudgeModel vs DecisionModel) is the real story. Thinner on production evidence than A.

Recommendation: **A as the spine**, B as the Debate. A has P0 sources (JEPs, release notes, release announcements) and direct migration impact for the CTO reader.

## 3. Candidate architecture debates

1. **Can the type system be the agent sandbox?** Odersky's capability tracking (compile-time: the code cannot reference a capability it was not given) against runtime isolation (containers, network policy, credential scoping). #5's lead story was an agent escaping a sandbox through ten runtime doors, so there is a natural callback. **Needs a credible opposing voice in research**: someone arguing compile-time guarantees do not survive reflection, FFI, shell-outs or generated code. If only one side has substance, demote to Signal per `newsletter-structure.md`.
2. **Durable execution inside the job library vs. a dedicated engine.** JobRunr v9 ships `runStepOnce` steps (charge-card runs once across retries). Netflix published "Conductor: The Next Chapter" (21 Aug) on its internal fork. Real tension: one less piece of infrastructure vs. the recovery semantics Temporal-class engines were built for. **Overlap risk:** #6 had Temporal in Today and #5 considered a Postgres-as-orchestrator debate. Only take this if research finds a fresh opposing argument, not a rerun.
3. **Typed decision models vs. LLM-as-judge.** Jev is invite-only and the evidence is mostly demos, including JVM Weekly's own warning that the demos look too good. Likely Signal or In the Know, not Debate.

## 4. Candidate trenches stories

1. **Arrays.fill 265× slower on G1** (Krzysztof Ślusarski, 19 Aug). The G1 write barrier (≈20 instructions, a memory fence on the slow path) against ParallelGC's two. Fixes are concrete: `arraycopy` doubling, null fill, JEP 522's second card table on JDK 26. **Freshness problem:** published in August. It becomes timely because JDK 27 makes G1 the default in every environment (JEP 523), so teams on ParallelGC in small containers will meet this barrier for the first time. Needs a `MATERIAL_UPDATE` justification or it cannot carry Trenches. Caveat from the author: measured on Apple M4 Max, numbers differ on server x86.
2. **Firebase global outage** (The Pulse, 1 Oct). Pragmatic Engineer piece is paywalled, so it can only point at the story. **Needs Google's own incident report (P0)** before it can carry anything.
3. **DoorDash's toolbox for AI agents** (ByteByteGo, 30 Sep). Chase the DoorDash engineering post it is based on, check date and whether it contains failure modes or only architecture.
4. **Box: Gradle for a Scala monorepo with 360+ modules.** Migration story, but check the date, and check overlap with #6's Metals v2 monorepo lead.

**Research priority:** a real September production incident with a published fix. None of the four is a clean fit yet.

## 5. Candidate signals (8, narrow to 3)

1. **JDK 27 GA (15 Sep), 9 JEPs.** PQ hybrid TLS by default (JEP 527), G1 default everywhere (JEP 523), compact object headers by default (JEP 534), JFR in-process redaction (JEP 536). Plus from the release notes: JVMCI and Graal JIT removed, no Intel Mac builds from Oracle or Adoptium (follow-up to #6's JEP 541 item).
2. **JEP 528 did not ship despite "Proposed to Target".** Small but on-brand: it is the state-ladder rule from `fact-check-rules.md` happening in public. Could fold into item 1.
3. **Scala 3.9 LTS (3 Sep).** SIP-71 `into` stable, Scala.js stable WebAssembly backend, 3.3 LTS gets one more year. Migration impact: Unsafe-based lazy vals in old dependencies, scala-reflect breakage on 3.8+ stdlib (Spark), and 3.10 will stop finding implicits in inaccessible companions (~20 community-build projects break).
4. **sbt 2.1.0 beta and the sbt plugin ecosystem push** (scala-lang.org, 16 Sep).
5. **GraalVM 25.4 after JVMCI left HotSpot.** What "Graal" means for a JVM shop now. Check scope before claiming anything.
6. **JobRunr v9 durable steps.** Either Signal or part of Debate 2.
7. **Kotlin 2.4.20, Groovy 6.0 GA, Gradle 9.8, LangChain4j 1.20, TornadoVM 7.0, Ktor 3.6.** Routine churn, In the Know unless one has migration impact.
8. **Kafka: nothing yet.** Get Kafka-Nated has no September Espresso in the feed. Research must check Kafka releases, the KIP index and dev@kafka directly. An issue with zero Kafka is fine if September had nothing, but it has to be checked, not assumed.

## 6. Known events / constraints

- **Competitors (`scalac-tone-of-voice.md`):** VirtusLab, SoftwareMill, Typelevel. This month's sources are full of VirtusLab work: Sloth (bytecode rewriter for the Unsafe lazy vals), tulip, VirtusLab Scala Stack, Besom, the Scala/WASM post. Do not feature or credit them. Scala 3.9 LTS itself is a scala-lang release and is fine to cover; describe the Unsafe problem and its fixes without naming Sloth as the answer. Typelevel Traverses Europe goes nowhere. Note that JVM Weekly's author works at VirtusLab; it stays a P1 discovery source, never the sole evidence.
- **Scala Days Berlin 12–13 Oct**, Scalac is present (and runs the 12 Oct roundtable). Possible mention in Footer or Today, not as filler content.
- **Do not reuse:** #5 (HF agent intrusion, Valhalla, Meerkat consensus), #6 (Metals v2, Netflix service topology, Gradle Isolated Projects, JEP 541, A2A, Temporal/LangGraph).
- **Sources checked so far (feed + issue text, not yet scored):** JVM Weekly vol. 190–194, This Week in Scala 7 Sep – 5 Oct, ByteByteGo and Pragmatic Engineer September feeds, Get Kafka-Nated (last: August). **Not checked:** InfoQ Software Architects' Newsletter, InfoQ Java roundups, r/scala, r/apachekafka, HN, engineering blogs, `/last30days`.
- **Cleanup carried over:** `cover: ./cover.png` dangles in both #5 and #6. Decide this time whether the cover lives in the repo or only in WP.

## 7. Standard or special edition

Standard monthly issue.
