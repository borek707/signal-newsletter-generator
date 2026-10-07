# SIGNAL #7 (September 2026), Track 2: Scala / Kotlin / concurrency / build tooling / ecosystem migration

Researched 2026-10-07. Window: 1–30 Sep 2026, plus 1–7 Oct where it changes a September story.
P0 = primary source (scala-lang.org, GitHub, Apache JIRA, openjdk.org, the author's own post). P1 = newsletter used for discovery only. P2 = social reaction.
"Verified locally" means I ran it myself with scala-cli on this machine. The JDK was Temurin/Coursier JDK `27+35` (GA build). Scratch files are in `signal7-research/lazytest`, `t39`, `t39r`.

**What I changed from the brief, up front:**
- The Odersky "Tracked Capabilities for Safer Agents" post is dated **27 Jul 2026**, not September. It is BACKGROUND_ONLY. I found no credible voice in the window arguing directly against type-level capability tracking. Verdict: it does not hold up as a two-sided Debate (see §2).
- The Unsafe lazy-val question is settled empirically. **On JDK 27 GA, Scala 3.0–3.7 lazy vals only print a warning and keep working.** They throw only when you pass `--sun-misc-unsafe-memory-access=deny`. The 3.9 announcement is right. Secondary sources that say "JDK 26 throws by default" are repeating JEP 471's *plan* language, which has not shipped.
- The Box Gradle post is dated **16 Sep 2026** (from the sitemap `lastmod` and the page's embedded epoch 1789570800). It is in window.
- **Scala 3.10.0 artifacts went up on Maven Central on 4 Oct** (git tag 2026-10-04, no GitHub release or announcement yet). This makes the "3.10 drops inaccessible companion implicits" breakage current rather than future.
- Brief correction for another track: JDK 27 *did* remove JVMCI and `-XX:+UseGraalJIT`, but **through JDK-8382582 with no JEP**. It is not on the openjdk.org/projects/jdk/27 feature list. Cite the bug or the Oracle release notes, not "a JEP".

---

## 1. Candidate register

### C1. Scala 3.9 LTS: you are on JDK 27 and the warning comes from a jar you never compiled
- **Freshness:** NEW_THIS_MONTH
- **Event date:** 3.9.0 artifacts on Maven Central 26 Aug 2026 (SethTisue, contributors thread #26). Official release announced 3 Sep 2026.
- **Source publication date:** 3 Sep 2026 (scala-lang.org/news/3.9/, author Wojciech Mazur, VirtusLab; this is a scala-lang release and fine to cover).
- **Falsifiable claim:** A Scala 3.3-compiled lazy val, run on JDK 27 GA, prints `WARNING: sun.misc.Unsafe::objectFieldOffset has been called by scala.runtime.LazyVals$` and still runs. With `--sun-misc-unsafe-memory-access=deny` it fails in the class initialiser with `UnsupportedOperationException: objectFieldOffset at scala.runtime.LazyVals$.getOffsetStatic`. The same code compiled with Scala 3.9.0 runs clean under `deny`.
- **Primary sources:**
  - https://www.scala-lang.org/news/3.9/ (P0, release announcement). Verbatim: "That API is implemented with sun.misc.Unsafe, which was terminally deprecated in JDK 24. Under JDK 26 it only prints a warning at runtime; once it is removed in a future JDK, the affected code stops working altogether. Compiling with Scala 3.8 or later is not enough to escape this, because any dependency published with the old lazy vals brings the problem back."
  - https://openjdk.org/jeps/471 (P0, JEP). The plan reads "Phase 3, throwing exceptions by default, in JDK 26 or later". It also says "deny will be the default value in phase 3. It will be possible in phase 3 to revert the value from deny to warn … It will not be possible to use allow to avoid the warning."
  - https://openjdk.org/projects/jdk/26/ and https://openjdk.org/projects/jdk/27/ (P0). Neither feature list contains an Unsafe-deny JEP. JDK 27 GA was 15 Sep 2026.
- **Verification (verified locally on JDK 27+35):**
  - Scala 3.3.6 with default flags: warning, then `computed`.
  - Scala 3.3.6 with `--sun-misc-unsafe-memory-access=deny`: `UnsupportedOperationException`, stack through `scala.runtime.LazyVals$.getOffsetStatic(LazyVals.scala:172)` and `Holder$.<clinit>`.
  - Scala 3.3.6 with `=allow`: silent and works.
  - Scala 3.9.0 with `deny`: works. This confirms the 3.8+ VarHandle path.
  - **Resolution of the "warning vs failure" disagreement:** the announcement is correct. JDK 26 and 27 both default to warn. Phase 3 (deny by default) is still future, and its JDK is unnamed. Web-search summaries saying "JDK 26 flips to deny" paraphrase JEP 471's 2024 plan and are wrong about what shipped.
  - Caution: the WebFetch summariser also garbled the announcement into "JDK 24 only prints warnings; JDK 26+ stops working". Quote the raw text, not a summary.
- **Hard evidence:** the reproducible runs above, plus the announcement and JEP text.
- **Non-competitor remediation paths, with sources:**
  1. **Find exposure now.** Run your test suite with `--sun-misc-unsafe-memory-access=deny` (JEP 471 option, available since JDK 23). Every Scala 3.0–3.7-compiled lazy val on the classpath fails fast. Verified locally.
  2. **Upgrade or recompile the dependency** onto a library release built with Scala 3.8+. The announcement says compiling *your* code with 3.8+ "is not enough" because dependencies carry the old bytecode.
  3. **Buy time on JDK 24–27** with `--sun-misc-unsafe-memory-access=allow` to suppress the warning (verified on JDK 27). JEP 471 says that once phase 3 lands, `allow` will no longer suppress anything, only `warn` is accepted, and after removal the flag is ignored. This is a bridge, not a fix.
  4. A bytecode-rewriting tool (Sloth) is built into 3.9 as an opt-in experiment. **It is VirtusLab's (COMPETITOR).** Do not present it as the answer. It is fine to say "the release ships an experimental bytecode rewriter".
- **Trade-off:** Staying on an older JDK avoids the noise but blocks JDK 27 (G1-everywhere, compact headers by default). Upgrading means auditing a transitive dependency graph you do not own.
- **Community reaction:**
  - HN 49550270 "Scala 3.9.0 LTS Released", 3 Sep: 2 points, 0 comments (verified via Algolia).
  - contributors.scala-lang.org/t/7477 release thread: 29 posts, 3,007 views, 96 likes. The release slipped from a planned ~22 Jul to RC6 on 19 Aug. Sides: gratitude and release-date pressure (charpov, ossum). No pushback on the LTS policy.
  - Library issue trackers show maintainers already getting reports (see C3).
- **Scores:** Freshness 5 / Relevance 5 / Evidence 5 / Stakes 4 / Tension 3 / Originality 4 = **26/30**
- **Suggested slot:** **Trenches**, or the main Signal, folded with C2 as "the dependency you didn't compile". Our own JDK 27 reproduction is original evidence nobody else has published.

### C2. Spark is de-reflecting itself so Scala 3.8+ can use it, and nothing has shipped yet
- **Freshness:** MATERIAL_UPDATE. The bug dates from April 2026. What changed in September: Scala 3.9 LTS made the 3.8+ stdlib the new LTS baseline on 3 Sep, and its announcement says "no planned compiler or standard-library fix". The Spark-side fixes were merged on 23 Aug and target Spark 4.3.0, which is still unreleased (JIRA: `4.3.0 released=False`).
- **Event dates:**
  - scala/scala3#25896 opened 22 Apr 2026 (labels regression, prio:high, still open).
  - SPARK-57548 opened 19 Jun and resolved 23 Aug (PR apache/spark#57303).
  - SPARK-58166, 58168 and 58169 resolved 23 Aug.
  - SPARK-57549 (TypeTag encoder derivation), 57596 and 58200 (Scala 3 build profile) still open.
- **Source publication date:** 3 Sep (announcement). JIRA and GitHub dates are as above.
- **Falsifiable claim:** On the Scala 3.9.0 stdlib, initialising `scala.reflect.runtime.universe` from scala-reflect 2.13.18 throws `scala.reflect.internal.FatalError: class Array does not have a member apply`. The same program works on 3.7.4. Released Spark (≤4.2.x) initialises that universe eagerly in `ScalaReflection`.
- **Primary sources:**
  - https://github.com/scala/scala3/issues/25896 (P0 issue, 17 comments)
  - https://issues.apache.org/jira/browse/SPARK-57548 (P0)
  - https://issues.apache.org/jira/browse/SPARK-54150 (P0 umbrella "Support Scala 3.x", opened 3 Nov 2025)
  - https://issues.apache.org/jira/browse/SPARK-57549 (P0)
  - https://www.scala-lang.org/news/3.9/ section "Runtime reflection with scala-reflect" (P0)
- **Verification:** reproduced locally on JDK 21. Scala 3.7.4 prints `List(constructor List, method iterableFactory, method ::)` and `57`. Scala 3.9.0 throws `FatalError: class Array does not have a member apply` from `JavaUniverse.init`.
- **Hard evidence:**
  - SPARK-57548 description: "On the Scala 3.8+ stdlib this crashes — `FatalError: class Array does not have a member apply` — an open Scala regression that names Spark."
  - SPARK-58043: "Affects 190 call sites across catalyst/sql-core/hive/sql-api" (companion-as-function removal).
  - SPARK-57549 calls TypeTag-based encoder derivation "the structural blocker for a Scala 3 build of Spark SQL".
  - The 3.9 announcement's workarounds: stay on 3.7.x, avoid code paths that initialise the universe, or migrate to Java reflection.
- **Trade-off:** Data teams on Scala 3 must choose. They can pin 3.7.x, which is not an LTS: 3.3 LTS ends about Sep 2027 and 3.9 is the new LTS. Or they can wait for a Spark minor release. Spark's policy is bugfix-only within a minor (eejbyfeldt, #25896, 24 Apr), so fixes do not reach 3.5.x or 4.2.x.
- **Community reaction (#25896, all P0 GitHub comments):**
  - SethTisue, 22 Apr: "It's reassuring that nobody else has reported this … except that obviously Spark is a big deal."
  - dispalt, 6 May: hit "weird runtime issues with 3.8.3 and rolled back to 3.7.4".
  - eejbyfeldt, 16 Jul: four Spark PRs make the tyda tests pass on 3.8.4, "there is some hope of a upstream fix".
  - lrytz floated a scala-reflect 2.13.19 shim. bishabosha has an experimental scala-reflect port branch, which the announcement says "is not something you can depend on".
  - Sides: Scala team (fix it in Spark) vs Spark users (Spark releases too slowly).
  - Engagement: 0 reactions on the issue. No HN discussion in window (Algolia "scala-reflect" returned 0 hits).
- **Scores:** Freshness 3 / Relevance 4 / Evidence 5 / Stakes 4 / Tension 4 / Originality 5 = **25/30**
- **Suggested slot:** **Trenches** (or merge into C1). It is the clearest "LTS vs the ecosystem's slowest dependency" story, with P0 evidence on both sides and a local reproduction.

### C3. Scala 3.10 stops finding implicits in inaccessible companions, and 3.10.0 is already on Maven Central
- **Freshness:** NEW_THIS_MONTH. The warning shipped in 3.9 on 3 Sep. 3.10.0-RC1 to RC3 came out 3, 11 and 25 Sep. The 3.10.0 final tag and artifacts followed on 4 Oct.
- **Event date:** 3 Sep (deprecation in 3.9). The 4 Oct artifacts are the 1–7 Oct item that changes the story.
- **Source publication date:** 3 Sep (announcement). Maven metadata lists `3.10.0`. The git tag `3.10.0` commit is dated 2026-10-04T13:36Z. GitHub release: 404 (not yet announced).
- **Falsifiable claim:** About 20 Open Community Build projects stop compiling on 3.10 because of this. Consumers usually cannot fix it themselves, because the library has to ship a release.
- **Primary source:** https://www.scala-lang.org/news/3.9/ (P0). Verbatim: "The Open Community Build found around 20 projects that stop compiling on 3.10 for this reason." and "you usually cannot fix it in the consuming project: the instance lives in a library, so that library needs a new release".
- **Verification:**
  - Maven Central metadata checked (P0).
  - Issues filed against libraries in the window: medeia/medeia#693 (2 Sep), wvlet/uni#691 (4 Sep), halotukozak-com/alpaca#470 (26 Aug). zio-dynamodb#909 (12 Aug) concerns 3.8.4 deprecations.
- **Hard evidence:** the announcement number, the RC thread (contributors t/7546, 4 posts), and the issues above.
- **Trade-off:** It closes a spec hole ("the specification has always required an eligible implicit to be accessible") at the cost of a release cascade for downstream libraries.
- **Community reaction:** low. There was no LTS-policy complaint thread in the window.
- **Scores:** Freshness 4 / Relevance 3 / Evidence 4 / Stakes 3 / Tension 2 / Originality 3 = **19/30**
- **Suggested slot:** **In the Know** (one line: "run 3.9 with -deprecation now; 3.10.0 artifacts are out").

### C4. sbt 2.1 milestones: a plugin binary split, Ivy removed, and test scheduling up for review
- **Freshness:** NEW_THIS_MONTH
- **Event dates:** sbt 2.1.0-M1 on 13 Sep, M2 on 21 Sep, M3 ("beta") on 28 Sep. sbt 2.0.9 on 14 Sep, 2.0.10 on 2 Oct (GitHub releases API). RFC-5 posted 4 Sep. "Reforesting the sbt plugin ecosystem" posted 16 Sep (Eugene Yokota, scala-lang.org).
- **Falsifiable claims:**
  - "A plugin built using sbt 2.1.x will not work on sbt 2.0.x", because the metabuild moves to Scala 3.9.0.
  - Scaladex lists **172 plugins** for sbt 2.x as of September 2026.
- **Primary sources:**
  - https://github.com/sbt/sbt/releases/tag/v2.1.0-M1 (P0 release notes)
  - https://www.scala-lang.org/blog/2026/09/16/sbt-plugin-updates.html (P0)
  - https://eed3si9n.com/rfc-5-test-scheduling/ (P0 author blog, 4 Sep; status "Review"; feedback at github.com/sbt/sbt/discussions/9714)
  - https://eed3si9n.com/sbt-2.1.0-beta (P0, 28 Sep)
- **Verification:** release dates and the compatibility table were read directly from the GitHub API.
- **Hard evidence:**
  - Compatibility table: 2.0.x pairs with Scala 3.8.x. 2.1.0 pairs with 3.9.x and its plugins do not run on 2.0.x.
  - "sbt 2.1.0 removes Apache Ivy from its transitive dependency, and implements Ivyless publishing."
  - `clean` now invalidates the disk cache.
  - RFC-5 adds `Global / workerMaxInstances` and `Test / testTopology` (for example `TestTopology.subprojectSplit(2)`) so that forked tests run concurrently across subprojects.
  - The plugin work was funded through the Sovereign Tech Fund ("sbt 2 Stable Release and Maintenance").
- **Trade-off:** Plugin authors now maintain three axes: sbt 1, sbt 2.0 and sbt 2.1. Teams moving to sbt 2 must decide whether to wait for 2.1.
- **Community reaction:** HN: none in window. Contributors forum: no sbt 2.1 thread found. HN comment 49712972 (15 Sep, "Java 27" thread), one anecdote: "sbt got too complex for it's own good".
- **Competitor note:** the blog credits VirtusLab people (Rikito Taniguchi, Lukas Rytz) among plugin contributors. Cover the release, but do not name or credit them.
- **Overlap:** check against #4/#5 (May/June issues mention sbt 2 GA, 14 Jun 2026).
- **Scores:** Freshness 5 / Relevance 4 / Evidence 5 / Stakes 3 / Tension 2 / Originality 3 = **22/30**
- **Suggested slot:** **Signal** (short) or **In the Know**. It pairs well with C5: sbt 2's Bazel-compatible remote cache vs Box's choice of Gradle.

### C5. Box: eight years moving a 360+ module Scala monorepo from sbt to Gradle
- **Freshness:** NEW_THIS_MONTH (published 16 Sep 2026). The migration itself ran 2015–2023.
- **Event date:** migration 2015–2023. Publication 16 Sep 2026: sitemap `lastmod 2026-09-16T15:00Z`, page `"date":"1789570800"` (= 16 Sep 2026 15:00 UTC). The visible `datePublished` field is empty. Picked up by This Week in Scala on 5 Oct (P1).
- **Falsifiable claim:** Box says remote build caching is "the largest single reason a typical PR validation runs in about 12 minutes today". A single cache pod (4 CPU, 4 GiB RAM, 100 GiB disk) moves about 337 GiB/month.
- **Primary source:** https://blog.box.com/gradle-scala-monorepo-box-experience-360-modules (P0, company engineering blog, author Artsiom Samasadau)
- **Verification:** author-reported. There is no independent check, and the 2015 benchmark figures are old (Gradle 10.6s vs sbt 50s dependency tree; IntelliJ refresh 18s vs 145s).
- **Hard evidence:**
  - 360+ modules, 100+ engineers committing Scala every year.
  - About 20 libraries had to be converted before a single service could move. 100+ modules carried dual build definitions.
  - Clean local build before the move: 25–27 min.
  - "Gradle never made the compiler itself faster". Zinc was carried over unchanged.
- **Trade-off (the post states these itself):**
  - There is no `%%` equivalent, so the Scala cross-version matrix lives partly outside Gradle.
  - Custom tasks replaced sbt plugins: Scrooge, BuildInfo, Specs2 discovery.
  - Coverage uses JaCoCo with exclusion lists in place of scoverage.
  - Loading all modules into Metals exhausts laptop memory.
  - The post also notes that sbt 2.0 now ships a Bazel-compatible remote cache.
- **Community reaction:** none found on HN, the Contributors forum or Reddit in the window. TWIS listing only.
- **Overlap risk:** #6 led with Metals v2 / Scala monorepo and covered Gradle Isolated Projects. Box mentions Metals v2 too. If used, angle it on build economics (cache vs compiler), not IDE scale.
- **Scores:** Freshness 4 / Relevance 4 / Evidence 3 / Stakes 3 / Tension 4 / Originality 4 = **22/30**
- **Suggested slot:** **Top Resources**, or **Trenches** if #6 overlap is acceptable. Box is not a competitor.

### C6. Pre-SIP: `T ? E`, a new type for optionals and errors (Odersky)
- **Freshness:** MATERIAL_UPDATE. The topic opened 25 Aug. 45 of 77 posts are dated September.
  - 3 Sep: prototype implementation posted.
  - 14 Sep: Odersky concedes it "cannot go in before explicit nulls are standard".
  - 28 Sep: switched to left-bias for `?`.
  - 30 Sep: mberndt's alternative desugaring (`A ? E` → `Maybe[E, A]`).
- **Event date:** 25 Aug to 7 Oct (ongoing).
- **Source publication date:** forum posts as dated.
- **Falsifiable claim:** The proposal needs `-Yexplicit-nulls` to parse `?` (odersky, #47, 14 Sep).
- **Primary source:** https://contributors.scala-lang.org/t/pre-sip-a-new-type-for-optionals-and-error-handling-2/7533 (P0 forum; 77 posts, 3,341 views, 178 likes)
- **Verification:** thread read in full through the Discourse JSON.
- **Hard evidence:** a prototype `scala.compiletime.Maybe[+T, +E]` (#34). The explicit-nulls dependency (#47).
- **Tension (real):**
  - jducoeur (#39, 10 likes): "The really serious fragmentation concern is specifically for libraries … a world that is half-Option, half-Maybe".
  - Ichoran (#46): "shouldn't be used for any serious library at this point".
  - mberndt (#54 and #67, 6 and 9 likes): shipping with right-bias "would be outright hostile to those of us who rely on typeclass based infrastructure libraries", and the "design mistake" rationale is "mere assertions".
  - gzoller (#44): `T?` "sends the message that 'nulls are ok now'".
  - For: sjrd (#15), datalin (#41).
- **Trade-off:** ergonomics and zero-allocation optionals vs a library-ecosystem split and a hard dependency on explicit nulls.
- **Community reaction:** confined to the forum. No HN or Reddit traction found.
- **Scores:** Freshness 4 / Relevance 3 / Evidence 4 / Stakes 2 / Tension 4 / Originality 4 = **21/30**
- **Suggested slot:** **Signal** (short) or **In the Know**. It is a pre-SIP, so for a CTO reader the stakes are years out. The fragmentation argument is the useful part. It is not a Debate, because one side has not even concluded the feature should exist.

### C7. Odersky / TACIT: tracked capabilities as the agent safety harness
- **Freshness:** BACKGROUND_ONLY.
  - Blog post: 27 Jul 2026 (Substack API `post_date 2026-07-27T13:22Z`).
  - arXiv 2603.00991: first version 1 Mar 2026, v2 7 May 2026.
  - TACIT repo: last release 0.2.2 on 17 Aug, **no commits since 1 Sep**.
  - The only September event is that the ACM DL version (doi 10.1145/3786335.3813127) was posted to HN on 6 Sep (49585491: 1 point, 0 comments).
- **Falsifiable claim:** In the paper's classified-data experiments, "both models achieve 100% security" with utility of 99.2% (Claude Sonnet 4.6) and 90.0% (MiniMax M2.5) (arXiv v2).
- **Primary sources:**
  - https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents (P0; 22 reactions, 3 comments, verified through the Substack API)
  - https://arxiv.org/html/2603.00991v2 (P0 paper)
  - https://github.com/lampepfl/tacit (86 stars, 12 forks)
  - The paper won best paper at CAIS 2026 per Odersky's own HN comment (49095664). There is no independent confirmation; check caisconf.org.
- **Scores:** Freshness 1 / Relevance 4 / Evidence 4 / Stakes 3 / Tension 2 / Originality 3 = **17/30**
- **Suggested slot:** **reject as Debate**. At most one line in Top Resources tied to a September hook (see §2). Prior use: #3 (July) cited the separation checker and System Capybara but not TACIT, so it is not a reuse.

### C8. JVM language churn: Kotlin 2.4.20, Groovy 6.0, Gradle 9.8, Ktor 3.6, Kyo 1.0.0-RC7
- **Freshness:** NEW_THIS_MONTH (all P0 GitHub/vendor dates):
  - Kotlin 2.4.20: 7 Sep
  - Groovy 6.0.0 tag: 19 Sep
  - Gradle 9.8.0: 24 Sep (Java 27 support)
  - Ktor 3.6.0: 18 Sep
  - Kyo 1.0.0-RC7: 28 Sep
- **Migration impact actually found:**
  - **Groovy 6.0:** minimum JDK 17. invokedynamic is the default, and non-indy needs the new `groovy-callsite` module. Grape's Ivy backend split into `groovy-grape-ivy`. Security Manager support removed. XML APIs are secure-by-default (XXE/DTD). (groovy-lang.org/releasenotes/groovy-6.0.html, P0)
  - **Kotlin 2.4.20:** mostly Native, Wasm and JS. Supports Gradle 7.6.3–9.7.0, which **excludes the Gradle 9.8 released 17 days later**. The `kotlin` runner was replaced by `kotlinr`.
  - **Gradle 9.8:** routine (Java 27 support).
- **Scores:** Freshness 4 / Relevance 2 / Evidence 4 / Stakes 2 / Tension 1 / Originality 1 = **14/30**
- **Suggested slot:** **In the Know**, one line, Groovy 6 first because of the JDK 17 floor and Security Manager removal. Kyo: low priority, and its 1.0 is still RC.

---

## 2. Debate dossier: "Can the type system be the agent sandbox?"

**Verdict: Side B lacks substance as a direct rebuttal in the window, and Side A is not fresh (27 Jul).** Demote, per the brief's own rule. The most interesting finding is that **the strongest "types aren't enough" points come from the TACIT paper itself.** The credible September voices argue *about sandboxes*, not against type-level capabilities.

### Side A: compile-time capability tracking as the safety harness
- Odersky et al., "Tracked Capabilities for Safer Agents", 27 Jul 2026: https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents
  - Verbatim: "agent safety should be a property of the infrastructure, not a bet on how the model behaves."
- Mechanism (arXiv 2603.00991v2):
  - The agent writes Scala 3 snippets, which are type-checked under capture checking plus a "safe mode" language import that bans unchecked casts and reflection.
  - Classified data is wrapped in `Classified[T]`, which only pure functions (`->`) can touch.
  - A trusted local LLM can read the classified content.
- Their argument against sandboxes (paper, related work), verbatim: "Sandboxing constrains which system resources agent code can touch … but it cannot enforce information-flow properties within the permitted operations … the agent legitimately reads a private file via a permitted file-system call and legitimately calls the cloud LLM via a permitted network call. The leak is the data flow from one to the other, which never crosses a sandbox boundary."

### Side A's own stated limits (the material for a "B" column)
- **Trusted computing base** (paper §3.1): "the Scala 3 compiler (with capture checking and safe mode), the tacit capability library, the runtime that executes type-checked code". The JVM and every capability-library implementation are trusted. Anything reachable through them is outside the proof.
- **Shell-out / external processes**, verbatim: "External processes spawned by the agent escape the Scala safe-mode boundary, so the static guarantee degrades to that of the underlying allowlist … security-critical deployments should combine tacit with sandboxing for defense in depth."
- **Side channels**, verbatim: "We do not cover covert channels such as timing or termination."
- **Escape hatches** (blog), verbatim: "the full language also has escape hatches — unchecked casts, reflection, and so on — that would let a determined agent slip out". They are closed only by restricting the agent to a safe subset.
- **Not covered:** JVM interop, FFI, generated code. The safe-mode subset governs only the code the agent submits. Java libraries the capability library calls are trusted by construction. This is my inference from the TCB list, not a quote.

### Side B: candidates found, and why none qualifies as a direct rebuttal
1. **Matthew Green, "Is sandboxing sufficient to contain rogue agents?"**, 30 Sep 2026: https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents/
   - HN 49920167: 53 points, ~100 comments (Algolia).
   - He argues the boundary is *instruction provenance*, not containment: "Agents will do what they're told by whoever manages to get text in front of them", and "A warden-guarded sandbox is just another version of the alignment problem."
   - He does **not** discuss type systems or capabilities.
   - Usable as the September hook: Green says runtime sandboxes fail at the data-flow layer, which is exactly the layer TACIT targets. That makes him closer to an ally of Side A on the diagnosis. It does not create opposition.
2. **Trail of Bits, "VMs won't contain cyber-capable agents"**, 26 Aug 2026 (just before the window): https://blog.trailofbits.com/2026/08/26/vms-wont-contain-cyber-capable-agents/
   - HN 49450188: 198 points, 147 comments.
   - Argues off-the-shelf VMs are escapable and recommends minimal-attack-surface virtualization (Firecracker). This is a runtime-isolation camp, but it argues for *harder* runtime isolation, not against types.
3. **XGR.Network, a comment on Odersky's post** (3 Aug), verbatim: "Capability flow can prove what the program was allowed to attempt; it cannot by itself prove which external effects completed."
   - This is a substantive, narrow critique (authority vs observed outcome). It comes from an unknown, unverified commenter, so it is not citable as a credible voice.
4. **r/scala "AI in Scala"** (20 Sep, 30 points; opencli read OK).
   - It is about LLM code quality in Scala, not sandboxing. The closest line is sloppycommitment: "the language doesn't matter that much with a LLM … tweaks in the coding harness are more impactful than the language."
   - Off-topic for the sandbox question.
5. **"Authority Is Not a String" / CapScope**, arXiv 2609.08371, 8 Sep 2026 (Bouras, Dai, Mechtaev).
   - A September paper that enforces typed capabilities at the *harness* level (outside the model and outside the language), for the Pi coding agent. It does not cite TACIT.
   - It is the nearest thing to an alternative architecture: capability security without a capability-safe language. It is an alternative, not a rebuttal.

**Recommendation:** Do not run this as a Debate. If you want it in the issue, use a Signal framed as "the September security voices say runtime sandboxes can't see data flow (Green, ToB); Odersky's group claims types can, and their own paper concedes external processes, side channels and the trusted JVM need a sandbox anyway". That is honest and has P0 quotes on every point. **The brief's Debate candidate A (Scala 3.9/JDK 27 upgrade) is better supported.** C1 and C2 together carry a real tension: the Scala team says "fix it in Spark", Spark users say "Spark releases too slowly", and the LTS is caught between them.

---

## 3. Rejected items and why
- **The tanishiking capture/separation checking intro** is on virtuslab.com (COMPETITOR) and dated 13 May 2026. Rejected.
- **Sloth** (bytecode rewriter), tulip, VirtusLab Scala Stack, Besom, the VirtusLab WASM post: COMPETITOR. Do not feature. Mention Sloth only generically, if at all (C1).
- **"VirtusLab assumes responsibility for Scala 2 maintenance"** (contributors t/7555 and scala-lang.org, **7 Oct 2026**): COMPETITOR news. It is outside the window anyway, but it does touch C2 (scala-reflect lives in Scala 2). Flag it to the editor and do not feature it.
- **Scala.js 1.22 stable WebAssembly backend:** Scala.js 1.22.0 was released **20 Jun 2026** (GitHub). It is only bundled into the 3.9 story, so BACKGROUND_ONLY. Its requirements (verbatim): "ECMAScript 2022 or newer, an engine implementing Wasm 3.0, and the ESModule module kind".
- **SIP-71 `into` stable:** true (announcement: "Scala 3.9 makes it part of the stable language"), but low CTO stakes. At most a fragment in In the Know.
- **The 3.3 LTS extension:** true. 3.3 is maintained "for one year after Scala 3.9.0" (so ~Sep 2027), and 3.9 for "at least three years". 3.3.9-RC1 came out 11 Sep (tested on "over 1500 projects"). There was no controversy, so it does not stand alone. Fold it into C1.
- **Backport stats (1,420 of 2,380 PRs, "almost 43%") and Open Community Build ("about 1,780 of nearly 2,000 projects"):** verified verbatim. These are supporting numbers for C1, not stories.
- **SLC: "Make Vector the default Seq"** (t/7482, 47 posts, last post 10 Sep): a stdlib proposal, too early.
- **"Pre-SIP: Optional parameters by symmetry with varargs" and "Status of SIP-72":** inside baseball.
- **The JDK 27 JVMCI removal as a Scala story:** I found no Scala-specific source of breakage. It belongs to the JDK track (cite JDK-8382582).
- **Kotlin 2.4.20, Ktor 3.6, Kyo RC7, Gradle 9.8:** routine (C8).

## 4. Open fact-check questions
1. **CAIS 2026 best paper award.** The only source is Odersky's own HN comment and Substack. Confirm on caisconf.org, along with the conference date.
2. **Box post date.** It rests on sitemap `lastmod` plus an embedded epoch. The visible byline date is empty. Ask Box, or accept "published mid-September 2026".
3. **Box numbers** (12-min PR validation, 337 GiB/month) are self-reported. The 2015 benchmark numbers are 11 years old, so do not present them as current sbt vs Gradle performance.
4. **When does Unsafe phase 3 (deny by default) land?** The JEP says "JDK 26 or later", and it did not happen in 26 or 27. Is there a JEP draft targeting JDK 28? I did not check JBS for a JDK 28 target.
5. **Scala 3.10.0 announcement status.** Artifacts are on Maven Central (4 Oct), but there is no GitHub release or blog post yet. Do not call it "released" until it is announced; per SethTisue's 3.9 disclaimer, publication is not the final step.
6. **Does the Spark 4.3.0 fix set fully unblock Spark 2.13 jars from Scala 3.9?** eejbyfeldt reports tyda tests passing on 3.8.4 with four PRs. TypeTag-based `encoderFor` (SPARK-57549) is still open, so typed Datasets of case classes from Scala 3 may still fail. Spark 4.3.0 has no release date.
7. **"~20 projects" for the 3.10 implicit change** is the announcement's own number. The OCB report itself was not checked.
8. **Kotlin 2.4.20 "Gradle 7.6.3–9.7.0 support"** is from the WebFetch summary of the what's-new page. Re-check the exact upper bound on kotlinlang.org before printing that it excludes Gradle 9.8.

## 5. URLs fetched
**OK:**
- Scala and JDK:
  - https://www.scala-lang.org/news/3.9/ (curl raw text plus WebFetch)
  - https://openjdk.org/jeps/471
  - https://openjdk.org/projects/jdk/26/
  - https://openjdk.org/projects/jdk/27/
- Spark and Scala issue tracking:
  - Apache JIRA REST: SPARK-54150, 57548, 57549, 57596, 58029, 58043, 58166, 58168, 58169, 58200, project versions
  - gh api: scala/scala3#25896 and comments
- Odersky / TACIT:
  - https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents (plus Substack API: post, archive, comments)
  - https://arxiv.org/html/2603.00991v2
  - export.arxiv.org API
  - gh api: lampepfl/tacit (repo, commits, releases)
- Release lists (gh api): sbt/sbt releases (v2.1.0-M1, v2.0.9), gradle/gradle, JetBrains/kotlin, ktorio/ktor, getkyo/kyo, apache/groovy tags, scala/scala3 releases and tags, scala-js/scala-js
- repo1.maven.org scala3-compiler_3 maven-metadata.xml
- sbt and build tooling:
  - https://www.scala-lang.org/blog/2026/09/16/sbt-plugin-updates.html
  - https://eed3si9n.com/ (index)
  - https://eed3si9n.com/rfc-5-test-scheduling/
  - https://eed3si9n.com/sbt-2.1.0-beta
- Box:
  - https://blog.box.com/gradle-scala-monorepo-box-experience-360-modules (WebFetch plus curl)
  - https://blog.box.com/sitemap.xml
- https://thisweekinscala.substack.com/api/v1/posts/this-week-in-scala-oct-5-2026 (P1)
- contributors.scala-lang.org Discourse JSON: search, t/7533, 7477, 7546, 7550, 7555
- HN Algolia: search API (re-run with the corrected 1 Sep–7 Oct 2026 window), items 49460658, 49250395, 49095664, 49450188, 49920167, 49822295
- https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents/
- https://arxiv.org/abs/2609.08371
- Reddit r/scala 1wl94vh through `opencli reddit read`
- https://kotlinlang.org/docs/whatsnew2420.html
- https://groovy-lang.org/releasenotes/groovy-6.0.html
- virtuslab.com capture-checking post (date only)
- Local scala-cli runs on JDK 27+35 and JDK 21 (Scala 3.3.6, 3.7.4, 3.9.0)

**Failed or partial:**
- reddit.com and old.reddit.com JSON search (blocked; 302 / non-JSON). Used opencli for the one thread only. I did not run a Reddit-wide search for TACIT or sandbox reactions.
- Contributors search for "optional error handling" returned HTTP 429 once (I got the topic through the "after:2026-09-01" search instead).
- Box page `datePublished` is empty, and Wayback has no snapshot.
- WebSearch for "eed3si9n RFC-5" returned junk (resolved through the eed3si9n.com index).
- The first HN queries used the wrong timestamp (fixed after the coordinator's correction, and 2025 results discarded).
- X/Twitter, LinkedIn and Lobsters were not searched (no time budget spent; HN, the forum and Substack covered the reaction surface).
