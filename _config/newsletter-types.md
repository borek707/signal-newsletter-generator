# SIGNAL Newsletter Types

## Standard Monthly Issue

Default format. Published monthly.

Sections:
1. Header
2. Intro
3. Today
4. The Architecture Debate
5. Notes from the Trenches
6. Signal Over Noise (3 items)
7. Community Voice (optional)
8. In the Know
9. Top Resources
10. Footer
11. References

## Special Editions

Use only when explicitly requested.

### Post-Conference Digest

Focus: major announcements from one conference (e.g. KotlinConf, ScalaDays).
- Replace Debate with `Conference Takeaways`.
- Keep Trenches if a concrete production story emerges.
- Signals limited to announcements with migration impact.

### Incident Deep-Dive

Focus: one major production incident or security event.
- Replace Debate with `What Happened`.
- Trenches becomes `How It Broke` / `How They Fixed It`.
- Signals: related tooling/security changes.

### Technology Radar

Focus: quarterly tool/framework assessment.
- Replace Debate with `Adopt / Trial / Assess / Hold` quadrant discussion.
- Trenches: one migration story.
- Signals: major version changes.

## Issue Lifecycle

| Stage | Output | Gate |
|-------|--------|------|
| Brief | Month, issue number, candidate themes | Human approves themes |
| Research | Raw signals from all required sources | Human checks source coverage |
| Select | Final Debate + Trenches + 3 Signals | Human approves lineup |
| Draft | Full newsletter markdown | Human reads draft |
| Review | Fact-checked, link-checked draft | Human approves for publish |
| Publish | Final markdown + frontmatter + images | Scheduled/send |
| Post-publish | Social snippets, tracking | — |
