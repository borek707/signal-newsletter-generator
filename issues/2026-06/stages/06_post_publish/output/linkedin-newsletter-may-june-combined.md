# SIGNAL, Catching Up: May + June 2026

We owe you an edition. May's SIGNAL never made it to LinkedIn, so here's both months in one: Oracle vs Amazon over JVMCI and an Anthropic postmortem from May, then GitHub's AI-agent capacity crisis and the fight over who owns your coding agent's harness from June.

Two months, two production stories, two architecture debates. Here's the filter.

## May: Oracle wants to kill JVMCI

Oracle opened a proposal to remove the JVM Compiler Interface, the API that lets GraalVM plug into the JVM as a JIT compiler. Their case: it exposes internals that change every release and is a maintenance burden. Amazon's case: they run GraalVM JIT at scale, it beats C2 on short-lived containers and lambda-style execution, and losing JVMCI means forking the JDK or migrating thousands of services to native image. Red Hat raised the governance question on top: if Oracle can unilaterally remove a core API, what's OpenJDK worth as a shared platform.

Earliest removal is JDK 29. If you're on GraalVM native image, you're unaffected. If you're on GraalVM JIT, check now whether the performance gain over C2 is real or marginal for your workloads, because that answer decides whether you standardize on stock OpenJDK or budget for a GraalVM vendor relationship.

## May, from the trenches: when Claude Code broke in production

Anthropic published a postmortem on an incident where Claude Code, given broad filesystem access for a refactoring task, hallucinated a path (confusing src/ with config/) and executed the change with no secondary check and no human in the loop. The root cause wasn't the hallucination, it was the missing sandbox: no validation layer, no capability model, no automatic rollback.

The fix: time-bound permissions per session, sandboxed writes requiring human approval outside the working directory, and automatic rollback if tests fail after an agent session. Treat any agent with write access like a junior developer with root, not a trusted pair of hands by default.

## June: who should own your coding agent's harness

Microsoft confirmed that GitHub Copilot CLI becomes the default agent harness for GitHub Copilot in JetBrains, deprecating the IDE's own local harness. The pitch: one harness means every surface gets new capabilities at the same time instead of a second implementation playing catch-up, and sessions now run independently in the background while the IDE just monitors. JetBrains placed the opposite bet the same week, shipping Mellum2, a self-hosted, on-premises model.

The tradeoff is real in both directions. One harness everywhere gets you faster feature parity, but it also means one vendor's roadmap, one cloud dependency, and an IDE reduced to a spectator on what the agent is actually doing to your codebase. Mellum2's pitch exists specifically for regulated environments and anyone who can't send code to someone else's cloud. Don't pick a harness on feature velocity alone: decide whether cloud dependency or audit-trail visibility is the constraint that actually binds for your team, then standardize on the bet that matches it.

## June, from the trenches: GitHub's infrastructure buckled under agent load

GitHub processed 1 billion commits in all of 2025. By April 2026, that pace hit 275 million commits a week. Claude Code alone went from about 100,000 commits a week in September 2025 to 2.6 million by April, a 25x jump in six months, and AI agent pull requests grew 325% over the same stretch. Infrastructure built for human-scale commit patterns buckled: outages, an 8.7-hour code search blackout, agent session wait times hitting 54 minutes against a normal baseline of 15-40 seconds. By June, availability had dropped below the 99.9% enterprise SLA threshold, and Microsoft started routing GitHub Actions runners and Codespaces to AWS, a competitor's cloud, as a bridge while Azure capacity expansion (18-24 months out) catches up.

The lesson generalizes past GitHub: capacity models built around human developer behavior don't transfer to agent-driven traffic. Agents commit more often and run in bursts tied to session length, not working hours. If you're scaling for agent workloads, load-test against agent-shaped traffic specifically, and have a real multi-cloud escape hatch ready before you need one. Microsoft had one. Building yours after the outage starts is too late.

## Also worth your attention

Kafka 4.3.1 closed a native memory leak in Kafka Streams that hit windowed RocksDB state stores hardest. JDK 27 locked its feature set, with compact object headers cutting heap use 22% in OpenJDK's own benchmarks and G1 becoming the default collector everywhere. Scala's codebase passed an independent security audit from Quarkslab with no critical findings. And OpenAI shipped a WebSocket Responses API cutting LLM response latency from hundreds of milliseconds to tens, while MCP got real architectural guidance for landing on the JVM.

Full May issue: [link]
Full June issue: [link]

---

Scalac builds high-throughput distributed systems in Scala, Java, and Rust. SIGNAL is the filter we wish we had when making our own architecture bets: no hype, no vendor marketing, just what changed and why it matters.

Got a story for SIGNAL, or living through one of these tradeoffs yourself? Drop a comment, we read everything.
