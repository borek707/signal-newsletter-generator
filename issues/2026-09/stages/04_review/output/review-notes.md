# Review notes — Issue #7 (September 2026)

Reviewed `03_draft/output/draft.md` against primary sources, `voice.md`, `fact-check-rules.md` and `newsletter-structure.md`. Output: `reviewed-draft.md`. Everything is true as of 2026-10-07.

## Fact-check: corrections made

Every quote and number in the issue was re-read at source in this stage or in `03_draft` (Jira/JBS REST APIs, lists.apache.org API, GitHub API, PDFs, arXiv HTML). Corrections that changed the text:

| Where | Draft said | Source says | Fix |
|---|---|---|---|
| Signal 3 | Kozlov argues against Shipilev | Kozlov: realigning crypto intrinsics "may cause more regression than improvement. -1%..-4% seems more acceptable" — he accepts the cost | Rewritten: both engineers lean toward accepting part of the cost (fixed in 03) |
| Signal 1 | One Tsai quote spliced from two sentences with "…" | Two separate sentences in one email | Two verbatim quotes (fixed in 03) |
| Debate | HN "apples-to-oranges" from a named commenter | Not found in the thread via Algolia | Replaced with a verified comment ("misleading because they make people believe they're as general purpose as LLMs") |
| Trenches | Scalac angle: "restart cleanly, confirm retention didn't fire" | Loss needs the restart to beat the OS metadata flush; a quick process restart won't reproduce it | Recommend the `grep` after restarts, with extra attention where host or volume goes down |
| Intro, Today | Firebase crashed iOS apps "everywhere at once" | Google: "released to a wide population of apps" | "a wide population of iOS apps at once" |
| Signal 1 | Codec CVEs as Kafka exposure | Luke Chen: "I think Kafka is not affected … but not 100% sure" | Added his own caveat |
| Signal 1 | KIP-909 DNS behaviour as an upgrade note | PR #23364: async mode enabled by a positive `bootstrap.resolve.timeout.ms`, marked evolving; default unclear | Removed (03) |
| Signal 3 | "Arrays of bytes, chars, ints and object references start at 12" | Ticket: first element offset becomes 12, breaking 8-byte alignment | Ticket wording |
| In the Know | GraalVM calendar "on JDK 25" | Calendar lists 25.x versions, doesn't state the JDK; 25.4 notes say OpenJDK 25.0.4.1 | "lists only 25.x releases … 25.4 is built on JDK 25", added 25.4 link |
| Top Resources | TACIT: "the JVM is trusted" | Paper's trusted set: compiler, capability library, "the runtime that executes type-checked code", optional local LLM | Paper's wording; added "the authors recommend combining it with a sandbox" (verbatim basis) |
| Top Resources | TACIT "July work" | Paper v1 1 Mar 2026, blog 27 Jul | "paper from March, blog post from July" |
| Debate | Category "arrived in two weeks" | Jev 15 Sep → LangChain4j 1.21.0 2 Oct | "under three weeks" |

Confirmed unchanged (sample): NATS timeline (10:02 link drop and 45 s recovery; 10:06 incident "recovered and is stable"; 12:32; 13:32; 8,000 forecast / 6,094 handled; "four and a half hours over a six-hour period"; 60-day final report; 18 pages). Firebase (2-line change, 2 h 11 min, dashboards "remained green", kill switch "released globally"). JEP 534 (22% heap / 8% CPU; Amazon "hundreds of services"). JEP 544 (Targeted, release 28; 65–80%; same CPU features and same GC, else warning and fallback). JEP 523 (Delivered in 27; publishes no percentages; 1792 MB). JDK-8386990 (Open, fix "tbd", Kuksenko; crypto −1..−4%, ScalaKmeans −15..−20%, ArrayCopy to −35%, String to −50%). JDK-8392511 (16 Sep, ~9%). JDK-8386450 (Won't Fix; Kuksenko attributes −20% to JVMCI removal). Kafka (KAFKA-20979 text and fix versions; 4.2.2 notes lack the fix; KIP-1279 "Accepted"; 4.5.0 revised plan 17 Mar 2027; RC4 posted 6 Oct, no votes yet; Ericsson addresses @ericsson.com). Scala 3.9 (3.9 "maintained for at least three years"; 3.3 "one year after Scala 3.9.0"; "no planned compiler or standard-library fix"). Jev paper (27/9/1, 11 non-overlapping, ECE 0.028, 346,009, $9.15, 0.36 s, degradation list, 0.5 threshold quote). LangChain4j 1.21.0 notes; naming 21–25 Sep. OpenAI Decisions "public beta". HN 1,989. GHSA-gmwr (6.6, patched 1.18.1-beta28). a2a-java GHSA-qw47 "Fail-open default task authorization", 7.5. Tigris (ratekeeper throttling, customer-visible replication lag).

## Link check

39 unique links checked. All return 200 except three `bugs.openjdk.org/browse/...` pages, which return 403 to scripted requests (bot block). The same tickets were read through the JBS REST API, so they exist; not opened in a browser.

## Tone pass (stop-slop + humanizer)

- Removed a dramatic fragment ("None of this is settled.") and a "not X" tail ("the price, not a bug to wait out").
- Replaced a pull-quote line in Top Resources with a reader-directed one.
- Rewrote the intro's meta-joiner ("The third is this month's Trenches").
- Swapped absolutes for plain verbs (`never`/`every` outside fixed footer text).
- Month mentions cut from 7 to 2 (header + a verbatim quote).
- No em or en dashes. No words from the `voice.md` ban list outside the fixed footer and JEP 523's own title.

## Structure checks

- Section order matches the blueprint; no Community Voice (optional).
- Today 7 bullets, every one linked on the bold text.
- Signal Over Noise exactly 3. In the Know 5. Top Resources 3.
- Debate and Trenches each end with a concrete Scalac angle.
- Dedup: decision models only in Debate; KAFKA-20979 only in Trenches; Signal 1 is release process only; JDK 27 split across Signal 3 (compact headers) and separate In the Know lines (JVMCI, G1, JEP 544).
- Freshness: all main items `NEW_THIS_MONTH` or `MATERIAL_UPDATE`. TACIT (`BACKGROUND_ONLY`) is labelled in the copy as not new.
- Claim boundaries present in prose: Debate ("Plenty is still unproven"), Trenches (analysis not reproduction; restart must beat metadata flush), Signal 1 (CVE exposure unconfirmed; snappy status disputed), Signal 2 (Spark 4.3.0 undated; SPARK-57549 open), Signal 3 (ScalaKmeans cause disputed).
- `images.md`: Debate, Trenches and cover prompts in house style; "Deliberately not drawn" section.

## Open before publish

1. **Kafka 4.4.0 RC4** — vote runs to 12 Oct; on 7 Oct no votes yet. If it passes before send, Signal 1's second sentence and the Trenches' "when they ship" need one edit each.
2. **Firebase SDK patch** — Google promised it "in the next week". If it ships before send, no change needed; the issue doesn't claim it hasn't.
3. **Publish date** — still undecided (recommendation: week of 19 Oct). Frontmatter goes in `05_publish`.
4. **Cover file** — decide whether `cover.png` lives in the repo this time (it dangled in #5 and #6).
