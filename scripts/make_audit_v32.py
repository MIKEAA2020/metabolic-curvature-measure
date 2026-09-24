#!/usr/bin/env python3
"""Build audit_v32_numbers.py from audit_v31_numbers.py (the v31 file
is never modified) for the V22/V15 Zenodo-archive round:

1. Functional retargets: journal_manuscript_v21_dam_refs ->
   journal_manuscript_v22_dam_refs (10); journal_manuscript_v21 ->
   journal_manuscript_v22 (17 remaining); companion_categorical_v14 ->
   companion_categorical_v15 (28); companion_refs_v14 ->
   companion_refs_v15 (5).
2. V20-9 count arithmetic extended by the six V22 checks (372 total);
   its label retargeted to the v32 ledger.
3. V21-7 label refreshed (v22 refs + v15 bib; wording 'no reference
   changes since the v13 DAM-alignment round').
4. New V22-family checks: V22-1 main availability statement wired to
   the Zenodo archive (version DOI 10.5281/zenodo.22941018, CC-BY 4.0,
   GitHub link and source sentences retained); V22-2 companion
   availability paragraph wired to its archive (version DOI
   10.5281/zenodo.22940820); V22-3 v22 refs + v15 bib + v22 refs
   database carried (29 entries, v21-identical, byte-identical bibs);
   V22-4 main minimal-diff (reversing the six declared V22 edits on
   v22 reproduces v21 byte-exactly); V22-5 companion minimal-diff
   (reversing the five declared V15 edits reproduces v14
   byte-exactly); V22-6 the two Reproducibility count sites refreshed
   to 372 with the n = 366 gene-count sites retained.
5. Outputs: v32_number_audit.json / v32_number_audit.md.
"""
import os

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "audit_v31_numbers.py")
DST = os.path.join(S, "audit_v32_numbers.py")

t = open(SRC, encoding="utf-8").read()
n_repl = 0


def rep(old, new, label, count=1):
    global t, n_repl
    found = t.count(old)
    assert found == count, f"{label}: expected {count}, found {found}"
    t = t.replace(old, new)
    n_repl += 1


# --- functional retargets (refs first, then the plain names) ---
rep("journal_manuscript_v21_dam_refs", "journal_manuscript_v22_dam_refs",
    "refs filename retarget", 10)
rep("journal_manuscript_v21", "journal_manuscript_v22",
    "main filename retarget", 17)
rep("companion_categorical_v14", "companion_categorical_v15",
    "companion filename retarget", 28)
rep("companion_refs_v14", "companion_refs_v15",
    "companion bib retarget", 5)

# --- docstring head (after the retargets, anchored on retargeted text) ---
rep('Numeric consistency audit of journal_manuscript_v22.tex +\n'
    'companion_categorical_v15.tex (V21/V14 final-prose round: the\n'
    'read-through findings of the final pass applied',
    'Numeric consistency audit of journal_manuscript_v22.tex +\n'
    'companion_categorical_v15.tex (V22/V15 Zenodo-archive round: the\n'
    'archival DOIs of the two submission packages wired into both data\n'
    'availability statements -- main DOI 10.5281/zenodo.22941018 (the\n'
    'v26 submission ZIP, MD5 8e7e367183a8f84493e65796bc7ebad4, CC-BY\n'
    '4.0, concept DOI 10.5281/zenodo.22941017) and companion DOI\n'
    '10.5281/zenodo.22940820 (the v26 submission ZIP, MD5\n'
    '6fa2d8d08386daeef563328fdfafad63, CC-BY 4.0, concept DOI\n'
    '10.5281/zenodo.22940819), both byte-verified against the live\n'
    'Zenodo records this round; refs/bib side files carried; the two\n'
    'Reproducibility count sites refreshed to the v32 ledger (372);\n'
    'extends the V21/V14 final-prose round: the\n'
    'read-through findings of the final pass applied',
    "docstring head")

# --- V20-9: count arithmetic + label ---
rep("_expected_total = len(checks) + 2 + 7  # V20-9 (self) + V20-10 "
    "(refs) + V21-1..V21-7",
    "_expected_total = len(checks) + 2 + 7 + 6  # V20-9 (self) + V20-10 "
    "(refs) + V21-1..V21-7 + V22-1..V22-6",
    "V20-9 arithmetic")
rep('"equals the v31 ledger size (no stale check count)",',
    '"equals the v32 ledger size (no stale check count)",',
    "V20-9 label")

# --- V21-7 label refresh ---
rep('check("V21-7", "v21 refs + v14 bib carried unchanged: the 29-entry "',
    'check("V21-7", "v22 refs + v15 bib carried unchanged: the 29-entry "',
    "V21-7 label head")
rep('"companion_refs_v13.bib (no reference changes in the "\n'
    '      "final-prose round)",',
    '"companion_refs_v13.bib (no reference changes since the "\n'
    '      "v13 DAM-alignment round)",',
    "V21-7 label tail")

# --- md header / out experiment ---
rep('md = ["# V21/V14 numeric consistency audit (final-prose round: '
    'read-through findings + Fig.-label alignment; v30 ledger retargeted to ',
    'md = ["# V22/V15 numeric consistency audit (Zenodo-archive round: '
    'archival DOIs wired into both availability statements; v31 ledger '
    'retargeted to ',
    "md header")
rep('out = {"experiment": "V21/V14 numeric consistency audit (final-prose "\n'
    '                     "round; extends the v30 audit)",',
    'out = {"experiment": "V22/V15 numeric consistency audit (Zenodo-'
    'archive "\n                     "round; extends the v31 audit)",',
    "out experiment")

# --- outputs ---
rep('v31_number_audit.json', 'v32_number_audit.json', "json output")
rep('v31_number_audit.md', 'v32_number_audit.md', "md output")

# --- V22 checks block, inserted before the out-dict write ---
NEW_BLOCK = r'''
# =====================================================================
# V32 section. V22/V15 Zenodo-archive round gates
# =====================================================================
check("V22-1", "main availability statement wired to the Zenodo "
      "archive: 'archived on Zenodo at' + the clickable version DOI "
      "10.5281/zenodo.22941018 (CC-BY 4.0); the GitHub bundle link and "
      "the external-source sentences retained",
      "journal_manuscript_v22.tex Data, Software, and Code Availability",
      "tokens (raw source)",
      "is archived on Zenodo at" in tex2 and
      "\\href{https://doi.org/10.5281/zenodo.22941018}"
      "{DOI 10.5281/zenodo.\n22941018} (CC-BY 4.0)" in tex2 and
      "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
      "{github.com/" in tex2 and
      "were obtained from the BiGG database" in tex2)

check("V22-2", "companion availability paragraph wired to the Zenodo "
      "archive: 'archived on Zenodo at' + the clickable version DOI "
      "10.5281/zenodo.22940820 (CC-BY 4.0); the GitHub repository link "
      "and the application-paper data-source pointer retained",
      "companion_categorical_v15.tex Declarations",
      "tokens (raw source)",
      "is archived on Zenodo at" in companion and
      "\\href{https://doi.org/10.5281/zenodo.22940820}"
      "{DOI 10.5281/zenodo.\n22940820} (CC-BY 4.0)" in companion and
      "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
      "{github.com/" in companion and
      "the application paper" in companion)

refs_v22zen = open(os.path.join(BASE, "scripts",
                   "journal_manuscript_v22_dam_refs.tex")).read()
refs_v21orig = open(os.path.join(BASE, "scripts",
                   "journal_manuscript_v21_dam_refs.tex")).read()
bib_v15zen = open(os.path.join(BASE, "scripts",
                 "companion_refs_v15.bib")).read()
bib_v14orig = open(os.path.join(BASE, "scripts",
                 "companion_refs_v14.bib")).read()
check("V22-3", "v22 refs + v15 bib + v22 refs database carried: the "
      "29-entry reference list identical to the v21 list (a v22 round "
      "header prepended only); companion_refs_v15.bib byte-identical "
      "to companion_refs_v14.bib; journal_manuscript_v22_refs.bib "
      "byte-identical to the v21 database",
      "journal_manuscript_v22_dam_refs.tex + companion_refs_v15.bib "
      "+ journal_manuscript_v22_refs.bib",
      "entries %d; entries identical: %s; bib identical: %s" % (
          len(re.findall(r"\\bibitem", refs_v22zen)),
          refs_v22zen.endswith(refs_v21orig),
          bib_v15zen == bib_v14orig),
      len(re.findall(r"\\bibitem", refs_v22zen)) == 29 and
      refs_v22zen.endswith(refs_v21orig) and
      bib_v15zen == bib_v14orig and
      open(os.path.join(BASE, "scripts",
                       "journal_manuscript_v22_refs.bib")).read() ==
      open(os.path.join(BASE, "scripts",
                       "journal_manuscript_v21_refs.bib")).read())

_v21full = open(os.path.join(BASE, "scripts",
                "journal_manuscript_v21.tex")).read()
_MAIN_PAIRS = [
    ("%  journal_manuscript_v22.tex -- main manuscript.",
     "%  journal_manuscript_v21.tex -- main manuscript."),
    ("%  publisher through 2027.\n"
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
     "%  V21 final-prose round (v20 -> v21), from the final read-through",
     "%  publisher through 2027.\n"
     "%  V21 final-prose round (v20 -> v21), from the final read-through"),
    ("\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}, and the compile-ready\n"
     "submission package of this manuscript (LaTeX sources, figures, and\n"
     "the compiled PDF) is archived on Zenodo at\n"
     "\\href{https://doi.org/10.5281/zenodo.22941018}"
     "{DOI 10.5281/zenodo.\n22941018} (CC-BY 4.0). Genome-scale models",
     "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}. Genome-scale models"),
    ("\\input{journal_manuscript_v22_dam_refs}",
     "\\input{journal_manuscript_v21_dam_refs}"),
    ("($372$ checks).", "($366$ checks)."),
    ("An automated suite of $372$ numeric checks",
     "An automated suite of $366$ numeric checks"),
]
_r = tex2
for _new, _old in _MAIN_PAIRS:
    assert _r.count(_new) == 1, ("V22-4 reverse anchor not unique: "
                                 + _new[:60])
    _r = _r.replace(_new, _old)
check("V22-4", "main minimal-diff: reversing the six declared V22 edits "
      "on journal_manuscript_v22.tex reproduces journal_manuscript_v21.tex "
      "byte-exactly (no other content changed in the round; v21 itself "
      "untouched)",
      "journal_manuscript_v22.tex vs journal_manuscript_v21.tex",
      "byte-identical after reverse: %s" % (_r == _v21full),
      _r == _v21full)

_v14full = open(os.path.join(BASE, "scripts",
                "companion_categorical_v14.tex")).read()
_COMP_PAIRS = [
    ("%  companion_categorical_v15.tex -- standalone theory paper.",
     "%  companion_categorical_v14.tex -- standalone theory paper."),
    ("%  Relation:   the application paper (journal_manuscript_v22.tex)",
     "%  Relation:   the application paper (journal_manuscript_v21.tex)"),
    ("%              paper is self-contained for its own claims.\n"
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
     "%  V14 final-prose round (v13 -> v14), from the final read-through",
     "%              paper is self-contained for its own claims.\n"
     "\n"
     "%  V14 final-prose round (v13 -> v14), from the final read-through"),
    ("\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}; the compile-ready\n"
     "submission package of this paper (LaTeX source, figures, and the\n"
     "compiled PDF) is archived on Zenodo at\n"
     "\\href{https://doi.org/10.5281/zenodo.22940820}"
     "{DOI 10.5281/zenodo.\n22940820} (CC-BY 4.0); the application paper",
     "\\href{https://github.com/MIKEAA2020/metabolic-curvature-measure}"
     "{github.com/\n"
     "MIKEAA2020/metabolic-curvature-measure}; the application paper"),
    ("\\bibliography{companion_refs_v15}",
     "\\bibliography{companion_refs_v14}"),
]
_r2 = companion
for _new, _old in _COMP_PAIRS:
    assert _r2.count(_new) == 1, ("V22-5 reverse anchor not unique: "
                                  + _new[:60])
    _r2 = _r2.replace(_new, _old)
check("V22-5", "companion minimal-diff: reversing the five declared V15 "
      "edits on companion_categorical_v15.tex reproduces "
      "companion_categorical_v14.tex byte-exactly (no other content "
      "changed in the round; v14 itself untouched)",
      "companion_categorical_v15.tex vs companion_categorical_v14.tex",
      "byte-identical after reverse: %s" % (_r2 == _v14full),
      _r2 == _v14full)

check("V22-6", "the two Reproducibility count sites refreshed to the "
      "v32 ledger: '($372$ checks).' and 'An automated suite of $372$ "
      "numeric checks'; the stale count tokens gone (the n = 366 "
      "gene-count sites are a different quantity and retained)",
      "journal_manuscript_v22.tex Reproducibility",
      "count sites",
      "($372$ checks)." in tex2 and
      "An automated suite of $372$ numeric checks" in tex2 and
      "($366$ checks)" not in tex2 and
      "$366$ numeric checks" not in tex2 and
      "n = 366" in tex2)

'''
rep('out = {"experiment": "V22/V15 numeric consistency audit (Zenodo-'
    'archive "\n                     "round; extends the v31 audit)",',
    NEW_BLOCK + 'out = {"experiment": "V22/V15 numeric consistency '
    'audit (Zenodo-archive "\n                     "round; extends the '
    'v31 audit)",',
    "V22 checks block inserted")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"audit_v32_numbers.py written ({n_repl} transformations + "
      "V22 checks block).")
print("NOTE: V20-9 self-consistency gate expects journal_manuscript_"
      "v22.tex to state the final v32 ledger size (372).")
