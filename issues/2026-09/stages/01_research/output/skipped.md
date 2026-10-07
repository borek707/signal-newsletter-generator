# Skipped Sources and Rejected Signals — September 2026

## Leads from the brief that did not survive research

| Lead | What research found |
|---|---|
| Odersky "Tracked Capabilities for Safer Agents" as Debate | Published 27 Jul → BACKGROUND_ONLY. TACIT repo quiet since August. No credible September voice opposes it; Matthew Green (30 Sep) and Trail of Bits (26 Aug) argue runtime sandboxes fail, which supports Odersky's diagnosis rather than opposing it. |
| Arrays.fill 265× slower on G1 as Trenches | Published 19 Aug. Measured on JDK 25; JDK 26 (JEP 522) removes the fence. Teams newly on G1 via JDK 27 don't hit it. JDK 25 LTS warning only. |
| "JDK 27 RC came two weeks late because of a bug" | False. `jdk-27+35` (= GA) tagged 19 Aug, on schedule. The real event: a P1 C2 corruption bug (JDK-8390546) backed out the day before the RC. |
| JEP 528 dropped from JDK 27 in September | Dropped 21 May. In September it was retargeted to JDK 28 (29 Sep). |
| JobRunr v9 "durable steps" | `runStepOnce` shipped in v8 (2025). v9 adds a Gantt view of steps. |
| LangChain4j DecisionModel in 1.20.0; PR #6469 "16 files, +1,293" | Shipped in 1.21.0 (2 Oct). Final PR: 54 files, +5,832. |
| Jev "invite-only", "official SDKs" | Waitlist. JVM SDKs are community projects. |
| Scala.js 1.22 stable Wasm as September news | Released 20 Jun. |
| "JDK 26 throws on Unsafe by default" (secondary sources) | Not shipped in 26 or 27; JEP 471 phase 3 has no JDK named. |
| Spring AI "next major" milestone (InfoQ wording) | 2.1.0-M1 is a minor milestone. |

## Rejected — competitor

| Item | Competitor |
|---|---|
| Sloth (bytecode rewriter for old lazy vals), tulip, VirtusLab Scala Stack, Besom, Scala/WASM post | VirtusLab |
| tanishiking capture/separation checking intro (virtuslab.com, May) | VirtusLab |
| "VirtusLab assumes responsibility for Scala 2 maintenance" (7 Oct) — touches the scala-reflect story | VirtusLab — flag to editor, don't feature |
| "Northguard and Xinfra: What LinkedIn Changed When Kafka Was No Longer Enough" | SoftwareMill (and LinkedIn's original is June 2025) |
| SoftwareMill diskless KIP-1150, Kafka vs Apache Iggy, Fluss posts | SoftwareMill |
| Typelevel Traverses Europe | Typelevel |

## Rejected — stale (BACKGROUND_ONLY)

- Netflix "Conductor: The Next Chapter" (21 Aug); Conductor was in #5.
- DoorDash agent gateway (30 Jul) behind ByteByteGo's 30 Sep rewrite.
- ByteByteGo "AI Agents Can Think. Now They Can Pay." — MPP only (launched March).
- Kafka CVE-2026-33557 / CVE-2026-35554 (April); no new Kafka CVE found in September.
- WarpStream Orbit (18 Aug).
- Antithesis "Finding bugs in Raft implementations" (27 Jul).
- TigerBeetle protocol-aware DST (20 Aug).
- Jepsen: no new analysis since MariaDB Galera (16 Mar).
- Flink 2.3 (June). No Flink core release in September.

## Rejected — weak or missing primary source

- ChatGPT / Claude / Grok outages on 3 Sep (HN 404 / 705): no shared cause published.
- GitLab.com outage 24 Sep: no public incident review found.
- Salesforce 16 Sep (legacy login server, 7.5 h): status timeline only, no RCA as of 7 Oct. Upgrade if an RCA appears.
- Pragmatic Engineer "Inside OpenAI's agentic software factory": no OpenAI primary sources linked.
- PE "What is happening with code reviews?": off-track, numbers inside a paywall.
- OpenAI Decisions API pricing: one community post.
- Phoronix JDK 8–27 benchmarks: not fetched.
- Razorpay "Five Years of Kafka at UPI Switch": 403.
- "SQLStreams — Kafka on Postgres" (r/apachekafka): couldn't be found.
- KAFKA-20416 RocksDB entries lost during patches: comment thread shows misconfiguration in at least one case; root cause too murky.
- TypeSafe "$1B round": Spanish-language aggregator only.

## Rejected — low stakes, overlap, or wrong format

- Kafgres / Postgres-as-Kafka as Debate: low engagement, no rebuttal, echoes #5's DBOS debate → Top Resources (Tigris).
- MCP obsolete-vs-governed: MCP in ~20 past issue files → one line at most.
- Streamhouse vendor working group (15 Sep): marketing category, no spec.
- Cockroach Continuum (15 Sep): product preview, vendor numbers.
- Temporal $550M raise: funding news; Standalone Activities GA is the only engineering hook.
- Kotlin 2.4.20, Ktor 3.6, Gradle 9.8, Kyo RC7: routine churn.
- Pre-SIP `T ? E`: real argument, but stakes are years out → In the Know at most.
- ZGC JEPs 545/546 (Candidate): status only.
- Telstra NTP (outage July, report 2 Sep): strong concept, weak freshness → In the Know.
- Hillel Wayne TLA+ (30 Sep): partial overlap with July's link → Top Resources.
- GTIG DUSTMAKER (8 Sep): coding-agent config injection, HN 13 → Today bullet if space.
- Liquid network / BTC peg-out RCA: gist 404, off-audience.

## Sources not covered

- **X / Twitter:** agent-reach has no credentials this session (`agent-reach configure twitter-cookies` needed).
- **LinkedIn:** not attempted.
- **Reddit:** API blocked; only titles via `/last30days` and one thread via opencli.
- **InfoQ Software Architects' Newsletter:** only the landing page's October items; the September issue itself was not read.
- **Red Hat Kafka Monthly Digest (September):** every URL 403.
- **mail.openjdk.org:** not attempted (known 403); GitHub and JBS used instead.
