# SIGNAL May 2026: Oracle vs Amazon, Koog 1.0, and the Anthropic Postmortem

Oracle proposed removing JVMCI. Amazon pushed back. Anthropic published a postmortem on a Claude Code production incident. OpenAI shipped a WebSocket Responses API. MCP landed in the Java world. JetBrains shipped Koog 1.0 at KotlinConf.

This is SIGNAL, Scalac's monthly filter for what actually matters in distributed systems — not a news firehose. Three sections: an architecture debate, a story from production, and the changes worth your attention this month.

## The architecture debate: Oracle wants to kill JVMCI

Oracle opened JDK-8382582, a proposal to remove the JVM Compiler Interface. JVMCI is the API that lets third-party JIT compilers, GraalVM in particular, plug into the JVM. Without it, GraalVM becomes an ahead-of-time compiler only.

Oracle's case: JVMCI exposes deep JVM internals that change every release, it's a maintenance burden, and the ecosystem should move to standardized APIs. C2 is good enough for almost everyone.

Amazon's case: they run GraalVM JIT at scale, and it outperforms C2 on short-lived containers and lambda-style execution. Removing JVMCI means forking the JDK, migrating thousands of services to native image, or accepting worse performance. Red Hat raised a governance question on top of the technical one: if Oracle can unilaterally remove a core API, what's the value of OpenJDK as a shared platform?

If JVMCI goes, GraalVM ships as its own JDK. Two JVMs, tested separately, "write once, run anywhere" cracking further.

Earliest removal is JDK 29, so there's time. If you're on GraalVM native image, you're unaffected. If you're on GraalVM JIT, check whether your workloads actually benefit from Graal over C2 — if the gain is marginal, standardizing on stock OpenJDK avoids the politics entirely. If the gain is real, budget for a JDK vendor relationship with GraalVM support now.

## Notes from the trenches: when Claude Code broke in production

Anthropic published a postmortem on a production incident involving Claude Code. The agent had broad filesystem access for a refactoring task. It hallucinated a path, confusing src/ with config/, and the tooling executed the change without a secondary check. No human was in the loop. The task had been marked routine.

The hallucination wasn't the root cause, it was the trigger. The root cause was the absence of a sandbox boundary: no validation layer, no capability model, no automatic rollback. The tooling trusted the model's output at face value.

Anthropic's fix had three parts: time-bound permissions per session, sandboxed file operations with human approval required for writes outside the working directory, and automatic rollback if test suites fail after an agent session.

The takeaway for anyone running AI agents with write access: treat the agent like a junior developer with root. Define a capability model — what it can read, what it can write, what needs approval — and run sessions in ephemeral containers with automatic rollback. The productivity gain from agentic coding is real. So is the blast radius of a hallucination with write access to your entire repository.

## Signal over noise: three changes worth tracking

**OpenAI shipped a WebSocket Responses API.** A persistent connection delivering LLM responses as real-time deltas, cutting latency from hundreds of milliseconds to tens. REST and SSE still work, but WebSocket is now the default for voice agents and latency-sensitive copilots.

**MCP landed in the Java world.** InfoQ published architectural guidance for bringing Model Context Protocol to JVM-based systems. The core idea: expose services, databases, and internal APIs as MCP-compatible tools any agent can discover and call. If you're building AI-integrated systems on the JVM, start designing internal APIs with MCP semantics — tool discovery, schema validation, structured error responses — now.

**An essay asked whether Scala is starving its own pipeline.** ["Scala's Growth Model: Building Inward, Starving Outward"](https://medium.com/@w.pitula/scalas-growth-model-building-inward-starving-outward-0344f66ba6f9) argues Scala keeps improving for existing users while its new-adoption curve declines. The data is anecdotal, but the question is the right one for anyone betting on Scala long-term: not "is it technically superior," but "will I be able to hire for it in 2028?"

## Also worth a look

Kafka 4.3.0 shipped KRaft-only — ZooKeeper mode is gone, a hard blocker if you're still on ZooKeeper-backed clusters. JetBrains' Koog 1.0 hit stable at KotlinConf, a production AI agents framework for JVM and Kotlin Multiplatform with OpenTelemetry and Anthropic prompt caching built in. And DoorDash published how they test LLMs in production before real users see them, worth reading before your next AI integration decision.

---

Scalac builds high-throughput distributed systems in Scala, Java, and Rust. SIGNAL is the filter we wish we had when making our own architecture bets — no hype, no vendor marketing, just what changed and why it matters.

Got a story for SIGNAL, or running into JVMCI/GraalVM decisions yourself? Reply or drop a comment — we read everything.
