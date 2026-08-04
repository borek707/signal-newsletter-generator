# SIGNAL Voice and Style

SIGNAL is written in **The Code format**: short, punchy, metric-driven.

## Do

- Short paragraphs (max 2-3 sentences), then line break.
- Bold hooks at the start: `**KIP-1150 makes diskless Kafka official:**`
- Metrics first: `80% cost reductions`, `10+ TB/day`, `100-500ms`.
- Active voice: `Apache Kafka approves` not `KIP-1150 was approved`.
- Concrete recommendations in `Scalac angle`, not general theses.
- Use hyphens (`-`) or periods. Never em-dashes (`—`).
- Link every company, project, and person mentioned.
- Put the reader in the room: `You` beats `People`.
- Varied rhythm: mix sentence lengths. Two items beat three.
- Specific over vague: `p99 dropped from 15s to 100ms` not `latency improved`.

## Don't

### Throat-clearers
- "Here's what you need to know"
- "In this article"
- "Let's dive in"
- "As mentioned earlier"
- "In conclusion"
- "To summarize"

### Emphasis crutches
- crucial
- critical
- essential
- key
- vital
- game-changer

### Business jargon
- leverage
- synergy
- ecosystem
- paradigm shift
- best practices
- unlock
- unlock value

### Adverbs
- importantly
- significantly
- effectively
- efficiently
- notably
- fundamentally

### Vague declaratives
- "The reasons are structural"
- "The implications are significant"
- "This changes everything"

### Absolute claims without proof
- entirely
- completely
- all
- removes all
- guarantees
- always
- never
- every

### Lazy extremes
- "every"
- "always"
- "never"

### Binary contrasts
- Never "not X, it's Y" — state Y directly.

### Wh- starters at paragraph openings
- Avoid starting paragraphs with What, Why, When, Where, Who.

### Passive voice
- "The team migrated" not "The migration was completed".

## Date Rules

- The header already says the month and year.
- Do NOT repeat "in May 2026", "in April 2026" throughout the body.
- Opening of Debate/Trenches: drop the date entirely. `Oracle opened JDK-8382582` not `In May 2026, Oracle opened JDK-8382582.`
- Signal Over Noise: use `last month` if a date reference is needed, or omit.
- Never repeat the same month phrase more than once in the body.

## Link Rules

- Today section: link belongs on the bold text, not loose at the end.
- Debate: link HN threads, blog posts, company announcements, people.
- Trenches: link CVE pages, release notes, technical blogs.
- Signal Over Noise: embed the link in the first sentence. No bare `[Source](url)` at the end of the paragraph.
- In the Know: every item linked.
- Top Resources: direct repo/paper URL.
- References: title + URL at the end.

## Metric Rules

- Concrete numbers require concrete sources.
- If no public source: use `reportedly`, `according to early adopters`, or remove the number.
- Never invent metrics (views, upvotes, engagement numbers).
