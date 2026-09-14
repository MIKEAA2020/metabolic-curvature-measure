#!/usr/bin/env python3
"""
OXYGEN-AXIS CANONICAL-SELECTION CONTROL (homogenization round).

Purpose.  The nitrogen axis established that the plain-FBA curvature
statistic kappa^flux_V is conditioned on the LP vertex: wherever the
optimum is non-unique in the carbon sector the solver's arbitrary
vertex choice scrambles the association, and canonical (parsimonious
FBA) vertex selection restores it (r +0.940/+0.915/+0.872 on the
N-limited levels; the baseline sharpens +0.603 -> +0.945).  The
oxygen axis was reported under plain FBA only (r +0.775/+0.607/
+0.519 on iJO1366; +0.559 on iML1515), so the three axes' reported
statistics are not yet homogeneous.  This script re-runs the oxygen
levels under the SAME canonical-selection protocol, making the
reported statistic identical in construction across all axes, and
adds the iML1515 baseline canonical sweep (the iML counterpart of
the baseline-sharpening control).

Levels.
  iJO1366:  EX_o2_e in {-10, -5, -2.5}.
    (0 = anaerobic skipped: the iJO1366 wild-type optimum is exactly
     zero -- OPHHX/PDX5POi lack anaerobic alternatives -- so both the
     5%-relative threshold and parsimonious selection degenerate;
     already disclosed as a model-level degeneracy, not a label
     claim.)
  iML1515:  EX_o2_e in {-20 (baseline control), -5, 0.0}.
    The 0.0 level is the regime-switch endpoint: it tests whether
    the anaerobic association collapse (r +0.260) is vertex-
    conditioned or a property of the regime.

Conventions (identical to nitrogen_degeneracy_diagnostic.py PART B
and nitrogen_pfba_control_remerge.py):
  - WT and every knockout solved by pfba(); the biomass rate is read
    from the solution vector at the biomass reaction (pfba's
    objective_value is the minimized L1 total flux, NOT growth);
  - objective preservation verified per level: plain-FBA optimum ==
    pFBA biomass flux, |diff| < 1e-6 (pFBA at fraction_of_optimum
    = 1.0 preserves the objective exactly);
  - labels y = 1{b_ko < 0.05 b_wt} unchanged by construction, and
    verified against the deposited plain sweeps (Cohen kappa);
  - E12/E15 statistics with the deposited seeds (42 / 20260830).

PART 0 of this script recomputes the plain-FBA reference statistics
directly from the deposited sweep CSVs (no LP cost), including the
on-iML transitive calibration of the glucose-only baseline (not part
of the original E16 artifact, which recorded the direct arm only).

Artifacts (download/):
  keio_o2_pfba_control.json
  keio_o2_pfba_control_ijo_<o2>.csv      (o2 = 10 / 5 / 2.5)
  keio_o2_pfba_control_iml_baseline.csv
  keio_o2_pfba_control_iml_<o2>.csv      (o2 = 5 / 0)
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

# NOTE: the analysis blocks (keio_tables, transitive_calibration,
# direct_arm) are imported from the nitrogen probe -- they are the
# E12/E15 conventions with identical seeds (42 / 20260830), verbatim
# the same code the oxygen probe uses.  The O2 probe module itself is
# NOT import-safe (its iML arm executes at import time without an
# artifact guard), so the two medium setters are redefined here from
# the O2 probe's design: glucose-only corrected medium (EX_tre_e
# closed) with EX_o2_e at the probe level.
from nitrogen_source_keio_probe import (
    keio_tables, transitive_calibration, direct_arm)

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def set_ijo_medium(model, o2_lb):
    """Glucose-only corrected medium with EX_o2_e at the probe level
    (the o2_limited_keio_probe convention: trehalose stays closed)."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = o2_lb
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0


def set_iml_medium(model, o2_lb):
    """iML1515 glucose-only medium with EX_o2_e/EX_o2s_e at the level."""
    for r in model.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    for o2_id in ['EX_o2_e', 'EX_o2s_e']:
        try:
            model.reactions.get_by_id(o2_id).lower_bound = o2_lb
            break
        except Exception:
            continue
    for ex_id in IML_MINERALS:
        try:
            model.reactions.get_by_id(ex_id).lower_bound = -10
        except Exception:
            pass

IJO_O2_LEVELS = [-10.0, -5.0, -2.5]
IML_O2_LEVELS = [-5.0, 0.0]
IML_O2_BASELINE = -20.0
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]

CTRL_JSON = os.path.join(OUT_DIR, "keio_o2_pfba_control.json")

# ---------------------------------------------------------------------
# PART 0: plain-FBA reference statistics from the deposited sweeps
# ---------------------------------------------------------------------
print("=" * 78)
print("PART 0: plain-FBA reference statistics (deposited sweeps, no LP)")
print("=" * 78, flush=True)

plain = {}

# iJO baseline (glucose-only medium, O2 -20)
dfb = pd.read_csv(os.path.join(OUT_DIR, "keio_glucose_only_e12.csv"))
plain["ijo_baseline"] = transitive_calibration(dfb)
print(f"iJO baseline (O2 -20): plain r = "
      f"{plain['ijo_baseline']['pearson_r_log_kV_delta_b']:+.4f}, "
      f"AUC {plain['ijo_baseline']['held_out']['roc_auc']:.4f}",
      flush=True)

# iJO O2 levels
dfo = pd.read_csv(os.path.join(OUT_DIR, "keio_o2_limited_e12_sweep.csv"))
for o2 in IJO_O2_LEVELS:
    d = dfo[dfo["o2_bound"] == o2]
    key = f"ijo_o2_{abs(o2):g}"
    plain[key] = transitive_calibration(d)
    print(f"iJO O2 {o2}: plain r = "
          f"{plain[key]['pearson_r_log_kV_delta_b']:+.4f}, "
          f"AUC {plain[key]['held_out']['roc_auc']:.4f}", flush=True)

# iML baseline + O2 levels (on-iML transitive calibration)
dfm = pd.read_csv(os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv"))
plain["iml_baseline"] = transitive_calibration(dfm)
print(f"iML baseline (O2 -20): plain r = "
      f"{plain['iml_baseline']['pearson_r_log_kV_delta_b']:+.4f}, "
      f"AUC {plain['iml_baseline']['held_out']['roc_auc']:.4f}", flush=True)
dfmo = pd.read_csv(os.path.join(OUT_DIR, "keio_o2_limited_e16_sweep.csv"))
for o2 in IML_O2_LEVELS:
    d = dfmo[dfmo["o2_bound"] == o2]
    key = f"iml_o2_{abs(o2):g}"
    plain[key] = transitive_calibration(d)
    print(f"iML O2 {o2}: plain r = "
          f"{plain[key]['pearson_r_log_kV_delta_b']:+.4f}, "
          f"AUC {plain[key]['held_out']['roc_auc']:.4f}", flush=True)

# ---------------------------------------------------------------------
# PART 1: canonical (pFBA) sweeps
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
print("PART 1: canonical (pFBA) vertex-selection sweeps")
print("=" * 78, flush=True)

keio_tab, st6_tab = keio_tables()
control = {"plain_fba_reference": plain,
           "ijo_levels": {}, "iml_levels": {},
           "method_note": (
               "Canonical kV values are pFBA (parsimonious) vertices "
               "for the wild type and every knockout; biomass rates "
               "are read from the solution vector at the biomass "
               "reaction (cobra's pfba().objective_value returns the "
               "minimized L1 total flux, not the growth rate). "
               "Objective preservation verified per level against "
               "the plain-FBA optimum (fraction_of_optimum = 1.0). "
               "Labels are unchanged by construction and verified "
               "against the deposited plain sweeps (Cohen kappa)."),
           "skipped": {
               "ijo_o2_0": ("iJO1366 anaerobic endpoint skipped: WT "
                            "optimum exactly zero (OPHHX/PDX5POi lack "
                            "anaerobic alternatives), so both the "
                            "5%-relative threshold and parsimonious "
                            "selection degenerate; disclosed in "
                            "prop:keio-o2-limited.")}}

if os.path.exists(CTRL_JSON):
    try:
        old = json.load(open(CTRL_JSON))
        if old.get("plain_fba_reference", {}).get("ijo_baseline", {})\
                .get("n_genes") == plain["ijo_baseline"]["n_genes"]:
            control.update({k: v for k, v in old.items()
                            if k in ("ijo_levels", "iml_levels")})
            print(f"resuming: {list(control['ijo_levels'])} iJO, "
                  f"{list(control['iml_levels'])} iML levels done",
                  flush=True)
    except Exception:
        pass


def degeneracy_signature(model, bio_id):
    raw = model.optimize()
    par = pfba(model)
    fr = fva(model, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
    widths = {}
    for rid in FVA_TARGETS:
        try:
            lo, hi = float(fr.loc[rid, "minimum"]), float(fr.loc[rid, "maximum"])
            widths[rid] = round(hi - lo, 3)
        except Exception:
            widths[rid] = None
    return {
        "fba_optimum": round(float(raw.objective_value), 6),
        "pfba_biomass_flux": round(float(par.fluxes[bio_id]), 6),
        "objective_abs_diff": round(abs(float(raw.objective_value)
                                        - float(par.fluxes[bio_id])), 9),
        "raw_glc_uptake": round(float(-raw.fluxes.EX_glc__D_e), 3),
        "pfba_glc_uptake": round(float(-par.fluxes.EX_glc__D_e), 3),
        "fva_widths": widths,
    }


def pfba_sweep_ijo(model, b_wt, flux_wt, bio_id):
    rows = []
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
    return rows


def pfba_sweep_iml(model, b_wt, v_wt_series, bio_id):
    """iML arm: KO by gene_reaction_rule membership (the deposited
    plain-arm convention; all 1516 gene ids are fixed-width b-numbers,
    so the membership test cannot over-match)."""
    rows = []
    v_wt = v_wt_series
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
            rows.append({"gene_id": g_id, "n_gpr_rxns": 0,
                         "n_changed": 0, "b_wt": b_wt, "b_ko": float("nan"),
                         "delta_b": float("nan"), "y_essential": -1,
                         "kV": 0.0})
        if len(rows) % 400 == 0:
            print(f"    progress {len(rows)}/{len(model.genes)} "
                  f"({time.time()-t0:.0f}s)", flush=True)
    return [r for r in rows if r["y_essential"] >= 0]


def finalize_level(df, key, cal, da, rho, kappa_lab, sig, plain_cal):
    entry = {
        "wild_type_biomass": float(df.b_wt.iloc[0]),
        "n_essential": int(df.y_essential.sum()),
        "n_genes": int(len(df)),
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kappa_lab,
        "objective_preservation": sig,
        "plain_reference_r": plain_cal["pearson_r_log_kV_delta_b"],
        "plain_reference_auc": plain_cal["held_out"]["roc_auc"],
    }
    print(f"  canonical r = {cal['pearson_r_log_kV_delta_b']:+.4f} "
          f"(plain {plain_cal['pearson_r_log_kV_delta_b']:+.4f}); "
          f"AUC {cal['held_out']['roc_auc']:.4f} "
          f"(plain {plain_cal['held_out']['roc_auc']:.4f}); "
          f"MCC {cal['held_out']['mcc']:.4f}; direct r "
          f"{da['pearson_r']:+.4f}, AUC {da['roc_auc']:.4f}; rank corr "
          f"vs baseline {rho:+.4f}; label kappa {kappa_lab:.4f}; "
          f"PGI width {sig['fva_widths'].get('PGI')}", flush=True)
    return entry


# ---- iJO1366 arm ----
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO_IJO = [r.id for r in ijo.reactions
           if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
base_kV_ijo = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
dfo_indexed = dfo.set_index("o2_bound")

for o2 in IJO_O2_LEVELS:
    key = f"ijo_o2_{abs(o2):g}"
    if key in control["ijo_levels"] and os.path.exists(os.path.join(
            OUT_DIR, f"keio_o2_pfba_control_{key}.csv")):
        print(f"{key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iJO1366 canonical, EX_o2_e = {o2} -----", flush=True)
    set_ijo_medium(ijo, o2)
    sig = degeneracy_signature(ijo, BIO_IJO)
    assert sig["objective_abs_diff"] < 1e-6, sig
    par_wt = pfba(ijo)
    b_wt = float(par_wt.fluxes[BIO_IJO])
    flux_wt = par_wt.fluxes.to_dict()
    t0 = time.time()
    rows = pfba_sweep_ijo(ijo, b_wt, flux_wt, BIO_IJO)
    df = pd.DataFrame(rows)
    print(f"  sweep done ({time.time()-t0:.0f}s), {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    mg = df[["gene_id", "kV"]].merge(base_kV_ijo, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
    pl = dfo_indexed.loc[o2][["gene_id", "y_essential"]]
    mgl = pl.merge(df[["gene_id", "y_essential"]], on="gene_id",
                   suffixes=("_fba", "_canon"))
    kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                        mgl.y_essential_canon))
    control["ijo_levels"][key] = finalize_level(
        df, key, cal, da, rho, kappa_lab, sig, plain[key])
    df.to_csv(os.path.join(OUT_DIR, f"keio_o2_pfba_control_{key}.csv"),
              index=False)
    with open(CTRL_JSON, "w") as f:
        json.dump(control, f, indent=2)

# ---- iML1515 arm (baseline + levels) ----
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
BIO_IML = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO_IML = r.id
        break
assert BIO_IML, "iML biomass reaction not found"
dfmo_indexed = dfmo.set_index("o2_bound")

# The iML baseline canonical kV reference (already swept and deposited
# by the baseline level above, or by a previous resumable run).
_base_csv = os.path.join(OUT_DIR, "keio_o2_pfba_control_iml_baseline.csv")
assert os.path.exists(_base_csv), "iML baseline canonical CSV missing"
base_kV_iml = pd.read_csv(_base_csv)[["gene_id", "kV"]]

for o2 in [IML_O2_BASELINE] + IML_O2_LEVELS:
    if o2 == IML_O2_BASELINE:
        key = "iml_baseline"
        plain_cal = plain["iml_baseline"]
        plain_labels = dfm[["gene_id", "y_essential"]]
    else:
        key = f"iml_o2_{abs(o2):g}"
        plain_cal = plain[key]
        plain_labels = dfmo_indexed.loc[o2][["gene_id", "y_essential"]]
    if key in control["iml_levels"] and os.path.exists(os.path.join(
            OUT_DIR, f"keio_o2_pfba_control_{key}.csv")):
        print(f"{key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iML1515 canonical, EX_o2_e = {o2} -----", flush=True)
    set_iml_medium(iml, o2)
    sig = degeneracy_signature(iml, BIO_IML)
    assert sig["objective_abs_diff"] < 1e-6, sig
    par_wt = pfba(iml)
    b_wt = float(par_wt.fluxes[BIO_IML])
    t0 = time.time()
    rows = pfba_sweep_iml(iml, b_wt, par_wt.fluxes, BIO_IML)
    df = pd.DataFrame(rows)
    print(f"  sweep done ({time.time()-t0:.0f}s), {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    if key == "iml_baseline":
        rho = float("nan")
        base_kV_iml = df[["gene_id", "kV"]]
    else:
        try:
            mg = df[["gene_id", "kV"]].merge(base_kV_iml, on="gene_id",
                                             suffixes=("", "_base"))
            rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
        except Exception:
            rho = float("nan")
    mgl = plain_labels.merge(df[["gene_id", "y_essential"]], on="gene_id",
                             suffixes=("_fba", "_canon"))
    kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                        mgl.y_essential_canon))
    df.to_csv(os.path.join(OUT_DIR, f"keio_o2_pfba_control_{key}.csv"),
              index=False)
    control["iml_levels"][key] = finalize_level(
        df, key, cal, da, rho, kappa_lab, sig, plain_cal)
    df.to_csv(os.path.join(OUT_DIR, f"keio_o2_pfba_control_{key}.csv"),
              index=False)
    with open(CTRL_JSON, "w") as f:
        json.dump(control, f, indent=2)

with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)
print("\nO2 CANONICAL CONTROL DONE.")
