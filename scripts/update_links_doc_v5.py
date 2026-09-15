#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md for the six-axis round (patch F):
new revision note, refreshed manuscript-PDF row (70 pp), and the new
artifact rows (phosphate / iron / ATPM / multi-axis table + figure /
measurement artifacts / audit v8)."""
import sys

F = "download/SUBMISSION_PACKAGE_LINKS.md"
src = open(F).read()
n = 0


def rep(old, new, what, count=1):
    global src, n
    c = src.count(old)
    if c != count:
        print(f"FAIL [{what}]: found {c} (expected {count})")
        sys.exit(1)
    src = src.replace(old, new)
    n += 1
    print(f"ok   [{what}] x{c}")


# ---- 1. header generation stamp -------------------------------------
rep("""Generated 2026-09-14 (3rd-wave repair round). All repository links follow
the repo/blob/main pattern verified live in the 2026-09-03 pass; journal""",
    """Generated 2026-09-15 (six-axis round). All repository links follow
the repo/blob/main pattern verified live in the 2026-09-03 pass; journal""", "header date")

# ---- 2. new revision note after the third-axis note header -----------
rep("""Revision note (2026-09-14, third perturbation axis round): the""",
    """Revision note (2026-09-15, six-axis round): the companion adds the
phosphate-limited probe (fourth axis), the iron-limited probe (fifth
axis, pre-screened over the seven trace metals: iron demand
0.0158/0.0132 mmol/gDW/h, 50-2500x the others), and the non-medium
ATPM-maintenance-stress probe (sixth axis, temperature-style; the
proton-leak pH-style surrogate pre-screened and rejected), each with
plain + canonical arms in both reconstructions, and promotes the
canonical-selection finding to its own protocol subsection
(sec:canonical-selection) with a consolidated 31-level table. Labels
are invariant along every limitation gradient (15 gradient levels,
zero flips); the apparent -89/-90% floor losses (fabZ/bioH/bioD) are
demonstrated LP-tolerance effects (demanded fluxes 2.07e-7 through
zero-bounded reactions); the maintenance-demand regime switch gains
the energy-transduction module (atp/cyo/nuo operons, OXPHOS enriched
26 vs 3.2 expected) already at mild stress; canonical selection
restores the association everywhere it is discriminating (24 supply
levels r >= +0.856, AUC >= 0.978; ATPM iJO r >= +0.937) and its
measured boundary is the iML1515/ATPM L1 near-tie (dL1 1.2e-6
relative, 782/1129 compensables at the ~200.01 floor). Companion
67 -> 70 pp, 0 errors / 0 undefined / 0 overfull; abstract six-axis,
264 words < 265. New artifacts: keio_phosphate_limited_e12/e16,
keio_phosphate_pfba_control[_iml]_pi_*, keio_iron_limited_e12/e16,
keio_iron_pfba_control[_iml]_fe_*, keio_atpm_stress_e12/e16,
keio_atpm_pfba_control[_iml]_atpm_*, keio_atpm_stress_summary.txt,
keio_fifth_axis_prescreen.json, keio_nonmedium_prescreen.json,
multiaxis_canonical_table.json/.txt,
keio_multiaxis_canonical_response.png,
keio_floor_tolerance_check.json, keio_atpm_neartie_measurement.json
(scripts phosphate_limited_keio_probe.py, iron_limited_keio_probe.py,
atpm_stress_keio_probe.py, multiaxis_table.py, multiaxis_figure.py,
sixth_axis_artifacts.py; audit_v8_numbers.py 184/184 PASS).

Revision note (2026-09-14, third perturbation axis round): the""",
    "six-axis revision note")

# ---- 3. manuscript PDF row: 67 pp -> 70 pp ---------------------------
rep("| Manuscript PDF (67 pp, + nitrogen-axis third-probe revision: prop:keio-n-source + rem:keio-n-invariance and the three-axis abstract, on top of the 3rd-wave repair, glucose-only re-run, oxygen-probe revision, viability-kernel + Poincare/averaging bridges, and the restoration revision) |",
    "| Manuscript PDF (70 pp, + six-axis round: props keio-phosphate / keio-iron / keio-atpm, the multi-axis canonical-selection protocol subsection with the 31-level table and the near-tie boundary, and the six-axis abstract, on top of the nitrogen-axis third-probe revision, 3rd-wave repair, glucose-only re-run, oxygen-probe revision, viability-kernel + Poincare/averaging bridges, and the restoration revision) |",
    "manuscript pdf row")

open(F, "w").write(src)
print(f"\n{n} replacements; {F} updated")
