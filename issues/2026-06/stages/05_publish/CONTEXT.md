## Inputs

- `../04_review/output/reviewed-draft.md`
- `../04_review/output/review-notes.md`
- `../../_config/newsletter-structure.md`

## Process

1. Add frontmatter:
   - `title`: `SIGNAL [Month] [Year]: [Main Topic]`
   - `description`: 150-160 chars
   - `authors`: `piotr_borkowicz` or `Scalac Engineering Team`
   - `date`: ISO format
   - `tags`: relevant tags
   - `cover`: `./cover.png` or `/images/blog/...`
   - `draft: false`

2. Add hero image placeholder if applicable.
3. Finalize footer and References section.
4. Ensure image paths are consistent.
5. Produce a send-ready markdown file.

## Outputs

- `output/SIGNAL_[Month]_[Year].md` — final newsletter.
- `output/images/` — any images used.

## Review gate

Human schedules or sends the newsletter.
