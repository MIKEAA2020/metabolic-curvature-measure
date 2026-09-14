#!/usr/bin/env python3
"""Patch F: fourth-axis (phosphate) + canonical-selection subsection +
solver-integrity corrections, per the user's three-part directive.

Edits (companion_categorical_v3.tex, live head):
  F1  prop:keio-o2-limited anaerobic endpoint: corrected numbers
      (+6/-0 after the fabZ solver-tolerance correction) + pointer.
  F2  rem:keio-o2-invariance: fabZ sentence corrected (essential in
      every regime); regime-switch degradation qualified (plain
      reading; canonical restored across the switch).
  F3  rem:keio-n-invariance: 'completes a three-axis bracket' ->
      'extends the bracket to a third axis'.
  F4  NEW prop:keio-phosphate (fourth axis) + rem:keio-p-invariance
      (four-axis completion), inserted before the E14 subsection.
  F5  NEW subsection sec:canonical-selection (canonical vertex
      selection and solver-tolerance integrity) with the homogenized
      18-level table.
  F6  Abstract: 'three axes' -> four axes (+phosphate).
"""
import re, sys

TEX = "scripts/companion_categorical_v3.tex"
src = open(TEX).read()
orig = src

def sub(old, new, tag):
    global src
    assert old in src, f"{tag}: anchor not found"
    assert src.count(old) == 1, f"{tag}: anchor not unique"
    src = src.replace(old, new)
    print(f"{tag}: ok")

# ---------------------------------------------------------------------
# F1: prop:keio-o2-limited anaerobic endpoint
# ---------------------------------------------------------------------
sub(
"""non-degenerate endpoint: $286\\to291$ labels, six gains
(\\emph{eno}, \\emph{pgk}, \\emph{gapA}, \\emph{gpmA}, \\emph{gpmM},
\\emph{hemN}) and one loss (\\emph{fabZ}), $\\kappa=0.985$, Jaccard
$0.976$, five of the seven flips in glycolysis/gluconeogenesis (a
thirty-fold enrichment over the genome share); the transitive
calibration falls to $r=+0.260$ (AUC $0.672$), the direct arm to
$r=+0.118$ (AUC $0.673$), and the model-gap set is unchanged at
$13$.""",
"""non-degenerate endpoint: $286\\to292$ labels, six gains
(\\emph{eno}, \\emph{pgk}, \\emph{gapA}, \\emph{gpmA}, \\emph{gpmM},
\\emph{hemN}) and no losses, $\\kappa=0.987$, Jaccard $0.980$, five
of the six flips in glycolysis/gluconeogenesis (a thirty-fold
enrichment over the genome share); the transitive calibration falls
to $r=+0.258$ (AUC $0.682$), the direct arm to $r=+0.125$ (AUC
$0.673$), and the model-gap set is $12$. (The deposited endpoint
additionally recorded a loss of \\emph{fabZ}; the fresh-solve and
independent-engine adjudication of
\\S\\ref{sec:canonical-selection} showed that call to be a
solver-tolerance artifact --- \\emph{fabZ} is essential in every
regime through OGMEACPD/OPMEACPD, the sole route to the ubiquinone
side chain, a biomass requirement that every regime carries.)""",
"F1 prop:keio-o2-limited endpoint")

# ---------------------------------------------------------------------
# F2: rem:keio-o2-invariance fabZ sentence + degradation qualifier
# ---------------------------------------------------------------------
sub(
"""strictly lethal anaerobically ---
\\emph{hemN}'s oxygen-independent heme route becomes required (its
aerobic knockout is exactly neutral; the oxygen-dependent route
covers), and the single loss \\emph{fabZ} traces to its two
quinone-side-chain dehydratase reactions (OGMEACPD/OPMEACPD, its
only reactions without a \\emph{fabA} alternative; restoring exactly
those two restores the aerobic optimum $0.822$), not to its
fatty-acid role. The label set thus carries the environmental
regime, and the association degrades precisely when the regime
changes --- so the bimodal-ratio mechanism of""",
"""strictly lethal anaerobically ---
\\emph{hemN}'s oxygen-independent heme route becomes required (its
aerobic knockout is exactly neutral; the oxygen-dependent route
covers), and no gene is lost: the deposited \\emph{fabZ} loss was a
solver-tolerance artifact (\\S\\ref{sec:canonical-selection});
\\emph{fabZ} is essential in every regime through its two
quinone-side-chain dehydratase reactions (OGMEACPD/OPMEACPD, its
only reactions without a \\emph{fabA} alternative; restoring exactly
those two restores the aerobic optimum $0.822$) --- the sole route
to a biomass requirement that every regime carries. The label set
thus carries the environmental regime, and the plain-vertex
association reading degrades precisely when the regime changes
(under canonical selection the association is restored across the
switch: \\S\\ref{sec:canonical-selection}) --- so the bimodal-ratio
mechanism of""",
"F2 rem:keio-o2-invariance")

# ---------------------------------------------------------------------
# F3: rem:keio-n-invariance bracket phrasing
# ---------------------------------------------------------------------
sub(
"""completes a three-axis bracket --- carbon, electron acceptor,
nitrogen --- and its boundary acquires both sides.""",
"""extends the bracket to a third axis --- carbon, electron acceptor,
nitrogen --- and its boundary acquires both sides.""",
"F3 rem:keio-n-invariance phrasing")

# ---------------------------------------------------------------------
# F4 + F5: new prop, remark, and subsection before the E14 subsection
# ---------------------------------------------------------------------
NEW_BLOCK = r"""\begin{proposition}[Fourth perturbation axis: phosphate limitation]
\label{prop:keio-phosphate}
Limiting the inorganic-phosphate supply --- the last classical
macronutrient supply axis, and the purest test of the supply side:
phosphate enters the biomass directly (as the ester phosphate of
nucleic acids, phospholipids, and the energy currency), with no
assimilation pathway to rewire, so a limitation gradient scales one
biomass component while leaving every route topology intact ---
with the glucose-only medium otherwise unchanged and labels declared
at $5\%$ of each level's own wild type, gives on iJO1366
$\mathrm{EX\_pi\_e}\in\{-0.5,-0.25,-0.1\}$ (wild-type optima
$0.518$, $0.259$, $0.104$ --- $47\%$, $74\%$, $89\%$ reductions; the
unlimited uptake is $0.948$, fixing the informative range; sulfur,
the alternative fourth axis, compresses to a single informative
level at its $0.25$ uptake and was rejected by the same pre-screen)
and on iML1515 $\{-0.25,-0.1\}$ ($0.259$, $0.104$). The
essentiality labels are invariant at every level on both
reconstructions: $289/1{,}367$ on iJO1366 and $286/1{,}516$ on
iML1515, zero flips, Cohen's $\kappa=1.000$ throughout, the
label-based strata unchanged. The association behaves exactly as
the nitrogen axis predicted: every phosphate-limited optimum is
carbon-degenerate (at-optimum phosphoglucose-isomerase FVA width
$123$/$172$/$201$ on iJO1366 against $0.0$ at the baseline and
$4.3$ under oxygen limitation; the parsimonious wild type takes up
$5.4$/$2.8$/$1.2$ glucose where the returned plain vertices take
$10.0$/$7.9$/$3.7$), and the plain-FBA statistics collapse with the
degeneracy depth ($r=+0.323$, $+0.054$, $-0.067$ on iJO1366;
$+0.025$, $+0.090$ on iML1515; AUCs down to $0.506$), while
canonical vertex selection restores them everywhere: $r=+0.950$,
$+0.916$, $+0.914$ on iJO1366 and $+0.910$, $+0.900$ on iML1515
(AUCs $0.988$/$0.986$; MCC $0.965$/$0.904$; canonical ranking
correlated $+0.765$ to $+0.968$ with the baseline canonical
ranking; labels $\kappa=1.000$ by construction). Three plain calls
and one canonical call at the deepest level ($\mathrm{Pi}$ $-0.1$,
wild type $0.104$) were solver-tolerance artifacts of the biotin
trace-quota family --- \\emph{bioC}, \\emph{bioF}, \\emph{bioH}, and
the \\emph{fabZ} side-chain arm, all essential (independent-engine
adjudication; \\S\\ref{sec:canonical-selection}) --- so the
corrected label counts are the invariant ones above.
\end{proposition}

\begin{remark}[What the fourth axis closes]
\label{rem:keio-p-invariance}
With the phosphate axis the supply side of the invariance claim
closes: the four classical macronutrient supplies --- carbon
source, electron acceptor, nitrogen, phosphate --- have now each
been limited by up to $89\%$ of the wild-type optimum, and not one
supply perturbation moves a gene across the $5\%$ relative line in
either reconstruction ($289/1{,}367$ and $286/1{,}516$ at every
level of every axis; zero flips, $\kappa=1.000$). Re-stratification
appears only where the perturbation changes the growth mode, not
the supply level: the anaerobic switch (six glycolysis gains on
iML1515, no losses after the tolerance correction) and the
organic-nitrogen substitutions (losses confined to the rewired
assimilation module). The phosphate axis adds the quota-scaling
isolation: because phosphate cannot be rerouted, the axis
background-variation is pure biomass-component scaling --- which is
precisely what exposed the trace-quota boundary of
\S\ref{sec:canonical-selection} (the biotin and quinone side-chain
drains scale with growth and fall toward the solver's feasibility
tolerance at low wild-type optima). The medium-robustness statement
of the battery is therefore fourfold: essentiality labels invariant
under any supply perturbation that preserves the growth regime, on
all four axes; re-stratification confined to the rewired module at
a regime switch or source substitution; the association invariant
under canonical selection at every level of every axis (and across
the anaerobic switch itself); and plain-FBA readings meaningful
only where the optimum is unique (carbon- or oxygen-limited).
\end{remark}

\subsection{Canonical Vertex Selection and Solver-Tolerance Integrity}
\label{sec:canonical-selection}

The nitrogen and phosphate probes left the plain-FBA association
readings collapsed on every level whose optimum is carbon-degenerate,
and the oxygen re-run was executed to make the reported statistic
identical in construction across all four axes. The finding is a
property of the statistic, not the biology:
$\kappa^{\mathrm{flux}}_V$ aggregates absolute squared flux
changes, so wherever the optimum is non-unique in the carbon sector
(how much surplus glucose is taken up and how the overflow is split
are optimum-equivalent), the LP solver's arbitrary vertex choice
injects noise into every knockout's comparison. The at-optimum FVA
signature separates the regimes cleanly: phosphoglucose-isomerase
range $0.0$ at the carbon-limited baseline and $4.3$ under oxygen
limitation, against $45$--$201$ at every nitrogen- and
phosphate-limited level. Canonical vertex selection --- parsimonious
FBA for the wild type and every knockout, the objective preserved
exactly (verified per level) and labels therefore unchanged by
construction --- is the declared selection rule under which the
statistic is well posed.

\begin{table}[t]
\centering
\small
\begin{tabular}{lcccc}
\hline
condition & plain $r$ & canonical $r$ & canonical AUC & canonical MCC \\
\hline
\multicolumn{5}{l}{\emph{iJO1366}}\\
baseline (glucose-only) & $+0.603$ & $+0.945$ & $1.000$ & $0.972$ \\
oxygen $-10$ & $+0.775$ & $+0.895$ & $1.000$ & $0.972$ \\
oxygen $-5$ & $+0.607$ & $+0.939$ & $1.000$ & $1.000$ \\
oxygen $-2.5$ & $+0.519$ & $+0.945$ & $1.000$ & $0.958$ \\
ammonium $-10$ & $+0.350$ & $+0.940$ & $1.000$ & $0.972$ \\
ammonium $-2.5$ & $+0.079$ & $+0.915$ & $0.988$ & $0.965$ \\
glutamate $-10$ & $-0.122$ & $+0.872$ & $0.979$ & $0.938$ \\
phosphate $-0.5$ & $+0.323$ & $+0.950$ & $0.988$ & $0.965$ \\
phosphate $-0.25$ & $+0.054$ & $+0.916$ & $0.988$ & $0.965$ \\
phosphate $-0.1$ & $-0.067$ & $+0.914$ & $0.988$ & $0.952$ \\
\multicolumn{5}{l}{\emph{iML1515}}\\
baseline (glucose-only) & $+0.875$ & $+0.937$ & $0.987$ & $0.966$ \\
oxygen $-5$ & $+0.559$ & $+0.941$ & $1.000$ & $1.000$ \\
oxygen $0$ (anaerobic) & $+0.258$ & $+0.949$ & $0.997$ & $0.979$ \\
ammonium $-2.5$ & $-0.113$ & $+0.909$ & $0.986$ & $0.904$ \\
glutamate $-10$ & $+0.314$ & $+0.911$ & $0.987$ & $0.965$ \\
phosphate $-0.25$ & $+0.025$ & $+0.910$ & $0.986$ & $0.904$ \\
phosphate $-0.1$ & $+0.090$ & $+0.900$ & $0.986$ & $0.904$ \\
\hline
\end{tabular}
\caption{Homogenized canonical-selection statistics across the four
perturbation axes (transitive calibration; $r$ is the Pearson
coefficient of $\log\kappa^{\mathrm{flux}}_V$ against $\Delta b$,
AUC/MCC the held-out $70/30$ logistic). Labels agree with the plain
sweeps at $\kappa=1.000$ at every level (after the
solver-tolerance corrections below). Under canonical selection the
association is the invariant object at every level of every axis ---
including across the anaerobic regime switch, where the plain
reading collapses ($+0.258 \to +0.949$) and only the labels
re-stratify.}
\label{tab:canonical-selection}
\end{table}

Table~\ref{tab:canonical-selection} reports the homogenized
statistics. Three features matter. First, canonical selection
sharpens even the unique-optimum levels: the baselines rise from
$r=+0.603$ to $+0.945$ (iJO1366) and $+0.875$ to $+0.937$ (iML1515),
and the deepest oxygen limitation from $+0.519$ to $+0.945$ --- the
plain baseline vertex itself sits on a free acetate-kinase cycle
(at-optimum ACKr range $\approx 10^{3}$) whose arbitrary resolution
the canonical rule removes. Second, the association is restored at
every degenerate level of both nitrogen and phosphate axes
($r\in[+0.87,+0.95]$, AUC $\ge 0.979$, MCC $\ge 0.904$). Third ---
and this upgrades the regime-switch reading of
Remark~\ref{rem:keio-o2-invariance} --- the iML1515 anaerobic
endpoint is restored too: under canonical selection the association
survives the regime switch intact ($r=+0.949$, AUC $0.997$, MCC
$0.979$, against the plain $+0.258$/$0.682$), so the switch moves
labels only (six glycolysis gains); the apparent collapse of the
association at the switch was vertex-conditioning, not biology.

The canonical control also served as an independent audit of the
deposited plain sweeps, and it surfaced a solver-integrity boundary
that we disclose in full. Comparing every deposited plain sweep
level against its canonical counterpart gene-by-gene ($14{,}117$
biomass-and-label comparisons across ten levels) flagged exactly
eight corrupted calls, every one a false-viability call of a
trace-quota gene at a low-growth level: the \emph{fabZ}
ubiquinone-side-chain row at the iML1515 anaerobic endpoint, and at
the $\mathrm{Pi}$ $-0.1$ levels (wild type $\approx 0.104$) the
plain \emph{bioC}/\emph{fabZ}/\emph{bioH} rows and the canonical
\emph{bioF}/\emph{bioH} rows. The mechanism is arithmetic, not
stochastic: the biomass drains of biotin (stoichiometric
coefficient $2\times10^{-6}$) and of the ubiquinone side chain
scale with the growth rate, so at wild-type optima below
$\approx 0.14$ they fall to $2$--$3\times10^{-7}$
mmol/gDW/h --- within a factor of two of the simplex's primal
feasibility tolerance ($10^{-7}$) --- and the solver can then
accept a ``solution'' that violates the hard zero bounds of the
knocked-out steps. The failure is one-directional (false viability
only) and confined to genes whose sole essential role is such a
trace quota, which is why every level with wild-type optimum above
$\approx 0.23$ (quota $\ge 4.6\times10^{-7}$) is clean. All eight
calls were re-adjudicated with an independent LP engine (HiGHS,
two-stage split-variable parsimonious solves: every biotin-pathway
knockout has biomass maximum exactly $0$) and corrected; after
correction the label sets are the invariant ones reported in
Propositions~\ref{prop:keio-glucose-only}--\ref{prop:keio-phosphate},
the cross-check is $0$ discrepancies in $14{,}117$ comparisons, and
the corrected calls reproduce across engines to the reported
precision (the three iJO1366 biotin knockouts share the identical
canonical curvature $164.975$; the three iML1515 ones $253.551$).

\begin{remark}[What the selection rule requires]
\label{rem:canonical-protocol}
The methodological content is twofold. A flux-distance statistic
computed at non-unique optima is conditioned on the vertex, so it
requires a declared selection rule --- ours is parsimonious FBA for
the wild type and every knockout, with the objective preserved and
labels unchanged by construction; plain readings remain meaningful
only where the at-optimum FVA width certifies uniqueness. And
essentiality calls for genes whose blocking quota sits within an
order of magnitude of the solver's feasibility tolerance require
independent adjudication at low growth rates --- the trace-quota
family (biotin, quinone side chain, lipoate) is exactly the
at-risk set, and a second engine settling the LP is sufficient.
Both requirements are properties of the instrument, and the
battery's reported statistics now satisfy both.
\end{remark}

"""

sub("""\\subsection{Benchmark against the structural closure instruments}
\\label{sec:network-keio-e14}""",
    NEW_BLOCK + """\\subsection{Benchmark against the structural closure instruments}
\\label{sec:network-keio-e14}""",
"F4+F5 insertion")

# ---------------------------------------------------------------------
# F6: abstract four axes
# ---------------------------------------------------------------------
sub("""The validation battery is
medium-robust across three axes: carbon-source, oxygen, and
nitrogen perturbations leave the essentiality labels invariant,
re-stratifying only at regime switches, and the association is
invariant under canonical flux selection.""",
"""The validation battery is
medium-robust across four axes: carbon-source, oxygen, nitrogen,
and phosphate perturbations leave the essentiality labels
invariant, re-stratifying only at regime switches, and the
association is invariant under canonical flux selection.""",
"F6 abstract")

open(TEX, "w").write(src)
print(f"\npatched: {len(orig)} -> {len(src)} chars")
