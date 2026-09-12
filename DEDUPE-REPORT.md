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

## Open — needs its own task, not a quick merge

- **Reading/Reader's Theatre: READERS' THEATRE 1.md vs "Readers' Theatre
  1-18.md"** — investigated in full. The second file is **not** a duplicate
  of the first; it's an 8-book anthology (*The Bunyip of Berkeley's Creek*,
  *Wombat Divine*, *Shoes from Grandpa*, *The Three Questions*, *My Little
  Sister Ate One Hare*, *The Grouchy Ladybug*, *Mister Seahorse*, *John
  Brown, Rose and the Midnight Cat*). Only the first and last of those eight
  were adapted into scripts already present in READERS' THEATRE 1.md — the
  other six books' full text exist nowhere else in the corpus. **Left
  untouched.** Proper fix: lift each of the 8 as its own Mentor Texts
  standalone (matching the existing lift convention), then retire this file
  once all 8 are confirmed captured elsewhere. Do not delete or merge before
  that's done — real content would be lost.
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
