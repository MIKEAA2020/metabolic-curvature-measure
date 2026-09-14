#!/usr/bin/env python3
"""
DEGENERACY DIAGNOSTIC + PARSIMONIOUS CONTROL for the nitrogen-axis
probe.

Observation to diagnose (keio_nitrogen_source_*): under ammonium
limitation the LABELS stay perfectly invariant (289/1367, kappa
1.000) while the curvature-phenotype association collapses
(held-out AUC 0.98 -> 0.71, MCC 0.88 -> 0.01) -- non-essential
genes' median kV explodes 37x (50 -> 1846) and the kV ranking
decorrelates from the baseline ranking (Spearman ~ -0.04).

Hypothesis: under nitrogen limitation carbon is in surplus, so the
FBA optimum is NON-UNIQUE in the carbon sector -- how much of the
surplus glucose is taken up and secreted as overflow is optimum-
equivalent, and the LP solver's vertex choice is arbitrary.  The
kappa^flux_V statistic aggregates absolute squared flux changes, so
vertex noise inflates it for unrelated knockouts and scrambles the
ranking.  Under the baseline (carbon-limited) and oxygen-limited
optima the carbon sector is pinned (uptake at the bound, redox
balance fixes the overflow split), the vertex is essentially unique,
and the statistic is well posed.

This script establishes the mechanism and the control:

  PART A (mechanism, WT level):
    - raw-vertex vs parsimonious (pFBA) vertex at four conditions
      (baseline nh4-unlimited; O2 -10 with nh4 unlimited; nh4 -10;
      glu -10): glucose uptake, overflow byproducts, L1 total flux;
    - flux variability analysis AT the optimum (fraction = 1.0) on
      the carbon/energy sector: the baseline and O2 -10 optima have
      (near-)point ranges; the N-limited optima have wide ranges.

  PART B (control, full sweeps):
    - recompute the gene sweep with BOTH the wild type and every
      knockout solved by parsimonious FBA (a canonical, deterministic
      vertex selection that minimizes total flux at the optimal
      objective -- labels are unchanged by construction, only the
      kV values are canonically selected);
    - levels: the baseline (control-of-the-control: the association
      must be unchanged where the FBA optimum is already unique) and
      every N-axis level whose plain-FBA held-out AUC < 0.90;
    - statistics: transitive calibration + direct arm (same
      conventions/seeds) + rank correlation of canonical kV against
      the baseline canonical kV; label agreement vs the plain-FBA
      sweep (kappa, expected 1.000).

Artifacts (download/):
  keio_nitrogen_degeneracy_diagnostic.json  (PART A)
  keio_nitrogen_pfba_control.json           (PART B)
  keio_nitrogen_pfba_control_<level>.csv    (PART B per level)

Implementation note: the delivered PART B artifacts were produced by
re-merging the canonical (pFBA) kV values with the plain-FBA biomass
values -- mathematically identical to re-running, because pFBA at
fraction_of_optimum = 1.0 preserves the objective value exactly
(verified: pFBA biomass flux 0.982372 = plain-FBA optimum 0.982372
at the baseline medium).  pfba().objective_value itself returns the
minimized L1 total flux and must NOT be used as the growth rate.
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")
MOESM9 = os.path.join(REPO, "raw tomoya baba supp",
                      "44320_2006_BFMSB4100050_MOESM9_ESM.xls")
MOESM8 = os.path.join(REPO, "raw tomoya baba supp",
                      "44320_2006_BFMSB4100050_MOESM8_ESM.xls")

from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

# reuse the probe's medium/level machinery and analysis blocks
from nitrogen_source_keio_probe import (
    set_ijo_medium, IJO_LEVELS, keio_tables, transitive_calibration,
    direct_arm, BYPRODUCTS)

IJO_MINERALS = ["EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]


def set_ijo_o2_medium(model, o2_lb):
    """The O2-probe medium (nh4 unlimited) for the contrast arm."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = o2_lb
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("EX_nh4_e").lower_bound = -1000.0


CONDITIONS = [
    {"key": "baseline", "set": lambda m: set_ijo_medium(
        m, {"nh4_lb": -1000.0, "n_source": None})},
    {"key": "o2_-10", "set": lambda m: set_ijo_o2_medium(m, -10.0)},
    {"key": "nh4_-10", "set": lambda m: set_ijo_medium(m, IJO_LEVELS[0])},
    {"key": "nh4_-2.5", "set": lambda m: set_ijo_medium(m, IJO_LEVELS[2])},
    {"key": "glu_-10", "set": lambda m: set_ijo_medium(m, IJO_LEVELS[3])},
]
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]
L1 = lambda sol: float(np.abs(sol.fluxes.values).sum())

# =====================================================================
# PART A: WT-level degeneracy evidence
# =====================================================================
print("=" * 78)
print("PART A: WT vertex + at-optimum FVA (degeneracy evidence)")
print("=" * 78, flush=True)
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO_ID = [r.id for r in ijo.reactions
          if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
diagA = {}
for cond in CONDITIONS:
    cond["set"](ijo)
    raw = ijo.optimize()
    par = pfba(ijo)
    fr = fva(ijo, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
    widths = {}
    for rid in FVA_TARGETS:
        lo, hi = float(fr.loc[rid, "minimum"]), float(fr.loc[rid, "maximum"])
        widths[rid] = {"min": round(lo, 4), "max": round(hi, 4),
                       "width": round(hi - lo, 4)}
    tot_width = float(sum(w["width"] for w in widths.values()))
    byp_raw = {r: round(float(raw.fluxes.get(r, 0.0)), 3) for r in BYPRODUCTS
               if abs(raw.fluxes.get(r, 0.0)) > 1e-6}
    byp_par = {r: round(float(par.fluxes.get(r, 0.0)), 3) for r in BYPRODUCTS
               if abs(par.fluxes.get(r, 0.0)) > 1e-6}
    diagA[cond["key"]] = {
        "wild_type_biomass": round(float(raw.objective_value), 6),
        "raw_vertex": {"glc_uptake": round(
                           float(-raw.fluxes.EX_glc__D_e), 3),
                       "o2_uptake": round(float(-raw.fluxes.EX_o2_e), 3),
                       "byproducts": byp_raw, "L1_total_flux": L1(raw)},
        "pfba_vertex": {"glc_uptake": round(
                            float(-par.fluxes.EX_glc__D_e), 3),
                        "o2_uptake": round(float(-par.fluxes.EX_o2_e), 3),
                        "byproducts": byp_par, "L1_total_flux": L1(par)},
        "fva_at_optimum": widths,
        "fva_total_width": round(tot_width, 3),
    }
    print(f"\n{cond['key']:>9}: WT {raw.objective_value:.4f} | raw glc "
          f"{-raw.fluxes.EX_glc__D_e:6.3f}, L1 {L1(raw):7.1f}, byp {byp_raw}"
          f" | pFBA glc {-par.fluxes.EX_glc__D_e:6.3f}, L1 {L1(par):7.1f}, "
          f"byp {byp_par}")
    print(f"{'':>9}  FVA-at-optimum total width {tot_width:8.3f}: " +
          "; ".join(f"{r} w={widths[r]['width']:.2f}" for r in FVA_TARGETS
                    if widths[r]["width"] > 1e-6), flush=True)
with open(os.path.join(OUT_DIR, "keio_nitrogen_degeneracy_diagnostic.json"),
          "w") as f:
    json.dump(diagA, f, indent=2)
print("\nPART A written.")

# =====================================================================
# PART B: parsimonious control sweeps
# =====================================================================
print("=" * 78)
print("PART B: pFBA canonical-vertex control sweeps")
print("=" * 78, flush=True)
probe_res = json.load(open(os.path.join(
    OUT_DIR, "keio_nitrogen_source_e12_results.json")))
plain_auc = {k: probe_res["levels"][k]["transitive_calibration"]
             ["held_out"]["roc_auc"] for k in probe_res["levels"]}
_scrambled = [k for k in ["nh4_-10", "glu_-10", "nh4_-2.5", "nh4_-5"]
              if k in plain_auc and plain_auc[k] < 0.90]
control_levels = ["baseline"] + _scrambled
print(f"plain-FBA held-out AUC per level: "
      f"{ {k: round(v, 4) for k, v in plain_auc.items()} }")
print(f"control levels (baseline + scrambled): {control_levels}", flush=True)

keio_tab, st6_tab = keio_tables()
base_csv = os.path.join(OUT_DIR, "keio_glucose_only_e12.csv")


def pfba_sweep(model, b_wt, flux_wt):
    """E12-convention sweep with pFBA-canonical vertices (labels are
    identical by construction; only kV is canonically selected)."""
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
                # pfba().objective_value is the minimized L1 total flux;
                # the biomass rate is its value at the pFBA solution and
                # equals the plain-FBA optimum exactly (fraction=1.0).
                b_ko = float(sol.fluxes[BIO_ID])
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


control = {"levels": {}, "plain_auc": plain_auc,
           "control_levels": control_levels}
CTRL_JSON = os.path.join(OUT_DIR, "keio_nitrogen_pfba_control.json")
if os.path.exists(CTRL_JSON):
    try:
        control = json.load(open(CTRL_JSON))
        control["plain_auc"] = plain_auc
        control["control_levels"] = control_levels
        print("resuming control from partial artifacts", flush=True)
    except Exception:
        control = {"levels": {}, "plain_auc": plain_auc,
                   "control_levels": control_levels}
base_df_pfba = None
if "baseline" in control["levels"] and os.path.exists(os.path.join(
        OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv")):
    base_df_pfba = pd.read_csv(os.path.join(
        OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[["gene_id", "kV"]]\
        .rename(columns={"kV": "kV_base"})
for key in control_levels:
    if key in control["levels"]:
        continue
    print(f"\n----- pFBA control, {key} -----", flush=True)
    if key == "baseline":
        set_ijo_medium(ijo, {"nh4_lb": -1000.0, "n_source": None})
    else:
        set_ijo_medium(ijo, next(l for l in IJO_LEVELS if l["key"] == key))
    t0 = time.time()
    par_wt = pfba(ijo)
    b_wt = float(par_wt.fluxes[BIO_ID])
    flux_wt = par_wt.fluxes.to_dict()
    rows = pfba_sweep(ijo, b_wt, flux_wt)
    df = pd.DataFrame(rows)
    print(f"  sweep done ({time.time()-t0:.0f}s), {len(df)} genes, "
          f"{int(df.y_essential.sum())} essential", flush=True)
    cal = transitive_calibration(df)
    da, _ = direct_arm(df, keio_tab, st6_tab)
    # rank correlation of canonical kV vs the baseline canonical kV
    if base_df_pfba is None:
        base_df_pfba = df[["gene_id", "kV"]].rename(
            columns={"kV": "kV_base"})
    mg = df[["gene_id", "kV"]].merge(base_df_pfba, on="gene_id")
    rho = float(spearmanr(mg.kV, mg.kV_base).statistic) if key != "baseline" \
        else float("nan")
    # label agreement with the plain-FBA sweep of the same level
    if key == "baseline":
        plain_df = pd.read_csv(base_csv)
    else:
        allsw = pd.read_csv(os.path.join(
            OUT_DIR, "keio_nitrogen_source_e12_sweep.csv"))
        plain_df = allsw[allsw["level"] == key]
    mgl = plain_df[["gene_id", "y_essential"]].merge(
        df[["gene_id", "y_essential"]], on="gene_id",
        suffixes=("_fba", "_pfba"))
    kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                        mgl.y_essential_pfba))
    control["levels"][key] = {
        "wild_type_biomass": b_wt,
        "transitive_calibration": cal, "direct_arm": da,
        "kV_rank_corr_vs_baseline_canonical": rho,
        "label_agreement_fba_vs_pfba_kappa": kappa_lab,
        "n_essential": int(df.y_essential.sum()),
    }
    df.to_csv(os.path.join(OUT_DIR, f"keio_nitrogen_pfba_control_{key}.csv"),
              index=False)
    with open(CTRL_JSON, "w") as f:
        json.dump(control, f, indent=2)
    print(f"  calibration r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
          f"held-out AUC = {cal['held_out']['roc_auc']:.4f}, MCC = "
          f"{cal['held_out']['mcc']:.4f}; direct r {da['pearson_r']:+.4f}, "
          f"AUC {da['roc_auc']:.4f}; kV rank corr vs baseline "
          f"{rho:+.4f}; label kappa (FBA vs pFBA) {kappa_lab:.4f}",
          flush=True)

with open(os.path.join(OUT_DIR, "keio_nitrogen_pfba_control.json"), "w") as f:
    json.dump(control, f, indent=2)
print("\nPART B written.")
print("DIAGNOSTIC + CONTROL DONE.")
