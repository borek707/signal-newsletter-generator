# SIGNAL
## What matters in distributed systems
March 2026 · **Scalac** · [scalac.io](https://scalac.io)

---

**Welcome back.** Confluent just bought WarpStream and changed the Kafka cost calculus for every team still running brokers. Scala 3.8 landed with a hard JDK 17 floor and a for-comprehension change subtle enough to slip through code review. And Akka launched an agentic AI platform the same week Perplexity's CTO publicly dumped MCP — the protocol Akka just built its whole new stack around.

**Also:** Reddit halved comment write latency by migrating from Python to Go without a single double-write to production. Microsoft declared war on every line of C and C++ in the company.

---

##### THE ARCHITECTURE DEBATE

## Diskless Kafka: the Confluent acquisition changes the calculus

WarpStream throws out the broker disk entirely and writes directly to S3. Robinhood runs more than 10 TB/day of log analytics through it and cut costs 80%. No inter-AZ networking fees, no provisioned capacity sitting idle, stateless agents that scale without rebalancing partitions. For any workload that tolerates a second of end-to-end latency, the economics are genuinely hard to argue with.

The latency constraint hasn't moved. S3 adds 100–500ms to read paths, which means transactional event streaming requiring sub-50ms p99 can't use this architecture. Teams that discover this in production — rather than in testing — end up running two systems anyway, which was supposed to be what they were escaping.

What changed in March is that Confluent acquired WarpStream. That resolves one of the main blockers for enterprise adoption: proprietary control plane risk. It's now inside the most feature-complete commercial Kafka distribution, which makes the migration considerably easier to justify internally.

**Scalac angle:** The framing was always wrong. It was never WarpStream or Kafka — it's routing by workload. Logs and analytics to WarpStream, transactions to Redpanda or MSK. The Confluent acquisition doesn't change the architecture decision, but it does reduce the risk of starting the migration today. Teams who keep waiting for one tool to serve every latency tier are paying unnecessary broker costs while they wait.

🔗 [Robinhood case study](https://www.warpstream.com/blog/robinhood-case-study) · [WarpStream joins Confluent](https://www.confluent.io/blog/confluent-acquires-warpstream/)

---

##### NOTES FROM THE TRENCHES

## How Reddit migrated 50M users' data without a single double-write

Reddit comments run the highest write throughput of any core model on the platform. One serialization mismatch doesn't file a bug report — it corrupts data at scale. So when the team migrated the comment backend from Python to Go, the constraint was absolute: no double-writes to production.

The first approach failed immediately. Standard shadow traffic doesn't work for write migrations because comment IDs must be unique. Early attempts also exposed a subtler problem: Go wrote data that Python's deserializer couldn't read back. Database pressure spiked because Go wrote directly to storage while Python's ORM applied hidden optimizations the new service didn't know about.

The solution they landed on was sister datastores — isolated mirrors of PostgreSQL, Memcached, and Redis running in parallel. A write would hit the Go service, which would pass it to Python for the actual production write, then write independently to the sister stores. Compare, log discrepancies, fix, repeat. CDC event consumers sat downstream reading every write event and attempting to deserialize Go-written data through the Python path — catching byte ordering assumptions, null-versus-zero distinctions the ORM had silently normalised for years, and floating point precision differences that only appeared in edge case comment score calculations. None of those would have shown up in a feature-parity test suite. All of them would have corrupted data silently after cutover. The team spent 40% of the migration timeline on this validation layer. P99 write latency dropped 50%. Spikes that reached 15 seconds disappeared.

**Scalac angle:** The lesson isn't the 18-path validation structure. The lesson is that feature parity tests don't test serialization contracts. Before any language migration, run real write traffic through the new implementation and compare raw bytes at the deserialization layer. The round-trip test — write with Go, read with Python — is the one that finds the hidden assumptions.

🔗 [Full write-up on InfoQ](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/)

---

##### SIGNAL OVER NOISE

**Scala 3.8 requires JDK 17, and the silent break is worse than the obvious one.** Released February 24, 2026. JDK 8 and 11 are out. That's the obvious break, and most teams saw it coming. The one that slips through is `betterFors`: for-comprehensions over Maps now return `Map` instead of `List` in certain cases, and the type mismatch is subtle enough to pass code review without failing tests. The 3.3 LTS line stays on JDK 8 for now, but 3.9 LTS lands in Q2 2026 with the same floor. That's the real deadline. `-source:3.7` buys time; explicit `.toIterable` on Map iterators is the permanent fix.
🔗 [Scala release blog](https://www.scala-lang.org/blog/releases/)

**Akka launched an agentic AI platform the same week MCP's reputation took a hit.** Lightbend, now rebranded as Akka, shipped four new components: Orchestration, Agents with MCP tool support, Memory as durable sharded state, and Streaming. All included in existing licenses. The same week, Perplexity's CTO announced they're replacing MCP with direct API calls, and Hacker News lit up with 200+ comments. The divide: MCP overhead doesn't matter for internal tooling with fixed integrations, but it earns its weight in multi-tenant environments that need centralised auth, observability, and governance — exactly the enterprise context Akka is targeting. The risk that hasn't changed: the BSL license continues pushing teams toward Apache Pekko. The fork decision needs to be made before you build anything new on Akka.
🔗 [Akka announcement](https://akka.io/blog/announcing-akkas-agentic-ai-release) · [MCP debate on HN](https://news.ycombinator.com)

**Microsoft's C/C++ goal is research, not a roadmap — but it matters for Rust adoption.** Distinguished Engineer Galen Hunt posted the goal publicly: eliminate every line of C and C++ from Microsoft by 2030, "1 engineer, 1 month, 1 million lines of code." Hunt clarified afterward that this is tooling research, not an immediate Windows rewrite. Azure CTO Mark Russinovich has separately confirmed the company is all-in on memory safety. The engineering reaction was predictably skeptical — automated translation at scale hasn't been proven anywhere, and real-world numbers run 10–100× slower than any aspirational baseline. If you're evaluating migration tooling, inventory modules by exploit history and test coverage before running any translation. Build the differential testing harness first.
🔗 [The Code](https://www.thecode.ai/p/microsoft-rust-2030)

---

##### IN THE KNOW

**@stryker_mutator · March 16, 2026 · 45 likes**
Stryker4s 0.20 is out. Unix socket support via FS2, Scala 3.8 dialect, single-file HTML reports. The replies split immediately on whether mutation testing is worth the CI overhead for functional codebases. Short answer: if your suite runs under 10 minutes, the overhead is noise and the signal is real.
🔗 [Release](https://github.com/stryker-mutator/stryker4s/releases)

**contributors.scala-lang.org · closes March 31, 2026**
Scala Survey 2026 is in its last days. VirtusLab and the Scala Center are asking about tooling preferences, migration blockers, Cats Effect vs ZIO vs stdlib. Last year's survey put Scala 3 adoption at 92%. This year's results shape the 3.9 LTS roadmap. Five minutes.
🔗 [Take the survey](https://contributors.scala-lang.org/t/new-scala-survey-2026/7398)

---

##### TOP RESOURCES

**Repo of the month — [stryker-mutator/stryker4s](https://github.com/stryker-mutator/stryker4s)**
Mutation testing framework for Scala. v0.20 brings Unix socket support, Scala 3.8 dialect, and single-file HTML reports. If you're going to add mutation testing to CI, this release makes the overhead argument significantly harder to justify skipping it.

**Paper of the month — [Automating Skill Acquisition of Agentic Repositories](https://arxiv.org/abs/2603.11808)**
AI models fail on complex multi-step tasks because they lack reusable procedural knowledge. This paper shows that automatically extracting standardised skills from open-source repositories improves task completion efficiency by 40% while staying at human-level output quality. If your team is building internal coding assistants or agent tooling on top of JVM infrastructure, the skill extraction architecture here is the baseline to benchmark against.

---

*Signal is published by [Scalac](https://scalac.io). We build distributed systems for teams who ship.*
[Case studies](https://scalac.io/case-studies) · [Subscribe](https://scalac.io/newsletter)

---

## Obrazki do wstawienia

| Temat | Plik lokalny | Źródło online |
|---|---|---|
| Reddit Python→Go migration | `reddit-migration-thumb.jpg` | [InfoQ](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/) |
| WarpStream / Kafka | `kafka-logo.png` | [Confluent blog](https://www.confluent.io/blog/confluent-acquires-warpstream/) |
| Stryker4s 0.20 | `stryker4s-thumb.jpg` | [GitHub releases](https://github.com/stryker-mutator/stryker4s/releases) |
| Scalac logo | `scalac-logo.png` | [scalac.io](https://scalac.io) |
