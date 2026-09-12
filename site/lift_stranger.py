#!/usr/bin/env python3
"""One-off lift: fill The Stranger stub from its INFERRING2 full text."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
src = (REPO / "content/Inferring Course JIM/INFERRING2 Jim.md"
       ).read_text(encoding="utf-8").splitlines()
story = src[1052:1146]  # 0-based: file lines 1053-1146
assert story[0].startswith("**It was the time of year"), story[0][:40]
assert story[-1].rstrip().endswith("**"), story[-1][-30:]
assert "See you next fall" in story[-1], story[-1][-40:]
out = []
for line in story:
    s = line.strip()
    if s.startswith("**") and s.endswith("**") and len(s) > 4:
        s = s[2:-2]
    out.append(s)
body = "\n".join(out)
stub_path = REPO / "content/Mentor Texts/The Stranger — Chris Van Allsburg.md"
stub = stub_path.read_text(encoding="utf-8").rstrip() + "\n"
stub_path.write_text(stub + "\n" + body + "\n", encoding="utf-8")
print("story lines:", len(out),
      "| words:", len(re.findall(r"[A-Za-z]+", body)))
