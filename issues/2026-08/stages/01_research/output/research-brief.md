# Research brief — SIGNAL Issue #6, August 2026

## Primary items

- **Metals v2:** Databricks published the source-first language-server design on
  11 August. Primary source: [Databricks](https://www.databricks.com/blog/open-sourcing-metals-v2-databricks-java-and-scala-language-server-multi-million-line-codebases).
- **Gradle 9.7:** release notes published 6 August; Isolated Projects move from
  experimental to incubating. Primary source: [Gradle](https://docs.gradle.org/9.7.0/release-notes.html).
- **JEP 541:** macOS/x64 deprecated-port work is integrated for JDK 28. Primary
  source: [OpenJDK](https://openjdk.org/jeps/541).
- **JEP 542:** proposes finalising the PEM API after previews. Primary source:
  [OpenJDK](https://openjdk.org/jeps/542).
- **JEP 540:** Simple JSON API remains incubating. Primary source:
  [OpenJDK](https://openjdk.org/jeps/540).
- **Confluent Cloud Q3 update:** capacity controls and follower fetching.
  Primary source: [Confluent](https://www.confluent.io/blog/2026-q3-confluent-cloud-launch/).
- **LinkedIn paper:** an agentic support system with a two-week randomised
  production test. Primary source: [arXiv](https://arxiv.org/abs/2608.10224).
- **Tutorial:** [Building Distributed Agents with LangGraph + Temporal](https://www.youtube.com/watch?v=jCHWup7-m8o), published 14 August.

## Production reference

Netflix Service Topology is a relevant Kafka and graph-processing architecture,
but its originating technical design predates August. Use it as a clearly labelled
reference, never as a new launch. Sources: [Netflix](https://medium.com/netflix-techblog/from-silos-to-service-topology-why-netflix-built-a-real-time-service-map-0165ba13a7bc) and [InfoQ's August coverage](https://www.infoq.com/news/2026/08/netflix-service-topology/).

## Research caveats

- A2A transfer coverage comes from Axios and is governance context, not a runtime
  implementation change.
- Medium, Axios and Reddit can return bot-block 403s to automated checks; claims
  were validated during research against the accessible content or alternate
  coverage.
