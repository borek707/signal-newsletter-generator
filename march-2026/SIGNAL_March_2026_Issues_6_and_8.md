# SIGNAL — March 2026
## What matters in distributed systems
**Scalac** · [scalac.io](https://scalac.io) · Issues #6 + #8

---

# Issue #6 · March 2026

**Welcome back.** Reddit cut comment latency in half by migrating from Python to Go — and they did it without risking a single byte of production data. Scala 3.8 landed with a hard JDK 17 floor that's about to split the ecosystem. And Microsoft's Distinguished Engineer just declared war on every line of C and C++ in the company.

**Also:** Robinhood cut their Kafka bill 80% by going diskless. Scala Survey 2026 closes end of month.

---

##### THE ARCHITECTURE DEBATE

## Diskless Kafka: cost savior or latency trap?

WarpStream — now part of Confluent — throws out the broker disk entirely and writes directly to S3. Robinhood runs more than 10 TB/day of log analytics through it and reports an 80% cost reduction. No inter-AZ networking fees, no provisioned capacity sitting idle, stateless agents that scale without rebalancing partitions. For any workload that can tolerate a second of latency, the economics are hard to argue with.

The argument against is just as concrete. S3 adds 100–500ms to read paths, which means transactional event streaming that needs sub-50ms p99 simply won't work here. Teams that try to use WarpStream as a drop-in replacement for a latency-sensitive Kafka cluster discover this in production, not in testing. You end up running both systems anyway — which was supposed to be what you were escaping.

**Scalac angle:** We see the framing of this debate as the main problem. It's not "WarpStream or Kafka" — it's routing by workload. Logs and analytics go to WarpStream. Transactions and anything latency-sensitive go to Redpanda or MSK. Teams who wait for a single tool that does everything well are paying broker costs while they wait. Start with the 80% of your data that tolerates latency. The S3 economics will pay for the rest of the migration.

🔗 [Robinhood case study](https://www.warpstream.com/blog/robinhood-case-study) · [WarpStream joins Confluent](https://www.confluent.io/blog/confluent-acquires-warpstream/)

---

##### NOTES FROM THE TRENCHES

## How Reddit halved comment latency without touching production data

Reddit comments process the highest write throughput of any core model on the platform. 50 million+ daily users. One serialization mismatch doesn't cause a bug report — it corrupts data at scale. So when the team decided to migrate from Python to a Go microservice, the constraint was absolute: no double-writes to production.

Standard shadow traffic doesn't work for writes. Comment IDs must be unique. Early attempts exposed a subtler problem — Go wrote data that Python's deserializer couldn't read back. Database pressure spiked because Go wrote directly while Python's ORM applied hidden optimizations the new service didn't know about.

The solution was sister datastores: isolated mirrors of PostgreSQL, Memcached, and Redis running alongside production. The flow: a write hits the Go service, Go passes it to Python for the actual production write (so the user gets the Python result), then Go writes independently to the sister stores. Compare production data against sister data. Log every discrepancy. Fix. Repeat. This created 18 separate validation paths — 3 endpoints × 3 datastores × 2 implementations — and CDC event consumers validated cross-language deserialization on the way through. The team spent 40% of the migration timeline on this validation layer alone.

P99 latency for write operations dropped 50% after the cutover. Spikes that previously hit 15 seconds disappeared.

**Scalac angle:** Every language migration has a serialization layer that looks trivial until it isn't. Byte ordering, null handling, numeric precision — different languages make different defaults, and none of them fail loudly. Budget for the validation infrastructure before you write the first line of the new service. Reddit's 18-path structure isn't over-engineering; it's what production validation actually requires.

🔗 [Full write-up on InfoQ](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/)

---

##### SIGNAL OVER NOISE

## Three changes that matter this month

**Scala 3.8 requires JDK 17.** Released February 24, 2026. JDK 8 and 11 are no longer supported. The `betterFors` feature also stabilised with the release, changing how for-comprehensions desugar — code that returned `List` on Scala 3.7 now returns `Map` in certain cases, and the breaks are subtle enough to survive code review. The 3.3 LTS line stays on JDK 8 for now, but 3.9 LTS arrives in Q2 2026 with the same floor. That's the real deadline: plan the JDK upgrade before 3.9 forces the issue.
🔗 [Scala release blog](https://www.scala-lang.org/blog/releases/)

**Microsoft targets C/C++ elimination by 2030.** Distinguished Engineer Galen Hunt posted the goal publicly: "eliminate every line of C and C++ from Microsoft by 2030," with a stated North Star of "1 engineer, 1 month, 1 million lines of code." Hunt clarified afterward that this is research infrastructure for building migration tooling — not an immediate Windows rewrite. Azure CTO Mark Russinovich has separately confirmed the company is "all-in on memory safety." The engineering community's reaction was mostly skepticism: automated translation at this scale hasn't been proven anywhere.
🔗 [The Code](https://www.thecode.ai/p/microsoft-rust-2030)

**Stryker4s 0.20 adds Unix socket support.** The mutation testing framework for Scala now uses FS2 Unix domain sockets for test runner communication instead of TCP. Faster handshakes, lower overhead. Also adds Scala 3.8 dialect support. Released March 16, 2026 — worth adding to CI if your team doesn't already run mutation testing.
🔗 [Release notes](https://github.com/stryker-mutator/stryker4s/releases)

---

**Paper worth your time:** [Automating Skill Acquisition of Agentic Repositories](https://arxiv.org/abs/2603.11808) — automatically extracting reusable skills from open-source repos improves AI task completion efficiency by 40%. If your team is building internal coding assistants, this is the architecture pattern to benchmark against.

**Scala Survey 2026** closes end of March. Results directly shape the 3.9 LTS roadmap. Takes five minutes.
🔗 [Take the survey](https://contributors.scala-lang.org/t/new-scala-survey-2026/7398)

---

*Signal is published by [Scalac](https://scalac.io). [Case studies](https://scalac.io/case-studies) · [Subscribe](https://scalac.io/newsletter)*

---
---

# Issue #8 · March 2026

**Welcome back.** Perplexity's CTO announced they're abandoning MCP for direct APIs — and Hacker News lit up with 200+ comments arguing about whether that's a one-off or a signal. Meanwhile, Akka quietly rebranded as an agentic AI platform. And the Kafka diskless debate has a new data point: Confluent just bought WarpStream.

**Also:** Andrej Karpathy says he hasn't written code since December. The Scala Survey closes this week.

---

##### THE ARCHITECTURE DEBATE

## Diskless Kafka: the Confluent acquisition changes the calculus

The case for WarpStream's S3-backed architecture hasn't changed — no brokers, no rebalancing, Robinhood's 80% cost reduction on 10+ TB/day, sub-1s producer latency that's acceptable for log and analytics workloads. What changed in March is that Confluent acquired WarpStream, which resolves one of the main objections: proprietary control plane risk. It's now embedded in the most feature-complete commercial Kafka distribution.

The latency constraint remains real. S3 read paths carry 100–500ms overhead that transactional workloads requiring sub-50ms p99 can't absorb. Teams who run both high-throughput analytics and latency-sensitive transactions still need two systems. The acquisition doesn't fix the physics.

**Scalac angle:** The Confluent umbrella makes the WarpStream migration easier to justify to a procurement team, but it doesn't change the architecture decision. If your estate has mixed latency requirements, you're still splitting traffic — logs and analytics to WarpStream, transactions to Redpanda or MSK. What the acquisition does do is reduce the risk of starting that migration today.

🔗 [WarpStream + Confluent announcement](https://www.confluent.io/blog/confluent-acquires-warpstream/)

---

##### NOTES FROM THE TRENCHES

## How Reddit's sister datastores caught what shadow traffic misses

The core architecture was covered in Issue #6, but the detail that matters for teams considering a similar approach is what actually got caught by the validation layer — and how.

CDC event consumers sat downstream of both the production and sister datastores, reading every write event and attempting to deserialize Go-written data using the Python deserialization path. This wasn't a synthetic test. It ran on real production traffic, and it caught byte ordering assumptions that Go's binary encoding made differently from Python's struct module, null-versus-zero distinctions that Python's ORM had quietly normalised for years, and floating point precision inconsistencies that only appeared in edge case comment score calculations. None of these would have shown up in a feature-parity test suite. All of them would have corrupted data silently after cutover.

**Scalac angle:** The lesson isn't "build 18 validation paths." The lesson is that feature parity tests don't test serialization contracts. Before any language migration, run your actual write traffic through the new implementation and compare raw bytes at the deserialization layer. The round-trip test — write with Go, read with Python — is the one that exposes the hidden assumptions.

🔗 [InfoQ deep dive](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/)

---

##### SIGNAL OVER NOISE

## Three changes that matter this month

**Akka pivots to agentic AI.** Lightbend, now rebranded as Akka, launched four new components at the end of March: Orchestration for multi-agent workflows, Agents with MCP tool support, Memory as durable sharded state, and Streaming for real-time AI processing. All included in existing licenses. The positioning is direct — they're going after LangChain and LlamaIndex with enterprise SLAs and claimed 3× velocity at ⅓ the cost. The risk that hasn't gone away: the BSL license continues pushing teams toward the Apache Pekko fork. If you're evaluating Akka for net-new work, that fork decision needs to be resolved before you build.
🔗 [Full announcement](https://akka.io/blog/announcing-akkas-agentic-ai-release)

**Scala 3.8 requires JDK 17.** Same break as Issue #6, but if you haven't planned the JDK upgrade yet: the pragmatic dual-targeting approach is applications on Scala 3.8 + JDK 21 LTS, libraries on Scala 3.3 LTS until the ecosystem catches up. If you need to ship before migrating JDK, `-source:3.7` in `scalacOptions` buys time. The permanent fix for `betterFors` breakage is explicit `.toIterable` conversion on Map iterators in for-comprehensions.
🔗 [Scala 3.8 highlights](https://www.scala-lang.org/highlights/)

**Microsoft's C/C++ rewrite: the $10M reality check.** Azure has invested roughly $10M in Rust since 2022. The "1 million lines per engineer per month" figure is an aspirational research target — every team that has attempted automated code translation at scale reports 10–100× slower throughput once testing and edge cases are included. If you're evaluating automated migration tooling, the practical starting point is inventorying modules by exploit history and test coverage density first. Translation without a differential testing harness produces code that compiles but breaks production in ways no reviewer catches.
🔗 [The Code](https://www.thecode.ai/p/microsoft-rust-2030)

---

## Trending

**The MCP backlash.** Perplexity's CTO said publicly they're replacing MCP with direct API calls. The top Hacker News response: "MCP solves enterprise auth and governance problems that CLI wrappers fundamentally can't." 200+ comments, no consensus. The dividing line is use case: MCP overhead is irrelevant for internal tooling with fixed integrations; it earns its weight in multi-tenant enterprise environments. Worth reading before committing either direction.
🔗 [HN #34728910](https://news.ycombinator.com)

**Andrej Karpathy** posted that he hasn't written code since December — "everything is vibes coding with LLMs now." 2.5M views, debate still running on whether this is a productivity unlock or a deskilling signal.
🔗 [X thread](https://x.com/karpathy)

---

**Paper of the month:** [Automating Skill Acquisition of Agentic Repositories](https://arxiv.org/abs/2603.11808) — 40% efficiency gain by extracting reusable skills from open-source codebases. The architecture pattern matters for any team shipping internal AI coding tools.

**Repo of the month:** [stryker-mutator/stryker4s](https://github.com/stryker-mutator/stryker4s) — v0.20, Unix socket support, Scala 3.8 dialect, single-file HTML reports.

---

*Signal is published by [Scalac](https://scalac.io). [Case studies](https://scalac.io/case-studies) · [Subscribe](https://scalac.io/newsletter)*

---
---

<a name="images"></a>
## Obrazki wątków — źródła do wstawienia

| # | Temat | Plik lokalny | Źródło online |
|---|---|---|---|
| 1 | Reddit Python→Go migration | `reddit-migration-thumb.jpg` | [InfoQ artykuł](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/) |
| 2 | Stryker4s 0.20 | `stryker4s-thumb.jpg` | [GitHub releases](https://github.com/stryker-mutator/stryker4s/releases) |
| 3 | WarpStream / Kafka architecture | `kafka-logo.png` | [Confluent blog](https://www.confluent.io/blog/confluent-acquires-warpstream/) |
| 4 | arXiv paper | `arxiv-logo.png` | [arxiv.org/abs/2603.11808](https://arxiv.org/abs/2603.11808) |
| 5 | Apache Kafka logo | — | [Wikipedia Commons SVG](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Apache_kafka.svg/1200px-Apache_kafka.svg.png) |
| 6 | Scalac logo | `scalac-logo.png` | [scalac.io](https://scalac.io) |

> Pliki lokalne są w katalogu głównym repozytorium. Przed publikacją hostuj je pod docelowym URL i podmień ścieżki.
