#!/usr/bin/env python3
"""V20 round: create journal_manuscript_v20.tex (from v19; v19 and all
earlier versions untouched) -- the F1-F7 causal-coherence/prose-alignment
review findings applied as a light touch-up, plus the Discover Applied
Mathematics venue alignment.

Findings status on the v19 base (re-verified before this round):
- F1 (stale '98 checks'): ALREADY RESOLVED in v19 (Reproducibility says
  349; the count is refreshed to the v30 audit count below).
- F2: companion-side (handled by scripts/v13_companion_edits.py).
- F3 (indirect trajectory-independence inference): the direct statistic
  is now computed from the deposited per-gene artifacts
  (scripts/v20_f3_rank_stability.py ->
  download/deepseek_bridge/v20_path_rank_stability.json): Spearman
  rho(kappa_mu_P0, kappa_mu_P1) = 0.9176 -> +0.92 and
  rho(kappa_mu_P0, kappa_mu_P2) = 0.9551 -> +0.96 over the 424 genes
  nonzero on both paths. Reported in situ.
- F4 (GC-rate compression): the abstract site no longer exists; the
  intro site (line ~353) lacked the random-panels qualifier -- added,
  mirroring sec:e32's own two-regime statement.
- F5 ('invariant' for rho = 0.99998): three sites corrected -- the
  intro remark and sec v5 wordings, plus the Discussion's 'measured
  metric invariance' -> 'measured metric agreement' (the audit's
  V20-3 gate caught the third site).
- V20-9 (audit ledger): the two Reproducibility/protocols count
  mentions refreshed 349 -> 359 (the v30 ledger size).
- F6 (flat translation-buffering assertion): hedged at both remaining
  flat sites (abstract + intro) with 'consistent with'; the TITLE also
  asserted 'predicts ... translational buffering' while the body says
  'the translational-buffering model this paper tests' -- the title is
  narrowed to 'predicts transcriptional regulation' (the buffering
  dissociation remains a keyword-indexed, hedged finding).
- F7 ('per crossing' vs per-crossing-pair): MOOT -- the categorical
  subsection carrying that gloss was removed from the v19 body; no
  v19 site quotes the companion's pairs-crossing theorem.

Venue alignment (Discover Applied Mathematics, springer.com/journal/
44585, live-verified submission guidelines):
- natbib [round] (author-year) -> [numbers,sort&compress,square]
  (numeric citations in square brackets);
- caption labelsep period -> space with \figurename 'Fig.' ("Fig. 1"
  label style);
- abstract 245 words < 250 (the DAM cap is 'less than 250');
- reference list renamed journal_manuscript_v20_dam_refs.tex (entries
  byte-identical; the zai2026categorical cross-citation title aligned
  to the companion's actual title);
- journal_manuscript_v20_refs.bib: the underlying BibTeX database
  (same title alignment).

Every theorem, proof, number, section, and figure is unchanged.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(BASE, "scripts")

SRC = os.path.join(S, "journal_manuscript_v19.tex")
DST = os.path.join(S, "journal_manuscript_v20.tex")

text = open(SRC).read()
n_orig = len(text)

edits = []


def edit(old, new, label, count=1):
    global text
    found = text.count(old)
    assert found == count, f"{label}: expected {count} match(es), found {found}"
    text = text.replace(old, new)
    edits.append(label)


# ------------------------------------------------------------------
# 0. Header identity block + V20 round note
# ------------------------------------------------------------------
edit(
    "%  journal_manuscript_v19.tex -- main manuscript.\n"
    "%  Target journal: Bulletin of Mathematical Biology (Springer).\n"
    "%  Author-year citations (natbib); reference list in\n"
    "%  journal_manuscript_v19_bmb_refs.tex. Long technical proofs are\n",
    "%  journal_manuscript_v20.tex -- main manuscript.\n"
    "%  Target journal: Discover Applied Mathematics (Springer\n"
    "%  Nature, link.springer.com/journal/44585): Snapp submission,\n"
    "%  Research article, abstract < 250 words, numeric square-bracket\n"
    "%  citations, single-anonymous review, APC covered by the\n"
    "%  publisher through 2027.\n"
    "%  V20 round (v19 -> v20), a light touch-up: the causal-coherence\n"
    "%  and prose-alignment review findings applied -- F3 the direct\n"
    "%  trajectory rank correlation now reported (rho = +0.92 P1,\n"
    "%  +0.96 P2, 424 shared nonzero genes, from the deposited\n"
    "%  per-gene path artifacts); F4 the intro Glivenko--Cantelli\n"
    "%  sentence qualified 'across random panels (designed panels\n"
    "%  reproduce them exactly)'; F5 three near-identity wordings\n"
    "%  corrected to 'rank agreement' (intro remark), 'the two\n"
    "%  metrics agree to five decimals' (sec v5), and 'measured\n"
    "%  metric agreement' (Discussion), since rho = 0.99998 is\n"
    "%  agreement, not identity; F6 the translation-buffering\n"
    "%  mechanism asserted\n"
    "%  flatly at the abstract and intro now carries 'consistent\n"
    "%  with', and the title no longer asserts it as a prediction\n"
    "%  (the body calls it 'the translational-buffering model this\n"
    "%  paper tests'). F1 was already resolved in v19 (audit count\n"
    "%  text, refreshed here to the v30 count); F7 is moot (the\n"
    "%  v19 restructure removed the categorical subsection that\n"
    "%  carried the flagged gloss). Venue: numeric citations,\n"
    "%  Fig.-label captions, reference list in\n"
    "%  journal_manuscript_v20_dam_refs.tex. Long technical proofs are\n",
    "header identity + V20 round note")

# ------------------------------------------------------------------
# 1. Venue: numeric citations, Fig.-label captions
# ------------------------------------------------------------------
edit("\\usepackage[round]{natbib}",
     "\\usepackage[numbers,sort&compress,square]{natbib}",
     "natbib numeric square-bracket mode")
edit("\\usepackage[labelsep=period]{caption}",
     "\\usepackage[labelsep=space]{caption}",
     "caption labelsep space (DAM 'Fig. 1' label style)")
edit("\\renewcommand{\\figurename}{Fig}",
     "\\renewcommand{\\figurename}{Fig.}",
     "figurename 'Fig.' (DAM label form)")

# ------------------------------------------------------------------
# 2. Title accuracy (F6): the title asserts only what is measured
# ------------------------------------------------------------------
edit(
    " pdftitle={A discrete curvature measure for flux balance analysis\n"
    "           predicts transcriptional regulation and translational\n"
    "           buffering in Escherichia coli},",
    " pdftitle={A discrete curvature measure for flux balance analysis\n"
    "           predicts transcriptional regulation in Escherichia coli},",
    "pdftitle narrowed")
edit(
    "\\title{A discrete curvature measure for flux balance analysis\n"
    "       predicts transcriptional regulation and translational\n"
    "       buffering in \\emph{Escherichia coli}}",
    "\\title{A discrete curvature measure for flux balance analysis\n"
    "       predicts transcriptional regulation in \\emph{Escherichia coli}}",
    "title narrowed (translational buffering stays a hedged, "
    "keyword-indexed finding)")

# ------------------------------------------------------------------
# 3. F6a: abstract hedge
# ------------------------------------------------------------------
edit(
    "($r = -0.083$, $366$ genes, matched proteomics): cells transcribe\n"
    "standby capacity for rerouting while buffering translation.",
    "($r = -0.083$, $366$ genes, matched proteomics), consistent with\n"
    "cells transcribing standby capacity for rerouting while buffering\n"
    "translation.",
    "F6 abstract: 'consistent with' hedge")

# ------------------------------------------------------------------
# 4. F4: intro GC-rate sentence gains the two-regime qualifier
# ------------------------------------------------------------------
edit(
    "($r \\in [+0.386, +0.396]$), with the underlying event measures\n"
    "stabilizing at the Glivenko--Cantelli rate. The association vanishes",
    "($r \\in [+0.386, +0.396]$), with the underlying event measures\n"
    "stabilizing at the Glivenko--Cantelli rate across random panels\n"
    "(designed panels reproduce them exactly). The association vanishes",
    "F4 intro: random-panels qualifier")

# ------------------------------------------------------------------
# 5. F6b: intro hedge
# ------------------------------------------------------------------
edit(
    "quantitative proteomics): cells transcribe standby capacity for\n"
    "rerouting while buffering energy-intensive translation --- the\n"
    "translational-buffering model this paper tests.",
    "quantitative proteomics), consistent with cells transcribing\n"
    "standby capacity for rerouting while buffering energy-intensive\n"
    "translation --- the translational-buffering model this paper tests.",
    "F6 intro: 'consistent with' hedge")

# ------------------------------------------------------------------
# 6. F5a: 'rank identity' -> 'rank agreement' (intro remark)
# ------------------------------------------------------------------
edit(
    "measured, not assumed: the within-layer rank identity\n"
    "$\\rho(\\kmu, \\kk^{\\mathrm{lex}}) = 0.99998$",
    "measured, not assumed: the within-layer rank agreement\n"
    "$\\rho(\\kmu, \\kk^{\\mathrm{lex}}) = 0.99998$",
    "F5a: rank identity -> rank agreement")

# ------------------------------------------------------------------
# 7. F5b: 'metric invariance holds' -> 'agree to five decimals'
# ------------------------------------------------------------------
edit(
    "digit ($r = +0.3739$, $n = 433$), and metric invariance holds,\n"
    "$\\rho(\\kmu, \\kk^{\\mathrm{lex}}) = 0.99998$: both metrics sample the",
    "digit ($r = +0.3739$, $n = 433$), and the two metrics agree to\n"
    "five decimals, $\\rho(\\kmu, \\kk^{\\mathrm{lex}}) = 0.99998$: both\n"
    "metrics sample the",
    "F5b: metric invariance -> five-decimal agreement")

# ------------------------------------------------------------------
# 8. F3: report the DIRECT trajectory rank correlation
# ------------------------------------------------------------------
edit(
    "transcriptional regulation across multiple environments, and\n"
    "      the per-gene\n"
    "      ranking is largely trajectory-independent.",
    "transcriptional regulation across multiple environments, and\n"
    "      the per-gene\n"
    "      ranking is largely trajectory-independent: the direct rank\n"
    "      correlation between the path predictors and the\n"
    "      reference-path $\\kmu$ is $\\rho = +0.92$ (P1) and $+0.96$\n"
    "      (P2) over the $424$ genes nonzero on both paths.",
    "F3: direct rank correlation reported")

# ------------------------------------------------------------------
# 9b. F5c: Discussion site -- the third near-identity wording
# ------------------------------------------------------------------
edit(
    "flux-layer footing and complementing the measured metric invariance\n"
    "of \\S\\ref{sec:v5}",
    "flux-layer footing and complementing the measured metric agreement\n"
    "of \\S\\ref{sec:v5}",
    "F5c: Discussion 'measured metric invariance' -> 'measured metric "
    "agreement'")

# ------------------------------------------------------------------
# 9c. V20-9: audit-suite count refreshed to the v30 ledger (359)
# ------------------------------------------------------------------
edit(
    "numeric verification described under Reproducibility\n($349$ checks).",
    "numeric verification described under Reproducibility\n($359$ checks).",
    "audit count 349 -> 359 (Statistical protocols)")
edit(
    "An automated suite of $349$ numeric checks",
    "An automated suite of $359$ numeric checks",
    "audit count 349 -> 359 (Reproducibility)")

# ------------------------------------------------------------------
# 9. Refs input retarget
# ------------------------------------------------------------------
edit("\\input{journal_manuscript_v19_bmb_refs}",
     "\\input{journal_manuscript_v20_dam_refs}",
     "refs input retargeted")

with open(DST, "w") as f:
    f.write(text)

print(f"journal_manuscript_v20.tex written "
      f"({n_orig} -> {len(text)} bytes, {len(edits)} anchored edits):")
for e in edits:
    print("  -", e)

# ==================================================================
# Refs file: journal_manuscript_v20_dam_refs.tex
# (entries byte-identical; header note + zai2026categorical title
# aligned to the companion's actual title)
# ==================================================================
SRC_R = os.path.join(S, "journal_manuscript_v19_bmb_refs.tex")
DST_R = os.path.join(S, "journal_manuscript_v20_dam_refs.tex")
refs = open(SRC_R).read()

old_head = (
    "% journal_manuscript_v19_bmb_refs.tex -- references for the v19\n"
    "% comprehension-restructure round. Entries byte-identical to the v18\n"
    "% list (itself the v7 list, generated by scripts/build_bmb_refs.py):\n")
new_head = (
    "% journal_manuscript_v20_dam_refs.tex -- references for the v20\n"
    "% Discover Applied Mathematics round. Entries byte-identical to the\n"
    "% v19 list (itself the v7 list, generated by scripts/build_bmb_refs.py),\n"
    "% with one alignment fix: the zai2026categorical cross-citation now\n"
    "% carries the companion's actual title (was a descriptive stand-in);\n"
    "% natbib is now in numeric square-bracket mode, so the optional\n"
    "% entry labels are inert for citation rendering.\n")
assert refs.count(old_head) == 1, "refs header anchor"
refs = refs.replace(old_head, new_head)

old_zai = (
    "\\bibitem[Abaee(2026)]{zai2026categorical}\n"
    "Abaee A (2026) Stratified Connections, Optic Composition, and the Homotopy\n"
    "           Fixed-Point Extension: A Categorical Framework for\n"
    "           Viability-Weighted Curvature. Companion theory manuscript, in preparation.")
new_zai = (
    "\\bibitem[Abaee(2026)]{zai2026categorical}\n"
    "Abaee A (2026) A Geometric and Category-Theoretic Theory of Viability: How\n"
    "           Sequential Adaptations Induce Path-Dependent Risk.\n"
    "           Companion theory manuscript, in preparation.")
assert refs.count(old_zai) == 1, "zai2026categorical entry anchor"
refs = refs.replace(old_zai, new_zai)

with open(DST_R, "w") as f:
    f.write(refs)
print("\njournal_manuscript_v20_dam_refs.tex written "
      "(header note + cross-citation title aligned; entries otherwise "
      "byte-identical).")

# ==================================================================
# BibTeX database copy: journal_manuscript_v20_refs.bib
# ==================================================================
SRC_B = os.path.join(S, "journal_manuscript_v19_refs.bib")
DST_B = os.path.join(S, "journal_manuscript_v20_refs.bib")
bib = open(SRC_B).read()
old_b = (
    "@misc{zai2026categorical,\n"
    "  author = {Abaee, Amin},\n"
    "  title = {Stratified Connections, Optic Composition, and the Homotopy\n"
    "           Fixed-Point Extension: A Categorical Framework for\n"
    "           Viability-Weighted Curvature},")
new_b = (
    "@misc{zai2026categorical,\n"
    "  author = {Abaee, Amin},\n"
    "  title = {A Geometric and Category-Theoretic Theory of Viability: How\n"
    "           Sequential Adaptations Induce Path-Dependent Risk},")
assert bib.count(old_b) == 1, "bib zai anchor"
bib = bib.replace(old_b, new_b)
with open(DST_B, "w") as f:
    f.write(bib)
print("journal_manuscript_v20_refs.bib written (same title alignment).")
print("\nAll v20 main files created. v19 and all earlier versions untouched.")
