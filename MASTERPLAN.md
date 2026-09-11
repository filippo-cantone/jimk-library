# Jim K Teacher Knowledge Base — Masterplan

**Status (2026-09-11): Phase 1 complete and committed. Restructuring deferred —
no reorganisation of note content until Phill approves the Phase 2 plan.**

## What this is

The complete course archive of Jim, literacy consultant to the school:
reading and writing workshop packs, genre courses, author studies, mentor-text
lists, vocabulary, inferring, First 20 Days — plus photo writing-prompt
libraries. Goal: an easily accessible, searchable online knowledge base for
classroom teachers working independently. Internal school use only.

## Where things live

| Location | Role |
|---|---|
| Jim K source folder (iCloud) | Originals (.doc/.pdf) + raw OCR baselines. Never edited. |
| This repo | Cleaned Markdown + web-resolution images. The source of truth for the site. |
| Cloudflare Pages (Phase 4) | The open link teachers use. |

## Locked decisions

- Access: open link (unlisted URL, not published publicly).
- Clean everything before publishing (no raw OCR on the live site).
- Find both ways: full-text search + browsable curriculum hierarchy.
- Host: Cloudflare Pages (free, unmetered bandwidth). Deploy via CLI/git.
- Copyright: retyped picture-book texts are fine for internal school use
  (confirmed 2026-09-09). Revisit if the link ever goes public.
- Presentation: search-first library home + guided strategy pages
  (see `sketches/` in the working folder for the approved visual direction).
- Restructuring waits until all documents are converted (confirmed; Phill:
  "restructure once all converted"). Phase 1 does not reorder teaching content.

## Phase 1 — Convert and clean (DONE 2026-09-11)

Per-note easy-read pass, folder by folder, smallest first. One commit per folder.
Per-note standard:

- Fix OCR errors; rebuild tables verified against the scans; repair landscape
  sections. Keep `<!-- p.N -->` page markers for traceability.
- **Visuals are preserved, not described.** Hand-drawn sketches, worked
  diagrams and annotated examples are clipped from the scans at high
  resolution into `assets/` and embedded as figures (with a text key beneath
  for searchability). Photocopy masters (planners, analysis forms, blank
  templates) keep their original line-by-line layout as structured forms —
  never flattened into paragraphs.
- Heading structure; keep Jim's wording. No teaching-order restructuring.
- Frontmatter everywhere: title, source_file, tags, strand, reviewed + date.
  Zero `review_status` / `needs-review` / `FLAGGED` markers remain.

Across all notes:

- Strip pandoc noise (`{width=…}` attrs, `media/media` doubling,
  INCLUDEPICTURE leftovers); confirm image links resolve.
- Downsize photo copies to web resolution (originals untouched).
- The 4 identical `(2)` duplicates become pointers, not copies.
- **Complete book texts get standalone documents.** Whenever a full text of a
  real picture book (or poem, essay, story) is found inside a pack, lift it
  into its own document in Mentor Texts (frontmatter: author, source pack,
  completeness full/likely). The copy in the original pack stays put.
  Abridged or boundary-unclear texts stay in the pack only.

Result: 262 sources → 504 Markdown notes (289 in Mentor Texts); 0 live
markers; 0 dead `/tmp` links. See PHASE1-AUDIT.md for the verified counts
and REVIEW-LOG.md for per-folder progress and open questions for Phill.

**Two passes per folder.** Pass 1 cleans (OCR, tables, frontmatter, headings,
visuals, standalone lifts). Pass 2 verifies the rebuilt note against the
original scan in page-range order: no truncation/duplication across
boundaries, landscape pages intact, blank-form tables rebuilt clean and left
empty, embedded `assets/` images resolve, mentor-text lifts end cleanly with
no bleed, frontmatter intact. Only then is the folder committed as reviewed.

## Phase 2 — Information architecture (NOT STARTED — needs Phill's approval)

One-page map: strand tree (Reading · Writing · Genres · Author studies ·
Mentor texts · Vocabulary · Inferring · First 20 Days) + filters (strand,
genre, year level where stated, resource type: mini-lesson / demonstration
text / template / list). Merge duplicated subtrees, don't publish twice.
Restructuring of note content happens here, not before.

## Phase 3 — Build the site from this repo (NOT STARTED)

Static generator + client-side full-text search. Must: render tables/callouts,
printable pages, lazy-loaded images. Preview link for review before launch.

## Phase 4 — Deploy + iterate (NOT STARTED)

Cloudflare Pages open link. Updates are a git push. Teacher feedback drives
further cleanup; new material enters via convert → review → publish.
