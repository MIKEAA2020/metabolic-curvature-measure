#!/usr/bin/env python3
"""Build audit_v31_numbers.py from audit_v30_numbers.py (the v30 file
is never modified) for the V21/V14 final-prose round:

1. Functional retargets: journal_manuscript_v20_dam_refs ->
   journal_manuscript_v21_dam_refs; journal_manuscript_v20 ->
   journal_manuscript_v21; companion_categorical_v13 ->
   companion_categorical_v14; companion_refs_v13 -> companion_refs_v14
   (reads and labels).
2. V20-9 count arithmetic extended by the seven V21 checks; its label
   retargeted to the v31 ledger.
3. New V21-family checks: M1/M2 (harmonized +0.419 token, per-gene
   path-metric provenance wording, 'locked' gone), M3 (six 'Fig.~'
   in-text references, 'Fig~' gone), C1 (where-clause restored to its
   equation), C2 (two-contractions state space = the theorem's box),
   C3 (punctuation repair), C4 (companion figure-label convention:
   figurename + labelsep=space, no mixed 'Figure~'), and the v21
   refs / v14 bib carry check.
4. Outputs: v31_number_audit.json / v31_number_audit.md.
"""
import os

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "audit_v30_numbers.py")
DST = os.path.join(S, "audit_v31_numbers.py")

t = open(SRC, encoding="utf-8").read()
n_repl = 0


def rep(old, new, label, count=1):
    global t, n_repl
    found = t.count(old)
    assert found == count, f"{label}: expected {count}, found {found}"
    t = t.replace(old, new)
    n_repl += 1


# --- docstring head (before the filename retargets) ---
rep("companion_categorical_v13.tex (V20/V13 Discover Applied Mathematics\n"
    "round: the causal-coherence/prose-alignment review findings F2-F6\n"
    "applied as a light touch-up",
    "companion_categorical_v13.tex (V21/V14 final-prose round: the\n"
    "read-through findings of the final pass applied -- the Discussion\n"
    "memory-subsection transcript token harmonized to +0.419, the\n"
    "unexplained 'locked' qualifier replaced by the per-gene\n"
    "path-metric provenance, six in-text figure references normalized\n"
    "to Fig. n, the companion where-clause restored to its equation,\n"
    "the two-contractions state space corrected to the theorem's box,\n"
    "an Ito-proof punctuation repair, and the companion figure labels\n"
    "aligned to the journal's Fig. n form; extends the V20/V13\n"
    "Discover Applied Mathematics round: the causal-coherence/"
    "prose-alignment review findings F2-F6 applied as a light touch-up",
    "docstring head")

# --- functional retargets (refs first, then the plain names) ---
rep("journal_manuscript_v20_dam_refs", "journal_manuscript_v21_dam_refs",
    "refs filename retarget", 8)
rep("journal_manuscript_v20", "journal_manuscript_v21",
    "main filename retarget", 15)
rep("companion_categorical_v13", "companion_categorical_v14",
    "companion filename retarget", 24)
rep("companion_refs_v13", "companion_refs_v14",
    "companion bib retarget", 2)

# --- V20-9: count arithmetic + label ---
rep("_expected_total = len(checks) + 2  # V20-9 (self) + V20-10 "
    "(refs count)",
    "_expected_total = len(checks) + 2 + 7  # V20-9 (self) + V20-10 "
    "(refs) + V21-1..V21-7",
    "V20-9 arithmetic")
rep('"equals the v30 ledger size (no stale check count)",',
    '"equals the v31 ledger size (no stale check count)",',
    "V20-9 label")

# --- md header / out experiment ---
rep('md = ["# V20/V13 numeric consistency audit (Discover Applied '
    'Mathematics round: F2-F6 light touch-up + venue gates; v29 ledger ',
    'md = ["# V21/V14 numeric consistency audit (final-prose round: '
    'read-through findings + Fig.-label alignment; v30 ledger ',
    "md header")
rep('out = {"experiment": "V20/V13 numeric consistency audit (Discover "\n'
    '                     "Applied Mathematics round; extends the v29 audit)",',
    'out = {"experiment": "V21/V14 numeric consistency audit (final-prose "\n'
    '                     "round; extends the v30 audit)",',
    "out experiment")

# --- outputs ---
rep('with open(os.path.join(DB, "v30_number_audit.json"), "w") as f:',
    'with open(os.path.join(DB, "v31_number_audit.json"), "w") as f:',
    "json output")
rep('with open(os.path.join(DB, "v30_number_audit.md"), "w") as f:',
    'with open(os.path.join(DB, "v31_number_audit.md"), "w") as f:',
    "md output")

# --- V21 checks block, inserted before the out-dict write ---
NEW_BLOCK = r'''
# =====================================================================
# V31 section. V21/V14 final-prose round gates: read-through findings
# =====================================================================
tex2_body = re.sub(r"(?m)^[ \t]*%[^\n]*\n", "", tex2)
tex2_flat = re.sub(r"\s+", " ", tex2_body)
check("V21-1", "final-prose M1/M2: memory-subsection transcript token "
      "harmonized to +0.419 (the e27 artifact value gated by E27-1, "
      "matching 5.9 and the buffering subsection); the +0.420 token "
      "(the v17-ledger recomputation) absent; the unexplained 'locked' "
      "qualifier replaced by the actual provenance of the "
      "-0.098/+0.339 pair (the per-gene path metric of 5.7)",
      "journal_manuscript_v21.tex Discussion (memory subsection)",
      "tokens (comment-stripped body)",
      "transcripts on the same genes carry $r = +0.419$" in tex2_flat
      and "+0.420" not in tex2_flat
      and re.search(r"(?<!\w)locked\b", tex2_flat) is None
      and "the picture is unchanged under the per-gene path metric "
      "of \\S\\ref{sec:v7}" in tex2_flat
      and "(protein $r = -0.098$, $p = 0.06$; transcript $r = "
      "+0.339$)" in tex2_flat)

check("V21-2", "final-prose M3: the six in-text figure references "
      "carry the Springer 'Fig. n' form (Fig.~); the bare 'Fig~' "
      "form absent",
      "journal_manuscript_v21.tex",
      "Fig.~ sites: %d" % tex2.count("Fig.~\\ref{"),
      tex2.count("Fig.~\\ref{") == 6 and "Fig~\\ref" not in tex2)

companion_flat = re.sub(r"\s+", " ", companion)
_iw = companion_flat.find("where $F_\\pm$ are the curvature")
_ia = companion_flat.find("For affine wall transitions")
check("V21-3", "final-prose C1: the where-clause of the piecewise-"
      "holonomy formula restored to its equation (v13 had it "
      "displaced behind the affine-wall regime paragraph, leaving a "
      "lowercase fragment after '(Open Problem 1).')",
      "companion_categorical_v14.tex thm:stratified-holonomy",
      "where-index %d < affine-index %d" % (_iw, _ia),
      0 <= _iw < _ia)

check("V21-4", "final-prose C2: the two-contractions remark's state "
      "space is the theorem's box X = [-1.5,1.5]^d (v13 said "
      "[0,1]^d, which the paper's own box-invariance computation "
      "excludes)",
      "companion_categorical_v14.tex rem:two-contractions",
      "state space",
      "X=[-1.5,1.5]^{d}$ (the optic-side Banach argument)" in
      companion_flat and
      "X=[0,1]^{d}$ (the optic-side" not in companion_flat)

check("V21-5", "final-prose C4: companion figure captions carry the "
      "journal's 'Fig. n' form (figurename + labelsep=space, "
      "matching the main paper); no mixed 'Figure~' in-text "
      "references remain",
      "companion_categorical_v14.tex preamble + text",
      "Figure~ sites: %d; Fig.~ sites: %d" % (
          companion.count("Figure~\\ref"), companion.count("Fig.~\\ref")),
      "\\renewcommand{\\figurename}{Fig.}" in companion and
      "labelsep=space" in companion and
      companion.count("Figure~\\ref") == 0 and
      companion.count("Fig.~\\ref") == 4)

check("V21-6", "final-prose C3: the Ito-expansion proof's variance "
      "parenthetical is an inline clause (the 'variance.);' "
      "punctuation artifact gone)",
      "companion_categorical_v14.tex lem:ito-expand proof",
      "punctuation",
      "variance.); and the" not in companion and
      "L\\'evy-area variance); and the" in companion)

refs_v21 = open(os.path.join(BASE, "scripts",
                             "journal_manuscript_v21_dam_refs.tex")).read()
bib_v14 = open(os.path.join(BASE, "scripts",
                            "companion_refs_v14.bib")).read()
bib_v13_orig = open(os.path.join(BASE, "scripts",
                                 "companion_refs_v13.bib")).read()
check("V21-7", "v21 refs + v14 bib carried unchanged: the 29-entry "
      "list; companion_refs_v14.bib byte-identical to "
      "companion_refs_v13.bib (no reference changes in the "
      "final-prose round)",
      "journal_manuscript_v21_dam_refs.tex + companion_refs_v14.bib",
      "entries %d; bib identical: %s" % (
          len(re.findall(r"\\bibitem", refs_v21)),
          bib_v14 == bib_v13_orig),
      len(re.findall(r"\\bibitem", refs_v21)) == 29 and
      bib_v14 == bib_v13_orig)

'''
rep('out = {"experiment": "V21/V14 numeric consistency audit (final-prose "\n'
    '                     "round; extends the v30 audit)",',
    NEW_BLOCK + 'out = {"experiment": "V21/V14 numeric consistency '
    'audit (final-prose "\n                     "round; extends the '
    'v30 audit)",',
    "V21 checks block inserted")

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print(f"audit_v31_numbers.py written ({n_repl} transformations + "
      "V21 checks block).")
print("NOTE: V20-9 self-consistency gate expects journal_manuscript_"
      "v21.tex to state the final v31 ledger size (366).")
