#!/usr/bin/env python3
"""Forbidden-pattern sweep for the v8 (main) / v7 (companion) synthesis round.

Pattern families per the merged synthesis implementation plan (Part 5.5):
meta-commentary / self-reference, changelog tense, previous-version
references, strawman negations, chat register, and the "Zai, A." author
hallucination guard.

Renders only body text (comments stripped) so tex header comments do not
trigger false positives.
"""
import re
import sys

PATTERNS = [
    # (label, regex, word-boundary?)
    ("strawman: not a smooth curvature", r"not a smooth curvature", False),
    ("strawman: not a smooth Hessian", r"not a smooth [Hh]essian", False),
    ("changelog: is now a theorem", r"is now a theorem", False),
    ("changelog: our previously", r"our previous(ly)?", False),
    ("changelog: previously explored", r"previously explored", False),
    ("changelog: is final for", r"is final for", False),
    ("changelog: What this closes", r"[Ww]hat this closes", False),
    ("meta: self-contained self-description",
     r"self-contained", False),
    ("meta: earlier drafts", r"earlier drafts?", False),
    ("meta: prior versions of this", r"prior versions? of this", False),
    ("meta: in this round/revision/pass",
     r"in this (round|revision|pass)", False),
    ("chat register: as requested", r"as requested", False),
    ("chat register: chat", r"\bchat\b", True),
    ("meta: the author's earlier", r"the author'?s earlier", False),
    ("homogenized", r"[Hh]omogenized", False),
    ("author guard: Zai", r"\bZai\b", True),
]


def strip_comments(tex: str) -> str:
    """Strip % comments (not \\%)."""
    out = []
    for line in tex.split("\n"):
        # find unescaped %
        m = re.search(r"(?<!\\)%", line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def sweep(path: str) -> int:
    tex = strip_comments(open(path).read())
    hits = 0
    for label, pat, wb in PATTERNS:
        regex = (r"\b" + pat + r"\b") if wb else pat
        found = re.findall(regex, tex)
        if found:
            hits += len(found)
            # locate line numbers for reporting
            for m in re.finditer(regex, tex):
                ln = tex[:m.start()].count("\n") + 1
                ctx = tex[max(0, m.start() - 60):m.end() + 60]
                ctx = " ".join(ctx.split())
                print(f"  [{path}] {label} @ line {ln}: ...{ctx}...")
    if hits == 0:
        print(f"  [{path}] clean ({len(PATTERNS)} patterns)")
    return hits


if __name__ == "__main__":
    total = 0
    for p in sys.argv[1:]:
        total += sweep(p)
    sys.exit(0 if total == 0 else 1)
