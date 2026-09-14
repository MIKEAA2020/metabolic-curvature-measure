#!/usr/bin/env python3
"""
GLUCOSE-ONLY RE-RUN OF THE CROSS-REBUILD KEIO STRESS TEST (E16).

Identical protocol to the deposited cross-rebuild study (E16) on iML1515,
with the trehalose exchange CLOSED (the deposited run left it open at
-10, effective uptake -6.4, giving WT 0.9259 vs a glucose-only optimum
of 0.8218).  Minerals remain at -10 as in the deposited run; the only
change is the medium.

Outputs (download/): keio_glucose_only_e16.csv / .txt / _results.json
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "download")
MOESM9 = os.path.join(REPO, "raw tomoya baba supp",
                      "44320_2006_BFMSB4100050_MOESM9_ESM.xls")
MOESM8 = os.path.join(REPO, "raw tomoya baba supp",
                      "44320_2006_BFMSB4100050_MOESM8_ESM.xls")

from cobra.io import load_json_model
from scipy.stats import spearmanr, pearsonr, pointbiserialr
from sklearn.metrics import (roc_auc_score, matthews_corrcoef, f1_score,
                             recall_score, confusion_matrix, precision_score)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

print("=" * 78)
print("GLUCOSE-ONLY RE-RUN: CROSS-REBUILD KEIO STRESS TEST (iML1515)")
print("  Medium: glucose -10, O2 -20, minerals -10, EX_tre_e CLOSED")
print("=" * 78)
model = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
n_genes = len(model.genes)
print(f"  {len(model.metabolites)} mets, {len(model.reactions)} rxns, {n_genes} genes")

for r in model.reactions:
    if r.id.startswith("EX_"):
        r.lower_bound = 0
model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
o2_set = False
for o2_id in ['EX_o2_e', 'EX_o2s_e']:
    try:
        model.reactions.get_by_id(o2_id).lower_bound = -20
        o2_set = True
        break
    except Exception:
        continue
if not o2_set:
    print("WARNING: no O2 exchange found; continuing anaerobic")
# Deposited E16 mineral list MINUS the trehalose exchange
for ex_id in ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
              'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
              'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
              'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']:
    try:
        model.reactions.get_by_id(ex_id).lower_bound = -10
    except Exception:
        pass
# EX_tre_e stays CLOSED (lower_bound = 0)  <-- the correction

# Wild-type
wt_sol = model.optimize()
assert wt_sol.status == "optimal"
b_wt = float(wt_sol.objective_value)
essential_threshold = 0.05 * b_wt
v_wt = np.array([wt_sol.fluxes.get(r.id, 0.0) for r in model.reactions])
print(f"\nWild-type glucose-only biomass = {b_wt:.6f} "
      f"(deposited trehalose-medium value: 0.925933)")
print(f"Essentiality threshold (5% of WT): < {essential_threshold:.6f}")

# Sweep
print(f"\nSingle-gene-deletion sweep over all {n_genes} iML1515 genes ...")
t_start = time.time()
results = []
for g in model.genes:
    g_id = g.id
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
        n_gpr = sum(1 for r in model.reactions if g_id in r.gene_reaction_rule)
        results.append({
            "gene_id": g_id, "n_gpr_rxns": n_gpr, "n_changed": int(mask.sum()),
            "b_wt": b_wt, "b_ko": b_ko, "delta_b": float(b_wt - b_ko),
            "y_essential": 1 if b_ko < essential_threshold else 0, "kV": kV,
        })
    except Exception:
        results.append({"gene_id": g_id, "n_gpr_rxns": 0, "n_changed": 0,
                        "b_wt": b_wt, "b_ko": float('nan'),
                        "delta_b": float('nan'), "y_essential": -1, "kV": 0.0})
    if len(results) % 300 == 0:
        el = time.time() - t_start
        print(f"    progress {len(results)}/{n_genes} ({el:.0f}s)")
results_ok = [r for r in results if r["y_essential"] >= 0]
n_ess = sum(1 for r in results_ok if r["y_essential"] == 1)
print(f"    done in {time.time()-t_start:.0f}s: {len(results_ok)}/{n_genes} OK; "
      f"essential {n_ess}/{len(results_ok)} = {100*n_ess/len(results_ok):.2f}%")
df_sweep = pd.DataFrame(results_ok)

# Merge against raw Keio
xl9 = pd.ExcelFile(MOESM9)
df9 = xl9.parse('Sup Table 7', header=None)
keio = df9.iloc[2:, [0, 1, 2, 3, 4, 5, 6]].copy()
keio.columns = ['keio_call', 'ECK', 'gene_name', 'JW', 'bnum', 'COG_id', 'COG_cat']
keio = keio[keio['keio_call'].isin(['E', 'N', 'u'])].copy()
keio['bnum'] = keio['bnum'].astype(str).str.strip()
keio = keio.drop_duplicates('bnum', keep='first')
xl8 = pd.ExcelFile(MOESM8)
df8 = xl8.parse('Sup Table 6', header=None)
st6 = df8.iloc[5:, [0, 1, 2, 6, 11, 12, 13]].copy()
st6.columns = ['ECK', 'gene_name', 'JW', 'bnum', 'PEC', 'MG_Tn5', 'Score']
st6 = st6.dropna(subset=['ECK'])
st6['bnum'] = st6['bnum'].astype(str).str.strip()
st6 = st6.drop_duplicates('bnum', keep='first')

df_sweep['gene_id_str'] = df_sweep['gene_id'].astype(str).str.strip()
merged = df_sweep.merge(keio[['bnum', 'keio_call', 'gene_name', 'COG_id']],
                        left_on='gene_id_str', right_on='bnum', how='inner')
merged = merged.merge(st6[['bnum', 'PEC', 'MG_Tn5', 'Score']],
                      on='bnum', how='left')
merged = merged.rename(columns={'gene_name': 'gene_name_keio'})
n_merged = len(merged)
n_keio_E = int((merged['keio_call'] == 'E').sum())
print(f"\nmerged n = {n_merged} ({100*n_merged/n_genes:.1f}% coverage); "
      f"E={n_keio_E}")
ct = pd.crosstab(merged['keio_call'], merged['y_essential'])
print("raw Keio call x in-silico essential (iML1515 glucose-only):")
print(ct.to_string())

bin_df = merged[merged['keio_call'].isin(['E', 'N'])].copy()
bin_df['keio_E'] = (bin_df['keio_call'] == 'E').astype(int)
bin_df['log10_kV'] = np.log10(bin_df['kV'].clip(lower=1.0))
n = len(bin_df); nE = int(bin_df['keio_E'].sum())
print(f"binary subset: n={n} (E={nE}, N={n-nE}, base rate {nE/n:.4f})")

x = bin_df['log10_kV'].values
y = bin_df['keio_E'].values
r_p, p_p = pearsonr(x, y)
r_s, p_s = spearmanr(x, y)
r_pb, p_pb = pointbiserialr(x, y)
rng = np.random.default_rng(20260830)
boot_rs = []
for _ in range(2000):
    idx = rng.integers(0, n, n)
    if len(np.unique(y[idx])) < 2:
        continue
    r_b, _ = pearsonr(x[idx], y[idx])
    boot_rs.append(r_b)
boot_rs = np.array(boot_rs)
ci_lo, ci_hi = np.percentile(boot_rs, [2.5, 97.5])
auc = float(roc_auc_score(y, x)) if len(np.unique(y)) == 2 else float('nan')
print(f"\nDIRECT (iML1515, glucose-only): Pearson r = {r_p:.4f} (p={p_p:.3e})")
print(f"  Spearman = {r_s:.4f} (p={p_s:.3e})")
print(f"  bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"  ROC AUC = {auc:.4f}")

X = x.reshape(-1, 1)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=20260830, stratify=y)
clf = LogisticRegression(class_weight='balanced', max_iter=200)
clf.fit(X_tr, y_tr)
y_pred = clf.predict(X_te)
y_prob = clf.predict_proba(X_te)[:, 1]
acc = float((y_pred == y_te).mean())
mcc = float(matthews_corrcoef(y_te, y_pred))
sens = float(recall_score(y_te, y_pred))
tn, fp, fn, tp = confusion_matrix(y_te, y_pred).ravel()
spec = tn / (tn + fp)
prec = float(precision_score(y_te, y_pred))
auc_te = float(roc_auc_score(y_te, y_prob))
print(f"Held-out 70/30: n_test={len(y_te)} (E={int(y_te.sum())})")
print(f"  acc={acc:.4f} sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}")
print(f"  MCC={mcc:.4f} ROC AUC={auc_te:.4f}")

model_gaps = merged[(merged['keio_call'] == 'E') & (merged['PEC'] == 'E') &
                    (merged['y_essential'] == 0)]
print(f"Model gaps (Keio=E, PEC=E, in-silico=N): {len(model_gaps)}")

csv_path = os.path.join(OUT_DIR, "keio_glucose_only_e16.csv")
merged.to_csv(csv_path, index=False)
sweep_path = os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv")
df_sweep.to_csv(sweep_path, index=False)
json_path = os.path.join(OUT_DIR, "keio_glucose_only_e16_results.json")
with open(json_path, "w") as f:
    json.dump({
        "task": "Glucose-only re-run of the cross-rebuild Keio stress test (E16 medium correction)",
        "model": "iML1515 (local BiGG JSON)",
        "medium": "glucose -10, O2 -20, minerals -10, EX_tre_e CLOSED",
        "wild_type_biomass": b_wt,
        "essential_threshold_5pct": float(essential_threshold),
        "n_genes_processed": len(results_ok),
        "n_essential_in_silico": int(n_ess),
        "n_merged": int(n_merged), "n_keio_E": int(n_keio_E),
        "binary_subset": {"n": int(n), "n_E": int(nE)},
        "direct_validation": {
            "pearson_r": float(r_p), "pearson_p": float(p_p),
            "spearman_rho": float(r_s), "spearman_p": float(p_s),
            "bootstrap_95ci": [float(ci_lo), float(ci_hi)],
            "roc_auc": auc,
        },
        "held_out_70_30": {
            "n_test": int(len(y_te)), "accuracy": acc,
            "sensitivity": sens, "specificity": float(spec),
            "precision": prec, "mcc": mcc, "roc_auc": auc_te,
            "confusion": {"tp": int(tp), "fp": int(fp),
                          "tn": int(tn), "fn": int(fn)},
        },
        "n_model_gaps_pecE_insilicoN": int(len(model_gaps)),
    }, f, indent=2)
txt_path = os.path.join(OUT_DIR, "keio_glucose_only_e16.txt")
with open(txt_path, "w") as f:
    f.write("GLUCOSE-ONLY RE-RUN: CROSS-REBUILD KEIO STRESS TEST (iML1515)\n")
    f.write("=" * 78 + "\n\n")
    f.write(f"Medium: glucose -10, O2 -20, minerals -10, EX_tre_e CLOSED\n")
    f.write(f"Wild-type biomass: {b_wt:.6f} (deposited medium gave 0.925933)\n")
    f.write(f"Genes processed: {len(results_ok)}; "
            f"essential in silico: {n_ess} ({100*n_ess/len(results_ok):.2f}%)\n")
    f.write(f"Merged to raw Keio: {n_merged} (E={n_keio_E}); binary n={n}\n\n")
    f.write("DIRECT VALIDATION:\n")
    f.write(f"  Pearson r = {r_p:+.4f} (p={p_p:.3e})\n")
    f.write(f"  Spearman rho = {r_s:+.4f} (p={p_s:.3e})\n")
    f.write(f"  bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]\n")
    f.write(f"  ROC AUC = {auc:.4f}\n\n")
    f.write("HELD-OUT 70/30:\n")
    f.write(f"  n_test={len(y_te)} (E={int(y_te.sum())}); acc={acc:.4f}\n")
    f.write(f"  sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}\n")
    f.write(f"  MCC={mcc:.4f} AUC={auc_te:.4f}\n")
    f.write(f"\nModel gaps (Keio=E, PEC=E, in-silico=N): {len(model_gaps)}\n")
print(f"\nWrote {csv_path}\n      {sweep_path}\n      {json_path}\n      {txt_path}")
