#!/usr/bin/env python3
"""Audit all local href/src targets inside site/dist/. Exit 1 on breakage."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

D = Path(__file__).resolve().parent / "dist"
bad, checked = [], 0
for p in sorted(D.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'(?:href|src)="([^"]+)"', t):
        u = m.group(1).split("#")[0]
        if not u or u.startswith(("http", "data:", "javascript:")):
            continue
        checked += 1
        if not (p.parent / unquote(u)).exists():
            bad.append(f"{p.relative_to(D)} -> {u}")
print(f"pages={len(list(D.rglob('*.html')))} links={checked} broken={len(bad)}")
for b in bad[:20]:
    print("BROKEN:", b)
sys.exit(1 if bad else 0)
