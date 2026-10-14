# SIGNAL Newsletter Structure

SIGNAL is a monthly B2B newsletter for CTO, VP of Engineering, and Chief Architect roles running distributed systems at scale.

**Philosophy:** Don't aggregate news. Aggregate lessons.

## Issue Blueprint

Every issue has the following sections in this order:

### 1. Header

```markdown
# SIGNAL: What matters in distributed systems

**[Month] [Year] | Issue #[N]**
```

### 2. Intro

- **Issue #1:** `Welcome to SIGNAL.` + 4-5 sentences explaining the newsletter + `Also:` with 2 teaser bullets.
- **Issues #2+:** `Welcome back.` + 2-3 sentences. Hook with the most surprising/debated insight. No throat-clearing.

Rules:
- Narrative, not a list.
- No dates repeated from the header.
- Mention 2-3 biggest stories of the month.

### 3. Today

6-8 one-line bullets. Every bullet is linked on the bold text. This is the table of contents.

Format:
```markdown
- **[Oracle proposes JVMCI deprecation.](https://link)** The JVM Compiler Interface is marked for removal.
```

### 4. The Architecture Debate

One hot topic with genuine controversy. Two sides with evidence. Technical + business implications.

Structure:
- 3-4 bold hooks, every claim linked.
- Give each side its honest best argument, plus the condition under which that side is right.
- End with **Scalac angle**: 2-3 sentences, concrete recommendations, challenge both sides.

**Do not construct a Debate when only one side has substance.** If the research turned up one credible position and some grumbling, that is a Signal or a Trenches story, not a Debate. Two failure modes to check for: a genuine controversy that turns out to be settled once you read the primary sources, and a business event that reads dramatic but has no technical disagreement in it (July 2026: the Prefect/Dagster acquisition looked like a Debate, then verification showed a well-received consolidation with no opposing technical camp, so it was demoted to one context sentence inside another Debate).

### 5. Notes from the Trenches

One concrete production problem with specific symptoms, errors, metrics. Solution with code/commands if applicable. Transferable lesson.

Structure:
- Bold hook: The Problem.
- Bold hook: The Solution.
- End with **Scalac angle**: what to do in production.

### 6. Signal Over Noise

Exactly 3 critical changes. Each: what changed + why it matters + migration path.

Focus:
- Breaking changes
- Deprecations
- Major shifts

Skip:
- Minor features
- Patch releases
- Betas
- Opinion essays without hard data

### 7. Community Voice (optional)

Synthesis from real articles/blogs. Never fake Reddit/HN quotes. Attribute every quote: `[Source](link) synthesizes: "quote"`.

Deduplication rule: if a topic appears in Debate or Trenches, it does NOT appear in Community Voice.

### 8. In the Know

3-5 short items. NO duplicates with Debate/Trenches. NO events (Devoxx, JavaOne → Scalendar).

Format:
```markdown
**[Name](link)** -- One sentence description.
```

### 9. Top Resources

Three items:
- **Repo to watch:** link + one sentence why.
- **Article to read:** link + one sentence why.
- **Paper to read:** link + one sentence why.

### 10. Footer

SIGNAL is published on the scalac.io blog only. **It is not emailed**, so never write "reply to this email" or anything else that assumes an inbox. Story submissions go to the contact page.

Fixed block (matches the live issues #6 and #7):
```markdown
**What is SIGNAL?** A monthly, opinionated newsletter for JVM and Scala teams who run real distributed systems. Each issue has three sections: Architecture Debate, Notes from the Trenches, Signal Over Noise, and focuses only on changes and incidents that matter in production, not on hype or vendor marketing.

Scalac builds high-throughput systems in Scala, Java, and Rust; SIGNAL is the filter we wish we had when making our own architecture bets.

**Got a story for SIGNAL?** [Send it our way.](https://scalac.io/contact-us/) We read every submission.
```

### 11. References

List every source used. One bullet per source with title and URL.

---

## Claim Boundary (required content in every main item)

Every Debate, Trenches, and Signal item has to make clear what is **not** yet established: what is still experimental, proof-of-concept, preview, single-sourced, or true only under stated conditions.

This is a content requirement, not a labelled field. Write it into the prose in SIGNAL's voice, never as a `Claim boundary:` heading.

- Weak: "Cloudflare's Meerkat replaces Raft with leaderless consensus."
- Correct: "Meerkat is not in production. Cloudflare has run proofs of concept with up to 50 replicas."

The reason this is structural rather than a review-time fix: without it, every item reads like a capability announcement, which is exactly the register `voice.md` and `fact-check-rules.md` exist to avoid. It also gives the reader the one thing a vendor blog never will, which is the honest edge of the claim.

## Issue Size

Maximum six main items. Fewer strong signals beats a padded issue.

Do not fill a section because the template lists it. Community Voice is already optional; Top Resources may ship with two entries instead of three, or be dropped entirely, if no candidate survives verification. A short issue with three well-evidenced stories is a better product than seven patch releases dressed as news, and it protects the newsletter's core promise of being a filter rather than a firehose.

## Section Selection Criteria

| Section | Must be | Must not be |
|---------|---------|-------------|
| Debate | Real controversy, both sides valid, technical + business | Manufactured conflict, one-sided rant |
| Trenches | Concrete error/metric, production context, actionable fix | Tutorial without incident, hypothetical scenario |
| Signals | Breaking change/deprecation/major shift with migration path | Minor release, beta, opinion without data |
| In the Know | Short, sourced, non-duplicate | Event announcement, duplicate story |
| Top Resources | Direct repo/paper/tool link | Generic recommendation without URL |
