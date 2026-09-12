# System Specification — Jim K Teacher Knowledge Base

Status: DRAFT, awaiting Phill's review. Once approved this becomes binding
alongside `MASTERPLAN.md` (`MASTERPLAN.md` stays the one-page status/history
file; this is the full technical spec it points to — the same relationship
`STRATEGY-TAXONOMY.md` and `DEDUPE-REPORT.md` already have to it).

**Purpose of this file:** so that anyone — Phill, another human, or a
different AI session with zero prior context — can pick this project up at
any point and know exactly what the finished thing is, why it's built this
way, and what to do next. If you are that person/AI: read this file fully
before touching `content/` or `site/`. `MASTERPLAN.md` §"Status" tells you
where the project actually is against this spec right now.

---

## 1. What this project is

A free, searchable, internal-use website for classroom teachers (Prep–Year
2), built from a literacy consultant's (Jim's) complete course archive.
Full background, constraints, and working agreement: `MASTERPLAN.md`.

The one-line design decision this whole spec follows from (approved by
Phill, 2026-09-12): **the site is organized around teaching strategies, not
source documents, and content that Jim repeated across multiple packs is
assembled once per topic, not duplicated per page.**

## 2. Content model

### 2.1 Entities, not files

The unit the site is built from is not "a converted pack" — it's an
**entity**: a thing a teacher searches for. Three entity types:

| Entity | What it is | Roughly how many |
|---|---|---|
| **Book** | A specific text (picture book, poem, story, fable) | ~300+ |
| **Strategy** | A reading or writing teaching strategy | ~21 (see `STRATEGY-TAXONOMY.md`) |
| **Author** | An author Jim wrote a study of | 38 |

A fourth category, **Getting Started** (First 20 Days, Teacher Planning,
Reading Conferences), is deliberately *not* an entity type — it's
sequential/routine content, shown as a small set of ordinary guide pages
outside this model. Don't try to force it in.

### 2.2 Fragments

A **fragment** is a bounded piece of text extracted from one source pack,
about one book, of one kind. This is the atomic unit of real content —
everything else (book pages, strategy pages) is a *view* over fragments.

Fragment kinds observed so far (extend this list as extraction finds new
ones, don't force a fragment into the wrong kind):

- `lesson` — a worked teaching sequence (e.g. an Inferring stop-and-infer
  routine)
- `vocab-focus` — a vocabulary/word-study treatment of the book
- `script` — a Reader's Theatre adaptation
- `craft-note` — writing-craft commentary/analysis of the book
- `discussion` — critical-literacy or discussion questions
- `mentor-text` — the complete lifted text of the book itself (already
  exist for ~300 books in `content/Mentor Texts/`; these are a fragment
  kind like any other, just usually the longest one)

**Every fragment records where it came from and stays traceable to it.**
Never present a fragment as if it has no source — that traceability is
inherited from `MASTERPLAN.md`'s existing working agreement and is not
negotiable.

### 2.3 The rule that resolves duplication

When the same fragment (or near-identical rewrite of one) exists in
multiple source packs — the confirmed, real pattern (see the Knuffle Bunny
example: the same plot-development write-up verbatim in `INFERRING2
Jim.md`, `Narrative Course 2014 June.md`, and `Mentor texts 1.md`) — **it
is extracted once**, attributed to its clearest/earliest source, and a note
records the other packs it was also found in. It is never shown twice on
the site.

### 2.4 The rule that resolves thin content (tabs vs. citations)

Decided 2026-09-12 after reviewing the book-page mockup: a book page (or
any entity page) gives a dedicated section/tab only to a fragment with real
depth — a paragraph or more of Jim's actual teaching text. A one-line
mention (a title on a list, a bare cross-reference) is never its own
section — it goes into a single shared **"Also appears in"** list, grouped
by what kind of appearance it is (strategy hub, reference list, author
connection), regardless of which shelf it came from. Do not create a
section for a fragment that has nothing to read.

## 3. Strategy taxonomy

Full table: `STRATEGY-TAXONOMY.md`. Summary of the structure it defines:

- **Three front doors**: Reading strategies (11), Writing strategies (14,
  including Genre Writing's internal sub-list), Author Studies (38,
  standalone — not filed under Reading or Writing, but every book page
  links to its author's page when one exists).
- **Search by text** is a fourth path into the same book pages, not a
  separate content type.
- **Getting Started** sits outside the taxonomy entirely (§2.1).

Known follow-up work the taxonomy itself surfaced (not yet done):
Questioning needs a 5-pack consolidation (bigger than the 2-pack merge
`DEDUPE-REPORT.md` originally scoped); Folktales (12 packs) and Poetry (4
packs) likely need internal sub-structure rather than one flat page.

## 4. Data storage — how entities and fragments are actually kept

This is new; `content/` alone (497 raw/cleaned pack files) cannot serve
entity pages directly — a book page needs material assembled from several
files at once. Decision: add a new top-level `entities/` directory that
sits *on top of* `content/`, which stays exactly what it is now (the
cleaned, deduplicated, but still pack-shaped raw material — never deleted,
never the thing a teacher lands on directly).

```
entities/
  books/<slug>.yaml
  strategies/<slug>.yaml
  authors/<slug>.yaml
```

**One YAML file per entity** (not JSON, not a database) — git-diffable,
human-readable, reviewable the same way `content/*.md` already is, no new
tooling dependency, consistent with the zero-cost/no-server constraint in
`MASTERPLAN.md`.

### 4.1 Book entity schema

```yaml
slug: knuffle-bunny
title: "Knuffle Bunny"
author: "Mo Willems"          # matches an authors/*.yaml slug if one exists
genre: picture-book
year: ["P", "1"]               # only where a source states it, per existing convention
strategies: [inferring]        # strategy slugs this book has a real fragment for
fragments:
  - kind: lesson
    strategy: inferring
    text: |
      <the extracted, reviewed text, as Markdown>
    source_file: "Inferring Course JIM/INFERRING2 Jim.md"
    source_lines: "2837-2952"
    also_found_in:
      - "Writing/Narrative Course 2014 June.md"
      - "Mentor Texts/Mentor texts 1.md"
  - kind: mentor-text
    text: |
      <full lifted text, if one exists in content/Mentor Texts/>
    source_file: "Mentor Texts/Knuffle Bunny — Mo Willems.md"   # only if it exists
also_appears_in:
  - kind: reference-list
    label: "Exploding a Moment"
    target: "Mentor Texts/Writing Craft Mentor List.md"
  - kind: author
    target: authors/mo-willems     # or explicitly "none" if honestly absent
```

### 4.2 Strategy entity schema

```yaml
slug: inferring
name: "Inferring"
branch: reading                 # reading | writing
overview: |
  <short synthesised why/how text, written fresh — see §6.2 on how much
  rewriting is acceptable>
routines:
  - name: "It Says – I Say – And So"
    source_file: "Inferring Course JIM/INFERRING2 Jim.md"
  - name: "Directed Listening Thinking Activity (DLTA)"
    source_file: "Inferring Course JIM/INFERRING2 Jim.md"
books: [knuffle-bunny, owl-moon, the-stranger, ...]   # book slugs with a fragment tagged this strategy
```

### 4.3 Author entity schema

```yaml
slug: mo-willems
name: "Mo Willems"
bio_source: "Author Studies Jim/<file>.md"   # only if a study exists; Willems currently has none — honest gap
books: [knuffle-bunny, ...]                   # every book by this author found anywhere in the corpus,
                                               # not only ones with a full author-study writeup
```

### 4.4 Provenance rule

`source_file` + `source_lines` must always resolve to something real in
`content/`. A fragment with no traceable source is a build error, not a
warning — this matches the existing "never fabricate; a failed tool call is
reported, not papered over" rule in `MASTERPLAN.md`.

## 5. Extraction pipeline

Five phases. Each one is a script producing a reviewable artifact — never
skip straight to generation without the intermediate artifact existing and
being checked.

**Phase A — Entity discovery.** Find every place in `content/` where a
known book is mentioned/quoted. Seed the book list from the ~300 already-
lifted `content/Mentor Texts/*.md` titles (known-good). Run a fuzzy
containment scan across all other notes — the same shingle-containment
technique already built and proven in `site/dedupe_scan.py` (it found 430
pack-contains-lift pairs and 152 cross-shelf reuse pairs during the dedupe
pass), applied here deliberately as extraction rather than dedupe-flagging.
Output: a candidate list of (book, source_file, approximate location)
hits.

**Phase B — Fragment extraction.** For each hit, find the actual start/end
boundary of that book's section within the source file — the same manual
technique used to split the Reader's Theatre anthology (title markers, page
breaks, checking the passage actually ends where you think it does, not
just where the next `##` happens to be — the Reader's Theatre split found 9
books in a file everyone assumed held fewer, precisely because of this
kind of careful boundary check). Classify the extracted span by kind
(§2.2). Write it into the relevant `entities/books/<slug>.yaml`.

**Phase C — Strategy/genre tagging at the fragment level.** Each fragment
gets tagged with which strategy(ies) it teaches. Start from Jim's own
existing trait tags (Phase 2's tagging pass, 309 books already tagged) as
grounding — don't re-derive from nothing where a grounded tag already
exists.

**Phase D — Page generation.** A static site generator (extend
`site/build.py`'s approach, or write its successor — it currently builds
one page per `content/*.md` file, which no longer matches the model; it
needs to read `entities/` instead) builds: book pages, strategy hub pages,
author pages, the home page, and a search index built over entity names
(so searching "Knuffle Bunny" returns the one book page, not scattered file
hits — this was the concrete problem identified when this model was first
proposed).

**Phase E — Human review**, one entity type or one strategy at a time —
same discipline as the existing "one commit per folder, verify before
committing" rule. Do not run Phase A–D across the whole corpus before a
pilot strategy has been reviewed and approved end-to-end.

**Pilot**: Inferring (10 packs) — already has trait/genre groundwork from
Phase 2, and the Knuffle Bunny example used throughout this spec came from
it. Build the full pipeline against Inferring first; do not start a second
strategy until Phill has reviewed the first one live.

## 6. Page templates and visual design

### 6.1 Approved visual design

Mockup: `df7b9973-d679-4ab6-b9ce-aaf8522dbbca` (claude.ai/code/artifact),
built from real Knuffle Bunny content, approved 2026-09-12 with one
revision (see `REVIEW-LOG.md`). Direction: a library catalogue-card
aesthetic — not Hermes's dashboard-card look. Design tokens (both themes
already specified in the mockup's CSS — reuse verbatim, don't re-derive):

| Token | Light | Dark | Role |
|---|---|---|---|
| `--paper` | `#EEECDF` | `#191C16` | page background |
| `--card` | `#FBFAF3` | `#21251C` | panel/card surface |
| `--ink` | `#22281D` | `#E9E7D9` | primary text |
| `--ink-muted` | `#5B6353` | `#A9AD9B` | secondary text |
| `--cloth` (accent, "book cloth" green) | `#35573A` | `#7CA980` | links, strategy tags, active tab |
| `--stamp` (accent, "library stamp" red) | `#AC3A2C` | `#D98A78` | used sparingly — duplication/merge notes, the prototype stamp |
| `--gold` (accent, "call number" gold) | `#99781F` | `#D8BC6C` | genre tags, kickers, citation labels |
| `--rule` | `#D2CEBA` | `#3A3E30` | hairline borders |

Typefaces: **Fraunces** (display/headings), **Source Sans 3** (body),
**Space Mono** (citations, tags, "call-number" metadata) — all Google
Fonts, loaded per the artifact CSP rules already used in the mockup file.

### 6.2 Book page

- Catalogue-card header: title, author, genre/strategy tag row.
- Tabs: one per fragment kind with real depth (§2.4) — never an empty or
  one-line tab.
- Every content section carries a source citation footer; a merged
  fragment carries a visible "also found in N other packs" note (§2.3).
- "Also appears in" section: flat card grid of every lightweight reference
  — strategy hubs, mentor lists, author link (or honest absence).
- Full spec by example: the approved mockup file itself is the reference
  implementation, not just a sketch — build against it directly rather
  than reinterpreting a written description of it.

### 6.3 Strategy page

Not yet mocked up visually — do that before building the Inferring pilot's
page, same process as §6.2 (real content, one look, iterate). Structural
requirement locked by the taxonomy discussion: short synthesised
"why teach it / how to teach it" overview (written fresh — label it as
synthesis, don't present it as Jim's verbatim words), a routines list, then
a browsable list/grid of every book with a fragment for this strategy,
linking into that book page's relevant tab.

### 6.4 Author page

Not yet mocked up. Structural requirement: Jim's author-study text kept in
his own words (this one *is* mostly verbatim, unlike the strategy
overview), plus a list of every book by that author found anywhere in the
corpus (§4.3) — not only the ones with full author-study coverage.

### 6.5 Home page

Not yet mocked up. Structural requirement: the three front doors (§3) as
primary navigation, plus a prominent search-by-text box. Build this only
after at least one real strategy (Inferring) exists to navigate to —
mocking it up first with dummy links was explicitly rejected by Phill
(2026-09-12: "I don't want to jump around just designing random pages").

## 7. Build and hosting

Reuses the existing decision from `MASTERPLAN.md` Phase 3: static
generator, Python stdlib + `markdown`/`pyyaml`, zero-cost hosting on
Cloudflare Pages, client-side search, deploy via git push. What changes is
the generator's *input* (§4, `entities/`, not `content/*.md` directly) —
the hosting/deploy mechanics don't need to change.

## 8. Cross-project interoperability — Ngarri Mentor Text Library

**Status: intent confirmed by Phill (2026-09-12), mechanism not yet built,
one real policy conflict flagged below and not resolved by this document.**

Phill also runs `Ngarri-Primary-School/ngarri-mentor-text-library` (a
separate, already-substantial Supabase-backed teacher library for a
different school). He wants this project's content genuinely
export/API-accessible to that project — not just a link between sites.

**What was found (2026-09-12) that this decision must account for:**
Ngarri's own repo already holds a private copy of 98 of this project's
Mentor Texts (`restricted-reference/jimk-mentor-texts/`, imported
2026-09-10, images excluded), under rules Phill approved in *that* project
two days before this conversation:

> "Never include this directory in website builds, Supabase records,
> public exports, releases or downloadable site assets." "Treat
> transcriptions as checking aids." "Use only short, necessary excerpts in
> teacher-facing analysis."

That rule, as written, forbids exactly the kind of consumption a real
export/API enables. **This document does not resolve that conflict** —
only Phill can, by updating Ngarri's `restricted-reference/README.md` (or
deciding the export should feed some *other* part of Ngarri's system that
isn't bound by that rule, e.g. informing their manual book-review workflow
rather than their public Supabase-backed viewer). Whoever builds the export
side of this must confirm that update has actually happened in the Ngarri
repo — not assume it — before wiring anything live.

**Recommended shape once that's resolved** (design-only, not yet built):

- Export **entity metadata and Jim's own teaching commentary** (fragment
  kinds `lesson`, `vocab-focus`, `script`, `craft-note`, `discussion`) —
  this is Jim's original analysis, not the book's copyrighted text.
- **Do not export the `mentor-text` fragment kind** (the verbatim lifted
  book texts) through this channel. This isn't just caution — it's the
  same line Ngarri's own content standard already draws for itself ("Do
  not publish copyrighted full texts") and the same line this project's
  own `MASTERPLAN.md` draws ("internal school use only... revisit if the
  link ever goes public"). An export fed into a *different school's*
  public-facing system is exactly the "going public" case that caveat was
  written for.
- Mechanism: static, versioned JSON published alongside the site build
  (e.g. `site/dist/api/books.json`, `strategies.json`, `authors.json`) —
  no server, no auth, consistent with the zero-cost constraint. Ngarri's
  side would fetch and parse it into their own Supabase-backed review
  workflow, the same way they currently manually mine the raw
  `restricted-reference` copy — just structured instead of raw Markdown.

This section is deliberately the least settled part of this document.
Treat §1–7 as the thing to build now; treat §8 as a real commitment that
needs its Ngarri-side policy question answered before the export mechanism
is built, not before the rest of this project proceeds.

## 9. Glossary additions

Extends `MASTERPLAN.md`'s existing glossary (Pass 1/2, strand, lift, etc. —
still current, still used inside `content/`):

- **entity**: a book, strategy, or author — the thing a page is built
  around, not a file.
- **fragment**: one bounded, sourced, kind-classified piece of extracted
  text belonging to one book entity.
- **front door**: one of the three primary navigation entry points
  (Reading strategies / Writing strategies / Author Studies), plus
  search-by-text as a fourth path.
- **also appears in**: the shared, tab-less reference section for
  lightweight citations (§2.4) — never a full section/tab.

## 10. Where the project actually is right now

Done: dedupe pass (`DEDUPE-REPORT.md`), Reader's Theatre anthology split,
Writer's Notebook cluster merge, strategy taxonomy (`STRATEGY-TAXONOMY.md`),
book-page visual design approved. This document. Not yet done: anything in
§4–§7 (no `entities/` directory exists yet, `site/build.py` still reads
`content/*.md` directly, no extraction scripts exist), strategy/author/home
page designs (§6.3–6.5), the Ngarri export mechanism (§8).

**Next concrete step, once this spec is approved:** build Phase A–E (§5)
for the Inferring strategy only, producing real `entities/books/*.yaml` and
`entities/strategies/inferring.yaml` files and the pages built from them,
for Phill's review — before touching any other strategy.
