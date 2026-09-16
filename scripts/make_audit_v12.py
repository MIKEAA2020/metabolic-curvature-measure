#!/usr/bin/env python3
"""Build scripts/audit_v12_numbers.py from audit_v11_numbers.py:
extends the v11 audit with the symmetric iJO second-engine round,
the pre-registered lex tie-break pilot, the full declared-rule
sweeps, and the patch-J amendment checks (P-15..P-30)."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "scripts", "audit_v11_numbers.py")
DST = os.path.join(REPO, "scripts", "audit_v12_numbers.py")

src = open(SRC).read()

# 1. docstring header
old_head = '''"""
Numeric consistency audit of journal_manuscript_v4.tex +
companion_categorical_v3.tex (proof-read + second-engine
engine-invariance round; extends the v10 six-axis audit with: the'''
new_head = '''"""
Numeric consistency audit of journal_manuscript_v4.tex +
companion_categorical_v3.tex (symmetric iJO1366 second-engine +
deterministic tie-break promotion round; extends the v11 audit
with: the iJO1366 ATPM-level stateless re-run
(keio_atpm_ijo_second_engine -- labels engine-invariant at kappa
1.000 at all four levels, canonical r engine-invariant to within
0.002 at the three deeper levels, the mildest level's 961-of-971
floor collapsing to 1), the pre-registered lexicographic tie-break
pilot (keio_atpm_lex_pilot -- verdict PROMOTE: cross-engine vertex
identity at 6e-11, floor collapse 40/40 random floor genes in both
engines, labels within 6.4e-8, the lamB contrast), the full
declared-rule sweeps at the four floor-affected levels
(keio_atpm_lex_full_sweep -- r +0.9534/+0.9686/+0.9440/+0.9510,
labels kappa 1.000 vs the deposit, floors 6/1/1/0, the
rule-determined rerouting sets), and the patch-J amendments; all
traced to committed artifacts).  Retains the v11 header content:
the'''
assert src.count(old_head) == 1
src = src.replace(old_head, new_head)

# 2. new checks inserted before the output block
NEW_CHECKS = '''
# ---- v12: symmetric iJO second-engine + deterministic tie-break ----
ijo2 = json.load(open(os.path.join(
    DL, "keio_atpm_ijo_second_engine.json")))
pilot = json.load(open(os.path.join(DL, "keio_atpm_lex_pilot.json")))
lexfs = json.load(open(os.path.join(
    DL, "keio_atpm_lex_full_sweep.json")))

check("P-15", "iJO1366 second-engine: labels engine-invariant at "
      "all four ATPM levels (kappa 1.000, zero flips)",
      "keio_atpm_ijo_second_engine.json",
      {k: (round(lv["vs_glpk"]["label_kappa"], 4),
           len(lv["vs_glpk"]["label_flips"]))
       for k, lv in ijo2["levels"].items()},
      all(lv["vs_glpk"]["label_kappa"] == 1.0
          and not lv["vs_glpk"]["label_flips"]
          for lv in ijo2["levels"].values()))

_r40h = ijo2["levels"]["atpm_40"]["transitive_calibration"][
    "pearson_r_log_kV_delta_b"]
_r40g = ijo2["levels"]["atpm_40"]["vs_glpk"]["glpk_canon_r"]
check("P-16", "iJO1366 second-engine: canonical r within 0.002 at "
      "the three deeper levels; +0.9685 -> +0.9496 at the mildest",
      "keio_atpm_ijo_second_engine.json",
      {k: round(lv["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"]
                - lv["vs_glpk"]["glpk_canon_r"], 4)
       for k, lv in ijo2["levels"].items()},
      all(abs(lv["transitive_calibration"]
              ["pearson_r_log_kV_delta_b"]
              - lv["vs_glpk"]["glpk_canon_r"]) <= 0.002
          for k, lv in ijo2["levels"].items() if k != "atpm_40")
      and round(_r40h, 4) == 0.9496 and round(_r40g, 4) == 0.9685)

check("P-17", "iJO1366 second-engine: floor census 961 -> 1 at "
      "atpm_40; 2 -> 1 at 60/80/100 (compensables 971)",
      "keio_atpm_ijo_second_engine.json",
      {k: (lv["floor_census_glpk"]["n_floor_190_210"],
           lv["floor_census_highs"]["n_floor_190_210"],
           lv["floor_census_highs"]["n_compensable"])
       for k, lv in ijo2["levels"].items()},
      ijo2["levels"]["atpm_40"]["floor_census_glpk"][
          "n_floor_190_210"] == 961
      and ijo2["levels"]["atpm_40"]["floor_census_highs"][
          "n_floor_190_210"] == 1
      and all(lv["floor_census_highs"]["n_floor_190_210"] == 1
              and lv["floor_census_highs"]["n_compensable"] == 971
              for lv in ijo2["levels"].values()))

check("P-18", "iJO1366 second-engine: maximum biomass discrepancy "
      "<= 1.2e-7 across all four levels",
      "keio_atpm_ijo_second_engine.json",
      max(lv["vs_glpk"]["max_abs_db_ko"]
          for lv in ijo2["levels"].values()),
      max(lv["vs_glpk"]["max_abs_db_ko"]
          for lv in ijo2["levels"].values()) <= 1.2e-7)

check("P-19", "lex pilot: pre-registered verdict PROMOTE "
      "(P1 engine-invariance, P2 floor collapse, P3 labels all true)",
      "keio_atpm_lex_pilot.json", pilot["verdict"],
      pilot["verdict"]["VERDICT"] == "PROMOTE"
      and pilot["verdict"]["P1_engine_invariance"]
      and pilot["verdict"]["P2_floor_collapse"]
      and pilot["verdict"]["P3_label_preservation"])

_cross = [d["cross_engine_kV_max"]
          for d in pilot["verdict_detail"].values()]
_cross += [m["wt"]["wt_cross_engine_kV"]
           for m in pilot["models"].values()]
check("P-20", "lex pilot: maximum cross-engine vertex distance "
      "<= 6e-11 (genes + wild types, both levels)",
      "keio_atpm_lex_pilot.json", max(_cross), max(_cross) <= 6e-11)

check("P-21", "lex pilot: floor collapse 40/40 random floor genes "
      "in both engines at both levels",
      "keio_atpm_lex_pilot.json",
      {t: (d["floor_collapse_frac_glpk"], d["floor_collapse_frac_highs"],
           d["n_floor_sampled"])
       for t, d in pilot["verdict_detail"].items()},
      all(d["floor_collapse_frac_glpk"] == 1.0
          and d["floor_collapse_frac_highs"] == 1.0
          and d["n_floor_sampled"] == 40
          for d in pilot["verdict_detail"].values()))

check("P-22", "lex pilot: label preservation, max |b_lex - "
      "b_deposited| <= 6.4e-8 (both engines, both levels)",
      "keio_atpm_lex_pilot.json",
      max(max(d["max_abs_db_vs_deposited_glpk"],
              d["max_abs_db_vs_deposited_highs"])
          for d in pilot["verdict_detail"].values()),
      all(max(d["max_abs_db_vs_deposited_glpk"],
              d["max_abs_db_vs_deposited_highs"]) <= 6.4e-8
          for d in pilot["verdict_detail"].values()))

_pl_i = pd.read_csv(os.path.join(DL, "keio_atpm_lex_pilot_iml_atpm_100.csv"))
_pl_j = pd.read_csv(os.path.join(DL, "keio_atpm_lex_pilot_ijo_atpm_40.csv"))
_lamB_i = _pl_i[_pl_i.gene_id == "b4036"]
_lamB_j = _pl_j[_pl_j.gene_id == "b4036"]
check("P-23", "lex pilot: the lamB contrast -- iML1515 kV 200.0 in "
      "both engines, iJO1366 kV 0 in both engines (the stateless "
      "2-stage iJO floor gene is itself a path realization)",
      "keio_atpm_lex_pilot_{iml,ijo}_atpm_*.csv",
      (float(_lamB_i.kV_lex_glpk_vs_wt.iloc[0]),
       float(_lamB_i.kV_lex_highs_vs_wt.iloc[0]),
       float(_lamB_j.kV_lex_glpk_vs_wt.iloc[0]),
       float(_lamB_j.kV_lex_highs_vs_wt.iloc[0])),
      round(float(_lamB_i.kV_lex_glpk_vs_wt.iloc[0]), 1) == 200.0
      and round(float(_lamB_i.kV_lex_highs_vs_wt.iloc[0]), 1) == 200.0
      and float(_lamB_j.kV_lex_glpk_vs_wt.iloc[0]) == 0.0
      and float(_lamB_j.kV_lex_highs_vs_wt.iloc[0]) == 0.0)

_lexr = {k: round(lv["transitive_calibration"]
                  ["pearson_r_log_kV_delta_b"], 4)
         for k, lv in lexfs["levels"].items()}
_lexauc = {k: round(lv["transitive_calibration"]["held_out"]["roc_auc"], 4)
           for k, lv in lexfs["levels"].items()}
check("P-24", "full lex sweep: declared-rule r +0.9534/+0.9686/"
      "+0.9440 (iML1515 60/80/100) and +0.9510 (iJO1366 40); AUC "
      "0.9919/0.9920/0.9844/1.0000",
      "keio_atpm_lex_full_sweep.json", (_lexr, _lexauc),
      _lexr == {"iml_atpm_60": 0.9534, "iml_atpm_80": 0.9686,
                "iml_atpm_100": 0.944, "ijo_atpm_40": 0.951}
      and _lexauc == {"iml_atpm_60": 0.9919, "iml_atpm_80": 0.992,
                      "iml_atpm_100": 0.9844, "ijo_atpm_40": 1.0})

check("P-25", "full lex sweep: labels kappa 1.000 vs the deposit at "
      "all four levels; essential counts identical",
      "keio_atpm_lex_full_sweep.json",
      {k: (round(lv["vs_glpk_deposit"]["label_kappa"], 4),
           lv["n_essential"], lv["n_essential_glpk"])
       for k, lv in lexfs["levels"].items()},
      all(lv["vs_glpk_deposit"]["label_kappa"] == 1.0
          and lv["n_essential"] == lv["n_essential_glpk"]
          for lv in lexfs["levels"].values()))

check("P-26", "full lex sweep: floors 6/1/1/0 (iML 60/80/100, iJO "
      "40); lamB kV 200.0 at every iML1515 level",
      "keio_atpm_lex_full_sweep.json",
      {k: (lv["floor_census_lex"]["n_floor_190_210"],
           lv["floor_census_lex"]["n_compensable"])
       for k, lv in lexfs["levels"].items()},
      [lexfs["levels"][k]["floor_census_lex"]["n_floor_190_210"]
       for k in ["iml_atpm_60", "iml_atpm_80", "iml_atpm_100",
                 "ijo_atpm_40"]] == [6, 1, 1, 0]
      and all(any(t["gene_id"] == "b4036"
                  and round(t["kV_lex"], 1) == 200.0
                  for t in lexfs["levels"][k]
                  ["top8_compensable_kV_lex"])
              for k in ["iml_atpm_60", "iml_atpm_80",
                        "iml_atpm_100"]))

_blk = {k: [t for t in lexfs["levels"][k]["top8_compensable_kV_lex"]
            if t["gene_id"] in ("b1198", "b1199", "b1200", "b3946",
                                "b0825")]
        for k in ["iml_atpm_60", "iml_atpm_80", "iml_atpm_100"]}
_blk_v = {k: [round(t["kV_lex"], 1) for t in v]
          for k, v in _blk.items()}
check("P-27", "full lex sweep: the dhaKLM/fsaA/fsaB block deepens "
      "194 -> 299 -> 427 across the iML1515 levels",
      "keio_atpm_lex_full_sweep.json", _blk_v,
      all(len(v) == 5 for v in _blk_v.values())
      and set(_blk_v["iml_atpm_60"]) == {193.6}
      and set(_blk_v["iml_atpm_80"]) == {298.8}
      and set(_blk_v["iml_atpm_100"]) == {427.2})

_top_j = {t["gene_id"]: round(t["kV_lex"], 1)
          for t in lexfs["levels"]["ijo_atpm_40"]
          ["top8_compensable_kV_lex"]}
check("P-28", "full lex sweep: iJO1366 floor-level rerouting block "
      "pfkB/fbaB/ydjI at 89.8 and fsaA/fsaB/dhaM at 68.9 "
      "(manuscript: kV 69--90)",
      "keio_atpm_lex_full_sweep.json", _top_j,
      all(_top_j.get(g) == 89.8 for g in ("b1723", "b2097", "b1773"))
      and all(_top_j.get(g) == 68.9 for g in ("b3946", "b0825",
                                              "b1198")))

check("P-29", "patch J present: tie-break paragraph, closure "
      "clauses, feature count fix; no regressions",
      "companion_categorical_v3.tex",
      "edits present: %s" % all(t in texS for t in
          ["Five features matter.",
           "\\\\paragraph{The deterministic tie-break.}",
           "closable by construction",
           "the declared deterministic tie-break $+0.953$, $+0.969$, "
           "$+0.944$",
           "$+0.9685$ to $+0.9496$ at the mildest",
           "\\\\emph{pfkB},", "\\\\emph{fbaB},"]),
      all(t in texS for t in
          ["Five features matter.",
           "\\\\paragraph{The deterministic tie-break.}",
           "closable by construction",
           "the declared deterministic tie-break $+0.953$, $+0.969$, "
           "$+0.944$",
           "$+0.9685$ to $+0.9496$ at the mildest",
           "\\\\emph{pfkB},", "\\\\emph{fbaB},"])
      and all(t not in texS for t in
              ["Four features matter",
               "or where the engine resolves a near-tie"]))

check("P-30", "iJO1366 second-engine + lex artifacts carry the "
      "probe-convention WT agreements (< 1e-6 at every level)",
      "keio_atpm_{ijo_second_engine,lex_full_sweep}.json",
      (max(abs(lv["wild_type_biomass"] - d)
           for lv, d in [(ijo2["levels"]["atpm_40"], 0.6947359182109596),
                         (ijo2["levels"]["atpm_60"], 0.4962399415792379),
                         (ijo2["levels"]["atpm_80"], 0.2977439649475629),
                         (ijo2["levels"]["atpm_100"], 0.09924798831587155)]),
       max(abs(lv["wild_type_biomass"] - d)
           for lv, d in [(lexfs["levels"]["iml_atpm_60"], 0.39839),
                         (lexfs["levels"]["iml_atpm_80"], 0.239034),
                         (lexfs["levels"]["iml_atpm_100"], 0.079678),
                         (lexfs["levels"]["ijo_atpm_40"],
                          0.6947359182109596)])),
      all(abs(lv["wild_type_biomass"] - d) < 1e-6
          for lv, d in [(ijo2["levels"]["atpm_40"], 0.6947359182109596),
                        (ijo2["levels"]["atpm_60"], 0.4962399415792379),
                        (ijo2["levels"]["atpm_80"], 0.2977439649475629),
                        (ijo2["levels"]["atpm_100"], 0.09924798831587155)])
      and all(abs(lv["wild_type_biomass"] - d) < 1e-6
              for lv, d in [(lexfs["levels"]["iml_atpm_60"], 0.39839),
                            (lexfs["levels"]["iml_atpm_80"], 0.239034),
                            (lexfs["levels"]["iml_atpm_100"], 0.079678),
                            (lexfs["levels"]["ijo_atpm_40"],
                             0.6947359182109596)]))


'''
old_out = 'out = {"experiment": "v11 numeric consistency audit (proof-read + "'
assert src.count(old_out) == 1
src = src.replace(old_out, NEW_CHECKS + old_out)
src = src.replace(
    'out = {"experiment": "v11 numeric consistency audit (proof-read + "\n'
    '                     "second-engine engine-invariance round; extends v10)",',
    'out = {"experiment": "v12 numeric consistency audit (symmetric iJO "\n'
    '                     "second-engine + deterministic tie-break '
    'promotion round; extends v11)",')

# 3. defect ledger: add D-P5
old_def = '''           "D-P4 (v11 round): nitrogen 4-panel figure shipped clobbered "
           "by the probe-import legacy figure in the sixth-axis commit "
           "(129,624 vs 157,682 bytes) -> regenerated byte-identical"],'''
new_def = '''           "D-P4 (v11 round): nitrogen 4-panel figure shipped clobbered "
           "by the probe-import legacy figure in the sixth-axis commit "
           "(129,624 vs 157,682 bytes) -> regenerated byte-identical",
           "D-P5 (v12 round): sec 13.6 feature count 'Four features "
           "matter' -> 'Five features' (five features listed since "
           "patch H added the fifth; caught by the tie-break "
           "promotion round)"],'''
assert src.count(old_def) == 1
src = src.replace(old_def, new_def)

# 4. output filenames + md title + md defect paragraph
assert src.count('v11_number_audit.json') == 1
src = src.replace('v11_number_audit.json', 'v12_number_audit.json')
assert src.count('v11_number_audit.md') == 1
src = src.replace('v11_number_audit.md', 'v12_number_audit.md')
src = src.replace(
    '# v11 numeric consistency audit (proof-read + second-engine round)',
    '# v12 numeric consistency audit (symmetric iJO second-engine + '
    'tie-break promotion round)')
src = src.replace(
    '"(compensable count 1,127), D-P3 (engine bracket [+0.475,+0.943]), "\n'
    '      "D-P4 (nitrogen figure clobber repaired).", ""',
    '"(compensable count 1,127), D-P3 (engine bracket [+0.475,+0.943]), "\n'
    '      "D-P4 (nitrogen figure clobber repaired); v12 round: D-P5 "\n'
    '      "(feature count Four -> Five).", ""')

# 5. R9 expectation: the feature count is now Five (patch J)
_old_r9a = """      "restored range [+0.80,+0.96]; 'Four features matter'","""
_new_r9a = """      "restored range [+0.80,+0.96]; 'Five features matter'","""
assert src.count(_old_r9a) == 1
src = src.replace(_old_r9a, _new_r9a)
_old_r9b = """      and "Four features matter" in tex)"""
_new_r9b = """      and "Five features matter" in tex)"""
assert src.count(_old_r9b) == 1
src = src.replace(_old_r9b, _new_r9b)

open(DST, "w").write(src)
print(f"[make_audit_v12] written: {DST} ({len(src)} chars)")
