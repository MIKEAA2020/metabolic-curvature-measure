#!/usr/bin/env python3
"""Retarget both DAM cover letters to the V22/V15 Zenodo-archive round
(v27 packages): file pointers v21 -> v22 / v14 -> v15, audit counts
366 -> 372, and the Zenodo archival DOIs added to the data-availability
disclosures. Anchored, count-asserted edits.
"""
import os

DL = "/home/z/my-project/metabolic-curvature-measure/download"

# ------------------------------------------------------------------
# Main cover letter
# ------------------------------------------------------------------
p1 = os.path.join(DL, "cover_letter_dam.md")
t = open(p1, encoding="utf-8").read()

EDITS1 = [
    ("`scripts/companion_categorical_v14.tex`, compiled PDF included) and",
     "`scripts/companion_categorical_v15.tex`, compiled PDF included) and"),
    ("verified by a 366-check numeric audit (366/366 PASS) that",
     "verified by a 372-check numeric audit (372/372 PASS) that"),
    ("- Data availability: all data and code public; complete bundle at\n"
     "  https://github.com/MIKEAA2020/metabolic-curvature-measure (SHA-256\n"
     "  manifest included); companion theory manuscript available at the\n"
     "  same repository and on request.",
     "- Data availability: all data and code public; complete bundle at\n"
     "  https://github.com/MIKEAA2020/metabolic-curvature-measure (SHA-256\n"
     "  manifest included); this submission package is archived on Zenodo\n"
     "  at DOI 10.5281/zenodo.22941018 (CC-BY 4.0); companion theory\n"
     "  manuscript available at the same repository and on request."),
]
for i, (old, new) in enumerate(EDITS1, 1):
    n = t.count(old)
    assert n == 1, f"letter-1 edit {i}: expected 1, found {n}"
    t = t.replace(old, new)
open(p1, "w", encoding="utf-8").write(t)
print("cover_letter_dam.md retargeted (3 edits).")

# ------------------------------------------------------------------
# Companion cover letter
# ------------------------------------------------------------------
p2 = os.path.join(DL, "cover_letter_dam_companion.md")
t = open(p2, encoding="utf-8").read()

EDITS2 = [
    ("`scripts/journal_manuscript_v21.tex`, compiled PDF included) and will",
     "`scripts/journal_manuscript_v22.tex`, compiled PDF included) and will"),
    ("from deposited artifacts, re-verified by a 366-check numeric audit\n"
     "covering both manuscripts (366/366 PASS). All code is publicly\n"
     "available at the repository above.",
     "from deposited artifacts, re-verified by a 372-check numeric audit\n"
     "covering both manuscripts (372/372 PASS). All code is publicly\n"
     "available at the repository above, and this submission package is\n"
     "archived on Zenodo at DOI 10.5281/zenodo.22940820 (CC-BY 4.0)."),
]
for i, (old, new) in enumerate(EDITS2, 1):
    n = t.count(old)
    assert n == 1, f"letter-2 edit {i}: expected 1, found {n}"
    t = t.replace(old, new)
open(p2, "w", encoding="utf-8").write(t)
print("cover_letter_dam_companion.md retargeted (2 edits).")

# no stale tokens left
for p in (p1, p2):
    s = open(p, encoding="utf-8").read()
    assert "366/366" not in s and "366-check" not in s, f"stale count in {p}"
    assert "companion_categorical_v14" not in s and \
        "journal_manuscript_v21" not in s, f"stale file pointer in {p}"
print("No stale count/file-pointer tokens remain in either letter.")
