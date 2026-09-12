# Review Log — post-hoc approval trail

Phill reviewed 2026-09-11 (answers recorded; items checked are closed).
Commits are per-folder so anything can be reverted or redone piecemeal.

## 2026-09-12 — full system spec written + Ngarri cross-project question raised

Phill: didn't want more page-by-page design before a single, complete,
documented plan existed — one anyone or any AI could pick up cold. Written
as `SYSTEM-SPEC.md`, covering everything decided below plus the parts not
yet decided (data schema, page templates, build process).

- [x] Data storage: new `entities/` directory (YAML, one file per book /
      strategy / author), sitting on top of `content/` which stays as-is
      (raw/cleaned pack material, never the thing a teacher lands on).
      `content/` is not deleted or replaced by this.
- [x] Design tokens (colour palette, type pairing) formalised from the
      approved mockup so future pages don't re-derive them.
- [x] Phill also runs `Ngarri-Primary-School/ngarri-mentor-text-library`
      (separate school, Supabase-backed teacher library) and wants this
      project's content genuinely export/API-accessible to it — confirmed
      2026-09-12, not "just a link between sites."
      **Found and flagged**: Ngarri's own repo already holds a private
      copy of 98 of this project's Mentor Texts
      (`restricted-reference/jimk-mentor-texts/`, imported 2026-09-10)
      under rules Phill approved in that project two days earlier, which
      as written forbid exactly this: "Never include this directory in
      website builds, Supabase records, public exports, releases or
      downloadable site assets."
      **Resolved 2026-09-12**: Phill will update that Ngarri-side
      restriction himself to allow full access, full texts included.
      `SYSTEM-SPEC.md` §8 updated to design for exporting everything (no
      commentary-only carve-out). Still true: this project can't verify
      the Ngarri-side change has actually happened — check
      `restricted-reference/README.md` there before wiring up a live
      export, whenever that work starts.

## 2026-09-12 — strategy-first IA + entity content model (Phill + Claude) — APPROVED

Phill, after Claude's review and the dedupe/Reader's Theatre/Writer's
Notebook work below: site should be organized around reading/writing
strategies, not source packs — and content spread across multiple packs
about the same thing (book, strategy) should be assembled together, not
just cross-linked to one source document.

- [x] Content model: entity-based (book / strategy / author pages
      assembled from every pack that touches them), not Hermes's
      inferring.html pattern (one-book-one-pack pages linked from a
      synthesis hub) and not the Phase 2.5 "restructured guide" pattern
      (one long doc per pack). Full spec: `MASTERPLAN.md` "New direction".
- [x] IA: strategy-first. Three front doors — Reading strategies, Writing
      strategies, Author Studies (kept separate from both branches, linked
      both ways from book pages) — plus search-by-text as a fourth path
      into the same book pages. Full taxonomy: `STRATEGY-TAXONOMY.md`
      (supersedes `IA-MAP.md`).
- [x] Word Choice (writing) vs Vocabulary (reading): keep as two separate
      pages, cross-linked. Not merged despite heavy book overlap — they
      answer different teacher questions.
- [x] Book-page visual design: approved with one revision. First draft had
      3 tabs (Inferring lesson / Craft & mentor lists / Where it's used);
      Phill flagged the 3rd as thin and redundant with the 2nd (both were
      "citation" content, just split across two tabs). Fixed rule: tabs
      only for content with real depth; everything else — list citations,
      hub links, author connections — goes in one shared "Also appears in"
      section. Mockup: `df7b9973-d679-4ab6-b9ce-aaf8522dbbca` on
      claude.ai/code/artifact, built from real Knuffle Bunny content (which
      also surfaced a live example of the exact duplication problem: the
      same plot-development write-up verbatim in 3 different packs).

Next: build the Inferring pilot on this model.

## 2026-09-12 — automated duplicate-detection pass (Claude) — RESOLVED (mostly)

Ran a full-corpus shingle-based near-duplicate/containment scan (script:
`site/dedupe_scan.py`, full results: `DEDUPE-REPORT.md`) to replace the
manual, folder-by-folder duplicate review this log previously relied on
(see the 2026-09-11 "Reader's Theatre" entry above — that check did not
scan file content, only folder names). 19 flagged pairs; Phill reviewed
Claude's per-pair recommendations and answered same day.

**Actioned (12 files retired/merged) — Phill approved 2026-09-12:**

- [x] Author Studies: all 6 "(2)"-suffix pairs (Rosemary Wells, Eve
      Bunting2, Eve Bunting, Judith Viorst, Margie Palatini, Patricia
      Polacco 2, Patricia Polacco 3) — kept the "(2)" content in each case
      (more complete and/or fewer OCR errors), old file retired, `(2)`
      dropped from the surviving filename.
- [x] Author Studies: Tony Johnston vs Tony Johnstone 2 — **kept Tony
      Johnston.md** (not Johnstone 2 as first leaned): checked in-body
      author-name spelling, Johnston.md has it right 81/81 times vs 36/81
      in Johnstone 2.
- [x] Author Studies: Phyllis Root.md deleted — no original author-study
      content, just a re-print of the already-lifted Rattletrap Car text.
- [x] Text Structures: kept "Using Non-fiction Texts 1-38.md" (structured
      form preserved), retired the "2" version (had flattened the form into
      prose, against project standard).
- [x] Writing: kept "Writer's Notebook 2 Quick Writes.md", retired "Writer's
      Notebook 2 2014.md" (99% identical, no unique content).
- [x] Mentor Texts: merged "Mentor Lists 2012 sorted.md" into "WRITING CRAFT
      MENTOR LIST (2).md" (renamed to "Writing Craft Mentor List.md") — the
      smaller list was 88% contained in the bigger one; its ~426 genuinely
      unique lines (book citations under headings the bigger list uses for
      technique definitions, not citations) appended and labelled.

**Reclassified as false positives — no action:**

- [x] Crescent Dragonwagon.md vs Home Place — normal pack-contains-lift
      pattern (poem + a real extra teaching activity after it), not a
      duplicate.
- [x] Mem Fox.md vs Critical Literacy/Stereotypes in Literature — cross-shelf
      passage reuse (Jim quoting Wilfred Gordon McDonald Partridge in an
      unrelated pack), not accidental duplication.

**Resolved 2026-09-12 — Reader's Theatre 1-18 anthology:**

- [x] Reading/Reader's Theatre: READERS' THEATRE 1.md vs "Readers' Theatre
      1-18.md" — was never a duplicate pair; on the re-read it turned out to
      be a **9**-book anthology (missed *Agatha's Feather Bed* on the first
      pass — found it while extracting exact boundaries). Checked every
      book's ending against a known-published conclusion: 8 of the 9 are
      complete texts, now lifted to Mentor Texts standalones (Wombat Divine,
      Shoes from Grandpa, Agatha's Feather Bed, The Three Questions, My
      Little Sister Ate One Hare, The Grouchy Ladybug, Mister Seahorse, John
      Brown Rose and the Midnight Cat). The 9th, Bunyip, breaks off mid-scene
      in this pack — not lifted (would misrepresent a fragment as complete);
      its full text already exists as a script in READERS' THEATRE 1.md, now
      noted there. "Readers' Theatre 1-18.md" retired — nothing left in it
      that isn't captured elsewhere. Full detail: `DEDUPE-REPORT.md`.

**Resolved 2026-09-12 — Writer's Notebook cluster:**

- [x] Writer's Notebook/Writer's Notebook.md, Writing/Writer's Notebook
      1-103.md, Writing/Writing - Writer's Notebook.md — checked each pair
      for genuine (not just reordered) content differences rather than
      picking a "least-bad" file. The first two turned out to be the same
      source text as the third, just worse-converted, with one real gap:
      the third was missing a "Kinds of Notebook Entries" list (40 items)
      that the first had — moved across and inserted at the matching point.
      The 103-page OCR pack added nothing recoverable (its only "unique"
      material was a poem OCR-garbled past usability). Also fixed 11 body
      paragraphs pandoc had mis-tagged as headings in the surviving file.
      Kept Writing/Writing - Writer's Notebook.md (retitled "Writer's
      Notebook"), retired the other two. 499 → 497 notes. Full detail:
      `DEDUPE-REPORT.md`.

**Deferred — Phill's explicit calls, 2026-09-12:**

- [ ] Reading: QUESTIONING Course Jim 2014.md vs QUESTIONING course 1.md —
      Phill: "keep both for now, flag as a future merge-into-one-
      comprehensive-guide candidate rather than a dedupe target." Each has
      book sections the other lacks; not a simple re-scan pair.

**Not action items, logged for scale/design awareness:**

- 430 pairs where an Author Study or course pack fully contains a text also
  lifted to Mentor Texts — this is the intended "lift" convention (pack
  copy stays put), not a defect.
- 152 pairs of cross-shelf passage reuse (same mentor text quoted whole
  inside an unrelated Vocabulary/Writing Voice/Reader's Theatre/Inferring
  pack) — Jim's own authorial habit, not OCR duplication. Relevant to future
  site design (cross-link the canonical text into every guide that uses it)
  rather than to cleanup.

Verification: re-ran `site/dedupe_scan.py` after the actioned fixes — 504 →
492 notes, exact-duplicate groups 1 → 0, near-duplicate pairs 642 → 613.
After the Reader's Theatre anthology split: 492 → 499 notes (8 lifted, 1
retired). After the Writer's Notebook merge: 499 → 497 notes (2 retired).
Still 0 exact-duplicate groups throughout; site rebuilds clean each time.
Task 2 above (2026-09-11, Reader's Theatre folder-level dedupe) stays
reopened until the Questioning-courses item above is resolved;
`MASTERPLAN.md` Phase 2 Task 2 updated to match.

## Phill's answers (2026-09-11)

- [x] Barefoot (Edwards) + John Henry (Lester) confirmed against published books → `completeness: confirmed`.
- [x] Bunny Cakes (Wells), Coyote and the Goat (fable), Zipping Zapping Bats (Earle) confirmed → `completeness: confirmed`.
- [x] Come on, Rain confirmed (ending verified against bleed boundary).
- [x] Clabbered Dirt / Spring / Winter (Paulsen) stay in pack (one collection, boundaries unclear).
- [x] Whale passage stays in pack as-is ("Leave as is").
- [x] Over and Under the Snow stays in pack as abridged.
- [x] Guess Who: scrambled in Jim's original, no print original held — left as-is.
- [x] Stone Swan / Prince's Unwelcome Disguise / Paddle Whispers: left in pack (sources unidentified).
- [x] Too Many Tamales (“Tomales” in pack), My Name Is Yoon (“YOON” in pack): titles corrected, both confirmed.
- [x] The Boy Who Loved Words / Bigmama's standalones accepted.
- [x] Time Somebody Told Me — Quantedius Hall standalone accepted.
- [x] Author Study – Patricia Polacco reviewed status accepted.
- [x] Phase 2 strand mapping approved in full (2026-09-11): Genres 41→genres; Author Studies 49→new `author-studies` tag; Text Structures 5→reading; Literacy 1-15→first-20-days; Teacher Planning→writing; Symbolism (`critical-literacy`)→reading; Bunny Cakes + Coyote and the Goat→`mentor-texts`; 12 missing strands filled (Reading 5→reading, Writing 6→writing, RLW 2 Supplement→mentor-texts); 10 Mentor Texts lists/supplements/indexes→`mentor-texts`. Convention ratified: `mentor-texts` = lift verified against published book (`completeness: "confirmed"`), `reading` = complete in-pack text (`completeness: full`).
- [x] 2026-09-11 mechanical pass (49 Author Studies strand + image-attr strip, 8 supplement/index/nursery/craft tags, 3 photo-library noise strips) — verified by Phill, all good.
- [x] Phase 2 resource-type kinds approved (2026-09-11): 6 kinds (guide, mini-lesson, demonstration-text, prompt-set, template, list); RT packs ruled guides. Follow-up idea from Phill: trait/strategy tags on book notes (books-by-craft lists exist in Mentor Lists 2012) — scoped as a later pass, not a 7th kind.
- [x] Phase 2 IA map approved in full (2026-09-11): 8 shelves as in IA-MAP.md; genre + year-level filters as a later tagging pass; trait/strategy tags join that pass.
- [x] Task 6 resolved as no-move (2026-09-11, agreed by Phill): shelves work from `strand` labels; no files moved (would break relative image links for no teacher-visible gain).
- [x] Genre/year/trait tagging pass DONE 2026-09-12: genre 323, traits 309, year 19 (all verified by census). Sources: Jim's own Mentor Lists (158 books' craft/genre/strategy mappings), agent judgment grounded in note bodies + source packs (152), folder path (15 genre guides). Honest gaps: 2 body-less books without genre; Moon Was the Best (Jim names no teaching use) without traits. Year tags explicit-only and spot-verified. One genre agent timed out mid-task; its body-dump survived and two half-agents finished the job.

## Folder progress (updated 2026-09-11)

- [x] Text Structures (5 notes) — rebuilt pilot
- [x] Choral reading (3 notes + guide + standalones)
- [x] Information Report — guide rewrite, twin scan retired, maps clipped
- [x] Literacy Overview Jim (2 guides) — rewritten, 2 diagrams clipped
- [x] First 20 Days Literacy (6 notes) — Spelling 11 lifts, Writing 7 lifts, Writing2 7 (Pamela Allen), Writing3 3 sets
- [x] Inferring Course JIM (10 notes) — lifts: INF1 5, INF2 6, INF3 9, INF5 2 (Tan), INF7 5, INF8 2 (nonfiction)
- [x] Vocabulary Course Jim (9 notes) — V1–V10 sweeps, ~100+ lifts
- [x] Genres (41 notes) — rebuilt; 9 fables lifted (Fables 1-23)
- [x] Reading (32 notes) — guides rebuilt, flowchart reconstructed, RT de-dupe pending Phill
- [x] Writing (14 notes) — strand tags added
- [x] Author Studies Jim (49 notes) — strand + image-attr strip
- [x] Mentor Texts (289 files) — lifts + 8 supplement/index/nursery/craft tags; all `likely` now confirmed by Phill
- [x] Writer's Notebook (23) + Writing Voice (20) — frontmatter + image-attr noise strip
- [x] Reader's Theatre — top-level source folder confirmed pure duplicate (11/11 content-identical; Reading copy also holds 2 extra PDFs). Repo keeps Reading copy. Source folder renamed 2026-09-11 to `Reader's Theatre (DUPLICATE - see Reading-Reader's Theatre)` as a one-off override of the read-only rule (Phill). Decided by Phill 2026-09-11.
- [ ] Phase 2 restructuring — APPROVED 2026-09-11, in progress (tasks in MASTERPLAN.md)
