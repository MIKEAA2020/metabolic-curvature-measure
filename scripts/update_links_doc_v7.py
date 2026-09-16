#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md + cover_letter_tac.md for the
symmetric iJO second-engine + deterministic tie-break promotion
round (patch J): new revision note, refreshed companion-PDF row
(74 pp), and the cover-letter near-tie clause extended with the
declared-rule closure."""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

n = 0


def rep(path, old, new, what, count=1):
    global n
    src = open(path).read()
    c = src.count(old)
    if c != count:
        print(f"FAIL [{what}]: found {c} (expected {count}) in {path}")
        sys.exit(1)
    open(path, "w").write(src.replace(old, new))
    n += 1
    print(f"ok   [{what}] x{c}")


F = "download/SUBMISSION_PACKAGE_LINKS.md"
C = "download/cover_letter_tac.md"

# ---- 1. header stamp --------------------------------------------------
rep(F, "Generated 2026-09-16 (proof-read + second-engine round). All "
    "repository links follow",
    "Generated 2026-09-16 (symmetric iJO second-engine + deterministic "
    "tie-break promotion round). All repository links follow",
    "header date")

# ---- 2. new revision note (newest first) -------------------------------
rep(F, "Revision note (2026-09-16, proof-read + second-engine round): final",
    """Revision note (2026-09-16, symmetric iJO second-engine +
deterministic tie-break promotion round): the engine-invariance
audit completed symmetrically and the near-tie boundary closed
constructively. (1) The symmetric iJO1366 re-run
(scripts/atpm_ijo_second_engine.py, keio_atpm_ijo_second_engine.json):
all four ATPM levels re-solved under stateless cold-start
scipy/HiGHS with the probe's exact conventions -- labels fully
engine-invariant (kappa = 1.000 at all four levels, zero flips, max
|db| 1.2e-7, essential counts 298/298/299/331 identical), the
canonical restoration itself engine-invariant (r within 0.002 at
the three deeper levels; +0.9685 -> +0.9496 at the mildest level,
whose massive 961-of-971 kV~200 floor collapses to one gene -- the
mirror of the iML1515 finding, the one genuine floor gene in both
models being lamB, b4036). (2) The deterministic tie-break
promotion, gated by a PRE-REGISTERED merit pilot
(scripts/atpm_lex_tiebreak_pilot.py, keio_atpm_lex_pilot.json,
verdict PROMOTE): the declared three-stage lexicographic rule
(stage 3 = min w^T v over the parsimony-pinned face, fixed seeded
weights U(0.5,1.5)) returns the SAME vertex under the GLPK
warm-start path and stateless HiGHS -- maximum cross-engine vertex
distance 6e-11 on the 105-gene stratified sample + WT at the two
worst levels -- collapses the floor for 40/40 random floor genes in
both engines, and preserves labels (max |db| 6.4e-8). The pilot's
instructive contrast: the stateless two-stage reading keeps lamB at
kV = 200 on iJO1366 while the declared rule returns 0 -- even a
stateless engine's vertex is a path; only a declared rule makes the
statistic well posed. (3) The full declared-rule sweeps at the four
floor-affected levels (scripts/atpm_lex_full_sweep.py,
keio_atpm_lex_full_sweep.json): iML1515 ATPM 60/80/100 read
+0.9534/+0.9686/+0.9440 and iJO1366 ATPM 40 reads +0.9510 (labels
kappa = 1.000 vs the deposit at all four; floors collapse to the
rule-determined rerouting sets: lamB 200.0 at every iML1515 level,
the dhaKLM/fsaA/fsaB block deepening 194 -> 427 with maintenance
demand, the iJO1366 floor level carrying the parallel-routing block
pfkB/fbaB/fsaA/fsaB/dhaKLM/ydjI at kV 69-90). (4) Patch J
(scripts/companion_v3_patch_j.py, 6 anchored edits): the
deterministic-tie-break paragraph in the canonical-selection
subsection (the promotion proper), the prop:keio-atpm engine-bracket
sentence extended with the symmetric iJO confirmation and the
declared-rule readings, rem:canonical-protocol's third requirement
closed constructively, the tab caption and rem:keio-multiaxis
clauses, and the latent feature-count defect fixed ('Four
features matter' -> 'Five features'; five listed since patch H).
audit_v12: 301/301 PASS (v11's 285 + 16 new checks P-15..P-30).
Companion 74 pp, 0 errors / 0 undefined / 0 overfull.

Revision note (2026-09-16, proof-read + second-engine round): final""",
    "symmetric/tie-break revision note")

# ---- 3. companion PDF row lead-in --------------------------------------
rep(F, "| Manuscript PDF (73 pp, + proof-read/second-engine revision: the ",
    "| Manuscript PDF (74 pp, + deterministic-tie-break promotion "
    "revision: the declared three-stage lexicographic rule measured "
    "engine-invariant at the near-tie levels (cross-engine vertex "
    "distance 6e-11, pre-registered pilot), the maintenance-level "
    "readings resolved under the declared rule (+0.953/+0.969/+0.944 "
    "iML1515, +0.951 iJO1366; labels kappa 1.000; floors collapsing to "
    "the rule-determined rerouting sets), the symmetric iJO1366 "
    "second-engine confirmation, and the feature-count fix -- patch J), "
    "on top of the proof-read/second-engine revision: the ",
    "companion pdf row")

# ---- 4. cover letter near-tie clause ------------------------------------
rep(C, """near-tied parsimony optima on one reconstruction's extreme
   maintenance level, making the transitive statistic
   solver-path-dependent (measured engine bracket [+0.475,
   +0.943]; a stateless second engine restores it) while the
   essentiality ranking stays engine-invariant); and an""",
    """near-tied parsimony optima on one reconstruction's extreme
   maintenance level, making the transitive statistic
   solver-path-dependent under the two-stage rule (measured engine
   bracket [+0.475, +0.943]) while the essentiality ranking stays
   engine-invariant --- a boundary the deterministic tie-break now
   closes under a declared rule (the same vertex under both simplex
   implementations; maintenance levels +0.953/+0.969/+0.944 and
   +0.951 at the floor level, labels unchanged)); and an""",
    "cover letter near-tie clause")

print(f"\n{n} replacements; links doc + cover letter updated")
