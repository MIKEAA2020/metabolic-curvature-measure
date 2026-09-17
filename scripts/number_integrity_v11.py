#!/usr/bin/env python3
"""Number-integrity diff between v10 and v11 (main) / v8 and v9 (companion).

Extracts every numeric token from each file's comment-stripped body and
compares multisets. Any number present in the old but missing in the
new (or vice versa) is flagged for manual adjudication. Numbers that
moved between sections are fine (multiset comparison); changed digits
are NOT fine unless explained.
"""
import re
import sys
from collections import Counter

def strip_comments(tex: str) -> str:
    out = []
    for line in tex.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)

# numeric tokens: integers, decimals, scientific notation, also
# LaTeX-embedded like $1.6 \times 10^{4}$ -> capture components
NUM = re.compile(r"""
    (?<![\w\\])            # not preceded by word char or backslash
    [-+]?\d*\.?\d+(?:\^{-?\d+})?   # plain / decimal / 10^{-3}
    (?!e[+-])              # avoid splitting sci-notation (rare in tex)
""", re.VERBOSE)

def numbers(tex: str):
    return Counter(NUM.findall(strip_comments(tex)))

def compare(old_path, new_path, label):
    old = numbers(open(old_path).read())
    new = numbers(open(new_path).read())
    missing = old - new   # in old, gone in new  -> POTENTIAL LOSS
    added = new - old     # in new, not in old    -> POTENTIAL FABRICATION
    print(f"=== {label}: {old_path.split('/')[-1]} -> {new_path.split('/')[-1]} ===")
    print(f"  old tokens: {sum(old.values())}, new tokens: {sum(new.values())}")
    if missing:
        print(f"  MISSING IN NEW ({sum(missing.values())} occurrences):")
        for k, v in sorted(missing.items(), key=lambda x: -x[1]):
            print(f"    {k!r} x{v}")
    else:
        print("  MISSING IN NEW: none")
    if added:
        print(f"  ADDED IN NEW ({sum(added.values())} occurrences):")
        for k, v in sorted(added.items(), key=lambda x: -x[1]):
            print(f"    {k!r} x{v}")
    else:
        print("  ADDED IN NEW: none")
    print()

if __name__ == "__main__":
    base = "/home/z/my-project/metabolic-curvature-measure/scripts/"
    compare(base + "journal_manuscript_v10.tex",
            base + "journal_manuscript_v11.tex", "MAIN")
    compare(base + "companion_categorical_v8.tex",
            base + "companion_categorical_v9.tex", "COMPANION")
