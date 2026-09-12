# Duplicate-detection pass — 2026-09-12

Automated, full-corpus scan (Claude), replacing the manual folder-by-folder
duplicate review from Phase 1/2. Method and script: `site/dedupe_scan.py`
(read-only; raw output `site/dedupe_report.json`). Approach: 8-word shingles
of normalized body text (frontmatter/images/HTML comments stripped),
inverted-shingle-index candidate generation, exact Jaccard + containment on
candidates. Ran across all 504 notes in ~9 seconds.

**Why this ran:** the only duplicate check on record (REVIEW-LOG Task 2) was
a human comparing folder names and concluded "no other duplicated shelves
found." That was never a systematic content scan — it couldn't catch
duplicates that don't share a folder or an obvious name. It didn't.

## Resolved 2026-09-12 (12 files retired, Phill's decisions applied)

Each pair was read in full (not just scored) before acting. Every survivor
carries a `dedupe_note` in its frontmatter recording what was retired/merged
and why.

| Kept as | Retired | Why |
|---|---|---|
| Author Studies Jim/Rosemary Wells.md | Rosemary Wells (2)'s content kept, old file's name/content dropped | (2) had 8 extra lines, no losses |
| Author Studies Jim/Eve Bunting.md | ↑ same pattern | (2) had ~226 extra lines (discussion questions) + Australian spelling |
| Author Studies Jim/Eve Bunting2.md | ↑ same pattern | byte-identical, arbitrary keep |
| Author Studies Jim/Judith Viorst.md | ↑ same pattern | (2) had a 95-line writing-craft table the original lacked |
| Author Studies Jim/Margie Palatini.md | ↑ same pattern | (2) had ~360 extra lines + fixed typos |
| Author Studies Jim/Patricia Polacco 2.md | ↑ same pattern | (2) had a full extra story (*Christmas Tapestry*) + Adaptation section |
| Author Studies Jim/Patricia Polacco 3.md | ↑ same pattern | (2) fixed 4 OCR typos, same length otherwise |
| Author Studies Jim/Tony Johnston.md (kept as-is) | Tony Johnstone 2.md | **Reversed from initial lean** — checked author-name spelling in-body: Johnston.md has 81/81 correct; Johnstone 2.md has only 36/81 correct despite a couple of other word-choice fixes. Correct spelling mattered more. |
| — | Author Studies Jim/Phyllis Root.md (deleted) | Zero original author-study content — file was just the Rattletrap Car text, already properly lifted to Mentor Texts from a different source pack |
| Text Structures/Using Non-fiction Texts 1-38.md (kept as-is) | ...1-38 2.md | The "2" version flattened a blank form into prose bullets, against the project's own standard of keeping forms structured |
| Writing/Writer's Notebook 2 Quick Writes.md (kept as-is) | Writer's Notebook 2 2014.md | 99% identical, no unique content, "Quick Writes" matches the folder's naming convention |
| Mentor Texts/Writing Craft Mentor List.md (renamed from "WRITING CRAFT MENTOR LIST (2)") | Mentor Lists 2012 sorted.md | The bigger list (88% containment) kept as base; ~426 unique lines from the smaller list (book citations under Character Development/Exploding a Moment/See-Saw Pattern etc — genuinely different from the bigger list's own same-named sections, which are technique definitions, not book citations) appended and labeled |

## Not resolved — reclassified as false positives on closer read

- **Crescent Dragonwagon.md vs Home Place — Crescent Dragonwagon.md**: the
  Author Study contains the full poem (matches the lift) plus a genuine
  extra teaching activity (sensory chart) after it. Normal "pack contains a
  lift" pattern, just under the earlier reporting threshold. No action.
- **Mem Fox.md vs Critical Literacy/Stereotypes in Literature**: the overlap
  is Jim quoting *Wilfred Gordon McDonald Partridge* whole inside an
  unrelated critical-literacy pack — cross-shelf passage reuse, not
  accidental duplication. No action.

## Resolved 2026-09-12 — Reader's Theatre 1-18 anthology

- **Reading/Reader's Theatre: READERS' THEATRE 1.md vs "Readers' Theatre
  1-18.md"** — investigated in full, then split up. The second file was
  **not** a duplicate of the first; it was a **9-book** anthology (my first
  pass missed *Agatha's Feather Bed*, found on the re-read): *The Bunyip of
  Berkeley's Creek*, *Wombat Divine*, *Shoes from Grandpa*, *Agatha's
  Feather Bed*, *The Three Questions*, *My Little Sister Ate One Hare*,
  *The Grouchy Ladybug*, *Mister Seahorse*, *John Brown, Rose and the
  Midnight Cat*. Checked every book's ending against a known-published
  conclusion:
  - **8 of the 9 are complete, clean texts** — lifted to their own Mentor
    Texts standalones (`strand: reading`, `completeness: full`,
    `source: "Lifted from Reader's Theatre 1-18 pack"`).
  - **The Bunyip excerpt is not complete** — it breaks off mid-scene ("Sh,
    he said, I'm busy," — not the book's real ending). Not lifted (would
    misrepresent an abridged fragment as a complete text). Its full text
    already exists as a script inside READERS' THEATRE 1.md (confirmed by
    reading it — includes the "Second Bunyip" resolution scene this excerpt
    lacks), so nothing was lost by leaving it out.
  - Added a note to READERS' THEATRE 1.md's Bunyip script flagging that the
    1-18 excerpt was partial, and a cross-link from its John Brown script to
    the new John Brown prose standalone.
  - The now-fully-decomposed "Readers' Theatre 1-18.md" was retired (all its
    non-fragmentary content lives on as 8 standalones; the one fragment is
    superseded by RT1's complete script).
- **Writer's Notebook cluster** (`Writer's Notebook/Writer's Notebook.md`,
  `Writing/Writer's Notebook 1-103.md`, `Writing/Writing - Writer's
  Notebook.md`) — none of the three is clean (pandoc noise, OCR errors, or
  broken heading structure respectively). Needs a merge/rebuild pass, not a
  keep/retire call. Scoped as its own task per Phill (2026-09-12).
- **Reading/QUESTIONING Course Jim 2014.md vs QUESTIONING course 1.md** —
  kept both per Phill's instruction (2026-09-12): each has book sections the
  other lacks, not a simple re-scan. Flagged as a future
  merge-into-one-comprehensive-guide candidate, not a dedupe target.

## Not action items, logged for scale/design awareness

- 430 pairs where an Author Study or course pack fully contains a text also
  lifted to Mentor Texts — the intended "lift" convention (pack copy stays
  put), not a defect.
- 152 pairs of cross-shelf passage reuse (same mentor text quoted whole
  inside an unrelated Vocabulary/Writing Voice/Reader's Theatre/Inferring
  pack) — Jim's own authorial habit, not OCR duplication. Relevant to future
  site design (cross-link the canonical text into every guide that uses it)
  rather than to cleanup.

## Verification

Re-ran `site/dedupe_scan.py` after the fixes above: 504 → 492 notes, exact-
duplicate groups 1 → 0, near-duplicate pairs 642 → 613. Every survivor's
image references were checked to resolve correctly after the asset-folder
renames.
