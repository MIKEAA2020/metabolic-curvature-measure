#!/usr/bin/env python3
"""Canonical (pFBA) control for the arginine-substitution levels
(arg_-10 on iJO1366 and iML1515) -- completing the axis x selection
table symmetry.

Every other nitrogen-axis level already carries canonical statistics
(keio_nitrogen_pfba_control.json: iJO baseline / nh4_-10 / nh4_-2.5 /
glu_-10; iML nh4_-2.5 / glu_-10).  Arginine -- the substitution level
whose optimum sits 28% ABOVE the glucose-minimal baseline (carbon
re-pinned by the N+C co-substrate) -- is the last gap.  Plain
references: iJO r +0.802 / AUC 0.981; iML r +0.915 / AUC 0.997.

Conventions identical to nitrogen_pfba_control_iml.py and the
phosphate/O2 canonical controls: biomass read from the pFBA solution
vector at the biomass reaction (cobra's pfba().objective_value returns
the minimized L1 total flux, not growth); objective preservation
asserted per level; labels unchanged by construction and verified
against the deposited plain sweeps (Cohen kappa); kV rank correlation
against the glucose-only baseline canonical sweep.

Import-safe (reuses the nitrogen probe's machinery), resumable per
level.  Writes keio_nitrogen_pfba_control_arg_-10.csv (iJO) and
keio_nitrogen_pfba_control_iml_arg_-10.csv (iML); updates
keio_nitrogen_pfba_control.json (levels/arg_-10, iml_levels/arg_-10).
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
    set_ijo_medium, set_iml_medium, keio_tables, transitive_calibration,
    direct_arm, IJO_LEVELS, IML_LEVELS)

CTRL_JSON = os.path.join(OUT_DIR, "keio_nitrogen_pfba_control.json")
ctrl = json.load(open(CTRL_JSON))
ctrl.setdefault("levels", {})
ctrl.setdefault("iml_levels", {})
KEY = "arg_-10"

keio_tab, st6_tab = keio_tables()


def pfba_sweep_ijo(model, b_wt, flux_wt, bio_id):
    """E12-convention canonical sweep (from the phosphate probe)."""
    rows = []
    t0 = time.time()
    for gene in model.genes:
        gpr_rxns = [r for r in gene.reactions if gene in r.genes]
        if not gpr_rxns:
            continue
        with model:
            for r in gpr_rxns:
                r.lower_bound = 0
                r.upper_bound = 0
            try:
                sol = pfba(model)
                b_ko = float(sol.fluxes[bio_id])
                flux_ko = sol.fluxes.to_dict()
            except Exception:
                b_ko, flux_ko = 0.0, {}
        kV = 0.0
        n_changed = 0
        for r_id, v_wt in flux_wt.items():
            dv = flux_ko.get(r_id, 0.0) - v_wt
            if abs(dv) > 1e-6:
                kV += dv * dv
                n_changed += 1
        rows.append({
            "gene_id": gene.id, "gene_name": gene.name,
            "n_gpr_rxns": len(gpr_rxns), "n_changed": n_changed,
            "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
            "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
        })
        if len(rows) % 400 == 0:
            print(f"    iJO canon progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    return rows


def pfba_sweep_iml(model, b_wt, v_wt, bio_id, part_csv=None):
    """E16-convention canonical sweep (from the iML nitrogen control).
    Per-400-gene checkpointed (part_csv) so a chunk timeout resumes
    instead of restarting; the WT pFBA reference is deterministic, so
    rows computed in earlier chunks remain valid."""
    rows, done_ids = [], set()
    if part_csv and os.path.exists(part_csv):
        prev = pd.read_csv(part_csv)
        rows = prev.to_dict("records")
        done_ids = set(prev["gene_id"])
        print(f"    resuming iML sweep from {len(rows)} genes", flush=True)
    t0 = time.time()
    for g in model.genes:
        g_id = g.id
        if g_id in done_ids:
            continue
        try:
            with model:
                for r in model.reactions:
                    if g_id in r.gene_reaction_rule:
                        r.lower_bound = 0
                        r.upper_bound = 0
                try:
                    sol = pfba(model)
                    b_ko = float(sol.fluxes[bio_id])
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
            if part_csv:
                pd.DataFrame(rows).to_csv(part_csv, index=False)
            print(f"    iML canon progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    if part_csv and rows:
        pd.DataFrame(rows).to_csv(part_csv, index=False)
    return [r for r in rows if r["y_essential"] >= 0]


# =====================================================================
# PART 1: iJO1366 arg_-10 canonical sweep
# =====================================================================
IJO_CSV = os.path.join(OUT_DIR, f"keio_nitrogen_pfba_control_{KEY}.csv")
if KEY in ctrl["levels"] and os.path.exists(IJO_CSV):
    print(f"iJO {KEY}: already done -- skipping", flush=True)
else:
    print(f"\n----- iJO1366 canonical, {KEY} -----", flush=True)
    ijo = load_json_model(os.path.join(REPO,
                                       "data/bigg_models/iJO1366.json"))
    BIO_IJO = [r.id for r in ijo.reactions
               if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
    lv = next(l for l in IJO_LEVELS if l["key"] == KEY)
    set_ijo_medium(ijo, lv)
    raw = ijo.optimize()
    par_wt = pfba(ijo)
    obj_diff = abs(float(raw.objective_value)
                   - float(par_wt.fluxes[BIO_IJO]))
    assert obj_diff < 1e-6, f"objective not preserved: {obj_diff}"
    b_wt = float(par_wt.fluxes[BIO_IJO])
    print(f"  WT plain {float(raw.objective_value):.6f} / canonical "
          f"{b_wt:.6f} (preserved to {obj_diff:.1e})", flush=True)
    t0 = time.time()
    rows = pfba_sweep_ijo(ijo, b_wt, par_wt.fluxes.to_dict(), BIO_IJO)
    df = pd.DataFrame(rows)
    print(f"  sweep done ({time.time()-t0:.0f}s), {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    base_kV = pd.read_csv(os.path.join(
        OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
    mg = df[["gene_id", "kV"]].merge(base_kV, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
    plain_sweep = pd.read_csv(os.path.join(
        OUT_DIR, "keio_nitrogen_source_e12_sweep.csv"))
    pl = plain_sweep[plain_sweep["level"] == KEY]
    assert len(pl) > 0, "plain arg_-10 sweep rows not found (iJO)"
    mgl = pl[["gene_id", "y_essential"]].merge(
        df[["gene_id", "y_essential"]], on="gene_id",
        suffixes=("_fba", "_canon"))
    kap = float(cohen_kappa_score(mgl.y_essential_fba,
                                  mgl.y_essential_canon))
    pl_res = json.load(open(os.path.join(
        OUT_DIR, "keio_nitrogen_source_e12_results.json")))
    pl_cal = pl_res["levels"][KEY]["transitive_calibration"]
    ctrl["levels"][KEY] = {
        "wild_type_biomass": b_wt,
        "n_essential": int(df.y_essential.sum()),
        "n_genes": int(len(df)),
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kap,
        "objective_preservation_abs_diff": float(f"{obj_diff:.3g}"),
        "plain_reference_r": pl_cal["pearson_r_log_kV_delta_b"],
        "plain_reference_auc": pl_cal["held_out"]["roc_auc"],
    }
    df.to_csv(IJO_CSV, index=False)
    with open(CTRL_JSON, "w") as f:
        json.dump(ctrl, f, indent=2)
    print(f"  CANON: r = {cal['pearson_r_log_kV_delta_b']:+.4f} "
          f"(plain {pl_cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
          f"{cal['held_out']['roc_auc']:.4f}; MCC "
          f"{cal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; label "
          f"kappa {kap:.4f}", flush=True)

# =====================================================================
# PART 2: iML1515 arg_-10 canonical sweep
# =====================================================================
IML_CSV = os.path.join(OUT_DIR, f"keio_nitrogen_pfba_control_iml_{KEY}.csv")
if KEY in ctrl["iml_levels"] and os.path.exists(IML_CSV):
    print(f"iML {KEY}: already done -- skipping", flush=True)
else:
    print(f"\n----- iML1515 canonical, {KEY} -----", flush=True)
    iml = load_json_model(os.path.join(REPO,
                                       "data/bigg_models/iML1515.json"))
    BIO_IML = None
    for r in iml.reactions:
        if r.objective_coefficient != 0 and "iomass" in r.id:
            BIO_IML = r.id
            break
    assert BIO_IML
    lv = next(l for l in IML_LEVELS if l["key"] == KEY)
    set_iml_medium(iml, lv)
    raw = iml.optimize()
    par_wt = pfba(iml)
    obj_diff = abs(float(raw.objective_value)
                   - float(par_wt.fluxes[BIO_IML]))
    assert obj_diff < 1e-6, f"objective not preserved: {obj_diff}"
    b_wt = float(par_wt.fluxes[BIO_IML])
    print(f"  WT plain {float(raw.objective_value):.6f} / canonical "
          f"{b_wt:.6f} (preserved to {obj_diff:.1e})", flush=True)
    t0 = time.time()
    rows = pfba_sweep_iml(iml, b_wt, par_wt.fluxes, BIO_IML,
                          part_csv=os.path.join(
                              OUT_DIR, "keio_arg_pfba_iml_partial.csv"))
    df = pd.DataFrame(rows)
    print(f"  sweep done ({time.time()-t0:.0f}s), {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    base_kV = pd.read_csv(os.path.join(
        OUT_DIR, "keio_o2_pfba_control_iml_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
    mg = df[["gene_id", "kV"]].merge(base_kV, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
    plain_sweep = pd.read_csv(os.path.join(
        OUT_DIR, "keio_nitrogen_source_e16_sweep.csv"))
    pl = plain_sweep[plain_sweep["level"] == KEY]
    assert len(pl) > 0, "plain arg_-10 sweep rows not found (iML)"
    mgl = pl[["gene_id", "y_essential"]].merge(
        df[["gene_id", "y_essential"]], on="gene_id",
        suffixes=("_fba", "_canon"))
    kap = float(cohen_kappa_score(mgl.y_essential_fba,
                                  mgl.y_essential_canon))
    pl_res = json.load(open(os.path.join(
        OUT_DIR, "keio_nitrogen_source_e16_results.json")))
    pl_cal = pl_res["levels"][KEY]["transitive_calibration"]
    ctrl["iml_levels"][KEY] = {
        "wild_type_biomass": b_wt,
        "n_essential": int(df.y_essential.sum()),
        "n_genes": int(len(df)),
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kap,
        "objective_preservation_abs_diff": float(f"{obj_diff:.3g}"),
        "plain_reference_r": pl_cal["pearson_r_log_kV_delta_b"],
        "plain_reference_auc": pl_cal["held_out"]["roc_auc"],
    }
    df.to_csv(IML_CSV, index=False)
    try:
        os.remove(os.path.join(OUT_DIR, "keio_arg_pfba_iml_partial.csv"))
    except Exception:
        pass
    with open(CTRL_JSON, "w") as f:
        json.dump(ctrl, f, indent=2)
    print(f"  CANON: r = {cal['pearson_r_log_kV_delta_b']:+.4f} "
          f"(plain {pl_cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
          f"{cal['held_out']['roc_auc']:.4f}; MCC "
          f"{cal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; label "
          f"kappa {kap:.4f}", flush=True)

json.dump(ctrl, open(CTRL_JSON, "w"), indent=2)
print("\nARGININE CANONICAL CONTROL DONE.")
