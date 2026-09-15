#!/usr/bin/env python3
"""Apply the ATPM-axis solver-tolerance corrections (6 corrupted calls
adjudicated by keio_atpm_integrity_adjudication.json) to the deposited
artifacts, following the repo's correction conventions (phosphate /
O2 rounds):

  plain corrected rows:     b_ko = 0, y = 1, kV/n_changed from the
                           HiGHS plain-vertex distances;
  canonical corrected rows: b_ko = 0, y = 1, kV = the shared
                           two-stage-pFBA zero-growth distance,
                           n_changed shared.

Then recomputes every affected statistic: the two plain sweeps'
transitive calibrations and flip records (atpm_100 levels), the iML
canonical level stats, the control JSON's plain references and label
agreements, and the summary txt.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from cobra.io import load_json_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from nitrogen_source_keio_probe import (transitive_calibration,
                                        flip_analysis)
DL = os.path.join(REPO, "download")

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']

CORRECTIONS = {
    ("iJO1366", 100.0): {"plain": ["b0180", "b3412"], "canon": []},
    ("iML1515", 100.0): {"plain": ["b0778", "b0180"],
                         "canon": ["b1288", "b0776"]},
}


def set_ijo(model, atpm):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex in IJO_MINERALS:
        model.reactions.get_by_id(ex).lower_bound = -1000.0
    model.reactions.get_by_id("ATPM").lower_bound = atpm


def set_iml(model, atpm):
    for r in model.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex in IML_MINERALS:
        try:
            model.reactions.get_by_id(ex).lower_bound = -10
        except Exception:
            pass
    model.reactions.get_by_id("ATPM").lower_bound = atpm


def lp_arrays(model):
    n, m = len(model.reactions), len(model.metabolites)
    rids = [r.id for r in model.reactions]
    midx = {met.id: i for i, met in enumerate(model.metabolites)}
    S = np.zeros((m, n))
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
    return (float(-res.fun) if res.status == 0 else 0.0,
            res.x if res.status == 0 else None)


def highs_pfba(S, lb, ub, c, bio_j):
    """Two-stage split-variable pFBA with HiGHS: stage 1 max biomass;
    stage 2 min L1 at biomass >= stage-1 optimum, with the full
    reaction bounds lb <= v <= ub imposed on v = vp - vm."""
    b, x0 = highs_solve(S, lb, ub, c)
    if x0 is None:
        return 0.0, None
    n = S.shape[1]
    S2 = np.hstack([S, -S])                       # 2n columns
    A_eq, b_eq = S2, np.zeros(S.shape[0])
    # biomass >= b:  -(vp_j - vm_j) <= -b
    cb = np.zeros(2 * n)
    cb[bio_j] = -1.0
    cb[bio_j + n] = 1.0
    # reaction bounds: lb_j <= vp_j - vm_j <= ub_j
    E = np.eye(n)
    A_ub = np.vstack([np.hstack([E, -E]),
                      np.hstack([-E, E]),
                      cb.reshape(1, -1)])
    b_ub = np.concatenate([ub, -lb, [-b]])
    cost = np.ones(2 * n)
    bounds = [(0, None)] * (2 * n)
    res = linprog(cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    if res.status != 0:
        return b, None
    v = res.x[:n] - res.x[n:]
    return b, v


def kV_between(v1, v2, rids):
    dv = np.abs(v1 - v2)
    mask = dv > 1e-6
    return float((dv[mask] ** 2).sum()), int(mask.sum())


report = {"corrections": []}
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
GENE_NAME = {g.id: (g.name or "?") for g in list(ijo.genes) + list(iml.genes)}

for (model, atpm), corr in CORRECTIONS.items():
    if not (corr["plain"] or corr["canon"]):
        continue
    mdl = ijo if model == "iJO1366" else iml
    setter = set_ijo if model == "iJO1366" else set_iml
    bio = None
    for r in mdl.reactions:
        if r.objective_coefficient != 0 and ("BIOMASS" in r.id or
                                             "iomass" in r.id):
            bio = r.id
            break
    bio_j = [r.id for r in mdl.reactions].index(bio)
    setter(mdl, atpm)

    # WT references (HiGHS)
    S, lb, ub, c, rids = lp_arrays(mdl)
    b_wt_plain, v_wt_plain = highs_solve(S, lb, ub, c)
    b_wt_can, v_wt_can = highs_pfba(S, lb, ub, c, bio_j)
    print(f"{model} ATPM {atpm}: HiGHS WT plain {b_wt_plain:.6f}, "
          f"pFBA {b_wt_can:.6f}", flush=True)

    for gid in sorted(set(corr["plain"])):
        with mdl:
            for r in mdl.reactions:
                if gid in r.gene_reaction_rule:
                    r.lower_bound = 0
                    r.upper_bound = 0
            S2, lb2, ub2, c2, _ = lp_arrays(mdl)
            b_ko, v_ko = highs_solve(S2, lb2, ub2, c2)
        kv, nc = kV_between(v_wt_plain, v_ko, rids)
        report["corrections"].append({
            "model": model, "atpm": atpm, "gene_id": gid,
            "gene_name": GENE_NAME.get(gid), "arm": "plain",
            "b_ko_true": 0.0, "kV": kv, "n_changed": nc})
        print(f"  plain {gid} ({GENE_NAME.get(gid)}): b_ko {b_ko:.2e}, "
              f"kV {kv:.1f}, n {nc}", flush=True)

    for gid in sorted(set(corr["canon"])):
        with mdl:
            for r in mdl.reactions:
                if gid in r.gene_reaction_rule:
                    r.lower_bound = 0
                    r.upper_bound = 0
            S2, lb2, ub2, c2, _ = lp_arrays(mdl)
            _, v_ko = highs_pfba(S2, lb2, ub2, c2, bio_j)
        kv, nc = kV_between(v_wt_can, v_ko, rids)
        report["corrections"].append({
            "model": model, "atpm": atpm, "gene_id": gid,
            "gene_name": GENE_NAME.get(gid), "arm": "canonical",
            "b_ko_true": 0.0, "kV": kv, "n_changed": nc})
        print(f"  canon {gid} ({GENE_NAME.get(gid)}): kV {kv:.4f}, "
              f"n {nc}", flush=True)

# ---------------- patch the artifacts --------------------------------
def patch_csv(path, key_col, key_val, arm, model):
    df = pd.read_csv(path)
    sel = (df[key_col] == key_val) if key_col else pd.Series(
        True, index=df.index)
    n_patched = 0
    for cr in report["corrections"]:
        if cr["arm"] != arm or cr["model"] != model:
            continue
        m = sel & (df.gene_id == cr["gene_id"])
        if not m.any():
            print(f"  WARN: {cr['gene_id']} not in {os.path.basename(path)}")
            continue
        df.loc[m, "b_ko"] = 0.0
        df.loc[m, "delta_b"] = df.loc[m, "b_wt"]
        df.loc[m, "y_essential"] = 1
        df.loc[m, "kV"] = cr["kV"]
        df.loc[m, "n_changed"] = cr["n_changed"]
        n_patched += int(m.sum())
    df.to_csv(path, index=False)
    return n_patched


print("\n--- patching artifacts ---", flush=True)
n1 = patch_csv(os.path.join(DL, "keio_atpm_stress_e12_sweep.csv"),
               "atpm_bound", 100.0, "plain", "iJO1366")
n2 = patch_csv(os.path.join(DL, "keio_atpm_stress_e16_sweep.csv"),
               "atpm_bound", 100.0, "plain", "iML1515")
n3 = patch_csv(os.path.join(DL, "keio_atpm_pfba_control_iml_atpm_100.csv"),
               None, None, "canonical", "iML1515")
print(f"patched rows: e12 plain {n1}, e16 plain {n2}, iml canon {n3}")

# ---------------- recompute statistics ------------------------------
from sklearn.metrics import cohen_kappa_score

# plain frames at atpm_100
e12 = pd.read_csv(os.path.join(DL, "keio_atpm_stress_e12_sweep.csv"))
pl_ijo = e12[e12.atpm_bound == 100.0].copy()
e16 = pd.read_csv(os.path.join(DL, "keio_atpm_stress_e16_sweep.csv"))
pl_iml = e16[e16.atpm_bound == 100.0].copy()
can_ijo = pd.read_csv(os.path.join(DL, "keio_atpm_pfba_control_atpm_100.csv"))
can_iml = pd.read_csv(
    os.path.join(DL, "keio_atpm_pfba_control_iml_atpm_100.csv"))

cal_ijo = transitive_calibration(pl_ijo)
cal_iml = transitive_calibration(pl_iml)
fl_ijo, _ = flip_analysis(
    pl_ijo, os.path.join(DL, "keio_glucose_only_e12.csv"), ijo,
    "ATPM=100 vs glucose-only (corrected)")
fl_iml, _ = flip_analysis(
    pl_iml, os.path.join(DL, "keio_glucose_only_e16_sweep.csv"), iml,
    "iML1515 ATPM=100 vs glucose-only (corrected)")
print(f"\niJO atpm_100 corrected plain: r {cal_ijo['pearson_r_log_kV_delta_b']:+.4f} "
      f"AUC {cal_ijo['held_out']['roc_auc']:.4f}; labels "
      f"{fl_ijo['n_essential_base']} -> {fl_ijo['n_essential_new']} "
      f"(+{fl_ijo['n_gain_essential']}/-{fl_ijo['n_loss_essential']}, "
      f"kappa {fl_ijo['cohen_kappa']:.4f})")
print(f"iML atpm_100 corrected plain: r {cal_iml['pearson_r_log_kV_delta_b']:+.4f} "
      f"AUC {cal_iml['held_out']['roc_auc']:.4f}; labels "
      f"{fl_iml['n_essential_base']} -> {fl_iml['n_essential_new']} "
      f"(+{fl_iml['n_gain_essential']}/-{fl_iml['n_loss_essential']}, "
      f"kappa {fl_iml['cohen_kappa']:.4f})")

ccal_iml = transitive_calibration(can_iml)
mgl = pl_iml[["gene_id", "y_essential"]].merge(
    can_iml[["gene_id", "y_essential"]], on="gene_id",
    suffixes=("_fba", "_canon"))
k_iml = float(cohen_kappa_score(mgl.y_essential_fba, mgl.y_essential_canon))
mgi = pl_ijo[["gene_id", "y_essential"]].merge(
    can_ijo[["gene_id", "y_essential"]], on="gene_id",
    suffixes=("_fba", "_canon"))
k_ijo = float(cohen_kappa_score(mgi.y_essential_fba, mgi.y_essential_canon))
print(f"iML atpm_100 corrected canonical: r "
      f"{ccal_iml['pearson_r_log_kV_delta_b']:+.4f} AUC "
      f"{ccal_iml['held_out']['roc_auc']:.4f} MCC "
      f"{ccal_iml['held_out']['mcc']:.4f} n_ess "
      f"{int(can_iml.y_essential.sum())}; arm kappa {k_iml:.4f}")
print(f"iJO atpm_100 arm kappa (plain corrected): {k_ijo:.4f}")

# ---- update the results JSONs + control JSON ----
r12 = json.load(open(os.path.join(DL, "keio_atpm_stress_e12_results.json")))
lv = r12["levels"]["atpm_100"]
lv["transitive_calibration"] = cal_ijo
lv["flips_vs_glucose_only"] = fl_ijo
lv["corrected_calls"] = {
    "note": ("two plain false-viability calls (b0180 fabZ, b3412 bioH) "
             "re-adjudicated with the independent HiGHS engine per the "
             "repo trace-quota protocol; labels +2 restored"),
    "genes": ["b0180", "b3412"]}
with open(os.path.join(DL, "keio_atpm_stress_e12_results.json"), "w") as f:
    json.dump(r12, f, indent=2)

r16 = json.load(open(os.path.join(DL, "keio_atpm_stress_e16_results.json")))
lv = r16["levels"]["atpm_100"]
lv["transitive_calibration"] = cal_iml
lv["flips_vs_glucose_only"] = fl_iml
lv["corrected_calls"] = {
    "note": ("two plain false-viability calls (b0778 bioD, b0180 fabZ) "
             "and two canonical false-viability calls (b1288, b0776 "
             "bioF) re-adjudicated with the independent HiGHS engine; "
             "labels +2 restored on each arm"),
    "genes_plain": ["b0778", "b0180"], "genes_canonical": ["b1288", "b0776"]}
with open(os.path.join(DL, "keio_atpm_stress_e16_results.json"), "w") as f:
    json.dump(r16, f, indent=2)

ctrl = json.load(open(os.path.join(DL, "keio_atpm_pfba_control.json"))
                 ) if os.path.exists(
    os.path.join(DL, "keio_atpm_pfba_control.json")) else {}
vj = ctrl["ijo_levels"]["atpm_100"]
vj["plain_reference_r"] = cal_ijo["pearson_r_log_kV_delta_b"]
vj["plain_reference_auc"] = cal_ijo["held_out"]["roc_auc"]
vj["label_agreement_fba_vs_pfba_kappa"] = k_ijo
vj["corrected_calls"] = ["b0180", "b3412"]
vm = ctrl["iml_levels"]["atpm_100"]
vm["n_essential"] = int(can_iml.y_essential.sum())
vm["transitive_calibration"] = ccal_iml
vm["plain_reference_r"] = cal_iml["pearson_r_log_kV_delta_b"]
vm["plain_reference_auc"] = cal_iml["held_out"]["roc_auc"]
vm["label_agreement_fba_vs_pfba_kappa"] = k_iml
vm["corrected_calls"] = {"plain": ["b0778", "b0180"],
                         "canonical": ["b1288", "b0776"]}
with open(os.path.join(DL, "keio_atpm_pfba_control.json"), "w") as f:
    json.dump(ctrl, f, indent=2)

# extend the adjudication artifact with the patch record
adj = json.load(open(
    os.path.join(DL, "keio_atpm_integrity_adjudication.json")))
adj["patch"] = report
adj["post_patch"] = {
    "iJO_atpm_100": {"plain_r": cal_ijo["pearson_r_log_kV_delta_b"],
                     "labels": fl_ijo["n_essential_new"],
                     "gains": fl_ijo["n_gain_essential"],
                     "losses": fl_ijo["n_loss_essential"],
                     "kappa": fl_ijo["cohen_kappa"],
                     "arm_kappa": k_ijo},
    "iML_atpm_100": {"plain_r": cal_iml["pearson_r_log_kV_delta_b"],
                     "canon_r": ccal_iml["pearson_r_log_kV_delta_b"],
                     "canon_auc": ccal_iml["held_out"]["roc_auc"],
                     "labels": fl_iml["n_essential_new"],
                     "gains": fl_iml["n_gain_essential"],
                     "losses": fl_iml["n_loss_essential"],
                     "kappa": fl_iml["cohen_kappa"],
                     "arm_kappa": k_iml,
                     "canon_n_essential": int(can_iml.y_essential.sum())}}
with open(os.path.join(DL, "keio_atpm_integrity_adjudication.json"),
          "w") as f:
    json.dump(adj, f, indent=2)
print("\nALL PATCHES + RECOMPUTATIONS DONE")
