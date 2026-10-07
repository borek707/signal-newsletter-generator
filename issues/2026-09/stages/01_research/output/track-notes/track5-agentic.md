# SIGNAL #7, Track 5: Agentic production systems (research, September 2026)

Researched 2026-10-07. Window: 1–30 Sep 2026, plus 1–7 Oct where it changes a September story.
HN numbers come from the Algolia API (`created_at_i` 1788220800–1791417600) and were read on 2026-10-07. GitHub data comes from api.github.com.

## 0. Corrections to the brief's leads (read first)

| Lead as given | What primary sources show |
|---|---|
| LangChain4j PR #6469 has "16 files, +1,293 lines" | Final merged PR: **54 files, +5,832 / −0**. Opened 19 Sep, merged 29 Sep 13:21 UTC (api.github.com/repos/langchain4j/langchain4j/pulls/6469). The 16/+1,293 figure may describe an early revision. I could not verify it, so don't use it. |
| "released in LangChain4j 1.20.0?" | **No.** 1.20.0 came out on 4 Sep and its headline is non-blocking/reactive AI Services plus Jackson 3. DecisionModel shipped in **1.21.0 on 2 Oct 2026**, with #6469, #6526, #6543, #6545 and #6561, and every API is marked `@Experimental`. |
| Naming debate "JudgeModel vs DecisionModel" | Three stages. `JudgeModel` was the original name. On 21 Sep maxandersen asked for "DecisionModel". maeste proposed `StructuredDecisionModel`, which was agreed around 24 Sep. On 25 Sep dliubarskyi reopened it and settled on **`DecisionModel`**, citing the ChatModel/ScoringModel naming and the industry's move to "decision" wording. Issue #6468, comments 21–25 Sep. |
| Jev "invite-only" | The TypeSafe blog says "early access … bringing developers off the waitlist". That is a waitlist, which is not the same as invite-only. |
| "official SDK support ~20 Sep" | Not official. spring-ai-typesafe v0.1.0 (20 Sep) lives in the **spring-ai-community** org and its commits are by tzolov. danvega/jev-spring-boot-starter dates from 20 Sep. Scala: ticofab/scala-jev-sdk (19 Sep). Kotlin: pambrose/jev4k (20 Sep). The TypeSafe blog only mentions a Python wrapper. |
| Jev launch date | HN submission "Introducing System One Models and Jev" was on **15 Sep 2026** (1,989 points, 520 comments). TechCrunch covered it on 18 Sep. The blog page now shows "September 28, 2026", which is probably an edit date. **Event date: 15 Sep.** |
| "only demos?" / JVM Weekly vol. 193 warns the demos look too good | **An independent evaluation exists**: arXiv 2609.37647 (29 Sep) by Deußer, Sparrenberg and Sifa (Uni Bonn / Lamarr Institute / Fraunhofer IAIS). **I could not find JVM Weekly vol. 193**, so treat that quote as unverified. |
| JobRunr v9 "`runStepOnce` durable steps" | `runStepOnce` is **not new in v9**. It shipped in **JobRunr 8.0** (the guide says "JobRunr 8.0.0 or later", and PR #1344 "Improve runStepOnce after demo v8" was merged 10 Jul 2025). What v9 (30 Sep 2026) adds is a free job-history **Gantt chart that shows every attempt and every durable step** (PR #1604), plus Pro analytics and an EventBus. |
| Netflix Conductor post | Dated **21 Aug 2026**, so BACKGROUND_ONLY. |
| ByteByteGo "AI Agents Can Think. Now They Can Pay." (28 Sep) | Covers **only MPP (Machine Payments Protocol, Stripe + Tempo, launched 18 Mar 2026, on the IETF track)**. It does not mention AP2 or x402. Background only. |
| DoorDash toolbox (ByteByteGo 30 Sep) | The underlying post is "How DoorDash Built a Centralized Gateway for AI Agent-Tool Access" by Siddarth Kodwani and Vasily Vlasov, **30 Jul 2026**. BACKGROUND_ONLY. |

---

## 1. Candidate register

### C1. LangChain4j makes typed decisions a first-class model type (Jev / System One)
- **Freshness:** NEW_THIS_MONTH
- **Event dates:** Jev public launch 15 Sep. PR #6469 merged 29 Sep. LangChain4j 1.21.0 released 2 Oct (allowed because it closes a September story). OpenAI Decisions API previewed at DevDay on 29 Sep.
- **Source publication dates:** GitHub release 2 Oct. arXiv eval 29 Sep. OpenAI DevDay recap 29 Sep.
- **Falsifiable claim:** LangChain4j 1.21.0 adds an experimental `DecisionModel` type in `langchain4j-core` (`dev.langchain4j.model.decision`). It returns typed answers with probabilities (yes/no, choice, scale), not text. The release also ships `RoutingChatModel`, `DecisionScoringModel` re-ranking, tool selection, guardrails and a `DecisionRouterPlanner` agentic router that all build on it.
- **Primary sources:**
  - https://github.com/langchain4j/langchain4j/releases/tag/1.21.0 (P0, release notes)
  - https://github.com/langchain4j/langchain4j/pull/6469 (P0, PR)
  - https://github.com/langchain4j/langchain4j/issues/6468 (P0, design and naming discussion)
  - https://arxiv.org/abs/2609.37647 (P0, independent paper)
  - https://developers.openai.com/api/docs/guides/decisions (P0, vendor docs: "The Decisions API is in public beta, and we expect to GA in the coming weeks")
  - https://openai.com/index/devday-2026-recap/ (P0: on 29 Sep it was "limited preview, wider rollout in coming days". I read this from the pl-PL locale render.)
- **Verification:** I checked the merge state, dates, file counts and comments through the GitHub API, and the release body on GitHub. The paper metadata and affiliations come from the arXiv abs and HTML pages.
- **Hard evidence:**
  - From the independent eval (jev-1.13.0 against Qwen3.8-27B and Gemma-4-E4B):
    - 37 datasets, 346,009 requests, about US$9.15.
    - Jev beats Qwen3.8-27B on 27 datasets and loses on 9. 11 of Jev's leads have non-overlapping 95% bootstrap CIs. None of Qwen's do.
    - Pooled Choice ECE is 0.028 across 22 datasets and 279,925 answers. Single Noul (binary) questions are "slightly under-confident" (ECE 0.052).
    - Mean latency is 0.36 s.
  - Weak spots in the same paper:
    - Emotion 58.5%, SST-5 57.9%, Financial PhraseBank 73.0%, AfriXNLI 64.0%.
    - "Binary probabilities rank well but are poorly placed relative to a fixed 0.5 threshold." Threshold tuning raised UNFAIR-ToS micro-F1 from 0.50 to 0.75.
  - Vendor's own claims, not independent: 70–500 ms, $0.042/MTok input, output free, a 255-choice cardinality cap, and "Jev gives up string generation".
- **Trade-off:** You get cheap, fast, calibrated choice outputs for routing, gating and grading, but you give up text generation. Binary outputs need threshold tuning per task. Noisy-label and rubric-quality tasks degrade. The API is `@Experimental` and its shape has already changed three times in ten days.
- **Community reaction:**
  - HN 49717558 "Introducing System One Models and Jev": **1,989 pts / 520 comments** (15 Sep). Sides:
    - Top thread (jacobgold): "the speed comparison seems misleading".
    - ramon156: "so far all claims just sound like marketing terms … 70-500ms vs 3-329 seconds are apples-to-oranges".
    - Supportive comments point to the home-assistant demo.
  - Follow-on HN stories: "Jev in 25 Lines of Python" (692/212), Ollaya (618/145), "Jeff – Jev-compatible 0.8B decision models" (575/232), Kev (463/210), and "OpenAI is well positioned to fast-follow Jev" (328/233, 22 Sep).
  - In the LangChain4j issue, maxandersen argued "Jev is explicitly not an LLM and doesn't reason step by step the way an 'LLM judge' does", against the JudgeModel name.
  - OpenAI community thread on the Decisions API public beta (6 Oct): user "platypus" reports that choice format returned heads 98% of the time on a 70/30 coin, and that choice order affected results. That is a P2 single-user test, so do not cite it as a finding.
- **JVM angle:** Very strong. It sits in LangChain4j core, Spring AI Community has spring-ai-typesafe (v0.1.0 20 Sep to v0.4.0 3 Oct), and there are Scala and Kotlin community SDKs. The core maintainers deliberately put the type in `-core` because it plugs into routing, guardrails, RAG and tool selection (dliubarskyi, 25 Sep).
- **Score:** Freshness 5 / Relevance 5 / Evidence 4 / Stakes 4 / Tension 4 / Originality 4 = **26/30**
- **Suggested slot:** LEAD or DEEP DIVE. It is the JVM-native story of the month, it has a real independent eval, and it has a built-in debate (C1 vs LLM-as-judge, Debate D1).

### C2. Agent state and agent-to-agent trust are the new JVM attack surface (langchain4j-agentic deserialization, a2a-java fail-open defaults, MCP "protocol pivoting")
- **Freshness:** NEW_THIS_MONTH. The a2a-java batch began 28 Aug and continued to 9 Sep. The Ars piece (5 Oct) frames September fixes.
- **Event dates:**
  - GHSA-gmwr-7wmf-mrjm (langchain4j-agentic), published 10 Sep.
  - GHSA-4fpj-g9jf-9rgg (a2a-java, high, 7.5), 9 Sep.
  - GHSA-qw47-mcm5-934w (a2a-java, high, 7.5), GHSA-9rhm-2h4x-jwmx, GHSA-x32g-jvvm-4725 and GHSA-q78c-5jjq-57g8, all 28 Aug.
  - Rapid7 CVE-2026-97228, published 25 Sep.
  - Ars Technica "protocol pivoting", 5 Oct.
- **Falsifiable claim:** Before 1.18.1-beta28, `AgenticScopeSerializer.fromJson` in langchain4j-agentic turned on Jackson default typing with a laissez-faire validator over `Map<String,Object>` state. Attacker-controlled persisted agent state could therefore instantiate arbitrary classes (CVSS 6.6, "with a suitable gadget … RCE"). Separately, a2a-java ≤1.2.0.Final's default `InMemoryTaskStore` did **no authorization on task reads** (CWE-1188/862, CVSS 7.5). Its AuthInterceptor also used a header name from the remote AgentCard, so credentials survived cross-origin redirects. The Android fix for that was then overridden in 1.3.0–1.3.1 and patched in 1.3.2.Final.
- **Primary sources:**
  - https://github.com/langchain4j/langchain4j/security/advisories/GHSA-gmwr-7wmf-mrjm (P0, advisory)
  - https://github.com/a2aproject/a2a-java/security/advisories (P0, five advisories)
  - https://www.rapid7.com/db/vulnerabilities/cve-2026-97228/ (P0, vendor CVE)
  - https://arstechnica.com/security/2026/10/vulnerability-in-agents-from-google-and-others-exposes-structural-flaw-in-mcp/ (P1 press, fetched via curl)
  - https://www.ietf.org/archive/id/draft-mohiuddin-mcp-security-considerations-00.html (P0, I-D from June 2026 defining protocol pivoting; seen only in a search snippet, not fetched)
- **Verification:** I pulled the advisory JSON through the GitHub API, including affected and patched ranges, and fetched the Rapid7 CVE page. Google's mcp-toolbox has six GHSAs (CVE-2026-9739, -11624, -11717, -11718, -11719, -11720), **all published between 28 May and 29 Jun**. Ars also says Google's SSRF guard was added at that time, and GitHub PRs #3448 (Jun), #3625 (Jul) and #3909 (closed 9 Sep) harden the default SSRF guard. So the Google part is background. Only Rapid7's fix and the a2a-java/langchain4j advisories fall in September.
- **Hard evidence:**
  - The CVSS scores above.
  - Rapid7 Bulk Export MCP 0.2.5–0.6.1 had GraphQL injection through `export_id`, CVSS 2.7, fixed in 0.6.2. Rapid7 itself says it "does not grant an existing actor any access they do not already have".
  - Ars quote from Douglas McKee (Rapid7): "anything passed from an LLM to your tool should be treated like input from a stranger on the Internet".
  - Counterpoint quote from Markus Vervier (X41 D-Sec): "For me this is indirect prompt injection." He sees protocol pivoting as a subclass, not a new class.
- **Trade-off:** Persisting and resuming agent state (needed for durable agents) creates a deserialization sink. Convenience defaults (an in-memory task store with null authorization, follow-redirects) fail open.
- **Community reaction:** HN 49991027 for the Ars piece: 4 points, 0 comments (7 Oct), so little discussion. The other A2A security items had low engagement too: "Loopjacking in A2A Implementations" (8 pts / 1 c, 23 Sep, LangGraph Agent Server only, no Java) and "A2ABreak" arXiv 2609.10871 (Purdue/Bertino group, 9 Sep, 11 protocol-level vulns, 2 pts).
- **Score:** Freshness 4 / Relevance 5 / Evidence 5 / Stakes 4 / Tension 3 / Originality 5 = **26/30**
- **Suggested slot:** DEEP DIVE or "Risk" box. It is JVM-specific, P0-backed, and almost certainly not covered by generalist newsletters. Do not inflate it. The langchain4j bug needs a gadget plus attacker-controlled serialized scope, and the Rapid7 CVE is low severity.

### C3. Durable steps in your job library: JobRunr 9.0 makes them visible, and the OSS/Pro durability split matters
- **Freshness:** NEW_THIS_MONTH for v9 (30 Sep). The `runStepOnce` primitive itself is BACKGROUND (v8, 2025).
- **Event dates:** v9.0.0 GitHub release 30 Sep 17:41 UTC. Blog dated 30 Sep. v9.0.1 on 6 Oct.
- **Falsifiable claim:** JobRunr's `runStepOnce` skips completed steps when a job is retried. In **OSS** the step markers are saved "on its normal poll interval … so a hard crash in the window since the last save can re-run the step that had just finished". **Pro** writes state "the moment a step finishes". Even then, "a step that is running at the moment your JVM dies can run again".
- **Primary sources:**
  - https://github.com/jobrunr/jobrunr/releases/tag/v9.0.0 (P0)
  - https://www.jobrunr.io/en/blog/v9-release/ (P0, vendor)
  - https://www.jobrunr.io/en/guides/advanced/durable-executions/ (P0, vendor docs)
- **Verification:** I checked the release notes and dates through the GitHub API, the version ("JobRunr 8.0.0 or later") in the guide, and the PR history (#1344 in 2025, #1479 in Feb 2026).
- **Hard evidence:**
  - Step markers "live in the same database as the job".
  - The feature is "not a workflow engine": single jobs only, no fan-out or multi-job coordination.
  - Step ids must stay stable, because renaming one makes it run again.
  - v9 OSS is the last major version on Java 8.
  - Vendor benchmark from JobRunr's own July post, not independent: about 1,200 DB commits for 1,000 orders vs Temporal's 113,218.
- **Scope wording:** Write "a completed step is not re-run on retry (Pro: as soon as it completes; OSS: after the next state save)". **Do not write "exactly-once".** JobRunr's own July blog states that both tools "may" execute steps more than once.
- **Trade-off:** You avoid new infrastructure, but you get no signals/queries, no cross-job orchestration, and a crash window in OSS.
- **Community reaction:** HN has no JobRunr stories in September (0 hits). InfoQ Java roundup (week of 28 Sep) is P1 discovery only.
- **Score:** Freshness 4 / Relevance 5 / Evidence 4 / Stakes 3 / Tension 4 / Originality 3 = **23/30**
- **Suggested slot:** TODAY bullet, or the Side A evidence in Debate D2. A standalone feature would oversell a dashboard release.

### C4. Temporal: $550M raise plus Java SDK 1.39 standalone activities GA
- **Freshness:** NEW_THIS_MONTH
- **Event dates:** Raise announced 14 Sep. sdk-java v1.39.0 on 14 Sep. v1.40.0 on 29 Sep.
- **Falsifiable claim:** Temporal raised a $550M Series E at a $12.55B valuation. It reports 1.9 trillion billable actions in August (+350% YoY), 4,300+ paying customers, and OpenAI usage up 60× in a year. The Java SDK 1.39.0 marks Standalone Activities GA and adds experimental External Storage (S3 driver) for large payloads.
- **Primary sources:**
  - https://temporal.io/blog/temporal-raises-usd550m-series-e-at-usd12-55b-valuation-ai (P0, vendor PR, so the figures are self-reported)
  - https://github.com/temporalio/sdk-java/releases/tag/v1.39.0 (P0)
- **Verification:** Fetched both pages.
- **Hard evidence:** Listed above. All metrics are self-reported by the vendor.
- **Trade-off:** You get an event-sourced replay engine with determinism constraints and a separate service fleet (or Cloud per-action pricing).
- **Community reaction:** HN 49696335 "Temporal raises $550M": **84 pts / 62 comments** (14 Sep). I did not read the comment sides in depth.
- **JVM angle:** Standalone Activities (activities without a workflow) blur the line toward job queues, which is exactly the JobRunr overlap.
- **Score:** Freshness 5 / Relevance 4 / Evidence 3 / Stakes 3 / Tension 3 / Originality 2 = **20/30**
- **Suggested slot:** TODAY bullet, or Side B context in Debate D2. Funding news on its own is weak for this audience. The standalone-activities GA is the engineering hook.

### C5. "MCP is dead / long live MCP": September's reversal, plus "MCP solves invocation, not governance"
- **Freshness:** NEW_THIS_MONTH for the debate posts and Open Liberty GA. The DoorDash post is BACKGROUND (30 Jul).
- **Event dates:** Maharship post 14 Sep. Earendil "You said no MCP" 29 Sep. Ask HN on MCP in production 3 Sep. Open Liberty 26.0.0.9 `mcp-1.0` GA on 8 Sep. MCP SEP-2640 Skills Extension marked Final 11 Sep and merged 13 Sep. Figma restricted MCP to whitelisted clients 1 Oct.
- **Falsifiable claim:** Earendil's Pi harness had publicly refused MCP support and reversed that on 29 Sep by building MCP into core, composed through a harness-side JavaScript "codemode" sandbox. In the same month, Open Liberty promoted its MCP server feature to GA with a breaking rename (`mcpServer-1.0` to `mcp-1.0`, `<mcpServer>` to `<mcp>`), Origin-header DNS-rebinding checks, and OAuth Protected Resource Metadata.
- **Primary sources:**
  - https://earendil.com/posts/you-said-no-mcp/ (P0, author's own post)
  - https://maharship.com/blog/why-mcp-was-always-a-bad-idea/ (P0 opinion)
  - https://openliberty.io/blog/2026/09/08/26.0.0.9.html (P0)
  - https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2640 (P0)
  - https://careersatdoordash.com/blog/how-doordash-built-a-centralized-gateway-for-ai-agent-tool-access/ (P0, 30 Jul, fetched with Scrapling)
- **Verification:** Fetched all of them. The MCP spec has **no new spec version in September**. The latest is 2026-07-28 (GitHub releases). September spec-repo activity was SEP-2640 plus process changes, such as "Require WG/IG discussion before SEP submission" (#3336, 28 Sep).
- **Hard evidence:**
  - DoorDash: 200+ MCP servers behind its gateway, 30+ agents and services, "millions of tool calls every week", and none of the agents handle raw credentials. Their lesson: "MCP solves invocation, not governance."
  - Open Liberty logs a warning when `@Prompt`, `@Resource` or `@ResourceTemplate` annotations are used, because `mcp-1.0` doesn't support them.
- **Community reaction (verified HN):**
  - "You said no MCP": **686 / 362** (30 Sep).
  - "MCP was always a bad idea?": **335 / 330** (20 Sep). Top reply by simonw (164-reply subthread): "there's almost no reason to use MCPs if you are running a full-blown terminal agent … If you want to operate something that's less YOLO than that, you'll…" That frames MCP as the sandboxed or governed path.
  - "Ask HN: Who is using MCP in production?": **198 / 201**.
  - "Figma restricts MCP access to whitelisted clients": 188 / 106.
- **Score:** Freshness 4 / Relevance 4 / Evidence 4 / Stakes 3 / Tension 5 / Originality 3 = **23/30**
- **Suggested slot:** DEBATE (D3) or Today bullets. MCP appeared in almost every past issue (grep: Mar through Sep). The new angle is governance, gateway and sandbox (DoorDash plus simonw's "less YOLO" point), not "MCP exists".

### C6. GTIG: in-the-wild prompt injection that plants instructions for AI coding agents in repo config files (DUSTMAKER / UNC6780)
- **Freshness:** NEW_THIS_MONTH
- **Event date:** report published 8 Sep 2026 (HN submission 9 Sep).
- **Falsifiable claim:** Google Threat Intelligence Group documented the DUSTMAKER credential stealer (UNC6780 / "TeamPCP"). It used "malicious configuration files inside hidden project directories to instruct the AI assistant to run arbitrary commands or scripts (such as setup.mjs) during routine developer interactions". It also embedded adversarial prompts in JS loaders to make LLM security scanners refuse or skip analysis.
- **Primary source:** https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai (P0 disclosure)
- **Verification:** Fetched. The report gives no victim counts or numbers for coding-agent incidents.
- **Trade-off:** Coding agents that auto-load repo-local config or instructions turn repos into an injection channel. Scanners that rely on LLMs can be made to refuse.
- **Community reaction:** HN 49628034: 13 pts / 1 comment. Low.
- **Score:** Freshness 5 / Relevance 3 / Evidence 4 / Stakes 4 / Tension 2 / Originality 3 = **21/30**
- **Suggested slot:** TODAY bullet (security). For this readership it matters most when paired with C2.

### C7. JVM agent-framework release sweep (September)
- **Freshness:** NEW_THIS_MONTH (all dates from the GitHub releases API)
- **Items:**
  - **Google ADK for Kotlin 1.0.0 GA (7 Sep):** "full feature parity with ADK 1.0 Core to Kotlin, Java, and Android developers". Then 1.1 (15 Sep), 1.2 (28 Sep), 1.3 (2 Oct). ADK Java 1.10.0 came out 16 Sep and 1.11.0 on 2 Oct, adding `EventActions.agentState` for session resumability.
  - **Koog 1.3.0 (24 Sep):** the Google cached-token count now reaches the OpenTelemetry `gen_ai.response.metadata` attribute, and Langfuse traces no longer show empty assistant content for Gemini signature-only reasoning parts. This is a small but concrete agent-observability fix.
  - **Spring AI 2.1.0-M1 (25 Sep):** OpenAI Responses API support, `VectorStore.upsert`, and Spring Boot 4.2.
  - **Quarkus LangChain4j:** 1.14.0 (25 Sep). Apicurio Registry integration for dynamic MCP server discovery landed in 1.14.0.CR2 (9 Sep). 2.0.0.Beta1 (3 Oct) ports to Quarkus 4.
  - **A2A Java SDK:** 1.3.1 (3 Sep), 1.3.2 (8 Sep, Android credential-redirect fix), 1.4.0.Final (28 Sep).
  - **Open Liberty `mcp-1.0` GA (8 Sep):** see C5.
  - **Jakarta Agentic AI 1.0 M1:** InfoQ (P1) says the M1 is out, and Azul Payara 7.4.0 supports the spec in Payara Micro and Embedded. I did not confirm the exact M1 date on jakarta.ee.
  - **Akka SDK 3.6.6 (1 Oct):** "evakit for running Agent experiments as integration tests" (PR #1839, merged 9 Sep, which describes itself as "still a draft"). This is an evaluation hook, but thin.
- **Primary sources:** github.com/{google/adk-kotlin, google/adk-java, JetBrains/koog, spring-projects/spring-ai, quarkiverse/quarkus-langchain4j, a2aproject/a2a-java, akka/akka-sdk}/releases (P0)
- **Score:** Freshness 5 / Relevance 5 / Evidence 5 / Stakes 2 / Tension 1 / Originality 2 = **20/30**
- **Suggested slot:** TODAY / "Releases" list. Pick 3–4: ADK Kotlin 1.0 GA, Open Liberty `mcp-1.0` GA, Spring AI 2.1.0-M1, Koog's OTel token fix.

### C8. Netflix Conductor: "The Next Chapter" (Java workflow SDK, Run Strategies)
- **Freshness:** BACKGROUND_ONLY. Published 21 Aug. An HN repost on 26 Sep got 2 points.
- **Claim:** Conductor backs about 200,000 workflow definitions across about 150 applications and runs "on the order of 420 million workflows" a month (5–20M a day). Netflix replaced Dynomite/DynoQueues with Cassandra and Timestone, rewrote the evaluation engine, added "Run Strategies" (Sequential per key), and added a type-safe **Java DSL Workflow SDK** that compiles to the JSON graph so the visual graph view stays.
- **Primary source:** https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649 (P0, fetched with Scrapling)
- **Score:** Freshness 1 / Relevance 4 / Evidence 4 / Stakes 2 / Tension 3 / Originality 2 = **16/30**
- **Suggested slot:** Debate D2 context only, as the third model: a declared graph, neither replay nor snapshot. Conductor was already in the Issue #5 selection and debate files (grep 2026-07).

---

## 2. Debate dossiers

### D1. Typed decision model vs LLM-as-judge (recommended: strongest fresh debate)
**Side A: dedicated decision models (Jev and the System One class)**
- Independent evidence: Choice ECE 0.028, 27/37 wins vs Qwen3.8-27B (11 significant), 0.36 s mean latency, US$9.15 for 346k requests (arXiv 2609.37647, 29 Sep).
- maxandersen (issue #6468, 21–22 Sep): an LLM judge implies chain-of-thought and explanations, while Jev is "designed to skip exactly that". He also says decisions are the general primitive and judging is only one use case.
- LangChain4j maintainers put DecisionModel in core so that routing, guardrails, re-ranking and tool selection can sit on one cheap primitive (dliubarskyi, 25 Sep; 1.21.0 notes).
- OpenAI shipped the same shape: Decisions API with Predicates, Choices and Scores on GPT-6 Luna, "up to 10x faster" than Luna via the Responses API. It is in public beta per the docs. That is market validation of the category.

**Side B: LLM-as-judge or general models still win where judgment is fuzzy**
- The same independent paper: all models "degrade on … fine-grained or noisy labels, and rubric-based quality judgments". Binary probabilities are "poorly placed relative to a fixed 0.5 threshold", so per-task tuning is needed. That partly undercuts the zero-config pitch.
- HN top threads (49717558): the speed comparisons are "misleading" and "apples-to-oranges" against reasoning LLMs.
- IRONICBo (#6468, 25 Sep) warns against treating confidence from a ChatModel emulation as equivalent to native calibrated confidence. That is an argument for recording where a confidence number came from, not against the approach.
- OpenAI community (P2, single user): choice outputs on GPT-6 Luna looked mode-seeking, not calibrated (98% heads on a 70/30 coin).

**Verdict:** Both sides have substance and P0 backing. The honest framing is that typed decision models win on short, well-scoped decisions, while LLM judges keep rubric and quality grading. Thresholds need tuning, and confidence numbers should be logged with where they came from. Not covered in previous issues (grep "Jev" and "System One" hit only the current brief).

### D2. Durable execution: job-library/Postgres steps vs a dedicated replay engine
**Verdict first:** Only worth running if you frame it around **new September evidence**. "Library vs engine" itself was Issue #5's debate (DBOS vs Temporal, 2026-07). The fresh September axis is **snapshot/checkpoint vs history replay**, with Temporal's CEO arguing in public.

**Side A: checkpoint, don't replay (or skip the engine)**
- Trigora "Durable execution without history replay" (9 Sep, Omar Abdelrahman): checkpoints the live continuation. In a controlled 4 KB-state prototype it measured 0.6–0.9 ms recovery vs 61 ms–1.7 s for replay as boundary depth went from 10 to 1,000. The author's own caveat: "should not be interpreted as a general production-speedup claim". HN 49635621: 41 / 34.
- JobRunr 9.0 (30 Sep): durable steps inside a job library, markers in the same DB, and every step now visible in the dashboard Gantt chart. The scope limits are spelled out (C3).

**Side B: replay is the right default**
- HN user mfateev (profile: "CEO/Co-founder of temporal.io"), 13 Sep, same thread: the first durable-execution POC at AWS SWF used reflection snapshots and "Performance was abysmal … So we switched to replay". Replay "lets you implement Durable Execution in any language as a library" and supports in-flight code changes (patching). Making snapshots backward-compatible with code changes "isn't practical". His long-term bet is a runtime with both snapshots and determinism, likely WASM.
- Market signal (vendor-reported): Temporal's $550M raise, 1.9T billable actions in August, and Java SDK Standalone Activities GA (14 Sep). The last one moves Temporal toward job-queue territory.

**Missing:** There was no September post from JobRunr directly answering Temporal. Their "JobRunr vs Temporal" post is from 12 Jul 2026. Netflix Conductor (21 Aug) offers a third model, a declared graph, but it is background.

### D3. MCP: obsolete overhead vs governed default
- **Side A (obsolete):** Maharship, 14 Sep: "Agents with terminal access can replace most MCP servers". HN 49779329 335/330. Ask HN commenters (3 Sep) say gh CLI beats the GitHub MCP.
- **Side B (governed default):** Earendil's reversal (29 Sep, 686/362). simonw's top reply on the "less YOLO" path. DoorDash's gateway (background): credentials, curation and audit, with the lesson "MCP solves invocation, not governance". Enterprise Java is going GA: Open Liberty `mcp-1.0`.
- **Verdict:** Real tension with high engagement, but MCP appears in about 20 past issue files. Only use it if the framing is "governance layer vs CLI freedom" and it links to C2's security findings.

---

## 3. Rejected or deprioritised items
- **Pragmatic Engineer "Inside OpenAI's agentic software factory" (15 Sep):** sections 1–3 are free, but there are **no hyperlinked OpenAI primary sources**. The numbers (about 10× PRs per engineer, CI load up 10×) can't be sourced to P0. Use as discovery only. HN: 4 pts and 1 pt.
- **Pragmatic Engineer "What is happening with code reviews?" (8 Sep):** off-track (engineering practice, not agentic production systems), and the cited numbers come from third parties inside a paywalled newsletter.
- **ByteByteGo "AI Agents Can Think. Now They Can Pay." (28 Sep):** MPP only (launched March 2026). I found no September P0 change for AP2 or x402. x402 has only Show HN noise (≤4 pts). Not a JVM topic.
- **ByteByteGo DoorDash (30 Sep):** a secondary write-up of a 30 Jul post. Folded into C5 as background.
- **Netflix Conductor:** BACKGROUND. Kept as C8 for debate context only.
- **A2A under the Agentic AI Foundation:** no new status in September. The 17 Aug move was in Issue #6. A2A spec latest is v1.0.1 (28 May).
- **MCP spec revision:** none in September (latest 2026-07-28). SEP-2640 Skills Final is a minor extension, so it is a C5 footnote at most.
- **OpenTelemetry GenAI semconv:** no September release (latest v1.44.0, 4 Aug). Only the Koog-level fix in C7.
- **GuardFall (Adversa/Aviatrix):** June 2026, out of window.
- **OpenAI/Hugging Face agent incident and CISA KEV adds:** July–August 2026, out of window. Check Issue #6 for coverage before any mention.
- **Loopjacking (A2A):** LangGraph Agent Server only, no Java, no CVE, 8 pts.
- **A2ABreak arXiv:** fresh (9 Sep) but low-signal at abstract level, and the implementations tested are unknown. Possible footnote to C2.
- **TypeSafe "$1B round" reports:** Spanish-language aggregator only, unverified. Do not use.
- **Competitors:** none surfaced in this track. polyvariant/jev4s (Polyvariant, Jakub Kozłowski) is not on the VirtusLab/SoftwareMill/Typelevel list, but check before naming it.

## 4. Open fact-check questions
1. Where does the "16 files, +1,293 lines" figure for PR #6469 come from? Check the PR's commit history for an early revision. Final is 54 / +5,832.
2. JVM Weekly vol. 193's "demos look too good" warning: not found. Get the URL from whoever supplied the lead, or drop it.
3. Is the TypeSafe blog date 15 Sep (HN, TechCrunch 18 Sep) or 28 Sep (current page)? Use 15 Sep as the event date and note that the page was edited.
4. OpenAI Decisions API status changed: limited preview on 29 Sep (DevDay recap), public beta by 6 Oct (docs and community post). Pricing of "$0.10 per 1M input tokens" comes only from the community post by "sps". Confirm on the pricing page before citing.
5. Is the TheNewStack article (29 Sep, "OpenAI answers TypeSafe's Jev…") paywalled? The body could not be fetched, so don't cite its content.
6. Jakarta Agentic AI 1.0 M1: confirm the date on jakarta.ee/specifications/agentic-ai/1.0/.
7. Was the A2A Java SDK for Jakarta Servers 1.0.0.Final (WildFly) shipped in September? It's an InfoQ lead and I did not verify a GitHub release.
8. Temporal metrics (1.9T actions, 4,300+ customers) are vendor-reported only. Label them that way.
9. Ars's "In the past five months, Google and four other organizations … acknowledged vulnerabilities": only Rapid7 (25 Sep) is in window. Don't present the whole set as a September event.
10. Spring AI 2.1.0-M1 is "the first milestone of the next minor (2.1)", not the next major. Check the InfoQ wording the coordinator relayed ("next major").

## 5. URLs fetched
**OK:**
- api.github.com: langchain4j PR #6469, issue #6468 plus comments, releases 1.19.2–1.21.0, and advisory GHSA-gmwr-7wmf-mrjm.
- api.github.com: jobrunr releases v8.8.0–v9.0.1 and issue search.
- api.github.com: releases for a2a-java (and advisories), spring-ai, koog, quarkus-langchain4j, adk-kotlin, adk-java, embabel, temporal sdk-java, mcp java-sdk, akka-sdk, langchain4j-community, spring-ai-typesafe, the A2A spec and otel semconv.
- api.github.com: mcp-toolbox advisories and PR search, plus MCP spec releases, commits and PR #2640.
- GitHub repo search for Jev Java/Scala/Kotlin SDKs.
- typesafe.ai, typesafe.ai/blog/introducing-system-one-models-and-jev.
- arxiv.org/abs/2609.37647 plus the HTML v1; arxiv.org/abs/2609.28940; arxiv.org/abs/2609.10871.
- jobrunr.io/en/blog/v9-release/, /guides/advanced/durable-executions/, /blog/jobrunr-vs-temporal/.
- temporal.io raise blog; trigora.dev post; earendil.com post; maharship.com post; adithyanak.com loopjacking.
- cloud.google.com GTIG report; openliberty.io 26.0.0.9 blog.
- rapid7.com CVE-2026-97228; arstechnica.com protocol-pivoting article (via curl).
- blog.bytebytego.com DoorDash and payments posts.
- newsletter.pragmaticengineer.com (both posts, free preview).
- infoq.com roundups (URLs sep07, sep14, sep21, and Oct sep28).
- community.openai.com Decisions API public beta thread.
- careersatdoordash.com gateway post, netflixtechblog Conductor post, openai.com DevDay recap and developers.openai.com Decisions guide (all via Scrapling stealthy-fetch).
- HN Algolia search and items API; HN Firebase user API (mfateev).

**Failed:**
- arstechnica.com via WebFetch (blocked; curl worked).
- careersatdoordash.com via WebFetch, curl and Jina (403 / Cloudflare; Scrapling worked).
- netflixtechblog.medium.com via WebFetch (403; Scrapling worked).
- openai.com via WebFetch (403; Scrapling worked).
- thenewstack.io/openai-decision-api-luna/ (body truncated, article text not retrieved).
- JVM Weekly vol. 193 (not found by search).
- careersatdoordash.com "Delegating engineering work to cloud-based agents" (403, not retried; not needed).
