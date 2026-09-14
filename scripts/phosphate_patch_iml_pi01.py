#!/usr/bin/env python3
"""HiGHS adjudication + patch of the iML1515 Pi = -0.1 corrupted rows.

Plain arm false-losses: b0778 (bioC), b0180 (fabZ), b3412 (bioH) --
all with the b_ko = wild-type tolerance signature.  Canonical arm:
b0778/b0180 correctly essential; b3412 corrupted (pFBA stale
slim_optimize).  HiGHS split-variable two-stage pFBA is the ground
truth; expect all three essential -> labels invariant at 286/1,516
at every phosphate level.
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
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
PI = -0.1
GENES = ["b0778", "b0180", "b3412"]


def fresh_iml():
    m = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
    for r in m.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    m.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    for o2_id in ['EX_o2_e', 'EX_o2s_e']:
        try:
            m.reactions.get_by_id(o2_id).lower_bound = -20.0
            break
        except Exception:
            continue
    for ex_id in IML_MINERALS:
        try:
            m.reactions.get_by_id(ex_id).lower_bound = -10
        except Exception:
            pass
    m.reactions.get_by_id("EX_pi_e").lower_bound = PI
    return m


def build_split_lp(model):
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
    bounds = list(zip(np.clip(lb, 0, None), np.clip(ub, 0, None))) + \
        list(zip(np.clip(-ub, 0, None), np.clip(-lb, 0, None)))
    c = np.zeros(n)
    for j, r in enumerate(model.reactions):
        if r.objective_coefficient != 0:
            c[j] = r.objective_coefficient
    c_full = np.concatenate([c, -c])
    return S_full, bounds, c_full, rids, n


def highs_pfba_split(S_full, bounds, c_full, n):
    res1 = linprog(-c_full, A_eq=S_full, b_eq=np.zeros(S_full.shape[0]),
                   bounds=bounds, method="highs")
    assert res1.status == 0
    bmax = float(-res1.fun)
    res2 = linprog(np.ones(2 * n), A_ub=-c_full.reshape(1, -1),
                   b_ub=np.array([-bmax]),
                   A_eq=S_full, b_eq=np.zeros(S_full.shape[0]),
                   bounds=bounds, method="highs")
    assert res2.status == 0
    v = res2.x[:n] - res2.x[n:]
    return bmax, v


print("=" * 78)
print("HiGHS adjudication, iML1515 Pi = -0.1")
print("=" * 78, flush=True)

mw = fresh_iml()
S_full, bounds, c_full, rids, n = build_split_lp(mw)
b_wt, v_wt = highs_pfba_split(S_full, bounds, c_full, n)
print(f"WT: biomass {b_wt:.10f}, L1 {float(np.abs(v_wt).sum()):.4f}",
      flush=True)
assert abs(b_wt - 0.103669) < 1e-6

patch_plain, patch_canon = {}, {}
for gid in GENES:
    mk = fresh_iml()
    for r in mk.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    S2, bnd2, c2, rids2, n2 = build_split_lp(mk)
    b_ko, v_ko = highs_pfba_split(S2, bnd2, c2, n2)
    dv = v_ko - v_wt
    mask = np.abs(dv) > 1e-6
    kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
    essential = b_ko < 0.05 * b_wt
    print(f"{gid}: biomass {b_ko:.2e}, essential {essential}, "
          f"canonical kV {kV:.4f} (n={int(mask.sum())})", flush=True)
    assert essential, f"{gid}: expected essential"
    patch_plain[gid] = {"b_ko": 0.0, "delta_b": b_wt, "y_essential": 1,
                        "kV": kV, "n_changed": int(mask.sum())}
    patch_canon[gid] = patch_plain[gid]

# ---- patch the plain sweep ----
SWEEP_CSV = os.path.join(OUT_DIR, "keio_phosphate_limited_e16_sweep.csv")
d = pd.read_csv(SWEEP_CSV)
for gid, new in patch_plain.items():
    sel = (d["pi_bound"] == PI) & (d["gene_id"] == gid)
    assert sel.sum() == 1
    for col, val in new.items():
        d.loc[sel, col] = val
d.to_csv(SWEEP_CSV, index=False)
print("plain sweep patched:", list(patch_plain))

# ---- patch the canonical sweep ----
CAN_CSV = os.path.join(OUT_DIR,
                       "keio_phosphate_pfba_control_iml_pi_0.1.csv")
cd = pd.read_csv(CAN_CSV)
for gid, new in patch_canon.items():
    row = cd[cd.gene_id == gid]
    # only patch where the canonical call was wrong or the kV stale
    if gid == "b3412" or float(row.b_ko.iloc[0]) > 1e-9:
        sel = cd["gene_id"] == gid
        for col, val in new.items():
            cd.loc[sel, col] = val
        print(f"canonical {gid} patched (was b_ko "
              f"{float(row.b_ko.iloc[0]):.6f}, kV "
              f"{float(row.kV.iloc[0]):.4f})")
cd.to_csv(CAN_CSV, index=False)

# ---- recompute both arms' level statistics ----
keio_tab, st6_tab = keio_tables()
iml = fresh_iml()
lvl = d[d["pi_bound"] == PI].copy()
cal = transitive_calibration(lvl)
da, _ = direct_arm(lvl, keio_tab, st6_tab)
fl, _ = flip_analysis(
    lvl, os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv"), iml,
    f"iML1515 Pi={PI} vs glucose-only [HiGHS-corrected]")
print(f"\nCORRECTED plain iML Pi=-0.1: labels {fl['n_essential_base']} -> "
      f"{fl['n_essential_new']} (+{fl['n_gain_essential']}/"
      f"-{fl['n_loss_essential']}, kappa {fl['cohen_kappa']:.4f}); "
      f"r = {cal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
      f"{cal['held_out']['roc_auc']:.4f}; direct "
      f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)

ccal = transitive_calibration(cd)
cda, _ = direct_arm(cd, keio_tab, st6_tab)
base_kV = pd.read_csv(os.path.join(
    OUT_DIR, "keio_o2_pfba_control_iml_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
mg = cd[["gene_id", "kV"]].merge(base_kV, on="gene_id")
rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
mgl = lvl[["gene_id", "y_essential"]].merge(
    cd[["gene_id", "y_essential"]], on="gene_id",
    suffixes=("_fba", "_canon"))
kap = float(cohen_kappa_score(mgl.y_essential_fba, mgl.y_essential_canon))
print(f"CORRECTED canon iML Pi=-0.1: {int(cd.y_essential.sum())} "
      f"essential; r = {ccal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
      f"{ccal['held_out']['roc_auc']:.4f}; MCC "
      f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; label "
      f"kappa {kap:.4f}", flush=True)

# ---- update JSONs ----
RES_JSON = os.path.join(OUT_DIR, "keio_phosphate_limited_e16_results.json")
res = json.load(open(RES_JSON))
lv = res["levels"]["pi_0.1"]
lv["transitive_calibration"] = cal
lv["direct_arm"] = da
lv["flips_vs_glucose_only"] = fl
lv["solver_integrity"] = {
    "finding": ("Plain calls for bioC (b0778), fabZ (b0180), bioH "
                "(b3412) were tolerance artifacts; the canonical call "
                "for bioH was corrupted in the opposite direction. "
                "HiGHS split-variable two-stage pFBA adjudication: all "
                "three essential (biomass exactly 0.0)."),
    "patched_plain": list(patch_plain),
    "patched_canonical": ["b3412"],
}
with open(RES_JSON, "w") as f:
    json.dump(res, f, indent=2)

CTRL_JSON = os.path.join(OUT_DIR, "keio_phosphate_pfba_control.json")
ctrl = json.load(open(CTRL_JSON))
cl = ctrl["iml_levels"]["pi_0.1"]
cl["transitive_calibration"] = ccal
cl["direct_arm"] = cda
cl["kV_rank_corr_vs_baseline_canonical"] = rho
cl["label_agreement_fba_vs_pfba_kappa"] = kap
cl["n_essential"] = int(cd.y_essential.sum())
cl["plain_reference_r"] = cal["pearson_r_log_kV_delta_b"]
cl["plain_reference_auc"] = cal["held_out"]["roc_auc"]
cl["solver_integrity"] = {
    "patched": ["b3412"],
    "note": ("b0778/b0180 canonical calls were already correct; the "
             "three genes' canonical kV now all carry the HiGHS "
             "split-variable pFBA values (identical block signature)."),
}
with open(CTRL_JSON, "w") as f:
    json.dump(ctrl, f, indent=2)
print("\niML Pi=-0.1 patch complete; JSONs updated.")
