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

**Primary Sources:**
1. **r/scala** - Scala ecosystem, FP, JVM trends
2. **This Week in Scala** ([Substack](https://thisweekinscala.substack.com/)) - Weekly Scala ecosystem roundup, releases, community news
3. **JVM Weekly** ([jvm-weekly.com](https://www.jvm-weekly.com/)) - JVM ecosystem updates, performance, tooling
4. **r/rust** - Systems programming, performance, safety
5. **This Week in Rust** ([this-week-in-rust.org](https://this-week-in-rust.org/)) - Curated Rust updates, RFCs, project news
6. **r/apachekafka** - Streaming, migrations, ops
7. **r/dataengineering** - Pipelines, architecture decisions
8. **InfoQ** - Enterprise case studies
9. **Hacker News** - Engineering discussions
10. **Engineering Blogs** - Reddit, Netflix, Uber, Confluent, Lightbend/Akka

**What to look for:**
- "Migrated from X to Y" with metrics
- Post-mortems ("lessons learned", "incident report")
- Architecture debates (50+ comments, controversy)
- Cost reductions ("cut bill by 80%")
- Breaking changes in core tools
- AI integration in existing stacks

**Substack sources (This Week in Scala, etc.):**
- Substack blocks bots on the homepage. Use RSS feed with mobile user-agent: `curl -s -L -A "Mozilla/5.0 (iPhone...)" "https://[subdomain].substack.com/feed"`
- Parse `<pubDate>` and `<link>` to get weekly issues, then fetch individual posts

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

## Output

Generate:
1. **Newsletter draft** in Markdown
2. **Sources used** - brief list
3. **Skipped sources** - rejected signals (for reference)
4. **Images list** - what images to include with sources

Do NOT:
- Include conference events (CFPs, ticket sales)
- Add artificial endings
- Use em-dashes
- Reference Scalac case studies by name in body
