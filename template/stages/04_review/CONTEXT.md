## Inputs

- `../03_draft/output/draft.md`
- `../01_research/output/research-brief.md`
- `../../_config/voice.md`
- `../../_config/fact-check-rules.md`
- `../../_config/newsletter-structure.md`

## Process

1. **Structure check:** verify all required sections exist in correct order.
2. **Fact-check:** verify release dates, metrics, KIP statuses, company case studies against sources.
3. **Link check:** every claim in Today, Debate, Trenches, Signals, In the Know, Top Resources has a source link.
4. **Tone check:** remove throat-clearers, emphasis crutches, business jargon, adverbs, passive voice, em-dashes.
5. **Deduplication check:** no topic repeated across Debate/Trenches/Signals/In the Know.
6. **Selection check:** exactly 3 Signals, 3-5 In the Know items, Today 6-8 bullets.
7. **Scalac angle check:** Debate and Trenches both end with concrete recommendation.
8. **Date rule check:** no repeated month/year phrases in body.
9. **Freshness check:** every main item has a freshness tag; no `BACKGROUND_ONLY` item appears as current news.
10. **Illustration check:** `images.md` contains Debate and Trenches prompts and matches the existing Scalac diagram-comic style.
11. Produce a fixed draft with inline notes for any unresolved issues.

## Outputs

- `output/reviewed-draft.md` — corrected newsletter.
- `output/review-notes.md` — list of changes and open questions.

## Review gate

Human approves reviewed draft before publish stage.
