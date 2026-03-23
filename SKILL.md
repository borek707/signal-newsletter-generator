---
name: signal-newsletter-generator
description: Generate the SIGNAL newsletter for Scalac. Use when the user asks to create a monthly newsletter, generate SIGNAL, or prepare the distributed systems newsletter. This skill searches Reddit communities for trending discussions, analyzes them as signals, and produces a draft newsletter with Scalac Angle expert commentary.
metadata:
  trigger: "monthly newsletter", "SIGNAL", "distributed systems newsletter", "create newsletter", "prepare newsletter draft"
  author: Scalac
  schedule: monthly
---

# SIGNAL Newsletter Generator

Generate a monthly B2B newsletter targeting CTO, VP of Engineering, and Chief Architect roles. The newsletter identifies two significant signals from distributed systems communities and provides expert analysis.

## Workflow

### Step 1: Collect Signals from Reddit

Search these subreddits for trending discussions:

1. **r/scala** - Scala ecosystem, functional programming, JVM trends
2. **r/rust** - Systems programming, performance, memory safety
3. **r/apachekafka** - Streaming infrastructure, Kafka migrations, operational issues
4. **r/dataengineering** - Data pipelines, infrastructure decisions, tool comparisons

Use web search to find recent high-engagement posts from these communities. Focus on:
- Posts with 50+ upvotes or 30+ comments
- Migration stories (e.g., "we moved from X to Y")
- Performance benchmarks and comparisons
- Cost optimization discussions
- "Why we chose/switched to" posts
- Production incidents and lessons learned

### Step 2: Select Two Signals

Choose signals based on:
- **Relevance**: Impacts infrastructure decisions
- **Recency**: Discussed within the last 30 days
- **Depth**: Has enough substance for analysis (not just a link)
- **Tension**: Involves real trade-offs (cost vs latency, simplicity vs control, etc.)

Good signals show engineering teams making difficult decisions with measurable outcomes.

### Step 3: Generate Newsletter Draft

Write the newsletter following this exact structure:

```
SIGNAL
What matters in distributed systems
[Month] [Year] | Issue [N]

[Intro paragraph - 3-4 sentences about the value proposition]

---

Signal 1: [Title]
[2-3 paragraphs describing the signal and context]

[Diagram placeholder - describe what diagram should illustrate]

Why It Matters
[1-2 paragraphs on implications]

SCALAC ANGLE
[Expert opinion with specific, actionable insight - 2-3 sentences]

---

Signal 2: [Title]
[Same structure as Signal 1]

---

The Takeaway
[2 paragraphs synthesizing both signals and their broader implications]

---

Signal is published by Scalac. We build distributed systems for teams who ship.
```

## Writing Rules (Stop-Slop)

CRITICAL: Follow these rules to avoid AI-typical writing patterns:

### Banned Phrases
- Throat-clearers: "Here's what you need to know", "In this article", "Let's dive in", "It's worth noting"
- Emphasis crutches: "crucial", "critical", "essential", "key", "vital", "game-changer"
- Business jargon: "leverage", "synergy", "ecosystem", "paradigm shift", "best practices"
- All adverbs: especially "importantly", "significantly", "effectively", "efficiently"
- Vague declaratives: "The reasons are structural", "The implications are significant"
- Meta-commentary: "As mentioned earlier", "In conclusion", "To summarize"

### Structural Rules
- **Active voice only**: Every sentence needs a human subject doing something
- **No passive constructions**: Never "the decision was made" - instead "the team decided"
- **No binary contrasts**: Never "not X, it's Y" - state Y directly
- **No em-dashes**: Ever
- **Varied rhythm**: Mix sentence lengths. Two items beat three. End paragraphs differently.
- **Specific over vague**: Name the specific thing, not abstractions

### Sentence-Level Rules
- No Wh- sentence starters (What, Why, When, Where, Who) at paragraph openings
- No lazy extremes: "every", "always", "never" doing vague work
- Put the reader in the room: "You" beats "People", specifics beat abstractions
- Cut quotables: If it sounds like a pull-quote, rewrite it

## Scalac Angle Guidelines

The Scalac Angle section provides expert commentary. It should:
- Offer a specific, actionable insight (not generic advice)
- Reference real experience (e.g., "We see teams underestimating...")
- Include concrete timelines or thresholds when relevant
- Challenge vendor promises with realistic expectations
- Recommend specific approaches or starting points

Format as a highlighted box with blue left border.

## Quality Scoring

Before finalizing, score 1-10 on each dimension (minimum 35/50 required):

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

## Output Format

Generate:
1. **Newsletter draft** in plain text (ready for review)
2. **Signal sources** - brief list of where each signal came from (for your reference)
3. **Diagram suggestions** - describe what visual would enhance each signal

Do NOT:
- Include external links in the newsletter body
- Reference specific Scalac case studies by name
- Add artificial endings ("End of newsletter")

## Example Signal Structure

**Signal: Kafka Economics Are Shifting**

Robinhood migrated their Kafka deployment to WarpStream. The engineering team posted details about the decision process. Cost drove the choice. Self-hosted Kafka at scale requires dedicated infrastructure teams. Broker management, partition rebalancing, replication factor tuning. These tasks consume engineering cycles that could ship features.

The discussion threads reveal a pattern. Teams running Kafka clusters above 50 brokers hit operational complexity walls. The threshold varies by organization, but the wall exists. Cloud-native alternatives promise to remove that wall. The trade-off? Latency increases.

**Why It Matters**

Streaming infrastructure decisions now balance three factors: operational burden, latency requirements, and cloud costs. Self-hosted Kafka wins on latency and control. Cloud-native options win on operational simplicity. Your latency budget determines the viable options.

**SCALAC ANGLE**

We see teams underestimating migration complexity. Moving from self-hosted Kafka to a cloud provider requires rewriting consumer offset management, adjusting retention policies, and rethinking exactly-once semantics. Budget 3-6 months for migration at scale, not the 6 weeks vendors promise.
