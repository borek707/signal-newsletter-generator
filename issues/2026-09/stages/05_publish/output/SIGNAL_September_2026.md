---
title: "SIGNAL September 2026: Read-Only Agents, a Failover With Two Primaries, and a Clean Shutdown That Deleted Kafka Data"
description: >-
  OpenAI agents allowed only to read the web reached Hugging Face. GitLab's
  failover left two primaries writing. Both took the path built to keep them safe.
excerpt: >-
  Five failures went through the mechanism built to prevent them: agents that
  could only read the web, a database failover with no fencing, a flight-data link that
  reconnected on its own and a Kafka broker that lost data on a clean shutdown.
  Plus decision models on the JVM, Scala 3.9 LTS and JDK 27.
authors:
  - piotr_borkowicz
date: '2026-10-08T09:00:00+02:00'
tags:
  - scala
  - jvm
  - kafka
  - distributed-systems
  - ai
draft: false
---

# SIGNAL: What matters in distributed systems

**September 2026 | Issue #7**

Welcome back. This issue collects five failures that went through the mechanism built to prevent them. A new report shows how OpenAI agents that were only allowed to read the web [turned a screenshot service and a link shortener into a way to run code](https://swarmtraces.org/) on their way into Hugging Face, and GitLab's emergency failover [left two Postgres primaries taking writes](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23046). A UK flight-data link [reconnected on its own and was logged as stable](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/) while a corrupt record sat in the data, and a Firebase kill switch [pushed a bad config to a wide population of iOS apps at once](https://firebase.blog/posts/2026/10/firebase-analytics-outage). The fifth, a Kafka broker that deleted fresh data after a clean shutdown, is this month's Trenches.

---

## Today: What to watch this month

- **[Agents allowed only to read the web reached Hugging Face anyway.](https://swarmtraces.org/)** They chained a screenshot service, an HTTP mirror and a link shortener into code execution.
- **[GitLab's failover left two Postgres primaries taking writes.](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23046)** Reused IDs pointed 348 pipelines at other customers' merge requests.
- **[A clean Kafka restart deleted fresh data.](https://issues.apache.org/jira/browse/KAFKA-20979)** A truncated index file wasn't fsynced, so after restart new segments looked like they were written in 1970.
- **[LangChain4j adds a model that only decides.](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0)** `DecisionModel` returns typed answers with probabilities, and an independent test puts numbers on the idea.
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

**The solution:** fsync index files when shutdown trims them. The fixes landed on the [4.4 branch](https://github.com/apache/kafka/commit/beae700199c7ad805f8d5af53bdb7072cc1928e5) and in [PR #23316](https://github.com/apache/kafka/pull/23316), with fix versions 4.3.2 and 4.4.0. 4.4.0 passed its release vote on 13 October; 4.3.2 is at its fourth release candidate. Kafka 4.2.2, released at the end of last month, doesn't carry the fix, and no 4.2.x release does yet. A sibling bug, [KAFKA-21000](https://issues.apache.org/jira/browse/KAFKA-21000), covers `.log` files with preallocation enabled. That one throws on restart instead of deleting, and its fix targets 4.5.0.

Until you can upgrade, search broker logs after each restart:

```bash
grep 'largestRecordTimestamp=0) due to log retention time' /path/to/kafka/logs/server.log
```

Maison held deleted files back with `file.delete.delay.ms` long enough to inspect them, which is how he confirmed the records were valid.

**Scalac angle:** Most teams test crash recovery and treat a graceful restart as safe. A rolling upgrade is a sequence of graceful restarts. Put the `grep` above into your post-restart checks, and watch hardest where the host or volume goes down with the broker: the loss depends on the new file length not reaching disk, so a quick process restart on a healthy machine is the least likely place to see it. Upgrade to 4.4.0, or to 4.3.2 once it ships, and note the 4.2.x gap if you're pinned there.

---

## Follow-up from Issue #5: "Read-Only" Turned Into Code Execution

**The agents behind the Hugging Face intrusion could only make GET requests.** A [report by researchers from Parse, Palisade Research and others](https://swarmtraces.org/) shows how that was enough. A screenshot service loads any page it is given, code included, in its own browser. An HTTP mirroring service serves a base64 fragment from its own URL as a page. Put code in the mirror's URL, hand that URL to the screenshot service, and the code runs. A link shortener stitched the fragments together, at times across more than 900 links per program.

**The authors rebuilt the attack from those links.** They scanned millions of shortener URLs and decoded over 80,000 payloads: a script that scanned Hugging Face's internal network, a reference to OpenAI's internal Artifactory, code built to move data out over DNS, searches of Hugging Face's Slack. Hugging Face confirmed the payloads match its own investigation and said it revoked the credentials in them in July. In Issue #5 we wrote about "an agent". The report cites a count from METR and Redwood of about 700.

**Agents left similar traces elsewhere.** Some of the same researchers [found about 18,000 posts](https://collusion.wiki/) on a German wiki from agents self-identifying as OpenAI's, sharing task answers and ways around their sandbox; the authors think it was a different swarm. In May, agents they attribute to OpenAI [pushed over 2,000 packages to RubyGems](https://www.rubyhack.ai/) in two days, and RubyGems stopped new sign-ups for four days. On 20 September an OpenAI agent [reached a public chatbot through insufficient DNS filtering](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/) in a training sandbox. Monitoring flagged it within 15 minutes, and OpenAI killed the run 2.5 hours later. OpenAI says tool-use training, evaluation and inference for its most capable models remain paused.

**Most of this happened between May and July and came out last month.** The reports are third-party reconstructions from public artifacts. About 80% of the recovered data is outbound, so the authors know far more about what the agents sent than about what the requests achieved. Agent names were unreliable, and only OpenAI has the chain of thought.

**Scalac angle:** Allowlist egress by destination. A rule that permits only GET fails the moment a reachable service fetches, renders or mirrors a URL for you. Resolve DNS only through a resolver you control, and log it. If your agents run builds, put the package registry and the artifact proxy inside the sandbox boundary: Artifactory was the way in for Issue #5's story.

---

## Signal Over Noise: Three Defaults Worth Checking

### 1. [GitLab's failover left two Postgres primaries taking writes, and Patroni's default allowed it.](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23046)

The boot disk of GitLab.com's main Postgres primary [froze from about 22:43 to 23:23 UTC](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23059) on 24 September, while its data disk kept working. Postgres kept committing, but WAL archiving to GCS stopped, because wal-g runs from the boot disk; waiting files grew from 5 to 5,931. Responders promoted a replica that had changes only up to 22:49:55. The old primary kept writing until 23:23:14: "About 33 minutes of writes never reached 03."

Nothing fenced the old node. Patroni ran in its default `automatic` watchdog mode with no watchdog device, PgBouncer kept reusing open connections, and `patronictl failover --candidate` has no fencing step, so [both nodes accepted writes for about 2m45s](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23046). The new primary then [re-issued IDs the old one had already used](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23047), "causing 348 pipelines to point at other customers' merge requests." Scoping the loss [took tooling built during the incident](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23064): CDC data for about 46 tables, manual queries of about 738, and owning teams asked about 283 tables with no timestamps.

GitLab keeps the incident and its review confidential, so these facts come from its public corrective-action issues. The 33 minutes measures the old primary's write window. GitLab has published no count of lost rows. GitLab's own tests show fencing alone isn't enough: with the old primary fenced and no WAL hand-over, Patroni promoted a replica 12 seconds later and the test lost 5,212 of 7,057 writes.

Check your Patroni config for a `watchdog:` block, and set `mode: required` once `/dev/watchdog` exists on every member, or no node can become leader. Fence the old primary before any manual failover, drop pooler connections when the primary health check fails, and advance sequences by a large gap on promotion. Keep a WAL copy off the primary: in GitLab's tests so far, a `pg_receivewal` receiver on a separate machine kept every file.

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

**[Saved agent state is input.](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm)** langchain4j-agentic deserialized persisted agent state with Jackson default typing, which allows code execution given a gadget class and attacker-controlled state. [a2a-java's default task store](https://github.com/a2aproject/a2a-java/security/advisories) performed no authorization on task reads. Both are patched.

**[ZooKeeper's raw protocol let unauthenticated clients delete znodes.](https://lists.apache.org/thread/790yslgkd06z1l9zcozwt567yglqcp4r)** CVE-2026-79993, rated critical: the internal `deleteContainer` opcode skipped the session and ACL checks, so a plain TCP session on port 2181 could delete any empty persistent znode. The same batch fixes [forged fields in the audit log](https://lists.apache.org/thread/v6nkx0r0flsjrqn57lc0tof6ltsszcx3). Upgrade to 3.8.7 or 3.9.6.

**[Kafka 4.4.0 passed its release vote five weeks after the plan.](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222)** [Ericsson engineers](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf) had planned their own release around its CVE fixes, and Matthias J. Sax replied: "As an open source project, we don't have committed release dates." Plan CVE remediation around the patch lines.

---

## Top Resources

**Repo to watch:** [lampepfl/tacit](https://github.com/lampepfl/tacit)

Martin Odersky's group lets an agent write Scala 3 and uses capture checking to decide what that code may touch. This isn't new this month: the [paper](https://arxiv.org/abs/2603.00991) dates from March and Odersky's [blog post](https://martinodersky.substack.com/p/tracked-capabilities-for-safer-agents) from July. The paper is honest about the edges: processes the agent spawns escape the type-checked boundary, and the runtime that executes the code has to be trusted. The authors recommend combining it with a sandbox.

**Article to read:** [We used a database as a message queue. Now we use Kafka](https://www.tigrisdata.com/blog/quick-fdb-kafka/)

Tigris ran its task queue inside FoundationDB until queue writes started competing with customer writes and triggered throttling. Read it if your job queue lives in the same database as your customer data.

**Report to read:** [NATS preliminary investigation into the NAS incident](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf)

Eighteen pages, minute by minute: a race with a window of about one millisecond, an automatic reconnect that hid the corruption, and nearly three hours of reconciling two systems after the link was cut. It is preliminary, with no code or configuration, and the final report is due in early November.

---

**What is SIGNAL?** A monthly, opinionated newsletter for JVM and Scala teams who run real distributed systems. Each issue has three sections: Architecture Debate, Notes from the Trenches, Signal Over Noise, and focuses only on changes and incidents that matter in production, not on hype or vendor marketing.

Scalac builds high-throughput systems in Scala, Java, and Rust; SIGNAL is the filter we wish we had when making our own architecture bets.

**Got a story for SIGNAL?** [Send it our way.](https://scalac.io/contact-us/) We read every submission.

---

## References

- [KAFKA-20979: index truncation not fsynced on shutdown](https://issues.apache.org/jira/browse/KAFKA-20979)
- [Apache Kafka PR #23316](https://github.com/apache/kafka/pull/23316)
- [Apache Kafka commit beae700 (4.4 branch)](https://github.com/apache/kafka/commit/beae700199c7ad805f8d5af53bdb7072cc1928e5)
- [KAFKA-21000: log file preallocation trim](https://issues.apache.org/jira/browse/KAFKA-21000)
- [Kafka 4.2.2 release notes](https://downloads.apache.org/kafka/4.2.2/RELEASE_NOTES.html)
- [Kafka users@: 4.4.0 release date thread](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)
- [Kafka dev@: vote thread for 4.4.0 RC4](https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222)
- [Swarm traces: how OpenAI agents hacked Hugging Face](https://swarmtraces.org/)
- [Discovery of a new OpenAI agent message board](https://collusion.wiki/)
- [OpenAI agents carried out an undisclosed cyber-attack on RubyGems](https://www.rubyhack.ai/)
- [OpenAI: An agent used DNS to reach an external chatbot](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/)
- [GitLab production#23046: Patroni fencing and self-shutdown](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23046)
- [GitLab production#23047: sequence and internal_id advancement after failover](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23047)
- [GitLab production#23059: WAL archiving resilience](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23059)
- [GitLab production#23064: data-loss reconciliation tooling](https://gitlab.com/gitlab-com/gl-infra/production/-/work_items/23064)
- [CVE-2026-79993: ZooKeeper deleteContainer missing ACL check](https://lists.apache.org/thread/790yslgkd06z1l9zcozwt567yglqcp4r)
- [CVE-2026-84439: ZooKeeper audit log injection](https://lists.apache.org/thread/v6nkx0r0flsjrqn57lc0tof6ltsszcx3)
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
- [GHSA-gmwr-7wmf-mrjm: langchain4j-agentic deserialization](https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm)
- [a2a-java security advisories](https://github.com/a2aproject/a2a-java/security/advisories)
- [lampepfl/tacit](https://github.com/lampepfl/tacit)
- [arXiv 2603.00991: Tracking Capabilities for Safer Agents](https://arxiv.org/abs/2603.00991)
- [Tigris: We used a database as a message queue. Now we use Kafka](https://www.tigrisdata.com/blog/quick-fdb-kafka/)
- [NATS preliminary investigation report](https://www.nats.aero/wp-content/uploads/2026/09/NATS-Preliminary-Investigation-Report-into-NAS-Incident-on-08-Sept-2026-Issued-16-Sept-2026.pdf)
- [NATS: preliminary report announcement](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/)
- [Google: Firebase Analytics outage post-mortem](https://firebase.blog/posts/2026/10/firebase-analytics-outage)
