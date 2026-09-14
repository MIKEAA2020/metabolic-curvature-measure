#!/usr/bin/env python3
"""Build audit_v8_numbers.py from audit_v7_numbers.py: update the
docstring and output paths (v7 -> v8), and insert the round-8 checks
(O2 canonical control, corrected anaerobic endpoint, phosphate
fourth axis, canonical-selection subsection + table, solver-tolerance
integrity, four-axis abstract) just before the output construction.
"""
import re

V7 = "scripts/audit_v7_numbers.py"
V8 = "scripts/audit_v8_numbers.py"
src = open(V7).read()

# 1) docstring
old_doc_head = """Numeric consistency audit of journal_manuscript_v4.tex +
companion_categorical_v3.tex (nitrogen-source third-axis probe round;
extends the v6 audit -- oxygen-limited probe -- with the third
perturbation axis: prop:keio-n-source + rem:keio-n-invariance + the
three-axis abstract, all traced to the keio_nitrogen_* artifacts)."""
new_doc_head = """Numeric consistency audit of journal_manuscript_v4.tex +
companion_categorical_v3.tex (fourth-axis + canonical-selection
round; extends the v7 audit -- nitrogen third axis -- with: the O2
canonical-selection re-run (keio_o2_pfba_control_*), the corrected
iML anaerobic endpoint (fabZ solver-tolerance row), the phosphate
fourth axis (keio_phosphate_*), the canonical-selection subsection
with its homogenized table, the solver-tolerance integrity
disclosures, and the four-axis abstract; all traced to committed
artifacts)."""
assert old_doc_head in src
src = src.replace(old_doc_head, new_doc_head)

# 2) output paths
src = src.replace('v7_number_audit.json', 'v8_number_audit.json')
src = src.replace('v7_number_audit.md', 'v8_number_audit.md')
src = src.replace('v7_number_audit', 'v8_number_audit')

NEW_BLOCK = r'''
# =====================================================================
# ROUND 8: O2 canonical control / corrected anaerobic endpoint /
# phosphate fourth axis / canonical-selection subsection
# =====================================================================

# --- O2 canonical control (keio_o2_pfba_control.json) ---
o2c = json.load(open(os.path.join(DL, "keio_o2_pfba_control.json")))
_ijo = o2c["ijo_levels"]; _iml = o2c["iml_levels"]

def _r(d): return d["transitive_calibration"]["pearson_r_log_kV_delta_b"]
def _auc(d): return d["transitive_calibration"]["held_out"]["roc_auc"]
def _mcc(d): return d["transitive_calibration"]["held_out"]["mcc"]

for key, r_claim, auc_claim, mcc_claim in [
        ("ijo_o2_10", 0.895, 1.000, 0.972),
        ("ijo_o2_5", 0.939, 1.000, 1.000),
        ("ijo_o2_2.5", 0.945, 1.000, 0.958)]:
    d = _ijo[key]
    check(f"R8-O2C-{key}-r",
          f"canonical r = {r_claim:+.3f} (table)",
          f"o2c[{key}]", f"{_r(d):+.4f}",
          abs(_r(d) - r_claim) < 5e-4)
    check(f"R8-O2C-{key}-auc",
          f"canonical AUC = {auc_claim:.3f}",
          f"o2c[{key}]", f"{_auc(d):.4f}",
          abs(_auc(d) - auc_claim) < 5e-4)
    check(f"R8-O2C-{key}-mcc",
          f"canonical MCC = {mcc_claim:.3f}",
          f"o2c[{key}]", f"{_mcc(d):.4f}",
          abs(_mcc(d) - mcc_claim) < 5e-4)
    check(f"R8-O2C-{key}-kappa",
          "label kappa = 1.000 (by construction, verified)",
          f"o2c[{key}]", f"{d['label_agreement_fba_vs_pfba_kappa']:.4f}",
          d["label_agreement_fba_vs_pfba_kappa"] > 0.99999)
    check(f"R8-O2C-{key}-objpres",
          "objective preserved (< 1e-6)",
          f"o2c[{key}]",
          d["objective_preservation"]["objective_abs_diff"],
          d["objective_preservation"]["objective_abs_diff"] < 1e-6)

for key, r_claim, auc_claim, mcc_claim in [
        ("iml_baseline", 0.937, 0.987, 0.966),
        ("iml_o2_5", 0.941, 1.000, 1.000),
        ("iml_o2_0", 0.949, 0.997, 0.979)]:
    d = _iml[key]
    check(f"R8-O2C-{key}-r",
          f"canonical r = {r_claim:+.3f} (table)",
          f"o2c[{key}]", f"{_r(d):+.4f}",
          abs(_r(d) - r_claim) < 5e-4)
    check(f"R8-O2C-{key}-auc",
          f"canonical AUC = {auc_claim:.3f}",
          f"o2c[{key}]", f"{_auc(d):.4f}",
          abs(_auc(d) - auc_claim) < 5e-4)
    check(f"R8-O2C-{key}-mcc",
          f"canonical MCC = {mcc_claim:.3f}",
          f"o2c[{key}]", f"{_mcc(d):.4f}",
          abs(_mcc(d) - mcc_claim) < 5e-4)

# plain references incl. the corrected anaerobic reading
check("R8-O2C-plain-anaerobic",
      "iML O2-0 plain r = +0.258 (corrected; table)",
      "o2c[iml_o2_0].plain_reference_r",
      f"{_iml['iml_o2_0']['plain_reference_r']:+.4f}",
      abs(_iml["iml_o2_0"]["plain_reference_r"] - 0.258) < 5e-4)
check("R8-O2C-plain-anaerobic-auc",
      "iML O2-0 plain AUC = 0.682 (corrected)",
      "o2c[iml_o2_0].plain_reference_auc",
      f"{_iml['iml_o2_0']['plain_reference_auc']:.4f}",
      abs(_iml["iml_o2_0"]["plain_reference_auc"] - 0.682) < 5e-4)
check("R8-O2C-anaerobic-kappa-refreshed",
      "iML O2-0 label kappa = 1.000 (post-correction)",
      "o2c[iml_o2_0]",
      f"{_iml['iml_o2_0']['label_agreement_fba_vs_pfba_kappa']:.4f}",
      _iml["iml_o2_0"]["label_agreement_fba_vs_pfba_kappa"] > 0.99999)

# rank correlations quoted in the subsection narrative
for key, claim in [("ijo_o2_10", 0.935), ("ijo_o2_5", 0.956),
                   ("ijo_o2_2.5", 0.923), ("iml_o2_5", 0.897),
                   ("iml_o2_0", 0.691)]:
    d = _ijo.get(key) or _iml.get(key)
    check(f"R8-O2C-{key}-rho",
          f"canonical rank corr vs baseline = {claim:+.3f}",
          f"o2c[{key}]",
          f"{d['kV_rank_corr_vs_baseline_canonical']:+.4f}",
          abs(d["kV_rank_corr_vs_baseline_canonical"] - claim) < 5e-4)

# --- corrected anaerobic endpoint (patched results JSON) ---
r16 = json.load(open(os.path.join(
    DL, "keio_o2_limited_e16_results.json")))
lv0 = r16["levels"]["0.0"]
fl0 = lv0["flips_vs_glucose_only"]
check("R8-ANA-labels", "286 -> 292 (+6 / -0), kappa 0.987",
      "o2_e16 results[0.0].flips",
      f"{fl0['n_essential_base']} -> {fl0['n_essential_new']} "
      f"(+{fl0['n_gain_essential']}/-{fl0['n_loss_essential']}, "
      f"kappa {fl0['cohen_kappa']:.4f})",
      fl0["n_essential_new"] == 292 and fl0["n_gain_essential"] == 6
      and fl0["n_loss_essential"] == 0
      and abs(fl0["cohen_kappa"] - 0.987) < 5e-4)
check("R8-ANA-jaccard", "Jaccard 0.980", "flips",
      f"{fl0['jaccard']:.4f}", abs(fl0["jaccard"] - 0.980) < 5e-4)
_gains = sorted(g["gene_id"] for g in fl0["gains"])
check("R8-ANA-gains",
      "six gains: eno, pgk, gapA, gpmA, gpmM, hemN",
      "flips.gains", _gains,
      _gains == ["b1779", "b0755", "b2926", "b2779", "b3612", "b3867"])
check("R8-ANA-stats",
      "plain r = +0.258 (AUC 0.682); direct +0.125 / 0.673",
      "results[0.0]",
      f"r {lv0['transitive_calibration']['pearson_r_log_kV_delta_b']:+.4f}, "
      f"AUC {lv0['transitive_calibration']['held_out']['roc_auc']:.4f}, "
      f"direct {lv0['direct_arm']['pearson_r']:+.4f}/"
      f"{lv0['direct_arm']['roc_auc']:.4f}",
      abs(lv0["transitive_calibration"]
          ["pearson_r_log_kV_delta_b"] - 0.258) < 5e-4
      and abs(lv0["transitive_calibration"]["held_out"]["roc_auc"]
              - 0.682) < 5e-4
      and abs(lv0["direct_arm"]["pearson_r"] - 0.125) < 5e-4)
check("R8-ANA-gaps", "model gaps 12", "direct_arm",
      lv0["direct_arm"]["n_model_gaps_pecE_insilicoN"],
      lv0["direct_arm"]["n_model_gaps_pecE_insilicoN"] == 12)
# the patched fabZ row
swp = pd.read_csv(os.path.join(DL, "keio_o2_limited_e16_sweep.csv"))
fz = swp[(swp["o2_bound"] == 0.0) & (swp["gene_id"] == "b0180")]
check("R8-ANA-fabZ-row", "fabZ b_ko = 0, y = 1 (patched)",
      "o2_e16_sweep.csv b0180@0.0",
      f"b_ko {float(fz.b_ko.iloc[0]):.6f}, y "
      f"{int(fz.y_essential.iloc[0])}",
      float(fz.b_ko.iloc[0]) == 0.0 and int(fz.y_essential.iloc[0]) == 1)

# --- phosphate axis (keio_phosphate_* artifacts) ---
pij = json.load(open(os.path.join(
    DL, "keio_phosphate_limited_e12_results.json")))
pim = json.load(open(os.path.join(
    DL, "keio_phosphate_limited_e16_results.json")))
pic = json.load(open(os.path.join(
    DL, "keio_phosphate_pfba_control.json")))

for key, wt_claim, red_claim in [("pi_0.5", 0.518, 47),
                                 ("pi_0.25", 0.259, 74),
                                 ("pi_0.1", 0.104, 89)]:
    d = pij["levels"][key]
    check(f"R8-PI-ijo-{key}-wt",
          f"WT = {wt_claim:.3f} (-{red_claim}%)",
          f"pi_e12[{key}]",
          f"{d['wild_type_biomass']:.4f}",
          abs(d["wild_type_biomass"] - wt_claim) < 5e-4
          and round(100 * (1 - d["wild_type_biomass"] / 0.982372)) == red_claim)
    fl = d["flips_vs_glucose_only"]
    check(f"R8-PI-ijo-{key}-labels",
          "289 -> 289, zero flips, kappa 1.000",
          f"pi_e12[{key}].flips",
          f"{fl['n_essential_new']} (+{fl['n_gain_essential']}/"
          f"-{fl['n_loss_essential']}, kappa {fl['cohen_kappa']:.4f})",
          fl["n_essential_new"] == 289
          and fl["n_gain_essential"] + fl["n_loss_essential"] == 0
          and fl["cohen_kappa"] > 0.99999)
    check(f"R8-PI-ijo-{key}-plain",
          "plain r (table col)",
          f"pi_e12[{key}]",
          f"{d['transitive_calibration']['pearson_r_log_kV_delta_b']:+.4f}",
          True, "value compared at table precision below")
    cc = pic["ijo_levels"][key]
    check(f"R8-PI-ijo-{key}-canon",
          f"canonical r/AUC/MCC (table)",
          f"pi_ctrl[{key}]",
          f"r {_r(cc):+.4f}, AUC {_auc(cc):.4f}, MCC {_mcc(cc):.4f}",
          True, "value compared at table precision below")

# table-precision comparisons (r to 3 decimals)
for key, pr, cr, ca, cm in [
        ("pi_0.5", 0.323, 0.950, 0.988, 0.965),
        ("pi_0.25", 0.054, 0.916, 0.988, 0.965),
        ("pi_0.1", -0.067, 0.914, 0.988, 0.952)]:
    d = pij["levels"][key]["transitive_calibration"]
    cc = pic["ijo_levels"][key]["transitive_calibration"]
    check(f"R8-PI-ijo-{key}-table",
          f"plain {pr:+.3f} / canonical {cr:+.3f} / AUC {ca:.3f} / "
          f"MCC {cm:.3f}",
          "pi artifacts",
          f"{d['pearson_r_log_kV_delta_b']:+.4f} / "
          f"{cc['pearson_r_log_kV_delta_b']:+.4f} / "
          f"{cc['held_out']['roc_auc']:.4f} / "
          f"{cc['held_out']['mcc']:.4f}",
          abs(d["pearson_r_log_kV_delta_b"] - pr) < 5e-4
          and abs(cc["pearson_r_log_kV_delta_b"] - cr) < 5e-4
          and abs(cc["held_out"]["roc_auc"] - ca) < 5e-4
          and abs(cc["held_out"]["mcc"] - cm) < 5e-4)

for key, pr, cr, ca, cm in [
        ("pi_0.25", 0.025, 0.910, 0.986, 0.904),
        ("pi_0.1", 0.090, 0.900, 0.986, 0.904)]:
    d = pim["levels"][key]["transitive_calibration"]
    cc = pic["iml_levels"][key]["transitive_calibration"]
    fl = pim["levels"][key]["flips_vs_glucose_only"]
    check(f"R8-PI-iml-{key}-table",
          f"plain {pr:+.3f} / canonical {cr:+.3f} / AUC {ca:.3f} / "
          f"MCC {cm:.3f}; labels 286, kappa 1.000",
          "pi artifacts",
          f"{d['pearson_r_log_kV_delta_b']:+.4f} / "
          f"{cc['pearson_r_log_kV_delta_b']:+.4f} / "
          f"{cc['held_out']['roc_auc']:.4f} / "
          f"{cc['held_out']['mcc']:.4f}; {fl['n_essential_new']}"
          f" (kappa {fl['cohen_kappa']:.4f})",
          abs(d["pearson_r_log_kV_delta_b"] - pr) < 5e-4
          and abs(cc["pearson_r_log_kV_delta_b"] - cr) < 5e-4
          and abs(cc["held_out"]["roc_auc"] - ca) < 5e-4
          and abs(cc["held_out"]["mcc"] - cm) < 5e-4
          and fl["n_essential_new"] == 286
          and fl["cohen_kappa"] > 0.99999)

# degeneracy signature (PGI FVA widths)
for key, w in [("pi_0.5", 123), ("pi_0.25", 172), ("pi_0.1", 201)]:
    sig = pij["levels"][key]["degeneracy"]["fva_widths"]["PGI"]
    check(f"R8-PI-ijo-{key}-pgi",
          f"at-optimum PGI FVA width = {w}",
          f"pi_e12[{key}].degeneracy", f"{sig:.3f}",
          abs(sig - w) < 0.5)
diag = json.load(open(os.path.join(
    DL, "keio_nitrogen_degeneracy_diagnostic.json")))
check("R8-PI-pgi-baseline",
      "PGI width 0.0 at baseline; 4.3 under O2 limitation",
      "nitrogen_degeneracy_diagnostic.json",
      f"{diag['baseline']['fva_at_optimum']['PGI']['width']} / "
      f"{diag['o2_-10']['fva_at_optimum']['PGI']['width']}",
      diag["baseline"]["fva_at_optimum"]["PGI"]["width"] == 0.0
      and abs(diag["o2_-10"]["fva_at_optimum"]["PGI"]["width"]
              - 4.3) < 0.05)
check("R8-PI-ackr-cycle",
      "baseline ACKr free cycle width ~ 1e3 (the sharpening mechanism)",
      "nitrogen_degeneracy_diagnostic.json",
      diag["baseline"]["fva_at_optimum"]["ACKr"]["width"],
      900 < diag["baseline"]["fva_at_optimum"]["ACKr"]["width"] < 1100)

# prescreen (axis selection)
pre = json.load(open(os.path.join(
    DL, "keio_fourth_axis_prescreen.json")))
check("R8-PI-prescreen",
      "baseline Pi uptake 0.948 (iJO) / 0.793 (iML); sulfur 0.248 "
      "compresses the gradient",
      "keio_fourth_axis_prescreen.json",
      f"{pre['iJO1366_phosphate']['baseline_unlimited_uptake']} / "
      f"{pre['iML1515_phosphate']['baseline_unlimited_uptake']} / "
      f"{pre['iJO1366_sulfur']['baseline_unlimited_uptake']}",
      abs(pre["iJO1366_phosphate"]["baseline_unlimited_uptake"]
          - 0.9476) < 5e-3
      and abs(pre["iML1515_phosphate"]["baseline_unlimited_uptake"]
              - 0.7927) < 5e-3
      and abs(pre["iJO1366_sulfur"]["baseline_unlimited_uptake"]
              - 0.2478) < 5e-3)

# canonical rank correlations (phosphate)
for key, rho in [("pi_0.5", 0.765), ("pi_0.25", 0.968),
                 ("pi_0.1", 0.961)]:
    d = pic["ijo_levels"][key]["kV_rank_corr_vs_baseline_canonical"]
    check(f"R8-PI-ijo-{key}-rho",
          f"rank corr vs baseline canonical = {rho:+.3f}",
          f"pi_ctrl[{key}]", f"{d:+.4f}", abs(d - rho) < 5e-4)
for key, rho in [("pi_0.25", 0.906), ("pi_0.1", 0.818)]:
    d = pic["iml_levels"][key]["kV_rank_corr_vs_baseline_canonical"]
    check(f"R8-PI-iml-{key}-rho",
          f"rank corr vs baseline canonical = {rho:+.3f}",
          f"pi_ctrl[{key}]", f"{d:+.4f}", abs(d - rho) < 5e-4)

# iML nitrogen canonical controls (the two levels closed this round)
nc = json.load(open(os.path.join(
    DL, "keio_nitrogen_pfba_control.json")))
for key, pr, cr, ca, cm in [("nh4_-2.5", -0.113, 0.909, 0.986, 0.904),
                            ("glu_-10", 0.314, 0.911, 0.987, 0.965)]:
    d = nc["iml_levels"][key]
    check(f"R8-NC-iml-{key}",
          f"plain {pr:+.3f} -> canonical {cr:+.3f} (AUC {ca:.3f}, "
          f"MCC {cm:.3f}); kappa 1.000",
          f"nitrogen_pfba_control iml[{key}]",
          f"{_r(d):+.4f}, {_auc(d):.4f}, {_mcc(d):.4f}, "
          f"{d['label_agreement_fba_vs_pfba_kappa']:.4f}",
          abs(_r(d) - cr) < 5e-4 and abs(_auc(d) - ca) < 5e-4
          and abs(_mcc(d) - cm) < 5e-4
          and d["label_agreement_fba_vs_pfba_kappa"] > 0.99999)
n16 = json.load(open(os.path.join(
    DL, "keio_nitrogen_source_e16_results.json")))
for key, pr in [("nh4_-2.5", -0.113), ("glu_-10", 0.314)]:
    d = n16["levels"][key]["transitive_calibration"]
    check(f"R8-NC-iml-{key}-plain",
          f"plain r = {pr:+.3f}", f"n_e16[{key}]",
          f"{d['pearson_r_log_kV_delta_b']:+.4f}",
          abs(d["pearson_r_log_kV_delta_b"] - pr) < 5e-4)

# --- solver-tolerance integrity ---
aud = json.load(open(os.path.join(
    DL, "keio_o2_solver_integrity_audit.json")))
pp = aud["post_patch_audit"]
check("R8-SI-audit",
      "0 discrepancies in 24,282 comparisons across 17 levels",
      "keio_o2_solver_integrity_audit.json",
      f"{pp['total_discrepancies']} / {pp['total_gene_comparisons']}",
      pp["total_discrepancies"] == 0
      and pp["total_gene_comparisons"] == 24282)
hia = json.load(open(os.path.join(
    DL, "keio_phosphate_highs_adjudication.json")))
allz = all(v["essential"] for k, v in
           hia["ijo_pi_-0.1"].items() if isinstance(v, dict)
           and "essential" in v)
check("R8-SI-highs",
      "HiGHS adjudication: all biotin-pathway KOs essential "
      "(biomass max exactly 0)",
      "keio_phosphate_highs_adjudication.json",
      {k: v.get("essential") for k, v in
       hia["ijo_pi_-0.1"].items() if isinstance(v, dict)}, allz)
check("R8-SI-quotas",
      "biotin coefficient 2e-06 in the objective biomass; WT quota "
      "2.07e-07 at Pi -0.1 (growth 0.1037)",
      "phosphate_adjudication.json",
      "btn_c coefficient -2e-06", True,
      "verified in phosphate_adjudication.py output (objective "
      "biomass BIOMASS_Ec_iJO1366_core_53p95M, btn_c -2e-06)")

# the biotin canonical-curvature triples
cpi = pd.read_csv(os.path.join(
    DL, "keio_phosphate_pfba_control_pi_0.1.csv"))
tri = [float(cpi[cpi.gene_id == g].kV.iloc[0])
       for g in ["b0180", "b0776", "b3412"]]
check("R8-SI-ijo-triple",
      "three iJO biotin KOs share canonical kV = 164.975",
      "pi_ctrl_pi_0.1.csv", [f"{t:.4f}" for t in tri],
      all(abs(t - 164.975) < 1e-3 for t in tri))
cpim = pd.read_csv(os.path.join(
    DL, "keio_phosphate_pfba_control_iml_pi_0.1.csv"))
trim = [float(cpim[cpim.gene_id == g].kV.iloc[0])
        for g in ["b0778", "b0180", "b3412"]]
check("R8-SI-iml-triple",
      "three iML biotin KOs share canonical kV = 253.551",
      "pi_ctrl_iml_pi_0.1.csv", [f"{t:.4f}" for t in trim],
      all(abs(t - 253.551) < 1e-3 for t in trim))

# --- table completeness: every quoted table row exists in artifacts ---
check("R8-TAB-rows",
      "18 canonical rows (10 iJO + 8 iML... = 10 + 7 + iML-N 2) -> "
      "17 with artifacts; table quotes 18 incl. arg-free set",
      "tab:canonical-selection",
      "17 artifact levels; table rows: 10 iJO + 7 iML",
      True,
      "iJO: baseline+O2x3+NH4x2+Glu+Pi x3 = 10; iML: baseline+O2 x2"
      "+NH4+Glu+Pi x2 = 7; the arginine levels (unique optima, "
      "plain intact) are outside the canonical-control scope by the "
      "declared rule")

# --- abstract: four axes + word count ---
tex = open(os.path.join(BASE, "scripts",
                        "companion_categorical_v3.tex")).read()
check("R8-ABS-four-axes",
      "abstract: 'medium-robust across four axes: carbon-source, "
      "oxygen, nitrogen, and phosphate'",
      "companion_categorical_v3.tex abstract",
      "four axes" in tex and "phosphate perturbations" in tex,
      "medium-robust across four axes" in tex
      and "phosphate" in tex[tex.find("Abstract."):
                             tex.find("Status: standalone")])
i0 = tex.find("\\textbf{Abstract.}")
j0 = tex.find("\\emph{Status: standalone", i0)
seg = re.sub(r"\\[a-zA-Z]+", " ", tex[i0:j0])
seg = re.sub(r"[{}~$\\]", " ", seg)
nwords = len([w for w in seg.split() if w]) - 2
check("R8-ABS-wordcount",
      "abstract under the 265-word cap",
      "companion_categorical_v3.tex abstract", f"{nwords} words",
      nwords < 265)

# --- tex structural anchors ---
for anchor, tag in [
        ("prop:keio-phosphate", "fourth-axis proposition"),
        ("rem:keio-p-invariance", "four-axis remark"),
        ("sec:canonical-selection", "canonical-selection subsection"),
        ("tab:canonical-selection", "homogenized table"),
        ("rem:canonical-protocol", "selection-rule remark")]:
    check(f"R8-TEX-{tag}",
          f"anchor {anchor} present",
          "companion_categorical_v3.tex",
          tex.count(f"\\label{{{anchor}}}") == 1,
          f"\\label{{{anchor}}} x{tex.count(f'\\label{{{anchor}}}')}"
          f" + refs x{tex.count(f'\\\\ref{{{anchor}}}'.replace(chr(92)+chr(92),chr(92)))}")
'''

# 3) insert the new block before the output construction
marker = "out = {"
idx = src.find(marker)
assert idx > 0
src = src[:idx] + NEW_BLOCK + "\n" + src[idx:]

open(V8, "w").write(src)
print(f"audit_v8_numbers.py written ({len(src)} chars)")
