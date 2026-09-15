#!/usr/bin/env python3
"""Generate scripts/iron_limited_keio_probe.py from the executed and
debugged phosphate probe by targeted string transformation.  The tested
control flow (resume logic, plain/canonical arms, checkpointing, the
empty-concat fix) is preserved verbatim outside the replaced strings;
the only semantic additions are the iron level values and the Fe3+
channel closure in the iML medium setter."""
import py_compile

SRC = "scripts/phosphate_limited_keio_probe.py"
DST = "scripts/iron_limited_keio_probe.py"

DOCSTRING = """FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (trace-metal supply).

Background.  Four axes are established (companion v3, props
keio-glucose-only / keio-o2-limited / keio-n-source / keio-phosphate):
carbon source, electron acceptor, nitrogen supply, phosphate supply.
The trace-metal pre-screen (fifth_axis_prescreen.py) measured all
seven candidate metals (Fe, Zn, Mn, Cu, Mo, Ni, Co) in both models:
every one is a pure biomass component and produces an exactly
proportional limitation gradient (WT ~ fraction x baseline demand,
full carbon-sector degeneracy at every level) -- the trace-metal axes
are interchangeable in gradient shape, so the representative is
chosen by demand and biological standing.  Iron carries the dominant
trace-metal demand (0.015778 mmol/gDW/h iJO1366 / 0.013199 iML1515;
50-2500x every other trace metal) and is the canonical
microbiological trace-metal limitation (FeS clusters, respiratory
chain).  Iron is supplied through the single Fe2+ channel in both
models (EX_fe2_e; the Fe3+ channel EX_fe3_e is closed -- already the
case in the iJO glucose-only medium, closed explicitly in iML1515).

Design (homogeneous with the canonical-selection protocol).
  iJO1366:  EX_fe2_e in {-0.008, -0.004, -0.0016}
            (50% / 75% / 90% WT reduction at demand 0.0158)
  iML1515:  EX_fe2_e in {-0.0066, -0.0033, -0.0013}
            (50% / 75% / 90% WT reduction at demand 0.0132)
  Per level, BOTH arms are computed:
    PLAIN  -- plain-FBA sweep (E12/E16 conventions, labels at 5% of
              that level's WT) -- the axis's own plain reading and
              the label-flip comparison vs the glucose-only baseline;
    CANON  -- pFBA (parsimonious) vertex selection for the wild type
              and every knockout (objective preservation verified;
              biomass read from the solution vector at the biomass
              reaction), label kappa vs the plain arm, and kV rank
              correlation vs the canonical baseline vertices
              (keio_nitrogen_pfba_control_baseline.csv for iJO1366;
              keio_o2_pfba_control_iml_baseline.csv for iML1515).

Artifacts:
  download/keio_iron_limited_e12_results.json   (iJO plain arm)
  download/keio_iron_limited_e12_sweep.csv
  download/keio_iron_limited_e16_results.json   (iML plain arm)
  download/keio_iron_limited_e16_sweep.csv
  download/keio_iron_pfba_control.json          (canonical arm)
  download/keio_iron_pfba_control_<level>.csv   (per level)
  download/keio_iron_limited_summary.txt
"""

s = open(SRC).read()

# 1. replace the module docstring (between the first pair of """ ... """)
before, _olddoc, after = s.split('"""', 2)
s = before + '"""' + DOCSTRING + '"""' + after

# 2. exact replacements, longest/most-specific first
reps = [
    # banners (suffixed forms BEFORE the bare form)
    ('"FOURTH PERTURBATION AXIS: PHOSPHATE-LIMITED MEDIUM (iJO1366)"',
     '"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM, TRACE-METAL SUPPLY '
     '(iJO1366)"'),
    ('"FOURTH PERTURBATION AXIS: PHOSPHATE-LIMITED MEDIUM (iML1515)"',
     '"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM, TRACE-METAL SUPPLY '
     '(iML1515)"'),
    ('"FOURTH PERTURBATION AXIS: PHOSPHATE-LIMITED MEDIUM"',
     '"FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (TRACE METAL)"'),
    # summary narrative
    ('"Supply-side closure of the label-invariance claim "',
     '"Trace-metal supply axis of the label-invariance claim "'),
    ('"Levels chosen by pre-screen (baseline uptake 0.948 "\n'
     '             "iJO / 0.793 iML): -0.5, -0.25, -0.1.")',
     '"Levels chosen by pre-screen (Fe demand 0.0158 iJO / 0.0132 "\n'
     '             "iML): iJO -0.008, -0.004, -0.0016; iML -0.0066, "\n'
     '             "-0.0033, -0.0013 (50/75/90% WT reduction).")'),
    # levels (token rename first so f-string references follow, then
    # the values)
    ("IJO_PI_LEVELS", "IJO_FE_LEVELS"),
    ("IML_PI_LEVELS", "IML_FE_LEVELS"),
    ("IJO_FE_LEVELS = [-0.5, -0.25, -0.1]",
     "IJO_FE_LEVELS = [-0.008, -0.004, -0.0016]"),
    ("IML_FE_LEVELS = [-0.25, -0.1]",
     "IML_FE_LEVELS = [-0.0066, -0.0033, -0.0013]"),
    # setter docstring / function names / comments
    ('"""Glucose-only corrected medium, phosphate at the probe level."""',
     '"""Glucose-only corrected medium, iron (Fe2+) at the probe level."""'),
    ("set_ijo_pi", "set_ijo_fe"),
    ("set_iml_pi", "set_iml_fe"),
    ("# PART 1: iJO1366 phosphate gradient",
     "# PART 1: iJO1366 iron gradient"),
    ("# PART 2: iML1515 cross-rebuild at Pi -0.25 and -0.1",
     "# PART 2: iML1515 cross-rebuild at Fe -0.0033 and -0.0013"),
    ('"probe": "phosphate-limited medium, iJO1366 gradient"',
     '"probe": "iron-limited medium, iJO1366 gradient"'),
    ('"probe": "phosphate-limited medium, iML1515 cross-rebuild"',
     '"probe": "iron-limited medium, iML1515 cross-rebuild"'),
    # artifact names
    ("keio_phosphate_pfba_control", "keio_iron_pfba_control"),
    ("keio_phosphate_limited", "keio_iron_limited"),
    # axis exchange + keys
    ("EX_pi_e", "EX_fe2_e"),
    # mineral lists AFTER the axis rename (the phosphate probe REMOVED
    # EX_pi_e from its lists -- pi was that probe's axis; the iron probe
    # must RESTORE phosphate to the open-mineral set; inserting it before
    # the axis rename would convert it straight back to EX_fe2_e)
    ('IJO_MINERALS = ["EX_nh4_e", "EX_so4_e",',
     'IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e",'),
    ("IML_MINERALS = ['EX_nh4_e', 'EX_so4_e',",
     "IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e',"),
    ("pi_bound", "fe_bound"),
    ("pi_uptake", "fe_uptake"),
    ("pi_lb", "fe_lb"),
    ('f"pi_{abs(lb):g}"', 'f"fe_{abs(lb):g}"'),
    # print labels
    ("Pi uptake", "Fe uptake"),
    ("Pi unlimited", "Fe unlimited"),
    ("PHOSPHATE-LIMITED PROBE DONE.", "IRON-LIMITED PROBE DONE."),
]
for old, new in reps:
    assert old in s, f"missing replacement source: {old[:60]!r}"
    s = s.replace(old, new)

# 3. Fe3+ channel closure -- semantic addition, anchored on the iML
#    setter's try/except minerals block (unique to set_iml_fe)
anchor = ("        except Exception:\n"
          "            pass\n"
          "    model.reactions.get_by_id(\"EX_fe2_e\").lower_bound = fe_lb\n")
assert s.count(anchor) == 1, "iML setter anchor not unique"
s = s.replace(anchor, anchor
              + "    # Fe3+ channel CLOSED: the iron axis is the single Fe2+\n"
              + "    # channel, homogeneous with the iJO glucose-only medium\n"
              + "    model.reactions.get_by_id(\"EX_fe3_e\").lower_bound = 0\n")

# 4. rename the standalone loop/argument variable pi -> fe (word
#    boundary; compound identifiers were already handled above)
import re
s = re.sub(r"\bpi\b", "fe", s)
# f-string labels that survived the regex as "Pi = {pi}" -> now "Pi = {fe}"
s = s.replace("Pi=", "Fe=").replace("Pi = ", "Fe = ")

# 5. verify no phosphate leftovers in the CODE (the iron docstring
#    legitimately cites the established phosphate axis, so split it off)
_head, _newdoc, code = s.split('"""', 2)
low = code.lower()
for bad in ("phosphate", '"pi_bound"', "pi_uptake", "pi_lb"):
    assert bad not in low, f"leftover token: {bad}"
# EX_pi_e legitimately survives as the restored phosphate mineral entry
assert low.count("ex_pi_e") == 2, low.count("ex_pi_e")

open(DST, "w").write(s)
py_compile.compile(DST, doraise=True)
print(f"generated {DST}: {len(s.splitlines())} lines, compiles, "
      f"no phosphate leftovers")
