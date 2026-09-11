#!/usr/bin/env python3
"""Jim K Teacher Knowledge Base — static site builder (Phase 3).

Reads content/**/*.md + symlinked/copied assets, writes a search-first
static site to site/dist/ (gitignored; built locally for preview and on
Cloudflare Pages via `pip install -r site/requirements.txt && python3 site/build.py --mode deploy`).

  preview (default): asset dirs are symlinked into dist (no disk duplication)
  deploy:           asset files are copied into dist (self-contained publish dir)

Layout of dist/:
  index.html          search-first library home + 8 shelf cards
  shelves/<id>.html   guided shelf page (groups + filters)
  notes/**/*.html     one page per note (mirrors content/ tree, slugified)
  search.json         client-side search index (504 entries)
  static/             styles.css + app.js (copied)
"""
import argparse
import html
import json
import os
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
SITE = REPO / "site"
DIST = SITE / "dist"

SHELVES = [
    ("reading", "Reading", ["reading"],
     "Comprehension strategies, questioning, critical literacy, reader's theatre, text structures."),
    ("writing", "Writing", ["writing", "writers-notebook", "writing-voice"],
     "Craft, conventions, writer's notebook and photo prompt sets."),
    ("genres", "Genres", ["genres"],
     "Folktales, persuasive, poetry, procedural, biography, memoir, information report…"),
    ("author-studies", "Author studies", ["author-studies"],
     "One section per author."),
    ("mentor-texts", "Mentor texts", ["mentor-texts"],
     "Complete books, poems and stories to show kids."),
    ("vocabulary", "Vocabulary", ["vocabulary"], "Word study course."),
    ("inferring", "Inferring", ["inferring"], "Inferring course."),
    ("first-20-days", "First 20 Days", ["first-20-days"],
     "First 20 days of literacy + launch guides."),
]
SHELF_OF = {s: sid for sid, _, strands, _ in SHELVES for s in strands}

KIND_LABEL = {"guide": "Guide", "demonstration-text": "Text",
              "mini-lesson": "Mini-lesson", "prompt-set": "Prompt set",
              "list": "List", "template": "Template"}

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])


def slug(seg: str) -> str:
    s = seg.lower().strip().replace("’", "").replace("'", "")
    s = re.sub(r"[\\s_]+", "-", s)
    s = re.sub(r"[^a-z0-9\-\.\(\)]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "note"


def parse_note(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError(f"no frontmatter: {path}")
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def as_list(v):
    if v is None:
        return []
    return list(v) if isinstance(v, list) else [v]


def clean_text(md_body: str) -> str:
    t = re.sub(r"<!--.*?-->", " ", md_body, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)          # md images
    t = re.sub(r"<img[^>]*>", " ", t)                    # raw imgs
    t = re.sub(r"[#>*`_\|\-]", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)       # links -> text
    return re.sub(r"\s+", " ", t).strip()


def render_body(md_body: str) -> str:
    MD.reset()
    out = MD.convert(md_body)
    # lazy-load every image (runtime perf; originals untouched)
    out = re.sub(r"<img(?![^>]*loading=)", "<img loading=\"lazy\" decoding=\"async\"",
                 out)
    return out


BASE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Jim K Library</title>
<link rel="stylesheet" href="{root}static/styles.css">
</head>
<body>
<header class="site-head"><div class="wrap">
<a class="brand" href="{root}index.html">Jim K Library<small>teacher knowledge base · internal use</small></a>
<nav class="nav">{nav}</nav>
</div></header>
<div class="wrap">
{body}
</div>
<footer class="site"><div class="wrap">Jim K teacher knowledge base — internal school use only. {count} notes.</div></footer>
{extra}
</body>
</html>"""


def page(title, body, depth, nav, total, extra=""):
    root = "../" * depth
    return BASE.format(title=html.escape(title), root=root, nav=nav,
                       body=body, count=total, extra=extra)


def nav_html(shelves, current=None, root=""):
    links = []
    for sid, label, _, _ in shelves:
        cls = ' class="on"' if sid == current else ""
        links.append(f'<a href="{root}shelves/{sid}.html"{cls}>{label}</a>')
    return "".join(links)


def build(mode: str):
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "notes").mkdir(parents=True)
    (DIST / "shelves").mkdir(parents=True)
    shutil.copytree(SITE / "static", DIST / "static")

    md_files = sorted(CONTENT.rglob("*.md"))
    notes = []          # dicts for index + shelf lists
    used = set()        # dist html paths taken (collision guard)

    for src in md_files:
        rel = src.relative_to(CONTENT)
        # mirror the source tree exactly (no slugifying): image srcs in the
        # markdown use original-case relative paths, so dist must match them
        out_rel = rel.parent / (src.stem + ".html")
        n = 2
        while str(out_rel) in used:  # same-name notes in one folder
            out_rel = rel.parent / (src.stem + f" ({n}).html")
            n += 1
        used.add(str(out_rel))

        fm, body = parse_note(src)
        strand = str(fm.get("strand", "")).strip()
        shelf = SHELF_OF.get(strand, "reading")
        title = str(fm.get("title") or src.stem)
        kind = str(fm.get("resource_type", "")).strip()
        genre = str(fm.get("genre", "") or "").strip()
        traits = [str(t) for t in as_list(fm.get("traits"))]
        years = [str(y) for y in as_list(fm.get("year"))]
        excerpt = clean_text(body)[:400]

        out_path = DIST / "notes" / out_rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        from urllib.parse import quote
        url = "notes/" + "/".join(quote(p) for p in out_rel.parts)
        notes.append({"t": title, "u": url, "shelf": shelf, "strand": strand,
                      "k": kind, "g": genre, "tr": traits,
                      "y": ",".join(years), "x": excerpt,
                      "src": str(src), "out": str(out_path)})

    # mirror non-markdown files (images etc.) into dist/notes tree
    linked, missing = 0, []
    for src in sorted(CONTENT.rglob("*")):
        if src.is_dir() or src.suffix.lower() == ".md":
            continue
        rel = src.relative_to(CONTENT)
        dest = DIST / "notes" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if mode == "deploy":
            shutil.copy2(src, dest)
        else:
            try:
                os.symlink(src, dest)
            except FileExistsError:
                pass
        linked += 1

    shelf_notes = {sid: [] for sid, _, _, _ in SHELVES}
    for n in notes:
        shelf_notes[n["shelf"]].append(n)
    for lst in shelf_notes.values():
        lst.sort(key=lambda n: n["t"].lower())

    # ---- note pages ----
    for n in notes:
        fm, body = parse_note(Path(n["src"]))
        depth = len(Path(n["out"]).relative_to(DIST / "notes").parts)
        nav = nav_html(SHELVES, root="../" * depth)
        chips = []
        for label in [n["shelf"], KIND_LABEL.get(n["k"], n["k"]), n["g"],
                      ("Year " + n["y"]) if n["y"] else ""]:
            if label:
                chips.append(f'<span class="chip">{html.escape(label)}</span>')
        for t in n["tr"]:
            chips.append(f'<span class="chip">{html.escape(t)}</span>')
        src_file = html.escape(str(fm.get("source_file") or fm.get("source") or ""))
        body_html = (
            f'<div class="crumb"><a href="{"../" * depth}index.html">Home</a> / '
            f'<a href="{"../" * depth}shelves/{n["shelf"]}.html">{n["shelf"]}</a></div>\n'
            f'<article class="note"><h1>{html.escape(n["t"])}</h1>\n'
            f'<div class="chips meta">{"".join(chips)}</div>\n'
            f'<div class="toolbar"><button class="btn" onclick="window.print()">Print this page</button></div>\n'
            f'<div class="body">\n{render_body(body)}\n</div>\n'
            f'<div class="src">Source: {src_file}</div></article>'
        )
        (Path(n["out"])).write_text(
            page(n["t"], body_html, depth, nav, len(notes)), encoding="utf-8")

    # ---- home ----
    sopts = "".join(f'<option value="{sid}">{label}</option>'
                    for sid, label, _, _ in SHELVES)
    cards = []
    for sid, label, _, desc in SHELVES:
        c = len(shelf_notes[sid])
        cards.append(
            f'<a class="shelf-card" href="shelves/{sid}.html"><h3>{label}</h3>'
            f'<p>{desc}</p><span class="n">{c} notes</span></a>')
    home_body = (
        '<section class="hero"><h1>Find a teaching idea</h1>\n'
        f'<p class="sub">{len(notes)} notes from Jim\u2019s archive — '
        "strategies, genre packs, author studies and books to show kids. "
        "Start typing, or browse a shelf.</p>\n"
        '<div class="searchbox"><input id="q" type="search" '
        'placeholder="Try \u2018inferring picture books\u2019 or \u2018QAR\u2019\u2026" '
        'autocomplete="off" aria-label="Search all notes"></div>\n'
        '<div class="filters">'
        f'<select id="f-shelf"><option value="">All shelves</option>{sopts}</select>'
        '<select id="f-kind"><option value="">All kinds</option>'
        '<option value="guide">Guide</option>'
        '<option value="demonstration-text">Text to show kids</option>'
        '<option value="mini-lesson">Mini-lesson</option>'
        '<option value="prompt-set">Prompt set</option>'
        '<option value="list">List</option>'
        '<option value="template">Template</option></select>'
        '<select id="f-genre"><option value="">All genres</option></select>'
        '<select id="f-year"><option value="">All years</option></select>'
        "</div>\n"
        '<div class="hint"><span id="count"></span> &nbsp;Type at least 2 letters. '
        "Results link straight to the note.</div>\n"
        '<ul id="results"></ul></section>\n'
        '<h2>Browse the shelves</h2>\n<section class="shelves">\n' +
        "\n".join(cards) + "\n</section>"
    )
    (DIST / "index.html").write_text(
        page("Home", home_body, 0, nav_html(SHELVES), len(notes),
             extra='<script src="static/app.js"></script>'),
        encoding="utf-8")

    # ---- shelf pages ----
    for sid, label, _, desc in SHELVES:
        lst = shelf_notes[sid]
        groups = {}
        for n in lst:
            groups.setdefault(n["k"] or "guide", []).append(n)
        order = ["guide", "demonstration-text", "mini-lesson",
                 "prompt-set", "list", "template"]
        glabel = {"guide": "Guides", "demonstration-text": "Texts to show kids",
                  "mini-lesson": "Mini-lessons", "prompt-set": "Prompt sets",
                  "list": "Lists", "template": "Templates"}
        sections = []
        for k in order + [g for g in groups if g not in order]:
            if k not in groups:
                continue
            items = "\n".join(
                f'<li><a href="../{n["u"]}">{html.escape(n["t"])}</a>'
                f'<div class="meta">{chips_html(chips_for(n))}</div></li>'
                for n in groups[k])
            sections.append(
                f'<h2 class="group-h">{glabel.get(k, k)} ({len(groups[k])})</h2>\n'
                f'<ul class="notelist">\n{items}\n</ul>')
        embedded = json.dumps(
            [{"t": n["t"], "u": "../" + n["u"], "s": n["strand"],
              "k": n["k"], "g": n["g"], "y": n["y"],
              "tr": n["tr"], "x": n["x"][:200]} for n in lst])
        shelf_body = (
            f'<div class="crumb"><a href="../index.html">Home</a> / {label}</div>\n'
            f"<h1>{label}</h1>\n<p class=\"sub\">{desc} ({len(lst)} notes)</p>\n"
            '<div class="searchbox"><input id="q2" type="search" '
            'placeholder="Filter on this shelf\u2026" autocomplete="off" '
            'aria-label="Filter shelf notes"></div>\n'
            '<div class="filters"><select id="f-kind">'
            '<option value="">All kinds</option>'
            + "".join(f'<option value="{k}">{glabel.get(k, k)}</option>'
                      for k in order if k in groups) + "</select></div>\n"
            '<ul class="notelist" id="shelf-results"></ul>\n'
            + "\n".join(sections)
            + f'\n<script>window.SHELF_NOTES = {embedded};</script>'
        )
        (DIST / "shelves" / f"{sid}.html").write_text(
            page(label, shelf_body, 1,
                 nav_html(SHELVES, sid, root="../"),
                 len(notes), extra='<script src="../static/app.js"></script>'),
            encoding="utf-8")

    # ---- search index ----
    index = [{"t": n["t"], "u": n["u"], "shelf": n["shelf"], "s": n["strand"],
              "k": n["k"], "g": n["g"], "tr": n["tr"], "y": n["y"],
              "x": n["x"]} for n in notes]
    (DIST / "search.json").write_text(json.dumps(index), encoding="utf-8")

    # ---- verify ----
    errors = []
    html_pages = list(DIST.rglob("*.html"))
    for n in notes:
        if not Path(n["out"]).exists():
            errors.append(f"missing page {n['u']}")
    # every note image src resolves inside dist
    img_srcs = set()
    for n in notes:
        text = Path(n["out"]).read_text(encoding="utf-8")
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', text):
            src = m.group(1)
            if src.startswith(("http", "data:")):
                continue
            img_srcs.add((n["u"], src, n["out"]))
    for page_u, src, out in img_srcs:
        if not (Path(out).parent / src).exists():
            # try URL-decoded variant (spaces)
            if not (Path(out).parent / src.replace("%20", " ")).exists():
                missing.append(f"{page_u} -> {src}")
    print(f"notes: {len(notes)}  pages: {len(html_pages)}  "
          f"assets linked: {linked}  img refs: {len(img_srcs)}")
    print(f"shelves: " + ", ".join(f"{sid}={len(shelf_notes[sid])}"
                                   for sid, _, _, _ in SHELVES))
    if errors or missing:
        print(f"ERRORS({len(errors)}):", errors[:10])
        print(f"BADIMG({len(missing)}):", missing[:15])
        return False
    print("verify: OK — all pages present, all image refs resolve")
    return True


def chips_html(items):
    return "".join(f'<span class="chip">{html.escape(x)}</span>'
                   for x in items if x)


def chips_for(n):
    out = []
    if n["g"]:
        out.append(n["g"])
    if n["y"]:
        out.append("Year " + n["y"])
    out.extend(n["tr"][:4])
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["preview", "deploy"], default="preview")
    args = ap.parse_args()
    ok = build(args.mode)
    sys.exit(0 if ok else 1)
