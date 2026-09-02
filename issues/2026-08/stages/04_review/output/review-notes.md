# Review notes — Issue #6 (August 2026)

Reviewed `03_draft/output/draft.md` against the issue selection, voice rules,
freshness rules and newsletter structure. Output: `reviewed-draft.md`.

## Corrections made

1. **Netflix is no longer framed as August news.** The original technical post
   predates the issue window. The section now opens by calling it a production
   reference, while its August InfoQ coverage supports the newer operational
   details. This preserves the requested Trenches chapter without misdating it.

2. **Removed an unbounded "biggest Scala codebase" community quote.** A Reddit
   commenter made the claim, but no named comparison set supports it. The remaining
   Community Voice statement is attributed to the same thread and avoids the claim.

3. **Kept proposal states distinct from releases.** JEP 542 remains a proposal to
   finalise after previews; JEP 540 remains incubating; JEP 541 is described as the
   JDK 28 deprecated-port path, not a supported port.

4. **Kept the tutorial as a video.** The selected Temporal video is the tutorial of
   the month. The Netflix material remains the full Trenches chapter, not a resource.

## Checks

- Section order matches the blueprint.
- Today has 6 linked items.
- Signal Over Noise has exactly 3 items.
- In the Know has 4 items.
- Debate and Trenches end with concrete Scalac recommendations.
- No em dashes; no claim-level banned precision words remain.
- Every externally verifiable claim is adjacent to a direct source link or is a
  clearly labelled editorial recommendation.

## Publish note

`cover: ./cover.png` is retained for the CMS pipeline, but this repository has no
August cover asset. The Markdown is publish-ready; attach the final cover in the
publishing system before the subscriber send.
