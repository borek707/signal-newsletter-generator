---
title: 'SIGNAL August 2026: Source-First Scala, Living Service Maps, and Durable Agents'
description: >-
  Metals v2 makes source-first indexing a Scala monorepo design choice. Gradle
  and OpenJDK move production boundaries teams need to notice.
excerpt: >-
  Databricks puts a source-first index in Metals v2, while Netflix shows why a
  materialised service map may prefer complete data to fresh data. Plus Gradle
  Isolated Projects, Intel Mac support, JDK PEM encodings and durable agents.
authors:
  - piotr_borkowicz
date: '2026-09-14T09:00:00+02:00'
tags:
  - scala
  - jvm
  - kafka
  - observability
  - distributed-systems
  - ai
cover: ./cover.png
draft: false
---

# SIGNAL: What matters in distributed systems

**August 2026 | Issue #6**

Welcome back. Large Scala codebases are starting to treat the build as one source of truth among several, rather than the first thing an editor must wait for. Databricks put that bet into Metals v2. Netflix made a different choice in a system with millions of records: preserve the whole stream, let Kafka retain the pressure, and accept a temporarily older service map. Both choices move work to the boundary where failure is easier to see.

---

## Today: What to watch this month

- **[Metals v2 opens its source-first indexer.](https://www.databricks.com/blog/open-sourcing-metals-v2-databricks-java-and-scala-language-server-multi-million-line-codebases)** Databricks reports an index for 26 million lines of Scala and Java.
- **[Netflix builds a living dependency map.](https://medium.com/netflix-techblog/from-silos-to-service-topology-why-netflix-built-a-real-time-service-map-0165ba13a7bc)** eBPF flows, IPC metrics and traces each carry a different part of the answer.
- **[Gradle 9.7 promotes Isolated Projects.](https://docs.gradle.org/9.7.0/release-notes.html)** Parallel configuration has a path out of experiment, with stricter project boundaries.
- **[OpenJDK deprecates the macOS/x64 port.](https://openjdk.org/jeps/541)** Intel Mac build agents now carry a visible support risk on the road to JDK 28.
- **[A2A changes its standards home.](https://www.axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards)** Agent-to-agent interoperability moves closer to MCP under the Agentic AI Foundation.
- **[Temporal demonstrates durable LangGraph agents.](https://www.youtube.com/watch?v=jCHWup7-m8o)** A worker crash and an API failure become workflow history, retries and a resumed human approval.

---

## The Architecture Debate: Should an IDE Start From Sources or From the Build?

**[Databricks open-sourced Metals v2](https://www.databricks.com/blog/open-sourcing-metals-v2-databricks-java-and-scala-language-server-multi-million-line-codebases) for a monorepo with 26 million lines, 2.9 million symbols and 142,000 Scala, Java and Protobuf files.** Its source index builds before build-server synchronisation. Databricks reports a 22-second clean index build on 32 cores, then a five-second disk parse for a persisted index. A developer or coding agent can navigate the repository before the full build model arrives.

**The source-first case is responsiveness.** A large repository is a changing graph of code, generated sources, dependencies and tooling. Metals can parse source immediately, then use BSP for classpaths, generated sources, test metadata and debugging. That makes symbol search, file navigation and initial diagnostics available without treating build import as the front door.

**The build-first case is semantic correctness.** Generated code, compiler options, source roots and third-party dependencies remain facts the source tree cannot infer. Metals keeps BSP synchronisation for that reason. Its first result is a useful approximation. The post-sync compiler pipeline carries the answer an engineer needs before trusting a refactor or an AI-produced patch.

**The agent changes the cost of a stale model.** Databricks says 92% of its weekly active IDE users opened Cursor in July, while 12% opened IntelliJ. That does not prove Cursor is the better Scala IDE. It does show why fast repository orientation has become a production concern: an agent that sees an incomplete classpath can generate a confident, locally plausible change against the wrong model of the system.

**Scalac angle:** Large Scala estates should measure time to usable navigation separately from time to build-correct diagnostics. Pilot source-first indexing on one representative module, then gate automated refactors on a completed build sync and compiler diagnostics. Teams with heavy code generation should make that second gate explicit rather than expecting the editor to infer it.

---

## Notes from the Trenches: Netflix Lets Kafka Hold the Pressure

**Netflix's Service Topology is a production reference, not August launch news.** [Its original design](https://medium.com/netflix-techblog/from-silos-to-service-topology-why-netflix-built-a-real-time-service-map-0165ba13a7bc) starts from a simple problem: a static dependency diagram cannot answer a 3am question. The system builds separate graphs from kernel-level eBPF network flows, application IPC metrics and distributed traces. Each source has a blind spot, so Netflix lets engineers query a layer independently or merge the layers for a unified view.

**The raw network graph lies by omission.** A flow log records App A to a load balancer and the load balancer to App B. Netflix needs App A to App B. Its pipeline consumes multi-region Kafka flow records, aggregates them, resolves intermediaries such as load balancers and NAT gateways, then enriches and persists the direct application relationship.

**[Three stages protect the hot path.](https://www.infoq.com/news/2026/08/netflix-service-topology/)** The staged design keeps intermediary resolution apart from final enrichment and persistence. InfoQ's account of Netflix's production implementation says an intermediary can see 100 times the traffic of a normal application. Separating the work stops a few hot nodes from concentrating CPU and I/O on a small part of the fleet.

**Freshness loses to completeness under write pressure.** When graph storage slows, backpressure travels through Apache Pekko Streams to the Kafka consumer. Consumption pauses and Kafka retains the records until capacity returns. The map gets older. It does not silently forget edges. Netflix also describes replacing gRPC between internal pipeline stages with SSE at this volume, while retaining a gRPC API for clients.

**Scalac angle:** For any graph or materialised view built from Kafka, decide which is worse before an incident: delayed freshness or an incomplete answer. If completeness wins, propagate backpressure to the consumer, alarm on lag and surface the map's freshness to users. If freshness wins, record exactly which events you discard and how the view will reconcile later.

---

## Signal Over Noise: Three Changes With a Migration Path

### 1. [Gradle turns Isolated Projects into an incubating feature.](https://docs.gradle.org/9.7.0/release-notes.html)

Gradle 9.7 moves Isolated Projects beyond its experimental status. It isolates project configuration and exposes cross-project mutable-state access as a problem, which enables parallel configuration only after a build is compatible with the configuration cache. Start with diagnostics in CI. Do not switch production build artifacts to the incubating mode until plugins and convention code pass cleanly.

### 2. [JDK 28 deprecates the macOS/x64 port.](https://openjdk.org/jeps/541)

Oracle stopped maintaining the Intel Mac port as of JDK 27. JEP 541 integrates a deprecated-port path for JDK 28, where builds require an explicit `--enable-deprecated-ports` flag and remain unsupported. Audit macOS runners and developer fleets now. Apple Silicon or Linux CI is the durable route.

### 3. [PEM encodings head toward finalisation in the JDK.](https://openjdk.org/jeps/542)

JEP 542 proposes finalising the PEM API after three preview rounds. It will not replace a certificate-management system, but it gives JVM services a standard route for common key and certificate encodings. Keep existing parsing code until the final JDK release lands, then use one compatibility test suite to compare errors and accepted input across old and new paths.

---

## Community Voice

The [r/scala discussion on Metals v2](https://www.reddit.com/r/scala/comments/1vm99gu/databricks_opensourcing_metals_v2_for_large/) shows a maintainer pointing to Scala Days as the target for a final release, with more Scala 3 improvements still under evaluation. The useful reading is narrower: large Scala codebases have enough distinct constraints to move language-server architecture, and the work is still in motion.

---

## In the Know

**[Simple JSON API reaches JDK 28.](https://openjdk.org/jeps/540)** The incubating API targets RFC 8259 use cases and explicitly does not replace full JSON libraries such as Jackson.

**[PEM encodings head toward finalisation.](https://openjdk.org/jeps/542)** OpenJDK proposes finalising the API after three preview rounds. Teams that parse certificates by hand should track the boundary, not schedule a migration from a proposal.

**[A2A moves to the Agentic AI Foundation.](https://www.axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards)** The transfer does not change a running system this week, but it brings agent-to-agent interoperability closer to MCP's standards home.

**[Confluent expands managed Kafka capacity controls.](https://www.confluent.io/blog/2026-q3-confluent-cloud-launch/)** The Q3 update adds higher eCKU limits, follower fetching and network controls. Treat it as an operations review item, not evidence that a workload needs a managed migration.

---

## Top Resources

**Repo to watch:** [Metals](https://github.com/scalameta/metals)

The open source language server behind the source-first work in this issue. Read the code and issue tracker beside the Databricks post before assuming its monorepo constraints match your own.

**Paper to read:** [Self-evolving Agentic Customer Support System at LinkedIn](https://arxiv.org/abs/2608.10224)

LinkedIn reports a two-week randomised production test of a versioned loop around retrieval, prompts and evaluation. The paper is useful because it gives the evaluation system equal weight with the agent behaviour.

**Tutorial to watch:** [Building Distributed Agents with LangGraph + Temporal](https://www.youtube.com/watch?v=jCHWup7-m8o)

An 11-minute failure demo rather than a framework tour. It kills workers, forces API failures and walks through recovery plus human approval, which makes the durable-execution boundary visible.

---

**What is SIGNAL?**

SIGNAL is a monthly, opinionated newsletter for engineers building and operating JVM and Scala systems, and agentic AI in production.

Each issue has three sections: Architecture Debate, Notes from the Trenches, and Signal Over Noise. They cover architecture decisions, production lessons, incidents, and ecosystem shifts worth paying attention to. No hype. No vendor talking points.

At Scalac, we build high-throughput distributed systems and agentic AI products in Scala, Java, and Rust. SIGNAL is the filter we wanted when making our own architecture bets.

**Have a story for SIGNAL?** Reply to this email. We read every response.

---

## References

- [Databricks: Open-sourcing Metals v2](https://www.databricks.com/blog/open-sourcing-metals-v2-databricks-java-and-scala-language-server-multi-million-line-codebases)
- [Netflix: From Silos to Service Topology](https://medium.com/netflix-techblog/from-silos-to-service-topology-why-netflix-built-a-real-time-service-map-0165ba13a7bc)
- [InfoQ: How Netflix Scaled its Real-Time Service Map](https://www.infoq.com/news/2026/08/netflix-service-topology/)
- [Gradle 9.7 release notes](https://docs.gradle.org/9.7.0/release-notes.html)
- [JEP 541: Deprecate the macOS/x64 Port](https://openjdk.org/jeps/541)
- [JEP 540: Simple JSON API](https://openjdk.org/jeps/540)
- [JEP 542: PEM Encodings](https://openjdk.org/jeps/542)
- [A2A moves to the Agentic AI Foundation](https://www.axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards)
- [LinkedIn: Self-evolving Agentic Customer Support System](https://arxiv.org/abs/2608.10224)
- [Building Distributed Agents with LangGraph + Temporal](https://www.youtube.com/watch?v=jCHWup7-m8o)
