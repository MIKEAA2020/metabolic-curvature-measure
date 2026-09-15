#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md + cover_letter_tac.md for the
proof-read + second-engine round (patch I): new revision note, refreshed
companion-PDF row, and the cover-letter near-tie clause disclosing the
measured engine bracket."""
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
rep(F, "Generated 2026-09-15 (six-axis round). All repository links follow",
    "Generated 2026-09-16 (proof-read + second-engine round). All "
    "repository links follow", "header date")

# ---- 2. new revision note (newest first) -------------------------------
rep(F, "Revision note (2026-09-14): main is now `journal_manuscript_v4.tex`",
    """Revision note (2026-09-16, proof-read + second-engine round): final
proof-read of the sixth-axis prop against every deposited artifact.
One numeric defect corrected (the supply-axis PGI at-optimum range
45-202 -> 45-201; max deposited width 201.492, with the previously
unrecorded iML1515 nh4_-2.5 cell certified at 158.316 by
scripts/iml_nh4_pgi_width_check.py); the fifth-feature compensable
count updated to the post-integrity-patch census (782 of 1,127); and
the nitrogen 4-panel figure restored byte-identical after the
sixth-axis probe import re-clobbered it with the legacy module-level
chart (the phosphate-round defect, reintroduced and caught again).
The engine-invariance audit: a full stateless scipy/HiGHS re-run of
the three iML1515 ATPM levels (scripts/atpm_iml_second_engine.py,
keio_atpm_iml_second_engine.json) shows the labels fully
engine-invariant (kappa = 1.000 at all three levels, zero flips,
max |db| 9.1e-8) and the near-tie itself engine-invariant (WT L1
reproduced to 1.1e-5), while the kV~200 floor is the deposited
simplex path's realization: the stateless engine collapses it to the
one genuinely forced knockout (lamB, kV = 200.0) plus a five-gene
dhaKLM/fsaA/fsaB rerouting block (kV 162-416), and restores the
transitive association to +0.952/+0.968/+0.943 -- the measured
engine bracket is [+0.475, +0.943]. The near-tie passages in
prop:keio-atpm, sec 13.6, and rem:canonical-protocol amended
accordingly (patch I); audit_v11: 285/285 PASS. Companion 73 pp,
0 errors / 0 undefined / 0 overfull.

Revision note (2026-09-14): main is now `journal_manuscript_v4.tex`""",
    "proof-read/second-engine revision note")

# ---- 3. companion PDF row lead-in --------------------------------------
rep(F, "| Manuscript PDF (73 pp, + sixth-axis revision: prop:keio-atpm",
    "| Manuscript PDF (73 pp, + proof-read/second-engine revision: the "
    "measured near-tie engine bracket on the iML1515 maintenance levels "
    "([+0.475, +0.943]; labels and the near-tie itself engine-invariant, "
    "the kV floor disclosed as the deposited simplex path's realization "
    "-- patch I), the PGI range correction (45-201) and the post-patch "
    "compensable count (1,127), on top of the sixth-axis revision: "
    "prop:keio-atpm",
    "companion pdf row")

# ---- 4. cover letter near-tie clause ------------------------------------
rep(C, """near-tied parsimony optima on one reconstruction's extreme
   maintenance level, decorrelating the transitive statistic
   without touching the essentiality ranking); and an""",
    """near-tied parsimony optima on one reconstruction's extreme
   maintenance level, making the transitive statistic
   solver-path-dependent (measured engine bracket [+0.475,
   +0.943]; a stateless second engine restores it) while the
   essentiality ranking stays engine-invariant); and an""",
    "cover letter near-tie clause")

print(f"\n{n} replacements; links doc + cover letter updated")
