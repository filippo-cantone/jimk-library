# Jim K Teacher Knowledge Base — Masterplan

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

## Phase 1 — Reorganise everything (current phase)

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
- Heading structure; reorder rambling sequences into teaching order with a
  change-note where order moves; keep Jim's wording.
- Replace `needs-review` with `reviewed` + date in frontmatter.

Across all notes:

- Frontmatter everywhere: title, source_file, tags, strand.
- Strip pandoc noise (`{width=…}` attrs, `media/media` doubling,
  INCLUDEPICTURE leftovers); confirm image links resolve.
- Downsize photo copies to web resolution (originals untouched); target ~150 MB repo.
- The 4 identical `(2)` duplicates become pointers, not copies.
- **Complete book texts get standalone documents.** Whenever a full text of a
  real picture book (or poem, essay, story) is found inside a pack, lift it
  into its own document in Mentor Texts (frontmatter: author, source pack,
  completeness confirmed/likely). The copy in the original pack stays put.
  Abridged or boundary-unclear texts stay in the pack only.

Order: Text Structures → Choral reading → Information Report →
Literacy Overview → Text Structures… (then by size; photo libraries last).
Review checkpoint per folder before moving on.

**Two passes per folder.** Pass 1 cleans (OCR, tables, frontmatter, headings,
visuals, standalone lifts). Pass 2 re-reads the finished folder top to
bottom asking: is the *organisation* right — method pages vs collections
split out? Any missed diagrams, missed complete texts, flattened forms,
mis-titled poems? Only then is the folder committed as reviewed.

## Phase 2 — Information architecture

One-page map: strand tree (Reading · Writing · Genres · Author studies ·
Mentor texts · Vocabulary · Inferring · First 20 Days) + filters (strand,
genre, year level where stated, resource type: mini-lesson / demonstration
text / template / list). Merge duplicated subtrees, don't publish twice.

## Phase 3 — Build the site from this repo

Static generator + client-side full-text search. Must: render tables/callouts,
printable pages, lazy-loaded images. Preview link for review before launch.

## Phase 4 — Deploy + iterate

Cloudflare Pages open link. Updates are a git push. Teacher feedback drives
further cleanup; new material enters via convert → review → publish.
