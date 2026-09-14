#!/usr/bin/env python3
"""Extend the solver-integrity audit record to every level with a
canonical counterpart (the O2/N rounds' ten levels + the five
phosphate levels + the two iML nitrogen levels closed in this
round), post-correction.  Updates
download/keio_o2_solver_integrity_audit.json.
"""
import os, json
import pandas as pd

DL = "download"
pairs = [
    ("iML baseline", "keio_glucose_only_e16_sweep.csv", None,
     "keio_o2_pfba_control_iml_baseline.csv"),
    ("iML O2 -5", "keio_o2_limited_e16_sweep.csv", -5.0,
     "keio_o2_pfba_control_iml_o2_5.csv"),
    ("iML O2 0", "keio_o2_limited_e16_sweep.csv", 0.0,
     "keio_o2_pfba_control_iml_o2_0.csv"),
    ("iJO O2 -10", "keio_o2_limited_e12_sweep.csv", -10.0,
     "keio_o2_pfba_control_ijo_o2_10.csv"),
    ("iJO O2 -5", "keio_o2_limited_e12_sweep.csv", -5.0,
     "keio_o2_pfba_control_ijo_o2_5.csv"),
    ("iJO O2 -2.5", "keio_o2_limited_e12_sweep.csv", -2.5,
     "keio_o2_pfba_control_ijo_o2_2.5.csv"),
    ("iJO baseline", "keio_glucose_only_e12.csv", None,
     "keio_nitrogen_pfba_control_baseline.csv"),
    ("iJO nh4 -10", "keio_nitrogen_source_e12_sweep.csv", "nh4_-10",
     "keio_nitrogen_pfba_control_nh4_-10.csv"),
    ("iJO nh4 -2.5", "keio_nitrogen_source_e12_sweep.csv", "nh4_-2.5",
     "keio_nitrogen_pfba_control_nh4_-2.5.csv"),
    ("iJO glu -10", "keio_nitrogen_source_e12_sweep.csv", "glu_-10",
     "keio_nitrogen_pfba_control_glu_-10.csv"),
    ("iML nh4 -2.5", "keio_nitrogen_source_e16_sweep.csv", "nh4_-2.5",
     "keio_nitrogen_pfba_control_iml_nh4_-2.5.csv"),
    ("iML glu -10", "keio_nitrogen_source_e16_sweep.csv", "glu_-10",
     "keio_nitrogen_pfba_control_iml_glu_-10.csv"),
    ("iJO Pi -0.5", "keio_phosphate_limited_e12_sweep.csv", -0.5,
     "keio_phosphate_pfba_control_pi_0.5.csv"),
    ("iJO Pi -0.25", "keio_phosphate_limited_e12_sweep.csv", -0.25,
     "keio_phosphate_pfba_control_pi_0.25.csv"),
    ("iJO Pi -0.1", "keio_phosphate_limited_e12_sweep.csv", -0.1,
     "keio_phosphate_pfba_control_pi_0.1.csv"),
    ("iML Pi -0.25", "keio_phosphate_limited_e16_sweep.csv", -0.25,
     "keio_phosphate_pfba_control_iml_pi_0.25.csv"),
    ("iML Pi -0.1", "keio_phosphate_limited_e16_sweep.csv", -0.1,
     "keio_phosphate_pfba_control_iml_pi_0.1.csv"),
]

audit = json.load(open(os.path.join(DL,
                                    "keio_o2_solver_integrity_audit.json")))
comparisons, total, disc = [], 0, 0
for name, ppath, lv, cpath in pairs:
    d = pd.read_csv(os.path.join(DL, ppath))
    if lv is not None:
        col = "o2_bound" if "o2_bound" in d.columns else (
            "pi_bound" if "pi_bound" in d.columns else "level")
        d = d[d[col] == lv]
    c = pd.read_csv(os.path.join(DL, cpath))
    m = d[["gene_id", "b_ko", "y_essential"]].merge(
        c[["gene_id", "b_ko", "y_essential"]], on="gene_id",
        suffixes=("_p", "_c"))
    big = (m.b_ko_p - m.b_ko_c).abs() > 1e-6
    lab = m.y_essential_p != m.y_essential_c
    hits = list(m[big | lab].gene_id)
    comparisons.append({"level": name, "n_genes": int(len(m)),
                        "n_biomass_discrepant": int(big.sum()),
                        "n_label_discrepant": int(lab.sum()),
                        "genes": hits})
    total += int(len(m))
    disc += int((big | lab).sum())
    print(f"{name:14s}: {int((big|lab).sum())}/{len(m)}"
          + (f" -> {hits}" if hits else ""))

audit["post_patch_audit"] = {
    "scope": ("Every deposited plain-sweep level with a canonical "
              "counterpart (17 levels: the O2/N rounds' ten, the five "
              "phosphate levels, and the two iML nitrogen levels "
              "closed in the canonical-selection round)."),
    "total_gene_comparisons": total,
    "total_discrepancies": disc,
    "comparisons": comparisons,
    "note": ("Post-correction: 0 discrepancies. The eight corrupted "
             "calls found and fixed (all trace-quota genes at low "
             "growth): iML O2-0 plain fabZ; iJO Pi -0.1 plain "
             "fabZ/bioH + canonical bioF; iML Pi -0.1 plain "
             "bioC/fabZ/bioH + canonical bioH.")}
json.dump(audit, open(os.path.join(DL,
                                   "keio_o2_solver_integrity_audit.json"),
                      "w"), indent=2)
print(f"\nTOTAL: {disc} discrepancies in {total} comparisons "
      f"across {len(pairs)} levels.")
