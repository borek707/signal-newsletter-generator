---
name: signal-newsletter-generator
description: Generate the SIGNAL newsletter for Scalac. Use when the user asks to create a monthly newsletter, generate SIGNAL, or prepare the distributed systems newsletter. This skill produces a strategic engineering newsletter combining The Code format (short, punchy) with deep architectural analysis (3 sections: Debate, Trenches, Signal).
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

## Workflow

### Step 1: Collect Signals from Multiple Sources

**Primary Sources:**
1. **r/scala** - Scala ecosystem, FP, JVM trends
2. **r/rust** - Systems programming, performance, safety
3. **r/apachekafka** - Streaming, migrations, ops
4. **r/dataengineering** - Pipelines, architecture decisions
5. **InfoQ** - Enterprise case studies
6. **Hacker News** - Engineering discussions
7. **Engineering Blogs** - Reddit, Netflix, Uber, Confluent, Lightbend/Akka

**What to look for:**
- "Migrated from X to Y" with metrics
- Post-mortems ("lessons learned", "incident report")
- Architecture debates (50+ comments, controversy)
- Cost reductions ("cut bill by 80%")
- Breaking changes in core tools
- AI integration in existing stacks

**What to SKIP (do NOT include):**
- Event/conference announcements (CFPs, ticket sales) — these go to Scalendar
- Minor library releases without architectural impact
- Tutorial posts without production context
- Vendor marketing without technical depth

### Step 2: Select Content for 3 Sections

**SECTION 1: THE ARCHITECTURE DEBATE**
- One hot topic with genuine controversy
- Two sides of the argument with evidence
- Technical + business implications
- Examples: "Diskless Kafka vs latency", "Scala 3 migration vs LTS", "Rust rewrite vs incremental"

**SECTION 2: NOTES FROM THE TRENCHES**
- One concrete production problem
- Specific context (scale, constraints)
- Solution with code/commands
- Lesson applicable to other teams

**SECTION 3: SIGNAL OVER NOISE**
- Exactly 3 critical changes
- Each with business/technical context
- Skip trivial patch notes
- Focus: breaking changes, deprecations, major shifts

### Step 3: Generate Newsletter

```
# SIGNAL
## What matters in distributed systems
[Month] [Year] | Issue [N]

**Welcome back.** [2-3 sentences. Hook with the most surprising/debated insight. No throat-clearing.]

**Also:** [2 bullet points teasing other major stories]

---

### **Today's Insights**

* [Bullet 1: Main debate topic]
* [Bullet 2: Production lesson]
* [Bullet 3: Critical change]

---

##### **SECTION 1: THE ARCHITECTURE DEBATE**

## **[Title of debate]**

[Setup: 2-3 sentences what sparked the debate and why it matters now.]

**The Arguments For:**
[2-3 sentences with specific evidence/metrics]

**The Arguments Against:**
[2-3 sentences with specific evidence/risks]

**The Scalac Angle:**
[2-3 sentences. Our expert take. Challenge both sides if needed. Concrete recommendation.]

---

##### **SECTION 2: NOTES FROM THE TRENCHES**

## **[Title of production problem]**

[Context: Scale, constraints, stakes. 2-3 sentences.]

**The Problem:**
[Specific symptoms, errors, metrics]

**The Solution:**
[Step-by-step fix with code/commands if applicable]

**The Lesson:**
[Why this matters beyond this specific case]

---

##### **SECTION 3: SIGNAL OVER NOISE**

## **Three critical changes this month**

**1. [Bold headline]:** [2-3 sentences. What changed + why it matters + migration path.]

**2. [Bold headline]:** [Same format]

**3. [Bold headline]:** [Same format]

---

##### **IN THE KNOW**

## **What's trending on X, HN, and engineering blogs**

* **[Bold topic]:** [One sentence]. [Source: X/HN/Threads with engagement metric]
* **[Bold topic]:** [One sentence]. [Source]
* **[Bold topic]:** [One sentence]. [Source]
* **[Bold topic]:** [One sentence]. [Source]

---

##### **TOP & TRENDING RESOURCES**

### **Tutorial of the Month**

**[Title](URL):** [One sentence: what it teaches, who it's for, why it stands out.]

---

### **Repo of the Month**

**[Project Name](URL):** [One sentence: what it does, tech stack, why it matters now.]

---

### **Paper of the Month**

**[Paper Title](URL):** [One sentence: the insight and practical implication.]

---

Signal is published by Scalac. We build distributed systems for teams who ship.

**Want deeper analysis?** Explore our case studies at scalac.io/case-studies  
**Subscribe:** Receive The Distributed Pulse monthly by signing up at scalac.io/newsletter
```

## Writing Rules (Stop-Slop)

### Banned Phrases
- Throat-clearers: "Here's what you need to know", "In this article", "Let's dive in"
- Emphasis crutches: "crucial", "critical", "essential", "key", "vital", "game-changer"
- Business jargon: "leverage", "synergy", "ecosystem", "paradigm shift", "best practices"
- All adverbs: "importantly", "significantly", "effectively", "efficiently"
- Vague declaratives: "The reasons are structural", "The implications are significant"
- Meta-commentary: "As mentioned earlier", "In conclusion", "To summarize"

### Structural Rules
- **Active voice only**: "The team migrated" not "The migration was completed"
- **No passive constructions**
- **No binary contrasts**: Never "not X, it's Y" - state Y directly
- **No em-dashes**: Ever
- **Varied rhythm**: Mix sentence lengths. Two items beat three.
- **Specific over vague**: "p99 dropped from 15s to 100ms" not "latency improved"

### Sentence-Level Rules
- No Wh- starters (What, Why, When, Where, Who) at paragraph openings
- No lazy extremes: "every", "always", "never"
- Put the reader in the room: "You" beats "People"

## Section Guidelines

### SECTION 1: THE ARCHITECTURE DEBATE
- Real controversy (not manufactured)
- Both sides have valid points
- End with Scalac Angle (expert synthesis)
- Technical depth + business implications

### SECTION 2: NOTES FROM THE TRENCHES  
- Concrete problem (error messages, metrics)
- Production context (scale, constraints)
- Actionable solution
- Transferable lesson

### SECTION 3: SIGNAL OVER NOISE
- Exactly 3 items
- Breaking changes, deprecations, major shifts only
- Each: What + Why it matters + Migration path
- Skip: minor features, patch releases, betas

## Quality Scoring

Score 1-10 (minimum 35/50 required):

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Depth | War stories or release notes? |
| Debate | Both sides represented? |
| Actionable | Can reader act on this? |
| Density | Anything cuttable? |

## Output

Generate:
1. **Newsletter draft** in Markdown
2. **Sources used** - brief list
3. **Skipped sources** - rejected signals (for reference)

Do NOT:
- Include conference events (CFPs, ticket sales)
- Add artificial endings
- Use em-dashes
- Reference Scalac case studies by name in body
