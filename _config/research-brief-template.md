# SIGNAL Research Brief Template

Use this skeleton for every issue. One section per heading.

## §1 Issue Metadata

- Issue number:
- Month / Year:
- Target publish date:
- Main theme or hook:

## §2 Source Coverage

List which required sources were checked and what they yielded:

| Source | Checked | Notable stories |
|--------|---------|-----------------|
| JVM Weekly | Yes / No | |
| This Week in Scala | Yes / No | |
| InfoQ Architects' Newsletter | Yes / No | |
| ByteByteGo | Yes / No | |
| Pragmatic Engineer | Yes / No | |
| r/scala | Yes / No | |
| r/apachekafka | Yes / No | |
| Hacker News | Yes / No | |

## §3 Candidate Register

8-15 candidates in a table. Every row needs every field filled before selection starts. "Unknown" is an acceptable value; a blank is not, because a blank hides the fact that nobody checked.

| Field | Requirement |
|-------|-------------|
| Working title | One sentence, no clickbait |
| Track | JVM / Scala-Kotlin / Kafka-streaming / distributed-correctness / agentic |
| Freshness | `NEW_THIS_MONTH`, `MATERIAL_UPDATE`, or `BACKGROUND_ONLY` (see `fact-check-rules.md`) |
| Event date | Date of the originating artefact, not the date of the article about it |
| Claim | One falsifiable sentence |
| Primary source | Link plus type: JEP / KIP / RFC / paper / repo / release / disclosure |
| Verification | An independent source or an executable artefact |
| Hard evidence | The number, status, diff, benchmark, test result, incident, or spec |
| Trade-off | What you gain and what you give up |
| Community reaction | Optional. Link plus what the sides actually argue. Engagement numbers go here, never in the evidence column. |
| Score | Rubric below |
| Decision | `SELECT` / `CONTEXT` / `REJECT` plus a one-line reason |

### Scoring rubric

Score each candidate 0-5 on six dimensions:

1. **Freshness** — did it actually happen this month?
2. **Relevance** — does it touch agentic / JVM / Scala / Kafka / distributed systems?
3. **Evidence** — is there a primary source and a checkable artefact?
4. **Stakes** — does it change an architecture, cost, or risk decision?
5. **Tension** — is there a real trade-off or an honest disagreement?
6. **Originality** — has general tech media already chewed it over?

Select from roughly 20/30 upward. Two hard rules override the score:

- **A low-evidence topic can never be the headline**, regardless of how much engagement it has. Engagement is a reason to investigate, never a substitute for proof.
- **A `BACKGROUND_ONLY` item can never be Debate, Trenches, or a Signal.** Context sentence or In the Know only.

## §4 Debate Candidate

- Topic:
- Side A (with evidence/link):
- Side B (with evidence/link):
- Why it matters for CTOs:
- Scalac angle (first draft):

## §5 Trenches Candidate

- Problem:
- Context (scale, constraints):
- Solution (with code/commands if applicable):
- Lesson:
- Scalac angle (first draft):

## §6 Signal Over Noise Candidates

Pick exactly 3 from §3. For each:

1. **Headline:**
   - What changed:
   - Why it matters:
   - Migration path:
   - Source:

2. **Headline:**
   - What changed:
   - Why it matters:
   - Migration path:
   - Source:

3. **Headline:**
   - What changed:
   - Why it matters:
   - Migration path:
   - Source:

## §7 In the Know Candidates

3-5 short items that do not duplicate Debate/Trenches/Signals.

## §8 Top Resources

- Repo to watch:
- Article to read:
- Paper to read:

## §9 Skipped Sources / Rejected Signals

List signals considered but rejected and why (duplicate, weak source, no production context, paywalled).

## §10 Image List

- Hero image source:
- Section images (optional):
- Alt text for each:

## §11 Open Questions / Fact-Check Needs

List any claims that need verification before draft.
