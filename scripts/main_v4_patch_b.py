#!/usr/bin/env python3
"""
Patch B on journal_manuscript_v4.tex (live head; frozen lineage untouched):
one Discussion sentence registering the companion's new viability-kernel
+ Poincare/averaging closures (T7b/T7c) in the division-of-labor list.
"""
import re

TEX = "journal_manuscript_v4.tex"


def flex_replace(text, anchor, replacement, label=""):
    words = anchor.split()
    pat = re.compile(r"\s+".join(re.escape(w) for w in words))
    matches = pat.findall(text)
    assert len(matches) == 1, (
        f"[{label}] expected 1 match, found {len(matches)}: {anchor[:80]}")
    print(f"  [{label}] applied")
    return pat.sub(lambda m: replacement, text, count=1)


src = open(TEX, encoding="utf-8").read()
n0 = len(src)

src = flex_replace(
    src,
    "strata, the optic-composition semantics with its contraction "
    "analysis, the filtered-colimit construction of autocatalytic sets, "
    "and the homotopy-type-theoretic extension --- is developed in full,",
    "strata, the optic-composition semantics with its contraction\n"
    "analysis, the filtered-colimit construction of autocatalytic sets,\n"
    "the viability-kernel reading of its dynamical closure test (a\n"
    "finite-time, feedback-certifying probe of kernel and capture-basin\n"
    "membership, with the Poincar\\'e/averaging analysis of its pathwise\n"
    "levels), and the homotopy-type-theoretic extension --- is developed\n"
    "in full,",
    label="B1 companion-list")

open(TEX, "w", encoding="utf-8").write(src)
print(f"{TEX}: {n0} -> {len(src)} chars")
print("PATCH B COMPLETE")
