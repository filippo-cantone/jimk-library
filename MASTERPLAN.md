# Jim K Teacher Knowledge Base — Masterplan

> **START HERE (any AI continuing this project):** this file is the single
> source of truth for status and history. `SYSTEM-SPEC.md` is the full
> technical specification — content model, data schema, extraction
> pipeline, page templates, build process, cross-project interop — read it
> before building anything. `REVIEW-LOG.md` holds open questions and
> Phill's recorded answers. Nothing else in the repo gives instructions —
> if another doc starts doing so, merge it here or into `SYSTEM-SPEC.md`,
> or delete it.

**Status (2026-09-12): Phase 2.5's "restructured guide" direction is
SUPERSEDED. New direction approved by Phill (2026-09-12): a strategy-first
information architecture, content assembled per-entity across every pack
that touches it — not the old shelf-per-folder model, and not Hermes's
inferring.html prototype either. See "New direction" below,
`STRATEGY-TAXONOMY.md` (the new IA, replaces `IA-MAP.md`), and
`DEDUPE-REPORT.md` (near-complete — see its own status). `site/drafts/`
and `INFERRING2 Jim.md`'s restructure are superseded, not deleted (kept as
reference/salvageable content). Next: build the Inferring reading-strategy
pilot on the new model.**

## Claude's review (2026-09-12) — pending Phill's response

Phill asked Claude (a second AI) to read this project fresh and report back
before doing more restructuring work. Full findings not reproduced here
(they're in the chat, not a repo file) — summary of what changed the plan:

- Task 2's "no other duplicated shelves found" was a manual, folder-by-folder
  check, not a systematic scan. It missed real duplicates outside Reader's
  Theatre. **Now corrected** — see `DEDUPE-REPORT.md` (2026-09-12 run).
- The Mentor Texts shelf count in `IA-MAP.md` (289) is stale: 190 of those
  289 files are actually tagged `strand: reading` (per the
  confirmed/likely-completeness split), not `strand: mentor-texts`. A
  teacher browsing "Mentor Texts" only sees 99 of them. Not yet fixed —
  needs a decision on whether shelf assignment should ever encode
  provenance/completeness at all.
- Two incompatible content models exist side by side: the approved Phase 2.5
  approach (one long restructured Markdown doc per guide, e.g. `INFERRING2
  Jim.md`) and the unreferenced `site/drafts/inferring.html` prototype (a
  short synthesis page linking to ~17 atomic per-book lesson pages). The
  second is markedly better for teachers and isn't mentioned as the target
  anywhere in this plan. Not yet resolved.
- 310 of 504 notes (61%) are tagged `demonstration-text` and Phase 2.5 rules
  them "stay as-is" — that's where the actual wall-of-text problem lives
  (e.g. a 45k-word, one-heading Folktales file). The near-term plan doesn't
  touch the thing Phill originally flagged as the problem.

Open question for Phill: confirm whether to proceed on Claude's
recommended order (dedupe audit → pick one content model → fix the
shelf/tagging mismatch → prioritize shelves by teacher traffic → mechanically
split the demonstration-text anthologies) before more Phase 2.5 guide
restructuring continues.

**Resolved 2026-09-12 — see "New direction" below.** Dedupe audit: done
(`DEDUPE-REPORT.md`). Content model: settled, but not Hermes's inferring.html
either — see below. Shelf/tagging mismatch: superseded by the new strategy
taxonomy, not separately fixed. Demonstration-text anthologies: the
extraction pipeline below handles this directly (fragments pulled out of
them per-entity) rather than a separate mechanical splitting pass.

## New direction (approved 2026-09-12): strategy-first, entity-assembled content

Phill: the site should be organized around **teaching strategies** (reading
and writing), not around source packs or even around books. A teacher's two
front doors: "I want to teach a strategy" (browse) and "I have a specific
text" (search). Both lead to the same underlying pages.

This goes further than Hermes's `inferring.html` prototype. That page still
linked out to one-book-one-source-pack pages. The new model: **content is
organized by entity (book / strategy / author), not by source file.** The
same teaching content Jim wrote once but pasted into 2-3 different packs
over the years (confirmed pattern — see Knuffle Bunny example below) is
extracted once and shown once, tagged with every strategy/pack it's relevant
to, not duplicated across pages.

**Three entity types, three page kinds:**
- **Book pages** (~300+) — assembled from every pack that uses that book,
  not just one. Sections only appear when real content exists for them
  (no empty tabs). Verified example while designing this: *Knuffle Bunny*'s
  plot-development breakdown appears near-verbatim in `INFERRING2 Jim.md`,
  `Narrative Course 2014 June.md`, and `Mentor texts 1.md` — three packs,
  one piece of content, now planned to be merged into one page section with
  the duplication noted rather than repeated.
- **Strategy pages** (~21, see `STRATEGY-TAXONOMY.md`) — the site's main
  navigation. Short synthesised why/how overview + a list of book pages
  that teach it, pulled together from every pack that touches that
  strategy (e.g. Questioning needs fragments from 5 separate packs, not 1).
- **Author pages** (38) — third front door alongside Reading/Writing
  strategies, not filed under either branch (an author study teaches both
  at once). Linked both ways: browsable on its own, and every book page
  links to its author's page when one exists.

**Mockup approved** (with one revision) — `df7b9973-d679-4ab6-b9ce-aaf8522dbbca`
on claude.ai/code/artifact: a from-scratch visual design (library
catalogue-card aesthetic — not Hermes's dashboard-card look), built from real
Knuffle Bunny content. Revision made: collapsed an initial 3-tab layout
(Inferring lesson / Craft & mentor lists / Where it's used) to 2, after
Phill flagged the 3rd tab as thin and overlapping the 2nd — rule now: a tab
only exists for content with real depth (a paragraph+), everything thinner
(list citations, hub links) goes in one shared "Also appears in" section
regardless of which pack it came from.

**Extraction pipeline** (not yet built): entity discovery (fuzzy
containment scan across all notes, same technique as `dedupe_scan.py`,
seeded from the ~300 already-lifted Mentor Texts) → fragment extraction
(bounded spans per book mention, same manual-boundary technique used for
the Reader's Theatre anthology split) → strategy/genre tagging at the
fragment level (reusing Jim's existing trait tags as a head start) → static
page generation (same free/stdlib approach as the existing `site/build.py`)
→ human review per entity type, same discipline as the folder-by-folder
Phase 1 review.

**Next step**: build the Inferring pilot (10 packs, already has trait/genre
groundwork from Phase 2's tagging pass) on this model before running the
pipeline across all strategies.

**2026-09-12, later the same day — full spec written.** Phill: wanted one
concrete, documented plan before any more page-by-page design, detailed
enough that anyone or any AI could pick this project up cold. Written as
`SYSTEM-SPEC.md` — entity/fragment data schema, the five-phase extraction
pipeline, page templates per entity type, design tokens from the approved
mockup, build/hosting, and a review process. Read it before building
anything past this point.

Also surfaced: Phill separately runs
`Ngarri-Primary-School/ngarri-mentor-text-library` (a different school's
Supabase-backed teacher library) and wants this project's content
genuinely export/API-accessible to it — not just a link between sites.
That repo already holds a private copy of 98 of this project's Mentor
Texts under rules that currently forbid exactly that kind of consumption
("must not... enter... website builds, Supabase records, public exports").
Not resolved here — see `SYSTEM-SPEC.md` §8. Only Phill can update the
Ngarri-side policy; do not assume it's been done.

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
- [~] 2. Reader's Theatre dedupe — top-level source folder confirmed redundant, repo keeps Reading copy (decided 2026-09-11). **Superseded 2026-09-12**: that check was manual/folder-level only. An automated full-corpus scan found 19 further full/near-full-document duplicate pairs it missed (7 by filename, 12 with no filename hint) plus a 152-pair cross-shelf content-reuse pattern. See `DEDUPE-REPORT.md`. 12 resolved same day; the "Readers' Theatre 1-18.md" flagged pair turned out to be a 9-book anthology, not a duplicate — 8 books lifted to Mentor Texts, the 9th (an incomplete Bunyip fragment) superseded by the complete script already in READERS' THEATRE 1.md, source file retired. The Writer's Notebook 3-file cluster (two folders) was also resolved same day: one genuine gap moved across (a missing "Kinds of Notebook Entries" list), a 103-page OCR pack confirmed to add nothing recoverable, 11 mis-tagged pandoc headings fixed, two files retired. Task stays open pending only the two Questioning-courses files (kept both, flagged as a future merge candidate).
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
