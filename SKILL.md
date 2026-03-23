---
name: signal-newsletter-generator
description: Generate the SIGNAL newsletter for Scalac. Use when the user asks to create a monthly newsletter, generate SIGNAL, or prepare the distributed systems newsletter. This skill searches for trending discussions, engineering blogs, and community news to produce a draft newsletter following The Code format with multiple short insights.
metadata:
  trigger: "monthly newsletter", "SIGNAL", "distributed systems newsletter", "create newsletter", "prepare newsletter draft"
  author: Scalac
  schedule: monthly
---

# SIGNAL Newsletter Generator

Generate a monthly B2B newsletter targeting CTO, VP of Engineering, and Chief Architect roles. The newsletter aggregates 4-6 significant signals from distributed systems communities and provides expert analysis in The Code format.

## Workflow

### Step 1: Collect Signals from Multiple Sources

Search these sources for trending discussions and news:

**Primary Sources:**
1. **r/scala** - Scala ecosystem, functional programming, JVM trends
2. **r/rust** - Systems programming, performance, memory safety
3. **r/apachekafka** - Streaming infrastructure, Kafka migrations, operational issues
4. **r/dataengineering** - Data pipelines, infrastructure decisions, tool comparisons
5. **InfoQ** - Enterprise architecture case studies
6. **Hacker News** - Engineering discussions, Show HN projects
7. **Engineering Blogs** - Reddit, Netflix, Uber, Confluent, etc.

**Focus areas:**
- Migration stories (e.g., "we moved from X to Y")
- Performance benchmarks with specific metrics
- Cost optimization discussions with numbers
- "Why we chose/switched to" posts
- Production incidents and lessons learned
- New tools/frameworks gaining traction
- Funding/acquisitions in infrastructure space

Use web search to find recent high-engagement posts from these communities. Look for:
- Posts with 50+ upvotes or 30+ comments
- Published within last 30 days
- Discussion in comments (not just link sharing)
- Specific metrics ("20x improvement", "50% cost reduction")

### Step 2: Select 4-6 Signals

Choose signals based on:
- **Relevance**: Impacts infrastructure decisions
- **Recency**: Discussed within last 30 days
- **Depth**: Has enough substance for analysis
- **Diversity**: Mix of migrations, benchmarks, incidents, announcements
- **Tension**: Involves real trade-offs (cost vs latency, simplicity vs control)

Good signals show engineering teams making difficult decisions with measurable outcomes.

### Step 3: Generate Newsletter Draft

Write the newsletter following this exact structure:

```
# SIGNAL
## What matters in distributed systems
[Month] [Year] | Issue [N]

**Welcome back.** [2-3 sentences summarizing the biggest stories. Hook the reader with the most surprising insight.]

**Also:** [2-3 bullet points teasing other stories in the issue]

---

### **Today's Insights**

* [Bullet point 1]
* [Bullet point 2]
* [Bullet point 3]
* [Bullet point 4]

---

##### **TODAY IN DISTRIBUTED SYSTEMS**

**[Bold headline]:** [One paragraph, 3-4 sentences. Lead with specific metrics. Link to source.] [Read more](URL)

**[Bold headline]:** [Same format. Different story. Vary the topics - one migration, one cost story, one performance, one announcement.]

**[Bold headline]:** [Continue for 4-5 stories total]

---

##### **INSIGHT**

## **[Title of deep analysis]**

**[Setup the debate/trend.]** [2-3 sentences explaining why this matters now.]

**[Argument A.]** [2-3 sentences presenting one side with evidence.]

**[Argument B.]** [2-3 sentences presenting counter-argument with evidence.]

**[The synthesis.]** [2-3 sentences on what smart teams actually do.]

---

##### **IN THE KNOW**

## **What's trending on socials and engineering blogs**

* **[Bold topic]:** [One sentence summary]. [Link or source]
* **[Bold topic]:** [One sentence summary]. [Link or source]
* **[Bold topic]:** [One sentence summary]. [Link or source]
* **[Bold topic]:** [One sentence summary]. [Link or source]

---

##### **AI CODING HACK** (or **DISTRIBUTED SYSTEMS HACK**)

## **[Title of practical technique]**

[Context: When would you use this? 1-2 sentences.]

[The technique: Step-by-step or pattern description. Use code blocks if relevant.]

[Why it works: 1-2 sentences on the principle behind it.]

---

##### **TOP & TRENDING RESOURCES**

### **Top Tutorial**

**[Title](URL):** [One sentence describing what it teaches and who it's for.]

---

### **Top Repo**

**[Project Name](URL):** [One sentence on what it does and why it matters.]

---

### **Trending Paper**

**[Paper Title](URL):** [One sentence on the insight and why practitioners should care.]

---

##### **SCALAC ANGLE**

**On [First Story]:** [Expert opinion with specific, actionable insight - 2-3 sentences. Challenge vendor promises or highlight hidden complexity.]

**On [Second Story]:** [Same format. Connect to real experience: "We see teams..." or "We witnessed similar patterns when..."]

**On [Third Story]:** [Same format. Include concrete timeline or threshold when relevant.]

---

Signal is published by Scalac. We build distributed systems for teams who ship.

**Want deeper analysis?** Explore our case studies at scalac.io/case-studies  
**Subscribe:** Receive The Distributed Pulse monthly by signing up at scalac.io/newsletter
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
- **Lead with metrics**: Put numbers in the first sentence of each story

### Sentence-Level Rules
- No Wh- sentence starters (What, Why, When, Where, Who) at paragraph openings
- No lazy extremes: "every", "always", "never" doing vague work
- Put the reader in the room: "You" beats "People", specifics beat abstractions
- Cut quotables: If it sounds like a pull-quote, rewrite it

## Section Guidelines

### TODAY IN DISTRIBUTED SYSTEMS
- 4-5 stories, each 3-4 sentences
- Bold the headline (not a question)
- Start with metrics: "p99 latency dropped 50%", "costs fell 80%", "1M lines/month"
- End with [Read more](URL) link
- Vary story types: migration, performance, cost, announcement, incident

### INSIGHT
- Pick ONE trend/debate from the stories
- Present as "Some say X, others say Y, the reality is Z"
- Avoid taking sides - show the trade-off
- 3 short paragraphs: setup, debate, synthesis

### IN THE KNOW
- 4-5 bullet points
- Mix of social media trends, GitHub repos, conference talks
- One sentence per item
- Include view counts or engagement metrics when available

### AI CODING HACK / DISTRIBUTED SYSTEMS HACK
- Practical technique from one of the stories
- Include specific commands, code, or process steps
- Explain when to use it and when NOT to use it

### TOP & TRENDING RESOURCES
- Tutorial: Link to guide/case study with target audience
- Repo: GitHub project with one-line description
- Paper: Academic or technical paper with practical insight

### SCALAC ANGLE
- 3 separate takes on 3 different stories
- Each 2-3 sentences max
- Include "We see teams..." or "We witnessed..." or "Budget X months..."
- Challenge vendor claims with realistic expectations
- Offer concrete thresholds ("40% of timeline", "3-6 months")

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
1. **Newsletter draft** in Markdown (ready for review)
2. **Signal sources** - brief list of URLs used
3. **Skipped sources** - interesting but rejected signals (for your reference)

Do NOT:
- Include external links in the newsletter body (except in [Read more] and Resources)
- Reference specific Scalac case studies by name in body text
- Add artificial endings ("End of newsletter")
- Use em-dashes anywhere in the text
