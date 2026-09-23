#!/usr/bin/env python3
"""companion_v11_alignment.py -- build companion_categorical_v11.tex (NEW
versioned file; v10 and all earlier versions untouched) as the companion-
side half of the v19 categorical-subsection delegation.

Context: the v19 comprehension restructure removed the categorical-reading
subsection from the main paper's body (JTB desk rejection: structure/intent
incomprehensible; the categorical prose was the densest barrier).  The
removed material's full development already lives in this companion, so
the removal is clean delegation, EXCEPT two companion sentences that still
describe the OLD division of labor ("the application paper states the
load-bearing definitions ... in brief, adapted form" / "the active-atom
bridge stated ... and in the application paper").  This round aligns those
two sentences (plus the header comment) with the v19 reality: the
application paper carries only a Discussion-level pointer and is written
in measure-theoretic terms alone.

Anchored splices (each must apply exactly once):
  A. header Relation block: journal_manuscript_v11.tex -> v19 + new
     division-of-labor description + v11 round note
  B. intro "Relation to the application paper" paragraph: drop the
     "states the load-bearing definitions ... in brief, adapted form"
     clause
  C. future-directions item: "and in the application paper" ->
     "and instantiated measure-theoretically in the application paper"
  D. \\bibliography{companion_refs_v10} -> \\bibliography{companion_refs_v11}
     (companion_refs_v11.bib = byte-identical copy, per repo convention)

Numerical invariance: no digit-bearing token is touched; the audit tokens
(0.498, 0.853, +0.395, 424, -0.083, 366, 2.000, 1.00 companion-side
quotes) are asserted unchanged by count.
"""
import shutil, sys

BASE = "/home/z/my-project/metabolic-curvature-measure"
SRC = f"{BASE}/scripts/companion_categorical_v10.tex"
DST = f"{BASE}/scripts/companion_categorical_v11.tex"
BIB_SRC = f"{BASE}/scripts/companion_refs_v10.bib"
BIB_DST = f"{BASE}/scripts/companion_refs_v11.bib"

tex = open(SRC, encoding="utf-8").read()
orig = tex
applied = []


def rep(old, new, tag):
    global tex
    assert old in tex, f"ANCHOR NOT FOUND: {tag}"
    assert tex.count(old) == 1, f"ANCHOR NOT UNIQUE: {tag}"
    tex = tex.replace(old, new)
    applied.append(tag)


# ---- A. header: filename line + Relation block + v11 round note --------
rep(
    "%  companion_categorical_v9.tex -- standalone theory paper.",
    "%  companion_categorical_v11.tex -- standalone theory paper.",
    "A0 header filename line")

rep(
    """%  Relation:   the application paper (journal_manuscript_v11.tex)
%              states the load-bearing definitions of this
%              framework in brief adapted form and cites this
%              development for the constructions and proofs; this
%              paper cites the application paper where the empirical
%              line is concerned. Each paper is self-contained for
%              its own claims.""",
    """%  Relation:   the application paper (journal_manuscript_v19.tex)
%              cites this development for the constructions,
%              machine verifications, and proofs; after its v19
%              comprehension restructure the application paper is
%              written in measure-theoretic terms alone and carries
%              the relation only as a Discussion-level pointer
%              paragraph (its former brief adapted statement of the
%              categorical definitions was removed there and is
%              carried here alone); this paper cites the application
%              paper where the empirical line is concerned. Each
%              paper is self-contained for its own claims.
%  V11 alignment round (v10 -> v11): two cross-paper sentences
%              updated to the v19 division of labor (intro
%              "Relation to the application paper" paragraph and the
%              future-directions discretization-bridge item); every
%              numerical claim, theorem, proof, and section
%              unchanged; companion_refs_v11.bib byte-identical.""",
    "A1 header Relation block")

# ---- B. intro "Relation to the application paper" paragraph ------------
rep(
    """selection-rule robustness checks. The application paper states the load-bearing definitions
of the present framework in brief, adapted form and cites this
paper for the constructions, machine verifications, and proofs at
the status marked per result --- complete proofs for the gluing""",
    """selection-rule robustness checks. The application paper cites this
paper for the constructions, machine verifications, and proofs at
the status marked per result, recording the division of labor in
one Discussion paragraph --- complete proofs for the gluing""",
    "B intro relation paragraph")

# ---- C. future-directions discretization-bridge item -------------------
rep(
    """two --- the precise discretization correspondence behind the
active-atom bridge stated in Definition~\\ref{def:kv} and in the
application paper \\citep{zai2026measure} --- is open.""",
    """two --- the precise discretization correspondence behind the
active-atom bridge stated in Definition~\\ref{def:kv} and
instantiated measure-theoretically in the
application paper \\citep{zai2026measure} --- is open.""",
    "C future-directions bridge item")

# ---- D. bibliography pointer --------------------------------------------
rep("\\bibliography{companion_refs_v10}",
    "\\bibliography{companion_refs_v11}",
    "D bibliography pointer")

# ---- invariance assertions ----------------------------------------------
audit_tokens = ["0.498", "0.853", "+0.395", "424", "-0.083", "366",
                "2.000", "1.00", "zai2026measure"]
for t in audit_tokens:
    assert tex.count(t) == orig.count(t), \
        f"TOKEN COUNT CHANGED: {t} {orig.count(t)} -> {tex.count(t)}"
assert tex.count("0.711") == orig.count("0.711")
# removed stale phrases must be gone; new phrases present exactly once
assert "states the load-bearing definitions" not in tex
assert "and in the\napplication paper" not in tex
assert tex.count("recording the division of labor in\none Discussion paragraph") == 1
assert tex.count("instantiated measure-theoretically in the\napplication paper") == 1

open(DST, "w", encoding="utf-8").write(tex)
shutil.copyfile(BIB_SRC, BIB_DST)  # byte-identical, per repo convention

# diff summary for the log
import difflib
diff = list(difflib.unified_diff(orig.splitlines(), tex.splitlines(),
                                  "v10", "v11", lineterm="", n=0))
print("[companion_v11_alignment] splices applied:", "; ".join(applied))
print(f"[companion_v11_alignment] diff hunks: {sum(1 for l in diff if l.startswith('@'))}")
print(f"[companion_v11_alignment] wrote {DST} ({len(tex)} chars) + {BIB_DST} (byte-identical)")
print("[companion_v11_alignment] ALL CHECKS PASSED")
