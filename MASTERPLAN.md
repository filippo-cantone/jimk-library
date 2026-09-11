# Jim K Teacher Knowledge Base — Masterplan

> **START HERE (any AI continuing this project):** this file is the single
> source of truth. It tells you what the project is, why it exists, how to
> work, where we are, and the exact next step. `REVIEW-LOG.md` holds open
> questions and Phill's recorded answers. Nothing else in the repo gives
> instructions — if another doc starts doing so, merge it here or delete it.

**Status (2026-09-11): Phase 1 complete and committed. Phase 2 needs Phill's
approval before anything starts. Next step: Phill approves the Phase 2
restructuring plan (strand tree below) — until then, do not reorganise,
rebuild the site, or convert anything new.**

## Why (the goal)

Jim, a literacy consultant, left the school his complete course archive:
reading/writing workshop packs, genre courses, author studies, mentor-text
lists, vocabulary, inferring, First 20 Days — plus photo writing-prompt
libraries. Target: classroom teachers working independently (students
Prep–Year 2), as an easily accessible, searchable online knowledge base.
Internal school use only.

Constraints: zero cost (hosting, search, maintenance); Victorian DoE /
curriculum sources preferred over generic ones; dictation punctuation is
semantic, not pause-based; retyped picture-book texts are fine for internal
school use (confirmed 2026-09-09 — revisit if the link ever goes public).

## How Phill works

- Iterative visual review: show screenshots/renders, he flags precisely, you correct.
- Faithful text semantics: Enter = new line, blank lines = visible gaps, multiple spaces = widened gaps.
- Pedagogical exactness over speed. Show work, don't describe it.
- Short reports: what changed, what's verified, what's left. No filler, no replays.

## Where things live

| Location | Role |
|---|---|
| Jim K source folder (iCloud) | Originals (.doc/.pdf) + raw OCR baselines. **Never edited.** |
| This repo | Cleaned Markdown + web-resolution images. Source of truth for the site. |
| Cloudflare Pages (Phase 4) | The open link teachers use (unlisted URL, not public). |

## Working agreement (standing instructions for any AI)

- Source folder is read-only. All work happens in this repo.
- Work folder by folder, smallest first; one commit per folder; verify before committing.
- Frontmatter everywhere: `title`, `source_file`, `tags`, `strand`, `reviewed` + date.
- **Visuals are preserved, not described.** Clip hand-drawn sketches, worked diagrams, annotated examples from scans into `assets/` as figures (text key beneath for search). Photocopy masters keep line-by-line layout as structured forms — never flattened.
- Complete book/poem/story texts found inside packs get standalone docs in Mentor Texts (`author`, `source pack`, `completeness: full/likely`); the pack copy stays put. Abridged/boundary-unclear texts stay in the pack only.
- Keep `<!-- p.N -->` page markers for traceability. Strip pandoc noise (`{width=…}`, `media/media` doubling, INCLUDEPICTURE leftovers); confirm image links resolve.
- Never fabricate: every claim about files must come from tool output (reads, greps, counts). A failed tool call is reported, not papered over.
- No restructuring of note content without Phill's explicit approval.

## Glossary (project-specific meanings)

- **Pass 1**: rebuild a note to readable Markdown (OCR fix, tables, frontmatter, headings, visuals, lifts).
- **Pass 2**: verify the rebuilt note against the original scan in page-range order (no truncation/duplication, landscape intact, blank forms left empty, images resolve, lifts end cleanly, frontmatter intact).
- **strand**: frontmatter curriculum tag (reading, writing, mentor-texts, …).
- **completeness** (`full`/`likely`): whether a lifted standalone text is verified complete vs probably-complete.
- **rebuilt**: a note converted to the easy-read standard (not restructured).
- **lift**: a complete text extracted to its own Mentor Texts document.
- **photo library**: Writer's Notebook (23 notes) + Writing Voice (20 notes) — image-prompt collections, not prose.

## Phase 1 — Convert and clean (DONE 2026-09-11)

262 sources → 504 Markdown notes across 14 content folders (289 in Mentor
Texts, incl. ~126 lifted full texts). Verified gate: zero live review
markers (`review_status`/`needs-review`/`FLAGGED`), zero dead `/tmp` image
links, frontmatter throughout, no `* 2` vestige dirs, source originals
untouched, committed and pushed. Per-folder trail and Phill's recorded
answers: `REVIEW-LOG.md`.

## Phase 2 — Information architecture (NOT STARTED — needs Phill's approval)

One-page map: strand tree (Reading · Writing · Genres · Author studies ·
Mentor texts · Vocabulary · Inferring · First 20 Days) + filters (strand,
genre, year level where stated, resource type: mini-lesson / demonstration
text / template / list). Merge duplicated subtrees, don't publish twice.
Content restructuring happens here, not before.

## Phase 3 — Build the site (NOT STARTED)

Static generator + client-side full-text search from this repo. Must: render
tables/callouts, printable pages, lazy-loaded images. Preview link for
review before launch. Presentation: search-first library home + guided
strategy pages.

## Phase 4 — Deploy + iterate (NOT STARTED)

Cloudflare Pages open link (free, unmetered; deploy via CLI/git). Updates
are a git push. Teacher feedback drives further cleanup; new material enters
via convert → review → publish.
