#!/usr/bin/env python3
"""Build journal_manuscript_v17.tex from journal_manuscript_v16.tex
(V17 enrichment round, per download/V17_Revision_Plan.md Parts A/B
and the computed ledger download/v17_insight_substantiation.json).

New files only: v16 is read, never written. The new manuscript adds:
  - Sec 2.6   A worked example (machine-verified)
  - Sec 4     The chemical coordinates of the walls (Table tab:walls)
              + A conserved interior architecture
              + Construction order as a design variable
  - Sec 5     Anatomy of one switch (Table tab:regulons,
              growth-silent partition)
  - Discussion: Relation to metabolic control analysis
              + Where metabolic memory lives
  - Abstract: bio-anchoring at the 255-word cap (254)
  - Intro: plan-of-the-paper paragraph updated
  - Limitations: item 8 (enrichment and prediction provenance)
  - Methods: enrichment/statistics protocols + worked-example
              verification; audit count placeholder AUDITCOUNT
  - refs: journal_manuscript_v17_bmb_refs.tex (+kacser1973,
              +heinrich1974)
All new numbers come from download/v17_insight_substantiation.json
and download/v17_worked_example_verification.json.
"""
import re

SRC = "scripts/journal_manuscript_v16.tex"
DST = "scripts/journal_manuscript_v17.tex"

tex = open(SRC).read()
frag = lambda name: open(f"scripts/{name}").read()

def splice(anchor, insert, before=True):
    global tex
    assert anchor in tex, f"anchor not found: {anchor[:70]!r}"
    assert tex.count(anchor) == 1, f"anchor not unique: {anchor[:70]!r}"
    tex = tex.replace(anchor,
                      (insert + "\n" + anchor) if before else
                      (anchor + "\n" + insert))

# ------------------------------------------------------------------
# 1. Header comment (v17 note, appended to the changelog block)
# ------------------------------------------------------------------
hdr_anchor = "%  Merged-register round (v14 -> v15):"
v17_hdr = """%  V17 enrichment round (v16 -> v17), per the V17 revision plan
%  (download/V17_Revision_Plan.md, commits 4776f2d + 74934d0) and
%  its computed insight ledger (download/v17_insight_substantiation.json
%  by scripts/v17_insight_substantiation.py): Sec. 2 gains a
%  hand-checkable worked example (machine-verified by
%  scripts/v17_worked_example_verify.py); Sec. 4 gains the chemical
%  coordinates of the walls (Table), a conserved interior
%  architecture, and the construction-order design rule; Sec. 5
%  gains the anatomy of one switch (regulon/operon enrichment
%  Table + growth-silent partition); the Discussion gains the
%  metabolic-control-analysis comparison and the memory-substrate
%  deduction; the abstract gains the bio-anchoring sentences at the
%  255-word cap; references gain kacser1973 and heinrich1974.
%  Every new number is computed from deposited artifacts and
%  covered by audit_v25_numbers.py (344/344). v16 and all earlier
%  versions untouched.
"""
splice(hdr_anchor, v17_hdr, before=True)

# ------------------------------------------------------------------
# 2. Abstract (full replacement, 254 audit-style words)
# ------------------------------------------------------------------
ab_start = tex.index("\\begin{abstract}")
ab_end = tex.index("\\end{abstract}") + len("\\end{abstract}")
old_ab = tex[ab_start:ab_end]
new_ab = "\\begin{abstract}\n\\noindent\n" + \
    frag("v17_frag_abstract_full.tex").strip() + \
    "\n\\end{abstract}"
tex = tex[:ab_start] + new_ab + tex[ab_end:]

# ------------------------------------------------------------------
# 3. Intro: plan-of-the-paper paragraph
# ------------------------------------------------------------------
old_plan = """\\paragraph{Plan of the paper.}
Section~\\ref{sec:measure} defines the measure and the metric, develops
the value-layer structure and the value--flux coupling, and records the
categorical reading in brief. Section~\\ref{sec:theoremB} states the
refinement--resolution bridge. Section~\\ref{sec:computational} reports
the computational validation of the geometric claims, and
Section~\\ref{sec:empirical} the empirical association and the
protein-layer decision. Section~\\ref{sec:discussion} discusses
limitations and scope. The Methods, a disambiguation table for
colliding gene counts, and the proofs complete the paper."""
new_plan = """\\paragraph{Plan of the paper.}
Section~\\ref{sec:measure} defines the measure and the metric, develops
the value-layer structure and the value--flux coupling, works a
hand-checkable example, and records the categorical reading in brief.
Section~\\ref{sec:theoremB} states the
refinement--resolution bridge. Section~\\ref{sec:computational} reports
the computational validation of the geometric claims --- where the
curvature mass sits chemically, the interior architecture it defines,
and a construction-order rule for genotype design --- and
Section~\\ref{sec:empirical} the empirical association, the anatomy of
one switch, and the protein-layer decision.
Section~\\ref{sec:discussion} positions the framework against smooth
sensitivity theory, develops the memory-substrate deduction, and
discusses limitations and scope. The Methods, a disambiguation table for
colliding gene counts, and the proofs complete the paper."""
assert old_plan in tex, "plan-of-the-paper paragraph not found"
tex = tex.replace(old_plan, new_plan)

# ------------------------------------------------------------------
# 4. Sec 2: worked example (before the categorical reading)
# ------------------------------------------------------------------
splice("\\subsection{The categorical reading, in brief}\\label{sec:categorical}",
       frag("v17_frag_worked_example.tex").strip())

# ------------------------------------------------------------------
# 5. Sec 4: wall coordinates + interior architecture (after the
#    M1 figures, before double-knockout epistasis)
# ------------------------------------------------------------------
splice("\\subsection{Double-knockout epistasis and path dependence}",
       frag("v17_frag_walls_interior.tex").strip())

# ------------------------------------------------------------------
# 6. Sec 4: construction order (before the regime dial)
# ------------------------------------------------------------------
splice("\\subsection{Regime dial}",
       frag("v17_frag_order.tex").strip())

# ------------------------------------------------------------------
# 7. Sec 5: anatomy of one switch (before the layer decision)
# ------------------------------------------------------------------
splice("\\subsection{The layer decision}",
       frag("v17_frag_anatomy.tex").strip())

# ------------------------------------------------------------------
# 8. Discussion: MCA (before why-growth-fails)
# ------------------------------------------------------------------
splice("\\subsection{Why growth rate fails to predict gene expression}",
       frag("v17_frag_mca.tex").strip())

# ------------------------------------------------------------------
# 9. Discussion: memory (before the Limitations paragraph)
# ------------------------------------------------------------------
splice("\\paragraph{Limitations.}",
       frag("v17_frag_memory.tex").strip())

# ------------------------------------------------------------------
# 10. Limitations: item 8
# ------------------------------------------------------------------
old_lim = """\\item \\textbf{Stabilization limits.} The sweep arm of the
      stabilization experiment is panel-limited (thirteen sweep
      families, two of them affine --- the finite-population
      correction is part of the reported result), and the
      two-dimensional arm is floor-limited at large panels by the
      transport-LP atom cap.
\\end{enumerate}"""
new_lim = """\\item \\textbf{Stabilization limits.} The sweep arm of the
      stabilization experiment is panel-limited (thirteen sweep
      families, two of them affine --- the finite-population
      correction is part of the reported result), and the
      two-dimensional arm is floor-limited at large panels by the
      transport-LP atom cap.
\\item \\textbf{Enrichment and prediction provenance.} The regulon and
      operon enrichment of \\S\\ref{sec:anatomy} is correlational and
      shares the parent association's confound structure; the
      metabolomics, cross-species, and effector statements of
      \\S\\S\\ref{sec:walls}--\\ref{sec:memory} are predictions, labeled
      as such and untested here.
\\end{enumerate}"""
assert old_lim in tex, "limitations item 7 anchor not found"
tex = tex.replace(old_lim, new_lim)

# ------------------------------------------------------------------
# 11. Methods: enrichment protocols + audit-count placeholder
# ------------------------------------------------------------------
old_meth = """protocol with TPM log-fold changes. Every manuscript number traces
to a deposited artifact file and is re-derived by the automated
numeric verification described under Reproducibility ($301$
checks)."""
new_meth = """protocol with TPM log-fold changes. The enrichment statistics of
\\S\\ref{sec:anatomy} use Fisher exact tests of the top-$\\kmu$
quartile against PRECISE regulatory annotations with the panel as
background, Benjamini--Hochberg corrected across the testable sets
($31$ regulons, $31$ operons, $18$ iModulons); the
within-versus-across-operon curvature gap and its disjoint-reaction
GPR control use $5{,}000$-fold label permutation ($p$ reported as
$< 2 \\times 10^{-4}$). The wall-coordinate, class-share, and
order-rule statistics of \\S\\S\\ref{sec:walls}--\\ref{sec:order}
aggregate the deposited per-reaction curvature masses of the eleven
boundary-crossing M1 sweeps (each normalized by its own total) and
the deposited M3 double-mutant panels, with $10^4$-fold class-label
permutation for the class shares. The worked example of
\\S\\ref{sec:example} is machine-verified by LP re-solves at
wall-straddling parameter values under both tie-break variants.
Every manuscript number traces
to a deposited artifact file and is re-derived by the automated
numeric verification described under Reproducibility
($344$ checks)."""
assert old_meth in tex, "statistical-protocols anchor not found"
tex = tex.replace(old_meth, new_meth)

old_rep = """An automated suite of $301$ numeric checks
re-derives every manuscript number from the deposited artifacts and
is re-runnable end-to-end."""
new_rep = """An automated suite of $344$ numeric checks
re-derives every manuscript number from the deposited artifacts and
is re-runnable end-to-end."""
assert old_rep in tex, "reproducibility anchor not found"
tex = tex.replace(old_rep, new_rep)

# ------------------------------------------------------------------
# 12. Refs file pointer
# ------------------------------------------------------------------
old_inp = "\\input{journal_manuscript_v16_bmb_refs}"
new_inp = "\\input{journal_manuscript_v17_bmb_refs}"
assert old_inp in tex
tex = tex.replace(old_inp, new_inp)

open(DST, "w").write(tex)
print(f"{DST} written: {len(tex)} chars, "
      f"{tex.count(chr(10))} lines")

# ------------------------------------------------------------------
# 13. Refs file: v16 refs + kacser1973 + heinrich1974
# ------------------------------------------------------------------
refs = open("scripts/journal_manuscript_v16_bmb_refs.tex").read()
refs = refs.replace("% journal_manuscript_v8_bmb_refs.tex -- references for the v8",
                    "% journal_manuscript_v17_bmb_refs.tex -- references for the v17")
refs = refs.replace("\\begin{thebibliography}{27}",
                    "\\begin{thebibliography}{29}")
he = """\\bibitem[Heinrich and Rapoport(1974)]{heinrich1974}
Heinrich R, Rapoport TA (1974) A linear steady-state treatment of enzymatic chains: general
             properties, control and effector strength. European Journal of Biochemistry 42: 89--95.
"""
ka = """\\bibitem[Kacser and Burns(1973)]{kacser1973}
Kacser H, Burns JA (1973) The control of flux. Symposia of the Society for Experimental Biology 27: 65--104.
"""
# alphabetical insertion: Heinrich after Gutiérrez, before Huangfu;
# Kacser after Ibarra, before Kochanowski.
anchor_he = "\\bibitem[Huangfu and Hall(2018)]{huangfu2018}"
anchor_ka = "\\bibitem[Kochanowski et~al.(2013)]{kochanowski2013}"
assert anchor_he in refs and anchor_ka in refs
refs = refs.replace(anchor_he, he + anchor_he)
refs = refs.replace(anchor_ka, ka + anchor_ka)
open("scripts/journal_manuscript_v17_bmb_refs.tex", "w").write(refs)
print("scripts/journal_manuscript_v17_bmb_refs.tex written:",
      refs.count("\\bibitem"), "entries")
