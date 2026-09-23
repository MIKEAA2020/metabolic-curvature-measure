#!/usr/bin/env python3
"""Update download/cover_letter_bmb.md for the v19 comprehension
restructure (BMB retarget): new title (2 sites), date, the companion
pointer rewritten for the removed categorical subsection, the audit
count 344 -> 349, and a restructure sentence in the opening.
The letter stays venue-clean (no mention of other journals)."""

P = ("/home/z/my-project/metabolic-curvature-measure/"
     "download/cover_letter_bmb.md")
txt = open(P).read()
applied = []


def rep(old, new, tag):
    global txt
    assert old in txt, f"ANCHOR NOT FOUND: {tag}"
    assert txt.count(old) == 1, f"ANCHOR NOT UNIQUE: {tag}"
    txt = txt.replace(old, new)
    applied.append(tag)


OLD_TITLE = ("A Geometric Theory of Metabolic Flux Rerouting: How Active-Set\n"
             "Curvature Predicts Transcriptional Regulation and Protein-Layer\n"
             "Buffering")
NEW_TITLE = ("A discrete curvature measure for flux balance analysis\n"
             "predicts transcriptional regulation and translational\n"
             "buffering in Escherichia coli")

# 1. title site 1 (header block, line-wrapped)
rep(OLD_TITLE + "\n\n---",
    NEW_TITLE + "\n\n---", "title site 1 (header)")

# 2. title site 2 (first paragraph)
rep('I am pleased to submit my manuscript "A Geometric Theory of Metabolic\n'
    'Flux Rerouting: How Active-Set Curvature Predicts Transcriptional\n'
    'Regulation and Protein-Layer Buffering" for consideration as an\n'
    'Original Research Article in the Bulletin of Mathematical Biology.',
    'I am pleased to submit my manuscript "A discrete curvature measure for\n'
    'flux balance analysis predicts transcriptional regulation and\n'
    'translational buffering in Escherichia coli" for consideration as an\n'
    'Original Research Article in the Bulletin of Mathematical Biology.',
    "title site 2 (opening paragraph)")

# 3. date
rep("**Date:** September 21, 2026", "**Date:** September 23, 2026",
    "date")

# 4. restructure sentence after the opening
rep("consideration as an\nOriginal Research Article in the Bulletin of "
    "Mathematical Biology.\n\nParametric flux balance "
    "analysis defines a piecewise-affine map from",
    "consideration as an\nOriginal Research Article in the "
    "Bulletin of Mathematical\nBiology.\n\nThe manuscript is written so "
    "that the biological line of argument leads:\nthe question, the "
    "measure, the validation, and the empirical association, with\nthe "
    "refinement theory and all proofs collected in appendices.\n\n"
    "Parametric flux balance analysis defines a piecewise-affine map from",
    "opening: structure-of-the-paper sentence")

# 5. companion bullet: the categorical subsection is no longer in the
#    main paper
rep("It is self-contained: all theorems it uses are proved in\n"
    "  its own appendices, and no empirical claim depends on the "
    "companion.\n"
    "  It carries only a brief, adapted summary of the categorical "
    "reading\n"
    "  that motivated the active-set curvature interpretation (its "
    "\u00a72.5),\n"
    "  with explicit pointers to the companion for the constructions "
    "and\n"
    "  proofs.",
    "It is self-contained: all theorems it uses are proved in\n"
    "  its own appendices, and no empirical claim depends on the "
    "companion.\n"
    "  It is written in measure-theoretic terms alone; one paragraph "
    "of the\n"
    "  Discussion points to the companion for the categorical "
    "constructions\n"
    "  and proofs.",
    "companion bullet: categorical subsection removed")

# 6. audit count
rep("verified by a 344-check numeric audit (344/344 PASS) that",
    "verified by a 349-check numeric audit (349/349 PASS) that",
    "audit count 344 -> 349")

open(P, "w").write(txt)
print("applied:", len(applied), "edits")
for t in applied:
    print("  -", t)
