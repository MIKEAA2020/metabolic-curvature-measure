#!/usr/bin/env python3
"""Patch H for companion_categorical_v3.tex (sixth-axis round, merged
with the remote's phosphate/iron lineage): prop:keio-atpm +
rem:keio-multiaxis insertion, tab:canonical-selection ATPM rows,
sec:canonical-selection fifth feature + integrity extension +
near-tie boundary, rem:canonical-protocol near-tie clause, and the
six-axis abstract (word-count asserted < 265 by the repo counter)."""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(REPO, "scripts", "companion_categorical_v3.tex")

src = open(TEX).read()
if "prop:keio-atpm" in src:
    print("patch H already applied -- nothing to do")
    sys.exit(0)
content_a = open(os.path.join(REPO, "scripts",
                             "patch_h_content_a.tex")).read()

# ---- 1. insert prop:keio-atpm + rem:keio-multiaxis before the
#         canonical-selection subsection -----------------------------
ANCHOR = ("\\subsection{Canonical Vertex Selection and "
          "Solver-Tolerance Integrity}")
assert src.count(ANCHOR) == 1
src = src.replace(ANCHOR, content_a + "\n" + ANCHOR, 1)

# ---- 2. extend tab:canonical-selection with the ATPM rows ----------
O_TAB_IJO = """iron $-0.0025$ & $-0.011$ & $+0.913$ & $0.988$ & $0.952$ \\\\
arginine $-10$ & $+0.802$ & $+0.953$ & $0.991$ & $0.978$ \\\\"""
N_TAB_IJO = """iron $-0.0025$ & $-0.011$ & $+0.913$ & $0.988$ & $0.952$ \\\\
arginine $-10$ & $+0.802$ & $+0.953$ & $0.991$ & $0.978$ \\\\
ATPM $\\ge 40$ & $+0.949$ & $+0.969$ & $1.000$ & $0.972$ \\\\
ATPM $\\ge 60$ & $+0.925$ & $+0.949$ & $0.988$ & $0.959$ \\\\
ATPM $\\ge 80$ & $+0.821$ & $+0.964$ & $0.982$ & $0.934$ \\\\
ATPM $\\ge 100$ & $+0.444$ & $+0.937$ & $0.991$ & $0.974$ \\\\"""
assert O_TAB_IJO in src
src = src.replace(O_TAB_IJO, N_TAB_IJO, 1)

O_TAB_IML = """iron $-0.0025$ & $-0.037$ & $+0.905$ & $0.986$ & $0.904$ \\\\
arginine $-10$ & $+0.915$ & $+0.850$ & $0.997$ & $0.993$ \\\\"""
N_TAB_IML = """iron $-0.0025$ & $-0.037$ & $+0.905$ & $0.986$ & $0.904$ \\\\
arginine $-10$ & $+0.915$ & $+0.850$ & $0.997$ & $0.993$ \\\\
ATPM $\\ge 60$ & $+0.747$ & $+0.703$ & $0.992$ & $0.980$ \\\\
ATPM $\\ge 80$ & $+0.435$ & $+0.655$ & $0.992$ & $0.960$ \\\\
ATPM $\\ge 100$ & $+0.244$ & $+0.476$ & $0.978$ & $0.868$ \\\\"""
assert O_TAB_IML in src
src = src.replace(O_TAB_IML, N_TAB_IML, 1)

O_CAP = """\\caption{Homogenized canonical-selection statistics across the five
perturbation axes (transitive calibration; $r$ is the Pearson"""
N_CAP = """\\caption{Homogenized canonical-selection statistics across the six
perturbation axes, medium-side and non-medium (transitive
calibration; $r$ is the Pearson"""
assert O_CAP in src
src = src.replace(O_CAP, N_CAP, 1)

# ---- 3. subsection intro: five -> six axes -------------------------
O_INTRO = """The nitrogen, phosphate, and iron probes left the plain-FBA
association readings collapsed on every level whose optimum is
carbon-degenerate, and the oxygen re-run was executed to make the
reported statistic identical in construction across all five axes
(the iron probe and the arginine-substitution levels were executed
under canonical selection from the outset)."""
N_INTRO = """The nitrogen, phosphate, and iron probes left the plain-FBA
association readings collapsed on every level whose optimum is
carbon-degenerate, the oxygen re-run was executed to make the
reported statistic identical in construction across all five
medium-side axes (the iron probe and the arginine-substitution
levels were executed under canonical selection from the outset),
and the sixth, non-medium maintenance-stress axis
(Proposition~\\ref{prop:keio-atpm}) extends the same construction --
with the refinement that its wild-type optima are carbon-unique
(phosphoglucose-isomerase width $0.0$ at every level) and the
plain arm still collapses at the extreme endpoints."""
assert O_INTRO in src
src = src.replace(O_INTRO, N_INTRO, 1)

# ---- 4. fifth feature paragraph after the "Fourth..." one -----------
O_FOURTH_END = """canonical rule is reported uniformly rather than cherry-picked
per level.

The canonical control also served as an independent audit"""
N_FOURTH_END = """canonical rule is reported uniformly rather than cherry-picked
per level. Fifth, the non-medium axis upgrades the degeneracy
reading itself: its wild-type optima are unique (widths $0.0$),
plain FBA is strong at moderate stress (above the baseline), and
the collapse appears only at the near-zero-biomass endpoints ---
so wild-level variability width is a sufficient but not necessary
indicator, the operative mechanism being per-knockout vertex
instability --- and the axis adds the one corner where canonical
selection is only partially sufficient: at elevated maintenance
demand the iML1515 parsimony stage itself carries \\emph{near-tied}
optima (vertices $\\approx200$ apart in the squared-flux metric
whose $L_1$ objectives differ by $8.6\\times10^{-4}$ absolute,
$1.2\\times10^{-6}$ relative --- within the simplex optimality
tolerance), so the returned canonical vertex is solver-path
dependent: $782$ of $1{,}129$ compensable knockouts record the
near-tie floor $kV\\approx200.01$ while the rest sit at $kV\\approx0$
(supply axes carry no floor; compensable medians $0.00$--$0.10$).
The floor decorrelates the transitive statistic on iML1515
($r$ caps near $+0.48$) without touching the essentiality ranking
(AUC $0.978$, labels $\\kappa=1.000$ at every level): canonical
selection is necessary everywhere and sufficient precisely where
the parsimony stage is discriminating.

The canonical control also served as an independent audit"""
assert O_FOURTH_END in src
src = src.replace(O_FOURTH_END, N_FOURTH_END, 1)

# ---- 5. integrity paragraph: extend to the ATPM adjudication -------
O_INTEG = r"""engine is the fallback for solver pathology at degenerate optima:
a plain LP that cycles indefinitely under one simplex
implementation is settled by the other, with the row marked as an
engine substitution in the deposited sweep."""
N_INTEG = r"""engine is the fallback for solver pathology at degenerate optima:
a plain LP that cycles indefinitely under one simplex
implementation is settled by the other, with the row marked as an
engine substitution in the deposited sweep. The sixth axis met
both requirements and one new boundary. Its sweeps run under a
simplex time limit (a handful of at-optimum $L_1$ LPs cycle
indefinitely at the deepest maintenance level; timed-out solves
fall back to the plain optimum vertex, label-preserving and
flagged per gene), and its endpoints sit at wild type $0.099$ and
$0.080$ --- inside the false-viability band --- so the cross-arm
scan was run there: six corrupted calls, all trace-quota genes
(the plain \emph{fabZ}/\emph{bioH} rows on iJO1366, the plain
\emph{bioD}/\emph{fabZ} and the canonical \emph{bioF}/\emph{fabI}
rows on iML1515), every one settled at biomass exactly zero by
the independent engine and corrected under the same conventions;
after correction the maintenance-stress re-stratification is
purely one-directional (energy-transduction gains only, no
losses) and the plain-versus-canonical arm agreement is
$\kappa=1.000$ at all seven levels of the axis. The new boundary
is the near-tie floor above: unlike the trace-quota calls, it is
not a corrupted reading but a property of the parsimony stage
itself, and it bounds the rule rather than violating it."""
assert O_INTEG in src
src = src.replace(O_INTEG, N_INTEG, 1)

# ---- 6. rem:canonical-protocol: near-tie clause ---------------------
O_PROTO = """Both requirements are
properties of the instrument, and the battery's reported
statistics now satisfy both."""
N_PROTO = """Both requirements are
properties of the instrument, and the battery's reported
statistics now satisfy both. A third requirement is measured, not
imposed: where the parsimony stage itself carries near-tied optima
--- the maintenance axis in iML1515, $\\Delta L_1$ at
$1.2\\times10^{-6}$ relative --- the canonical vertex is only
weakly determined and the transitive statistic must be read with
the near-tie floor in mind; the essentiality ranking is unaffected
(held-out AUC $\\ge0.978$), which is why the table's iML1515
maintenance rows are reported with their AUC and MCC intact."""
assert O_PROTO in src
src = src.replace(O_PROTO, N_PROTO, 1)

# ---- 7. abstract: five -> six axes ----------------------------------
O_ABS = """The validation battery is
medium-robust across five axes: carbon-source, oxygen, nitrogen,
phosphate, and iron perturbations leave the essentiality labels
invariant, re-stratifying only at regime switches; the
association is invariant under canonical flux selection."""
N_ABS = """The validation battery is
medium-robust across six axes: carbon, oxygen, nitrogen,
phosphate, and iron supply plus a non-medium maintenance stress
leave the essentiality labels invariant, re-stratifying only at
regime switches; the association is invariant under canonical
flux selection up to a measured near-degeneracy boundary."""
assert O_ABS in src
src = src.replace(O_ABS, N_ABS, 1)

# word-count discipline (repo counter), trims if needed
def wc(s):
    m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", s, re.S)
    b = re.sub(r"\\[a-zA-Z]+", " ", m.group(1))
    b = re.sub(r"[\\${}~]", " ", b)
    return len([w for w in b.split() if w != "---"])

n_words = wc(src)
TRIMS = [
    ("The companion paper\ndevelops the atomic curvature measure of parametric flux balance\nanalysis and its genome-scale validation.",
     "The companion paper\ndevelops the atomic curvature measure and its genome-scale\nvalidation."),
    ("theory with proof-sketch status marked.",
     "theory, proof-sketch status marked."),
    ("and establishes, for an explicit\nseven-map instantiation, a per-optic",
     "and establishes, for a\nseven-map instantiation, a per-optic"),
    ("an adapter-level optic statement and verified at scale;",
     "an adapter-level optic statement, verified at scale;"),
    ("iron supply plus a non-medium maintenance stress",
     "iron supply plus non-medium maintenance stress"),
    ("medium-robust across six axes",
     "robust across six axes"),
    ("sequences of\nindividually manageable changes accumulate",
     "sequences of\nmanageable changes accumulate"),
    ("threat through the policy holonomy they induce.",
     "threat through the holonomy they induce."),
    ("leave the essentiality labels invariant, re-stratifying only at",
     "leave the labels invariant, re-stratifying only at"),
]
for o, n in TRIMS:
    if n_words < 265:
        break
    if o in src:
        src = src.replace(o, n, 1)
        n_words = wc(src)
        print(f"trim applied ({n_words} words)")
assert n_words < 265, f"abstract too long: {n_words}"
print(f"abstract word count: {n_words} < 265")

with open(TEX, "w") as f:
    f.write(src)

for token in ["prop:keio-atpm", "rem:keio-multiaxis",
              "ATPM $\\ge 100$", "near-tie floor"]:
    assert token in src, f"missing {token}"
print("patch H applied: sixth-axis prop + multiaxis remark + table "
      "rows + subsection extensions + six-axis abstract")
