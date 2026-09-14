#!/usr/bin/env python3
"""SOLVER-INTEGRITY CORRECTION for the iML1515 anaerobic (O2 = 0)
level of the oxygen probe.

Finding (o2_pfba_control.py, chunk 7).  The deposited plain sweep
recorded the fabZ (b0180) knockout at the anaerobic level as fully
viable (b_ko = 0.134109 = the wild-type value exactly).  Three
independent fresh solves disagree:
  - fresh single-shot plain FBA on a newly loaded model:  optimal,
    b_ko = 0.0;
  - fresh two-stage parsimonious FBA (the canonical control): b_ko
    = 0.0, essential;
  - a verbatim re-run of the sequential warm-started sweep loop
    REPRODUCES the wrong 0.134109 -- the persistent glpk solver,
    when the objective is unchanged and only bounds are patched,
    can return the stale wild-type solution marked 'optimal'.

Damage audit (this script, PART B).  Every deposited plain sweep
level with a canonical counterpart is compared gene-by-gene:
  iML baseline / O2 -5 / O2 0;  iJO baseline / O2 -10/-5/-2.5;
  iJO nh4 -10/-2.5 / glu -10.
  Result: exactly ONE discrepancy in ~14,700 comparisons -- b0180
  at iML O2 0.  Labels agree everywhere else; biomass values agree
  to < 1e-6 everywhere else.  The invariance claims and all other
  statistics are unaffected; the canonical control doubles as an
  independent audit of the deposited plain artifacts.

Corrections applied (PART A):
  1. fresh single-shot re-solve of b0180 at the anaerobic level
     (new model load, no warm start); patch the sweep CSV row
     (b_ko, delta_b, y_essential, kV, n_changed) and the results
     JSON (flips_vs_glucose_only, transitive_calibration,
     direct_arm, n_essential fields);
  2. the corrected anaerobic label change is +6 gains / -0 losses
     (the six glycolysis genes; fabZ remains essential in every
     regime through its quinone-side-chain dehydratases
     OGMEACPD/OPMEACPD -- the only route to the ubiquinone side
     chain, required by the biomass reaction in every regime);
  3. the plain-FBA anaerobic association statistics are recomputed
     from the patched sweep (they were quoted from the corrupted
     row);
  4. a solver_integrity record is appended to the results JSON.

Artifacts (in-place corrections + audit record):
  download/keio_o2_limited_e16_sweep.csv        (one row patched)
  download/keio_o2_limited_e16_results.json     (level recomputed)
  download/keio_o2_solver_integrity_audit.json  (the audit record)
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from nitrogen_source_keio_probe import (
    keio_tables, transitive_calibration, direct_arm, flip_analysis)

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
GENE = "b0180"

SWEEP_CSV = os.path.join(OUT_DIR, "keio_o2_limited_e16_sweep.csv")
RES_JSON = os.path.join(OUT_DIR, "keio_o2_limited_e16_results.json")

# =====================================================================
# PART A: fresh re-solve of the corrupted row + patch + recompute
# =====================================================================
print("=" * 78)
print(f"PART A: fresh single-shot re-solve of {GENE} (fabZ) at O2 = 0")
print("=" * 78, flush=True)

iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
for r in iml.reactions:
    if r.id.startswith("EX_"):
        r.lower_bound = 0
iml.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
for o2_id in ['EX_o2_e', 'EX_o2s_e']:
    try:
        iml.reactions.get_by_id(o2_id).lower_bound = 0.0
        break
    except Exception:
        continue
for ex_id in IML_MINERALS:
    try:
        iml.reactions.get_by_id(ex_id).lower_bound = -10
    except Exception:
        pass

# WT (fresh) -- must reproduce the deposited WT exactly
wt = iml.optimize()
b_wt = float(wt.objective_value)
v_wt = wt.fluxes
print(f"fresh WT anaerobic: {b_wt:.10f} (deposited 0.1341091592)",
      flush=True)
assert abs(b_wt - 0.1341091591851952) < 1e-9

# KO (fresh single-shot on a SECOND, newly loaded model -- the
# warm-start pathology returns the stale WT solution whenever a
# plain optimize() has already run on the same model object, so the
# knockout must be the very first solve of a fresh instance)
iml2 = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
for r in iml2.reactions:
    if r.id.startswith("EX_"):
        r.lower_bound = 0
iml2.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
for o2_id in ['EX_o2_e', 'EX_o2s_e']:
    try:
        iml2.reactions.get_by_id(o2_id).lower_bound = 0.0
        break
    except Exception:
        continue
for ex_id in IML_MINERALS:
    try:
        iml2.reactions.get_by_id(ex_id).lower_bound = -10
    except Exception:
        pass
ko_rxns = [r.id for r in iml2.reactions if GENE in r.gene_reaction_rule]
for r in iml2.reactions:
    if GENE in r.gene_reaction_rule:
        r.lower_bound = 0
        r.upper_bound = 0
ko_sol = iml2.optimize()
assert ko_sol.status == "optimal"
b_ko = float(ko_sol.objective_value)
v_ko = ko_sol.fluxes
dv = v_ko - v_wt
mask = np.abs(dv) > 1e-6
kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
thr = 0.05 * b_wt
y_new = 1 if b_ko < thr else 0
print(f"fresh KO: status {ko_sol.status}, b_ko = {b_ko:.10f}, "
      f"kV = {kV:.6f}, n_changed = {int(mask.sum())}, "
      f"y_essential = {y_new}", flush=True)
assert b_ko < thr, "expected essential"

# mechanism check: which of the KO reactions carry flux in the WT?
wt_flux_ko_rxns = {r: float(v_wt.get(r, 0.0)) for r in ko_rxns
                   if abs(float(v_wt.get(r, 0.0))) > 1e-6}
print(f"WT flux through the knocked-out reactions: "
      f"{ {k: round(v, 3) for k, v in wt_flux_ko_rxns.items()} }",
      flush=True)

# ---- patch the sweep CSV ----
d = pd.read_csv(SWEEP_CSV)
sel = (d["o2_bound"] == 0.0) & (d["gene_id"] == GENE)
assert sel.sum() == 1
old = d[sel].iloc[0]
d.loc[sel, "b_ko"] = b_ko
d.loc[sel, "delta_b"] = b_wt - b_ko
d.loc[sel, "y_essential"] = y_new
d.loc[sel, "kV"] = kV
d.loc[sel, "n_changed"] = int(mask.sum())
d.to_csv(SWEEP_CSV, index=False)
print(f"patched CSV row: b_ko {old.b_ko:.6f} -> {b_ko:.6f}, "
      f"y {old.y_essential} -> {y_new}, kV {old.kV:.4f} -> {kV:.4f}",
      flush=True)

# ---- recompute the level statistics from the patched sweep ----
keio_tab, st6_tab = keio_tables()
lvl = d[d["o2_bound"] == 0.0].copy()
cal = transitive_calibration(lvl)
da, _ = direct_arm(lvl, keio_tab, st6_tab)
fl, _ = flip_analysis(
    lvl, os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv"),
    iml, "iML1515 O2=0 vs glucose-only (O2=-20) [corrected]")
print(f"\nCORRECTED anaerobic level statistics:")
print(f"  labels {fl['n_essential_base']} -> {fl['n_essential_new']} "
      f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, "
      f"kappa {fl['cohen_kappa']:.4f}, Jaccard {fl['jaccard']:.4f})")
print(f"  gains: {[x['gene_id'] for x in fl['gains']]}")
print(f"  losses: {[x['gene_id'] for x in fl['losses']]}")
print(f"  transitive r = {cal['pearson_r_log_kV_delta_b']:+.4f}, "
      f"AUC {cal['held_out']['roc_auc']:.4f}, "
      f"MCC {cal['held_out']['mcc']:.4f}")
print(f"  direct r = {da['pearson_r']:+.4f}, AUC {da['roc_auc']:.4f}; "
      f"model gaps {da['n_model_gaps_pecE_insilicoN']}, "
      f"mismatch {da['n_medium_mismatch_insilicoE_keioN']}", flush=True)

# ---- patch the results JSON ----
res = json.load(open(RES_JSON))
lv = res["levels"]["0.0"]
old_fl = lv["flips_vs_glucose_only"]
old_cal = lv["transitive_calibration"]
old_da = lv["direct_arm"]
lv["flips_vs_glucose_only"] = fl
lv["transitive_calibration"] = cal
lv["direct_arm"] = da
res["solver_integrity"] = {
    "finding": (
        "The deposited plain sweep recorded the fabZ (b0180) knockout "
        "at the anaerobic level as fully viable (b_ko = wild type "
        "exactly).  Fresh single-shot plain FBA and fresh two-stage "
        "parsimonious FBA both give b_ko = 0.0 (essential); a "
        "verbatim re-run of the sequential warm-started sweep loop "
        "reproduces the wrong value, identifying the mechanism as the "
        "persistent glpk solver returning a stale solution marked "
        "'optimal' when only bounds (not the objective) are patched."),
    "correction": (
        "The row was re-solved fresh and patched; the level statistics "
        "were recomputed.  The corrected anaerobic label change is "
        "+6 gains / -0 losses (fabZ remains essential in every regime "
        "through OGMEACPD/OPMEACPD, the only route to the ubiquinone "
        "side chain, a biomass requirement in every regime)."),
    "damage_audit": (
        "All deposited plain-sweep levels with canonical counterparts "
        "were compared gene-by-gene (biomass to 1e-6 + labels): "
        "exactly one discrepancy in ~14,700 comparisons (this row)."),
    "patched_gene": GENE, "level": "0.0",
    "old_values": {"b_ko": float(old.b_ko), "y_essential": int(old.y_essential),
                   "kV": float(old.kV)},
    "new_values": {"b_ko": b_ko, "y_essential": y_new, "kV": kV},
    "old_level_stats": {
        "labels": [old_fl["n_essential_base"], old_fl["n_essential_new"]],
        "flips": [old_fl["n_gain_essential"], old_fl["n_loss_essential"]],
        "kappa": old_fl["cohen_kappa"],
        "r": old_cal["pearson_r_log_kV_delta_b"],
        "auc": old_cal["held_out"]["roc_auc"],
        "direct_r": old_da["pearson_r"], "direct_auc": old_da["roc_auc"]},
    "new_level_stats": {
        "labels": [fl["n_essential_base"], fl["n_essential_new"]],
        "flips": [fl["n_gain_essential"], fl["n_loss_essential"]],
        "kappa": fl["cohen_kappa"], "jaccard": fl["jaccard"],
        "r": cal["pearson_r_log_kV_delta_b"],
        "auc": cal["held_out"]["roc_auc"],
        "mcc": cal["held_out"]["mcc"],
        "direct_r": da["pearson_r"], "direct_auc": da["roc_auc"]},
}
with open(RES_JSON, "w") as f:
    json.dump(res, f, indent=2)
print("\nResults JSON patched.")

# =====================================================================
# PART B: the full damage audit, recorded
# =====================================================================
print("\n" + "=" * 78)
print("PART B: damage audit (deposited plain vs fresh canonical)")
print("=" * 78, flush=True)

pairs = [
    ("iML baseline", "keio_glucose_only_e16_sweep.csv", None,
     "keio_o2_pfba_control_iml_baseline.csv"),
    ("iML O2 -5", "keio_o2_limited_e16_sweep.csv", -5.0,
     "keio_o2_pfba_control_iml_o2_5.csv"),
    ("iML O2 0", "keio_o2_limited_e16_sweep.csv", 0.0,
     "keio_o2_pfba_control_iml_o2_0.csv"),
    ("iJO O2 -10", "keio_o2_limited_e12_sweep.csv", -10.0,
     "keio_o2_pfba_control_ijo_o2_10.csv"),
    ("iJO O2 -5", "keio_o2_limited_e12_sweep.csv", -5.0,
     "keio_o2_pfba_control_ijo_o2_5.csv"),
    ("iJO O2 -2.5", "keio_o2_limited_e12_sweep.csv", -2.5,
     "keio_o2_pfba_control_ijo_o2_2.5.csv"),
    ("iJO baseline", "keio_glucose_only_e12.csv", None,
     "keio_nitrogen_pfba_control_baseline.csv"),
    ("iJO nh4 -10", "keio_nitrogen_source_e12_sweep.csv", "nh4_-10",
     "keio_nitrogen_pfba_control_nh4_-10.csv"),
    ("iJO nh4 -2.5", "keio_nitrogen_source_e12_sweep.csv", "nh4_-2.5",
     "keio_nitrogen_pfba_control_nh4_-2.5.csv"),
    ("iJO glu -10", "keio_nitrogen_source_e12_sweep.csv", "glu_-10",
     "keio_nitrogen_pfba_control_glu_-10.csv"),
]
audit = {"comparisons": [], "total_gene_comparisons": 0,
         "total_discrepancies": 0, "discrepant_genes": []}
for name, ppath, lv_, cpath in pairs:
    dd = pd.read_csv(os.path.join(OUT_DIR, ppath))
    if lv_ is not None:
        col = "o2_bound" if "o2_bound" in dd.columns else "level"
        dd = dd[dd[col] == lv_]
    c = pd.read_csv(os.path.join(OUT_DIR, cpath))
    m = dd[["gene_id", "b_ko", "y_essential"]].merge(
        c[["gene_id", "b_ko", "y_essential"]], on="gene_id",
        suffixes=("_p", "_c"))
    big = (m.b_ko_p - m.b_ko_c).abs() > 1e-6
    lab = m.y_essential_p != m.y_essential_c
    hits = list(m[big | lab].gene_id)
    audit["comparisons"].append({
        "level": name, "n_genes": int(len(m)),
        "n_biomass_discrepant": int(big.sum()),
        "n_label_discrepant": int(lab.sum()), "genes": hits})
    audit["total_gene_comparisons"] += int(len(m))
    audit["total_discrepancies"] += int((big | lab).sum())
    audit["discrepant_genes"] += [f"{name}:{g}" for g in hits]
    print(f"  {name:14s}: {int((big|lab).sum())}/{len(m)} discrepant"
          + (f"  -> {hits}" if hits else ""), flush=True)

with open(os.path.join(OUT_DIR, "keio_o2_solver_integrity_audit.json"),
          "w") as f:
    json.dump(audit, f, indent=2)
print(f"\nTOTAL: {audit['total_discrepancies']} discrepancies in "
      f"{audit['total_gene_comparisons']} gene-level comparisons.")
print("AUDIT RECORD WRITTEN.")
