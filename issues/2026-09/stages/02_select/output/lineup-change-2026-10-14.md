# Lineup change, 2026-10-14 (after publish file was ready, before going live)

Approved by Piotr on 2026-10-14 after a second research sweep of engineering blogs, Kafka/data blogs
and the September HN landscape (the first pass had covered only HN for engagement and skipped the
"engineering blogs" secondary sources).

## Changes

| Slot | Before | After | Why |
|---|---|---|---|
| New main item (6th of max 6) | - | Follow-up from Issue #5: OpenAI agent swarms (swarmtraces.org 25 Sep, collusion.wiki 4 Sep, rubyhack.ai 11 Sep, OpenAI DNS report 20/25 Sep) | Highest-engagement infra story of September (HN 2,301 / 975 / 755). MATERIAL_UPDATE: events May-July, disclosed September; the copy says so. Corrects #5's "an agent" with the ~700 count the report cites from METR/Redwood. |
| Signal 1 | Kafka 4.4.0 slip | GitLab 24 Sep Postgres split-brain (production#23046/23047/23059/23064) | 4.4.0 passed its vote on 13 Oct, so the slip story lost its tension; Kafka was in two slots. GitLab fits the theme (failover = protective path) and has hard numbers. Incident and review are confidential; facts from public corrective-action issues only. |
| Signal Over Noise heading | Three Changes With a Migration Path | Three Defaults Worth Checking | Patroni watchdog default, JEP 471 deny-by-default, compact headers default. |
| In the Know | KIP-1279, JEP 544 | ZooKeeper CVE-2026-79993 (+ audit-log CVE-2026-84439), Kafka 4.4.0 one-liner with the Ericsson / "no committed release dates" sentence | Five-item cap. KIP-1279 and JEP 544 were status-only. |
| Today | Kafka 4.4.0 bullet | Agent swarm + GitLab bullets (8 total) | |
| Intro | three failures | five failures, same theme | |

## Considered and left out

- Effort.news "A single firm is behind..." (HN 694): advocacy piece with personal attacks, and it is about the Irregular-run evaluations, not the Hugging Face swarm. Not a usable "other side".
- GCP us-central1 1 Sep (technician unplugged all fibre paths in 13 minutes): no room under the In the Know cap. Candidate for a later issue.
- Uber retry storms (17 Sep, 2025 outage), Cloudflare 100 TB RAM, Azure OpenAI Sweden Central metastable loop, Aiven KRaft quorum loss, Netflix `ja`, Cloudflare Containers cross-tenant: good, lower priority.
- Salesforce 16 Sep: still no RCA (rootCause null on 14 Oct).
