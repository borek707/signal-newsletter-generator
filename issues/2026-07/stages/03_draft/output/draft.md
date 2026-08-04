---
description: >-
  SIGNAL Issue #5 -- July 2026. Value objects merge into OpenJDK mainline after a
  decade. Cloudflare builds consensus without timeouts. Kafka proposes RPO=0 for a
  price in write latency. And DBOS argues your database should be your workflow engine.
authors:
  - piotr_borkowicz
tags:
  - jvm
  - scala
  - kafka
  - valhalla
  - consensus
  - postgres
  - ai
title: 'SIGNAL July 2026: Valhalla Lands, Consensus Without Timeouts, and Postgres Comes for Your Workflow Engine'
date: '2026-08-04T09:00:00+02:00'
cover: ./cover.png
draft: true
---

# SIGNAL: What matters in distributed systems

**July 2026 | Issue #5**

Welcome back. Value objects merged into OpenJDK mainline after a decade of work,
Cloudflare built a consensus service that does not depend on timeouts, and Kafka
started proposing a way to buy zero-RPO disaster recovery with write latency. The
primitives everyone treated as settled are moving, and each move carries a price.
Below is a filter, not a firehose.

---

## Today: What to watch this month

- **[Value objects land in OpenJDK mainline.](https://github.com/openjdk/jdk/pull/31120)** A decade of Project Valhalla,
  roughly 197,000 lines of code, preview in JDK 28.

- **[Strict field initialization gets targeted for JDK 28.](https://openjdk.org/jeps/539)** Fields must be written
  before they are read, so default `0` and `null` stop being observable.

- **[Cloudflare builds consensus without timeouts.](https://blog.cloudflare.com/meerkat-introduction/)** Meerkat runs on QuePaxa,
  where any replica can drive consensus and no leader is required.

- **[Kafka proposes synchronous mirroring.](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring)** KIP-1360 offers RPO=0 across
  clusters and charges for it in write latency.

- **[Postgres wants your workflow engine's job.](https://www.infoq.com/presentations/dbos/)** DBOS argues the database is
  the orchestrator. Practitioners disagree about where that breaks.

- **[Prefect acquires Dagster.](https://dagster.io/blog/prefect-is-acquiring-dagster)** The two leading Airflow alternatives
  consolidate under one owner.

- **[A pipeline that was late, not slow.](https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/)** Worst-case freshness went from
  ten minutes to 30 seconds by changing the trigger, not the semantics.

---

## The Architecture Debate: Postgres Comes for Your Workflow Engine

**DBOS argues the database is already the orchestrator.** Jeremy Edberg makes the
pitch in [Compiling Workflows into Databases](https://www.infoq.com/presentations/dbos/): workflows are data, and
Postgres is good at managing data. Each step writes its checkpoint into ordinary
tables in the same transaction that does the work. `SKIP LOCKED` keeps workers off
each other. Postgres catches duplicate execution the way it catches any duplicate,
with an integrity constraint. The whole thing runs in-process as a library, so you
deploy no orchestrator service and nobody gets paged about one. One
adopter [put it plainly on Hacker News](https://news.ycombinator.com/item?id=44840693): "I evaluated Temporal, Trigger,
Cloudflare Workflows... this was the easiest to implement incrementally. Didn't
need to change our infrastructure at all."

**The exactly-once guarantee stops at the database boundary.** The phrase does more
work in marketing than in practice. Writing the step and its checkpoint in one
transaction gives you
exactly-once *for the database write*. A step that calls a third-party API and
crashes after the call but before the checkpoint commits will fire that call again
on recovery, as [an independent analysis of the approach](https://dev.to/contrite42/durable-workflows-on-postgres-what-you-dont-need-temporal-actually-buys-you-3o0f) sets out.
[Community pushback](https://finance.biggo.com/news/202510030712_DBOS_Developer_Skepticism_Exactly_Once_Processing) goes further on scope: the guarantee covers
workflow initiation only, and individual step execution stays the developer's
problem.

**Coupling is the second bill.** Workflow state in your primary database means
workflow load and application load compete for the same connections and the same
I/O. At modest volume that is a feature, because it is one less system to run and
back up. At high throughput a workflow spike starts competing with user queries.
Practitioners split on the operational side too. From the same thread: "Temporal
observability and UI was better than DBOS," and separately, DBOS's server-side
equivalent, Conductor, is not open source.

**Both sides of the market moved this month.** [Prefect acquired Dagster](https://dagster.io/blog/prefect-is-acquiring-dagster),
consolidating the two leading Airflow alternatives under one owner, with roughly 40
staff moving across and a commitment to keep developing the open-source project.
Databricks shipped [LTAP](https://www.databricks.com/blog/lakebase-ltap-rethinking-database-storage), separating OLTP and OLAP engines while sharing
storage, aimed at deleting change-data-capture pipelines between transactional
databases and warehouses. Orchestrator vendors consolidate while more of the
industry pushes work down into the transactional layer.

**Scalac angle:** Ask one question first, and it is not which tool is better.
Does your workflow load scale independently of your application load? High-fan-out
jobs and pipelines on their own schedule say yes, and that is what Temporal's
separation of orchestration from data store is for. Bounded workflow volume on
Postgres you already operate says no, and the library approach deletes a service
from your diagram. Either way, budget for idempotency keys on every outbound call.
The transaction protects what Postgres owns and nothing beyond it.

---

## Notes from the Trenches: The Pipeline Was Late, Not Slow

**The problem.** The team ran a delta index pipeline for ads and campaign search
across several million documents and tens of gigabytes, with fresh data arriving
every five to seven minutes and a full rebuild taking two to three hours plus
validation and deployment. Data that landed just after a scheduled run waited almost a full
interval before anything touched it. Any failure meant re-running the entire
window, even when only part of the data was incomplete.

**The diagnosis changed the fix.** The team's throughput was fine. Their
*scheduling cadence* was the bottleneck, and those two problems have different
solutions. Read the symptom as slow processing and you land on
record-level streaming, a rewrite with real operational risk. Read it as late
scheduling and the fix gets much cheaper.

**The fix.** They moved to Spark Structured Streaming on a fixed 30-second
trigger, with time-driven execution comparing the latest available partition
against a watermark. A freshness-first rule skips intermediate partitions and
takes the newest, which gives deterministic progress without depending on
completion markers that break. They also scheduled restarts every 24 hours and
handed job liveness to an external watchdog.

**The numbers.** End-to-end latency dropped roughly 50 percent. Worst-case
freshness lag went from about ten minutes to 30 seconds. The team's own summary,
from [the write-up](https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/): "The best streaming design is the one that works
reliably in production, not the one that looks the most elegant in theory."

**Scalac angle:** Measure whether your latency is processing or scheduling before
you touch semantics. If fresh data waits on a clock rather than on compute, a
trigger interval and a watermark will beat a rewrite to per-record processing, and
they will not hand you a new class of operational failure. Reach for record-level
streaming when per-record immediacy is the actual product requirement, not when
the dashboard looks stale.

---

## Signal Over Noise: Three Critical Changes This Month

### 1. The JVM renegotiates two fundamentals at once

[JEP 401, Value Classes and Objects, merged into OpenJDK mainline](https://github.com/openjdk/jdk/pull/31120) after roughly a
decade of Project Valhalla work and about 197,000 lines of code. Value objects
have no identity: two instances with equal fields are indistinguishable, which
frees the JVM to flatten and scalarize them. Fewer heap allocations, better cache
locality, less GC pressure for small immutable data.

In the same month, [JEP 539, Strict Field Initialization](https://openjdk.org/jeps/539), moved from Candidate to
Proposed to Target and then to Targeted for JDK 28. Strictly-initialized fields
must be written before they are read, so a default `0` or `null` can never be
observed. The two belong together. Stripping identity from the object model only
works if nobody can read an object half-built.

Migration path and the honest edge of the claim: both are preview features aimed
at JDK 28, which arrives March 2027, and both are opt-in. Brian Goetz has
[discouraged expecting JEP 401 to leave preview even in JDK 29](https://www.theregister.com/devops/2026/06/15/javas-project-valhalla-finally-lands-a-preview-in-jdk-28/5255557). One breaking
change deserves a grep today: code that synchronizes on `Integer` objects will
throw once those migrate to value classes.

### 2. Consensus without the tyranny of timeouts

[Cloudflare Research introduced Meerkat](https://blog.cloudflare.com/meerkat-introduction/), a global consensus service built on
QuePaxa rather than Raft. Raft detects a dead leader with a timeout, which forces a
choice Cloudflare's network makes hard: tune it short and replicas panic and block
writes on latency jitter, tune it long and the cluster sits idle through a real
failure. QuePaxa drops the dependency. Any replica can drive consensus for
the current slot, a leader exists only as an optimization worth one round trip
instead of three or more, and concurrent proposals converge rather than destroying
each other. [Arpit Bhayani's walkthrough](https://x.com/arpit_bhayani/status/2075218756499071037) is the clearest short explanation of
the mechanism.

Meerkat is not in production. Cloudflare has run proofs of concept with up to 50
replicas worldwide, built it in Rust with formal verification work underway, and
scoped it to small pieces of control-plane state such as leadership for replicated
databases. Cloudflare also did not invent QuePaxa, which comes from a 2023 SOSP
paper.

The [Hacker News thread](https://news.ycombinator.com/item?id=48831565) is worth reading alongside the announcement, because
the objections are specific. Comparing a leaderless protocol to Raft flatters it;
the honest comparison is against other Paxos-class leaderless protocols. And the
retry-and-abandon pattern trades Raft's timeout-bounded latency for a tail nobody
has bounded.

### 3. Kafka wants to sell you RPO=0

[KIP-1279 introduced asynchronous cluster mirroring](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring). KIP-1360 proposes the
synchronous version on top of it: a record counts as received only once all
in-sync replicas on all mirror clusters have it. That is what makes zero-RPO
disaster recovery possible, and it is also the entire cost. Every write now waits
on the slowest mirror cluster in the set.

Both are proposals. Nothing here has shipped, and the state matters: KIP freeze for
4.4.0 landed on 8 July with the release moving to September, per [Red Hat's Kafka
digest](https://developers.redhat.com/blog/2026/07/01/kafka-monthly-digest-june-2026). Treat this as a design direction to plan multi-region architecture
against, not a capability to promise anyone this quarter.

If you run multi-region Kafka today, make this decision on purpose instead of by
default. Name your actual RPO requirement, then price it in p99 write latency.
Teams who have never written that number down discover they have been buying
asynchronous replication and calling it disaster recovery.

---

## Community Voice

[Vincent Vauban](https://www.linkedin.com/posts/vvauban_jep-401-value-classes-and-objects-preview-activity-7483158484075655168-Zp3Q) walked through JEP 401 with code rather than
adjectives, and landed on an example worth borrowing: `value record
QuantizedWeight(byte value)`. Value classes give the JVM freedom to flatten
numeric domain types, which is exactly the shape of quantized model weights.
His framing of the guarantee is careful in a way most coverage was not: "JEP 401
enables these optimizations; it does not guarantee a particular memory layout."

---

## In the Know

**[Share Groups meet production](https://getkafkanated.substack.com/p/get-kafka-nated-espresso-july-2026)** -- Jack Vanlightly documented fetch failures under specific `record_limit` configurations, and Aiven's Olena Babenko published a deep dive on the elastic-scaling and per-message-control trade-offs. Kafka 4.3.1 separately fixed a RocksDB native memory leak in Streams (KAFKA-20616) that caused OutOfMemory errors in 4.3.0.

**[Chrome DevTools MCP v1.5.0 and v1.6.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases)** -- Two releases in one month. An agent gets DOM, console, network requests, and performance traces from a live browser, which moves MCP from handing agents data to letting them check whether the running system behaves.

**[Scala 3's separation checker](https://www.scala-lang.org/api/current/docs/experimental/capture-checking/separation-checking.html)** -- An extension of capture checking that enforces un-aliased access to capabilities, with `caps.Mutable` and an `update` modifier for state-mutating methods. Aimed at data races. Backed by the [System Capybara paper](https://arxiv.org/abs/2607.09383). Experimental and behind a language import.

**[sbt 2.0.3](https://eed3si9n.com/sbt-1.12.14-and-2.0.3)** -- Point releases through July following the 2.0 GA at the end of June. Plugin compatibility remains the migration question.

**[Project Leyden tightens agent rules](https://www.jvm-weekly.com/p/the-rest-of-the-story-july-edition)** -- JDK-8387190, targeting JDK 27, restricts what Java agents may do with the AOT cache: no appending to the bootstrap or system classloader search, no native agents, and `-javaagent` must stay identical across training and production. A Quarkus and PostgreSQL setup measured startup readiness falling from 1022.4ms to 380.3ms.

---

## Top Resources

**Repo to watch:** [GPULlama3.java](https://github.com/beehive-lab/GPULlama3.java)

GPU-accelerated Llama3 inference in pure Java through TornadoVM, now on Maven
Central with a CUDA backend and LangChain4j integration. Useful as a reference for
what the JVM can do with numeric AI workloads without dropping to Python.

**Article to read:** [Formal methods with Hillel Wayne](https://newsletter.pragmaticengineer.com/p/formal-methods-with-hillel-wayne)

The example that earns the read: AWS used TLA+ to find a defect whose shortest
error trace ran 35 steps, after design reviews, code inspection, and testing all
missed it. Wayne is also clear about where formal methods stop being practical.

**Paper to read:** [QuePaxa: Escaping the tyranny of timeouts in consensus](https://dl.acm.org/doi/10.1145/3600006.3613150)

SOSP 2023, by Tennage, Basescu and colleagues at EPFL. The protocol behind
Meerkat, laying out the normal-case fast path and the randomized asynchronous
core. [Open access copy here](https://bford.info/pub/os/quepaxa/).

---

Scalac is a software house that helps companies build high-throughput distributed
systems in Scala, Java, and Rust. We run the SIGNAL newsletter as a filter for
what actually matters in our stack.

**What is SIGNAL?** A monthly, opinionated newsletter for JVM and Scala teams who run real distributed systems. Each issue has three sections -- Architecture Debate, Notes from the Trenches, Signal Over Noise -- and focuses only on changes and incidents that matter in production, not on hype or vendor marketing.

Scalac builds high-throughput systems in Scala, Java, and Rust; SIGNAL is the filter we wish we had when making our own architecture bets.

**Got a story for SIGNAL?** Reply to this email. We read everything.

---

## References

- JEP 401: Value Classes and Objects (Preview). OpenJDK.
  https://openjdk.org/jeps/401

- Implement JEP 401: Value Objects (Preview). openjdk/jdk PR #31120.
  https://github.com/openjdk/jdk/pull/31120

- JEP 539: Strict Field Initialization in the JVM (Preview). OpenJDK.
  https://openjdk.org/jeps/539

- Java's Project Valhalla finally lands a preview in JDK 28. The Register, June 2026.
  https://www.theregister.com/devops/2026/06/15/javas-project-valhalla-finally-lands-a-preview-in-jdk-28/5255557

- JEP 401: Value Objects (Preview) merged to OpenJDK master. Hacker News.
  https://news.ycombinator.com/item?id=49119063

- Introducing Meerkat: an experiment in global consensus. Cloudflare Blog, July 2026.
  https://blog.cloudflare.com/meerkat-introduction/

- Cloudflare Meerkat: Globally distributed consensus. Hacker News.
  https://news.ycombinator.com/item?id=48831565

- QuePaxa: Escaping the tyranny of timeouts in consensus. SOSP 2023.
  https://dl.acm.org/doi/10.1145/3600006.3613150

- KIP-1279: Cluster Mirroring. Apache Kafka.
  https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring

- Kafka Monthly Digest. Red Hat Developer, July 2026.
  https://developers.redhat.com/blog/2026/07/01/kafka-monthly-digest-june-2026

- Get Kafka-Nated Espresso: July 2026.
  https://getkafkanated.substack.com/p/get-kafka-nated-espresso-july-2026

- Compiling Workflows into Databases: The Architecture That Shouldn't Work (But Does). InfoQ.
  https://www.infoq.com/presentations/dbos/

- Durable Workflows on Postgres: What "You Don't Need Temporal" Actually Buys You.
  https://dev.to/contrite42/durable-workflows-on-postgres-what-you-dont-need-temporal-actually-buys-you-3o0f

- DBOS Faces Developer Skepticism Over "Exactly-Once" Processing Claims.
  https://finance.biggo.com/news/202510030712_DBOS_Developer_Skepticism_Exactly_Once_Processing

- Build durable workflows with Postgres. Hacker News.
  https://news.ycombinator.com/item?id=44840693

- Prefect is Acquiring Dagster. Dagster Blog, July 2026.
  https://dagster.io/blog/prefect-is-acquiring-dagster

- Lakebase LTAP: Rethinking Database Storage. Databricks.
  https://www.databricks.com/blog/lakebase-ltap-rethinking-database-storage

- From Batch to Micro-Batch Streaming: Lessons Learned the Hard Way in a Delta Index Pipeline. InfoQ.
  https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/

- The Rest of the Story: July Edition. JVM Weekly Vol. 186.
  https://www.jvm-weekly.com/p/the-rest-of-the-story-july-edition

- Separation Checking. Scala 3 documentation.
  https://www.scala-lang.org/api/current/docs/experimental/capture-checking/separation-checking.html

- System Capybara: Tracking Capabilities for Separation and Freshness. arXiv.
  https://arxiv.org/abs/2607.09383

- sbt 1.12.14 and 2.0.3. eed3si9n.com.
  https://eed3si9n.com/sbt-1.12.14-and-2.0.3

- chrome-devtools-mcp releases. GitHub.
  https://github.com/ChromeDevTools/chrome-devtools-mcp/releases

- GPULlama3.java. GitHub.
  https://github.com/beehive-lab/GPULlama3.java

- Formal methods with Hillel Wayne. The Pragmatic Engineer, July 2026.
  https://newsletter.pragmaticengineer.com/p/formal-methods-with-hillel-wayne

- JEP 401: Value Classes and Objects (Preview). Vincent Vauban on LinkedIn, July 2026.
  https://www.linkedin.com/posts/vvauban_jep-401-value-classes-and-objects-preview-activity-7483158484075655168-Zp3Q

- QuePaxa explainer thread. Arpit Bhayani on X, July 2026.
  https://x.com/arpit_bhayani/status/2075218756499071037
