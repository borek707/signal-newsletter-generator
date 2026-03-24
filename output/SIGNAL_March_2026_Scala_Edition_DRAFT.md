# SIGNAL
## What matters in distributed systems
March 2026 | Issue #4 — Scala Edition

**Welcome back.** Akka just pivoted hard into agentic AI, launching a full platform for orchestrating multi-agent systems. Meanwhile, Scala 3 adoption hit 92% among surveyed teams, but migration stories reveal the real cost: one engineer spent a week just preparing a codebase to avoid merge conflicts. Also, the Akka-to-Pekko exodus continues as teams dodge the BSL license.

**Also:** Scala.js enables genuine full-stack development, Ziverge sponsors backend WASM for Scala, and Cats Effect 3.6 drops with improved fiber scheduling.

---

### **Today's Insights**

* Akka's agentic AI pivot and what it means for existing users
* Real-world Scala 3 migration strategies (and pitfalls)
* BSL license fallout: Pekko gains traction
* Scala ecosystem health: AI integration, WASM, full-stack

---

##### **TODAY IN DISTRIBUTED SYSTEMS**

**Akka launches Agentic AI Platform:** The company formerly known as Lightbend introduced a comprehensive platform for building agentic AI systems. Four new components: Akka Orchestration (multi-agent workflows), Akka Agents (goal-directed agents with MCP tool support), Akka Memory (durable sharded state with nanosecond writes), and Akka Streaming (real-time processing for ambient AI). CEO Tyler Jewell claims 3X velocity and ⅓ the cost of other approaches. The move positions Akka against LangChain and LlamaIndex, but with enterprise SLAs for certainty and recovery. All features included in existing licenses. [Read more](https://akka.io/blog/news-akka-introduces-agentic-ai-platform)

**Scala 3 adoption reaches 92% in production:** The State of Scala 2025 survey reveals nearly all teams use Scala 3 partially or fully, with ~50% having migrated production systems. Finance leads adoption (largest segment), followed by e-commerce and analytics. Scala Days 2025 saw 20% new attendees—fresh interest in the ecosystem. Key drivers: streamlined syntax, stronger type safety, new metaprogramming. Migration friction remains the main blocker for holdouts. [Read more](https://scalac.io/blog/scala-days-2025-recap-a-scala-community-reunion/)

**Scala 3 migration war stories emerge:** SoftwareMill published a detailed guide on cross-building—compiling the same codebase against both Scala 2.13 and 3.x—to enable gradual migration. Key technique: `ThisBuild / crossScalaVersions := Seq("2.13.20", "3.3.6")` with version-specific source directories (`src/main/scala-2`, `src/main/scala-3`). Meanwhile, Pierre Ricadat documented his team's failed first attempt: one week of work, thousands of lines changed, IDE unresponsive from compile errors, merge conflicts overwhelming. Second attempt succeeded by applying `-Xsource:3` changes to the Scala 2 main branch first, avoiding conflicts. [Read more](https://softwaremill.com/migrating-to-scala-3/)

**Digital.ai completes Akka-to-Pekko migration:** The DevOps platform migrated Deploy from Akka to Apache Pekko starting version 24.1. Pekko graduated to Apache Top-Level Project in May 2024 as the community fork of Akka 2.6.x (last Apache 2.0 version). Migration requires replacing all `akka` references with `pekko` in config files, packages, and class names. Digital.ai notes: upgrades from pre-24.1 require manual updates; otherwise startup fails with "Configuration settings found which contains not supported term: akka." [Read more](https://docs.digital.ai/deploy/docs/how-to/deploy-migrate-akka-to-pekko)

**Scala.js advances full-stack capabilities:** Scala Days 2025 showcased production-ready GenAI applications using Scala with LLM4S toolkit. UI framework options expanded: Laminar (reactive), Slinky (React bindings), Tyrian (Elm-inspired), scalajs-react. Domain-Driven Design workshops targeted enterprise architects implementing complex event-sourced systems. Cloud-native deployment leverages native binary compilation for instant startup and Scala Native for reduced binary sizes. [Read more](https://xebia.com/blog/scala-days-2025-ai-integration/)

---

##### **INSIGHT**

## **Why the Akka BSL license change keeps creating ripples**

**The license shift fundamentally altered trust.** When Lightbend moved Akka to Business Source License 1.1 in 2022, they triggered a community exodus that continues today. Apache Pekko exists solely because of this decision. Digital.ai's recent migration guide shows the operational cost: every configuration file, import statement, and dependency must change.

**But the new agentic AI platform complicates the calculus.** Akka's four new components—Orchestration, Agents, Memory, Streaming—are included in existing licenses. For teams building AI-native systems, this is genuinely differentiated capability. LangChain and LlamaIndex lack enterprise SLAs for behavioral certainty. Akka offers "3X velocity" with recovery guarantees.

**The strategic fork is clear.** Choose Akka if you need vendor support and can accept BSL terms for mission-critical agentic systems. Choose Pekko if you want Actor Model power without licensing fees and are comfortable with community support. The middle ground is shrinking. Pekko graduated Apache Top-Level; Akka launched a whole new product category. Both are viable, but the choice commits you to different business models for years.

---

##### **IN THE KNOW**

## **What's trending in the Scala ecosystem**

* **Ziverge sponsors backend WASM:** The ZIO-focused consultancy is funding "backend WASM" for Scala, enabling lightweight serverless deployments. Part of their expansion beyond pure-Scala into Rust, Java, TypeScript. [Source](https://www.ziverge.com/post/zio-in-2025)

* **Cats Effect 3.6 released:** Latest version improves fiber scheduling and adds new concurrent primitives. Still the standard choice for Spring ecosystem integration via Project Reactor interop. [Maven](https://mvnrepository.com/artifact/org.typelevel/cats-effect)

* **Holon Streaming uses Akka/Pekko CRDTs:** New research project implements Windowed CRDTs on top of Akka/Pekko Distributed Data for global aggregations. Uses Kafka for input/output streams. [Paper](https://arxiv.org/html/2510.25757v1)

* **VirtusLab offers free Scala 3 migration support:** The Scala maintainers will help migrate your Scala 2 project to Scala 3 at no cost. Part of their mandate to drive ecosystem adoption. [Details](https://softwaremill.com/migrating-to-scala-3/)

---

##### **DISTRIBUTED SYSTEMS HACK**

## **How to cross-build Scala 2 and 3 without merge hell**

Pierre Ricadat's failed first attempt at Scala 3 migration taught a hard lesson: you cannot stop feature development for a migration. The solution: apply migration-compatible changes to your Scala 2 main branch first.

**Step 1:** Enable `-Xsource:3` in Scala 2.13:
```scala
scalacOptions ++= Seq("-Xsource:3")
```

This enables Scala 3 syntax for imports (`*` instead of `_`, `as` instead of `=>`), intersection types (`&` instead of `with`), and warnings for unsupported features.

**Step 2:** Use IntelliJ inspections with quick-fix to batch-apply changes. Select which transformations you want (exclude "case in pattern bindings" which transforms weirdly).

**Step 3:** Set up cross-building in build.sbt:
```scala
ThisBuild / crossScalaVersions := Seq("2.13.20", "3.3.6")
ThisBuild / scalaVersion := "2.13.20"
```

**Step 4:** Create version-specific source directories for incompatible code:
```
src/main/scala      // Shared code
src/main/scala-2    // Scala 2 only
src/main/scala-3    // Scala 3 only
```

**Step 5:** Use `CrossVersion.for3Use2_13` for dependencies not yet on Scala 3:
```scala
libraryDependencies += 
  "com.lihaoyi" %% "utest" % "0.7.11" 
    cross CrossVersion.for3Use2_13
```

Result: Your main branch remains deployable throughout migration, and you avoid the merge conflict avalanche that kills momentum.

---

##### **TOP & TRENDING RESOURCES**

### **Top Tutorial**

**[Scala 3 Migration: Report from the Field](https://blog.pierre-ricadat.com/scala-3-migration-report-from-the-field/):** Honest account of a failed first attempt and successful second try. Covers `-Xsource:3` strategy, IntelliJ quick-fixes, handling macro annotations removal, and managing team coordination during long-running migrations.

---

### **Top Repo**

**[Apache Pekko](https://github.com/apache/pekko):** Community fork of Akka 2.6.x, now Apache Top-Level Project. Includes Pekko HTTP, Streams, and Cluster. Migration guides available for moving from Akka. Good for teams avoiding BSL licensing.

---

### **Trending Paper**

**[Correct Black-Box Monitors for Distributed Deadlock Detection](https://arxiv.org/abs/2603.11808):** Formal model for detecting deadlocks in RPC-based services using Akka/Pekko patterns. Implements monitors for Single-threaded RPC (SRPC) services. Relevant for teams running large Actor Model systems who need runtime verification.

---

##### **SCALAC ANGLE**

**On Akka's agentic pivot:** We see teams struggle with LangChain's operational opacity in production. Akka's bet is that enterprises will pay for certainty—SLAs for agent behavior, recovery guarantees, observability. The "3X velocity" claim is aspirational; budget 6 months to productionize any agentic system, regardless of framework. The real differentiator is Memory: durable, sharded, replicated state with nanosecond writes. Most AI frameworks treat memory as an afterthought.

**On Scala 3 migration:** The cross-building approach is correct but underestimated. Teams focus on syntax changes; the real cost is dependency ecosystem. If you use libraries with heavy macro usage (Circe, Slick), verify Scala 3 support before starting. VirtusLab's free migration support is genuine—use it. We've guided clients through 100k+ line migrations. The pattern: 2 weeks preparation on Scala 2 branch, 1 week actual migration, 4 weeks stabilization. Merge conflicts kill migrations, not compiler errors.

**On Pekko vs Akka:** The BSL license is a forcing function, not just a legal concern. Pekko is production-ready; we've deployed it for clients with strict open-source policies. The trade-off is ecosystem velocity. Akka's new agentic features won't appear in Pekko immediately. If you're building traditional reactive systems (not AI-native), Pekko is the pragmatic choice. If you need the agentic capabilities, Akka's BSL terms are the cost of admission.

---

Signal is published by Scalac. We build distributed systems for teams who ship.

**Want deeper analysis?** Explore our case studies at scalac.io/case-studies  
**Subscribe:** Receive The Distributed Pulse monthly by signing up at scalac.io/newsletter
