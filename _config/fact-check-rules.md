# SIGNAL Fact-Check Rules

Based on corrections from March, April, May, and July 2026 issues. Apply to all future issues.

## Freshness Classification (do this first, for every candidate)

Tag every candidate before it enters the selection table. This is the cheapest defence against the most common research failure: a real, well-sourced story that simply did not happen this month.

| Tag | Meaning | How it may be used |
|-----|---------|--------------------|
| `NEW_THIS_MONTH` | The originating event happened inside the issue's month. | Eligible for Debate, Trenches, or Signal Over Noise. |
| `MATERIAL_UPDATE` | Older story that gained a real new status this month (merge, GA release, accepted KIP/JEP, new benchmark result, incident disclosure). | Eligible, but the write-up must name what changed *this month*, not restate the original story. |
| `BACKGROUND_ONLY` | Real and relevant, but nothing new happened this month. | Context sentence or In the Know at most. **Never present as news.** |

**Publication date is not event date.** When they differ, record both and base the freshness tag on the event date. A July blog post about a June release is `BACKGROUND_ONLY` or `MATERIAL_UPDATE`, never `NEW_THIS_MONTH`.

Observed failures this rule exists for (July 2026 research pass): Scala 3.3.8 LTS was claimed as a July release, actually shipped June 10. ScarfBench was pitched as a July story, actually published March with a June 30 blog post. Definity's Spark-agent story was surfaced as current, actually dated April 29. Kotlin's Koog 1.0 read as new, actually already covered in the May issue. All four were real; none were July news.

## 1. Release Dates — Verify, Don't Assume

- **ALWAYS** check actual release date in GitHub releases, blog posts, or official announcements.
- **NEVER** assume "Released this month".
- Example correction: Mill 1.0 was July 2025, not March 2026.
- Example correction: Akka Agentic Platform was announced in 2025, not launched in March 2026.

## 2. Metrics and Numbers — Source or Soften

- Concrete numbers require concrete sources.
- ❌ BAD: "80% cost reductions", "10+ TB/day", "3-6x faster"
- ✅ GOOD: "order-of-magnitude cost reductions reported by early adopters", "significantly faster... with reports of 3-6x in some projects"
- If no public source: use "reportedly", "according to early adopters", or remove the number.
- Never invent metrics (views, upvotes, engagement numbers).

## 3. Community Voice Quotes — Source or Skip

- **NEVER** invent fake Reddit/HN quotes.
- If you cannot find a specific thread, synthesize from a real article/blog and attribute it: `[State of Scala 2026](link) synthesizes migration patterns: 'quote...'`
- Deduplicate HN quotes: if a HN quote appears in the intro/Today section, do NOT repeat it in Community Voice.
- Specific upvote counts require specific thread links.
- When in doubt: mark as "Paraphrased sentiment from [source name]" with a real link.

## 4. Future Dates — Estimate, Don't Promise

- Roadmap dates are estimates, not facts.
- ❌ BAD: "production readiness is 2027 at earliest"
- ✅ GOOD: "production readiness is unlikely before 2027", "realistically a post-2026 feature"
- Support timelines: "through at least 2026" instead of "until Q2 2027" unless exact date confirmed.

## 5. Technical Claims — Precision Matters

- Don't overstate integration/dependency:
  - ❌ BAD: "built entirely on MCP", "removes all BSL dependencies"
  - ✅ GOOD: "with MCP integration", "clean Apache-licensed fork"
- KIPs/Proposals status:
  - Check if KIP is "accepted", "under discussion", or "proposed".
  - ❌ BAD: "KIP-1222 adds lease extension" (implies implemented)
  - ✅ GOOD: "KIP-1222 proposes lease extensions... a separate proposal under development"
- Observed behavior vs official feature:
  - ❌ BAD: "betterFors stabilised with semantic changes" (implies official)
  - ✅ GOOD: "In practice, we've observed subtle semantic changes with betterFors"

## 6. Social Media/Quotes — Verify or Generalize

- Specific claims need specific sources.
- ❌ BAD: "hasn't typed code since December 2025 — 2.5M views"
- ✅ GOOD: "describes shifting from mostly manual coding to mostly LLM-assisted coding"
- Remove exact dates, view counts, engagement metrics unless verified with link.

## 7. Companies/Case Studies

- Verify public case studies.
- Example: Robinhood + WarpStream removed because no public source.
- Example: Manulife + Akka kept with direct link to press release.
- When mentioning companies: link to official announcement, not "reportedly".

## 8. Paywalled Sources

- Do NOT reference articles behind paywalls (e.g. Pragmatic Engineer paid tier) as primary sources.
- If the key data point is not accessible, either find a free alternative source or drop the story.

## 9. Claim-Level Banned Words (different from the style bans in `voice.md`)

`voice.md` bans marketing filler. These words are banned for a different reason: each one asserts a *verifiable precision* that is usually not verified. Do not use any of them without a direct source and an explicit scope.

| Word | Only usable when |
|------|------------------|
| `first` / `first industrial` | A source states it and you can name the category it is first *in*. Cloudflare's own Meerkat post says "to our knowledge, the first industrial deployment of QuePaxa at global scale" — quote that framing, don't flatten it to "first". |
| `largest` / `biggest` | A cited number and a named comparison set exist. |
| `production-ready` / `production-proven` | A named organisation is running it in production, with a public source. Otherwise: `experimental`, `research`, `proof-of-concept`, `early-stage`. |
| `exactly-once` | The scope is stated in the same sentence. Almost every real system means "exactly-once for the database write" or "exactly-once workflow initiation" — not end-to-end. This word is load-bearing in the DBOS/Temporal debate; unscoped use is a factual error, not a style issue. |
| `guarantees` / `removes all` / `never fails` | A specification says so. See `voice.md` on absolute claims. |

Separate these states in prose and never let one stand in for another: **proposal → under discussion → accepted → merged → preview → released → adopted in production.** A JEP at Candidate is not a Java feature. A KIP under vote is not a Kafka capability.

## Pre-publish Verification Checklist

- [ ] Every candidate carries a freshness tag, and no `BACKGROUND_ONLY` item is presented as news.
- [ ] For any item where publication date differs from event date, the event date drove the freshness decision.
- [ ] No `first` / `largest` / `production-ready` / `exactly-once` without a direct source and stated scope.
- [ ] Proposal / accepted / merged / preview / released / in-production states are not conflated anywhere.
- [ ] All release dates verified against GitHub/blog sources.
- [ ] All metrics either sourced or softened with "reportedly"/"early adopters".
- [ ] Community Voice quotes attribute real articles/blogs, never fake Reddit threads.
- [ ] HN quotes in intro are removed from Community Voice.
- [ ] Reddit quotes either link to specific threads OR marked as "paraphrased" with source.
- [ ] Future roadmap dates use "unlikely before" or "post-YYYY" not exact dates.
- [ ] Technical integrations use "with X support" not "built entirely on X".
- [ ] KIPs/proposals checked for actual status (accepted vs proposed).
- [ ] Social media claims stripped of unverified metrics (views, dates).
- [ ] Company case studies have direct links to announcements.
- [ ] Event announcements moved to Scalendar, not In the Know.
