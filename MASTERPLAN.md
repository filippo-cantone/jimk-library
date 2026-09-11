# Jim K Teacher Knowledge Base — Masterplan

> **START HERE (any AI continuing this project):** this file is the single
> source of truth. It tells you what the project is, why it exists, how to
> work, where we are, and the exact next step. `REVIEW-LOG.md` holds open
> questions and Phill's recorded answers. Nothing else in the repo gives
> instructions — if another doc starts doing so, merge it here or delete it.

**Status (2026-09-12): Phase 2.5 IN PROGRESS (INF 2 pilot). Site build paused:
restructured guides will BE the site content (raw packs stay repo-only).
Phase 3 preview exists; guided inferring draft exists (site/drafts/).**

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

## Phase 2 — Information architecture (APPROVED 2026-09-11 — in progress)

One-page map: strand tree (Reading · Writing · Genres · Author studies ·
Mentor texts · Vocabulary · Inferring · First 20 Days) + filters (strand,
genre, year level where stated, resource type: mini-lesson / demonstration
text / template / list). Merge duplicated subtrees, don't publish twice.

### Tasks (approved by Phill 2026-09-11)

- [x] 1. Leftover Phase 1 sample — mechanical pass verified by Phill, all good.
- [x] 2. Reader's Theatre dedupe — top-level source folder confirmed redundant, repo keeps Reading copy (decided 2026-09-11).
- [x] 3. Strand-tag audit — DONE 2026-09-11. 121 notes retagged and verified (504 total, zero missing): Genres 41→genres; Author Studies 49→new author-studies tag; Text Structures 5→reading; Literacy 1-15→first-20-days; Teacher Planning→writing; Symbolism→reading; Bunny Cakes + Coyote/Goat→mentor-texts; 12 missing strands filled; 10 Mentor lists/supplements→mentor-texts.
- [x] 4. Resource-type tagging — DONE 2026-09-11. All 504 tagged and verified: demonstration-text 310, guide 160 (incl. 13 RT packs per ruling; Voice/strategy/vocab packs ruled guides on size — multi-thousand-line packs, not single sittings; 3 unclear author-study files slotted as teacher background reading), mini-lesson 4, prompt-set 24, list 5, template 1.
- [x] 5. One-page IA map — APPROVED 2026-09-11 (all 3 questions yes: 8 shelves; genre + year as later tagging pass; trait/strategy tags join that pass). Saved as `IA-MAP.md`.
- [x] 6. Restructure — DONE 2026-09-11 as no-move (agreed by Phill): shelves work from `strand` labels (verified complete across all 504); the site will build shelf views from tags. No files moved — moving would break relative image links for zero teacher-visible gain.

## Phase 2.5 — Restructure guides for teachers (APPROVED 2026-09-12, in progress)

Teachers must never face raw packs. The 160 guides get rebuilt to the
Easy-Read standard: contents-dump becomes navigation (one section per unit:
Why → steps → worked example); book applications link out to standalone
mentor texts instead of inline walls. Jim's wording kept; order and hierarchy
rebuilt; Phill approves per folder. Demonstration texts (310) stay as-is;
lists/prompt-sets/templates get light structuring after guides. Restructured
guides ARE the site content (raw packs remain repo-only source). Pilot:
INFERRING2 Jim.md (parent: guided inferring page in site/drafts/). Site build
paused until the pilot formula is approved.

## Phase 3 — Build the site (BUILT 2026-09-12, preview exists; paused for 2.5)

Static generator + client-side full-text search from this repo. Must: render
tables/callouts, printable pages, lazy-loaded images. Preview link for
review before launch. Presentation: search-first library home + guided
strategy pages.

Built: `site/build.py` (stdlib + markdown/pyyaml; `pip install -r
site/requirements.txt`) writes `site/dist/` (gitignored; preview symlink
mode, deploy copy mode). Home with live search + shelf/kind/genre/year
filters, 8 shelf pages grouped by kind with on-shelf filter, one page per
note (breadcrumb, chips, print button, lazy images, print CSS).
`site/linkcheck.py` audits all local targets. Rebuild + verify:
`python3 site/build.py --mode preview && python3 site/linkcheck.py`.
Deploy (Phase 4) runs the same builder with `--mode deploy` on Cloudflare.

Two dead image refs found by the builder and repaired in source (not site
code): Lost Thing standalone repointed to its INFERRING5 pack image;
unrenderable /tmp .wmf tag removed from character study narratives
(empty asset folder, nothing to point at).

## Phase 4 — Deploy + iterate (NOT STARTED)

Cloudflare Pages open link (free, unmetered; deploy via CLI/git). Updates
are a git push. Teacher feedback drives further cleanup; new material enters
via convert → review → publish.

## Open next — genre/year/trait tagging pass (in progress 2026-09-11)

Three new frontmatter fields — `genre:` (what kind of text), `year:` (only
where Jim states it), `traits:` (list of writing-craft elements and reading
strategies the book serves). DONE 2026-09-12: 323 carry genre (308 of 310
books + 15 genre guides; 2 books body-less, honestly skipped), 309 carry
traits (158 from Jim's own lists, 152 agent-judged grounded in notes/packs;
1 book Jim names no use for, left blank), 19 carry year (explicit statements
only, verified against false positives; incl. Grade 3 poetry anthology the
first sweep missed). Guides take genre from folder path; no traits on guides.
