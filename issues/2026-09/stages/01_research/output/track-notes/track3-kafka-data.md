# SIGNAL #7 (September 2026), Track 3: Kafka and data systems

Researched 2026-10-07. Window: 1–30 Sep 2026, plus 1–7 Oct where it changes a September story.
Bottom line: September was busy for Kafka. The project shipped nothing new, but a lot changed. No 4.4.0 GA. One patch release (4.2.2), one KIP accepted (KIP-1279), a silent data-loss bug fixed, a public argument about the release schedule, and a compression supply-chain problem raised.

Primary-source method: I pulled the Apache dev@/users@ archive for kafka.apache.org (Sept: 520 messages) through the lists.apache.org API. I checked Jira REST for each KAFKA issue cited, GitHub (`gh api`) for tag and PR merge dates, and Confluence REST for KIP status.

---

## 1. Candidate register

### C1. A clean shutdown could delete recent data: Kafka's unsynced index truncation (KAFKA-20979 + KAFKA-21000)

- **Freshness:** MATERIAL_UPDATE. Issue filed 24 Aug. The fixes were merged in September, and the fix ships in 4.3.2 RC0 (cut 28 Sep) and in 4.4.0 RCs.
- **Event dates:** KAFKA-20979 created 2026-08-24, first fix on the 4.4 branch 2026-09-10 (commit beae700), second fix PR #23316 merged 2026-09-15, Jira resolved 2026-09-15. Sibling KAFKA-21000 created 2026-08-28, PR #23303 merged to trunk 2026-09-03 (fix version 4.5.0 only).
- **Source publication date:** Jira, 2026-08-24 / 2026-09-15.
- **Falsifiable claim:** On Kafka 4.1.0 (affects-version also lists 4.3.0), a broker restarting after a *clean* shutdown could read the zero-filled tail of a pre-allocated time index as `timestamp=0`. Time-based retention then deleted segments holding recent, valid records. Fix versions are 4.4.0 and 4.3.2.
- **Primary source:** https://issues.apache.org/jira/browse/KAFKA-20979 (Jira, reporter Mickael Maison, PMC member). PRs: https://github.com/apache/kafka/pull/23258 (via commit beae700), https://github.com/apache/kafka/pull/23316. Sibling: https://issues.apache.org/jira/browse/KAFKA-21000, https://github.com/apache/kafka/pull/23303.
- **Verification:** Jira REST fields (status, fixVersions, affects, comments) and GitHub PR `merged_at`, read directly. The mechanism is quoted from the reporter.
- **Hard evidence (verbatim from Jira):** "It's deleting many segments due to the retention limits. This has happened multiple times in the past few weeks." Log line: `Deleting segment LogSegment(baseOffset=83454, size=4483, ..., largestRecordTimestamp=0) due to log retention time 604800000ms breach`. Mechanism: "The flush() fsyncs the time index file at its pre-allocated size (10MB by default, zero-filled). The close() truncates the file ... which calls RandomAccessFile.setLength(), but never fsyncs the truncation." Luke Chen: "Given this issue will cause data loss for the impacted partitions, I think we should include this fix in v4.4.0." KAFKA-21000 is the same class of bug for `.log` files when preallocation is on (`trim()` without flushing length metadata). That causes an exception on restart, not deletion.
- **Trade-off:** fsyncing on every shutdown truncation makes shutdown slower, and that's the price of durability. Mitigation discussed in the thread: sanity-check indexes on startup. This is classic "metadata isn't durable until you fsync the directory/file", the same lesson as the 2018–2020 filesystem-durability papers.
- **Community reaction:** dev@/Jira only. 6 comments on KAFKA-20979, 33 review comments on PR #23316 (GitHub API). No HN or Reddit thread found. Sides: no disagreement that it's a bug. The discussion was about scope (whether to cherry-pick into 4.4.0; agreed by Chia-Ping Tsai, 2026-09-10).
- **Scores:** Freshness 4 / Relevance 5 / Evidence 5 / Stakes 5 / Tension 3 / Originality 5 = **27/30**
- **Suggested slot:** **Notes from the Trenches.** It has a real production observation by a PMC member, a root cause, a published fix, and an operator action: upgrade to 4.3.2 or 4.4.0, and until then check `largestRecordTimestamp=0` deletions in broker logs after restarts. Nobody in the newsletter space has covered it (Kafka-Nated had no Sept issue).

### C2. Kafka 4.4.0 slipped a month, and the project is redrawing its calendar

- **Freshness:** NEW_THIS_MONTH.
- **Event dates:** Code freeze 12 Aug. Release plan says "release no earlier than September 9 2026". RC0 tagged 2026-08-21, failed (blockers KAFKA-21025, KAFKA-19414 reopened, 2–4 Sep). RC1 tagged 2026-09-22, failed. RC3 tagged 2026-09-29, failed (David Jacot found an issue, 5 Oct). RC4 tagged 2026-10-06, vote open until **12 Oct 2026**. 4.5.0 schedule proposed 25 Sep (Andrew Schofield): KIP freeze 13 Jan 2027, target release 17 Mar 2027. Two +1s, Chia-Ping Tsai and Matthias Sax. Not formally fixed yet.
- **Source publication dates:** dev@ and users@ threads, 8–30 Sep 2026.
- **Falsifiable claim:** As of 2026-10-07, Apache Kafka 4.4.0 has not been released. Three release candidates (RC0, RC1, RC3) failed between 21 Aug and 5 Oct, and the RC4 vote closes 12 Oct.
- **Primary sources:** Release plan https://cwiki.apache.org/confluence/spaces/KAFKA/pages/429064575/Release+Plan+4.4.0 · RC4 vote https://lists.apache.org/thread/yy0gybz2y9b3ylylr5rsdxq4j0xmf222 · users@ "formal release date" thread https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf · dev@ "Tightening time-based releases" https://lists.apache.org/thread/o1d5p48t7br2bbh0rwl65rybd331pn7d (mailing lists, primary).
- **Hard evidence (verbatim):**
  - Ericsson engineers on users@ (8–9 Sep): "We have a release planned for the end of September and are planning to include this Kafka version with the vulnerability fixes in the release."
  - Matthias J. Sax (PMC): "As an open source project, we don't have committed release dates. The page literally says 'no earlier than'." Also: "At this point, I would think we need _at least_ two more weeks..."
  - Chia-Ping Tsai (PMC), 28 Sep: "have you considered packaging Kafka 4.3.2 or 4.2.2 instead if they are released before 4.4.0?"
  - Chia-Ping Tsai, 29 Sep: "We had too many must-have changes in 4.4.0, which caused a serious delay. ... The codebase is large and CVEs are common these days."
  - Dejan Stojadinović: maintainers are "juggl[ing] ... multiple release branches/versions (trunk/4.5.0, 4.4.0, 4.3.2, 4.2.2)."
  - A blocker from the RC cycle, KAFKA-20939 (Blocker, resolved 10 Sep): KIP-909 changed DNS-failure behaviour without opt-in. Producers built with an unresolvable bootstrap would previously throw `ConfigException` in the constructor. In 4.4.0 they throw a non-retriable `BootstrapResolutionException` from `send()`, leaving "a broken instance ... which needs to be discarded". The fix was PR #23364, "Disable async dns resolution in streams and connect", merged 9 Sep. Follow-ups KAFKA-21046/21047 make Streams and Connect "KIP-909 ready". **This is an upgrade-note item for 4.4.0 users.**
- **What 4.4.0 contains (from RC4 RELEASE_NOTES "New Feature"):** dead-letter queues for share groups (KAFKA-19469), share group offset initialisation from a specific offset or file (KAFKA-20524), broker-side custom assignors for "streams" groups (KAFKA-20683), KIP-1170 unified cluster-metadata bootstrapping, detection of misrouted connections. The RC mail says "26 KIPs".
- **Trade-off:** time-based releases versus "must-have" scope plus CVE backports across four live branches. Enterprises that plan a vulnerability-fix release around an OSS minor's target date carry that schedule risk themselves. Patch lines (4.2.2 released, 4.3.2 at RC) are the hedge.
- **Community reaction:** users@ thread with roughly 15 messages, 8–28 Sep, Ericsson asking and PMC members replying. dev@ thread with 6 messages in Sept. No HN thread.
- **Scores:** Freshness 5 / Relevance 5 / Evidence 5 / Stakes 4 / Tension 4 / Originality 4 = **27/30**
- **Suggested slot:** **Main Signal**, or Architecture/ops debate in the form "Don't plan your CVE remediation on an unreleased minor." It's concrete, sourced from primary documents, and useful to CTOs. If 4.4.0 GA lands before publication (vote closes 12 Oct), reframe: "4.4.0 shipped five weeks late; here's what to check (KIP-909 DNS behaviour, share-group DLQ)."

### C3. KIP-1279 Cluster Mirroring: proposal became accepted (vote passed 18 Sep)

- **Freshness:** MATERIAL_UPDATE. Issue #5/July covered KIP-1279 as a *proposal*. What changed in September: the vote opened 11 Sep and passed 18 Sep, and the wiki status is now "Accepted".
- **Event date:** vote passed 2026-09-18 (+3 binding: Mickael Maison, Andrew Schofield, Rajini Sivaram; +1 non-binding: Vaquar Khan). Red Hat article by co-author Federico Valeri published 2026-09-22.
- **Falsifiable claim:** KIP-1279 (broker-native cross-cluster replication that preserves offsets, intended to replace MirrorMaker 2 for DR and migration) was accepted on 18 Sep 2026. It is **not merged or released** in any version. 4.4.0 KIP freeze was 8 July, so it can't be in 4.4.0.
- **Primary source:** https://cwiki.apache.org/confluence/display/KAFKA/KIP-1279:+Cluster+Mirroring (KIP wiki, "Current state: Accepted", page last edited 2026-10-07) · vote result https://lists.apache.org/thread/15rddlqk42tqsjh5rw2r6so5cgns122f (dev@ message, Federico Valeri, 2026-09-18: "the vote for KIP-1279 has passed").
- **Secondary/position:** https://developers.redhat.com/articles/2026/09/22/data-liberation-apache-kafka-native-cluster-mirroring (Red Hat; the author is a KIP co-author, so this is advocacy). Direct fetch returned 403/404; the date and author were confirmed through HN item 49801700 and rmoff's September links.
- **Hard evidence (from KIP text):** the authors list Luke Chen, Federico Valeri, Omnia Ibrahim and Gaurav Narula. KIP-1279 is presented as a simplification of KIP-986. Destination partitions are read-only (`ReadOnlyTopicException`). Use-case guidance in the KIP itself: "MirrorMaker 2: Best for active-active topologies, multi-region writes ... Cluster Mirroring: Best for disaster recovery, failover, migration ... with exact offset preservation". Stated limits: active-active is "not initially supported". Tiered storage on the destination is unsupported during LOG_ALIGNMENT. Kafka Streams internal topics are not supported. Diskless topics are deferred to future KIPs. Migration claim: source brokers back to version 2.1 are supported for one-way migration, which the KIP presents as an alternative to multi-hop upgrades and ZK→KRaft migration.
- **Related:** KIP-1360 (synchronous mirroring, RPO=0) is still **DRAFT** (wiki edited 2026-06-25). Don't let the July framing ("Kafka wants to sell you RPO=0") imply progress on it.
- **Trade-off:** offsets are exact and no Connect cluster is needed, but you give up active-active and tiered-storage destinations at first. Mirroring now runs inside broker processes, so it shares broker resources and failure domains.
- **Community reaction:** HN 17 points / 4 comments on the Red Hat article (item 49801700, Algolia API). rmoff listed it in September links. No visible opposition on dev@; the vote was clean.
- **Scores:** Freshness 4 / Relevance 5 / Evidence 5 / Stakes 4 / Tension 2 / Originality 3 = **23/30**
- **Suggested slot:** **Today bullet** ("accepted, not shipped; earliest realistic target is 4.5, which is being pushed to ~Mar 2027"). Repeat coverage, so don't run it as a full section.
- **Reuse flag:** KIP-1279 is in issues/2026-07 (research, selection, draft, published). In the July published bullet the link text "Kafka proposes synchronous mirroring" points at KIP-1279 but describes KIP-1360. Avoid repeating that conflation.

### C4. Kafka's compression codecs depend on unmaintained or single-maintainer Java libraries

- **Freshness:** NEW_THIS_MONTH (dev@ post 29 Sep, Jira KAFKA-21178 created 29 Sep). Pushback on 5 Oct.
- **Event date:** 2026-09-29 (Luke Chen, PMC). KAFKA-21099 (CVE-2026-90559 snappy-java) filed 15 Sep.
- **Falsifiable claim:** Kafka maintainers say three snappy-java CVEs (CVE-2026-93452, -90559, -93451) can't be fixed with a version bump because upstream isn't responding. Kafka's LZ4 support already depends on a third-party fork (`yawkat/lz4-java`) maintained by one person. Removing codecs isn't an option because historical logs must stay readable, so the proposal is an admin config to disable selected codecs *on write* (KAFKA-21178).
- **Primary sources:** dev@ https://lists.apache.org/thread/6mlgc3b012hhq2v7gj08pzybltnrj7p8 · https://issues.apache.org/jira/browse/KAFKA-21178 · https://issues.apache.org/jira/browse/KAFKA-21099
- **Hard evidence (verbatim, Luke Chen):** "Unfortunately, the snappy-java community seems to be not maintained anymore. So we can't just bump the version to resolve them. I have an investigation (collaborate with AI), I think Kafka is not affected by these 2 CVEs, but not 100% sure about it." Also: "We cannot just find other compression methods and replace them because that means the historical log in kafka will not be decompressed anymore."
- **Counterpoint (verbatim, Martin Andersson, 2026-10-05):** "While xerial/snappy-java seems to be maintained, lz4-java is indeed a problem." So the snappy claim is disputed and the lz4 claim stands.
- **Trade-off:** a log format is a forever contract. Every codec you ever let producers use has to stay decodable for the retention lifetime, and for compacted topics that means indefinitely. Disabling a codec on write limits future exposure, but the decoder stays in your attack surface.
- **Community reaction:** dev@ only (2 messages so far). Jira picked up by Arnab Nandy on 4 Oct. Related users@ threads in Sept about dependency CVEs (jackson, jline, zstd-jni, jetty) show downstream pressure. No HN.
- **Scores:** Freshness 5 / Relevance 4 / Evidence 4 / Stakes 4 / Tension 4 / Originality 5 = **26/30**
- **Suggested slot:** **Signal (security/supply chain)** or a strong **Today bullet**. It fits next to C2 (CVE pressure is a cause of the 4.4.0 slip). Mark the snappy "unmaintained" claim as disputed. Don't state CVE severity, because I didn't verify NVD entries.

### C5. Postgres-as-Kafka vs leaving the database queue: two September posts arguing opposite directions

- **Freshness:** NEW_THIS_MONTH.
- **Event / publication dates:** Kafgres intro 2026-09-07. "700 MB/s of Kafka throughput, on Postgres" 2026-09-23 (rynr.dev, HN 2026-09-25). Tigris "We used a database as a message queue. Now we use Kafka" 2026-09-22 (HN 2026-09-30). bitdrift blob-stream 2026-09-28.
- **Falsifiable claims:**
  - (a) Kafgres, a Postgres extension embedding a singleton Kafka-protocol broker, reports ~700 MB/s produce (256 KiB records) and ~600k evt/s on a single Hetzner i9 with PLP NVMe. That was measured with `relaxed_produce_commit` and topic data written directly to disk, bypassing Postgres internals.
  - (b) Tigris moved event-triggered and S3-API jobs off a FoundationDB queue (Apple QuiCK) to Kafka because sustained inserts saturated FDB storage servers and triggered ratekeeper throttling. Deleting one tombstone cost six writes.
- **Primary sources:** https://rynr.dev/blog/700mbskafgres/ · https://rynr.dev/blog/kafgres/ · https://www.tigrisdata.com/blog/quick-fdb-kafka/ · https://blog.bitdrift.io/post/blob-stream-kafka-alternative (engineering blogs, first-party but self-reported).
- **Hard evidence / caveats in their own words:** Kafgres admits it can't "seamlessly shrug off a zonal outage in the way a 3-zone Kafka cluster can", and that "Non-transactional produce did not guarantee the actual topic data had been flushed to drive by the time it acked." Tigris accepted a second system and dual writes outside FDB transactions. Their failure mode: "a tombstone sticking around longer than it would otherwise, not user data falling into the shadow realm". They kept FDB for replication tasks. blob-stream reports a ~6M records/s, ~11 Gbps production cluster on 6 small brokers at ~2 s end-to-end latency, about $2,100/month, roughly 10x cheaper than their previous MSK. There's no per-key global ordering, no authn/authz, and only a Rust client.
- **Trade-off (the debate):** "one database" simplicity and transactional coupling (Kafgres) versus write amplification and blast radius once the queue outgrows the DB (Tigris). The third option, object-storage logs, trades latency for cost (blob-stream). The Kafgres 700 MB/s is a single-node, relaxed-durability number. Don't compare it with replicated, acks=all Kafka figures.
- **Community reaction (HN Algolia, verified):** Tigris 21 points / 1 comment (item 49913886). Kafgres 700 MB/s 4 points / 0 comments (49840594). Kafgres intro 5 / 0 (49850082). blob-stream 9 / 0 (49877947). Low engagement. I found no published rebuttal. The "SQLStreams" Reddit lead couldn't be located (web search empty, Reddit API blocked).
- **Scores:** Freshness 5 / Relevance 4 / Evidence 3 / Stakes 3 / Tension 5 / Originality 4 = **24/30**
- **Suggested slot:** **Architecture Debate** ("When does your database stop being a good queue?"). Use Tigris as the evidence-rich side. Present Kafgres as an experiment with explicit caveats, not a benchmark verdict.

### C6. KRaft quorum loss has no stock recovery path (Aiven, 29 Sep) + KRaft controller bugs filed in September

- **Freshness:** NEW_THIS_MONTH.
- **Event / publication dates:** Aiven post 2026-09-29 (Anton Agestam). KAFKA-21129 created 2026-09-20. KAFKA-21062 created 2026-09-10 (PR #23639 open on the 3.9 branch, 30 Sep).
- **Falsifiable claim:** On a dynamic KRaft quorum (KIP-853), losing a majority of controller voters leaves the cluster unable to commit metadata indefinitely, and upstream tooling has no supported recovery. Aiven says it built proprietary tooling for this; it isn't open source and there's no KIP.
- **Primary sources:** https://aiven.io/blog/kafka-never-lose-quorum (vendor blog = position) · https://issues.apache.org/jira/browse/KAFKA-21129 · https://issues.apache.org/jira/browse/KAFKA-21062
- **Hard evidence:** Aiven: "To demote the lost voters you must commit a membership change to the Raft log. To commit a membership change you need quorum. To have quorum you must remove the lost voters." Also: "We refuse to recover from any copy that would move surviving participants backwards in time." That means availability is restored, but data integrity isn't guaranteed. Aiven references KIP-1347 (`--override-voters`) as related but aimed at different failures. KAFKA-21129 (affects 4.3.1, open): an off-by-one in `QuorumController.appendRecords` sends an empty batch when the record count is an exact multiple of `maxRecordsPerBatch`, "so the active controller renounces leadership". KAFKA-21062 (affects 3.9.2): a lost ZooKeeper ack on the `/migration` write can permanently stall a ZK→KRaft migration in DUAL_WRITE and let the two diverge.
- **Trade-off:** Raft safety (refuse unsafe membership changes) versus operability after correlated failures. Recovery means you accept that you lose the most recent metadata.
- **Community reaction:** no HN found (search "KRaft" returned noise). The Reddit post was reported by the coordinator but I couldn't verify it (Reddit blocked).
- **Scores:** Freshness 5 / Relevance 4 / Evidence 3 / Stakes 4 / Tension 3 / Originality 4 = **23/30**
- **Suggested slot:** **Today bullet**, or a secondary Trenches note ("controller placement across AZs is now a data-integrity decision"). Label it as a vendor post. I didn't verify that KIP-1347 exists or its state (see open questions).

### C7. "Streamhouse": five streaming vendors define a category (15 Sep)

- **Freshness:** NEW_THIS_MONTH (announced 2026-09-15).
- **Claim:** Aiven, Confluent, Redpanda, StreamNative and Ververica formed a working group and published a "vendor-neutral" Streamhouse definition with a trademark commitment. The GitHub spec repo is marked "coming soon" on streamhouse.com.
- **Sources:** https://streamhouse.com/ · https://aiven.io/press/aiven-others-form-streamhouse-working-group · critique: https://www.conduktor.io/blog/streamhouse-what-it-is-what-it-isnt-whats-missing (Stéphane Derosiaux, 2026-09-21; Conduktor is also a vendor).
- **Tension:** Conduktor says it lacks technical primitives and guarantees, unlike Lakehouse, and treats governance as one pipeline step.
- **Scores:** Freshness 5 / Relevance 3 / Evidence 3 / Stakes 2 / Tension 3 / Originality 2 = **18/30**
- **Suggested slot:** an optional **Today bullet** with skeptical framing (a marketing category, no spec yet). Low priority.

### C8. Adjacent releases (bullet material)

| Project | Version | Date | Source |
|---|---|---|---|
| Apache Kafka | 4.2.2 (bug-fix) | announced 2026-09-29 | dev@ [ANNOUNCE], Apoorv Mittal |
| Apache Kafka | 4.3.2 RC0 | tagged 2026-09-28, vote ongoing in Oct | GitHub tag, dev@ |
| Apache Kafka | 4.4.0 RC1 / RC3 / RC4 | 2026-09-22 / 2026-09-29 / 2026-10-06 | GitHub tags |
| Apache Iceberg | 1.12.0 | GitHub release 2026-09-30 | github.com/apache/iceberg/releases |
| Apache Fluss | 1.0.0 | 2026-09-22 | github.com/apache/fluss/releases |
| Flink Kubernetes Operator | 1.16.0 | 2026-09-15 | flink.apache.org/posts |
| Apache Pulsar | 5.0.0-M2 (2026-09-16), 5.0.0 GA (2026-10-05) | GitHub releases | October GA is outside the window |
| AutoMQ | 1.7.5-rc0 / rc1 | 2026-09-02 / 09-24 | GitHub |
| Apache Flink (core) | none in Sept; 2.3.0 was 2026-06-25 | flink.apache.org | BACKGROUND |

Current 2026 (Confluent) is 4–5 Nov 2026, Moscone West, SF (web search, plus rmoff confirms "November ... San Francisco"). There were no Current announcements in September.

---

## 2. What did Kafka ship in September 2026?

- **Released:** **Apache Kafka 4.2.2** (bug-fix), [ANNOUNCE] on dev@ 2026-09-29. That's the only Apache Kafka GA release in September. downloads.apache.org/kafka/ lists 4.1.2, 4.2.1, 4.2.2, 4.3.1.
- **Not released:** **4.4.0.** Planned "no earlier than 9 Sep". RC0 (21 Aug) failed, RC1 (22 Sep) failed, RC3 (29 Sep) failed. RC4 (6 Oct) vote closes 12 Oct.
- **In flight:** **4.3.2 RC0** (tagged 28 Sep). It contains the KAFKA-20979 data-loss fix and the KAFKA-20416 fix.
- **KIP state changes in Sept (dev@ evidence):** **KIP-1279 Cluster Mirroring: ACCEPTED** (vote passed 18 Sep). Votes opened in Sept (outcome not verified): KIP-1097 (Connect exception handler), KIP-1262 (auto-formatting directories), KIP-1357 (broker-side custom assignors for streams groups; implementation already in 4.4.0 RC notes as KAFKA-20683), KIP-1349 (share-group snapshot frequency, still voting on 5 Oct), KIP-1368 (client framework name/version). New DISCUSS threads: KIP-1371, 1373, 1374, 1375, 1377, 1378 (MM2 consumer-group renaming).
- **Diskless:** no state change in September. KIP-1150 Diskless Topics has been Accepted since before March. KIP-1163 Diskless Core is still "Under Discussion". The KIP-1165 rename to "Object Consolidation" was posted on 5 Oct (outside window). Aiven ran a Diskless Topics webinar on 21 Sep (users@ post), which is vendor marketing.
- **Kafka-own CVEs:** I didn't find any new Kafka CVE announcement in September. The announce@ list API returned no September messages, and the kafka.apache.org/cve-list page is JS-rendered, so I couldn't parse it (see failures). September CVE activity was in dependencies: snappy-java (3 CVEs), jline CVE-2026-56740 (KAFKA-21020), jackson-databind CVE-2026-68497 (KAFKA-21004), and KAFKA-21032 asking for a kafka-clients update for CVE-2026-59949 (resolved the same day; nature not checked). CVE-2026-33557 and CVE-2026-35554 are April items, BACKGROUND_ONLY. Nothing new happened on them in September as far as I could see.

---

## 3. Rejected items

| Item | Why rejected |
|---|---|
| "Northguard and Xinfra: What LinkedIn Changed When Kafka Was No Longer Enough" | It's a **SoftwareMill** post (softwaremill.com/linkedin-northguard-xinfra-kafka/), **COMPETITOR**. LinkedIn's own Northguard announcement is June 2025, so BACKGROUND_ONLY. I found no new LinkedIn engineering post in Sept 2026. |
| SoftwareMill "Diskless Kafka … KIP-1150", "Kafka vs Apache Iggy", "Log-first or Table-first? Kafka, Fluss" (Sept) | COMPETITOR. Never feature. |
| WarpStream "Orbit" automatic migrations | Published 2026-08-18, outside window, vendor. |
| Confluent Rust client announcement | ~6 Oct, outside window; low priority per coordinator. |
| Red Hat "Why your Kafka topic ignores retention.ms" (2026-09-16) | Correct but evergreen explainer (active segment never rolls; set `segment.ms` < `retention.ms`). No new fact. Possible tip-box filler only. |
| Razorpay "Five Years of Kafka at UPI Switch" | Fetch returned 403. Couldn't verify date or content. Might be a Trenches backup if someone can read it. |
| Booking.com "Automated Capacity Testing for Kafka Consumers" (HN 2026-09-14, 3 pts) | Not fetched or verified. Low engagement. Backup only. |
| "Anatomy of a Kafka Lock Convoy" (alex.bularca.me, HN 2026-09-12) | Not fetched. Low engagement (3 pts). Worth a look as a Trenches backup. |
| KAFKA-20416 "RocksDB loses entries during broker patches" (Critical, resolved 25 Sep, fix 4.3.2/4.4.0/4.5.0) | The comment thread (to 5 Oct) shows confusion. One reporter admits a config was set twice ("Yea that was my bad"), and another case involved a custom store. Root cause is too murky to feature. |
| KAFKA-20547 Streams EOS_v2 duplicates | Closed as Duplicate (11 Sep) of KAFKA-17754. Nothing new. |
| Diskless KIP-1163/1165 | Only an October update; no September state change. |
| Flink 2.3 | Released June 2026. |
| Kafka CVE-2026-33557 / -35554 | April 2026, BACKGROUND_ONLY. No new activity found. |
| Netflix service topology / Kafka backpressure | Already Issue #6 (Aug). Reuse. |
| Confluent Q3 cloud launch | Already in Issue #6 (Aug). |

Reuse grep (`~/Documents/signal-newsletter-generator/issues/`): KIP-1279/"cluster mirroring" are in 2026-07. "diskless" is in 2026-03 and 2026-07. "share group" is in 03/04/05/07. These have zero prior hits: snappy, lz4, KIP-909, fsync, "time index", iceberg, Redpanda, AutoMQ, mirrormaker. WarpStream is in 2026-03.

---

## 4. Open fact-check questions

1. Did 4.4.0 RC4 pass, and what is the GA date? Vote closes 12 Oct. Re-check https://lists.apache.org/list.html?dev@kafka.apache.org before drafting.
2. 4.5.0 revised schedule (KIP freeze 13 Jan 2027, release 17 Mar 2027): was it formally adopted on the wiki, or is it still a proposal with +1s?
3. KAFKA-20979: does 4.2.2 (released 29 Sep) include the fix? The Jira fix versions list only 4.4.0 and 4.3.2. If not, 4.2.x users stay exposed until a 4.2.3. Check the 4.2.2 release notes.
4. Which RC numbers failed and why: RC2 has no GitHub tag (the 422 error suggests it was skipped). Confirm what David Jacot found in RC3 (owbhl5yl… thread).
5. snappy-java maintenance status: Luke Chen says unmaintained, Martin Andersson says maintained. Check the github.com/xerial/snappy-java commit and release history, and NVD severity for CVE-2026-93452/90559/93451.
6. The Kafgres author's name ("Ray Elg" according to the WebFetch summary) is unconfirmed, as are the licence and repo URL. Confirm on rynr.dev and GitHub.
7. KIP-1347 (`--override-voters`), cited by Aiven: verify it exists and its status on cwiki.
8. The Red Hat KIP-1279 article returned 404/403 to direct fetches. Confirm the exact URL slug (rmoff links `...native-cluster-mirroring`; HN links `...native-cluster-mirror`).
9. Kafka's official CVE list: did it gain any 2026-08/09 entries? (The JS-rendered page couldn't be read; try a browser.)
10. Votes opened in Sept on KIP-1097, KIP-1262, KIP-1357 and KIP-1368: did any pass by 30 Sep? I didn't check the outcomes.

---

## 5. URLs fetched: OK vs failed

**OK**
- GitHub API via `gh`: apache/kafka tags and commit dates (4.4.0-rc0/rc1/rc3/rc4, 4.3.2-rc0, 4.3.1, 4.3.0); PRs #23316, #23303, #23364, #23639; commit beae700; releases for apache/iceberg, apache/pulsar, apache/fluss, AutoMQ/automq (apache/flink and redpanda returned none in window)
- https://lists.apache.org/api/stats.lua?list=dev&domain=kafka.apache.org&d=2026-09 (520 msgs) and d=2026-10; users@ 2026-09; plus about 30 individual email.lua fetches
- Jira REST: KAFKA-20939, 21000, 20979, 21062, 20547, 20416, 21158, 21178, 21129
- Confluence REST: KIP-1279 (full text), KIP-1360, KIP-1163, KIP-1150; Release Plan 4.4.0 (page 429064575)
- https://dist.apache.org/repos/dist/dev/kafka/4.4.0-rc4/RELEASE_NOTES.html
- https://downloads.apache.org/kafka/
- https://flink.apache.org/posts/
- https://hn.algolia.com/api/v1/search_by_date (several queries)
- https://rmoff.net/2026/09/29/interesting-links-september-2026/ (discovery index)
- https://www.tigrisdata.com/blog/quick-fdb-kafka/
- https://rynr.dev/blog/700mbskafgres/ , https://rynr.dev/blog/kafgres/
- https://blog.bitdrift.io/post/blob-stream-kafka-alternative
- https://aiven.io/blog/kafka-never-lose-quorum
- https://developers.redhat.com/articles/2026/09/16/why-your-kafka-topic-ignores-retentionms-and-how-fix-it (via WebFetch)
- https://streamhouse.com/ ; https://www.conduktor.io/blog/streamhouse-what-it-is-what-it-isnt-whats-missing
- Web searches: Northguard, Current 2026, Streamhouse, KRaft quorum, Red Hat digest

**Failed / partial**
- https://developers.redhat.com/articles/2026/09/22/data-liberation-apache-kafka-native-cluster-mirror (404) and `...-mirroring` (403 via curl)
- Red Hat "Kafka Monthly Digest September 2026": every guessed URL returned 403. Search shows the August digest (published 1 Sep) but no September one.
- https://kafka.apache.org/cve-list/ (JS-rendered; WebFetch refused, curl got no CVE IDs)
- https://kafka.apache.org/blog: dates only (Sept 29 entry = 4.2.2)
- https://www.reddit.com/r/apachekafka/new.json (blocked, non-JSON response). Reddit leads are unverified.
- https://engineering.razorpay.com/tryst-with-kafka-2f5cef766c45 (403)
- "SQLStreams": not found in web search
- api.github.com unauthenticated (rate-limited; switched to `gh`)
- announce@kafka.apache.org stats for 2026-09 returned no messages (couldn't tell whether that's empty or an API quirk)
