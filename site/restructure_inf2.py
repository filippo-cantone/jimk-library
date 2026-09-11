#!/usr/bin/env python3
"""Phase 2.5 pilot: restructure INFERRING2 Jim.md (structure + merges only).

No words removed. Added: editor intro (marked), TOC with anchors, a few
structural subheads (marked). Reports link-out candidates (embedded full
texts with verified standalones) WITHOUT replacing them.
"""
import difflib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INF2 = REPO / "content/Inferring Course JIM/INFERRING2 Jim.md"
MENTORS = REPO / "content/Mentor Texts"

ED = "<!-- editor: Phase 2.5 restructure; hierarchy rebuilt, wording untouched -->"

TOC = """{ed}

This pack teaches inferring through portable routines, theme work,
illustration, wordless books and minimum-text books. Start with the routines;
use the book units in any order.

## Contents

- [Teaching inferring: the model](#u-model)
- [It Says – I Say – And So](#u-itsays)
- [DLTA and Granddaddy's Gift](#u-dlta)
- [Reciprocal Teaching routines](#u-reciprocal)
- [Inferring about theme](#u-theme)
- [The Stranger](#u-stranger)
- [Using illustrations and TC+BK=I](#u-illustrations)
- [Tight Times](#u-tight)
- [Yo! Yes! and Create a Dialogue](#u-yo)
- [I Want My Hat Back / This Is Not My Hat](#u-klassen)
- [Wordless picture books](#u-wordless)
- [The Sweetest Fig](#u-fig)
- [Bootsie Barker Bites](#u-bootsie)
- [O.W.I.: Observe, Wonder, Infer](#u-owi)
- [Books with minimum text](#u-mintext)
- [Knuffle Bunny](#u-knuffle)
- [A Splendid Friend, Indeed](#u-splendid)
- [Top Cat](#u-topcat)
""".format(ed=ED)

# (anchor id, exact ## heading, occurrence index 0-based)
ANCHORS = [
    ("u-model", "## Teaching Inferring", 0),
    ("u-itsays", "## It Says – I Say – And So …", 0),
    ("u-dlta", "## Directed Listening Thinking Activity DLTA", 0),
    ("u-reciprocal", "## Predicting", 0),
    ("u-theme", "## Inferring about THEME", 0),
    ("u-stranger", "## The Stranger Chris Van Allsburg", 0),
    ("u-illustrations", "## Using illustrations", 0),
    ("u-tight", "## Tight Times Barbara Shook Hazen", 0),
    ("u-yo", "## Yo! Yes! Chris Raschka", 0),
    ("u-klassen", "## I Want My Hat Back Jon Klassen", 0),
    ("u-wordless", "## Wordless Picture Books", 0),
    ("u-fig", "## The Sweetest Fig Chris Van Allsburg", 0),
    ("u-bootsie", "## Bootsie Barker Bites Barbara Bottner", 0),
    ("u-owi", "## O.W.I", 0),
    ("u-mintext", "## Inferring from Books with MINIMUM TEXT", 0),
    ("u-knuffle", "## Knuffle Bunny Mo Willems", 0),
    ("u-splendid", "## A Splendid Friend, Indeed Suzanne Bloom", 0),
    ("u-topcat", "## Top Cat Lois Ehlert", 0),
]

# (line, old, new) micro-edits, applied bottom-up
MICRO = [
    # Knuffle repair (source .doc verified): truncated prompt
    (2862, "What wo", "What would Trixie say if she could talk?"),
    # Knuffle full text -> subhead under the teaching unit
    (2864, "## Knuffle Bunny Mo Willems", "### Text: Knuffle Bunny"),
    # Mama blurb + full text -> blurb stays, text becomes subhead
    (2640, "## A Mama for Owen Marion Dane Bauer",
     "### Text: A Mama for Owen"),
    # OWI x4 -> one section, per-book subheads (keep images + tables)
    (2546, "## O.W.I", "### Tough Boris — Mem Fox"),
    (2535, "## O.W.I", "### Bootsie Barker Bites — Barbara Bottner"),
    (2523, "## O.W.I",
     "### The Mysteries of Harris Burdick — Chris Van Allsburg"),
    (2512, "## O.W.I\n\nBook: Owen & Mzee Author: Isabella Hatkoff",
     '## O.W.I\n\nObserve, Wonder, Infer — one chart per book.\n\n'
     '### Owen & Mzee — Isabella Hatkoff'),
    # Wordless book list -> subhead (routine section keeps its head)
    (1848, "## Wordless Picture Books", "### Wordless book list"),
    # It Says duplicate head -> worked + blank under one head
    (179, "## It Says – I Say – And So …\n\n**Reading Strategies:** Making "
          "Inferences, Making Connections,\nSynthesising",
     "### Blank table (copy for students)"),
]

CANDIDATES = {  # embedded section head line -> standalone mentor text
    405: "Granddaddy’s Gift — Margaree Mitchell.md",
    1019: "The Stranger — Chris Van Allsburg.md",
    1186: "Tight Times — Barbara Shook Hazen.md",
    1388: "Yo! Yes! — Chris Raschka.md",
    1496: "I Want My Hat Back — Jon Klassen.md",
    1599: "This Is Not My Hat — Jon Klassen.md",
    2221: "The Sweetest Fig — Chris Van Allsburg.md",
}


def section_spans(lines):
    heads = [i for i, l in enumerate(lines) if l.startswith("## ")]
    spans = {}
    for n, h in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        spans[h + 1] = (h, end)  # 1-based head line -> (start idx, end idx)
    return spans


def body_text(path):
    t = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n.*?\n---\n(.*)$", t, re.S)
    return m.group(1) if m else t


def main():
    raw = INF2.read_text(encoding="utf-8")
    lines = raw.splitlines()
    # snapshot ORIGINAL section texts for candidate analysis (line numbers
    # below refer to the pristine file; edits shift them afterwards)
    orig_spans = section_spans(lines)
    orig_heads = sorted(orig_spans)
    orig_text = "\n".join(lines)
    # sanity: expected heads present
    spans = section_spans(lines)
    for _anchor, head, _occ in ANCHORS:
        assert any(l == head for l in lines), f"head missing: {head}"
    for ln, _old, _new in MICRO:
        assert lines[ln - 1].strip().startswith(
            _old.strip().split("\n")[0][:20]), f"micro mismatch: {ln}"

    # apply micro-edits bottom-up (line numbers stay valid)
    for ln, old, new in sorted(MICRO, reverse=True):
        seg = "\n".join(lines[ln - 1:ln - 1 + old.count("\n") + 1])
        assert old in seg, f"micro context: {ln}"
        seg2 = seg.replace(old, new, 1)
        lines[ln - 1:ln - 1 + old.count("\n") + 1] = seg2.split("\n")

    # opening contents-dump (lines 14-86: after frontmatter/img, before
    # "## Teaching Inferring") -> intro + TOC. Locate robustly:
    idx_head = next(i for i, l in enumerate(lines)
                    if l.startswith("## Teaching Inferring"))
    # opening block = from first bold line to line before head
    idx_start = next(i for i, l in enumerate(lines)
                     if l.strip() == "**INFERRING**")
    opening = lines[idx_start:idx_head]
    assert any("Knuffle Bunny" in l for l in opening), "opening not found"
    # keep EVERY dump line: title block as-is, the rest becomes a real list
    glance = []
    for l in opening:
        s = l.strip()
        if not s or s.startswith("<img"):
            glance.append(l)
        elif s in ("**INFERRING**", "**PART 2**", "**Inferring 2**",
                   "Teaching inferring"):
            glance.append(l)
        elif s.startswith("- "):
            glance.append(l)
        else:
            glance.append("- " + s)
    block = (TOC + "\n### At a glance (Jim's contents)\n\n"
             + "\n".join(glance)).split("\n")
    lines[idx_start:idx_head] = block

    # anchors LAST: match by exact heading text, bottom-up.
    # Micro-edits above already de-duplicated repeated heads, so each
    # (heading, occurrence) below resolves to one line.
    used = set()
    for anchor, head, occ in ANCHORS:
        hits = [i for i, l in enumerate(lines) if l == head
                and i not in used]
        assert len(hits) > occ, f"anchor head missing: {head}"
        i = sorted(hits, reverse=True)[0] if occ == 0 and len(hits) > 1 \
            else hits[occ]
        # occ==0 with duplicates (Yo! Yes! transcript kept): take FIRST
        if len(hits) > 1 and occ == 0:
            i = min(hits)
        lines.insert(i, f'<a id="{anchor}"></a>')
        used.add(i + 1)

    INF2.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # word-diff: visible words before vs after (minus declared additions)
    def words(t):
        t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
        t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
        t = re.sub(r"<[^>]+>", " ", t)
        t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
        t = re.sub(r"[#>*`_\|\-]", " ", t)
        return re.findall(r"[A-Za-z'’\-]+", t.lower())
    before, after = words(raw), words("\n".join(lines))
    from collections import Counter
    cb, ca = Counter(before), Counter(after)
    removed = sum((cb - ca).values())
    added = sum((ca - cb).values())
    print(f"words before={len(before)} after={len(after)} "
          f"removed={removed} added={added} (TOC/intro/subheads)")
    print("removed words:", sorted((cb - ca).elements()))
    print("added words:", sorted((ca - cb).elements())[:40])

    # link-out candidates: overlap ORIGINAL embedded section vs standalone
    for ln, stand in sorted(CANDIDATES.items()):
        sfile = MENTORS / stand
        if not sfile.exists():
            print(f"candidate L{ln}: NO STANDALONE {stand}")
            continue
        h = max([x for x in orig_heads if x <= ln])
        s, e = orig_spans[h]
        emb = "\n".join(orig_text.splitlines()[s:e])
        st = body_text(sfile)
        ratio = difflib.SequenceMatcher(
            None, emb[:8000], st[:8000]).ratio()
        print(f"candidate L{ln} {stand}: overlap={ratio:.2f} "
              f"(embedded {e - s} lines)")


def open_head(lines, ln):
    return lines[ln - 1][3:].strip()[:12]


if __name__ == "__main__":
    main()
