#!/usr/bin/env python3
"""v21_v14_final_prose_fixes.py -- final read-through pass of both
manuscripts' prose, applied as a light touch-up on NEW versioned files
(journal_manuscript_v21.tex from v20; companion_categorical_v14.tex
from v13). v20/v13 and all earlier versions are untouched.

MAIN (v20 -> v21), three prose findings from the read-through:
  M1  The Discussion memory subsection quotes the same-gene transcript
      correlation as +0.420 while 5.9 and the buffering subsection
      quote +0.419 for the same quantity (the e27 artifact value gated
      by audit E27-1; +0.420 is the v17-ledger recomputation at
      slightly different gene matching). Harmonized to +0.419.
  M2  'under the locked kappa_mu metric' -- 'locked' is unexplained
      anywhere in the paper and contradicts 5.9's flat attribution of
      -0.083 to kappa_mu. The -0.098/+0.339 pair is the per-gene path
      metric of the V7 P0 deposits; the wording now says so.
  M3  The six in-text figure references read 'Fig 1' (Fig~\\ref, no
      period); the journal's form is 'Fig. n'. Normalized to Fig.~.
  Plus: audit-count text refreshed 359 -> 366 (the v31 ledger) and
  the stale header comment (companion v9) refreshed to v14.

COMPANION (v13 -> v14), four findings:
  C1  The where-clause of the piecewise-holonomy formula (eq:piecewise-F)
      was displaced behind the affine-wall regime paragraph, leaving
      '...(Open Problem 1). where F_pm are...' -- a lowercase sentence
      fragment. Transposed back to directly follow its equation.
  C2  rem:two-contractions says the Banach contraction holds on
      X=[0,1]^d, but the theorem and the box-invariance paragraph use
      X=[-1.5,1.5]^d and state that [0,1]^d FAILS the hypothesis.
      Corrected to the theorem's box.
  C3  The Ito-expansion proof's variance parenthetical ends
      '...variance.); and' -- a punctuation artifact. Made an inline
      lowercase clause.
  C4  Figure-label convention aligned with the main paper and the
      journal's 'Fig. n' form: caption package (labelsep=space) +
      \\figurename=Fig. in the preamble; the three 'Figure~\\ref'
      in-text references normalized to 'Fig.~\\ref' (the fourth site
      already used that form).

No theorem, proof, numerical claim, section, table, or figure is
changed in either paper.
"""
import os
import shutil

S = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(S)


def patch(path, edits, label):
    t = open(path, encoding="utf-8").read()
    for i, (old, new, tag, count) in enumerate(edits):
        found = t.count(old)
        assert found == count, (
            f"{label} edit {i + 1} ({tag}): expected {count}, "
            f"found {found}")
        t = t.replace(old, new)
    return t


def write(path, t):
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)


# =====================================================================
# MAIN: journal_manuscript_v20.tex -> journal_manuscript_v21.tex
# =====================================================================
src = os.path.join(S, "journal_manuscript_v20.tex")
dst = os.path.join(S, "journal_manuscript_v21.tex")

V21_NOTE = """\
%  V21 final-prose round (v20 -> v21), from the final read-through
%  pass of both manuscripts' prose: the Discussion memory
%  subsection's same-gene transcript correlation harmonized to
%  +0.419 (the e27 artifact value gated by audit E27-1, matching
%  5.9 and the buffering subsection; the +0.420 token was the
%  v17-ledger recomputation of the same quantity at slightly
%  different gene matching), the unexplained 'locked' qualifier
%  replaced by the actual provenance of the -0.098/+0.339 pair
%  (the per-gene path metric of 5.7, the V7 P0 deposits), the six
%  in-text figure references normalized to the Springer 'Fig. n'
%  form (Fig.~), and the audit-count text refreshed to the v31
%  ledger (366). No numerical claim added or removed; every v20
%  audited number unchanged; v20 and all earlier versions
%  untouched.
"""

t = patch(src, [
    # identity line
    ("%  journal_manuscript_v20.tex -- main manuscript.\n",
     "%  journal_manuscript_v21.tex -- main manuscript.\n",
     "identity line", 1),
    # round note inserted after the venue block
    ("%  publisher through 2027.\n",
     "%  publisher through 2027.\n" + V21_NOTE,
     "v21 round note", 1),
    # stale companion-version pointer in the header comment
    ("scripts/companion_categorical_v9.tex)",
     "scripts/companion_categorical_v14.tex)",
     "companion pointer", 1),
    # M1 + M2: the memory-subsection sentence
    ("+0.420$; under the locked $\\kmu$ metric the picture is unchanged\n"
     "(protein $r = -0.098$, $p = 0.06$; transcript $r = +0.339$). A",
     "+0.419$; the picture is unchanged under the per-gene path metric\n"
     "of \\S\\ref{sec:v7} (protein $r = -0.098$, $p = 0.06$; transcript\n"
     "$r = +0.339$). A",
     "M1+M2 memory sentence", 1),
    # M3: six in-text figure references -> Fig.~
    ("Fig~\\ref", "Fig.~\\ref", "M3 Fig~ -> Fig.~ (6 sites)", 6),
    # refs input retarget
    ("\\input{journal_manuscript_v20_dam_refs}",
     "\\input{journal_manuscript_v21_dam_refs}",
     "refs input", 1),
    # audit count refresh (two sites)
    ("($359$ checks).", "($366$ checks).", "count site 1", 1),
    ("suite of $359$ numeric checks", "suite of $366$ numeric checks",
     "count site 2", 1),
], "main v21")

write(dst, t)
print("journal_manuscript_v21.tex written "
      f"({len(t)} bytes, from {os.path.getsize(src)})")

# ---- refs side files ----
refs_src = os.path.join(S, "journal_manuscript_v20_dam_refs.tex")
refs_dst = os.path.join(S, "journal_manuscript_v21_dam_refs.tex")
rt = patch(refs_src, [
    ("% journal_manuscript_v20_dam_refs.tex -- references for the v20\n"
     "% Discover Applied Mathematics round.",
     "% journal_manuscript_v21_dam_refs.tex -- references for the v21\n"
     "% final-prose round: entries byte-identical to the v20 list (no\n"
     "% reference changes this round; v20 and earlier untouched). The\n"
     "% v20 header follows:\n"
     "% Discover Applied Mathematics round.",
     "refs header", 1),
], "refs v21")
write(refs_dst, rt)
print("journal_manuscript_v21_dam_refs.tex written")

shutil.copyfile(os.path.join(S, "journal_manuscript_v20_refs.bib"),
                os.path.join(S, "journal_manuscript_v21_refs.bib"))
print("journal_manuscript_v21_refs.bib copied (byte-identical to v20)")

# =====================================================================
# COMPANION: companion_categorical_v13.tex -> v14
# =====================================================================
src_c = os.path.join(S, "companion_categorical_v13.tex")
dst_c = os.path.join(S, "companion_categorical_v14.tex")

V14_NOTE = """\
%  V14 final-prose round (v13 -> v14), from the final read-through
%  pass of both manuscripts' prose: the where-clause of the
%  piecewise-holonomy formula restored to its equation (it had been
%  displaced behind the affine-wall regime paragraph, leaving a
%  lowercase fragment after '(Open Problem 1).'), the
%  two-contractions remark's state space corrected to the theorem's
%  box X = [-1.5,1.5]^d ([0,1]^d fails the hypothesis by the
%  paper's own box-invariance computation), a punctuation repair in
%  the Ito-expansion proof's variance parenthetical, and the
%  figure-label convention aligned with the application paper and
%  the journal's 'Fig. n' form (captions via the caption package
%  with labelsep=space and figurename=Fig.; the three in-text
%  'Figure~' references normalized to 'Fig.~'). Every theorem,
%  proof, number, and section unchanged; v13 and all earlier
%  versions untouched.
"""

tc = patch(src_c, [
    # identity line
    ("%  companion_categorical_v13.tex -- standalone theory paper.\n",
     "%  companion_categorical_v14.tex -- standalone theory paper.\n",
     "identity line", 1),
    # round note inserted after the Relation block
    ("%              paper is self-contained for its own claims.\n"
     "%  V13 DAM round",
     "%              paper is self-contained for its own claims.\n\n" +
     V14_NOTE + "%  V13 DAM round",
     "v14 round note", 1),
    # application-paper pointer in the Relation comment
    ("%  Relation:   the application paper (journal_manuscript_v20.tex)",
     "%  Relation:   the application paper (journal_manuscript_v21.tex)",
     "application pointer", 1),
    # C4: caption package + figurename, before hyperref (main's order)
    ("\\graphicspath{{./}{../download/}}\n"
     "\\usepackage[colorlinks=true,linkcolor=blue!55!black,"
     "citecolor=blue!45!black,urlcolor=blue!55!black,bookmarks=true,"
     "bookmarksnumbered=true,unicode=true]{hyperref}",
     "\\graphicspath{{./}{../download/}}\n"
     "\\usepackage[labelsep=space]{caption}\n"
     "\\renewcommand{\\figurename}{Fig.}\n"
     "\\usepackage[colorlinks=true,linkcolor=blue!55!black,"
     "citecolor=blue!45!black,urlcolor=blue!55!black,bookmarks=true,"
     "bookmarksnumbered=true,unicode=true]{hyperref}",
     "C4 preamble caption+figurename", 1),
    # C1: where-clause transposition in thm:stratified-holonomy
    ("\\end{equation}\n"
     "For affine wall transitions the terms neglected beyond the "
     "displayed\n"
     "$O(\\varepsilon)$ and $O(\\varepsilon^2)$ contributions are\n"
     "$O(\\varepsilon^3)$ --- the regime the numerics of\n"
     "Remark~\\ref{rem:2cat-gluing-numeric} verify; for general\n"
     "transitions, second-order Taylor terms of $\\log g_{+-}$ along "
     "the\n"
     "wall and commutators of the two resets enter at "
     "$O(\\varepsilon^2)$\n"
     "(Open Problem~1).\n"
     "where $F_\\pm$ are the curvature $2$-forms on strata $S_\\pm$ "
     "and\n"
     "$\\Sigma$ is the small enclosed disk. The two boundary resets "
     "cancel",
     "\\end{equation}\n"
     "where $F_\\pm$ are the curvature $2$-forms on strata $S_\\pm$ "
     "and\n"
     "$\\Sigma$ is the small enclosed disk. For affine wall "
     "transitions\n"
     "the terms neglected beyond the displayed\n"
     "$O(\\varepsilon)$ and $O(\\varepsilon^2)$ contributions are\n"
     "$O(\\varepsilon^3)$ --- the regime the numerics of\n"
     "Remark~\\ref{rem:2cat-gluing-numeric} verify; for general\n"
     "transitions, second-order Taylor terms of $\\log g_{+-}$ along "
     "the\n"
     "wall and commutators of the two resets enter at "
     "$O(\\varepsilon^2)$\n"
     "(Open Problem~1). The two boundary resets cancel",
     "C1 where-clause transposition", 1),
    # C2: state space of rem:two-contractions
    ("$X=[0,1]^{d}$ (the optic-side Banach argument), while",
     "$X=[-1.5,1.5]^{d}$ (the optic-side Banach argument), while",
     "C2 state space", 1),
    # C3: punctuation in lem:ito-expand proof
    ("(The value $1/12$ is the\n"
     "Brownian-bridge time-integral variance, not the\n"
     "free-Brownian-motion L\\'evy-area variance.); and the",
     "(the value $1/12$ is the\n"
     "Brownian-bridge time-integral variance, not the\n"
     "free-Brownian-motion L\\'evy-area variance); and the",
     "C3 punctuation", 1),
    # C4: in-text figure references
    ("Figure~\\ref", "Fig.~\\ref", "C4 Figure~ -> Fig.~ (3 sites)", 3),
    # bibliography retarget
    ("\\bibliography{companion_refs_v13}",
     "\\bibliography{companion_refs_v14}",
     "bibliography pointer", 1),
], "companion v14")

write(dst_c, tc)
print("companion_categorical_v14.tex written "
      f"({len(tc)} bytes, from {os.path.getsize(src_c)})")

shutil.copyfile(os.path.join(S, "companion_refs_v13.bib"),
                os.path.join(S, "companion_refs_v14.bib"))
print("companion_refs_v14.bib copied (byte-identical to v13)")

print("\nAll edits applied. Verify with:")
print("  diff <(sed 's/$//' scripts/journal_manuscript_v20.tex) "
       "scripts/journal_manuscript_v21.tex")
print("  diff scripts/companion_categorical_v13.tex "
       "scripts/companion_categorical_v14.tex")
