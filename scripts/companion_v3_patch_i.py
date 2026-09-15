#!/usr/bin/env python3
"""Patch I to companion_categorical_v3.tex (proof-read + engine-
invariance round):

1. prop:keio-atpm: the supply-axis PGI at-optimum range corrected
   $45$--$202$ -> $45$--$201$ (max deposited width 201.492, iJO1366
   phosphate -0.1; the qualifier tightened to 'at every nitrogen-,
   phosphate-, and iron-limited level', matching sec 13.6; the one
   unrecorded cell, iML1515 nh4_-2.5, measured at 158.316 by
   scripts/iml_nh4_pgi_width_check.py).
2. prop:keio-atpm: the iML1515 canonical sentence discloses the
   second-engine bracket -- the deposited simplex path's r values
   are kept, with the stateless HiGHS re-run restoring the same
   statistic (+0.952/+0.968/+0.943) at unchanged labels.
3. sec 13.6 fifth feature: 'the one corner where canonical selection
   is only partially sufficient' -> 'where the canonical vertex
   itself is only weakly determined'; the floor census corrected to
   the post-integrity-patch compensable count ($1{,}129$ -> $1{,}127$
   -- the 1,129 was the pre-patch measurement); 'r caps near +0.48'
   -> path-dependent reading; the full second-engine measurement
   inserted (labels engine-invariant at kappa 1.000 / max biomass
   discrepancy 9e-8 / AUC 0.992/0.992/0.984; near-tie itself
   engine-invariant, WT L1 reproduced to 1e-5; floor collapsed to
   the one genuinely forced knockout lamB at kV 200.0 plus the
   five-gene dhaKLM/fsaA/fsaB rerouting block at kV 162-416;
   transitive association restored to +0.952/+0.968/+0.943).
4. rem:canonical-protocol (third requirement): 'must be read with
   the near-tie floor in mind' -> the measured engine bracket
   [+0.475, +0.943]; essentiality ranking engine-invariant under
   both engines; the table's iML1515 maintenance r read as the
   deposited path's realization.
5. tab:canonical-selection caption: same clause in one line.

Driven by download/keio_atpm_iml_second_engine.json (scripts/
atpm_iml_second_engine.py) and download/keio_iml_nh4_pgi_width.json.
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(REPO, "scripts", "companion_categorical_v3.tex")

tex = open(TEX).read()
orig = tex

EDITS = []

EDITS.append((
    "PGI range fix (prop:keio-atpm)",
    """variability $0.0$ at every level in both models against $45$--$202$
on every supply level.""",
    """variability $0.0$ at every level in both models against $45$--$201$
at every nitrogen-, phosphate-, and iron-limited level.""",
))

EDITS.append((
    "prop:keio-atpm engine bracket",
    """and restores the ranking separation
but not the transitive correlation on iML1515 ($r=+0.703$,
$+0.655$, $+0.475$; AUC $0.992$, $0.992$, $0.978$; labels
$\\kappa=1.000$ at every level) --- the near-tie boundary of
Remark~\\ref{rem:canonical-protocol}.""",
    """and on iML1515 restores the ranking
separation at every level (AUC $0.992$, $0.992$, $0.978$; labels
$\\kappa=1.000$) while the transitive correlation on the deposited
simplex path reads $r=+0.703$, $+0.655$, $+0.475$ --- the near-tie
boundary of Remark~\\ref{rem:canonical-protocol}, where a stateless
second engine resolves the near-tie consistently and restores the
same statistic to $+0.952$, $+0.968$, $+0.943$ (labels unchanged at
$\\kappa=1.000$; maximum biomass discrepancy $9\\times10^{-8}$).""",
))

EDITS.append((
    "fifth feature: weak determination + second-engine measurement",
    """instability --- and the axis adds the one corner where canonical
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
the parsimony stage is discriminating.""",
    """instability --- and the axis adds the one corner where the
canonical vertex itself is only weakly determined: at elevated
maintenance demand the iML1515 parsimony stage itself carries
\\emph{near-tied} optima (vertices $\\approx200$ apart in the
squared-flux metric whose $L_1$ objectives differ by
$8.6\\times10^{-4}$ absolute, $1.2\\times10^{-6}$ relative --- within
the simplex optimality tolerance), so the returned canonical vertex
is solver-path dependent: on the deposited simplex path $782$ of
$1{,}127$ compensable knockouts record the near-tie floor
$kV\\approx200.01$ while the rest sit at $kV\\approx0$ (supply axes
carry no floor; compensable medians $0.00$--$0.10$), and the floor
decorrelates that path's transitive statistic on iML1515 ($r$ down
to $+0.475$) without touching the essentiality ranking (AUC
$0.978$, labels $\\kappa=1.000$ at every level). A full
second-engine re-run of the three iML1515 levels under the
stateless cold-start rule (scipy/HiGHS, same two-stage selection)
measures the path dependence directly: the near-tie itself is
engine-invariant (wild-type $L_1$ reproduced to $1\\times10^{-5}$;
labels $\\kappa=1.000$ at all three levels, maximum biomass
discrepancy $9\\times10^{-8}$, AUC $0.992$/$0.992$/$0.984$), but the
floor is the deposited path's realization --- the stateless engine
collapses the floor band to the one genuinely forced knockout
(\\emph{lamB}, $kV=200.0$ at every level) with a single further
five-gene rerouting block (\\emph{dhaKLM}, \\emph{fsaA}/\\emph{fsaB},
$kV$ $162$--$416$ across the levels), and restores the transitive
association to $+0.952$, $+0.968$, $+0.943$. Canonical selection is
necessary everywhere and sufficient precisely where the parsimony
stage is discriminating --- or where the engine resolves a near-tie
consistently.""",
))

EDITS.append((
    "rem:canonical-protocol third requirement: engine bracket",
    """statistics now satisfy both. A third requirement is measured, not
imposed: where the parsimony stage itself carries near-tied optima
--- the maintenance axis in iML1515, $\\Delta L_1$ at
$1.2\\times10^{-6}$ relative --- the canonical vertex is only
weakly determined and the transitive statistic must be read with
the near-tie floor in mind; the essentiality ranking is unaffected
(held-out AUC $\\ge0.978$), which is why the table's iML1515
maintenance rows are reported with their AUC and MCC intact.""",
    """statistics now satisfy both. A third requirement is measured, not
imposed: where the parsimony stage itself carries near-tied optima
--- the maintenance axis in iML1515, $\\Delta L_1$ at
$1.2\\times10^{-6}$ relative --- the canonical vertex is only weakly
determined and the transitive statistic is path-dependent, the
measured engine bracket at the deepest level being
$[+0.475,+0.943]$ (the deposited simplex path against the stateless
second engine of the re-run above); the essentiality ranking is
engine-invariant (labels $\\kappa=1.000$, held-out AUC $\\ge0.978$
under both engines), which is why the table's iML1515 maintenance
rows are reported with their AUC and MCC intact and their $r$ read
as the deposited path's realization.""",
))

EDITS.append((
    "tab:canonical-selection caption clause",
    """sweeps at $\\kappa=1.000$ at every level (after the
solver-tolerance corrections below). Under canonical selection the""",
    """sweeps at $\\kappa=1.000$ at every level (after the
solver-tolerance corrections below); the iML1515 maintenance rows'
canonical $r$ is the deposited simplex path's realization, the
stateless second engine reading $+0.952$, $+0.968$, $+0.943$
(Remark~\\ref{rem:canonical-protocol}). Under canonical selection the""",
))

for label, old, new in EDITS:
    n = tex.count(old)
    assert n == 1, f"{label}: expected 1 occurrence, found {n}"
    tex = tex.replace(old, new)
    print(f"[patch I] applied: {label}")

# ---- post-conditions -------------------------------------------------
MUST_HAVE = [
    "against $45$--$201$\nat every nitrogen-, phosphate-, and iron-limited level",
    "$782$ of\n$1{,}127$ compensable knockouts record the near-tie floor",
    "restores the transitive\nassociation to $+0.952$, $+0.968$, $+0.943$",
    "engine bracket at the deepest level being\n$[+0.475,+0.943]$",
    "the\nstateless second engine reading $+0.952$, $+0.968$, $+0.943$",
    "\\emph{lamB}, $kV=200.0$ at every level",
    "must be read with\nthe near-tie floor in mind",  # must be GONE
]
MUST_NOT_HAVE = [
    "45$--$202", "1{,}129", "caps near", "only partially sufficient",
]
for s in MUST_HAVE[:-1]:
    assert s in tex, f"post-condition missing: {s!r}"
for s in MUST_NOT_HAVE:
    assert s not in tex, f"post-condition: forbidden string present: {s!r}"
assert MUST_HAVE[-1] not in tex, "old third-requirement phrasing still present"

open(TEX, "w").write(tex)
print(f"[patch I] written: {TEX} "
      f"({len(orig)} -> {len(tex)} chars, {len(EDITS)} edits)")
