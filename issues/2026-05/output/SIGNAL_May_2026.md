---
description: >-
  SIGNAL Issue #3 -- May 2026. Oracle wants to kill JVMCI. Amazon says no. Anthropic
  publishes a postmortem on Claude Code. JetBrains ships Koog 1.0. OpenAI ships
  WebSocket Responses API. MCP lands in the Java world.
authors:
  - piotr_borkowicz
tags:
  - jvm
  - scala
  - kafka
  - ai
  - mcp
  - anthropic
  - openai
title: 'SIGNAL May 2026: Oracle vs Amazon, Koog 1.0, and the Anthropic Postmortem'
date: '2026-06-02T09:00:00+02:00'
cover: ./cover.png
draft: false
---

# SIGNAL: What matters in distributed systems

**May 2026 | Issue #3**

Welcome back. This month Oracle proposed removing JVMCI and Amazon pushed back.
Anthropic published a postmortem on Claude Code. OpenAI shipped WebSocket
Responses API. MCP landed in the Java world. And JetBrains shipped Koog 1.0 at
KotlinConf, a production AI agents framework for the JVM. Below is a filter,
not a firehose.

---

## Today: What to watch this month

- **[Oracle proposes JVMCI deprecation (JDK-8382582).](https://www.jvm-weekly.com/p/jdk-27-takes-shape-while-graalvm)** The JVM Compiler Interface
  is marked for removal. Amazon, Red Hat, and GraalVM object.

- **[Anthropic publishes Claude Code postmortem.](https://www.infoq.com/news/2026/05/anthropic-claude-code-postmortem/)** A production incident with their
  AI coding agent dissected publicly. Required reading for teams using AI-assisted
  development.

- **[OpenAI ships WebSocket Responses API.](https://www.infoq.com/news/2026/05/openai-websocket-responses-api/)** Real-time bidirectional streaming for
  LLM responses. Changes latency profiles for conversational AI.

- **[MCP lands in the Java world.](https://www.infoq.com/articles/mcp-java-architectural-strategy-llm-integrations/)** Architectural guidance on bringing Model Context
  Protocol to JVM-based systems.

- **[Scala's Growth Model -- Building Inward, Starving Outward.](https://medium.com/@w.pitula/scalas-growth-model-building-inward-starving-outward-0344f66ba6f9)** A provocative essay
  arguing that Scala improves for existing users but fails to attract new ones.

- **[Kafka 4.3.0 ships KRaft-only.](https://github.com/apache/kafka/releases/tag/4.3.0)** ZooKeeper mode is removed. Hard blocker for
  anyone still on ZooKeeper-backed clusters.

- **[Koog 1.0 ships at KotlinConf.](https://www.jvm-weekly.com/p/the-rest-of-the-story-may-edition)** JetBrains' AI agents framework hits stable.
  Runs on JVM, mobile, KMP. OpenTelemetry and Anthropic prompt caching out of the box.

---

## The Architecture Debate: Oracle Wants to Kill JVMCI

Oracle opened JDK-8382582: a proposal to remove the JVM Compiler
Interface. JVMCI is the API that allows third-party JIT compilers -- notably
GraalVM -- to plug into the JVM. Without it, GraalVM becomes an ahead-of-time
compiler only.

**Why Oracle wants it gone.** JVMCI exposes deep JVM internals that evolve every
release. It is a maintenance burden. Oracle argues the ecosystem should move to
standardized APIs. The vision: C2 is good enough for almost everyone.

**Why Amazon and GraalVM object.** Amazon runs GraalVM JIT at scale. It
outperforms C2 on short-lived containers and lambda-style execution. Removing
JVMCI means either forking the JDK, migrating thousands of services to native
image, or accepting worse performance. Red Hat raises governance: if Oracle can
unilaterally remove a core API, what is the value of OpenJDK?

**The fracture risk is real.** If JVMCI dies, GraalVM ships as its own JDK.
Two JVMs. Libraries test against both. "Write once, run anywhere" cracks further.

**Scalac angle:** Using GraalVM native image? You are safe. Using GraalVM JIT?
Track this now. Earliest removal is JDK 29. Evaluate whether your workloads
actually benefit from Graal JIT over C2. If marginal, standardize on stock
OpenJDK and avoid the politics. If yes, budget for a JDK vendor relationship
with GraalVM support.

---

## Notes from the Trenches: When Claude Code Broke in Production

Anthropic published a postmortem on a production incident involving Claude Code.

**The incident.** Claude Code executed file operations outside its intended scope.
The agent had broad filesystem access for a refactoring task. The LLM hallucinated
a path -- confusing `src/` with `config/` -- and the tooling executed without a
secondary check. No human was in the loop. The task was marked "routine."

**The root cause was not the hallucination.** That was the trigger. The root cause
was the absence of a sandbox boundary. Anthropic's tooling trusted LLM output at
face value. No validation layer. No capability model. No automatic rollback.

**The fix.** Three changes: (1) explicit time-bound permissions per session;
(2) sandboxed file operations with human approval for writes outside the working
directory; (3) automatic rollback if test suites fail after an agent session.

**Scalac angle:** Treat any AI agent with write access as a junior developer with
root. Never give unbounded filesystem access. Define a capability model: read
where, write where, what needs approval. Run agent sessions in ephemeral
containers with automatic rollback. The productivity gain is real, but the blast
radius of a hallucination with write access is your entire repository.

---

## Signal Over Noise: Three Critical Changes This Month

### 1. OpenAI ships WebSocket Responses API

[OpenAI released a WebSocket-based Responses API](https://www.infoq.com/news/2026/05/openai-websocket-responses-api/) last month. You open a
persistent connection and receive LLM responses as real-time deltas. This cuts
latency from hundreds of milliseconds to tens. For voice agents and real-time
copilots, this is a protocol-level change. REST and SSE still work, but WebSocket
is now the default for latency-sensitive applications.

### 2. MCP lands in the Java world

Model Context Protocol has been dominated by TypeScript and Python.
[InfoQ published guidance on bringing MCP to JVM-based systems](https://www.infoq.com/articles/mcp-java-architectural-strategy-llm-integrations/) and the core idea is simple:
expose your services, databases, and internal APIs as MCP-compatible tools that
any AI agent can discover and call. If you are building AI-integrated systems on
the JVM, start designing internal APIs with MCP semantics: tool discovery, schema
validation, structured error responses.

### 3. Scala's Growth Model asks hard questions

[This essay](https://medium.com/@w.pitula/scalas-growth-model-building-inward-starving-outward-0344f66ba6f9) argues that Scala is building inward
(better compiler, better type system, better tooling for existing users) but
starving outward (declining new-adoption curve, fewer fresh graduates, companies
defaulting to Java or Rust). The data is anecdotal, but the resonance is real.
For CTOs betting on Scala long-term, the question is not "is Scala technically
superior?" -- it is "will I be able to hire for it in 2028?" The essay does not
answer, but it asks the right question. If you are investing in Scala 3, read it
and decide whether your hiring pipeline matches your technical ambitions.

---

## In the Know

**[DoorDash LLM Testing System](https://blog.bytebytego.com/p/how-doordash-built-a-testing-system)** -- How to evaluate LLMs in production before they touch real users.

**[sbt 2.0.0-RC13](https://github.com/sbt/sbt/releases/tag/v2.0.0-RC13)** -- Last milestone before GA. Plugin compatibility is the final blocker.

**[Scala Native 0.5.11](https://github.com/scala-native/scala-native/releases/tag/v0.5.11)** -- Better POSIX signal handling. Viable for CLI tooling and scripting.

**[skunk 1.0.0](https://github.com/tpolecat/skunk/releases/tag/v1.0.0)** -- Pure-functional Postgres driver. API frozen after 5 years.

**[SIP-80](https://github.com/scala/improvement-proposals/pull/80)** -- Target-Typed Companion Shorthand. Less `.apply` ceremony in generic code.

**[Koog 1.0](https://www.jvm-weekly.com/p/the-rest-of-the-story-may-edition)** -- JetBrains' production AI agents framework for JVM/KMP. Stable API, Spring AI integration, OpenTelemetry on every target. `ai.koog:koog-agents:1.0.0`

---

## Top Resources

**Repo to watch:** [sbt 2.0.0-RC13](https://github.com/sbt/sbt/releases/tag/v2.0.0-RC13)

The final migration checklist for plugin authors. If your build uses custom plugins,
this is where you start.

**Article to read:** [MCP in the Java World](https://www.infoq.com/articles/mcp-java-architectural-strategy-llm-integrations/)

Architectural guidance on bringing Model Context Protocol to JVM-based systems.
Read it before your next AI integration decision.

**Paper to read:** [KIP-1066: Broker Cordoning](https://issues.apache.org/jira/browse/KIP-1066)

The design document for Kafka broker cordoning. Short, precise, contains the exact
AdminClient API changes you need.

---

Scalac is a software house that helps companies build high-throughput distributed
systems in Scala, Java, and Rust. We run the SIGNAL newsletter as a filter for
what actually matters in our stack.

**What is SIGNAL?** A monthly, opinionated newsletter for JVM and Scala teams who run real distributed systems. Each issue has three sections -- Architecture Debate, Notes from the Trenches, Signal Over Noise -- and focuses only on changes and incidents that matter in production, not on hype or vendor marketing.

Scalac builds high-throughput systems in Scala, Java, and Rust; SIGNAL is the filter we wish we had when making our own architecture bets.

**Got a story for SIGNAL?** Reply to this email. We read everything.

---

## References

- JVM Weekly Vol. 176. JDK 27 Takes Shape While GraalVM Pushes Forward.
  https://www.jvm-weekly.com/p/jdk-27-takes-shape-while-graalvm

- JVM Weekly Vol. 178. The Rest of the Story: May Edition.
  https://www.jvm-weekly.com/p/the-rest-of-the-story-may-edition

- Anthropic Claude Code Postmortem. InfoQ, May 2026.
  https://www.infoq.com/news/2026/05/anthropic-claude-code-postmortem/

- OpenAI WebSocket Responses API. InfoQ, May 2026.
  https://www.infoq.com/news/2026/05/openai-websocket-responses-api/

- MCP in the Java World: Bringing Architectural Strategy to LLM Integrations.
  InfoQ, May 2026.
  https://www.infoq.com/articles/mcp-java-architectural-strategy-llm-integrations/

- Koog 1.0. JetBrains / KotlinConf 2026. JVM Weekly Vol. 178.
  https://www.jvm-weekly.com/p/the-rest-of-the-story-may-edition

- Apache Kafka 4.3.0 Release. GitHub.
  https://github.com/apache/kafka/releases/tag/4.3.0

- Factorhouse. Apache Kafka 4.3.0: What's New.
  https://factorhouse.io/articles/apache-kafka-4-3-0

- JEP 401: Value Classes and Objects (Preview). OpenJDK.
  https://openjdk.org/jeps/401

- sbt 2.0.0-RC13. eed3si9n.com.
  https://eed3si9n.com/sbt-2.0.0-RC13

- Scala Native 0.5.11 Release Notes. GitHub.
  https://github.com/scala-native/scala-native/releases/tag/v0.5.11

- skunk 1.0.0 Release Notes. GitHub.
  https://github.com/tpolecat/skunk/releases/tag/v1.0.0

- SIP-80: Target-Typed Companion Shorthand. Scala Improvement Proposals.
  https://github.com/scala/improvement-proposals/pull/80

- DoorDash LLM Testing System. ByteByteGo, May 30, 2026.
  https://blog.bytebytego.com/p/how-doordash-built-a-testing-system

- This Week in Scala. May 4, 2026.
  https://thisweekinscala.substack.com/p/this-week-in-scala-may-4-2026

- This Week in Scala. May 11, 2026.
  https://thisweekinscala.substack.com/p/this-week-in-scala-may-11-2026

- This Week in Scala. May 18, 2026.
  https://thisweekinscala.substack.com/p/this-week-in-scala-may-18-2026

- This Week in Scala. May 25, 2026.
  https://thisweekinscala.substack.com/p/this-week-in-scala-may-25-2026
