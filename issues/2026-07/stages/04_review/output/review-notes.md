# Review notes — Issue #5 (July 2026)

Reviewed `03_draft/output/draft.md` against `voice.md`, `fact-check-rules.md` and
`newsletter-structure.md`. Output: `reviewed-draft.md`.

## Fact-check corrections

**1. Hacker News engagement was stale and understated.** The draft said 405 points
and 224 comments, taken from a secondary analysis written days earlier. Direct check
of the thread returns **468 points, 258 comments**. Corrected in both the Debate and
the References.

**2. One quote could not be verified and was cut.** The draft attributed a line about
"a lab swimming in more funding than any startup in history" failing to spot a large
egress signature. That phrasing appears in a secondary analysis but **not** in the
Hacker News thread on direct inspection. Removed rather than softened.

**3. Another quote was embellished and was replaced with plain statement.** The draft
rendered a comment as "closed model with disabled safeguards attacks, other closed
model with safeguards refuses to help defend, open model saves the day." Only the
opening fragment is verifiable on the page. The full three-part line is not, so the
quote is gone and the same point is now made in our own words, which the sourcing
fully supports.

**4. Two quotes confirmed verbatim, one corrected.** `cmiles8` reads "**This** mostly
reads like script kiddie style hacking, not some state actor black-ops stuff"
(capitalised, was lowercase in the draft). `llama052` is fuller than quoted and the
stronger version is now used: "I would argue that it's negligence and that's aside
from the fact that if a human did this there would actually be repercussions."

**5. Artifactory is back in, with provenance stated.** The draft deliberately said
"package registry cache proxy" because Hugging Face's timeline names no product and
OpenAI's disclosure returned HTTP 403. A comment on the thread quotes OpenAI's report
naming **Artifactory** directly. The reviewed draft now names it and says
"reportedly", because the primary source remains unreachable from here. This matters
editorially: Artifactory is a Java application, which turns the JVM connection from a
category argument into a specific one.

**6. The escalation chain is now sourced step by step, with harder numbers.** Every
link was verified against Hugging Face's timeline and several details were missing
from the draft: server-side template injection as the code-execution vector,
`curl -k https://kubernetes.default.svc/api`, **forged service-account tokens valid
for 24 hours**, a cluster secret object holding **136 keys**, and cluster-admin on
two clusters **within one second**. All added. Naming SSTI also strengthens the
Log4Shell and SpEL parallel, since it is literally the same class.

## Structure corrections

**7. In the Know exceeded the allowed range.** `newsletter-structure.md` specifies
3-5 items; the draft carried seven after the Debate rewrite displaced two stories
downward. Cut **Prefect/Dagster** (business consolidation with no technical stake and
no opposing camp) and **sbt 2.0.3** (point release, and the 2.0 GA itself was 29 June
rather than July). Five remain.

## Checks passed

- Section order matches the blueprint, all required sections present.
- Today: 7 bullets, inside the 6-8 range, every link on the bold text.
- Signals: exactly 3.
- Scalac angle present in both Debate and Trenches, both concrete and actionable.
- Date rule: no month or year phrase anywhere in the body. All occurrences are in the
  header and References, where they belong.
- Zero em-dashes and en-dashes.
- Zero throat-clearers, emphasis crutches, business jargon or banned adverbs.
- Links: 33 unique URLs, 30 return HTTP 200. Three return 403 to automated requests
  (`developers.redhat.com`, `dl.acm.org`, `www.scworld.com`). All three are bot
  blocks on live pages, not dead links, and each claim they support has a second
  working source: the QuePaxa paper also links open access at `bford.info`, and the
  guardrail story is also carried by SiliconANGLE at 200.

## Judgment calls, flagged rather than changed

**Valhalla appears in both Signal 1 and Community Voice.** The deduplication rule in
`newsletter-structure.md` bars a Debate or Trenches topic from reappearing elsewhere
but says nothing about Signals feeding Community Voice. Kept, because Vauban's angle
(value types as a representation for quantized model weights) is not covered in
Signal 1. Worth a decision if it reads repetitive to you.

**Two AI-adjacent lead sections in one issue,** and the third in a row touching agent
security after June's Meta story. Deliberate, since the two July items sit on
completely different axes: platform blast radius versus language design. Flagging it
so the pattern is a choice rather than a drift.

## Open items for publish stage

- `draft: true` still set in the frontmatter, and the cover image is referenced as
  `./cover.png` but not present in the issue folder.
- Publish date is a placeholder at `2026-08-04T09:00:00+02:00`.
