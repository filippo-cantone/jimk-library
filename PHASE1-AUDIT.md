# Phase 1 audit — 2026-09-11 (verified from repo files; no restructuring applied)

Audit rule (frozen): a file counts as flagged only on the exact literals
`FLAGGED: low-confidence`, `needs-review`, `garbled_ocr`, or a dead
`src="/tmp` image link. Broad substring matches caused false positives
against `source_file` reference lines, so they are not used.

## Pass 2 page-range scan (the verification procedure)

Pass 1 rebuilt each note to readable Markdown. Pass 2 checks the rebuilt
`.md` against the original scan in page-range order (`<!-- p.N -->`):
per chunk, open rebuilt note + same-range source page and confirm (1) no
text truncation or duplication across boundaries, (2) landscape/rotated
pages intact, (3) blank-form tables rebuilt clean from photocopy masters
and left empty (e.g. Spelling 1-99 templates — empty is correct),
(4) embedded `assets/<stem>/media/` images resolve, (5) mentor-text lifts
end cleanly with no bleed into adjacent sections, (6) frontmatter intact.

## Verified counts

| Check | Result |
|---|---|
| Sources converted | 262 → 504 `.md` notes across 14 content folders |
| Mentor Texts | 289 files; full-text lifts carry `completeness: full/likely` (5 marked `likely`) |
| Author Studies Jim | 49/49 `strand: reading`, image-attr noise stripped |
| Supplement / index / nursery / craft (8 files) | all `reviewed` + `strand` in frontmatter |
| Photo libraries (Writer's Notebook 23 + Writing Voice 20) | 43 notes, cosmetic image-attr strip only, `src`/`alt` preserved |
| Live markers (`review_status`, `needs-review`, `FLAGGED`) | 0 |
| Dead `/tmp` image links | 0 |
| Vestige `* 2` directories | 0 |
| Restructuring of note content | none (deferred to Phase 2) |

## Fixes applied during this pass

- 3 files had `reviewed:`/`strand:` inserted in the body instead of
  frontmatter (Nursery Rhymes, Reading Like Writers Supplement, Accompanying
  Reading Like Writers): moved into frontmatter, replaced `review_status`.
- Author Study – Patricia Polacco and Mentor Lists 2012 sorted: last two
  `review_status` frontmatters promoted to `reviewed` + `strand` (same
  treatment as the other rebuilt notes; Polacco did not get a dedicated
  page-range check — flagged in REVIEW-LOG.md).

## Gate

Phase 1 DONE. Restructuring deferred per MASTERPLAN.md and Phill's
instruction ("restructure once all converted"). Phase 2 needs Phill's
approval before any note content is reorganised or the site is built.
