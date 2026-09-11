#!/usr/bin/env python3
"""Print section spans (## headings with line counts) for a markdown file."""
import sys

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().splitlines()
heads = [(i + 1, l[3:].strip()[:60]) for i, l in enumerate(lines)
         if l.startswith("## ")]
for n in range(len(heads)):
    s = heads[n][0]
    e = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
    print(f"{s:5} +{e - s:<4} {heads[n][1]}")
