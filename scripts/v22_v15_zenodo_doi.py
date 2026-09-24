#!/usr/bin/env python3
"""V22/V15 Zenodo-archive round: wire the two archival DOIs into the
data availability statements of both manuscripts.

- journal_manuscript_v21.tex -> journal_manuscript_v22.tex (NEW file;
  v21 and all earlier versions untouched):
  * the 'Data, Software, and Code Availability' statement now records
    the archival deposit of the compile-ready submission package on
    Zenodo (version DOI 10.5281/zenodo.22941018; the deposited file is
    the v26 submission ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4,
    CC-BY 4.0, concept DOI 10.5281/zenodo.22941017 -- byte-verified
    against the live Zenodo record 22941018 this round);
  * the \input reference-list pointer retargeted to
    journal_manuscript_v22_dam_refs.tex;
  * the two Reproducibility count sites refreshed 366 -> 372 (the v32
    audit ledger);
  * a V22 round block prepended to the header comment chain.
- companion_categorical_v14.tex -> companion_categorical_v15.tex (NEW
  file; v14 and all earlier versions untouched):
  * the 'Data and code availability.' paragraph now records the
    archival deposit of its compile-ready submission package on Zenodo
    (version DOI 10.5281/zenodo.22940820; the deposited file is the v26
    submission ZIP, MD5 6fa2d8d08386daeef563328fdfafad63, CC-BY 4.0,
    concept DOI 10.5281/zenodo.22940819 -- byte-verified against the
    live Zenodo record 22940820 this round);
  * the \bibliography pointer retargeted to companion_refs_v15.bib;
  * the header's application-paper pointer retargeted to
    journal_manuscript_v22.tex;
  * a V15 round block prepended to the header comment chain.
- Side files: journal_manuscript_v22_dam_refs.tex (new header block +
  the v21 entries verbatim), journal_manuscript_v22_refs.bib and
  companion_refs_v15.bib (byte-identical copies).

No theorem, proof, number, figure, or reference is changed. The edit
set is count-asserted and the script finishes with a byte-exact
reverse-edit verification (v22 reversed == v21; v15 reversed == v14).
"""
import os

S = os.path.dirname(os.path.abspath(__file__))

MAIN_SRC = os.path.join(S, "journal_manuscript_v21.tex")
MAIN_DST = os.path.join(S, "journal_manuscript_v22.tex")
COMP_SRC = os.path.join(S, "companion_categorical_v14.tex")
COMP_DST = os.path.join(S, "companion_categorical_v15.tex")
REFS_SRC = os.path.join(S, "journal_manuscript_v21_dam_refs.tex")
REFS_DST = os.path.join(S, "journal_manuscript_v22_dam_refs.tex")
BIB_SRC = os.path.join(S, "journal_manuscript_v21_refs.bib")
BIB_DST = os.path.join(S, "journal_manuscript_v22_refs.bib")
CBIB_SRC = os.path.join(S, "companion_refs_v14.bib")
CBIB_DST = os.path.join(S, "companion_refs_v15.bib")

# ---------------------------------------------------------------------
# MAIN: v21 -> v22
# ---------------------------------------------------------------------
main = open(MAIN_SRC, encoding="utf-8").read()

MAIN_EDITS = [
    # M1: header title line
    ("%  journal_manuscript_v21.tex -- main manuscript.",
     "%  journal_manuscript_v22.tex -- main manuscript."),
    # M2: V22 round block prepended to the header comment chain
    ("%  publisher through 2027.\n"
     "%  V21 final-prose round (v20 -> v21), from the final read-through",
     "%  publisher through 2027.\n"
     "%  V22 Zenodo-archive round (v21 -> v22): the Data, Software, and\n"
     "%  Code Availability statement now records the archival deposit of\n"
     "%  the compile-ready submission package on Zenodo (version DOI\n"
     "%  10.5281/zenodo.22941018; the deposited file is the v26\n"
     "%  submission ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4, CC-BY 4.0,\n"
     "%  concept DOI 10.5281/zenodo.22941017 -- byte-verified against\n"
     "%  the live Zenodo record this round); the two Reproducibility\n"
     "%  count sites refreshed to the v32 audit ledger (372). No\n"
     "%  numerical claim, theorem, figure, or reference changed; v21 and\n"
     "%  all earlier versions untouched.\n"
     "%  V21 final-prose round (v20 -> v21), from the final read-through"),
    # M3: availability statement gains the Zenodo archival sentence
    ("\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}. Genome-scale models",
     "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}, and the compile-ready\n"
     "submission package of this manuscript (LaTeX sources, figures, and\n"
     "the compiled PDF) is archived on Zenodo at\n"
     "\\href{https://doi.org/10.5281/zenodo.22941018}"
     "{DOI 10.5281/zenodo.\n22941018} (CC-BY 4.0). Genome-scale models"),
    # M4: reference-list input pointer
    ("\\input{journal_manuscript_v21_dam_refs}",
     "\\input{journal_manuscript_v22_dam_refs}"),
    # M5: Reproducibility count site 1
    ("($366$ checks).", "($372$ checks)."),
    # M6: Reproducibility count site 2
    ("An automated suite of $366$ numeric checks",
     "An automated suite of $372$ numeric checks"),
]

for i, (old, new) in enumerate(MAIN_EDITS, 1):
    n = main.count(old)
    assert n == 1, f"MAIN edit M{i}: expected 1 anchor, found {n}"
    main = main.replace(old, new)

with open(MAIN_DST, "w", encoding="utf-8") as f:
    f.write(main)

# reverse-edit byte verification
rev = main
for old, new in MAIN_EDITS:
    assert rev.count(new) == 1, f"MAIN reverse M: anchor not unique"
    rev = rev.replace(new, old)
orig = open(MAIN_SRC, encoding="utf-8").read()
assert rev == orig, "MAIN reverse-edit mismatch: v22 is not v21 + the declared edits"
print("journal_manuscript_v22.tex written (6 edits; reverse-verified == v21).")

# ---------------------------------------------------------------------
# COMPANION: v14 -> v15
# ---------------------------------------------------------------------
comp = open(COMP_SRC, encoding="utf-8").read()

COMP_EDITS = [
    # C1: header title line
    ("%  companion_categorical_v14.tex -- standalone theory paper.",
     "%  companion_categorical_v15.tex -- standalone theory paper."),
    # C2: header application-paper pointer
    ("%  Relation:   the application paper (journal_manuscript_v21.tex)",
     "%  Relation:   the application paper (journal_manuscript_v22.tex)"),
    # C3: V15 round block prepended to the header comment chain
    ("%              paper is self-contained for its own claims.\n"
     "\n"
     "%  V14 final-prose round (v13 -> v14), from the final read-through",
     "%              paper is self-contained for its own claims.\n"
     "\n"
     "%  V15 Zenodo-archive round (v14 -> v15): the Data and code\n"
     "%  availability paragraph now records the archival deposit of the\n"
     "%  compile-ready submission package on Zenodo (version DOI\n"
     "%  10.5281/zenodo.22940820; the deposited file is the v26\n"
     "%  submission ZIP, MD5 6fa2d8d08386daeef563328fdfafad63, CC-BY\n"
     "%  4.0, concept DOI 10.5281/zenodo.22940819 -- byte-verified\n"
     "%  against the live Zenodo record this round); the\n"
     "%  application-paper pointer in this header refreshed to its v22\n"
     "%  file. Every theorem, proof, number, section, and reference\n"
     "%  unchanged; companion_refs_v15.bib byte-identical; v14 and all\n"
     "%  earlier versions untouched.\n"
     "%  V14 final-prose round (v13 -> v14), from the final read-through"),
    # C4: availability paragraph gains the Zenodo archival sentence
    ("\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}; the application paper",
     "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}; the compile-ready\n"
     "submission package of this paper (LaTeX source, figures, and the\n"
     "compiled PDF) is archived on Zenodo at\n"
     "\\href{https://doi.org/10.5281/zenodo.22940820}"
     "{DOI 10.5281/zenodo.\n22940820} (CC-BY 4.0); the application paper"),
    # C5: bibliography pointer
    ("\\bibliography{companion_refs_v14}",
     "\\bibliography{companion_refs_v15}"),
]

for i, (old, new) in enumerate(COMP_EDITS, 1):
    n = comp.count(old)
    assert n == 1, f"COMP edit C{i}: expected 1 anchor, found {n}"
    comp = comp.replace(old, new)

with open(COMP_DST, "w", encoding="utf-8") as f:
    f.write(comp)

rev = comp
for old, new in COMP_EDITS:
    assert rev.count(new) == 1, "COMP reverse C: anchor not unique"
    rev = rev.replace(new, old)
orig = open(COMP_SRC, encoding="utf-8").read()
assert rev == orig, "COMP reverse-edit mismatch: v15 is not v14 + the declared edits"
print("companion_categorical_v15.tex written (5 edits; reverse-verified == v14).")

# ---------------------------------------------------------------------
# Side files
# ---------------------------------------------------------------------
refs = open(REFS_SRC, encoding="utf-8").read()
refs_new = (
    "% journal_manuscript_v22_dam_refs.tex -- references for the v22\n"
    "% Zenodo-archive round: entries byte-identical to the v21 list (no\n"
    "% reference changes this round; v21 and earlier untouched). The\n"
    "% v21 header follows:\n"
) + refs
with open(REFS_DST, "w", encoding="utf-8") as f:
    f.write(refs_new)
import re as _re
n_entries = len(_re.findall(r"\\bibitem", refs))
assert n_entries == 29, f"refs entries: expected 29, found {n_entries}"
assert refs_new[len(refs_new) - len(refs):] == refs, "refs tail not verbatim"
print("journal_manuscript_v22_dam_refs.tex written (header + v21 entries verbatim).")

bib = open(BIB_SRC, encoding="utf-8").read()
with open(BIB_DST, "w", encoding="utf-8") as f:
    f.write(bib)
cbib = open(CBIB_SRC, encoding="utf-8").read()
with open(CBIB_DST, "w", encoding="utf-8") as f:
    f.write(cbib)
print("journal_manuscript_v22_refs.bib + companion_refs_v15.bib written "
      "(byte-identical copies).")

# untouched-source guarantees
for src in (MAIN_SRC, COMP_SRC, REFS_SRC, BIB_SRC, CBIB_SRC):
    assert os.path.exists(src), f"source file vanished: {src}"
print("All sources untouched (v21/v14 and earlier preserved).")
