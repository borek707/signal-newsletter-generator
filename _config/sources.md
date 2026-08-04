# SIGNAL Sources

## Evidential Tiers (read before citing anything)

The "Required" list below is a **coverage** obligation: what to sweep every month so nothing is missed. It is not a statement of evidential weight. Those are separate axes, and conflating them is how a newsletter ends up sourcing a breaking change to a roundup post.

| Tier | What it is | Rule |
|------|-----------|------|
| **P0 — primary** | The artefact itself: JEP, KIP, RFC, spec, paper, commit, PR, release notes, mailing-list thread, official incident disclosure, benchmark repo. | Required to support any load-bearing claim (status, date, number, scope). |
| **P1 — editorial radar** | JVM Weekly, InfoQ, ByteByteGo, Pragmatic Engineer, Kafka Monthly Digest, Scala Times, Get Kafka-Nated, Red Hat Developer, Java Annotated Monthly, Inside Java Newscast, Foojay, The Morning Paper, ACM Queue. | Excellent for **discovery** and context. Never the sole evidence for an important claim — always chase the artefact it points at. |
| **P2 — community temperature** | Hacker News, X, LinkedIn, Reddit, Mastodon, GitHub issue/PR discussion, conference talks. | Use to show a story provoked real reaction, and for Debate / Community Voice. **Never** a source of technical fact. Separate opinion from fact explicitly. |

Worked example (July 2026): JVM Weekly (P1) surfaced JDK-8377715, a virtual-thread SIGSEGV regression. The loom-dev thread it pointed at (P0) returned 403. Without P0 confirmation the story could not carry Trenches, and a GitHub issue found while trying to corroborate it turned out to be a *different, older* bug. Correct outcome: demoted, flagged, not published. That is the tiering working as intended.

## P0 primary sources — check when a claim needs proof

Not a monthly sweep. This is the lookup list for verifying a specific claim, and the escape hatch when a P1 source is all you have.

- **JVM / OpenJDK:** [JEP index](https://openjdk.org/jeps/0), [openjdk/jdk on GitHub](https://github.com/openjdk/jdk) (commits, PRs, tags), [OpenJDK mailing lists](https://mail.openjdk.org/mailman/listinfo), JDK release pages, and the Valhalla / Loom / Panama / Leyden project pages. Note: `mail.openjdk.org` has returned 403 to automated fetches — use the GitHub PR or the JEP page itself instead.
- **Scala / Kotlin:** [Scala Blog](https://www.scala-lang.org/blog/), [Scala Contributors](https://contributors.scala-lang.org/) (best signal for SIPs, compiler work, and live controversy), [scala/scala releases](https://github.com/scala/scala/releases), [sbt releases](https://github.com/sbt/sbt/releases), Kotlin releases and KEEP proposals, ZIO releases, Apache Pekko releases.
- **Kafka / streaming:** [KIP index](https://cwiki.apache.org/confluence/display/KAFKA/Kafka+Improvement+Proposals) (the only place to confirm whether something is an idea, under vote, or accepted), [Kafka releases](https://kafka.apache.org/downloads), [apache/kafka on GitHub](https://github.com/apache/kafka), [dev@kafka mailing list](https://lists.apache.org/list.html?dev@kafka.apache.org) for disputes before they reach a digest, Flink releases and FLIPs.
- **Distributed correctness:** [Jepsen analyses](https://jepsen.io/analyses) (use whenever a vendor claims consistency, transactionality, or exactly-once), arXiv `cs.DC` / `cs.DB` / `cs.SE` / `cs.PL`, USENIX / SOSP / OSDI / NSDI / VLDB / SIGMOD proceedings.
- **Workflow / durable execution:** Temporal and DBOS docs, releases, and blogs. Treat both as **positions in a debate**, not neutral references, and never cite one in isolation. LittleHorse likewise, as an explicit vendor source.
- **Agentic on the JVM:** [Model Context Protocol spec](https://modelcontextprotocol.io) and its GitHub, LangChain4j releases and issues, Spring AI releases, Quarkus releases and AI extensions, OpenTelemetry specs and semantic conventions (for agent observability), [Chrome DevTools MCP releases](https://github.com/ChromeDevTools/chrome-devtools-mcp/releases).

## Required Sources (check every month)

1. **JVM Weekly** ([jvm-weekly.com](https://www.jvm-weekly.com/))
   - JVM ecosystem, JDK, GraalVM, performance.
   - Sitemap: `curl -s "https://www.jvm-weekly.com/sitemap.xml" | grep -oE "https://[^<]+"`

2. **This Week in Scala** ([thisweekinscala.substack.com](https://thisweekinscala.substack.com/))
   - Scala releases, SIPs, tooling.
   - Sitemap: `curl -s "https://thisweekinscala.substack.com/sitemap.xml" | grep -oE "https://[^<]+"`

3. **InfoQ Software Architects' Newsletter** ([infoq.com/software-architects-newsletter/](https://www.infoq.com/software-architects-newsletter/))
   - Enterprise architecture, AI, postmortems.
   - Find latest issue URL on the landing page.

4. **ByteByteGo Newsletter** ([blog.bytebytego.com](https://blog.bytebytego.com/))
   - System design, distributed systems, AI infrastructure.
   - Use Substack archive or homepage. Check dates (`MAY 28, 2026` format).

5. **The Pragmatic Engineer** ([newsletter.pragmaticengineer.com](https://newsletter.pragmaticengineer.com/))
   - Engineering leadership, AI tooling trends, job market.
   - Key series: "The Pulse" (weekly trends), deepdives.
   - Note: do NOT reference paywalled articles as primary sources.

## Secondary Sources (check if time allows)

- **r/scala** — Scala ecosystem, FP, JVM trends.
- **r/apachekafka** — Streaming, migrations, ops.
- **r/dataengineering** — Pipelines, architecture decisions.
- **Hacker News** — Engineering discussions.
- **Engineering Blogs** — Netflix, Uber, Confluent, Lightbend/Akka.
- **Get Kafka-Nated** ([getkafkanated.substack.com](https://getkafkanated.substack.com/)) — biweekly Kafka-community-specific newsletter. Good for production edge-case reports (e.g. Jack Vanlightly's Share Groups findings, Jul 2026) and KIP-status tracking. Use Substack archive/RSS fallback method below.
- **Data Engineering Digest** ([dataengineeringcommunity.substack.com](https://dataengineeringcommunity.substack.com/)) — monthly, broader data-engineering/lakehouse/orchestrator-market news (e.g. Prefect/Dagster consolidation, Databricks architecture moves). Useful context for the Debate/Trenches even when the story itself isn't JVM-specific.
- **Kai Waehner's blog** ([kai-waehner.de/blog](https://www.kai-waehner.de/blog/)) — frequent (weekly-ish), Confluent-affiliated but vendor-neutral in tone; strong on Kafka/Flink/Spark architecture trade-offs and Kafka+agentic-AI integration patterns. Check the blog's own listing page directly (not just WebSearch, which tends to surface stale posts).
- **Scala Times** ([scalatimes.com](https://scalatimes.com/)) — weekly Scala-community roundup. **Published by SoftwareMill, a named Scalac competitor** (per `scalac-tone-of-voice.md`). Fine to use as a discovery source for independent, non-SoftwareMill stories (e.g. a Scala-core-team language feature); never use it to justify featuring SoftwareMill's own tools/projects (sttp, tapir, ox, chimp, Orca Flow, etc.) — those follow the same "do not feature or credit" rule already established for VirtusLab.
- **Rock the JVM** ([rockthejvm.com](https://rockthejvm.com/)) — Scala/JVM educational content (Daniel Ciocîrlan). The site's `/articles` index doesn't expose dates to a plain WebFetch; individual articles surface reliably via This Week in Scala's link roundups instead — treat as "found via TWiS," not directly browsable.

## Checked and found unusable

- **"TypeSafe Brew"** — referenced in older internal notes as a source, but no such active newsletter could be found (as of 2026-08, only historical "Typesafe→Lightbend" rebrand news surfaces). Likely defunct or misremembered; don't spend research time searching for it again unless a human points to a live URL.

## Skipped (stale / unreliable)

- **Distributed Systems Newsletter** (distributedsystems.substack.com) — last post January 2026, irregular cadence. Only check if explicitly requested.

## Substack RSS Fallback

```bash
curl -s -L -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" "https://[subdomain].substack.com/feed" | grep -oE '<link>[^<]*</link>'
```

Then fetch individual post URLs.

## Fetch Method

Try `WebFetch` first. It handled most Substack archives and individual issues fine during the July 2026 pass, so the older "curl fails, always use Chrome MCP" advice overstated the problem. Chrome MCP (`chrome-devtools-mcp` or `hangwin/mcp-chrome`; example client `mcp-client.js` in repo root) is the fallback for genuinely JS-rendered pages, not the default.

### When a fetch fails, change the evidence path — do not give up

The goal is to verify a claim, not to retrieve one specific HTML page. Walk down this ladder and stop at the first rung that confirms date, status, scope, and authorship.

1. **Search** for the canonical URL, the date, and the artefact name (JEP / KIP / release tag / paper ID).
2. **Read the search result's own content** rather than hand-assembling a URL from fragments.
3. **Fetch the URL** directly.
4. **Move to an equivalent source:** GitHub releases / tags / commit history, GitHub issues and PRs, mailing-list archive, official changelog, arXiv abstract or PDF, conference proceedings, versioned docs. For anything OpenJDK, the GitHub PR is usually more reachable than the mailing list.
5. **Two independent secondary sources**, only if no primary exists, and only when they agree on both the date and the specific artefact.
6. **Flag the uncertainty in the brief, or reject the item.** Never fill the gap with inference.

| Failure | Response |
|---------|----------|
| JS-rendered or empty page | GitHub repo, release notes, RSS, sitemap, raw Markdown, or the cached text in search results |
| Paywall (e.g. Pragmatic Engineer paid tier) | Find the primary source, paper, or release note it cites; free-preview text is quotable, paid body is not (see `fact-check-rules.md` §8) |
| 403 / robots block (`mail.openjdk.org`, `reddit.com`) | Go to the official repo, a mirror, the mailing-list archive, or whatever the article itself cited. Do not retry in a loop. |
| HTTP 429 (HN has done this mid-pass) | Wait and retry once, then use Exa/search-result text for the thread instead |
| Result has no date | Look for a release/tag/commit, paper version date, announcement post, or mailing-list message |
| Marketing claim with no artefact | Look for a benchmark, a limitations section, the issue tracker, an independent case study, or a test suite |
| Cannot confirm production usage | Do not write `production-proven`. Use `experimental` / `research` / `early-stage`, or drop the item. |

## What to Look For

- "Migrated from X to Y" with metrics.
- Post-mortems ("lessons learned", "incident report").
- Architecture debates (50+ comments, controversy).
- Cost reductions ("cut bill by 80%").
- Breaking changes in core tools.
- AI integration in existing stacks.

## What to Skip

- Event/conference announcements (CFPs, ticket sales, Devoxx, JavaOne, MCP Dev Summit) — these go to Scalendar, not SIGNAL.
- Minor library releases without architectural impact.
- Tutorial posts without production context.
- Vendor marketing without technical depth.
- Future-dated threads if newsletter date is in the future relative to available data.

## Supplementary Research Tools (use in `01_research`, alongside the sources above)

Two Claude Code skills fill gaps the newsletter/blog sources above don't cover: real-time social engagement, and X/LinkedIn/Reddit specifically. Both were used to research Issue #5 (July 2026) and are worth reaching for on every future issue, not just when things feel thin.

### `/last30days` (skill: `last30days` or `last30days-skill`)

A research engine that pulls and ranks Reddit/X/YouTube/TikTok/HN/Polymarket/GitHub/web activity for a topic over a lookback window. Useful for a fast pulse-check on a candidate Debate/Trenches/Signal topic before committing research time to it — e.g. running it on "JVM and Distributed Systems" surfaced the Cloudflare Meerkat and DBOS/Postgres-orchestrator threads independently of the newsletter-source sweep, which is what first flagged both as worth deep-diving.

**How to use it for a SIGNAL issue:** invoke `/last30days {candidate topic}` (e.g. a specific debate framing) early in `01_research`, before the deep per-source WebFetch pass — treat its output as a triage signal (what's actually getting engagement) rather than a citable source on its own. Follow its own skill instructions for the actual invocation mechanics (query planning, `--subreddits`/`--x-handle` targeting, etc.) — don't reinvent that here.

### `agent-reach` (skill: `agent-reach`)

A router for platform-specific searches this session's normal WebFetch/WebSearch can't reach well: X/Twitter, LinkedIn (via Exa `site:linkedin.com`), Reddit, and others. Run `agent-reach doctor --json` first to see what's actually configured.

- **X/Twitter:** needs either (a) the OpenCLI browser extension connected to a logged-in x.com session (`opencli twitter search/thread -f yaml` — no cookie juggling once connected), or (b) a manual Cookie-Editor export of `auth_token`/`ct0` via `agent-reach configure twitter-cookies`. OpenCLI was set up and connected during Issue #5's research (2026-08-04) — check `agent-reach doctor --json` first; if the extension has disconnected, `opencli daemon restart` usually reconnects it.
- **LinkedIn:** no dedicated backend was configured this session — `mcporter call exa.web_search_exa(query: "site:linkedin.com ...")` was used as a working substitute and found real, citable posts (e.g. Cloudflare's own Meerkat post, an independent JEP 401 explainer). Filter out junior "I built X from scratch" portfolio posts — they're common and not SIGNAL-tier.
- **Reddit:** still not configured as of Issue #5 (no OpenCLI Reddit login, no rdt-cli). This remains the one real gap in `sources.md`'s secondary-source checklist (r/scala, r/apachekafka, r/dataengineering) — worth setting up before the next issue if Reddit coverage matters (`agent-reach install --channels opencli` + log into reddit.com in the same Chrome profile).

**Why both matter for SIGNAL specifically:** the newsletter/blog sources above tell you *what shipped*; `/last30days` and `agent-reach` tell you *whether anyone reacted to it* — engagement numbers (Cloudflare's Meerkat tweet: 458 likes/225K views; @arpit_bhayani's explainer thread: 346 likes) are exactly the kind of "is this actually a debate or just a press release" evidence the Debate/Trenches selection criteria ask for.

## Special Monthly Checks

### KotlinConf / JetBrains Ecosystem (typically May, Munich)

- Kotlin release announcements (breaking changes, backend removals).
- JetBrains agent/AI framework releases (Koog, kotlin-agent-skills).
- Security policy updates (CVE numbering, support windows).
