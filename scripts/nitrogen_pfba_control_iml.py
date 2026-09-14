#!/usr/bin/env python3
"""Canonical (pFBA) controls for the two iML1515 nitrogen-axis levels
whose plain readings degenerated (nh4_-2.5, glu_-10) -- closing the
gap in the nitrogen-round control (which iterated iJO levels only).

Import-safe (reuses the nitrogen probe's machinery), resumable.
Writes keio_nitrogen_pfba_control_iml_<key>.csv and updates
keio_nitrogen_pfba_control.json.
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from cobra.flux_analysis import pfba
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

from nitrogen_source_keio_probe import (
    set_iml_medium, keio_tables, transitive_calibration, direct_arm)

CTRL_JSON = os.path.join(OUT_DIR, "keio_nitrogen_pfba_control.json")
IML_KEYS = ["nh4_-2.5", "glu_-10"]

ctrl = json.load(open(CTRL_JSON))
if "iml_levels" not in ctrl:
    ctrl["iml_levels"] = {}

iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
BIO_IML = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO_IML = r.id
        break
assert BIO_IML

base_kV = pd.read_csv(os.path.join(
    OUT_DIR, "keio_o2_pfba_control_iml_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
plain_sweep = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_source_e16_sweep.csv"))
keio_tab, st6_tab = keio_tables()


def pfba_sweep_iml(model, b_wt, v_wt):
    rows = []
    t0 = time.time()
    for g in model.genes:
        g_id = g.id
        try:
            with model:
                for r in model.reactions:
                    if g_id in r.gene_reaction_rule:
                        r.lower_bound = 0
                        r.upper_bound = 0
                try:
                    sol = pfba(model)
                    b_ko = float(sol.fluxes[BIO_IML])
                    v_ko = sol.fluxes
                except Exception:
                    b_ko, v_ko = 0.0, None
            if v_ko is None:
                v_ko = pd.Series(0.0, index=v_wt.index)
            dv = v_ko - v_wt
            mask = np.abs(dv) > 1e-6
            kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
            n_gpr = sum(1 for r in model.reactions
                        if g_id in r.gene_reaction_rule)
            rows.append({
                "gene_id": g_id, "n_gpr_rxns": n_gpr,
                "n_changed": int(mask.sum()), "b_wt": b_wt, "b_ko": b_ko,
                "delta_b": float(b_wt - b_ko),
                "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
            })
        except Exception:
            rows.append({"gene_id": g_id, "n_gpr_rxns": 0, "n_changed": 0,
                         "b_wt": b_wt, "b_ko": float("nan"),
                         "delta_b": float("nan"), "y_essential": -1,
                         "kV": 0.0})
        if len(rows) % 400 == 0:
            print(f"    {len(rows)}/{len(model.genes)} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    return [r for r in rows if r["y_essential"] >= 0]


# level definitions mirror the nitrogen probe's IML arm
from nitrogen_source_keio_probe import IML_LEVELS as N_IML_LEVELS
for key in IML_KEYS:
    if key in ctrl["iml_levels"] and os.path.exists(os.path.join(
            OUT_DIR, f"keio_nitrogen_pfba_control_iml_{key}.csv")):
        print(f"{key}: already done -- skipping", flush=True)
        continue
    lv = next(l for l in N_IML_LEVELS if l["key"] == key)
    print(f"\n----- iML1515 canonical, {key} -----", flush=True)
    set_iml_medium(iml, lv)
    # objective-preservation check
    raw = iml.optimize()
    par_wt = pfba(iml)
    assert abs(float(raw.objective_value)
               - float(par_wt.fluxes[BIO_IML])) < 1e-6
    b_wt = float(par_wt.fluxes[BIO_IML])
    rows = pfba_sweep_iml(iml, b_wt, par_wt.fluxes)
    df = pd.DataFrame(rows)
    print(f"  sweep done, {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    mg = df[["gene_id", "kV"]].merge(base_kV, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
    pl = plain_sweep[plain_sweep["level"] == key]
    mgl = pl[["gene_id", "y_essential"]].merge(
        df[["gene_id", "y_essential"]], on="gene_id",
        suffixes=("_fba", "_canon"))
    kap = float(cohen_kappa_score(mgl.y_essential_fba,
                                  mgl.y_essential_canon))
    ctrl["iml_levels"][key] = {
        "wild_type_biomass": b_wt,
        "n_essential": int(df.y_essential.sum()),
        "n_genes": int(len(df)),
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kap,
    }
    df.to_csv(os.path.join(
        OUT_DIR, f"keio_nitrogen_pfba_control_iml_{key}.csv"),
        index=False)
    with open(CTRL_JSON, "w") as f:
        json.dump(ctrl, f, indent=2)
    print(f"  canonical r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
          f"AUC {cal['held_out']['roc_auc']:.4f}; MCC "
          f"{cal['held_out']['mcc']:.4f}; rho {rho:+.4f}; kappa "
          f"{kap:.4f}", flush=True)

json.dump(ctrl, open(CTRL_JSON, "w"), indent=2)
print("\niML nitrogen canonical controls done.")
