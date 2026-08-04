# Today — SIGNAL July 2026 (Issue #5)

Seven bullets. Link sits on the bold text, per `voice.md`. Each is one line, no second sentence.

- **[Value objects land in OpenJDK mainline.](https://github.com/openjdk/jdk/pull/31120)** A decade of Project Valhalla, ~197K lines of code, preview in JDK 28.
- **[Strict field initialization gets targeted for JDK 28.](https://openjdk.org/jeps/539)** Fields must be written before they are read, so default `0` and `null` stop being observable.
- **[Cloudflare builds consensus without timeouts.](https://blog.cloudflare.com/meerkat-introduction/)** Meerkat runs on QuePaxa, where any replica can drive consensus and no leader is required.
- **[Kafka proposes synchronous mirroring.](https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring)** KIP-1360 offers RPO=0 across clusters and charges for it in write latency.
- **[Postgres wants your workflow engine's job.](https://www.infoq.com/presentations/dbos/)** DBOS argues the database is the orchestrator; practitioners disagree about where that breaks.
- **[Prefect acquires Dagster.](https://dagster.io/blog/prefect-is-acquiring-dagster)** The two leading Airflow alternatives consolidate under one owner.
- **[A pipeline that was late, not slow.](https://www.infoq.com/articles/micro-batch-streaming-lessons-learned/)** Worst-case freshness went from ~10 minutes to 30 seconds by changing the trigger, not the semantics.

## Notes for the draft stage

- No em-dashes anywhere. Hyphens or periods.
- Every bullet above is `NEW_THIS_MONTH` or `MATERIAL_UPDATE`. Nothing here is `BACKGROUND_ONLY`.
- KIP-1360 must read as a proposal in the body too, never as a Kafka capability.
- The Meerkat bullet is deliberately phrased as what Cloudflare is building, not what it runs. It is not in production.
