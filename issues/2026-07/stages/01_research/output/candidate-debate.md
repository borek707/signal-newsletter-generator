# Candidate Debate — July 2026

## Postgres-as-orchestrator vs. dedicated durable-execution platforms

**Topic:** Is Postgres-as-orchestrator (DBOS's "workflows are data, your database can manage them") a genuine alternative to dedicated durable-execution platforms like Temporal, or a v1 shortcut that hits the same coupling/scaling wall those platforms exist to avoid?

**Corroborated as a live July story** via [InfoQ Architects' Newsletter #108](https://assets.infoq.com/newsletter/architect/en/newsletter_sample/108Architects_NL_July-2026.html) featuring the DBOS "Compiling Workflows into Databases" presentation — this isn't a stale rehash, it's actively surfacing in July's editorial coverage.

### Side A — the pitch

[InfoQ: "Compiling Workflows into Databases: The Architecture That Shouldn't Work (But Does)"](https://www.infoq.com/presentations/dbos/) (Jeremy Edberg):
- Core mechanism: checkpoint workflow state directly into Postgres tables (`workflow_status`, `step_outputs`); `SKIP LOCKED` queries avoid lock contention across workers; exactly-once guarantee comes from writing the step's work and its checkpoint in the same transaction.
- Runs as a library, in-process — no separate orchestrator service or cluster to operate.
- Real adopter voice from a related HN thread: ["I evaluated Temporal, Trigger, Cloudflare Workflows... this was the easiest to implement incrementally. Didn't need to change our infrastructure at all."](https://news.ycombinator.com/item?id=44840693)

### Side B — the skepticism

- [dev.to: "Durable Workflows on Postgres: What 'You Don't Need Temporal' Actually Buys You"](https://dev.to/contrite42/durable-workflows-on-postgres-what-you-dont-need-temporal-actually-buys-you-3o0f) — grounded, non-hostile analysis: the exactly-once guarantee only covers the database write, not calls that reach past the database (a step that calls a third-party API and crashes after the call but before its checkpoint commits can still fire twice). At high throughput, workflow load competes with application load for the same Postgres connections and I/O.
- [BigGo: "DBOS Faces Developer Skepticism Over 'Exactly-Once' Processing Claims"](https://finance.biggo.com/news/202510030712_DBOS_Developer_Skepticism_Exactly_Once_Processing) — community pushback that the exactly-once claim applies to workflow *initiation*, not individual step execution; developers still must design idempotent steps themselves.
- Same HN thread, opposing adopter voice: "Temporal observability and UI was better than DBOS... [Conductor, DBOS's server equivalent] is not open source."

### Why it matters for CTOs

A real build-vs-adopt infrastructure decision with a concrete tell: does your workflow load scale independently of your application load? Not a framework religious war — the trade-off is legible and falls out cleanly from that one question.

### Scalac angle (first draft)

Modest workflow volume, already on Postgres, want fewer moving parts? DBOS-style database-backed checkpointing removes a whole service from your architecture diagram. Workflow load that genuinely scales independently of your app — high-fan-out jobs, pipelines with their own schedule — or need polyglot workers? Temporal's separation of orchestration from data store is what you're paying for. Either way: the exactly-once guarantee only covers the database write. Any step calling an external API still needs its own idempotency key, regardless of which system you pick.

### Market context worth one line in the write-up

The dedicated-orchestrator market is itself consolidating right now: **Prefect acquired Dagster** in July 2026 (two leading Airflow alternatives merging under one brand; Dagster's founders are leaving; community expects the usual post-acquisition price hikes and reduced OSS investment — [Dagster's own announcement](https://dagster.io/blog/prefect-is-acquiring-dagster)). Meanwhile Databricks shipped **LTAP** ("lakebase," derived from Neon's design), separating OLTP/OLAP while sharing storage specifically to eliminate CDC pipelines off transactional Postgres-compatible databases — the same "push more into the transactional-database layer" instinct as DBOS, just at lakehouse scale. Neither is the Debate itself, but both are good one-sentence evidence that the timing question ("why does this debate matter *now*") has real market backing on both sides.

### Backup candidate: leaderless consensus vs. Raft (Cloudflare Meerkat / QuePaxa)

Considered and **demoted to Signal Over Noise** — the production-readiness side of this debate is too thin (Cloudflare's Meerkat is proof-of-concept only, up to 50 replicas, not deployed) to carry a full two-sided Debate on its own. The real technical tension (see [HN thread](https://news.ycombinator.com/item?id=48831565)) is worth keeping — sharp, sourced skepticism exists ("this feels like manure," confusion over the Raft-vs-Paxos framing, a genuine long-tail-latency concern about the retry/abandon/retry pattern) — but it reads better as a fuller-than-usual Signal item than as the issue's main Debate.
