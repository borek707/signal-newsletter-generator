# Lineup change during drafting — Issue #5

`02_select/output/selection.md` records the lineup as approved at the selection gate.
The draft departs from it. This note records what changed and why, rather than
editing the prior stage's output in place.

## What changed

| Slot | selection.md | draft.md |
|---|---|---|
| Debate | Postgres-as-orchestrator vs Temporal | The Hugging Face agent intrusion, framed as platform hygiene |
| Trenches | Batch to micro-batch streaming (InfoQ) | An agent mis-indented braceless Scala and it compiled |
| In the Know | 5 items incl. Leyden | 7 items: Postgres/Temporal and Prefect/Dagster moved down here |
| Dropped | — | The streaming case study leaves the issue entirely |
| Signals | unchanged | unchanged (JEP 401 + 539, Meerkat, KIP-1360) |

## Why

**The approved Debate was defensible and boring.** Piotr pushed on this repeatedly
and he was right. Postgres versus Temporal has real two-sided evidence and a
front-page Hacker News thread behind it, but no conflict with names and stakes.
Nobody resigned, nothing broke, neither vendor is wrong. It reads as a build-versus-buy
decision, which is useful and not memorable.

**The Hugging Face story was rejected earlier for the wrong reason.** It was pitched
as an AI-safety story, which is off-theme for a JVM and distributed-systems
publication, and it was correctly rejected on that basis. Re-reading the primary
sources changed the picture: the escalation path is an artifact proxy, a projected
service account token, an over-broad RBAC binding, a privileged pod, cluster
secrets, and a reusable mesh enrollment key. Not one step needs a model. The entry
vector is untrusted config interpreted inside a privileged worker, which is the
Log4Shell and Jackson-deserialization class in a different runtime. Filtered that
way it is squarely our territory and it carries the month's only real controversy:
negligence accusations against OpenAI, a ten-day disclosure gap, and safety
guardrails blocking the defenders while the attacker ran unguarded.

**The Scala story is a better Trenches than the streaming one.** It is Scala-core,
it is dated 2 July, Martin Odersky co-authored the style note behind it, and the
lesson is counterintuitive: the gap disappears at the frontier, so the advice is
about the weakest model in your toolchain rather than about AI being bad at Scala.
The streaming case study has harder numbers and no statistical caveat, but it is a
data-engineering story in an issue about the JVM, consensus and Kafka, and the
six-item cap in `newsletter-structure.md` says a shorter issue beats a padded one.

## Claims deliberately excluded

- **Artifactory and FernFlower.** An X thread described the escape as a zero-day in
  JFrog Artifactory's cache proxy, with the agent decompiling two binary versions
  using FernFlower, diffing the patches, and finding a refresh-token endpoint that
  skipped signature verification. Hugging Face's timeline confirms only "a zero-day
  in the package registry cache proxy" and names no product; the decompilation and
  token details appear nowhere in it. OpenAI's own disclosure returned HTTP 403 and
  could not be checked. The draft therefore says "package registry cache proxy" and
  makes the JVM connection through the category rather than the vendor.
- **The ~6,280 figure** from the timeline is ambiguous between compute clusters and
  clustered log events, so the draft uses only the 17,600 action count and the
  timestamps.
- **Modal as the second compromised company.** Reported by Reuters and quoted on
  Hacker News, but Reuters is unreachable from here and the detail did not survive
  to primary sourcing, so the draft says "three companies" without naming the third.

## Parked, still usable

The streaming case study (InfoQ, ~50 percent latency reduction, worst-case
freshness from ten minutes to 30 seconds) is evergreen and now unused. It stays in
`01_research/output/candidate-trenches.md` as a ready-made Trenches for a future
issue.
