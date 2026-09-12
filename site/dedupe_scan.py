#!/usr/bin/env python3
"""
Duplicate / near-duplicate detection pass over content/**/*.md.

Two passes:
  1. Exact-duplicate: hash of normalized body text (frontmatter + image refs
     + markdown punctuation stripped). Catches byte-for-byte-equivalent
     re-conversions.
  2. Near-duplicate / containment: 8-word shingles, inverted index to find
     candidate pairs (files sharing shingles), then exact Jaccard +
     containment computed only for those candidates. Catches:
       - two OCR/pandoc passes of the same source (Jaccard high, sizes similar)
       - a small lifted text fully contained in a bigger compiled pack
         (containment high even though Jaccard is low, because the pack is
         much bigger than the lift)

Output: printed report, ranked by containment then Jaccard, plus a JSON dump
for follow-up. Read-only — does not touch content/.
"""
import glob, hashlib, json, re, sys
from collections import defaultdict

ROOT = "content"
SHINGLE_K = 8          # words per shingle
MAX_FILES_PER_SHINGLE = 20   # generic/boilerplate shingle -> skip as candidate source
JACCARD_MIN_REPORT = 0.10
CONTAINMENT_MIN_REPORT = 0.60

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
IMG_RE = re.compile(r"<img[^>]*>|!\[[^\]]*\]\([^)]*\)")
PAGE_MARK_RE = re.compile(r"<!--.*?-->", re.S)
NONWORD_RE = re.compile(r"[^a-z0-9']+")

def normalize(text):
    text = FRONTMATTER_RE.sub("", text, count=1)
    text = IMG_RE.sub(" ", text)
    text = PAGE_MARK_RE.sub(" ", text)
    text = text.lower()
    text = NONWORD_RE.sub(" ", text)
    return text.split()

def shingles(words, k=SHINGLE_K):
    if len(words) < k:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i+k]) for i in range(len(words) - k + 1)}

def main():
    files = sorted(glob.glob(f"{ROOT}/**/*.md", recursive=True))
    docs = {}  # path -> {words, shingle_set, norm_hash}
    print(f"Loading {len(files)} files...", file=sys.stderr)
    for f in files:
        raw = open(f, encoding="utf-8", errors="replace").read()
        words = normalize(raw)
        sh = shingles(words)
        norm_hash = hashlib.sha256(" ".join(words).encode()).hexdigest()
        docs[f] = {"words": len(words), "shingles": sh, "hash": norm_hash}

    # --- Pass 1: exact duplicates ---
    by_hash = defaultdict(list)
    for f, d in docs.items():
        by_hash[d["hash"]].append(f)
    exact_groups = [v for v in by_hash.values() if len(v) > 1]

    # --- Pass 2: candidate pairs via inverted shingle index ---
    print("Building shingle index...", file=sys.stderr)
    index = defaultdict(list)
    for f, d in docs.items():
        for s in d["shingles"]:
            index[s].append(f)

    candidate_pairs = set()
    skipped_generic = 0
    for s, flist in index.items():
        if len(flist) < 2:
            continue
        if len(flist) > MAX_FILES_PER_SHINGLE:
            skipped_generic += 1
            continue
        flist = sorted(set(flist))
        for i in range(len(flist)):
            for j in range(i + 1, len(flist)):
                candidate_pairs.add((flist[i], flist[j]))

    print(f"{len(candidate_pairs)} candidate pairs "
          f"({skipped_generic} generic shingles skipped)", file=sys.stderr)

    results = []
    for a, b in candidate_pairs:
        sa, sb = docs[a]["shingles"], docs[b]["shingles"]
        if not sa or not sb:
            continue
        inter = len(sa & sb)
        union = len(sa | sb)
        jaccard = inter / union if union else 0
        containment = inter / min(len(sa), len(sb))
        if jaccard >= JACCARD_MIN_REPORT or containment >= CONTAINMENT_MIN_REPORT:
            results.append({
                "a": a, "b": b,
                "words_a": docs[a]["words"], "words_b": docs[b]["words"],
                "jaccard": round(jaccard, 3),
                "containment": round(containment, 3),
            })

    results.sort(key=lambda r: (-r["containment"], -r["jaccard"]))

    print("\n" + "=" * 70)
    print(f"EXACT DUPLICATES (identical normalized text): {len(exact_groups)} group(s)")
    print("=" * 70)
    for g in exact_groups:
        print("  = " + "  ==  ".join(g))

    print("\n" + "=" * 70)
    print(f"NEAR-DUPLICATE / CONTAINMENT CANDIDATES: {len(results)} pair(s)")
    print(f"(jaccard >= {JACCARD_MIN_REPORT} or containment >= {CONTAINMENT_MIN_REPORT})")
    print("=" * 70)
    for r in results:
        print(f"\n  jaccard={r['jaccard']:.2f}  containment={r['containment']:.2f}  "
              f"({r['words_a']}w vs {r['words_b']}w)")
        print(f"    A: {r['a']}")
        print(f"    B: {r['b']}")

    json.dump({"exact_groups": exact_groups, "near_dupes": results},
               open("site/dedupe_report.json", "w"), indent=2)
    print(f"\nFull JSON written to site/dedupe_report.json", file=sys.stderr)

if __name__ == "__main__":
    main()
