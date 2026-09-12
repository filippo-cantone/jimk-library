#!/usr/bin/env python3
"""Apply the confident dedupe decisions from DEDUPE-REPORT.md. Run once."""
import subprocess, os, re, shutil

ROOT = "content"

def sh(*args):
    subprocess.run(args, check=True)

def swap_in_place(dirpath, winner, loser, target_title=None, note_source=None):
    """Keep `winner`'s content under the name `loser` currently has (the
    clean/canonical name), i.e. winner becomes <loser-name>.md, old loser is
    deleted. If winner == loser name already, just delete the other file
    (byte-identical case)."""
    wpath = f"{ROOT}/{dirpath}/{winner}.md"
    lpath = f"{ROOT}/{dirpath}/{loser}.md"
    wassets = f"{ROOT}/{dirpath}/assets/{winner}"
    lassets = f"{ROOT}/{dirpath}/assets/{loser}"

    if winner == loser:
        raise ValueError("winner == loser")

    # delete loser first (md + assets)
    sh("git", "rm", "-q", lpath)
    if os.path.isdir(lassets):
        sh("git", "rm", "-rq", lassets)

    # move winner .md to loser's name (the canonical name we're keeping)
    sh("git", "mv", wpath, lpath)
    # move winner assets to loser's asset-folder name, if present
    if os.path.isdir(wassets):
        sh("git", "mv", wassets, lassets)
        # fix internal refs
        text = open(lpath, encoding="utf-8").read()
        text = text.replace(f"assets/{winner}/", f"assets/{loser}/")
        open(lpath, "w", encoding="utf-8").write(text)

    # fix title + add dedupe note
    text = open(lpath, encoding="utf-8").read()
    m = re.search(r'^title:\s*"([^"]*)"', text, re.M)
    old_title = m.group(1) if m else None
    new_title = target_title or loser
    if old_title is not None:
        text = text.replace(f'title: "{old_title}"', f'title: "{new_title}"', 1)
    note = note_source or f"Retired near-duplicate {loser}.doc (see DEDUPE-REPORT.md, 2026-09-12)."
    text = text.replace(
        f'source_file:',
        f'dedupe_note: "{note}"\nsource_file:',
        1,
    )
    open(lpath, "w", encoding="utf-8").write(text)
    print(f"OK: {dirpath}/{loser}.md now holds {winner}'s content")


if __name__ == "__main__":
    # (dir, winner_file_stem, loser_file_stem_which_survives_as_the_name, title)
    jobs = [
        ("Author Studies Jim", "Eve Bunting2 (2)", "Eve Bunting2", "Eve Bunting2"),
        ("Author Studies Jim", "Eve Bunting (2)", "Eve Bunting", "Eve Bunting"),
        ("Author Studies Jim", "Judith Viorst (2)", "Judith Viorst", "Judith Viorst"),
        ("Author Studies Jim", "Margie Palatini (2)", "Margie Palatini", "Margie Palatini"),
        ("Author Studies Jim", "Patricia Polacco 2 (2)", "Patricia Polacco 2", "Patricia Polacco 2"),
        ("Author Studies Jim", "Patricia Polacco 3 (2)", "Patricia Polacco 3", "Patricia Polacco 3"),
    ]
    for dirpath, winner, loser, title in jobs:
        swap_in_place(dirpath, winner, loser, title)
