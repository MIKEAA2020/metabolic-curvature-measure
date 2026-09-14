#!/usr/bin/env python3
"""Companion v3 patch E: the nitrogen-source third-axis probe.

(1) Abstract: promote the medium-robustness sentence to the
    three-axis form (carbon / oxygen / nitrogen), staying under the
    265-word cap.
(2) Keio section: insert prop:keio-n-source + rem:keio-n-invariance
    after rem:keio-o2-invariance (before the E14 benchmark
    subsection).

Idempotent: skips if the labels are already present.
"""
import re

TEX = "scripts/companion_categorical_v3.tex"
s = open(TEX).read()
orig = s

# ------------------------------------------------------------------
# (1) abstract sentence -> three-axis form
# ------------------------------------------------------------------
OLD_ABS = ("""level with an adapter-level optic statement and verified at scale;
the $\\infty$-categorical extension is developed in homotopy type
theory with proof-sketch status marked. The validation battery is
medium-robust: correcting the carbon source and limiting oxygen
leave the genome-scale essentiality labels invariant and the
association intact, with re-stratification only at the anaerobic
regime switch. The companion application paper develops the atomic
curvature measure of parametric flux balance analysis and its
genome-scale validation.""")
NEW_ABS = ("""level with an adapter-level optic statement and verified at scale;
the $\\infty$-categorical extension is developed in homotopy type
theory with proof-sketch status marked. The validation battery is
medium-robust across three axes: carbon-source, oxygen, and
nitrogen perturbations leave the essentiality labels invariant,
re-stratifying only at regime switches, and the association is
invariant under canonical flux selection. The companion paper
develops the atomic curvature measure of parametric flux balance
analysis and its genome-scale validation.""")

if "prop:keio-n-source" not in s:
    assert OLD_ABS in s, "abstract anchor not found"
    s = s.replace(OLD_ABS, NEW_ABS)

# ------------------------------------------------------------------
# (2) insert the proposition + remark before the E14 subsection
# ------------------------------------------------------------------
ANCHOR = """\\subsection{Benchmark against the structural closure instruments}
\\label{sec:network-keio-e14}"""

BLOCK = r"""\begin{proposition}[Third perturbation axis: nitrogen source]
\label{prop:keio-n-source}
Perturbing the nitrogen axis of the same glucose-only medium ---
ammonium-supply limitation $\mathrm{EX\_nh4\_e}\in\{-10,-5,-2.5\}$
on iJO1366 ($-2.5$ on iML1515) and, in the form the first two axes
did not test, full substitution of the nitrogen source (ammonium
closed; the sole donor replaced by L-glutamate at $-10$, one
nitrogen per molecule so the nitrogen flux is stoichiometrically
matched to the $\mathrm{NH}_4$ $-10$ level and both optima coincide
at $0.9259$ --- the nitrogen-to-growth map is donor-independent ---
or by L-arginine at $-10$, a four-nitrogen carbon co-substrate
whose optimum $1.2595$ exceeds the glucose-minimal baseline by
$28\%$) --- leaves the essentiality labels invariant along the
entire limitation gradient: $289/1{,}367$ at every level on iJO1366
and $286/1{,}516$ on iML1515, zero flips, Cohen's $\kappa=1.000$,
the wild-type optimum falling $76\%$ at $-2.5$. Under substitution
the re-stratification is a pure loss concentrated in the
nitrogen-assimilation module: glutamate costs five labels on iJO1366
(\emph{gltA}, \emph{acnA}, \emph{acnB}, \emph{icd}, \emph{amtB})
and seven on iML1515 (those five plus the GOGAT subunits
\emph{gltB}/\emph{gltD}); arginine costs fourteen on iJO1366 and
fifteen on iML1515 (the same sets plus the arginine-biosynthesis
genes \emph{argA}, \emph{argB}, \emph{argC}, \emph{argE},
\emph{argF}, \emph{argG}, \emph{argH}, \emph{argI}, with
\emph{astC} on iJO1366); $\kappa=0.989$ and $0.969$ (iJO1366),
$0.985$ and $0.967$ (iML1515); gains exactly zero; arginine and
proline metabolism enriched twenty-fold over the genome share; and
every rescue substitution-mediated --- closing the sole nitrogen
donor in the knockout background returns all $41$ lost-label
backgrounds to exactly zero growth. The mechanism is that the
carbon skeleton arrives with its nitrogen: the reductive
assimilation flux through GLUDy ($8.40$~mmol/gDW/h of
$\alpha$-ketoglutarate at the baseline optimum) falls to zero under
glutamate supply --- the $\alpha$-ketoglutarate arm is then fed by
transaminases (ASPTA $4.99$, ALATA\_L $1.77$ around an \emph{icd}
knockout) --- and reverses under arginine supply ($-7.32$), while
\emph{amtB} is the ammonium channel itself. The label-based strata
are otherwise unchanged (model gaps $30$ and $13$; the iJO1366
medium-mismatch stratum moves $180\to175\to166$, exactly the loss
counts). The association splits by regime. Under arginine, where
carbon is again the binding resource, it is intact-to-stronger:
$r=+0.802$ (CI $[0.780,0.823]$), held-out ROC AUC $0.981$, MCC
$0.905$, direct $+0.297$/$0.729$; on iML1515 $r=+0.915$, AUC
$0.997$, direct $+0.425$/$0.821$. Under every nitrogen-limited
optimum the plain-FBA statistics collapse ($r=+0.350$, $+0.079$,
$-0.122$, $+0.213$ at $\mathrm{NH}_4$ $-10/-5/-2.5$ and Glu $-10$;
AUCs $0.546$--$0.709$) --- a degeneracy of the vertex, not of the
biology. At-optimum flux variability gives phosphoglucose isomerase
a range of $45.2$ at $\mathrm{NH}_4$ $-10$ and $177.2$ at $-2.5$,
against $0.0$ at the baseline and $4.3$ under oxygen limitation;
the parsimonious wild type takes up $9.58$, $2.49$, $4.15$
mmol/gDW/h of glucose where the returned vertices take $10.00$,
$7.14$, $10.00$; the non-essential median
$\kappa^{\mathrm{flux}}_V$ inflates from $50$ to $1{,}846$ and its
ranking decorrelates from the baseline ranking (Spearman $-0.04$).
Canonical vertex selection --- parsimonious FBA for the wild type
and every knockout, labels unchanged by construction
($\kappa=1.000$; the objective is preserved to $10^{-13}$) ---
restores the association everywhere: $r=+0.940$ at $\mathrm{NH}_4$
$-10$, $+0.915$ at $-2.5$, $+0.872$ at Glu $-10$ (AUCs $1.000$,
$0.988$, $0.979$; MCC $0.972$, $0.965$, $0.938$), the canonical
ranking correlated $+0.975$, $+0.956$, $+0.735$ with the baseline
canonical ranking; and it sharpens the baseline itself ($r$
$+0.603\to+0.945$, AUC $0.977\to1.000$).
\end{proposition}

\begin{remark}[What the third axis adds: the two-sided boundary]
\label{rem:keio-n-invariance}
With the nitrogen axis, the invariance claim of
Remarks~\ref{rem:keio-invariance} and~\ref{rem:keio-o2-invariance}
completes a three-axis bracket --- carbon, electron acceptor,
nitrogen --- and its boundary acquires both sides. On the supply
side the labels are unconditionally invariant: a $76\%$ reduction
of the wild-type optimum moves no gene across the $5\%$ line in
either reconstruction, exactly as the bimodal-ratio mechanism of
Remark~\ref{rem:keio-invariance} predicts. On the substitution
side the re-stratification is confined to the module the
perturbation rewires: replacing ammonium by an organic donor shuts
down the assimilation arm (the channel \emph{amtB}, the
$\alpha$-ketoglutarate-supply TCA steps, GOGAT) and, when the donor
is arginine, the biosynthetic route to the donor itself --- losses
only, every one substitution-mediated, the exact mirror of the
anaerobic gains in the energy-strategy module. The statistic
acquires its own boundary condition:
$\kappa^{\mathrm{flux}}_V$ under plain FBA is conditioned on the
vertex, and nitrogen-limited optima are carbon-degenerate --- the
surplus glucose may be burned or left on the table, the overflow
may take any of several secretion patterns --- so the collapse of
the plain-FBA association is a property of the solver, not of the
biology; under canonical selection the association is the invariant
object on all three axes (AUC $\ge 0.979$; strengthened at the
baseline). Where the nitrogen enters is itself legible in the
optimum: under glutamate supply the released ammonia comes from
D-amino-acid dehydrogenase (\emph{dadA}, $1.95$) on iJO1366 and
from GLUDy ($2.08$) on iML1515; under arginine supply the
succinylarginine dihydrolase step of the AST pathway (\emph{astB},
$19.3$/$16.0$) dominates, with GLUDy and aspartase (\emph{aspA})
secondary. The medium-robustness statement of the battery is
therefore threefold: essentiality labels invariant under any supply
perturbation that preserves the growth regime, on all three axes;
re-stratification confined to the rewired module at a regime
switch; and the association invariant under canonical selection,
with plain-FBA association readings reported only where the optimum
is unique (carbon- or oxygen-limited).
\end{remark}

"""

if "prop:keio-n-source" not in s:
    assert ANCHOR in s, "E14 anchor not found"
    s = s.replace(ANCHOR, BLOCK + ANCHOR)

assert s != orig or "prop:keio-n-source" in s
open(TEX, "w").write(s)

# verification
n_labels = s.count("prop:keio-n-source")
m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", s, re.S)
body = re.sub(r"\\[a-zA-Z]+", " ", m.group(1))
body = re.sub(r"[\${}~]", " ", body)
words = len([w for w in body.split() if w != "---"])
print(f"prop:keio-n-source labels: {n_labels}; "
      f"rem:keio-n-invariance: {s.count('rem:keio-n-invariance')}; "
      f"abstract words: {words} (< 265: {words < 265})")
assert n_labels == 1 and s.count("rem:keio-n-invariance") == 1
assert words < 265, f"abstract over cap: {words}"
print("PATCH E APPLIED.")
