#!/usr/bin/env python3
"""SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS
(temperature-style, NON-MEDIUM).

Background.  Five axes are established (companion v3, props
keio-glucose-only / keio-o2-limited / keio-n-source / keio-phosphate /
keio-iron): carbon source, electron acceptor, nitrogen supply,
phosphate supply, iron supply -- all MEDIUM-side perturbations.
Genome-scale FBA has no temperature or pH state variables; the
standard constraint-based surrogate for temperature-style stress is
escalation of the non-growth-associated ATP maintenance demand
(ATPM lower bound; default 3.15 iJO1366 / 6.86 iML1515 mmol
ATP/gDW/h).  The non-medium pre-screen (nonmedium_axis_prescreen.py)
compared this encoding head-to-head with proton-leak forcing
(EX_h_e secretion floor, the pH-style surrogate) and selected ATPM:
it spans 29-90% WT reduction with 4-5 usable levels in both models,
while the proton-leak axis compresses to 2 usable levels in iJO1366
(the proton leaves partly 'for free' with organic-acid secretion)
before hard infeasibility.

The pre-screen also established the decisive structural fact: the
ATPM axis carries ZERO carbon-sector degeneracy (at-optimum FVA PGI
width 0.0 at every level, both models) -- unlike every supply axis
(widths 100-200).  The maintenance demand pins the energy sector and
makes the optimum unique.  This axis therefore doubles as a POSITIVE
CONTROL for the degeneracy diagnosis: under temperature-style stress
the plain-FBA association is predicted NOT to collapse, isolating
optimum non-uniqueness (not WT reduction per se) as the collapse
mechanism on the supply axes.

Design (homogeneous with the canonical-selection protocol).
  iJO1366:  ATPM lower bound in {40, 60, 80, 100}
            (29% / 50% / 70% / 90% WT reduction)
  iML1515:  ATPM lower bound in {60, 80, 100}
            (52% / 71% / 90% WT reduction)
  Per level, BOTH arms are computed:
    PLAIN  -- plain-FBA sweep (E12/E16 conventions, labels at 5% of
              that level's WT) -- the axis's own plain reading and
              the label-flip comparison vs the glucose-only baseline;
    CANON  -- pFBA (parsimonious) vertex selection (objective
              preservation verified; biomass read from the solution
              vector at the biomass reaction), label kappa vs the
              plain arm, kV rank correlation vs the canonical
              baselines.

Artifacts:
  download/keio_atpm_stress_e12_results.json   (iJO plain arm)
  download/keio_atpm_stress_e12_sweep.csv
  download/keio_atpm_stress_e16_results.json   (iML plain arm)
  download/keio_atpm_stress_e16_sweep.csv
  download/keio_atpm_pfba_control.json         (canonical arm)
  download/keio_atpm_pfba_control_<level>.csv  (per level)
  download/keio_atpm_stress_summary.txt
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

from nitrogen_source_keio_probe import (
    keio_tables, ko_sweep_ijo, transitive_calibration, direct_arm,
    flip_analysis)

IJO_ATPM_LEVELS = [40.0, 60.0, 80.0, 100.0]
IML_ATPM_LEVELS = [60.0, 80.0, 100.0]
BYPRODUCTS = ["EX_etoh_e", "EX_lac__D_e", "EX_for_e", "EX_succ_e",
              "EX_ac_e"]
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]
IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def key_of(lb):
    return f"atpm_{lb:g}"


def set_ijo_atpm(model, atpm_lb):
    """Glucose-only corrected medium, ATPM at the probe level."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("ATPM").lower_bound = atpm_lb
    # EX_tre_e stays CLOSED (glucose-only correction retained)


def set_iml_atpm(model, atpm_lb):
    for r in model.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    for o2_id in ['EX_o2_e', 'EX_o2s_e']:
        try:
            model.reactions.get_by_id(o2_id).lower_bound = -20.0
            break
        except Exception:
            continue
    for ex_id in IML_MINERALS:
        try:
            model.reactions.get_by_id(ex_id).lower_bound = -10
        except Exception:
            pass
    model.reactions.get_by_id("ATPM").lower_bound = atpm_lb


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
        "atpm_flux": round(float(raw.fluxes.ATPM), 4),
        "fva_widths": widths,
    }


def pfba_sweep_ijo(model, b_wt, flux_wt, bio_id, scratch=None):
    """Canonical pFBA KO sweep, resumable across process kills via a
    scratch CSV (every 100 newly processed genes)."""
    rows = []
    done = set()
    if scratch and os.path.exists(scratch):
        _part = pd.read_csv(scratch)
        rows = _part.to_dict("records")
        done = set(_part["gene_id"].tolist())
        print(f"    resuming canon sweep: {len(done)} genes already done",
              flush=True)
    t0 = time.time()
    n_new = 0
    for gene in model.genes:
        if gene.id in done:
            continue
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
                src = "pfba"
            except Exception:
                # GLPK simplex time limit (tm_lim, see solver config) or
                # numerical failure in the L1 stage.  Fall back to the
                # plain-FBA optimum vertex: same biomass optimum, so the
                # essentiality label is unchanged by construction; only
                # the kV vertex reference changes (flagged in solve_src).
                try:
                    psol = model.optimize()
                    if psol.status == "optimal":
                        b_ko = float(psol.objective_value)
                        flux_ko = psol.fluxes.to_dict()
                        src = "plain_fallback"
                    else:
                        b_ko, flux_ko, src = 0.0, {}, "infeasible"
                except Exception:
                    b_ko, flux_ko, src = 0.0, {}, "infeasible"
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
            "solve_src": src,
        })
        n_new += 1
        if n_new % 20 == 0:
            print(f"    canon progress +{n_new} new "
                  f"({len(rows)}/{len(model.genes)} total, "
                  f"{time.time()-t0:.0f}s)", flush=True)
            if scratch and rows:
                pd.DataFrame(rows).to_csv(scratch, index=False)
    if scratch and rows:
        pd.DataFrame(rows).to_csv(scratch, index=False)
    return rows


def plain_sweep_iml(model, b_wt, v_wt, scratch=None):
    """E16-convention plain sweep (the deposited O2/N iML-arm code),
    resumable across process kills via a scratch CSV (every 100 genes)."""
    rows = []
    done = set()
    if scratch and os.path.exists(scratch):
        _part = pd.read_csv(scratch)
        rows = _part.to_dict("records")
        done = set(_part["gene_id"].tolist())
        print(f"    resuming plain sweep: {len(done)} genes already done",
              flush=True)
    t0 = time.time()
    n_new = 0
    for g in model.genes:
        g_id = g.id
        if g_id in done:
            continue
        try:
            with model:
                for r in model.reactions:
                    if g_id in r.gene_reaction_rule:
                        r.lower_bound = 0
                        r.upper_bound = 0
                ko_sol = model.optimize()
                if ko_sol.status != "optimal":
                    b_ko = 0.0
                    v_ko = np.zeros_like(v_wt)
                else:
                    b_ko = float(ko_sol.objective_value)
                    v_ko = np.array([ko_sol.fluxes.get(r.id, 0.0)
                                     for r in model.reactions])
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
                         "b_wt": b_wt, "b_ko": float('nan'),
                         "delta_b": float('nan'), "y_essential": -1,
                         "kV": 0.0})
        n_new += 1
        if n_new % 20 == 0:
            print(f"    plain progress +{n_new} new "
                  f"({len(rows)}/{len(model.genes)} total, "
                  f"{time.time()-t0:.0f}s)", flush=True)
            if scratch and rows:
                pd.DataFrame(rows).to_csv(scratch, index=False)
    if scratch and rows:
        pd.DataFrame(rows).to_csv(scratch, index=False)
    return [r for r in rows if r["y_essential"] >= 0]


def pfba_sweep_iml(model, b_wt, v_wt_series, bio_id, scratch=None):
    """Canonical pFBA KO sweep, resumable across process kills: every
    20 newly processed genes the partial rows are checkpointed to the
    scratch CSV, and genes already present there are skipped."""
    rows = []
    done = set()
    if scratch and os.path.exists(scratch):
        _part = pd.read_csv(scratch)
        rows = _part.to_dict("records")
        done = set(_part["gene_id"].tolist())
        print(f"    resuming canon sweep: {len(done)} genes already done",
              flush=True)
    v_wt = v_wt_series
    t0 = time.time()
    n_new = 0
    for g in model.genes:
        g_id = g.id
        if g_id in done:
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
                    src = "pfba"
                except Exception:
                    # solver time limit / L1-stage failure: plain-FBA
                    # optimum vertex fallback (label-preserving)
                    try:
                        psol = model.optimize()
                        if psol.status == "optimal":
                            b_ko = float(psol.objective_value)
                            v_ko = psol.fluxes
                            src = "plain_fallback"
                        else:
                            b_ko, v_ko, src = 0.0, None, "infeasible"
                    except Exception:
                        b_ko, v_ko, src = 0.0, None, "infeasible"
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
                "solve_src": src,
            })
        except Exception:
            rows.append({"gene_id": g_id, "n_gpr_rxns": 0, "n_changed": 0,
                         "b_wt": b_wt, "b_ko": float('nan'),
                         "delta_b": float('nan'), "y_essential": -1,
                         "kV": 0.0})
        n_new += 1
        if n_new % 20 == 0:
            print(f"    canon progress +{n_new} new "
                  f"({len(rows)}/{len(model.genes)} total, "
                  f"{time.time()-t0:.0f}s)", flush=True)
            if scratch and rows:
                pd.DataFrame(rows).to_csv(scratch, index=False)
    if scratch and rows:
        pd.DataFrame(rows).to_csv(scratch, index=False)
    return [r for r in rows if r["y_essential"] >= 0]


# =====================================================================
# PART 1: iJO1366 ATPM gradient -- plain + canonical per level
# (resumable per level; artifacts checkpointed after each)
# =====================================================================
IJO_JSON = os.path.join(OUT_DIR, "keio_atpm_stress_e12_results.json")
IJO_CSV = os.path.join(OUT_DIR, "keio_atpm_stress_e12_sweep.csv")
CTRL_JSON = os.path.join(OUT_DIR, "keio_atpm_pfba_control.json")
keio_tab, st6_tab = keio_tables()

ijo_results = {"probe": "ATPM-escalation stress, iJO1366 gradient",
               "baseline_medium": "glucose -10, O2 -20, minerals -1000, "
                                  "EX_tre_e CLOSED (glucose-only run)",
               "levels": {}}
control = {"ijo_levels": {}, "iml_levels": {},
           "method_note": (
               "Canonical kV values are pFBA (parsimonious) vertices for "
               "the wild type and every knockout; biomass rates are read "
               "from the solution vector at the biomass reaction (cobra's "
               "pfba().objective_value returns the minimized L1 total "
               "flux, not the growth rate). Objective preservation "
               "verified per level; labels unchanged by construction and "
               "verified against the plain arm (Cohen kappa).  A GLPK "
               "simplex time limit (30 s) guards the pFBA L1 stage; "
               "timed-out or numerically failed solves fall back to the "
               "plain-FBA optimum vertex, which preserves the "
               "essentiality label by construction (per-gene solve_src "
               "column in the level CSVs).")}
if os.path.exists(IJO_JSON):
    ijo_results = json.load(open(IJO_JSON))
if os.path.exists(CTRL_JSON):
    try:
        old = json.load(open(CTRL_JSON))
        control.update({k: v for k, v in old.items()
                        if k in ("ijo_levels", "iml_levels")})
    except Exception:
        pass

ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
# GLPK native simplex time limit (tm_lim, seconds): without it a handful
# of at-optimum L1 LPs cycle indefinitely at ATPM >= 100 (identified in
# atpm_stuck_gene_diagnostic.py); timed-out solves fall back to the
# plain-FBA optimum vertex (label-preserving, see pfba_sweep_*).
ijo.solver.configuration.timeout = 30
BIO_IJO = [r.id for r in ijo.reactions
           if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
base_kV_ijo = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})

ijo_sweep_rows = []
if os.path.exists(IJO_CSV):
    _done = pd.read_csv(IJO_CSV)
    ijo_sweep_rows = [g for _, g in _done.groupby("atpm_bound")]
    have = {float(g["atpm_bound"].iloc[0]) for g in ijo_sweep_rows}
else:
    have = set()

print("=" * 78)
print("SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS (TEMPERATURE-STYLE, NON-MEDIUM) (iJO1366)")
print("  Baseline: glucose-only medium (glc -10, O2 -20, tre CLOSED)")
print(f"  Probe levels: ATPM lower bound in {IJO_ATPM_LEVELS}")
print(f"  (resuming with {sorted(have)} already swept)")
print("=" * 78, flush=True)

for atpm in IJO_ATPM_LEVELS:
    key = key_of(atpm)
    need_plain = atpm not in have or key not in ijo_results["levels"]
    need_canon = key not in control["ijo_levels"] or not os.path.exists(
        os.path.join(OUT_DIR, f"keio_atpm_pfba_control_{key}.csv"))
    if not need_plain and not need_canon:
        print(f"{key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iJO1366, ATPM >= {atpm} -----", flush=True)
    set_ijo_atpm(ijo, atpm)
    sig = degeneracy_signature(ijo, BIO_IJO)
    assert sig["objective_abs_diff"] < 1e-6, sig
    print(f"  WT {sig['fba_optimum']:.6f}; ATPM flux {sig['atpm_flux']}; "
          f"glc raw {sig['raw_glc_uptake']} / pFBA "
          f"{sig['pfba_glc_uptake']}; PGI width "
          f"{sig['fva_widths'].get('PGI')}", flush=True)

    plain_df = None
    if need_plain:
        t0 = time.time()
        wt = ijo.optimize()
        b_wt = float(wt.objective_value)
        flux_wt = wt.fluxes.to_dict()
        byp = {r: round(float(flux_wt.get(r, 0.0)), 3) for r in BYPRODUCTS
               if abs(flux_wt.get(r, 0.0)) > 1e-6}
        rows = ko_sweep_ijo(ijo, b_wt, flux_wt)
        plain_df = pd.DataFrame(rows)
        plain_df.insert(0, "atpm_bound", atpm)
        print(f"  plain sweep done ({time.time()-t0:.0f}s), "
              f"{len(plain_df)} genes", flush=True)
        _prior = [r for r in ijo_sweep_rows
                  if float(r['atpm_bound'].iloc[0]) != atpm]
        ijo_sweep_rows = [g for _, g in pd.concat(
            _prior + [plain_df]).groupby("atpm_bound")]
        pd.concat(ijo_sweep_rows).to_csv(IJO_CSV, index=False)
        cal = transitive_calibration(plain_df)
        da, _ = direct_arm(plain_df, keio_tab, st6_tab)
        fl, _ = flip_analysis(
            plain_df, os.path.join(OUT_DIR, "keio_glucose_only_e12.csv"),
            ijo, f"ATPM={atpm} vs glucose-only (default maintenance)")
        ijo_results["levels"][key] = {
            "atpm_bound": atpm, "wild_type_biomass": b_wt,
            "atpm_flux": sig["atpm_flux"], "byproducts": byp,
            "degeneracy": sig,
            "transitive_calibration": cal, "direct_arm": da,
            "flips_vs_glucose_only": fl,
        }
        with open(IJO_JSON, "w") as f:
            json.dump(ijo_results, f, indent=2)
        print(f"  PLAIN: r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"AUC = {cal['held_out']['roc_auc']:.4f}; labels "
              f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
              f"(+{fl['n_gain_essential']}/-{fl['n_loss_essential']}, "
              f"kappa {fl['cohen_kappa']:.4f}); direct "
              f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)
    else:
        _d = pd.read_csv(IJO_CSV)
        plain_df = _d[_d["atpm_bound"] == atpm]
        cal = ijo_results["levels"][key]["transitive_calibration"]

    if need_canon:
        t0 = time.time()
        par_wt = pfba(ijo)
        b_wt_c = float(par_wt.fluxes[BIO_IJO])
        _scratch = os.path.join(
            OUT_DIR, f"keio_atpm_pfba_control_{key}_partial.csv")
        rows = pfba_sweep_ijo(ijo, b_wt_c, par_wt.fluxes.to_dict(),
                              BIO_IJO, _scratch)
        cdf = pd.DataFrame(rows)
        if os.path.exists(_scratch):
            os.remove(_scratch)
        _vc = (cdf["solve_src"].value_counts().to_dict()
               if "solve_src" in cdf.columns else {})
        print(f"  canonical sweep done ({time.time()-t0:.0f}s), "
              f"{len(cdf)} genes, {int(cdf.y_essential.sum())} essential "
              f"(solve: {_vc})",
              flush=True)
        ccal = transitive_calibration(cdf)
        cda, _ = direct_arm(cdf, keio_tab, st6_tab)
        mg = cdf[["gene_id", "kV"]].merge(base_kV_ijo, on="gene_id")
        rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
        mgl = plain_df[["gene_id", "y_essential"]].merge(
            cdf[["gene_id", "y_essential"]], on="gene_id",
            suffixes=("_fba", "_canon"))
        kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                            mgl.y_essential_canon))
        control["ijo_levels"][key] = {
            "wild_type_biomass": b_wt_c,
            "n_essential": int(cdf.y_essential.sum()),
            "n_genes": int(len(cdf)),
            "transitive_calibration": ccal, "direct_arm": cda,
            "kV_rank_corr_vs_baseline_canonical": rho,
            "label_agreement_fba_vs_pfba_kappa": kappa_lab,
            "objective_preservation": sig,
            "solve_sources": {str(k): int(v) for k, v in _vc.items()},
            "plain_reference_r": cal["pearson_r_log_kV_delta_b"],
            "plain_reference_auc": cal["held_out"]["roc_auc"],
        }
        cdf.to_csv(os.path.join(
            OUT_DIR, f"keio_atpm_pfba_control_{key}.csv"), index=False)
        with open(CTRL_JSON, "w") as f:
            json.dump(control, f, indent=2)
        print(f"  CANON: r = {ccal['pearson_r_log_kV_delta_b']:+.4f} "
              f"(plain {cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
              f"{ccal['held_out']['roc_auc']:.4f}; MCC "
              f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; "
              f"label kappa {kappa_lab:.4f}", flush=True)

with open(IJO_JSON, "w") as f:
    json.dump(ijo_results, f, indent=2)
with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)

# =====================================================================
# PART 2: iML1515 cross-rebuild at ATPM 80 and 100
# =====================================================================
print("\n" + "=" * 78)
print("SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS (TEMPERATURE-STYLE, NON-MEDIUM) (iML1515)")
print("=" * 78, flush=True)
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
iml.solver.configuration.timeout = 30
BIO_IML = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO_IML = r.id
        break
assert BIO_IML, "iML biomass reaction not found"

IML_JSON = os.path.join(OUT_DIR, "keio_atpm_stress_e16_results.json")
IML_CSV = os.path.join(OUT_DIR, "keio_atpm_stress_e16_sweep.csv")
iml_results = {"probe": "ATPM-escalation stress, iML1515 cross-rebuild",
               "baseline_medium": "glucose -10, O2 -20, minerals -10, "
                                  "EX_tre_e CLOSED",
               "levels": {}}
if os.path.exists(IML_JSON):
    iml_results = json.load(open(IML_JSON))

# iML baseline canonical reference (glucose-only medium, O2 -20) --
# the O2 canonical control computes it (keio_o2_pfba_control_iml_
# baseline.csv); if absent, fall back to recomputing the rank
# correlation against the plain baseline kV (still informative).
iml_base_canon_csv = os.path.join(OUT_DIR,
                                  "keio_o2_pfba_control_iml_baseline.csv")
if os.path.exists(iml_base_canon_csv):
    base_kV_iml = pd.read_csv(iml_base_canon_csv)[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
    iml_base_source = "canonical (o2 control baseline)"
else:
    base_kV_iml = pd.read_csv(
        os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv"))[
            ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
    iml_base_source = "plain (glucose-only baseline; canonical pending)"
print(f"iML baseline kV reference: {iml_base_source}", flush=True)

iml_sweep_rows = []
if os.path.exists(IML_CSV):
    _done = pd.read_csv(IML_CSV)
    iml_sweep_rows = [g for _, g in _done.groupby("atpm_bound")]
    have_iml = {float(g["atpm_bound"].iloc[0]) for g in iml_sweep_rows}
else:
    have_iml = set()

for atpm in IML_ATPM_LEVELS:
    key = key_of(atpm)
    need_plain = atpm not in have_iml or key not in iml_results["levels"]
    need_canon = key not in control["iml_levels"] or not os.path.exists(
        os.path.join(OUT_DIR, f"keio_atpm_pfba_control_iml_{key}.csv"))
    if not need_plain and not need_canon:
        print(f"iML {key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iML1515, ATPM >= {atpm} -----", flush=True)
    set_iml_atpm(iml, atpm)
    sig = degeneracy_signature(iml, BIO_IML)
    assert sig["objective_abs_diff"] < 1e-6, sig
    print(f"  WT {sig['fba_optimum']:.6f}; ATPM flux {sig['atpm_flux']}; "
          f"glc raw {sig['raw_glc_uptake']} / pFBA "
          f"{sig['pfba_glc_uptake']}; PGI width "
          f"{sig['fva_widths'].get('PGI')}", flush=True)

    plain_df = None
    if need_plain:
        t0 = time.time()
        wt = iml.optimize()
        b_wt = float(wt.objective_value)
        v_wt = np.array([wt.fluxes.get(r.id, 0.0) for r in iml.reactions])
        _scratch_plain = os.path.join(
            OUT_DIR, f"keio_atpm_stress_e16_plain_{key}_partial.csv")
        rows = plain_sweep_iml(iml, b_wt, v_wt, _scratch_plain)
        plain_df = pd.DataFrame(rows)
        plain_df.insert(0, "atpm_bound", atpm)
        if os.path.exists(_scratch_plain):
            os.remove(_scratch_plain)
        print(f"  plain sweep done ({time.time()-t0:.0f}s), "
              f"{len(plain_df)} genes", flush=True)
        _prior = [r for r in iml_sweep_rows
                  if float(r['atpm_bound'].iloc[0]) != atpm]
        iml_sweep_rows = [g for _, g in pd.concat(
            _prior + [plain_df]).groupby("atpm_bound")]
        pd.concat(iml_sweep_rows).to_csv(IML_CSV, index=False)
        cal = transitive_calibration(plain_df)
        da, _ = direct_arm(plain_df, keio_tab, st6_tab)
        fl, _ = flip_analysis(
            plain_df, os.path.join(OUT_DIR,
                                   "keio_glucose_only_e16_sweep.csv"),
            iml, f"iML1515 ATPM={atpm} vs glucose-only (default maintenance)")
        iml_results["levels"][key] = {
            "atpm_bound": atpm, "wild_type_biomass": b_wt,
            "atpm_flux": sig["atpm_flux"],
            "degeneracy": sig,
            "transitive_calibration": cal, "direct_arm": da,
            "flips_vs_glucose_only": fl,
        }
        with open(IML_JSON, "w") as f:
            json.dump(iml_results, f, indent=2)
        print(f"  PLAIN: r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"AUC = {cal['held_out']['roc_auc']:.4f}; labels "
              f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
              f"(+{fl['n_gain_essential']}/-{fl['n_loss_essential']}, "
              f"kappa {fl['cohen_kappa']:.4f}); direct "
              f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)
    else:
        _d = pd.read_csv(IML_CSV)
        plain_df = _d[_d["atpm_bound"] == atpm]
        cal = iml_results["levels"][key]["transitive_calibration"]

    if need_canon:
        t0 = time.time()
        par_wt = pfba(iml)
        b_wt_c = float(par_wt.fluxes[BIO_IML])
        _scratch = os.path.join(
            OUT_DIR, f"keio_atpm_pfba_control_iml_{key}_partial.csv")
        rows = pfba_sweep_iml(iml, b_wt_c, par_wt.fluxes, BIO_IML,
                              _scratch)
        cdf = pd.DataFrame(rows)
        _vc = (cdf["solve_src"].value_counts().to_dict()
               if "solve_src" in cdf.columns else {})
        print(f"  canonical sweep done ({time.time()-t0:.0f}s), "
              f"{len(cdf)} genes, {int(cdf.y_essential.sum())} essential "
              f"(solve: {_vc})",
              flush=True)
        ccal = transitive_calibration(cdf)
        cda, _ = direct_arm(cdf, keio_tab, st6_tab)
        mg = cdf[["gene_id", "kV"]].merge(base_kV_iml, on="gene_id")
        rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
        mgl = plain_df[["gene_id", "y_essential"]].merge(
            cdf[["gene_id", "y_essential"]], on="gene_id",
            suffixes=("_fba", "_canon"))
        kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                            mgl.y_essential_canon))
        control["iml_levels"][key] = {
            "wild_type_biomass": b_wt_c,
            "n_essential": int(cdf.y_essential.sum()),
            "n_genes": int(len(cdf)),
            "transitive_calibration": ccal, "direct_arm": cda,
            "kV_rank_corr_vs_baseline_canonical": rho,
            "kV_rank_reference": iml_base_source,
            "label_agreement_fba_vs_pfba_kappa": kappa_lab,
            "objective_preservation": sig,
            "solve_sources": {str(k): int(v) for k, v in _vc.items()},
            "plain_reference_r": cal["pearson_r_log_kV_delta_b"],
            "plain_reference_auc": cal["held_out"]["roc_auc"],
        }
        cdf.to_csv(os.path.join(
            OUT_DIR, f"keio_atpm_pfba_control_iml_{key}.csv"), index=False)
        if os.path.exists(_scratch):
            os.remove(_scratch)
        with open(CTRL_JSON, "w") as f:
            json.dump(control, f, indent=2)
        print(f"  CANON: r = {ccal['pearson_r_log_kV_delta_b']:+.4f} "
              f"(plain {cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
              f"{ccal['held_out']['roc_auc']:.4f}; MCC "
              f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; "
              f"label kappa {kappa_lab:.4f}", flush=True)

with open(IML_JSON, "w") as f:
    json.dump(iml_results, f, indent=2)
with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)

# =====================================================================
# PART 3: summary
# =====================================================================
lines = []
lines.append("SIXTH PERTURBATION AXIS: ATPM-ESCALATION STRESS (NON-MEDIUM)")
lines.append("Non-medium (temperature-style maintenance-stress) axis of the "
             "label-invariance claim "
             "(iJO1366 + iML1515)")
lines.append("=" * 78)
lines.append("Baseline: glucose-only corrected medium (trehalose closed), "
             "default maintenance. Probe: ATPM lower bound.")
lines.append("Levels chosen by pre-screen: iJO 40/60/80/100, iML 60/80/100 "
             "(29-90% WT reduction; ATPM default 3.15 iJO / "
             "6.86 iML; zero degeneracy on this axis -- the "
             "positive-control property).")
lines.append("")
base_ijo = json.load(open(os.path.join(OUT_DIR,
                                       "keio_glucose_only_e12_results.json")))
lines.append(f"iJO1366 baseline: WT {base_ijo['wild_type_biomass']:.4f}, "
             f"{base_ijo['n_essential']}/{base_ijo['n_genes_processed']} "
             f"essential, plain r = "
             f"{base_ijo['calibration']['pearson_r_log_kV_delta_b']:+.4f}")
nctrl = json.load(open(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control.json")))
bl = nctrl["levels"]["baseline"]["transitive_calibration"]
lines.append(f"             canonical r = "
             f"{bl['pearson_r_log_kV_delta_b']:+.4f} "
             f"(AUC {bl['held_out']['roc_auc']:.4f})")
for atpm in IJO_ATPM_LEVELS:
    key = key_of(atpm)
    lv = ijo_results["levels"][key]
    cal = lv["transitive_calibration"]
    fl = lv["flips_vs_glucose_only"]
    sig = lv["degeneracy"]
    c = control["ijo_levels"][key]
    ccal = c["transitive_calibration"]
    lines.append(
        f"ATPM = {atpm:>5}: WT {lv['wild_type_biomass']:.4f} "
        f"(-{100*(1-lv['wild_type_biomass']/base_ijo['wild_type_biomass']):.0f}%); "
        f"labels {fl['n_essential_base']} -> {fl['n_essential_new']} "
        f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, kappa "
        f"{fl['cohen_kappa']:.4f}); plain r = "
        f"{cal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{cal['held_out']['roc_auc']:.4f}; canonical r = "
        f"{ccal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{ccal['held_out']['roc_auc']:.4f} / MCC "
        f"{ccal['held_out']['mcc']:.4f}; PGI FVA width "
        f"{sig['fva_widths'].get('PGI')}")
lines.append("")
for atpm in IML_ATPM_LEVELS:
    key = key_of(atpm)
    lv = iml_results["levels"][key]
    cal = lv["transitive_calibration"]
    fl = lv["flips_vs_glucose_only"]
    c = control["iml_levels"][key]
    ccal = c["transitive_calibration"]
    lines.append(
        f"iML1515 ATPM = {atpm}: WT {lv['wild_type_biomass']:.4f}; labels "
        f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
        f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, kappa "
        f"{fl['cohen_kappa']:.4f}); plain r = "
        f"{cal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{cal['held_out']['roc_auc']:.4f}; canonical r = "
        f"{ccal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{ccal['held_out']['roc_auc']:.4f}")
lines.append("")
lines.append("Flip details (iJO):")
for atpm in IJO_ATPM_LEVELS:
    fl = ijo_results["levels"][key_of(atpm)]["flips_vs_glucose_only"]
    if fl["n_gain_essential"] + fl["n_loss_essential"] == 0:
        continue
    lines.append(f"  ATPM = {atpm}: gains "
                 + ", ".join(f"{g['gene_id']}"
                             f"({g.get('gene_name', '')})"
                             for g in fl["gains"][:20])
                 + "; losses "
                 + ", ".join(f"{g['gene_id']}"
                             f"({g.get('gene_name', '')})"
                             for g in fl["losses"][:20]))
    lines.append(f"    enrichments: " + "; ".join(
        f"{d['subsystem']} ({d['n_flip']} vs exp {d['expected']})"
        for d in fl["subsystem_enrichment_top"][:5]))
with open(os.path.join(OUT_DIR, "keio_atpm_stress_summary.txt"),
          "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSummary written.")
print("ATPM-STRESS PROBE DONE.")
