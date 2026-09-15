#!/usr/bin/env python3
"""Patch G on companion_categorical_v3.tex: fifth perturbation axis
(iron limitation) + arginine canonical symmetry + five-axis updates.

Edits:
  G1  abstract: four axes -> five axes (word-count neutral: ', and'
      -> ';' in the same sentence).
  G2  prop:keio-phosphate: 'the last classical macronutrient supply
      axis' -> 'the fourth ...' (iron extends the supply classes).
  G3  prop:keio-phosphate: fix the double-escaped \\emph / \\S\\ref
      rendering defect introduced by patch F (lines with bioC/bioF/
      bioH/fabZ).
  G4  rem:keio-p-invariance: macronutrient-side phrasing + 'all five
      axes' pointer.
  G5  NEW prop:keio-iron + rem:keio-iron-invariance (inserted before
      the canonical-selection subsection).
  G6  sec:canonical-selection intro: nitrogen/phosphate/iron; five
      axes; iron + arginine executed under canonical selection.
  G7  FVA signature sentence: iron included.
  G8  tab:canonical-selection: +3 iron rows (iJO), +1 arginine row
      (iJO), +2 iron rows (iML), +1 arginine row (iML) -> 25 levels;
      caption five axes.
  G9  post-table body: 'Three features' -> 'Four features'; restored
      range [+0.80,+0.96]; iron deepest-degeneracy sentence; fourth
      feature = arginine symmetry.
  G10 integrity paragraph: iron round extension (7,133 cross-arm
      comparisons, b0887 engine substitution).
  G11 rem:canonical-protocol: iron verification + engine-fallback
      clause.
  G12 'Propositions glucose-only--phosphate' range -> '--iron'.
"""
import re, sys

TEX = ("/home/z/my-project/metabolic-curvature-measure/scripts/"
       "companion_categorical_v3.tex")

src = open(TEX).read()


def apply(src, old, new, tag):
    n = src.count(old)
    assert n == 1, f"{tag}: expected exactly 1 occurrence, found {n}"
    print(f"  [ok] {tag}")
    return src.replace(old, new, 1)


# ---------------------------------------------------------------- G1
src = apply(
    src,
    """medium-robust across four axes: carbon-source, oxygen, nitrogen,
and phosphate perturbations leave the essentiality labels
invariant, re-stratifying only at regime switches, and the
association is invariant under canonical flux selection.""",
    """medium-robust across five axes: carbon-source, oxygen, nitrogen,
phosphate, and iron perturbations leave the essentiality labels
invariant, re-stratifying only at regime switches; the
association is invariant under canonical flux selection.""",
    "G1 abstract five axes (word-count neutral)")

# ---------------------------------------------------------------- G2
src = apply(
    src,
    """Limiting the inorganic-phosphate supply --- the last classical
macronutrient supply axis, and the purest test of the supply side:""",
    """Limiting the inorganic-phosphate supply --- the fourth classical
macronutrient supply axis, and the purest test of the supply side:""",
    "G2 phosphate 'fourth' not 'last'")

# ---------------------------------------------------------------- G3
src = apply(
    src,
    """trace-quota family --- \\\\emph{bioC}, \\\\emph{bioF}, \\\\emph{bioH}, and
the \\\\emph{fabZ} side-chain arm, all essential (independent-engine
adjudication; \\\\S\\\\ref{sec:canonical-selection}) --- so the
corrected label counts are the invariant ones above.""",
    """trace-quota family --- \\emph{bioC}, \\emph{bioF}, \\emph{bioH}, and
the \\emph{fabZ} side-chain arm, all essential (independent-engine
adjudication; \\S\\ref{sec:canonical-selection}) --- so the
corrected label counts are the invariant ones above.""",
    "G3 fix double-escaped emph/S/ref")

# ---------------------------------------------------------------- G4
src = apply(
    src,
    """With the phosphate axis the supply side of the invariance claim
closes: the four classical macronutrient supplies --- carbon""",
    """With the phosphate axis the macronutrient side of the supply claim
closes: the four classical macronutrient supplies --- carbon""",
    "G4a P-remark macronutrient side")
src = apply(
    src,
    """under any supply perturbation that preserves the growth regime, on
all four axes; re-stratification confined to the rewired module at""",
    """under any supply perturbation that preserves the growth regime, on
all five axes (iron: Proposition~\\ref{prop:keio-iron}); re-stratification confined to the rewired module at""",
    "G4b P-remark five axes")

# ---------------------------------------------------------------- G5
IRON_PROP = r"""
\begin{proposition}[Fifth perturbation axis: iron limitation]
\label{prop:keio-iron}
Limiting the ferrous-iron supply --- the trace-metal class, the last
classical nutrient supply after carbon source, electron acceptor,
nitrogen, and phosphate; iron pinned to the single ferrous channel
(the bound reaction $\mathrm{EX\_fe2\_e}$, the ferric channel
closed, the closure leaving the wild-type optimum unchanged to
solver noise) --- with the glucose-only medium otherwise unchanged
and labels declared at $5\%$ of each level's own wild type, gives
on iJO1366 $\mathrm{EX\_fe2\_e}\in\{-0.01,-0.005,-0.0025\}$
(wild-type optima $0.623$, $0.311$, $0.156$ --- $37\%$, $68\%$,
$84\%$ reductions; the parsimonious unlimited requirement is
$0.0158$ mmol/gDW/h, fixing the informative range; zinc and
manganese, the alternative trace metals, compress their informative
bands to the $10^{-4}$ bound scale and were rejected by the same
pre-screen) and on iML1515 $\{-0.005,-0.0025\}$ ($0.311$, $0.156$
--- $62\%$ and $81\%$ reductions). The pre-screen also exposes a
structural fact: the iron dose response is identical on the two
reconstructions to six decimals --- both biomass equations carry
the same iron quota, so $b=\mathrm{fe2}/0.0161$: a pure linear
biomass-quota scaling, every iron demand scaling with growth, with
no assimilation pathway to reroute (the trace-metal counterpart of
the quota purity that made phosphate the cleanest macronutrient
axis). The essentiality labels are invariant at every level on
both reconstructions: $289/1{,}367$ on iJO1366 and $286/1{,}516$
on iML1515, zero flips, Cohen's $\kappa=1.000$ throughout, the
label-based strata unchanged. The association replicates the
phosphate pattern in full: every iron-limited optimum is
carbon-degenerate (at-optimum phosphoglucose-isomerase FVA width
$103$/$162$/$192$ on iJO1366 and $139$/$176$ on iML1515 against
$0.0$ at the baseline; the parsimonious wild type takes up
$6.5$/$3.3$/$1.7$ glucose where the returned plain vertices take
$10.0$/$9.3$/$5.0$), the plain-FBA statistics collapse with the
degeneracy depth ($r=+0.518$, $+0.303$, $-0.011$ on iJO1366;
$+0.127$, $-0.037$ on iML1515; AUCs down to $0.522$), and
canonical vertex selection restores them everywhere: $r=+0.957$,
$+0.800$, $+0.913$ on iJO1366 and $+0.843$, $+0.905$ on iML1515
(AUCs $0.988$/$0.986$; MCC $0.965$/$0.904$; canonical ranking
correlated $+0.63$ to $+0.85$ with the baseline canonical ranking;
labels $\kappa=1.000$ by construction). One plain LP at the
deepest level (the cysteine/glutathione ABC-exporter ATPase
\texttt{b0887}, non-essential) hangs under GLPK simplex cycling;
it was settled by the independent engine under both arm
conventions, the row disclosed as an engine substitution
(\S\ref{sec:canonical-selection}). The deepest levels (wild type
$0.156$, above the $0.14$ tolerance boundary) were
integrity-scanned by cross-arm agreement: $0$ discrepancies in
$7{,}133$ gene-level biomass comparisons across the five levels,
no gene in the false-viability band on either arm, zero corrupted
calls.
\end{proposition}

\begin{remark}[What the fifth axis closes]
\label{rem:keio-iron-invariance}
With the trace-metal axis the supply side of the invariance claim
closes across all five classical nutrient classes --- carbon
source, electron acceptor, nitrogen, phosphate, iron: no supply
perturbation that preserves the growth regime moves one gene
across the $5\%$ relative line in either reconstruction
($289/1{,}367$ and $286/1{,}516$ at every level of every axis;
zero flips, $\kappa=1.000$), down to the deepest levels probed
($89\%$ wild-type reduction on phosphate, $84\%$ on iron). Beyond
the count, the iron axis adds two structural facts. First, quota
purity: because the two reconstructions share the iron quota
constant, the axis collapses both media onto one identical linear
dose response --- even phosphate, whose unlimited uptake differs
($0.948$ against $0.793$), does not do that --- making iron the
purest supply perturbation of the battery. Second, the gradient's
floor is set by arithmetic, not biology: the deepest iron level
sits at wild type $0.156$, deliberately above the $0.14$
trace-quota tolerance boundary of \S\ref{sec:canonical-selection},
and the cross-arm scan verifies it clean ($0$ discrepancies in
$7{,}133$ comparisons); pushing to the next pre-screen level
($94\%$ reduction, wild type $0.062$) would place every
trace-quota call inside the tolerance zone and convert the label
invariance claim into an adjudication exercise, so the axis stops
where the instrument is still exact.
\end{remark}

\subsection{Canonical Vertex Selection and Solver-Tolerance Integrity}"""

src = apply(
    src,
    r"""only where the optimum is unique (carbon- or oxygen-limited).
\end{remark}

\subsection{Canonical Vertex Selection and Solver-Tolerance Integrity}""",
    r"""only where the optimum is unique (carbon- or oxygen-limited).
\end{remark}
""" + IRON_PROP,
    "G5 insert prop:keio-iron + rem:keio-iron-invariance")

# ---------------------------------------------------------------- G6
src = apply(
    src,
    """The nitrogen and phosphate probes left the plain-FBA association
readings collapsed on every level whose optimum is carbon-degenerate,
and the oxygen re-run was executed to make the reported statistic
identical in construction across all four axes. The finding is a""",
    """The nitrogen, phosphate, and iron probes left the plain-FBA
association readings collapsed on every level whose optimum is
carbon-degenerate, and the oxygen re-run was executed to make the
reported statistic identical in construction across all five axes
(the iron probe and the arginine-substitution levels were executed
under canonical selection from the outset). The finding is a""",
    "G6 sec intro five axes")

# ---------------------------------------------------------------- G7
src = apply(
    src,
    """signature separates the regimes cleanly: phosphoglucose-isomerase
range $0.0$ at the carbon-limited baseline and $4.3$ under oxygen
limitation, against $45$--$201$ at every nitrogen- and
phosphate-limited level.""",
    """signature separates the regimes cleanly: phosphoglucose-isomerase
range $0.0$ at the carbon-limited baseline and $4.3$ under oxygen
limitation, against $45$--$201$ at every nitrogen-, phosphate-,
and iron-limited level.""",
    "G7 FVA signature includes iron")

# ---------------------------------------------------------------- G8
src = apply(
    src,
    """phosphate $-0.1$ & $-0.067$ & $+0.914$ & $0.988$ & $0.952$ \\\\
\\multicolumn{5}{l}{\\emph{iML1515}}\\\\""",
    """phosphate $-0.1$ & $-0.067$ & $+0.914$ & $0.988$ & $0.952$ \\\\
iron $-0.01$ & $+0.518$ & $+0.957$ & $0.988$ & $0.965$ \\\\
iron $-0.005$ & $+0.303$ & $+0.800$ & $0.988$ & $0.965$ \\\\
iron $-0.0025$ & $-0.011$ & $+0.913$ & $0.988$ & $0.952$ \\\\
arginine $-10$ & $+0.802$ & $+0.953$ & $0.991$ & $0.978$ \\\\
\\multicolumn{5}{l}{\\emph{iML1515}}\\\\""",
    "G8a table iJO iron+arg rows")
src = apply(
    src,
    """phosphate $-0.1$ & $+0.090$ & $+0.900$ & $0.986$ & $0.904$ \\\\
\\hline
\\end{tabular}""",
    """phosphate $-0.1$ & $+0.090$ & $+0.900$ & $0.986$ & $0.904$ \\\\
iron $-0.005$ & $+0.127$ & $+0.843$ & $0.986$ & $0.904$ \\\\
iron $-0.0025$ & $-0.037$ & $+0.905$ & $0.986$ & $0.904$ \\\\
arginine $-10$ & $+0.915$ & $+0.850$ & $0.997$ & $0.993$ \\\\
\\hline
\\end{tabular}""",
    "G8b table iML iron+arg rows")
src = apply(
    src,
    """\\caption{Homogenized canonical-selection statistics across the four
perturbation axes (transitive calibration; $r$ is the Pearson""",
    """\\caption{Homogenized canonical-selection statistics across the five
perturbation axes (transitive calibration; $r$ is the Pearson""",
    "G8c caption five axes")

# ---------------------------------------------------------------- G9
src = apply(
    src,
    """statistics. Three features matter. First, canonical selection""",
    """statistics. Four features matter. First, canonical selection""",
    "G9a Three->Four features")
src = apply(
    src,
    """the canonical rule removes. Second, the association is restored at
every degenerate level of both nitrogen and phosphate axes
($r\\in[+0.87,+0.95]$, AUC $\\ge 0.979$, MCC $\\ge 0.904$). Third ---""",
    """the canonical rule removes. Second, the association is restored at
every degenerate level of the nitrogen, phosphate, and iron axes
($r\\in[+0.80,+0.96]$, AUC $\\ge 0.979$, MCC $\\ge 0.904$); the
iron axis replicates the full collapse-and-restore pattern at the
deepest degeneracy yet recorded (plain $r$ down to $-0.011$
(iJO1366) and $-0.037$ (iML1515) against
phosphoglucose-isomerase ranges of $192$/$176$, canonical
$+0.913$/$+0.905$). Third ---""",
    "G9b restored range + iron sentence")
src = apply(
    src,
    """labels only (six glycolysis gains); the apparent collapse of the
association at the switch was vertex-conditioning, not biology.""",
    """labels only (six glycolysis gains); the apparent collapse of the
association at the switch was vertex-conditioning, not biology.
Fourth, the substitution side is now symmetric with the limitation
side: the arginine levels --- run under canonical selection to
complete the table --- confirm that where the substituted optimum
is carbon-re-pinned and unique, the plain reading was already well
posed (iML1515: plain $+0.915$, canonical $+0.850$, AUC $0.997$,
MCC $0.993$; iJO1366 sharpens $+0.802$ to $+0.953$), so the
canonical rule is reported uniformly rather than cherry-picked
per level.""",
    "G9c fourth feature (arginine symmetry)")

# ---------------------------------------------------------------- G10
src = apply(
    src,
    """precision (the three iJO1366 biotin knockouts share the identical
canonical curvature $164.975$; the three iML1515 ones $253.551$).""",
    """precision (the three iJO1366 biotin knockouts share the identical
canonical curvature $164.975$; the three iML1515 ones $253.551$).
The iron round extends the audit to the fifth axis. Its deepest
levels sit at wild type $0.156$ --- between the $0.14$ corruption
boundary and the $0.23$ sufficiency margin, the one band the
phosphate round had not sampled --- so the level was verified
directly: cross-arm agreement over all five iron levels gives $0$
discrepancies in $7{,}133$ gene-level biomass comparisons (maximum
$|{\\Delta b}| = 6\\times10^{-8}$), no gene lands in the
false-viability band on either arm, and the trace-quota family
reads exactly zero on iJO1366. The round also met a new solver
pathology at a degenerate optimum: one plain LP (the
cysteine/glutathione ABC-exporter ATPase \\texttt{b0887},
non-essential) hangs under GLPK simplex cycling, and was settled
under the independent HiGHS rule in both arms, the row disclosed
as an engine substitution in the deposited sweeps.""",
    "G10 iron round audit extension")

# ---------------------------------------------------------------- G11
src = apply(
    src,
    """family (biotin, quinone side chain, lipoate) is exactly the
at-risk set, and a second engine settling the LP is sufficient.
Both requirements are properties of the instrument, and the
battery's reported statistics now satisfy both.""",
    """family (biotin, quinone side chain, lipoate) is exactly the
at-risk set, and a second engine settling the LP is sufficient ---
as the iron levels at wild type $0.156$ verify directly ($0$
discrepancies in $7{,}133$ cross-arm comparisons). The same second
engine is the fallback for solver pathology at degenerate optima:
a plain LP that cycles indefinitely under one simplex
implementation is settled by the other, with the row marked as an
engine substitution in the deposited sweep. Both requirements are
properties of the instrument, and the battery's reported
statistics now satisfy both.""",
    "G11 rem:canonical-protocol extension")

# ---------------------------------------------------------------- G12
src = apply(
    src,
    """Propositions~\\ref{prop:keio-glucose-only}--\\ref{prop:keio-phosphate},""",
    """Propositions~\\ref{prop:keio-glucose-only}--\\ref{prop:keio-iron},""",
    "G12 proposition range to iron")

# ---------------------------------------------------------------- write
open(TEX, "w").write(src)

# abstract word-count neutrality check (crude whitespace tokens)
m = re.search(r"\\begin\{minipage\}.*?\\end\{minipage\}", src, re.S)
plain = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})*", " ", m.group(0))
plain = re.sub(r"[{}\\$%&^_~]", " ", plain)
toks = [t for t in plain.split() if re.search(r"[A-Za-z0-9]", t)]
print(f"\nabstract token count after patch: {len(toks)}")
assert "\\\\emph" not in src and "\\\\S\\\\ref" not in src, \
    "double-escape defect still present!"
print("PATCH G APPLIED CLEANLY.")
