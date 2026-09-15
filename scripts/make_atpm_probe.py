#!/usr/bin/env python3
"""Generate scripts/atpm_stress_keio_probe.py from the executed and
debugged iron probe by targeted string transformation.  The tested
control flow (resume logic incl. scratch sweeps, plain/canonical arms,
checkpointing) is preserved verbatim; the semantic changes are the
axis encoding (ATPM lower bound instead of an exchange bound), the
level values, artifact names, and removal of the Fe3+ closure."""
import py_compile
import re

SRC = "scripts/iron_limited_keio_probe.py"
DST = "scripts/atpm_stress_keio_probe.py"

DOCSTRING = """SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS
(temperature-style, NON-MEDIUM).

Background.  Five axes are established (companion v3, props
keio-glucose-only / keio-o2-limited / keio-n-source / keio-phosphate /
keio-iron): carbon source, electron acceptor, nitrogen supply,
phosphate supply, iron supply -- all MEDIUM-side perturbations.
Genome-scale FBA has no temperature or pH state variables; the
standard constraint-based surrogate for temperature-style stress is
escalation of the non-growth-associated ATP maintenance demand
(ATPM lower bound; default 3.15 iJO1366 / 6.86 iML1515 mmol
ATP/gDW/h).  The non-medium pre-screen (nonmedium_axis_prescreen.py)
compared this encoding head-to-head with proton-leak forcing
(EX_h_e secretion floor, the pH-style surrogate) and selected ATPM:
it spans 29-90% WT reduction with 4-5 usable levels in both models,
while the proton-leak axis compresses to 2 usable levels in iJO1366
(the proton leaves partly 'for free' with organic-acid secretion)
before hard infeasibility.

The pre-screen also established the decisive structural fact: the
ATPM axis carries ZERO carbon-sector degeneracy (at-optimum FVA PGI
width 0.0 at every level, both models) -- unlike every supply axis
(widths 100-200).  The maintenance demand pins the energy sector and
makes the optimum unique.  This axis therefore doubles as a POSITIVE
CONTROL for the degeneracy diagnosis: under temperature-style stress
the plain-FBA association is predicted NOT to collapse, isolating
optimum non-uniqueness (not WT reduction per se) as the collapse
mechanism on the supply axes.

Design (homogeneous with the canonical-selection protocol).
  iJO1366:  ATPM lower bound in {40, 60, 80, 100}
            (29% / 50% / 70% / 90% WT reduction)
  iML1515:  ATPM lower bound in {60, 80, 100}
            (52% / 71% / 90% WT reduction)
  Per level, BOTH arms are computed:
    PLAIN  -- plain-FBA sweep (E12/E16 conventions, labels at 5% of
              that level's WT) -- the axis's own plain reading and
              the label-flip comparison vs the glucose-only baseline;
    CANON  -- pFBA (parsimonious) vertex selection (objective
              preservation verified; biomass read from the solution
              vector at the biomass reaction), label kappa vs the
              plain arm, kV rank correlation vs the canonical
              baselines.

Artifacts:
  download/keio_atpm_stress_e12_results.json   (iJO plain arm)
  download/keio_atpm_stress_e12_sweep.csv
  download/keio_atpm_stress_e16_results.json   (iML plain arm)
  download/keio_atpm_stress_e16_sweep.csv
  download/keio_atpm_pfba_control.json         (canonical arm)
  download/keio_atpm_pfba_control_<level>.csv  (per level)
  download/keio_atpm_stress_summary.txt
"""

s = open(SRC).read()

# 1. replace the module docstring
before, _olddoc, after = s.split('"""', 2)
s = before + '"""' + DOCSTRING + '"""' + after

# 2. explicit replacements (most specific first)
reps = [
    # banners
    ('"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM, TRACE-METAL '
     'SUPPLY (iJO1366)"',
     '"SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS '
     '(TEMPERATURE-STYLE, NON-MEDIUM) (iJO1366)"'),
    ('"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM, TRACE-METAL '
     'SUPPLY (iML1515)"',
     '"SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS '
     '(TEMPERATURE-STYLE, NON-MEDIUM) (iML1515)"'),
    ('"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (TRACE METAL)"',
     '"SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS (NON-MEDIUM)"'),
    ('"IRON-LIMITED PROBE DONE."', '"ATPM-STRESS PROBE DONE."'),
    # summary narrative
    ('"Trace-metal supply axis of the label-invariance claim "',
     '"Non-medium (temperature-style maintenance-stress) axis of the "\n'
     '             "label-invariance claim "'),
    ('"Levels chosen by pre-screen (Fe demand 0.0158 iJO / 0.0132 "\n'
     '             "iML): iJO -0.008, -0.004, -0.0016; iML -0.0066, "\n'
     '             "-0.0033, -0.0013 (50/75/90% WT reduction).")',
     '"Levels chosen by pre-screen: iJO 40/60/80/100, iML 60/80/100 "\n'
     '             "(29-90% WT reduction; ATPM default 3.15 iJO / "\n'
     '             "6.86 iML; zero degeneracy on this axis -- the "\n'
     '             "positive-control property).")'),
    ('"Baseline: glucose-only corrected medium (trehalose "\n'
     '             "closed), Fe unlimited. Probe: EX_fe2_e bound."',
     '"Baseline: glucose-only corrected medium (trehalose closed), "\n'
     '             "default maintenance. Probe: ATPM lower bound."'),
    # levels (token renames first, then values)
    ("IJO_FE_LEVELS", "IJO_ATPM_LEVELS"),
    ("IML_FE_LEVELS", "IML_ATPM_LEVELS"),
    ("IJO_ATPM_LEVELS = [-0.008, -0.004, -0.0016]",
     "IJO_ATPM_LEVELS = [40.0, 60.0, 80.0, 100.0]"),
    ("IML_ATPM_LEVELS = [-0.0066, -0.0033, -0.0013]",
     "IML_ATPM_LEVELS = [60.0, 80.0, 100.0]"),
    # setter docstring + names
    ('"""Glucose-only corrected medium, iron (Fe2+) at the probe '
     'level."""',
     '"""Glucose-only corrected medium, ATPM at the probe level."""'),
    ("set_ijo_fe", "set_ijo_atpm"),
    ("set_iml_fe", "set_iml_atpm"),
    # axis encoding: exchange bound -> ATPM lower bound (both setters
    # share the identical axis line)
    ('model.reactions.get_by_id("EX_fe2_e").lower_bound = fe_lb',
     'model.reactions.get_by_id("ATPM").lower_bound = atpm_lb'),
    # signature axis readout: uptake -> maintenance flux
    ('"fe_uptake": round(float(-raw.fluxes.EX_fe2_e), 4),',
     '"atpm_flux": round(float(raw.fluxes.ATPM), 4),'),
    # part headers
    ("# PART 1: iJO1366 iron gradient",
     "# PART 1: iJO1366 ATPM gradient"),
    ("# PART 2: iML1515 cross-rebuild at Fe -0.0033 and -0.0013",
     "# PART 2: iML1515 cross-rebuild at ATPM 80 and 100"),
    ('"probe": "iron-limited medium, iJO1366 gradient"',
     '"probe": "ATPM-escalation stress, iJO1366 gradient"'),
    ('"probe": "iron-limited medium, iML1515 cross-rebuild"',
     '"probe": "ATPM-escalation stress, iML1515 cross-rebuild"'),
    # artifact names
    ("keio_iron_pfba_control", "keio_atpm_pfba_control"),
    ("keio_iron_limited", "keio_atpm_stress"),
    # key function (positive levels, no abs)
    ('f"fe_{abs(lb):g}"', 'f"atpm_{lb:g}"'),
    # print labels
    ("Fe uptake", "ATPM flux"),
    ('print(f"  Probe levels: EX_fe2_e in {IJO_ATPM_LEVELS}")',
     'print(f"  Probe levels: ATPM lower bound in {IJO_ATPM_LEVELS}")'),
    ("Fe unlimited", "default maintenance"),
    ("EX_fe2_e = {fe}", "ATPM >= {fe}"),
    ("Fe = {", "ATPM = {"),
    ("Fe={fe} vs glucose-only", "ATPM={fe} vs glucose-only"),
]
for old, new in reps:
    assert old in s, f"missing replacement source: {old[:70]!r}"
    s = s.replace(old, new)

# 3. remove the Fe3+ closure block (not an iron probe; both Fe channels
#    stay open at the glucose-only defaults)
fe3_block = (
    "    # Fe3+ channel CLOSED: the iron axis is the single Fe2+\n"
    "    # channel, homogeneous with the iJO glucose-only medium\n"
    "    model.reactions.get_by_id(\"EX_fe3_e\").lower_bound = 0\n")
assert fe3_block in s, "fe3 closure block not found"
s = s.replace(fe3_block, "")

# 4. token renames (word-boundary; compound identifiers already handled)
s = re.sub(r"\bfe_lb\b", "atpm_lb", s)
s = re.sub(r"\bfe_bound\b", "atpm_bound", s)
s = re.sub(r"\bfe_uptake\b", "atpm_flux", s)
s = re.sub(r"\bfe\b", "atpm", s)

# 5. verify no iron leftovers in the CODE (docstring cites the axes)
_head, _newdoc, code = s.split('"""', 2)
low = code.lower()
for bad in ("iron", '"fe_bound"', "fe_uptake", "fe_lb", "abs(lb)"):
    assert bad not in low, f"leftover token: {bad}"
# EX_fe2_e legitimately survives in the mineral lists (2 occurrences:
# iJO + iML) -- the ATPM probe leaves iron unlimited
assert low.count("ex_fe2_e") == 2, low.count("ex_fe2_e")

open(DST, "w").write(s)
py_compile.compile(DST, doraise=True)
print(f"generated {DST}: {len(s.splitlines())} lines, compiles, "
      f"no iron leftovers")
