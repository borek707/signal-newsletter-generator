# Today bullets — SIGNAL Issue #7, September 2026

Draft table of contents. Wording gets a full pass in `03_draft`; links are final.

- **[A clean Kafka restart deleted fresh data.](https://issues.apache.org/jira/browse/KAFKA-20979)** An index truncation was never fsynced, so after restart new segments looked like they were written in 1970 and retention deleted them.
- **[LangChain4j adds a model that only decides.](https://github.com/langchain4j/langchain4j/releases/tag/1.21.0)** `DecisionModel` returns typed answers with probabilities, not text, and an independent test puts numbers on it.
- **[Kafka 4.4.0 is a month late.](https://lists.apache.org/thread/gvl8zgcqskrlhyswjlbbyrcjdcyhklyf)** Teams that planned CVE fixes around it learned the project never committed to a date.
- **[Scala 3.9 is the new LTS.](https://www.scala-lang.org/news/3.9/)** Old lazy vals in your dependencies still call `sun.misc.Unsafe`, and recompiling your own code doesn't fix them.
- **[JDK 27 changes your object layout by default.](https://bugs.openjdk.org/browse/JDK-8386990)** Compact headers save heap; Oracle's open ticket lists what they cost.
- **[A UK flight-data link "recovered" while corruption spread.](https://www.nats.aero/news/nats-publishes-preliminary-report-on-technical-incident-of-8-september/)** A one-millisecond race grounded UK departures for about four and a half hours.
- **[Firebase's kill switch crashed iOS apps everywhere at once.](https://firebase.blog/posts/2026/10/firebase-analytics-outage)** A two-line flag cleanup, served globally for two hours, with status pages green.
