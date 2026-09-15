#!/usr/bin/env python3
"""Pull exact numbers for the fifth-axis + arginine manuscript text."""
import json, os, re

D = "/home/z/my-project/metabolic-curvature-measure/download"

# b0887 gene name from the iJO plain sweep
import pandas as pd
sw = pd.read_csv(os.path.join(D, "keio_iron_limited_e12_sweep.csv"))
row = sw[sw.gene_id == "b0887"]
print("b0887 rows:", row[["fe_bound", "gene_name", "b_ko",
                          "y_essential"]].to_dict("records"))

# integrity scan numbers
sc = json.load(open(os.path.join(D, "keio_iron_integrity_scan.json")))
tot = 0
for lv, rec in sc["levels"].items():
    tot += rec["n_genes"]
    print(lv, "n_genes", rec["n_genes"], "maxdiff",
          f"{rec['cross_arm_max_abs_b_ko_diff']:.2e}",
          "n>1e-6", rec["cross_arm_n_diff_gt_1e-6"])
print("total cross-arm comparisons:", tot)

# iron control canonical stats
ic = json.load(open(os.path.join(D, "keio_iron_pfba_control.json")))
for key in ("fe_0.01", "fe_0.005", "fe_0.0025"):
    v = ic["ijo_levels"][key]
    t = v["transitive_calibration"]
    print("iJO", key, "r", round(t["pearson_r_log_kV_delta_b"], 4),
          "AUC", round(t["held_out"]["roc_auc"], 4),
          "MCC", round(t["held_out"]["mcc"], 4),
          "rho", round(v["kV_rank_corr_vs_baseline_canonical"], 4),
          "kappa", round(v["label_agreement_fba_vs_pfba_kappa"], 4),
          "plain_r", round(v["plain_reference_r"], 4),
          "plain_auc", round(v["plain_reference_auc"], 4))
for key in ("fe_0.005", "fe_0.0025"):
    v = ic["iml_levels"][key]
    t = v["transitive_calibration"]
    print("iML", key, "r", round(t["pearson_r_log_kV_delta_b"], 4),
          "AUC", round(t["held_out"]["roc_auc"], 4),
          "MCC", round(t["held_out"]["mcc"], 4),
          "rho", round(v["kV_rank_corr_vs_baseline_canonical"], 4),
          "kappa", round(v["label_agreement_fba_vs_pfba_kappa"], 4),
          "plain_r", round(v["plain_reference_r"], 4),
          "plain_auc", round(v["plain_reference_auc"], 4))

# iron plain results (WT, degeneracy)
for f, tag in [("keio_iron_limited_e12_results.json", "iJO"),
               ("keio_iron_limited_e16_results.json", "iML")]:
    r = json.load(open(os.path.join(D, f)))
    for key, lv in r["levels"].items():
        fl = lv["flips_vs_glucose_only"]
        dg = lv["degeneracy"]
        print(tag, key, "WT", lv["wild_type_biomass"],
              "raw_glc", dg["raw_glc_uptake"],
              "pfba_glc", dg["pfba_glc_uptake"],
              "PGI", dg["fva_widths"].get("PGI"),
              "flips", fl["n_gain_essential"], fl["n_loss_essential"],
              "kappa", round(fl["cohen_kappa"], 4),
              "byproducts", lv.get("byproducts", {}))

# arginine canonical entries
nc = json.load(open(os.path.join(D, "keio_nitrogen_pfba_control.json")))
for arm, key in [("levels", "arg_-10"), ("iml_levels", "arg_-10")]:
    v = nc[arm][key]
    t = v["transitive_calibration"]
    print("ARG", arm, "WT", v["wild_type_biomass"],
          "n_ess", v["n_essential"], "/", v["n_genes"],
          "r", round(t["pearson_r_log_kV_delta_b"], 4),
          "AUC", round(t["held_out"]["roc_auc"], 4),
          "MCC", round(t["held_out"]["mcc"], 4),
          "rho", round(v["kV_rank_corr_vs_baseline_canonical"], 4),
          "kappa", round(v["label_agreement_fba_vs_pfba_kappa"], 4),
          "plain_r", round(v["plain_reference_r"], 4))

# direct arms for iron (for completeness)
for key in ("fe_0.01", "fe_0.005", "fe_0.0025"):
    da = ic["ijo_levels"][key]["direct_arm"]
    print("iJO", key, "direct r/AUC:", round(da["pearson_r"], 4),
          round(da["roc_auc"], 4))
for key in ("fe_0.005", "fe_0.0025"):
    da = ic["iml_levels"][key]["direct_arm"]
    print("iML", key, "direct r/AUC:", round(da["pearson_r"], 4),
          round(da["roc_auc"], 4))

# abstract word count (minipage block)
tex = open("/home/z/my-project/metabolic-curvature-measure/scripts/"
           "companion_categorical_v3.tex").read()
m = re.search(r"\\begin\{minipage\}.*?\\end\{minipage\}", tex, re.S)
if m:
    body = m.group(0)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-,\.]*", body)
    # crude but consistent with prior rounds: count whitespace tokens
    plain = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})*", " ", body)
    plain = re.sub(r"[{}\\$%&^_~]", " ", plain)
    toks = [t for t in plain.split() if re.search(r"[A-Za-z0-9]", t)]
    print("abstract-ish token count:", len(toks))
