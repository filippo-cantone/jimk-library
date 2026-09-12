#!/usr/bin/env python3
"""
Phase D generator (SYSTEM-SPEC.md ss5) -- reads entities/ and renders pages.
This is the seed of the real generator, built out for the Inferring pilot
batch (5 books + 1 strategy hub + 1 novel-study page). Extend as more
strategies are built; don't rewrite from scratch.

Usage: python3 site/entity_build.py [--out DIR]
"""
import argparse, glob, html, os, re, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTITIES = os.path.join(ROOT, "entities")
CONTENT = os.path.join(ROOT, "content")


def load_mentor_text_body(rel_path):
    """Strip frontmatter + image tags, return paragraphs as simple HTML."""
    path = os.path.join(CONTENT, rel_path)
    if not os.path.exists(path):
        return None
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"^---\n.*?\n---\n", "", t, count=1, flags=re.S)
    t = re.sub(r"<img[^>]*/?>", "", t)
    t = re.sub(r"^#\s.*$", "", t, count=1, flags=re.M)  # drop the H1 title line
    paras = [p.strip() for p in t.split("\n\n") if p.strip()]
    return "\n".join(f"    <p>{html.escape(p)}</p>" for p in paras)


def load_all(kind):
    out = {}
    for f in sorted(glob.glob(os.path.join(ENTITIES, kind, "*.yaml"))):
        d = yaml.safe_load(open(f, encoding="utf-8"))
        out[d["slug"]] = d
    return out


def e(s):
    return html.escape(s or "", quote=True)


PAGE_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Source+Sans+3:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_path}styles.css">
</head>
<body>
<div class="wrap">
"""
PAGE_TAIL = """</div>
<script>
  const tabs = document.querySelectorAll('.tab');
  tabs.forEach(t => t.addEventListener('click', () => {{
    tabs.forEach(o => o.setAttribute('aria-selected', 'false'));
    document.querySelectorAll('.panel').forEach(p => p.hidden = true);
    t.setAttribute('aria-selected', 'true');
    document.getElementById(t.getAttribute('aria-controls')).hidden = false;
  }}));
</script>
</body>
</html>
"""

KIND_LABEL = {
    "strategy-hub": "Strategy hub",
    "reference-list": "Reference list",
    "author": "Author",
    "genre": "Genre",
    "getting-started": "Getting started",
}


def render_also_appears(entries, prefix):
    if not entries:
        return ""
    cards = []
    for it in entries:
        kind = KIND_LABEL.get(it["kind"], it["kind"])
        target = it["target"]
        href = "#"
        if target.startswith("strategy:"):
            href = f"{prefix}strategies/{target.split(':',1)[1]}.html"
        elif target.startswith("author:"):
            href = f"{prefix}authors/{target.split(':',1)[1]}.html"
        elif target.startswith("genre:"):
            href = "#"  # genre hubs not built this pilot
        cards.append(f"""      <div class="used-card">
        <div class="kind">{e(kind)}</div>
        <div class="name"><a href="{e(href)}">{e(it['label'])}</a></div>
      </div>""")
    return f"""
  <div class="panel" id="panel-used" role="tabpanel" hidden>
    <h2>Also appears in</h2>
    <div class="dek">Every hub, list, and mention that points back to this book — not full content, just where else to find it</div>
    <div class="usedgrid">
{chr(10).join(cards)}
    </div>
  </div>"""


def render_lesson_fragment(frag, book):
    body = ""
    if frag.get("blurb"):
        body += f'    <p class="lede">{e(frag["blurb"])}</p>\n'
    if frag.get("lede"):
        body += f'    <p class="lede">{e(frag["lede"])}</p>\n'

    if frag.get("formula"):
        f = frag["formula"]
        body += f"""    <div class="formula-box">
      <div class="formula-eq">{e(f['equation'])}</div>
      <p>{e(f['note'])}</p>
    </div>
"""

    if frag.get("stages"):
        for stage in frag["stages"]:
            items = "".join(f"      <li>{e(it)}</li>\n" for it in stage["items"])
            body += f"""    <div class="stage">
      <div class="stage-label">{e(stage['label'])}</div>
      <ul class="stage-items">
{items}      </ul>
    </div>
"""

    if frag.get("steps"):
        for term, desc in frag["steps"]:
            body += f"""    <div class="stepline">
      <div class="term">{e(term.upper())}</div>
      <div class="desc">{e(desc)}</div>
    </div>
"""
    if frag.get("chart_columns"):
        cols = "".join(f"<th>{e(c)}</th>" for c in frag["chart_columns"])
        rows_data = frag.get("chart_rows") or [[""] * len(frag["chart_columns"])]
        rows_html = "".join(
            "<tr>" + "".join(f"<td>{e(cell)}</td>" for cell in row) + "</tr>"
            for row in rows_data
        )
        row_note = f'<p class="note-inline">{e(frag["chart_note"])}</p>' if frag.get("chart_note") else ""
        body += f"""    <table class="chart"><thead><tr>{cols}</tr></thead>
    <tbody>{rows_html}</tbody></table>
    {row_note}
"""
    if frag.get("note"):
        body += f'    <p class="note-inline">{e(frag["note"])}</p>\n'

    if frag.get("pairs"):
        for quote, q in frag["pairs"]:
            body += f"""    <div class="infer-prompt">
      <b>Inferring prompt</b>
      <i>“{e(quote)}”</i> — {e(q)}
    </div>
"""
    if frag.get("infer_prompt"):
        body += f"""    <div class="infer-prompt">
      <b>Stop &amp; infer</b>
      {frag['infer_prompt']}
    </div>
"""
    if frag.get("quote"):
        body += f'    <blockquote>&ldquo;{frag["quote"]}&rdquo;</blockquote>\n'

    also_found = ""
    if frag.get("also_found_in"):
        also_found = f'<span class="merged-note">identical text also found in {len(frag["also_found_in"])} other pack(s) — merged here</span>'

    citation = f"""    <div class="citation">
      <span>From {e(frag['source_file'])}, lines {e(frag['source_lines'])}</span>
      {also_found}
    </div>
"""
    return f"""
  <div class="panel" id="panel-{frag['strategy']}" role="tabpanel">
    <h2>{e(frag['title'])}</h2>
    <div class="dek">{e(frag.get('dek',''))}</div>
{body}{citation}  </div>"""


def render_book(book, out_dir, css_path):
    title = book["title"]
    author = book.get("author") or "Unknown"
    tags = []
    for s in book.get("strategies", []):
        tags.append(f'<span class="tag strategy">used for &middot; {e(s)}</span>')
    if book.get("genre"):
        tags.append(f'<span class="tag genre">genre &middot; {e(book["genre"])}</span>')

    frags = book.get("fragments", [])
    tab_btns = []
    panels = []
    for i, frag in enumerate(frags):
        sel = "true" if i == 0 else "false"
        tab_btns.append(f'<button class="tab" role="tab" aria-selected="{sel}" aria-controls="panel-{frag["strategy"]}">{e(frag["title"].split(":")[0])}</button>')
        panels.append(render_lesson_fragment(frag, book))

    if book.get("mentor_text"):
        mt_path = book["mentor_text"]
        mt_slug = "mentor-text"
        body = load_mentor_text_body(mt_path)
        tab_btns.append(f'<button class="tab" role="tab" aria-selected="false" aria-controls="panel-{mt_slug}">Full text</button>')
        if body:
            panels.append(f"""
  <div class="panel" id="panel-{mt_slug}" role="tabpanel" hidden>
    <h2>Full text</h2>
    <div class="dek">Complete lifted text, kept as Jim recorded it</div>
{body}
    <div class="citation"><span>From {e(mt_path)}</span></div>
  </div>""")
        else:
            panels.append(f"""
  <div class="panel" id="panel-{mt_slug}" role="tabpanel" hidden>
    <h2>Full text</h2>
    <p class="note-inline">Could not load <code>{e(mt_path)}</code> — check the path.</p>
  </div>""")
    else:
        panels.append("""
  <div class="panel-note">No standalone mentor-text lift exists yet for this book — honest gap, not hidden.</div>""")

    also_count = len(book.get("also_appears_in", []))
    tab_btns.append(f'<button class="tab" role="tab" aria-selected="false" aria-controls="panel-used">Also appears in <span class="count">({also_count})</span></button>')
    panels.append(render_also_appears(book.get("also_appears_in", []), css_path))

    # fix first panel to be visible, others hidden
    panels_html = []
    for i, p in enumerate(panels):
        if i == 0:
            panels_html.append(p)
        else:
            panels_html.append(p.replace('role="tabpanel">', 'role="tabpanel" hidden>', 1) if 'hidden' not in p else p)

    content = f"""  <div class="crumb"><a href="{css_path}strategies/inferring.html">Inferring</a> / {e(title)}</div>

  <div class="card-header">
    <div class="kicker">Book</div>
    <h1>{e(title)}</h1>
    <div class="byline">by <b>{e(author)}</b></div>
    <div class="tagrow">{''.join(tags)}</div>
  </div>

  <div class="tabs" role="tablist">
    {chr(10).join('    ' + t for t in tab_btns)}
  </div>
{''.join(panels_html)}
"""
    html_out = PAGE_HEAD.format(title=e(title), css_path=css_path) + content + PAGE_TAIL
    path = os.path.join(out_dir, "books", f"{book['slug']}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html_out)
    return path


def render_strategy(strat, books, novel_studies, out_dir, css_path):
    routine_html = []
    for r in strat["routines"]:
        we = r["worked_example"]
        if we.get("book_slug") and we["book_slug"] in books:
            link = f'<a href="{css_path}books/{we["book_slug"]}.html">{e(we["label"])}</a>'
        else:
            link = f'{e(we["label"])} <span class="note-inline">{e(r.get("note", ""))}</span>'
        attribution = f'<p class="note-inline">{e(r["attribution"])}</p>' if r.get("attribution") else ""
        routine_html.append(f"""    <div class="stepline">
      <div class="term">{e(r['name'].upper())}</div>
      <div class="desc">{e(r['description'])}{attribution}<br><span class="worked">Worked example: {link}</span></div>
    </div>""")

    # ---- Section 1: Why teach it ----
    def_html = "".join(
        f'    <blockquote>&ldquo;{e(d["quote"])}&rdquo;<span class="attrib">— {e(d["source"])}</span></blockquote>\n'
        for d in strat.get("definitions", [])
    )
    why_html = "".join(f'      <li>{e(p)}</li>\n' for p in strat.get("why_points", []))

    # ---- Section 2: How to teach it ----
    dq_html = "".join(f"""    <div class="stepline">
      <div class="term">{e(dq['q'].upper())}</div>
      <div class="desc">{e(dq['note'])}</div>
    </div>""" for dq in strat.get("discussion_questions", []))

    release_html = "".join(f"""    <div class="stepline">
      <div class="term">{e(rs['stage'].upper())}</div>
      <div class="desc">{e(rs['note'])}</div>
    </div>""" for rs in strat.get("release_stages", []))

    wg = strat.get("worked_goldilocks")
    goldilocks_html = ""
    if wg:
        rows = "".join(f"<li>{e(ev)}</li>" for ev in wg["evidence"])
        goldilocks_html = f"""    <table class="chart"><thead><tr><th>Inference</th><th>Evidence</th></tr></thead>
    <tbody><tr><td>{e(wg['inference'])}</td><td><ul style="margin:0;padding-left:16px;">{rows}</ul></td></tr></tbody></table>
    <p class="note-inline">Worked example using a familiar story — inferring is easier to model with a story everyone already knows.</p>
"""

    book_cards = []
    for slug in strat["books"]:
        b = books[slug]
        book_cards.append(f"""    <div class="used-card">
      <div class="kind">Book</div>
      <div class="name"><a href="{css_path}books/{slug}.html">{e(b['title'])}</a></div>
      <div class="desc">{e(b.get('author') or '')}</div>
    </div>""")

    novel_cards = []
    for slug in strat.get("novel_studies", []):
        ns = novel_studies[slug]
        novel_cards.append(f"""    <div class="used-card">
      <div class="kind">Novel study</div>
      <div class="name"><a href="{css_path}novel-studies/{slug}.html">{e(ns['title'])}</a></div>
      <div class="desc">{e(ns.get('author') or '')} — inferring-relevant sections only</div>
    </div>""")

    content = f"""  <div class="crumb">Reading strategies / Inferring</div>

  <div class="card-header">
    <div class="kicker">Reading strategy</div>
    <h1>{e(strat['name'])}</h1>
    <div class="byline">{e(strat['lede'])}</div>
  </div>

  <h2 class="section-h"><span class="section-n">1</span>Why teach it</h2>
{def_html}
  <ul class="why-list">
{why_html}  </ul>
  <p class="note-inline">{e(strat.get('why_source',''))}</p>

  <h2 class="section-h"><span class="section-n">2</span>How to teach it</h2>
  <div class="subhead">Discussion questions, to ask about any inference a student makes</div>
{dq_html}
  <p class="note-inline">{e(strat.get('discussion_source',''))}</p>

  <div class="subhead" style="margin-top:18px;">Gradual release</div>
{release_html}

  <div class="subhead" style="margin-top:18px;">Worked example — a familiar story</div>
{goldilocks_html}

  <h2 class="section-h"><span class="section-n">3</span>Routines</h2>
{chr(10).join(routine_html)}

  <h2 class="section-h"><span class="section-n">4</span>Books with an Inferring lesson</h2>
  <div class="usedgrid">
{chr(10).join(book_cards)}
{chr(10).join(novel_cards)}
  </div>

  <div class="designnote">{e(strat['pilot_note'])}</div>
  <p class="note-inline">{e(strat.get('source_note',''))}</p>
"""
    html_out = PAGE_HEAD.format(title=e(strat["name"]), css_path=css_path) + content + PAGE_TAIL
    path = os.path.join(out_dir, "strategies", f"{strat['slug']}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html_out)
    return path


def render_novel_study(ns, out_dir, css_path):
    sections = []
    for s in ns["inferring_sections"]:
        body = f'    <p>{e(s["description"])}</p>\n'
        if s.get("example"):
            body += f'    <blockquote>{e(s["example"])}</blockquote>\n'
        if s.get("questions"):
            body += "    <ul>\n" + "".join(f"      <li>{e(q)}</li>\n" for q in s["questions"]) + "    </ul>\n"
        body += f'    <div class="citation"><span>Source lines: {e(s["source_lines"])}</span></div>\n'
        sections.append(f"""  <div class="panel" style="margin-bottom:16px;">
    <h2>{e(s['title'])}</h2>
{body}  </div>""")

    content = f"""  <div class="crumb"><a href="{css_path}strategies/inferring.html">Inferring</a> / {e(ns['title'])}</div>

  <div class="card-header">
    <div class="kicker">Novel study — inferring sections only</div>
    <h1>{e(ns['title'])}</h1>
    <div class="byline">by <b>{e(ns['author'])}</b></div>
  </div>

  <p class="note-inline">{e(ns['note'])}</p>

{''.join(sections)}
"""
    html_out = PAGE_HEAD.format(title=e(ns["title"]), css_path=css_path) + content + PAGE_TAIL
    path = os.path.join(out_dir, "novel-studies", f"{ns['slug']}.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html_out)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "site", "dist-pilot"))
    args = ap.parse_args()

    books = load_all("books")
    strategies = load_all("strategies")
    novel_studies = load_all("novel-studies")

    for slug, b in books.items():
        p = render_book(b, args.out, "../")
        print("book:", p)
    for slug, s in strategies.items():
        p = render_strategy(s, books, novel_studies, args.out, "../")
        print("strategy:", p)
    for slug, n in novel_studies.items():
        p = render_novel_study(n, args.out, "../")
        print("novel-study:", p)


if __name__ == "__main__":
    main()
