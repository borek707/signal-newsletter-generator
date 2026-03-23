# SIGNAL
## What matters in distributed systems
March 2026 | Issue #3

**Welcome back.** Reddit just cut their comment latency in half by migrating from Python to Go. They used a technique called "tap-compare" that let them test in production without risking user data. Meanwhile, Microsoft announced plans to eliminate every line of C and C++ by 2030 using AI-assisted refactoring. Ambition level: one engineer, one month, one million lines of code.

**Also:** Robinhood's WarpStream migration is now a case study in cost-efficient log analytics, and the debate over MCP vs direct APIs is splitting the agent tooling world.

---

### **Today's Insights**

* Reddit's production testing strategy for language migrations
* Microsoft's AI-assisted Rust rewrite goals
* Diskless Kafka economics and latency trade-offs
* Why some teams are ditching MCP for CLI tools

---

##### **TODAY IN DISTRIBUTED SYSTEMS**

**Reddit halves comment latency with Go migration:** The engineering team completed their migration of the comment backend from Python to a domain-specific Go microservice. P99 latency for write operations dropped by 50%, eliminating spikes that previously reached 15 seconds. The migration used "tap-compare" testing: new Go services handled traffic internally but returned only Python responses to users, allowing safe discrepancy detection. For writes, Reddit deployed "sister datastores" — isolated mirrors of PostgreSQL, Memcached, and Redis — creating 18 separate validation paths across three write endpoints. [Read more](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/)

**Microsoft aims to eliminate C/C++ by 2030 using AI:** Distinguished Engineer Galen Hunt posted a goal to "eliminate every line of C and C++ from Microsoft by 2030" using AI agents and algorithmic code analysis. The stated North Star: "1 engineer, 1 month, 1 million lines of code." Hunt later clarified this is a research project for building migration technology, not an immediate Windows rewrite. Microsoft has invested ~$10M in Rust since 2022, with Azure CTO Mark Russinovich stating the company is "all-in" on memory-safe languages. [Read more](https://www.thecode.ai/p/microsoft-rust-2030)

**Robinhood's WarpStream migration cuts costs 80%:** The fintech completed their migration from Apache Kafka to WarpStream (now Confluent) for log analytics. The diskless architecture stores data directly in S3, eliminating inter-AZ networking fees and broker management. Robinhood now pays only for actual usage rather than maintaining static clusters. WarpStream reports sub-one-second P99 producer latency and sub-two-second end-to-end latency, though object storage introduces trade-offs for ultra-low-latency transactional workloads. [Read more](https://www.warpstream.com/blog/robinhood-case-study)

**IBM acquisition of Confluent pending:** The $25B acquisition announced December 2025 is awaiting regulatory approval. Confluent Platform remains the most feature-complete commercial Kafka distribution, with WarpStream now integrated for cost-sensitive workloads. IBM plans to maintain Confluent's open-source commitments while expanding enterprise reach. [Read more](https://www.conduktor.io/compare/kafka-alternatives)

---

##### **INSIGHT**

## **Why the MCP debate misses the point**

**A protocol backlash is brewing.** Perplexity CTO Denis Yarats revealed at Ask 2026 that the company is ditching MCP in favor of direct APIs and CLIs. The argument: tools like curl and git already live in model training data, so agents can use them without schema overhead.

**Not everyone needs a protocol.** For individual developers calling a few APIs, a lightweight CLI wrapper is often faster and more cost-effective than maintaining MCP servers.

**But the debate has a blind spot.** MCP runs in two modes. Stdio keeps servers local. Remote HTTP puts them on centralized infrastructure. Almost no one in the backlash separates the two. Centralized MCP gives teams one place to manage auth, track tools, and keep prompts consistent across agents.

**Built for the boring layer.** Smart teams play to strengths of both. They use CLIs when models already understand the tool, but pivot to MCP when they need unified auth, observability, and governance. The protocol got overhyped early, but its real story was always enterprise adoption.

---

##### **IN THE KNOW**

## **What's trending on socials and engineering blogs**

* **Diskless Kafka is rising:** Multiple vendors (WarpStream, Aiven KIP-1150, Confluent Freight) are pushing Kafka architectures that store data directly in object storage. Trade-off: latency increases, but costs drop 80%+. [Discussion](https://www.geeknarrator.com/blog/diskless-warpstream-confluentfreight)

* **Redpanda hits 10x lower latency:** C++ Kafka-compatible broker gains traction for latency-sensitive workloads where JVM-based Kafka is too heavy. [Repo](https://github.com/redpanda-data/redpanda)

* **Apache Spark Kubernetes Operator launches:** Official subproject launched May 2025, bringing Spark 3.5+ support to Kubernetes with rapid release cadence. [Details](https://lakefs.io/blog/the-state-of-data-ai-engineering-2025/)

* **Serialization hell is real:** Reddit engineers discovered Python couldn't deserialize data written by Go due to byte ordering and null handling differences. They added CDC event consumer validation to catch cross-language compatibility issues before production. [Source](https://blog.bytebytego.com/p/how-reddit-migrated-comments-functionality)

---

##### **AI CODING HACK**

## **How Reddit validated 18 paths without production risk**

When migrating writes across three datastores (Postgres, Memcached, Redis), Reddit couldn't use standard shadow traffic — comment IDs must be unique, and double-writing to production would violate constraints.

Their solution: **sister datastores**. Completely isolated mirrors that received only Go writes. The comparison flow:

1. Route write to Go microservice
2. Go calls Python to perform actual production write (user sees result)
3. Go writes to isolated sister datastores
4. System compares production vs sister data across all three stores
5. Log discrepancies, fix, repeat

This created 18 validation paths (3 endpoints × 3 datastores × 2 implementations) with zero risk to production data. The team also added CDC consumer validation: Python services attempted to deserialize events written by Go, catching serialization mismatches early.

---

##### **TOP & TRENDING RESOURCES**

### **Top Tutorial**

**[How Reddit orchestrates agent teams for complex migrations](https://www.infoq.com/news/2025/11/reddit-comments-go-migration/):** This case study covers practical strategies for zero-downtime language migrations, managing context across polyglot systems, and controlling costs when running duplicate infrastructure during transition periods.

---

### **Top Repo**

**[Bento](https://github.com/warpstreamlabs/bento):** WarpStream's actively maintained stream processing framework. Declarative data pipelines with 200+ connectors, recently rebranded with strict mode for production validation. Good for teams outgrowing basic Kafka Connect.

---

### **Trending Paper**

**[Automating skill acquisition of agentic repositories](https://arxiv.org/abs/2603.11808):** AI models struggle with complex, step-by-step tasks. This paper shows that automatically extracting skills from open-source code improves learning efficiency 40% while maintaining human-level quality. Relevant for teams building internal AI coding assistants.

---

##### **SCALAC ANGLE**

**On Reddit's approach:** We see teams attempt language migrations with insufficient validation. Reddit's 18-path testing strategy reveals the hidden complexity in seemingly simple CRUD operations. Budget 40% of your migration timeline for discrepancy detection. The serialization mismatches between Python and Go are typical — different languages make different defaults for byte ordering, null handling, and numeric precision. Test serialization round-trips before migrating a single byte of production data.

**On Microsoft's goal:** The "1 million lines per month" metric is an aspirational North Star, not an engineering baseline. We have seen similar promises from automated modernization vendors. Reality is typically 10-100x slower after accounting for testing, edge cases, and production validation. If considering automated translation, inventory modules by exploit history and test coverage first. Build differential testing infrastructure before running any translation. Treat translated code as a feature flag until proven safe.

**On diskless Kafka:** WarpStream's cost reduction is real, but the latency trade-off is non-negotiable. Object storage adds 100-500ms to read paths. For log analytics and observability, this is acceptable. For transactional event streaming where p99 latency must stay under 50ms, self-hosted Kafka or Redpanda remains the better choice. Match the architecture to the latency budget, not the marketing materials.

---

Signal is published by Scalac. We build distributed systems for teams who ship.

**Want deeper analysis?** Explore our case studies at scalac.io/case-studies  
**Subscribe:** Receive The Distributed Pulse monthly by signing up at scalac.io/newsletter
