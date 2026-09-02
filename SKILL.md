---
name: signal-newsletter-generator
description: Generate the SIGNAL newsletter for Scalac. Use when the user asks to create a monthly newsletter, generate SIGNAL, or prepare the distributed systems newsletter. This skill produces a strategic engineering newsletter combining The Code format (short, punchy, metric-driven) with deep architectural analysis (3 sections: Debate, Trenches, Signal).
metadata:
  trigger: "monthly newsletter", "SIGNAL", "distributed systems newsletter", "create newsletter", "prepare newsletter draft"
  author: Scalac
  schedule: monthly
---

# SIGNAL Newsletter Generator

Generate a monthly B2B newsletter targeting CTO, VP of Engineering, and Chief Architect roles. The newsletter combines The Code format (short, punchy, metric-driven) with strategic depth (3 sections: Debate, Trenches, Signal).

## Newsletter Philosophy

**Don't aggregate news. Aggregate lessons.**

Senior engineers don't need library release notes. They need:
- Architecture debates with real trade-offs
- Production war stories with solutions  
- 3 critical signals with business context

**Scope:** Scala + JVM + Java + Rust + Kafka + Akka + Data Engineering + AI integration

---

## Writing Style: The Code Format

SIGNAL piszemy w stylu "The Code" - short, punchy, metric-driven:

✅ DO:
- Krótkie akapity (max 2-3 zdania), potem enter
- Boldowane hooki na początku: "**KIP-1150 makes diskless Kafka official:**"
- Metryki na pierwszym miejscu: "80% cost reductions", "10+ TB/day", "100-500ms"
- Aktywny głos: "Apache Kafka approves" nie "KIP-1150 was approved"
- Konkretne rekomendacje w "Scalac angle", nie ogólne tezy
- Bez em-dash (—), używaj myślników (-) lub kropek
- Wszystko podlinkowane - każda firma, projekt, osoba

❌ DON'T:
- Długie, narracyjne wstępy
- Pasywne konstrukcje
- "The debate is a false binary" - za ogólne
- Throat-clearers: "Here's what you need to know", "In this article", "Let's dive in"
- Emphasis crutches: "crucial", "critical", "essential", "key", "vital", "game-changer"
- Business jargon: "leverage", "synergy", "ecosystem", "paradigm shift", "best practices"
- Adverbs: "importantly", "significantly", "effectively", "efficiently"

---

## Issue Structure

### Issue #1 (pierwszy numer):
```
**Welcome to SIGNAL.** This is a monthly briefing for CTOs, VP Engineering, 
and Chief Architects running distributed systems at scale. We don't aggregate 
news. We aggregate lessons. Three sections every month: one architecture debate 
with real trade-offs, one production war story with solutions, and three critical 
signals with business context. No hype cycles. No vendor pitches.

**Also:** [2 bullet points teasing other major stories]
```

### Issues #2+ (kolejne numery):
```
**Welcome back.** [2-3 sentences. Hook with the most surprising/debated insight. 
No throat-clearing.]

**Also:** [2 bullet points teasing other major stories]
```

---

## Workflow

### Step 1: Collect Signals from Multiple Sources

**Required Sources (must check every month):**
1. **JVM Weekly** ([jvm-weekly.com](https://www.jvm-weekly.com/)) - JVM ecosystem, JDK, GraalVM, performance
   - Use sitemap: `curl -s "https://www.jvm-weekly.com/sitemap.xml" | grep -oE "https://[^<]+"`
   - Fetch individual posts directly
2. **This Week in Scala** ([thisweekinscala.substack.com](https://thisweekinscala.substack.com/)) - Scala releases, SIPs, tooling
   - Use sitemap: `curl -s "https://thisweekinscala.substack.com/sitemap.xml" | grep -oE "https://[^<]+"`
   - Fetch individual weekly issues, then extract article links from HTML
3. **InfoQ Software Architects' Newsletter** ([infoq.com/software-architects-newsletter/](https://www.infoq.com/software-architects-newsletter/)) - Enterprise architecture, AI, postmortems
   - Find latest issue URL on the landing page (e.g. `https://assets.infoq.com/newsletter/architect/en/newsletter_sample/NNNArchitects_NL_Month-YYYY.html`)
   - Fetch and extract article links
4. **ByteByteGo Newsletter** ([blog.bytebytego.com](https://blog.bytebytego.com/)) - System design, distributed systems, AI infrastructure
   - Use Substack archive or homepage to find monthly posts
   - Check dates (MAY 28, 2026 format)
5. **The Pragmatic Engineer** ([newsletter.pragmaticengineer.com](https://newsletter.pragmaticengineer.com/)) - Engineering leadership, AI tooling trends, job market
   - Use Substack archive or homepage
   - Key series: "The Pulse" (weekly trends), deepdives
   - Check for AI spend rationalization, hiring trends, tool adoption data

**Secondary Sources (check if time allows):**
5. **r/scala** - Scala ecosystem, FP, JVM trends
6. **r/apachekafka** - Streaming, migrations, ops
7. **r/dataengineering** - Pipelines, architecture decisions
8. **Hacker News** - Engineering discussions
9. **Engineering Blogs** - Netflix, Uber, Confluent, Lightbend/Akka

### Research tools and routing

Use `agent-reach` for every external lookup, URL and platform query. It routes
GitHub, Reddit, YouTube, LinkedIn and ordinary web pages through the available
backend. Use it to discover sources and to recover readable copies when a direct
page blocks ordinary fetchers. A social post is a lead, never the sole evidence for
a technical claim.

If `agent-reach` or its reader cannot retrieve a public page because of rendering
or a simple bot block, use Scrapling as the fallback fetcher. Use it to render or
extract publicly available pages, then verify the result against the source. Do
not use it to bypass authentication, paywalls, CAPTCHA challenges or access
controls. If the page still cannot be read, find an accessible primary or
independent source instead.

Use `last30days` as a constrained discovery pass after the source sweep. Run a
small set of focused queries, not a broad firehose: `Scala JVM`, `Kafka distributed
systems`, `agentic AI in production`, and one timely combined query when the month
provides one. Treat its output as an attention and community-sentiment radar. Verify
selected claims against primary sources before they enter the issue.

For every candidate, record the originating event date and assign a freshness tag:
`NEW_THIS_MONTH`, `MATERIAL_UPDATE` or `BACKGROUND_ONLY`. Only the first two can
lead Debate, Trenches or Signal Over Noise. A background item may provide context
but must never be written as current news.

**Skip (stale / unreliable):**
- **Distributed Systems Newsletter** (distributedsystems.substack.com) - Last post January 2026, irregular cadence. Only check if user explicitly requests.

**What to look for:**
- "Migrated from X to Y" with metrics
- Post-mortems ("lessons learned", "incident report")
- Architecture debates (50+ comments, controversy)
- Cost reductions ("cut bill by 80%")
- Breaking changes in core tools
- AI integration in existing stacks

**How to fetch pages (use Chrome MCP, NOT curl):**
- `curl` fails on Medium (403), Substack paywalls, Cloudflare bot checks, and JS-rendered SPAs
- Use `chrome-devtools-mcp` (headless Chrome via stdio) or `hangwin/mcp-chrome` (real Chrome profile via extension)
- Chrome MCP tools: `navigate_page`, `take_snapshot`, `evaluate_script`, `get_web_content`
- Example stdio script pattern is in the repo (`/tmp/mcp-*.js`)

**Substack RSS Access (fallback only):**
```bash
curl -s -L -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" "https://[subdomain].substack.com/feed" | grep -oE '<link>[^<]*</link>'
```
Then fetch individual post URLs.

**What to SKIP (do NOT include):**
- Event/conference announcements (CFPs, ticket sales, Devoxx, JavaOne, MCP Dev Summit) — these go to Scalendar, not SIGNAL
- Minor library releases without architectural impact
- Tutorial posts without production context
- Vendor marketing without technical depth
- Future-dated threads: if the newsletter date (e.g., April 2026) is in the future relative to training data, Reddit/HN threads from that month may not exist. Rely on official release notes, blogs, and newsletters instead.

---

### Step 2: Select Content for 3 Sections

**SECTION 1: THE ARCHITECTURE DEBATE**
- One hot topic with genuine controversy
- Two sides of the argument with evidence
- Technical + business implications
- Examples: "Diskless Kafka vs latency", "Scala 3 migration vs LTS", "Rust rewrite vs incremental"
- **MUST HAVE:** "Scalac angle" na końcu

**SECTION 2: NOTES FROM THE TRENCHES**
- One concrete production problem
- Specific context (scale, constraints)
- Solution with code/commands if applicable
- Lesson applicable to other teams
- **MUST HAVE:** "Scalac angle" na końcu

**SECTION 3: SIGNAL OVER NOISE**
- Exactly 3 critical changes
- Each with business/technical context
- Skip trivial patch notes
- Focus: breaking changes, deprecations, major shifts

---

### Step 3: Scalac Angle Format

Każda sekcja Debate i Trenches kończy się "Scalac angle":

**Structure:**
- 2-3 zdania
- Konkretna rekomendacja akcyjna
- Nie esej, nie analiza - co zrobić
- Format: "[Warunek]? [Rekomendacja]. [Alternatywa]? [Rekomendacja]."

**Przykład (DOBRY):**
```
**Scalac angle:** Greenfield without latency constraints? WarpStream under 
Confluent's umbrella carries less operational risk than betting on 2027 timelines. 
Existing Kafka estates? Wait for KIP-1150. Running both systems is what you're 
trying to escape. The decision isn't which technology; it's your organization's 
tolerance for vendor lock-in versus timeline uncertainty.
```

**Przykład (ZŁY - za ogólny):**
```
**Scalac angle:** The framing of this debate is the main problem. It's not 
"WarpStream or Kafka" - it's routing by workload. Teams who wait for a single 
tool that does everything well are paying broker costs while they wait.
```

---

### Step 4: Generate Newsletter

```markdown
---
title: "SIGNAL [Month] [Year]: [Main Topic]"
description: "[SEO description 150-160 chars]"
author: "Scalac Engineering Team"
date: "[YYYY-MM-DD]"
tags: ["distributed-systems", ...]
image: "/images/blog/signal-[month]-[year]-[topic].png"
---

# SIGNAL: What matters in distributed systems

**[Month] [Year] | Issue [N]**

![Hero description](/images/blog/signal-[month]-[year]-[topic].png)
*[Caption for hero image]*

**Welcome back.** [2-3 sentences. Hook with the most surprising/debated insight. 
No throat-clearing.]

**Also:** [2 bullet points teasing other major stories]

---

## Today

• **[Topic 1]** — [One line description]  
• **[Topic 2]** — [One line description]  
• **[Topic 3]** — [One line description]

---

## The Architecture Debate: [Title]

![Image if applicable](/images/blog/...)

**[Bold hook]:** [2-3 sentences with specific evidence/metrics]
**[Bold hook]:** [2-3 sentences with specific evidence/risks]

**Scalac angle:** [2-3 sentences. Concrete recommendations. Challenge both sides.]

---

## Notes from the Trenches: [Title]

![Image if applicable](/images/blog/...)

**[Bold hook - The Problem]:** [Specific symptoms, errors, metrics]
**[Bold hook - The Solution]:** [Step-by-step fix with code/commands]

**Scalac angle:** [Concrete recommendation. What to do in production.]

---

## Signal Over Noise: Three Critical Changes This Month

### 1. [Bold headline]
[2-3 sentences. What changed + why it matters + migration path.]

### 2. [Bold headline]
[Same format]

### 3. [Bold headline]
[Same format]

---

## In the Know

**[Name]** [linked] — [One sentence with source]. [Engagement metric if available].

---

## Top Resources

**Repo:** [link] — [description]
**Paper:** [link] — [description]

---

*Signal is published by [Scalac](https://scalac.io).*

**What is SIGNAL?** A monthly briefing for senior engineering leaders. Three sections: 
Architecture Debate, Notes from the Trenches, Signal Over Noise. No hype. No vendor pitches. 
Just lessons that matter.

---

## References

- [Source 1](URL)
- [Source 2](URL)
```

---

## Images and Visuals

### SIGNAL illustration style

Match the illustration style already used on scalac.io. For SIGNAL, original
diagram-comics take priority over vendor hero images.

- Create `stages/03_draft/output/images.md` with two required prompts: one for
  Architecture Debate and one for Notes from the Trenches. Add a cover prompt only
  when one idea unifies the issue.
- Use a warm off-white background, rough black hand-drawn outlines, solid-black
  sticky figures and red as the only accent. Red carries arrows, warnings,
  underlines and the one metric that matters.
- Make each image a single readable system relationship, failure mode or decision.
  Short hand-lettered labels, speech bubbles and one bottom-line sentence are part
  of the illustration when they clarify the lesson.
- Keep it bright, sparse and 16:9. Exclude vendor logos, gradients, photorealism,
  dense dashboards and generic robots. When AI matters, draw it as a bounded actor
  in the system.

Prompt format: left-to-right composition, exact labels, visual metaphor,
bottom-line sentence, palette and exclusions.

### Hero Images from Blogs (priority)
Always check if the blog post has a hero image. Use it instead of generic logos:

1. **Confluent/Kafka blogs:**
   - Check `<meta property="og:image">` or first large image
   - URL pattern: `https://images.ctfassets.net/...`
   - Example: `curl -s "https://www.confluent.io/blog/POST-URL/" | grep -o 'https://images.ctfassets.net[^"]*'`

2. **Scala blogs:**
   - scala-lang.org: `https://www.scala-lang.org/resources/img/scala-spiral-3d-2-toned-down.png`
   - Check `<meta property="og:image">`

3. **GitHub repos:**
   - Use repo owner's avatar or social preview
   - URL: `https://avatars.githubusercontent.com/u/[USER_ID]`

### Image placement in markdown:
```markdown
![Alt text](/images/blog/filename.png)
*Caption: opis*

**Bold hook:** Rest of paragraph...
```

### Required images per issue:
- Header: Hero image from main source blog (1200x627px)
- 1-2 section images (logos or diagrams) - optional
- Image path format: `/images/blog/signal-[month]-[year]-[topic].png`

---

## Writing Rules (Stop-Slop)

### Banned Phrases
- Throat-clearers: "Here's what you need to know", "In this article", "Let's dive in"
- Emphasis crutches: "crucial", "critical", "essential", "key", "vital", "game-changer"
- Business jargon: "leverage", "synergy", "ecosystem", "paradigm shift", "best practices"
- All adverbs: "importantly", "significantly", "effectively", "efficiently"
- Vague declaratives: "The reasons are structural", "The implications are significant"
- Meta-commentary: "As mentioned earlier", "In conclusion", "To summarize"
- Absolute claims without proof: "entirely", "completely", "all", "removes all", "guarantees"

### Structural Rules
- **Active voice only**: "The team migrated" not "The migration was completed"
- **No passive constructions**
- **No binary contrasts**: Never "not X, it's Y" - state Y directly
- **No em-dashes**: Ever. Use periods or hyphens.
- **Varied rhythm**: Mix sentence lengths. Two items beat three.
- **Specific over vague**: "p99 dropped from 15s to 100ms" not "latency improved"

### Sentence-Level Rules
- No Wh- starters (What, Why, When, Where, Who) at paragraph openings
- No lazy extremes: "every", "always", "never"
- Put the reader in the room: "You" beats "People"

---

## Section Guidelines

### SECTION 1: THE ARCHITECTURE DEBATE
- Real controversy (not manufactured)
- Both sides have valid points
- End with Scalac Angle (expert synthesis)
- Technical depth + business implications
- Bold hooki dla każdej strony argumentu

### SECTION 2: NOTES FROM THE TRENCHES
- Concrete problem (error messages, metrics)
- Production context (scale, constraints)
- Actionable solution
- Transferable lesson
- Scalac angle: co zrobić w produkcji

### SECTION 3: SIGNAL OVER NOISE
- Exactly 3 items
- Breaking changes, deprecations, major shifts only
- Each: What + Why it matters + Migration path
- Skip: minor features, patch releases, betas

---

## Pre-publish Checklist

- [ ] "Welcome back." lub "Welcome to SIGNAL." w introduction (zgodnie z issue number)
- [ ] "Also:" z 2 teaserami
- [ ] "Today" - 4-5 bullet points
- [ ] 3 sekcje: Debate, Trenches, Signals
- [ ] Każda sekcja Debate/Trenches ma "Scalac angle" (konkretna rekomendacja)
- [ ] Signal Over Noise: dokładnie 3 punkty
- [ ] In the Know: 4-5 social/trending items
- [ ] Top Resources: Repo + Paper (+ opcjonalnie Tutorial)
- [ ] Wszystkie linki są konkretne (nie ogólne "x.com/karpathy")
- [ ] Obrazki: min 1 hero, opcjonalnie 1-2 sekcje
- [ ] Issue number w headerze
- [ ] Format "The Code": krótkie akapity, bold hooki, metryki
- [ ] Bez em-dash, bez throat-clearers, bez passive voice
- [ ] Frontmatter z title, description, tags, image
- [ ] Sekcja References na końcu

---

## Fact-Check Guidelines (Verification Rules)

Based on March 2026 issue corrections. Apply to all future issues:

### 1. Release Dates - Verify, Don't Assume
- **ALWAYS** check actual release date in GitHub releases, blog posts, or official announcements
- **NEVER** assume "Released this month" - verify the date
- **Example correction:** Mill 1.0 was July 2025, not March 2026
- **Example correction:** Akka Agentic Platform was announced in 2025, not launched in March 2026

### 2. Metrics and Numbers - Source or Soften
- **Concrete numbers require concrete sources**
- ❌ BAD: "80% cost reductions", "10+ TB/day", "3-6x faster"
- ✅ GOOD: "order-of-magnitude cost reductions reported by early adopters", "significantly faster... with reports of 3-6x in some projects"
- **If no public source:** Use "reportedly", "according to early adopters", or remove the number
- **Never invent metrics** (views, upvotes, engagement numbers)

### 3. Community Voice Quotes - Source or Skip
- **NEVER invent fake Reddit/HN quotes.** If you cannot find a specific thread, synthesize from a real article/blog and attribute it: "[State of Scala 2026](link) synthesizes migration patterns: 'quote...'"
- ❌ BAD: "r/scala on JDK 17: *Paraphrased sentiment:* 'Teams are splitting...'" (no source, implies real thread)
- ✅ GOOD: "Scala ecosystem — [State of Scala 2026](link) synthesizes migration patterns: 'New services should default to 3.8.x...'"
- **Deduplicate HN quotes:** If a Hacker News quote appears in the intro/Today section, do NOT repeat it in Community Voice. Move quotes to the intro once, remove from Community Voice.
- **Specific upvote counts require specific thread links** (HN, Reddit)
- **When in doubt:** Mark as "Paraphrased sentiment from [source name]" with a real link

### 4. Future Dates - Estimate, Don't Promise
- **Roadmap dates are estimates, not facts**
- ❌ BAD: "production readiness is 2027 at earliest"
- ✅ GOOD: "production readiness is unlikely before 2027", "realistically a post-2026 feature"
- **Support timelines:** "through at least 2026" instead of "until Q2 2027" (unless exact date confirmed)

### 5. Technical Claims - Precision Matters
- **Don't overstate integration/dependency:**
  - ❌ BAD: "built entirely on MCP", "removes all BSL dependencies"
  - ✅ GOOD: "with MCP integration", "clean Apache-licensed fork"
- **KIPs/Proposals status:**
  - Check if KIP is "accepted", "under discussion", or "proposed"
  - ❌ BAD: "KIP-1222 adds lease extension" (implies implemented)
  - ✅ GOOD: "KIP-1222 proposes lease extensions... a separate proposal under development"
- **Observed behavior vs official feature:**
  - ❌ BAD: "betterFors stabilised with semantic changes" (implies official)
  - ✅ GOOD: "In practice, we've observed subtle semantic changes with betterFors"

### 6. Social Media/Quotes - Verify or Generalize
- **Specific claims need specific sources**
- ❌ BAD: "hasn't typed code since December 2025 — 2.5M views"
- ✅ GOOD: "describes shifting from mostly manual coding to mostly LLM-assisted coding"
- **Remove:** Exact dates, view counts, engagement metrics unless verified with link

### 7. Companies/Case Studies
- **Verify public case studies:**
  - Robinhood + WarpStream: removed because no public source
  - Manulife + Akka: kept with direct link to press release
- **When mentioning companies:** Link to official announcement, not "reportedly"

### Pre-publish Verification Checklist
- [ ] All release dates verified against GitHub/blog sources
- [ ] All metrics either sourced or softened with "reportedly"/"early adopters"
- [ ] Community Voice quotes attribute real articles/blogs, never fake Reddit threads
- [ ] HN quotes in intro are removed from Community Voice (no duplicates)
- [ ] Reddit quotes either link to specific threads OR marked as "paraphrased" with source
- [ ] Future roadmap dates use "unlikely before" or "post-YYYY" not exact dates
- [ ] Technical integrations use "with X support" not "built entirely on X"
- [ ] KIPs/proposals checked for actual status (accepted vs proposed)
- [ ] Social media claims stripped of unverified metrics (views, dates)
- [ ] Company case studies have direct links to announcements
- [ ] Event announcements (Devoxx, JavaOne, conferences) moved to Scalendar, not In the Know

---

## Quality Scoring

Score 1-10 (minimum 35/50 required):

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Depth | War stories or release notes? |
| Debate | Both sides represented? |
| Actionable | Can reader act on this? |
| Density | Anything cuttable? |

---

## Example: Complete Architecture Debate Section

```markdown
## The Architecture Debate: Diskless Kafka

![Apache Kafka 4.2.0 Release](/images/blog/signal-march-2026-kafka.png)
*Apache Kafka 4.2.0 brings production-ready Share Groups.*

**Apache Kafka approves KIP-1150.** Diskless topics are now officially on the 
Apache Kafka roadmap. The community voted yes on March 2nd, accepting a leaderless 
architecture where brokers serve partitions directly from object storage. 
The catch: production readiness is unlikely before 2027.

**Confluent acquired WarpStream in January.** The proprietary fork already delivers 
order-of-magnitude cost reductions reported by early adopters for log analytics workloads. 
Latency remains in the 100-500ms range — fine for logs, unacceptable for transactions 
requiring sub-50ms p99.

**Scalac angle:** Greenfield without latency constraints? WarpStream under Confluent's 
umbrella carries less operational risk than betting on 2027 timelines. Existing Kafka 
estates? Wait for KIP-1150. The decision isn't which technology; it's your organization's 
tolerance for vendor lock-in versus timeline uncertainty.
```

---

## Lessons from April 2026 Issue

### Content Architecture (what goes where and why)

**Order of sections matters:**
1. **Intro** → 4-5 sentences, narrative, no `Also:`, no bullet points. Tease the month, mention 2-3 biggest stories.
2. **Today** → 6-8 one-line bullets, every bullet linked. This is the table of contents.
3. **Debate** → The main story with real controversy. 3-4 bold hooks, every claim linked (HN thread, blog post, company announcement). Ends with Scalac angle.
4. **Trenches** → Production problem + solution. Every metric and claim sourced. Ends with Scalac angle.
5. **Signal Over Noise** → Exactly 3 critical changes. Each: what + why it matters + migration path.
6. **Community Voice** → Synthesis from real articles/blogs, never fake Reddit threads. Every quote attributed: "[Source](link) synthesizes: 'quote'".
7. **In the Know** → 3-5 short items. NO duplicates with Debate/Trenches. NO events (Devoxx, JavaOne → Scalendar).
8. **Top Resources** → Repo + Tool + Paper. Each with link and one-sentence why.

### Linking Strategy (every claim needs a source)

| Section | What to link | Why |
|---------|-------------|-----|
| Today | Every bullet | Readers scan here first; every claim must be verifiable |
| Debate | HN threads, blog posts, company announcements, people | This is the core argument; without sources it's opinion |
| Trenches | CVE pages, release notes, technical blogs | Production claims require proof |
| Community Voice | The article/blog being synthesized | Without attribution it's fake |
| In the Know | Original announcement or report | Short items still need provenance |
| Top Resources | Direct repo/paper URL | These exist to be clicked |

**Deduplication rule:** If a topic appears in Debate or Trenches, it does NOT appear in In the Know or Community Voice.

### What We Removed and Why

| Removed | Reason | Where it went |
|---------|--------|---------------|
| Images in body | Distraction from text, hard to source | Removed entirely |
| `Also:` section in intro | Duplicates Today bullets | Removed, intro stays narrative |
| Fake Reddit quotes | No real threads found, syntetyczne | Replaced with real article synthesis |
| HN quotes in Community Voice | Duplicates intro/Debate | Removed, kept only in Debate |
| JPMorgan in In the Know | Duplicates Debate | Removed |
| Bram Cohen in In the Know | Duplicates Debate | Removed |
| State of Scala 2026 in Community Voice | Was in March issue | Removed |
| Event announcements (Devoxx, JavaOne, MCP Summit) | Events go to Scalendar, not SIGNAL | Removed from In the Know |
| JVM listing sentence in intro | "Kafka graduated and Rust shipped" reads like a bullet | Removed, keep intro narrative |

---

## Lessons from May 2026 Issue

### Link Placement

**Today section** -- Link belongs on the bold text, not loose at the end of the bullet:
```
- **[Oracle proposes JVMCI deprecation.](https://link)** The JVM Compiler Interface is marked for removal.
```
Never:
```
- **Oracle proposes JVMCI deprecation.** The JVM Compiler Interface is marked for removal.
  [JVM Weekly Vol. 176](https://link)
```

**Signal Over Noise** -- Embed the link in the first sentence of each item. Never leave a bare `[Source](url)` at the end of the paragraph.

**In the Know** -- Use bullet format, NOT a markdown table. Tables break in many renderers.
```
**[Name](link)** -- One sentence description.
```

### Date References in Body

The newsletter header already says the month and year. Do NOT repeat "in May 2026", "in April 2026" etc. throughout the body -- it reads like a changelog.

- Opening of Debate/Trenches: drop the date entirely. "Oracle opened JDK-8382582" not "In May 2026, Oracle opened JDK-8382582."
- Signal Over Noise: use "last month" if a date reference is needed, or omit.
- Never repeat the same month phrase more than once in the body.

### Footer Consistency

The "What is SIGNAL?" block must be identical across all issues:
```
**What is SIGNAL?**

SIGNAL is a monthly, opinionated newsletter for engineers building and operating JVM and Scala systems, and agentic AI in production.

Each issue has three sections: Architecture Debate, Notes from the Trenches, and Signal Over Noise. They cover architecture decisions, production lessons, incidents, and ecosystem shifts worth paying attention to. No hype. No vendor talking points.

At Scalac, we build high-throughput distributed systems and agentic AI products in Scala, Java, and Rust. SIGNAL is the filter we wanted when making our own architecture bets.

**Have a story for SIGNAL?** Reply to this email. We read every response.
```
Do NOT have two separate blocks describing Scalac and SIGNAL -- merge into one.

### Signal Over Noise Selection Criteria

"Signal Over Noise" = breaking changes, deprecations, major shifts with migration implications. NOT opinion essays without hard data. If there is no concrete action a reader can take, it does not belong here.

### Paywalled Sources

Do NOT reference articles behind paywalls (e.g. Pragmatic Engineer paid tier) as primary sources. If the key data point is not accessible, either find a free alternative source or drop the story.

### KotlinConf / JetBrains Ecosystem

KotlinConf (typically May, Munich) is a tier-1 event for this newsletter's audience. Always check:
- Kotlin release announcements (breaking changes, backend removals)
- JetBrains agent/AI framework releases (Koog, kotlin-agent-skills)
- Security policy updates (CVE numbering, support windows)

### Substack RSS Access

Substack blocks bots on the homepage. To read newsletters programmatically:
```bash
curl -s -L -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" "https://[subdomain].substack.com/feed" | grep -oE '<link>[^<]*</link>'
```
Then fetch individual post URLs.

---

## Output

Generate:
1. **Newsletter draft** in Markdown
2. **Sources used** - brief list
3. **Skipped sources** - rejected signals (for reference)
4. **Image prompts** - two section prompts and, when useful, one cover prompt

Do NOT:
- Include conference events (CFPs, ticket sales)
- Add artificial endings
- Use em-dashes
- Reference Scalac case studies by name in body
