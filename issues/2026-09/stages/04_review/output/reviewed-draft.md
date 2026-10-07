# SIGNAL: What matters in distributed systems

**September 2026 | Issue #7**

Welcome back. Last month, three systems failed through the mechanism built to protect them. A UK flight-data link [dropped, reconnected on its own and was logged as stable](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/), while a corrupt record sat in the data for two and a half hours. A Firebase kill switch, built to undo bad releases, [pushed a bad config to a wide population of iOS apps at once](https://firebase.blog/posts/2026/10/firebase-analytics-outage), and the status pages stayed green throughout. The third, a Kafka broker that deleted fresh data after a clean shutdown, is this month's Trenches.

---

## Today: What to watch this month

- **[A clean Kafka restart deleted fresh data.](https://issues.apache.org/jira/browse/KAFKA-20979)** A truncated index file wasn't fsynced, so after restart new segments looked like they were written in 1970.
- **[LangChain4j adds a model that only decides.](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0)** `DecisionModel` returns typed answers with probabilities, and an independent test puts numbers on the idea.
- **[Kafka 4.4.0 is a month late.](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)** A team that planned CVE fixes around it learned the project had not committed to a date.
- **[Scala 3.9 is the new LTS.](https://www.scala-lang.org/news/3.9/)** Old lazy vals inside your dependencies still call `sun.misc.Unsafe`, and recompiling your own code won't remove them.
- **[JDK 27 changes your object layout by default.](https://bugs.openjdk.org/browse/JDK-8386990)** Compact headers save heap. Oracle's open ticket lists what they cost.
- **[A UK flight-data link "recovered" while corruption spread.](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/)** A one-millisecond race stopped UK departures for about four and a half hours.
- **[Firebase's kill switch crashed iOS apps in one go.](https://firebase.blog/posts/2026/10/firebase-analytics-outage)** A two-line flag cleanup left a broken config live for 2 hours 11 minutes.

---

## The Architecture Debate: Should a Model That Only Decides Replace Your LLM Judge?

**[LangChain4j 1.21.0](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0) ships a model type that returns no text.** A `DecisionModel` takes yes/no, choice and scale questions about an input and returns the probability of each answer. The release builds model routing, RAG re-ranking, tool selection, guardrails and an agentic router on top of it. The whole API is marked `@Experimental`.

**The category arrived in under three weeks.** [TypeSafe launched Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev), a model that answers typed questions instead of generating text, and the [Hacker News thread](https://news.ycombinator.com/item?id=49717558) reached 1,989 points. OpenAI followed with a [Decisions API](https://developers.openai.com/api/docs/guides/decisions), now in public beta. LangChain4j contributors argued over the name in [issue #6468](https://github.com/langchain4j/langchain4j/issues/6468) before settling on `DecisionModel` instead of `JudgeModel`. One participant's reason: Jev "is explicitly not an LLM and doesn't reason step by step the way an 'LLM judge' does."

**The case for: an independent test.** Researchers from Bonn, the Lamarr Institute and Fraunhofer IAIS [ran Jev on 37 datasets](https://arxiv.org/abs/2609.37647): 346,009 requests for about $9.15. Jev beat Qwen3.8-27B on 27 datasets and lost on 9, with one tie. Eleven of its wins had non-overlapping 95% bootstrap intervals; none of Qwen's did. Calibration error on choice questions was 0.028 and mean latency 0.36 seconds. This side is right when the decision is short, well-scoped and repeated at volume: route this request, gate this output, pick this tool.

**The case against: the same paper.** All three models in the test, Jev included, degraded on low-resource languages, fine-grained or noisy labels, and rubric-based quality judgments. Binary answers "rank well but are poorly placed relative to a fixed 0.5 threshold": tuning the threshold moved one legal benchmark from 0.50 to 0.75 micro-F1. On Hacker News, one commenter called the vendor's comparison with LLMs "misleading because they make people believe they're as general purpose as LLMs." A general model stays the better judge when the call is fuzzy and the grader has to explain itself.

**Plenty is still unproven.** Jev access runs through a waitlist. The Spring, Scala and Kotlin clients are community projects. The LangChain4j interface went through three names in five days before release, and OpenAI's API is still in beta.

**Scalac angle:** Put decisions behind their own interface, separate from generation. That is what LangChain4j just did, and it lets you swap a decision model in or out per call site. Tune the threshold for each task against labelled data before you trust 0.5. Log where each confidence number came from, because a calibrated probability and a number a chat model wrote down are different evidence. Keep LLM judges for rubric grading until a test like this one says otherwise for your data.

---

## Notes from the Trenches: A Clean Shutdown That Deleted Kafka Data

**The problem:** Kafka PMC member Mickael Maison [saw brokers on 4.1.0 delete recent segments at startup](https://issues.apache.org/jira/browse/KAFKA-20979). "This has happened multiple times in the past few weeks." The broker log said retention had fired:

```
Deleting segment LogSegment(baseOffset=83454, size=4483, ..., largestRecordTimestamp=0)
due to log retention time 604800000ms breach
```

He checked the segments with `DumpLogSegments`. The records had valid timestamps and the seven-day retention had not been breached. "In all cases it happened on a clean shutdown."

**The mechanism sits in the graceful path.** On a clean shutdown the broker flushes each log, then closes it. The flush fsyncs the time index at its pre-allocated size: 10 MB by default, zero-filled. The close truncates the file to its real size with `RandomAccessFile.setLength()` and doesn't fsync that truncation. If the broker comes back before the operating system has written the new file length to disk, the index returns at full size. The zero-filled tail reads as entries with timestamp 0, the segment looks like it was written in 1970, and time-based retention deletes it.

This is Maison's analysis of the code, and the fix was merged on that basis; the ticket contains no standalone reproduction. Data loss also needs the restart to beat the metadata flush, so a clean shutdown on its own isn't enough.

**The solution:** fsync index files when shutdown trims them. The fixes landed on the [4.4 branch](https://github.com/apache/kafka/commit/beae700199c7ad805f8d5af53bdb7072cc1928e5) and in [PR #23316](https://github.com/apache/kafka/pull/23316), with fix versions 4.3.2 and 4.4.0. 4.3.2 is at release candidate. Kafka 4.2.2, released at the end of last month, doesn't carry the fix, and no 4.2.x release does yet. A sibling bug, [KAFKA-21000](https://issues.apache.org/jira/browse/KAFKA-21000), covers `.log` files with preallocation enabled. That one throws on restart instead of deleting, and its fix targets 4.5.0.

Until you can upgrade, search broker logs after each restart:

```bash
grep 'largestRecordTimestamp=0) due to log retention time' /path/to/kafka/logs/server.log
```

Maison held deleted files back with `file.delete.delay.ms` long enough to inspect them, which is how he confirmed the records were valid.

**Scalac angle:** Most teams test crash recovery and treat a graceful restart as safe. A rolling upgrade is a sequence of graceful restarts. Put the `grep` above into your post-restart checks, and watch hardest where the host or volume goes down with the broker: the loss depends on the new file length not reaching disk, so a quick process restart on a healthy machine is the least likely place to see it. Upgrade to 4.3.2 or 4.4.0 when they ship, and note the 4.2.x gap if you're pinned there.

---

## Signal Over Noise: Three Changes With a Migration Path

### 1. [Kafka 4.4.0 misses its window, and the PMC says there was no date to miss.](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)

The [release plan](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/429064575/Release+Plan+4.4.0) said "no earlier than September 9". Three release candidates failed before RC4 [went to vote on 6 October](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222). The vote runs to 12 October. Ericsson engineers wrote to the users list that they had planned their own release for the end of that month around 4.4.0's vulnerability fixes. Matthias J. Sax replied: "As an open source project, we don't have committed release dates." Chia-Ping Tsai suggested shipping 4.3.2 or 4.2.2 instead. On the dev list he named the cause: "We had too many must-have changes in 4.4.0, which caused a serious delay." And separately: "The codebase is large and CVEs are common these days."

Part of that CVE load sits in compression. Luke Chen [told the dev list](https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8) that snappy-java CVEs can't be fixed with a version bump because upstream isn't responding, and that LZ4 support depends on a fork kept by one person. He thinks Kafka isn't affected by the CVEs he checked, but says he isn't 100% sure. Another contributor disputes that snappy-java is unmaintained; nobody disputed the LZ4 point. Kafka can't drop a codec, because old logs have to stay readable, so [KAFKA-21178](https://issues.apache.org/jira/browse/KAFKA-21178) proposes letting admins disable codecs for new writes.

Don't plan CVE remediation around an unreleased minor. The patch lines are the hedge: 4.2.2 is out and 4.3.2 is at release candidate.

### 2. [Scala 3.9 LTS: the Unsafe warning comes from a jar you didn't compile.](https://www.scala-lang.org/news/3.9/)

Scala 3.9 is the new long-term support line, guaranteed for at least three years; 3.3 LTS gets one more year. Lazy vals compiled with Scala 3.0 to 3.7 still go through `sun.misc.Unsafe`, which [JEP 471](https://openjdk.org/jeps/471) is phasing out. We ran it on JDK 27 GA: a Scala 3.3 lazy val prints a warning and runs. With `--sun-misc-unsafe-memory-access=deny` it fails with `UnsupportedOperationException`. The same code compiled with 3.9 runs clean. Recompiling your own code doesn't help when the old bytecode ships inside a dependency.

Spark is the harder case. On the 3.8+ standard library, scala-reflect's runtime universe throws `FatalError: class Array does not have a member apply`, and released Spark initialises it. The 3.9 announcement says no compiler or standard-library fix is planned, and the [Scala issue](https://github.com/scala/scala3/issues/25896) is still open. The Spark-side fixes were merged in August and [target Spark 4.3.0](https://issues.apache.org/jira/browse/SPARK-57548), which has no release date.

Run your test suite with `--sun-misc-unsafe-memory-access=deny` now to find the dependencies that carry old lazy vals, then move to releases built with Scala 3.8 or later. Treat `=allow` as a bridge: JEP 471 says it will stop working once `deny` becomes the default. Spark teams on Scala 3 should stay on 3.7.x until Spark 4.3.0 ships, and read its notes before moving: typed encoders for Scala 3 case classes are tracked in a [separate, still-open ticket](https://issues.apache.org/jira/browse/SPARK-57549).

### 3. [JDK 27 turns compact object headers on by default, with an open regression ticket.](https://openjdk.org/jeps/534)

Object headers shrink, so heap shrinks. [JEP 534](https://openjdk.org/jeps/534) reports 22% less heap and 8% less CPU on SPECjbb2015, and Amazon runs the feature in hundreds of production services. The cost is in [JDK-8386990](https://bugs.openjdk.org/browse/JDK-8386990), filed by Oracle's own performance team and still open at GA with fix version "tbd". The first element of an array now sits at byte offset 12 instead of 16, which breaks 8-byte alignment for vectorised code. The ticket lists crypto benchmarks down 1% to 4%, String microbenchmarks down by up to 50% and a Scala k-means benchmark down 15% to 20%. That last number is disputed: one engineer questions its significance, and a second ticket attributes the same drop to the JVMCI removal. A report filed the day after GA [measured a 9% drop](https://bugs.openjdk.org/browse/JDK-8392511) on a 2-D array benchmark.

The engineers in the ticket lean toward accepting part of the cost. Aleksey Shipilev: "it would be unwise to be spooked by single-digit-% regressions on microbenchmarks, when the real world footprint improvements from COH in real world production environments are double-digit-%." Vladimir Kozlov looked at realigning the crypto intrinsics and concluded it "may cause more regression than improvement." In practice, budget for the 1% to 4% crypto loss as part of the default.

Before you roll out JDK 27, benchmark your hot paths twice, once with `-XX:-UseCompactObjectHeaders`. Array-heavy, string-heavy and crypto-heavy code is where the difference shows. The [release notes](https://jdk.java.net/27/release-notes) put that flag on the path to deprecation and removal, so the time to measure is before it goes.

---

## In the Know

**[There is no Graal JIT on JDK 27, and we got this wrong.](https://bugs.openjdk.org/browse/JDK-8382582)** JDK 27 removed JVMCI and the Graal JIT without a JEP. [GraalVM's calendar](https://www.graalvm.org/release-calendar/) lists only 25.x releases through February 2027, and [25.4](https://www.graalvm.org/release-notes/25.4/) is built on JDK 25. A team on the Graal JIT can't reach JDK 27 by swapping builds. In Issue #3 we wrote "Earliest removal is JDK 29." It shipped in 27.

**[G1 is the default collector in every environment.](https://openjdk.org/jeps/523)** On Linux, containers with a memory limit under 1792 MB or fewer than 2 CPUs, started without a GC flag, move from Serial to G1. The JEP publishes no G1-versus-Serial numbers; measure before you pin either.

**[JEP 544 targets AOT-compiled code for JDK 28.](https://openjdk.org/jeps/544)** The AOT cache will also store compiled native code; the JEP's own examples show startup 65% to 80% shorter. The code is used only if training and production share CPU features and the garbage collector. Otherwise HotSpot warns and falls back to the JIT.

**[Saved agent state is input.](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm)** langchain4j-agentic deserialized persisted agent state with Jackson default typing, which allows code execution given a gadget class and attacker-controlled state. [a2a-java's default task store](https://github.com/a2aproject/a2a-java/security/advisories) performed no authorization on task reads. Both are patched.

**[Kafka accepts native cluster mirroring.](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring)** KIP-1279 passed its vote. It isn't merged or released, and with 4.5.0 proposed for around March 2027, MirrorMaker 2 stays the tool for now.

---

## Top Resources

**Repo to watch:** [lampepfl/tacit](https://github.com/lampepfl/tacit)

Martin Odersky's group lets an agent write Scala 3 and uses capture checking to decide what that code may touch. This isn't new this month: the [paper](https://arxiv.org/abs/2603.00991) dates from March and Odersky's [blog post](https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents) from July. The paper is honest about the edges: processes the agent spawns escape the type-checked boundary, and the runtime that executes the code has to be trusted. The authors recommend combining it with a sandbox.

**Article to read:** [We used a database as a message queue. Now we use Kafka](https://www.tigrisdata.com/blog/quick-fdb-kafka/)

Tigris ran its task queue inside FoundationDB until queue writes started competing with customer writes and triggered throttling. Read it if your job queue lives in the same database as your customer data.

**Report to read:** [NATS preliminary investigation into the NAS incident](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf)

Eighteen pages, minute by minute: a race with a window of about one millisecond, an automatic reconnect that hid the corruption, and nearly three hours of reconciling two systems after the link was cut. It is preliminary, with no code or configuration, and the final report is due in early November.

---

**What is SIGNAL?**

SIGNAL is a monthly, opinionated newsletter for engineers building and operating JVM and Scala systems, and agentic AI in production.

Each issue has three sections: Architecture Debate, Notes from the Trenches, and Signal Over Noise. They cover architecture decisions, production lessons, incidents, and ecosystem shifts worth paying attention to. No hype. No vendor talking points.

At Scalac, we build high-throughput distributed systems and agentic AI products in Scala, Java, and Rust. SIGNAL is the filter we wanted when making our own architecture bets.

**Have a story for SIGNAL?** Reply to this email. We read every response.

---

## References

- [KAFKA-20979: index truncation not fsynced on shutdown](https://issues.apache.org/jira/browse/KAFKA-20979)
- [Apache Kafka PR #23316](https://github.com/apache/kafka/pull/23316)
- [Apache Kafka commit beae700 (4.4 branch)](https://github.com/apache/kafka/commit/beae700199c7ad805f8d5af53bdb7072cc1928e5)
- [KAFKA-21000: log file preallocation trim](https://issues.apache.org/jira/browse/KAFKA-21000)
- [Kafka 4.2.2 release notes](https://downloads.apache.org/kafka/4.2.2/RELEASE_NOTES.html)
- [Kafka Release Plan 4.4.0](https://cwiki.apache.org/confluence/spaces/KAFKA/pages/429064575/Release+Plan+4.4.0)
- [Kafka users@: 4.4.0 release date thread](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)
- [Kafka dev@: vote thread for 4.4.0 RC4](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222)
- [Kafka dev@: compression codec dependencies](https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8)
- [KAFKA-21178: disable compression codecs on write](https://issues.apache.org/jira/browse/KAFKA-21178)
- [KIP-1279: Cluster Mirroring](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring)
- [LangChain4j 1.21.0 release notes](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0)
- [LangChain4j issue #6468: naming the decision model](https://github.com/langchain4j/langchain4j/issues/6468)
- [TypeSafe: Introducing System One models and Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [OpenAI: Decisions API guide](https://developers.openai.com/api/docs/guides/decisions)
- [arXiv 2609.37647: independent evaluation of Jev](https://arxiv.org/abs/2609.37647)
- [Hacker News: Introducing System One Models and Jev](https://news.ycombinator.com/item?id=49717558)
- [Scala 3.9 LTS announcement](https://www.scala-lang.org/news/3.9/)
- [JEP 471: Deprecate the memory-access methods in sun.misc.Unsafe](https://openjdk.org/jeps/471)
- [scala/scala3 #25896: scala-reflect on the 3.8+ stdlib](https://github.com/scala/scala3/issues/25896)
- [SPARK-57548](https://issues.apache.org/jira/browse/SPARK-57548)
- [SPARK-57549: Scala 3 typed encoders](https://issues.apache.org/jira/browse/SPARK-57549)
- [JEP 534: Compact Object Headers by Default](https://openjdk.org/jeps/534)
- [JDK-8386990: compact headers array alignment regressions](https://bugs.openjdk.org/browse/JDK-8386990)
- [JDK-8392511: SERT LU regression with compact headers](https://bugs.openjdk.org/browse/JDK-8392511)
- [JDK 27 release notes](https://jdk.java.net/27/release-notes)
- [JDK-8382582: Remove JVMCI](https://bugs.openjdk.org/browse/JDK-8382582)
- [GraalVM release calendar](https://www.graalvm.org/release-calendar/)
- [GraalVM 25.4 release notes](https://www.graalvm.org/release-notes/25.4/)
- [JEP 523: Make G1 the Default Garbage Collector in All Environments](https://openjdk.org/jeps/523)
- [JEP 544: Ahead-of-Time Code Compilation](https://openjdk.org/jeps/544)
- [GHSA-gmwr-7wmf-mrjm: langchain4j-agentic deserialization](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm)
- [a2a-java security advisories](https://github.com/a2aproject/a2a-java/security/advisories)
- [lampepfl/tacit](https://github.com/lampepfl/tacit)
- [arXiv 2603.00991: Tracking Capabilities for Safer Agents](https://arxiv.org/abs/2603.00991)
- [Tigris: We used a database as a message queue. Now we use Kafka](https://www.tigrisdata.com/blog/quick-fdb-kafka/)
- [NATS preliminary investigation report](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf)
- [NATS: preliminary report announcement](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/)
- [Google: Firebase Analytics outage post-mortem](https://firebase.blog/posts/2026/10/firebase-analytics-outage)
