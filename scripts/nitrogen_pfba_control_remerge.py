#!/usr/bin/env python3
"""Re-merge the pFBA canonical-vertex control with the plain-FBA
biomass values, producing the corrected PART B control artifacts.

Why: cobra's pfba().objective_value returns the minimized L1 total
flux, not the growth rate.  The swept canonical kV values are valid
(the flux vectors are the parsimonious-optimum vertices); only the
b/delta_b/y_essential columns were contaminated.  Because pFBA at
fraction_of_optimum = 1.0 preserves the objective value exactly, the
correct biomass rates are the plain-FBA optima already deposited by
the probe (verified at the baseline medium: pFBA biomass flux
0.982372 = plain-FBA optimum 0.982372).  This script re-merges and
recomputes the statistics -- mathematically identical to re-running
the sweeps, at zero LP cost.

Outputs (download/, overwrite in place):
  keio_nitrogen_pfba_control.json            (corrected)
  keio_nitrogen_pfba_control_<level>.csv     (corrected b columns)
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from nitrogen_source_keio_probe import (
    IJO_LEVELS, keio_tables, transitive_calibration, direct_arm)
from cobra.io import load_json_model
from cobra.flux_analysis import pfba
from nitrogen_source_keio_probe import set_ijo_medium
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

CTRL_JSON = os.path.join(OUT_DIR, "keio_nitrogen_pfba_control.json")
control = json.load(open(CTRL_JSON))

# plain-FBA biomass source per control level
BASE_FBA = os.path.join(OUT_DIR, "keio_glucose_only_e12.csv")
N_FBA = os.path.join(OUT_DIR, "keio_nitrogen_source_e12_sweep.csv")


def fba_frame(key):
    if key == "baseline":
        df = pd.read_csv(BASE_FBA)
    else:
        df = pd.read_csv(N_FBA)
        df = df[df["level"] == key]
    return df[["gene_id", "b_wt", "b_ko", "delta_b", "y_essential",
               "n_gpr_rxns"]]


# ---- verify the objective-preservation claim at every control level ----
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO_ID = [r.id for r in ijo.reactions
          if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
verify = {}
for key in control["levels"]:
    if key == "baseline":
        set_ijo_medium(ijo, {"nh4_lb": -1000.0, "n_source": None})
    else:
        set_ijo_medium(ijo, next(l for l in IJO_LEVELS if l["key"] == key))
    fba_b = float(ijo.optimize().objective_value)
    pfba_b = float(pfba(ijo).fluxes[BIO_ID])
    verify[key] = {"fba_optimum": round(fba_b, 6),
                   "pfba_biomass_flux": round(pfba_b, 6),
                   "abs_diff": round(abs(fba_b - pfba_b), 9)}
    print(f"objective preservation @ {key}: FBA {fba_b:.6f} vs "
          f"pFBA {pfba_b:.6f} (diff {abs(fba_b-pfba_b):.2e})", flush=True)
    assert abs(fba_b - pfba_b) < 1e-6

keio_tab, st6_tab = keio_tables()
base_kV = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})

for key, old in list(control["levels"].items()):
    csv_path = os.path.join(OUT_DIR, f"keio_nitrogen_pfba_control_{key}.csv")
    df = pd.read_csv(csv_path)
    fb = fba_frame(key)
    m = df[["gene_id", "kV", "n_changed"]].merge(fb, on="gene_id",
                                                how="inner")
    assert len(m) == len(df), (key, len(m), len(df))
    cal = transitive_calibration(m)
    da, _ = direct_arm(m, keio_tab, st6_tab)
    mg = m[["gene_id", "kV"]].merge(base_kV, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
    # label agreement between the canonical-kV frame (labels = plain-FBA
    # labels, since pFBA preserves the optimum) and the deposited
    # plain-FBA sweep -- must be exact
    if key == "baseline":
        pl = pd.read_csv(BASE_FBA)[["gene_id", "y_essential"]]
    else:
        pl = pd.read_csv(N_FBA)
        pl = pl[pl["level"] == key][["gene_id", "y_essential"]]
    mgl = pl.merge(m[["gene_id", "y_essential"]], on="gene_id",
                   suffixes=("_fba", "_canon"))
    kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                        mgl.y_essential_canon))
    control["levels"][key] = {
        "wild_type_biomass": float(m.b_wt.iloc[0]),
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kappa_lab,
        "n_essential": int(m.y_essential.sum()),
        "n_genes": int(len(m)),
    }
    # corrected CSV
    out = m[["gene_id", "n_gpr_rxns", "n_changed", "b_wt", "b_ko",
             "delta_b", "y_essential", "kV"]].copy()
    out.insert(0, "level", key)
    out.to_csv(csv_path, index=False)
    print(f"{key}: b_wt {float(m.b_wt.iloc[0]):.4f}; "
          f"{int(m.y_essential.sum())} essential; "
          f"r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
          f"held-out AUC = {cal['held_out']['roc_auc']:.4f}, "
          f"MCC = {cal['held_out']['mcc']:.4f}; direct r "
          f"{da['pearson_r']:+.4f}, AUC {da['roc_auc']:.4f}; "
          f"rank corr vs baseline {rho:+.4f}; label kappa "
          f"{kappa_lab:.4f}", flush=True)

control["objective_preservation_check"] = verify
control["method_note"] = (
    "Canonical kV values are the pFBA (parsimonious) vertices swept "
    "by nitrogen_degeneracy_diagnostic.py PART B; biomass rates are "
    "the plain-FBA optima, which pFBA preserves exactly at "
    "fraction_of_optimum=1.0 (see objective_preservation_check). "
    "pfba().objective_value returns the minimized L1 total flux and "
    "is NOT the growth rate; the b columns of the originally swept "
    "CSVs were contaminated by that misread and have been re-merged "
    "here (mathematically identical to a corrected re-run).")
control["plain_fba_reference"] = {
    k: control["plain_auc"][k] for k in control["plain_auc"]}
with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)
print("\nCORRECTED CONTROL WRITTEN.")
