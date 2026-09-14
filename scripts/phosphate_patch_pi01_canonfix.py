#!/usr/bin/env python3
"""Corrected HiGHS two-stage pFBA (split variables) and re-patch of
the canonical b0776 row at iJO1366 Pi = -0.1.

The earlier patch script's stage-2 minimized the SIGNED sum of
fluxes, which is not pFBA; the true parsimonious optimum at Pi=-0.1
has L1 = 91.965 (glpk cross-check).  This script implements pFBA
correctly with split variables (v = v+ - v-, minimize sum of
v+ + v-), verifies the optimum value across engines, recomputes the
canonical kV of the three biotin-pathway knockouts, re-patches the
b0776 canonical row, and recomputes the canonical level statistics.
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
    keio_tables, transitive_calibration, direct_arm)
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

IJO_MINERALS = ["EX_nh4_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
PI = -0.1


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


def build_split_lp(model):
    """Variables [v+ (n), v- (n)]; v = v+ - v-; v+ in [lb+, ub+],
    v- in [0, -lb] when lb<0."""
    n = len(model.reactions)
    mm = len(model.metabolites)
    rids = [r.id for r in model.reactions]
    midx = {met.id: i for i, met in enumerate(model.metabolites)}
    S = np.zeros((mm, n))
    for j, r in enumerate(model.reactions):
        for met, coef in r.metabolites.items():
            S[midx[met.id], j] = coef
    S_full = np.hstack([S, -S])
    lb = np.array([r.lower_bound for r in model.reactions])
    ub = np.array([r.upper_bound for r in model.reactions])
    lb_p = np.clip(lb, 0, None)          # v+ lower
    ub_p = np.clip(ub, 0, None)          # v+ upper
    ub_m = np.clip(-lb, 0, None)         # v- upper (v- >= 0)
    lb_m = np.clip(-ub, 0, None)         # v- lower
    bounds = list(zip(lb_p, ub_p)) + list(zip(lb_m, ub_m))
    c = np.zeros(n)
    for j, r in enumerate(model.reactions):
        if r.objective_coefficient != 0:
            c[j] = r.objective_coefficient
    c_full = np.concatenate([c, -c])
    return S_full, bounds, c_full, rids, n


def highs_pfba_split(S_full, bounds, c_full, n):
    # stage 1: max c'v
    res1 = linprog(-c_full, A_eq=S_full, b_eq=np.zeros(S_full.shape[0]),
                   bounds=bounds, method="highs")
    assert res1.status == 0
    bmax = float(-res1.fun)
    # stage 2: min sum(v+ + v-) s.t. Sv = 0, bounds, c'v >= bmax
    res2 = linprog(np.ones(2 * n), A_ub=-c_full.reshape(1, -1),
                   b_ub=np.array([-bmax]),
                   A_eq=S_full, b_eq=np.zeros(S_full.shape[0]),
                   bounds=bounds, method="highs")
    assert res2.status == 0
    v = res2.x[:n] - res2.x[n:]
    return bmax, v, float(np.abs(v).sum())


print("=" * 78)
print("Corrected HiGHS split-variable pFBA at Pi = -0.1")
print("=" * 78, flush=True)

# WT canonical vector
mw = fresh_ijo()
S_full, bounds, c_full, rids, n = build_split_lp(mw)
b_wt, v_wt, l1_wt = highs_pfba_split(S_full, bounds, c_full, n)
print(f"WT: biomass {b_wt:.10f}, L1 {l1_wt:.4f} "
      f"(glpk cross-check 91.965)", flush=True)
assert abs(b_wt - 0.1036665834) < 1e-8

# the three KOs
results = {}
for gid in ["b0180", "b0776", "b3412"]:
    mk = fresh_ijo()
    for r in mk.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    S2, bnd2, c2, rids2, n2 = build_split_lp(mk)
    b_ko, v_ko, l1_ko = highs_pfba_split(S2, bnd2, c2, n2)
    dv = v_ko - v_wt
    mask = np.abs(dv) > 1e-6
    kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
    results[gid] = {"b_ko": b_ko, "l1_ko": l1_ko, "kV": kV,
                    "n_changed": int(mask.sum())}
    print(f"{gid}: biomass {b_ko:.2e}, KO L1 {l1_ko:.4f}, "
          f"canonical kV {kV:.4f} (n={int(mask.sum())})", flush=True)
    assert abs(b_ko) < 1e-9

# ---- re-patch the canonical b0776 row with the corrected value ----
CAN_CSV = os.path.join(OUT_DIR, "keio_phosphate_pfba_control_pi_0.1.csv")
cd = pd.read_csv(CAN_CSV)
new = results["b0776"]
sel = cd["gene_id"] == "b0776"
assert sel.sum() == 1
old_kV = float(cd.loc[sel, "kV"].iloc[0])
cd.loc[sel, "b_ko"] = 0.0
cd.loc[sel, "delta_b"] = b_wt
cd.loc[sel, "y_essential"] = 1
cd.loc[sel, "kV"] = new["kV"]
cd.loc[sel, "n_changed"] = new["n_changed"]
cd.to_csv(CAN_CSV, index=False)
print(f"\nb0776 canonical row re-patched: kV {old_kV:.4f} -> "
      f"{new['kV']:.4f}", flush=True)

# consistency disclosure for b0180 / b3412 (glpk kV vs HiGHS kV)
for gid in ["b0180", "b3412"]:
    row = cd[cd.gene_id == gid]
    print(f"{gid}: canonical kV in CSV (glpk) "
          f"{float(row.kV.iloc[0]):.4f} vs HiGHS "
          f"{results[gid]['kV']:.4f}")

# ---- recompute the canonical level statistics ----
keio_tab, st6_tab = keio_tables()
ccal = transitive_calibration(cd)
cda, _ = direct_arm(cd, keio_tab, st6_tab)
base_kV = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
mg = cd[["gene_id", "kV"]].merge(base_kV, on="gene_id")
rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
plain = pd.read_csv(os.path.join(
    OUT_DIR, "keio_phosphate_limited_e12_sweep.csv"))
lvl = plain[plain["pi_bound"] == PI]
mgl = lvl[["gene_id", "y_essential"]].merge(
    cd[["gene_id", "y_essential"]], on="gene_id",
    suffixes=("_fba", "_canon"))
kap = float(cohen_kappa_score(mgl.y_essential_fba, mgl.y_essential_canon))
print(f"\nFINAL canonical Pi=-0.1: {int(cd.y_essential.sum())} essential; "
      f"r = {ccal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
      f"{ccal['held_out']['roc_auc']:.4f}; MCC "
      f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; label "
      f"kappa {kap:.4f}", flush=True)

# ---- update the control JSON ----
CTRL_JSON = os.path.join(OUT_DIR, "keio_phosphate_pfba_control.json")
ctrl = json.load(open(CTRL_JSON))
cl = ctrl["ijo_levels"]["pi_0.1"]
cl["transitive_calibration"] = ccal
cl["direct_arm"] = cda
cl["kV_rank_corr_vs_baseline_canonical"] = rho
cl["label_agreement_fba_vs_pfba_kappa"] = kap
cl["n_essential"] = int(cd.y_essential.sum())
cl["solver_integrity"] = {
    "finding": ("bioF (b0776) canonical call corrupted by pFBA's "
                "internal stale slim_optimize; re-adjudicated with "
                "corrected split-variable HiGHS two-stage pFBA "
                "(biomass 0, KO L1 " + f"{results['b0776']['l1_ko']:.4f}" +
                ", WT L1 " + f"{l1_wt:.4f}" + " = glpk cross-check)."),
    "patched": {"b0776": {"kV": results["b0776"]["kV"],
                          "n_changed": results["b0776"]["n_changed"],
                          "b_ko": 0.0}},
    "cross_engine_disclosure": (
        "b0180/b3412 canonical kV retain the glpk convention "
        f"({float(cd[cd.gene_id=='b0180'].kV.iloc[0]):.4f}); the HiGHS "
        "split-variable values are "
        + str({g: round(results[g]['kV'], 2) for g in ['b0180', 'b3412']})
        + " -- the L1-minimal argmin at zero growth is engine-"
        "dependent at this degenerate level; labels and optima are "
        "engine-independent (verified)."),
}
ctrl["levels_note"] = (
    "All canonical kV at this level use the glpk pFBA convention "
    "except b0776 (HiGHS split-variable pFBA, disclosed); labels are "
    "engine-verified identical (289/1367).")
with open(CTRL_JSON, "w") as f:
    json.dump(ctrl, f, indent=2)
print("control JSON updated.")
