#!/usr/bin/env python3
"""Update the PDF rows in SUBMISSION_PACKAGE_LINKS.md to the v5/v4
files, prepending the v8 revision description to each stack (the
established newest-first convention)."""
import re

P = ("/home/z/my-project/metabolic-curvature-measure/download/"
     "SUBMISSION_PACKAGE_LINKS.md")
s = open(P).read()

# ---- main paper row: v4 -> v5 ----
old_main = ("| Manuscript PDF (28 pp, full proofs in appendices, "
            "declarations in backmatter, + v7 author-finalization")
new_main = ("| Manuscript PDF (27 pp, full proofs in appendices, "
            "declarations in backmatter, + v8 formal-tone and "
            "figure-repair revision: declarations rewritten as brief "
            "single sentences; meta-commentary, self-referential prose, "
            "and internal project jargon removed (proofs untouched at "
            "full length); all six figures regenerated without internal "
            "experiment codes, with the Fig 3 panel-(b) "
            "annotation-collision fix (prior versions retained as "
            "separate files: journal_manuscript_v4.pdf and earlier), "
            "+ v7 author-finalization")
assert old_main in s, "main row anchor not found"
s = s.replace(old_main, new_main, 1)
s = s.replace("download/journal_manuscript_v4.pdf)",
              "download/journal_manuscript_v5.pdf)")

# ---- companion row: v3 -> v4 ----
old_comp = ("| Manuscript PDF (74 pp, + author-finalization revision: "
            "Amin Abaee")
new_comp = ("| Manuscript PDF (74 pp, + v8 formal-tone revision: "
            "declarations rewritten as brief single sentences with the "
            "author-contribution placeholder replaced by A.A.; the "
            "Status note below the abstract removed; audit-diary and "
            "correction-history phrasing rewritten as scientific "
            "observation (proofs untouched at full length); prior "
            "version retained as companion_categorical_v3.pdf, "
            "+ author-finalization revision: Amin Abaee")
assert old_comp in s, "companion row anchor not found"
s = s.replace(old_comp, new_comp, 1)
# swap ONLY the two companion PDF link targets for the v4 row
s = s.replace(
    "[download/companion_categorical_v3.pdf]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v3.pdf) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "companion_categorical_v3.pdf) |",
    "[download/companion_categorical_v4.pdf]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v4.pdf) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "companion_categorical_v4.pdf) |", 1)

open(P, "w").write(s)
print("PDF rows updated to v5 / v4")
