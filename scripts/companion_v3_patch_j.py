#!/usr/bin/env python3
"""Patch J to companion_categorical_v3.tex (deterministic tie-break
promotion + symmetric iJO second-engine round):

1. sec 13.6 feature count defect: 'Four features matter' -> 'Five
   features' (five features have been listed since patch H added the
   fifth; the count was never updated).
2. prop:keio-atpm: the engine-bracket sentence extended with the
   symmetric iJO1366 second-engine confirmation (labels kappa 1.000
   at all four levels; canonical r within 0.002 at the three deeper
   levels; +0.9685 -> +0.9496 at the mildest, whose 961-of-971 floor
   is the deposited path's realization) and the declared-rule closure
   pointer (iML1515 maintenance readings +0.953/+0.969/+0.944).
3. sec 13.6 fifth feature closing sentence: the 'or where the engine
   resolves a near-tie consistently' ending replaced by the pointer
   to the deterministic tie-break paragraph.
4. NEW \paragraph{The deterministic tie-break.} after the fifth
   feature: the promotion proper -- the declared three-stage rule,
   the pre-registered pilot (105 stratified genes + WT at the two
   worst levels: cross-engine vertex identity at most 6e-11, floor
   collapse 40/40 random floor genes in both engines, labels within
   6e-8; the lamB contrast showing even the stateless engine's vertex
   is a path), and the full declared-rule sweeps at the four
   floor-affected levels (r +0.953/+0.969/+0.944 iML1515, +0.951
   iJO1366; labels kappa 1.000 vs the deposit; floors collapsing to
   the rule-determined rerouting sets: lamB 200.0 at every iML1515
   level, the dhaKLM/fsaA/fsaB block deepening 194->427, the iJO1366
   parallel-routing block pfkB/fbaB/fsaA/fsaB/dhaKLM/ydjI at
   kV 69-90).
5. rem:canonical-protocol third requirement: the constructive
   closure appended (requirement closable by construction; the
   engine bracket records the two-stage spread that motivated it).
6. tab:canonical-selection caption: the declared tie-break readings
   added to the engine clause.
7. rem:keio-multiaxis: 'acquires its measured boundary' -> 'acquires
   --- then closes, by the deterministic tie-break --- its measured
   boundary'.

Driven by download/keio_atpm_ijo_second_engine.json (scripts/
atpm_ijo_second_engine.py), download/keio_atpm_lex_pilot.json
(scripts/atpm_lex_tiebreak_pilot.py, pre-registered verdict PROMOTE),
and download/keio_atpm_lex_full_sweep.json (scripts/
atpm_lex_full_sweep.py).
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEX = os.path.join(REPO, "scripts", "companion_categorical_v3.tex")

tex = open(TEX).read()
orig = tex

EDITS = []

EDITS.append((
    "feature count: Four -> Five",
    """statistics. Four features matter.""",
    """statistics. Five features matter.""",
))

EDITS.append((
    "prop:keio-atpm: symmetric iJO confirmation + declared-rule closure",
    """same statistic to $+0.952$, $+0.968$, $+0.943$ (labels unchanged at
$\\kappa=1.000$; maximum biomass discrepancy $9\\times10^{-8}$). Since the wild-type optimum is""",
    """same statistic to $+0.952$, $+0.968$, $+0.943$ (labels unchanged at
$\\kappa=1.000$; maximum biomass discrepancy $9\\times10^{-8}$); the
symmetric re-run of the iJO1366 levels confirms the restoration
itself is engine-invariant --- labels $\\kappa=1.000$ at all four
levels, canonical $r$ within $0.002$ at the three deeper levels and
$+0.9685$ to $+0.9496$ at the mildest, whose $961$-of-$971$ floor is
the deposited path's realization --- and the deterministic tie-break
of the selection subsection closes the near-tie under a declared
rule, the iML1515 maintenance levels reading $+0.953$, $+0.969$,
$+0.944$. Since the wild-type optimum is""",
))

EDITS.append((
    "fifth feature closing + NEW deterministic tie-break paragraph",
    """association to $+0.952$, $+0.968$, $+0.943$. Canonical selection is
necessary everywhere and sufficient precisely where the parsimony
stage is discriminating --- or where the engine resolves a near-tie
consistently.

The canonical control also served as an independent audit of the""",
    """association to $+0.952$, $+0.968$, $+0.943$.

\\paragraph{The deterministic tie-break.}
The near-tie boundary is not only measurable but closable, and the
closure is the selection rule's own completion: a third
lexicographic stage minimizing a fixed functional $w^{T}v$ over the
wild-type-pinned, parsimony-pinned face (weights
$w\\sim U(0.5,1.5)$ under a fixed seed, the optimum generically
unique) selects a unique vertex by construction, so the returned
canonical vertex becomes a property of the declared protocol rather
than of the solver's path. A pre-registered pilot at the two worst
levels verified exactly this. On a stratified sample of $105$ genes
plus the wild types (the random $40$-gene floor draw at each level,
the near-tie gene \\emph{ltaE}, \\emph{lamB}, the stateless
top-rerouting blocks, and compensable controls), the GLPK
warm-start path and the stateless cold-start engine return the
\\emph{same} tie-broken vertex --- maximum cross-engine squared
distance $6\\times10^{-11}$, against two-stage vertices some
$kV\\approx200$ apart at the same genes --- and every one of the
$80$ randomly drawn floor genes collapses to $kV\\le0.1$ under the
declared rule in both engines, with labels unchanged (maximum
biomass discrepancy $6\\times10^{-8}$). The pilot also exposes the
limit of engine substitution alone: the stateless two-stage reading
had kept \\emph{lamB} at $kV=200$ on iJO1366 --- its one-gene floor
--- while the declared rule returns $kV=0$ there; even a stateless
engine's vertex is a path, and only a declared rule makes the
statistic well posed. Full sweeps under the declared rule at the
four floor-affected levels close the boundary in the instrument's
own terms: the transitive association reads $r=+0.953$, $+0.969$,
$+0.944$ on the iML1515 maintenance levels and $+0.951$ at the
iJO1366 floor level (labels $\\kappa=1.000$ against the deposit at
all four; held-out AUC $0.992$, $0.992$, $0.984$, $1.000$), and the
floor census collapses to the rule-determined rerouting sets:
\\emph{lamB} at $kV=200.0$ at every iML1515 level with the
\\emph{dhaKLM}/\\emph{fsaA}/\\emph{fsaB} block deepening from $194$
to $427$ as maintenance demand grows, and the iJO1366 floor level
carrying instead a parallel-routing block (\\emph{pfkB},
\\emph{fbaB}, \\emph{fsaA}/\\emph{fsaB}, \\emph{dhaKLM}, and the
putative receptor \\emph{ydjI}) at $kV$ $69$--$90$. Canonical
selection is necessary everywhere, and with the deterministic
tie-break it is sufficient at every level measured, including the
near-tied maintenance levels.

The canonical control also served as an independent audit of the""",
))

EDITS.append((
    "rem:canonical-protocol: constructive closure of the third requirement",
    """rows are reported with their AUC and MCC intact and their $r$ read
as the deposited path's realization.
\\end{remark}""",
    """rows are reported with their AUC and MCC intact and their $r$ read
as the deposited path's realization. The requirement is also
closable by construction: the deterministic tie-break --- a third
lexicographic stage minimizing the fixed functional $w^{T}v$ over
the parsimony-pinned face, with fixed-seed weights whose optimum is
generically unique --- returns the same vertex under both engines
(cross-engine squared distance at most $6\\times10^{-11}$ on the
stratified pilot; labels unchanged), collapses the floor to the
rule-determined rerouting set, and reads the maintenance levels at
$+0.953$, $+0.969$, $+0.944$ (iML1515) and $+0.951$ (iJO1366, floor
level) under the single declared rule; the engine bracket above
records the two-stage spread that motivated the closure.
\\end{remark}""",
))

EDITS.append((
    "tab:canonical-selection caption: declared tie-break readings",
    """stateless second engine reading $+0.952$, $+0.968$, $+0.943$
(Remark~\\ref{rem:canonical-protocol}). Under canonical selection the""",
    """stateless second engine reading $+0.952$, $+0.968$, $+0.943$ and
the declared deterministic tie-break $+0.953$, $+0.969$, $+0.944$
(Remark~\\ref{rem:canonical-protocol}). Under canonical selection the""",
))

EDITS.append((
    "rem:keio-multiaxis: boundary closed by the tie-break",
    """and acquires its
measured boundary on the maintenance axis in iML1515 ---
to which the selection subsection now turns.""",
    """and acquires --- then closes, by the
deterministic tie-break --- its measured boundary on the maintenance
axis in iML1515, to which the selection subsection now turns.""",
))

for label, old, new in EDITS:
    n = tex.count(old)
    assert n == 1, f"{label}: expected 1 occurrence, found {n}"
    tex = tex.replace(old, new)
    print(f"[patch J] applied: {label}")

# ---- post-conditions -------------------------------------------------
MUST_HAVE = [
    "Five features matter.",
    "\\paragraph{The deterministic tie-break.}",
    "maximum cross-engine squared\ndistance $6\\times10^{-11}$",
    "$+0.951$ at the\niJO1366 floor level",
    "closable by construction",
    "\\emph{pfkB},\n\\emph{fbaB}",
    "the declared deterministic tie-break $+0.953$, $+0.969$, $+0.944$",
    "$+0.9685$ to $+0.9496$ at the mildest",
    "even a stateless\nengine's vertex is a path",
]
MUST_NOT_HAVE = [
    "Four features matter",
    "or where the engine resolves a near-tie",
]
for s in MUST_HAVE:
    assert s in tex, f"post-condition missing: {s!r}"
for s in MUST_NOT_HAVE:
    assert s not in tex, f"post-condition: forbidden string present: {s!r}"

open(TEX, "w").write(tex)
print(f"[patch J] written: {TEX} "
      f"({len(orig)} -> {len(tex)} chars, {len(EDITS)} edits)")
