# SIGNAL
## What matters in distributed systems
March 2026 | Issue #6

**Welcome back.** Reddit cut their comment latency in half by migrating from Python to Go, using a technique called "tap-compare" that let them validate in production without risking user data. Meanwhile, Scala 3.8.2 dropped with a breaking change: JDK 17 is now the minimum, and the new `betterFors` feature changes how for-comprehensions desugar. Microsoft also announced plans to eliminate C and C++ by 2030 using AI-assisted refactoring.

**Also:** Robinhood's WarpStream migration saves 80% on Kafka costs, and the Scala Survey 2026 closes end of month.

---

### **Today's Insights**

* Reddit's tap-compare testing strategy for zero-risk migrations
* Scala 3.8 breaking changes (JDK 17+, betterFors warnings)
* Microsoft AI-assisted Rust rewrite goals
* Diskless Kafka economics vs latency trade-offs

---

##### **TODAY IN DISTRIBUTED SYSTEMS**

**Reddit halves comment latency with Go migration:** The engineering team completed their migration of the comment backend from Python to a domain-specific Go microservice. P99 latency for write operations dropped by 50%, eliminating spikes that previously reached 15 seconds. The migration used "tap-compare" testing: new Go services handled traffic internally but returned only Python responses to users, allowing safe discrepancy detection. For writes, Reddit deployed "sister datastores" — isolated mirrors of PostgreSQL, Memcached, and Redis — creating 18 separate validation paths across three write endpoints. [Read more](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/)

**Scala 3.8.2 released with JDK 17 requirement:** The latest Scala version dropped February 24, 2026, and it breaks backwards compatibility for anyone still on JDK 8 or 11. Starting with 3.8, Java 17 is the minimum supported version. The change addresses JEP 471 (deprecated Object methods) and enables support for JDK 25+. The `betterFors` feature also stabilized, changing how for-comprehensions desugar—code that previously returned `List` now returns `Map` in certain cases. Teams face forced JVM upgrades and potential breaking changes in collection behavior. [Read more](https://www.scala-lang.org/blog/releases/)

**Microsoft aims to eliminate C/C++ by 2030 using AI:** Distinguished Engineer Galen Hunt posted a goal to "eliminate every line of C and C++ from Microsoft by 2030" using AI agents and algorithmic code analysis. The stated North Star: "1 engineer, 1 month, 1 million lines of code." Hunt later clarified this is a research project for building migration technology, not an immediate Windows rewrite. Microsoft has invested ~$10M in Rust since 2022, with Azure CTO Mark Russinovich stating the company is "all-in" on memory-safe languages. [Read more](https://www.thecode.ai/p/microsoft-rust-2030)

**Robinhood's WarpStream migration cuts costs 80%:** The fintech completed their migration from Apache Kafka to WarpStream (now Confluent) for log analytics. The diskless architecture stores data directly in S3, eliminating inter-AZ networking fees and broker management. Robinhood now pays only for actual usage rather than maintaining static clusters. WarpStream reports sub-one-second P99 producer latency and sub-two-second end-to-end latency, though object storage introduces trade-offs for ultra-low-latency transactional workloads. [Read more](https://www.warpstream.com/blog/robinhood-case-study)

---

##### **INSIGHT**

## **Why the JDK 17 requirement splits the Scala ecosystem**

**The upgrade forces a hard choice.** Scala 3.8's JDK 17 requirement reflects modern JVM reality—Java 8 is ancient (2014), and features like pattern matching and sealed classes require newer baselines. But enterprise reality is messy. Many banks and insurers still run JDK 8 in production, and library authors now face an uncomfortable decision.

**Target 3.8+ for new features, or stay on 3.3 LTS for reach?** The Scala Center promises 3.3 LTS support for at least a year after 3.9 releases (Q2 2026), but that clock ticks loudly. Smart teams are dual-targeting: applications on Scala 3.8 + JDK 21 (LTS), libraries on Scala 3.3 LTS until the ecosystem catches up.

**The risk is library stagnation.** If authors abandon 3.3 before enterprises migrate, the ecosystem fractures. VirtusLab offers free migration support, but cultural resistance to JDK upgrades often outweighs technical blockers. The pragmatic path is clear—upgrade your JDK before 3.9 LTS forces the issue—but execution remains painful for large enterprises.

---

##### **IN THE KNOW**

## **What's trending on socials and engineering blogs**

* **Scala Survey 2026 closes end of March:** VirtusLab and Scala Center collecting data on tooling preferences and migration blockers. Results will shape Scala 3.9 LTS roadmap. Takes 5 minutes to complete. [Source](https://contributors.scala-lang.org/t/new-scala-survey-2026/7398)

* **Stryker4s 0.20 adds Unix socket support:** Mutation testing framework leverages new FS2 Unix domain sockets for faster test runner communication. Also adds Scala 3.8 dialect support. Released March 16, 2026. [Source](https://github.com/stryker-mutator/stryker4s/releases)

* **Scala 3.9 LTS scheduled for Q2 2026:** Will succeed 3.3 as the new LTS line. Requires JDK 17+. 3.3 will receive patches for at least one year after 3.9 release. [Source](https://www.scala-lang.org/highlights/)

* **IBM acquisition of Confluent pending:** The $25B deal announced December 2025 awaits regulatory approval. Confluent Platform remains the most feature-complete commercial Kafka distribution. [Source](https://www.conduktor.io/compare/kafka-alternatives)

---

##### **DISTRIBUTED SYSTEMS HACK**

## **How to handle betterFors breaking changes in Scala 3.8**

Scala 3.8's `betterFors` optimization changes for-comprehension desugaring. If your code breaks:

**Option 1: Stay on 3.7 source level (temporary)**
```scala
scalacOptions ++= Seq("-source:3.7")
```

**Option 2: Explicit type conversions (permanent fix)**
Before (breaks in 3.8):
```scala
val result = for {
  (k, v) <- Map(1 -> 1, 2 -> 1)
  x = k + v
} yield (x, v)
// Returns List in 3.7, Map in 3.8
```

After (explicit):
```scala
val result: Iterable[(Int, Int)] = for {
  (k, v) <- Map(1 -> 1, 2 -> 1).toIterable
  x = k + v
} yield (x, v)
// Explicitly Iterable, consistent across versions
```

**Option 3: Enable warnings**
```scala
scalacOptions ++= Seq("-Werror")
```
The compiler now warns when multiple `val` assignments appear in for-comprehensions over Maps.

---

##### **TOP & TRENDING RESOURCES**

### **Top Tutorial**

**[How Reddit orchestrates agent teams for complex migrations](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/):** Case study covering practical strategies for zero-downtime language migrations, managing context across polyglot systems, and controlling costs when running duplicate infrastructure during transition periods.

---

### **Top Repo**

**[Stryker4s](https://github.com/stryker-mutator/stryker4s):** Mutation testing framework for Scala. Version 0.20 adds Unix socket support via FS2, Scala 3.8 dialect support, and improved HTML reporting. Good for teams adding mutation testing to CI pipelines.

---

### **Trending Paper**

**[Automating skill acquisition of agentic repositories](https://arxiv.org/abs/2603.11808):** AI models struggle with complex, step-by-step tasks. This paper shows that automatically extracting skills from open-source code improves learning efficiency 40% while maintaining human-level quality. Relevant for teams building internal AI coding assistants.

---

##### **SCALAC ANGLE**

**On Reddit's approach:** We see teams underestimate the validation phase of language migrations. Reddit's 18-path testing strategy reveals the complexity hidden in seemingly simple CRUD operations. Budget 40% of your migration timeline for discrepancy detection and reconciliation. The serialization mismatches between Python and Go are typical—different languages make different defaults for byte ordering, null handling, and numeric precision.

**On Scala 3.8 JDK requirement:** We see enterprise clients still running JDK 8 in production. The Scala 3.8 upgrade forces a JVM migration that many postponed for years. Budget 2-3 sprints just for JVM testing if you're coming from JDK 8. The LTS line (3.3) is your safety valve, but it won't last forever—plan the JDK upgrade before 3.9 LTS releases in Q2 2026. The betterFors change is subtle but dangerous—we caught similar collection type changes breaking Akka Streams expectations in client code.

**On Microsoft's goal:** The "1 million lines per month" metric is an aspirational North Star, not an engineering baseline. We have seen similar promises from automated modernization vendors. Reality is typically 10-100x slower after accounting for testing, edge cases, and production validation. If considering automated translation, inventory modules by exploit history and test coverage first. Build differential testing infrastructure before running any translation.

---

Signal is published by Scalac. We build distributed systems for teams who ship.

**Want deeper analysis?** Explore our case studies at scalac.io/case-studies  
**Subscribe:** Receive The Distributed Pulse monthly by signing up at scalac.io/newsletter
