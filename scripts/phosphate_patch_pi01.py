#!/usr/bin/env python3
"""Patch the three tolerance-corrupted rows at iJO1366 Pi = -0.1 with
HiGHS-verified values and recompute the level statistics.

Adjudicated truth (phosphate_highs_adjudication.py, scipy-HiGHS, no
glpk code): fabZ (b0180), bioF (b0776), bioH (b3412) are ALL
essential at Pi = -0.1 (biomass max exactly 0.0 in every KO).  The
label set is therefore invariant at every phosphate level (289/1367).

Corrupted calls being patched:
  PLAIN arm  : b0180 b_ko 0.103667 -> 0.0 ; b3412 b_ko 0.103667 -> 0.0
  CANON arm  : b0776 b_ko 0.103667 -> 0.0 (its pFBA slim_optimize
               warm start returned the stale value; kV ~ 0 was bogus)

Mechanism (revised): primal-feasibility tolerance, not warm-start
staleness.  At Pi = -0.1 the wild-type growth 0.1037 scales the
biotin drain to 2.07e-07 mmol/gDW/h (coefficient 2e-06 per biomass
unit) -- about twice glpk's default bound tolerance (1e-7, scaled
internally) -- so the simplex sometimes accepts a 'solution' that
violates the hard zero bounds of the knocked-out biotin steps.
This also explains the iML1515 anaerobic fabZ row (q8 side-chain
quota 2.68e-07 at growth 0.134) and why no corruption appears at
growth >= 0.23 (quota >= 4.6e-07, reliably detected) or for genes
with buffered roles.  The failure is one-directional (false
viability); every observed 'loss' call at a low-growth level
belongs to the trace-quota set and is re-adjudicated here or in
keio_o2_solver_integrity_fix.py.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.optimize import linprog

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from nitrogen_source_keio_probe import (
    keio_tables, transitive_calibration, direct_arm, flip_analysis)

IJO_MINERALS = ["EX_nh4_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
PI = -0.1
PLAIN_PATCH = {"b0180": None, "b3412": None}   # gene -> new row dict
CANON_PATCH = {"b0776": None}


def fresh_ijo():
    m = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
    for r in m.exchanges:
        r.lower_bound = 0
    m.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    m.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        m.reactions.get_by_id(ex_id).lower_bound = -1000.0
    m.reactions.get_by_id("EX_pi_e").lower_bound = PI
    return m


def build_lp(model):
    n, mm = len(model.reactions), len(model.metabolites)
    rids = [r.id for r in model.reactions]
    midx = {met.id: i for i, met in enumerate(model.metabolites)}
    S = np.zeros((mm, n))
    for j, r in enumerate(model.reactions):
        for met, coef in r.metabolites.items():
            S[midx[met.id], j] = coef
    lb = np.array([r.lower_bound for r in model.reactions])
    ub = np.array([r.upper_bound for r in model.reactions])
    c = np.zeros(n)
    for j, r in enumerate(model.reactions):
        if r.objective_coefficient != 0:
            c[j] = r.objective_coefficient
    return S, lb, ub, c, rids


def highs_solve(S, lb, ub, c):
    res = linprog(-c, A_eq=S, b_eq=np.zeros(S.shape[0]),
                  bounds=np.column_stack([lb, ub]), method="highs")
    assert res.status == 0
    return float(-(res.fun)), res.x


def highs_pfba(S, lb, ub, c):
    """Two-stage HiGHS pFBA: max biomass, then min L1 at that optimum."""
    bmax, _ = highs_solve(S, lb, ub, c)
    # stage 2: min 1'v s.t. S v = 0, bounds, c'v >= bmax (exact)
    res = linprog(np.ones(len(c)), A_ub=-c.reshape(1, -1),
                  b_ub=np.array([-bmax]),
                  A_eq=S, b_eq=np.zeros(S.shape[0]),
                  bounds=np.column_stack([lb, ub]), method="highs")
    assert res.status == 0
    return bmax, res.x


print("=" * 78)
print("HiGHS-verified patch of the Pi = -0.1 tolerance-corrupted rows")
print("=" * 78, flush=True)

# ---- canonical WT reference (HiGHS pFBA) for kV computation ----
mw = fresh_ijo()
S, lb, ub, c, rids = build_lp(mw)
b_wt, x_wt_canon = highs_pfba(S, lb, ub, c)
wt_canon = pd.Series(x_wt_canon, index=rids)
print(f"HiGHS pFBA WT at Pi={PI}: biomass {b_wt:.10f}, "
      f"L1 {np.abs(x_wt_canon).sum():.3f}", flush=True)
# sanity: must match the deposited canonical WT (0.103667)
assert abs(b_wt - 0.103667) < 1e-6

# ---- patch values per gene ----
for gid in ["b0180", "b3412", "b0776"]:
    mk = fresh_ijo()
    for r in mk.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    S2, lb2, ub2, c2, rids2 = build_lp(mk)
    b_ko, x_ko_plain = highs_solve(S2, lb2, ub2, c2)      # plain vertex
    b_ko_c, x_ko_canon = highs_pfba(S2, lb2, ub2, c2)     # canonical vertex
    assert abs(b_ko) < 1e-12 and abs(b_ko_c) < 1e-12
    # plain kV: HiGHS plain vertex vs the deposited plain WT vector
    # (the plain arm's WT vector: recompute with HiGHS plain solve)
    _, x_wt_plain = highs_solve(S, lb, ub, c)
    wt_plain = pd.Series(x_wt_plain, index=rids)
    dv_p = x_ko_plain - x_wt_plain
    kV_p = float(np.sum(dv_p[np.abs(dv_p) > 1e-6] ** 2))
    n_p = int(np.sum(np.abs(dv_p) > 1e-6))
    dv_c = x_ko_canon - x_wt_canon
    kV_c = float(np.sum(dv_c[np.abs(dv_c) > 1e-6] ** 2))
    n_c = int(np.sum(np.abs(dv_c) > 1e-6))
    l1_ko_highs = float(np.abs(x_ko_canon).sum())
    print(f"{gid}: plain kV {kV_p:.4f} (n={n_p}); canonical kV "
          f"{kV_c:.4f} (n={n_c}); HiGHS KO L1 {l1_ko_highs:.3f}",
          flush=True)
    if gid in PLAIN_PATCH:
        PLAIN_PATCH[gid] = {"b_ko": 0.0, "delta_b": b_wt,
                            "y_essential": 1, "kV": kV_p,
                            "n_changed": n_p,
                            "l1_ko_highs": l1_ko_highs}
    if gid in CANON_PATCH:
        CANON_PATCH[gid] = {"b_ko": 0.0, "delta_b": b_wt,
                            "y_essential": 1, "kV": kV_c,
                            "n_changed": n_c,
                            "l1_ko_highs": l1_ko_highs}

# ---- patch the plain sweep CSV ----
SWEEP_CSV = os.path.join(OUT_DIR, "keio_phosphate_limited_e12_sweep.csv")
d = pd.read_csv(SWEEP_CSV)
for gid, new in PLAIN_PATCH.items():
    sel = (d["pi_bound"] == PI) & (d["gene_id"] == gid)
    assert sel.sum() == 1
    for col, val in new.items():
        d.loc[sel, col] = val
d.to_csv(SWEEP_CSV, index=False)
print("plain sweep patched:", list(PLAIN_PATCH))

# ---- patch the canonical CSV ----
CAN_CSV = os.path.join(OUT_DIR, "keio_phosphate_pfba_control_pi_0.1.csv")
cd = pd.read_csv(CAN_CSV)
for gid, new in CANON_PATCH.items():
    sel = cd["gene_id"] == gid
    assert sel.sum() == 1
    for col, val in new.items():
        cd.loc[sel, col] = val
cd.to_csv(CAN_CSV, index=False)
print("canonical sweep patched:", list(CANON_PATCH))

# ---- recompute the plain level statistics ----
keio_tab, st6_tab = keio_tables()
ijo = fresh_ijo()
lvl = d[d["pi_bound"] == PI].copy()
cal = transitive_calibration(lvl)
da, _ = direct_arm(lvl, keio_tab, st6_tab)
fl, _ = flip_analysis(
    lvl, os.path.join(OUT_DIR, "keio_glucose_only_e12.csv"), ijo,
    f"Pi={PI} vs glucose-only [HiGGS-corrected]")
print(f"\nCORRECTED plain Pi=-0.1: labels {fl['n_essential_base']} -> "
      f"{fl['n_essential_new']} (+{fl['n_gain_essential']}/"
      f"-{fl['n_loss_essential']}, kappa {fl['cohen_kappa']:.4f}); "
      f"r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
      f"AUC {cal['held_out']['roc_auc']:.4f}; direct "
      f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)

# ---- recompute the canonical level statistics ----
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score
base_kV = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
ccal = transitive_calibration(cd)
cda, _ = direct_arm(cd, keio_tab, st6_tab)
mg = cd[["gene_id", "kV"]].merge(base_kV, on="gene_id")
rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
mgl = lvl[["gene_id", "y_essential"]].merge(
    cd[["gene_id", "y_essential"]], on="gene_id",
    suffixes=("_fba", "_canon"))
kap = float(cohen_kappa_score(mgl.y_essential_fba, mgl.y_essential_canon))
print(f"CORRECTED canon Pi=-0.1: {int(cd.y_essential.sum())} essential; "
      f"r = {ccal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
      f"{ccal['held_out']['roc_auc']:.4f}; MCC "
      f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; label "
      f"kappa {kap:.4f}", flush=True)

# ---- update the JSONs ----
RES_JSON = os.path.join(OUT_DIR, "keio_phosphate_limited_e12_results.json")
res = json.load(open(RES_JSON))
key = "pi_0.1"
lv = res["levels"][key]
lv["transitive_calibration"] = cal
lv["direct_arm"] = da
lv["flips_vs_glucose_only"] = fl
lv["solver_integrity"] = {
    "finding": ("Plain-sweep calls for fabZ (b0180) and bioH (b3412) "
                "were tolerance artifacts (b_ko returned at the wild-"
                "type value); HiGHS adjudication gives biomass max "
                "exactly 0.0 for every biotin-pathway knockout."),
    "mechanism": ("Primal-feasibility tolerance: the biotin drain at "
                  "growth 0.1037 is 2.07e-07 mmol/gDW/h, ~2x glpk's "
                  "default bound tolerance, so the simplex can accept "
                  "solutions violating the hard zero bounds of the "
                  "knocked-out steps. One-directional (false "
                  "viability); affects only trace-quota genes at "
                  "low growth."),
    "patched": ["b0180", "b3412"],
}
with open(RES_JSON, "w") as f:
    json.dump(res, f, indent=2)

CTRL_JSON = os.path.join(OUT_DIR, "keio_phosphate_pfba_control.json")
ctrl = json.load(open(CTRL_JSON))
cl = ctrl["ijo_levels"][key]
cl["transitive_calibration"] = ccal
cl["direct_arm"] = cda
cl["kV_rank_corr_vs_baseline_canonical"] = rho
cl["label_agreement_fba_vs_pfba_kappa"] = kap
cl["n_essential"] = int(cd.y_essential.sum())
cl["plain_reference_r"] = cal["pearson_r_log_kV_delta_b"]
cl["plain_reference_auc"] = cal["held_out"]["roc_auc"]
cl["solver_integrity"] = {
    "finding": ("The canonical call for bioF (b0776) was corrupted in "
                "the opposite direction (pFBA's internal slim_optimize "
                "returned the stale wild-type optimum, so the knockout "
                "was recorded as fully buffered, kV ~ 0). HiGHS "
                "two-stage pFBA gives biomass 0.0."),
    "patched": ["b0776"],
}
ctrl["tolerance_note"] = (
    "All three corrupted calls at this level belong to the biotin "
    "biosynthesis pathway (fabZ side-chain arm, bioH, bioF); the "
    "HiGHS adjudication (keio_phosphate_highs_adjudication.json) "
    "confirms all three essential, so the label set is invariant at "
    "every phosphate level: 289/1,367.")
with open(CTRL_JSON, "w") as f:
    json.dump(ctrl, f, indent=2)
print("\nJSONs updated. Patch complete.")
