#!/usr/bin/env python3
"""
GLUCOSE-ONLY RE-RUN OF THE DIRECT PRIMARY-SOURCE KEIO VALIDATION (E15).

Identical protocol to the deposited direct validation (E15), but reading
the glucose-only kappa^flux_V values (keio_glucose_only_e12.csv) instead
of the trehalose-medium values.  Everything else -- raw Baba 2006
Supplementary Tables 6/7 parsing, b-number matching, seeds, metrics --
is unchanged, so the two runs are directly comparable.

Outputs (download/): keio_glucose_only_e15.csv / .txt / _results.json
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
E12_CSV = os.path.join(OUT_DIR, "keio_glucose_only_e12.csv")

from scipy.stats import spearmanr, pearsonr, pointbiserialr
from sklearn.metrics import (roc_auc_score, matthews_corrcoef, f1_score,
                             recall_score, confusion_matrix, precision_score)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

print("=" * 78)
print("GLUCOSE-ONLY RE-RUN: DIRECT kV vs RAW Baba 2006 KEIO ESSENTIALITY")
print("=" * 78)

# 1. Raw Keio Sup Table 7
xl9 = pd.ExcelFile(MOESM9)
df9 = xl9.parse('Sup Table 7', header=None)
keio = df9.iloc[2:, [0, 1, 2, 3, 4, 5, 6]].copy()
keio.columns = ['keio_call', 'ECK', 'gene_name', 'JW', 'bnum', 'COG_id', 'COG_cat']
keio = keio[keio['keio_call'].isin(['E', 'N', 'u'])].copy()
keio['bnum'] = keio['bnum'].astype(str).str.strip()
keio = keio.drop_duplicates('bnum', keep='first')
print(f"Keio Sup Table 7 (dedup): {len(keio)} unique bnums")

# 2. Sup Table 6 (PEC cross-validation)
xl8 = pd.ExcelFile(MOESM8)
df8 = xl8.parse('Sup Table 6', header=None)
st6 = df8.iloc[5:, [0, 1, 2, 6, 11, 12, 13]].copy()
st6.columns = ['ECK', 'gene_name', 'JW', 'bnum', 'PEC', 'MG_Tn5', 'Score']
st6 = st6.dropna(subset=['ECK'])
st6['bnum'] = st6['bnum'].astype(str).str.strip()
st6 = st6.drop_duplicates('bnum', keep='first')

# 3. Glucose-only kappa values
e12 = pd.read_csv(E12_CSV)
e12['gene_id_str'] = e12['gene_id'].astype(str).str.strip()
print(f"Glucose-only sweep genes: {len(e12)}; "
      f"in-silico essential (5%): {int(e12['y_essential'].sum())}")

# 4. Merge
e12_no_gname = e12.drop(columns=['gene_name'], errors='ignore')
merged = e12_no_gname.merge(keio[['bnum', 'keio_call', 'gene_name', 'COG_id']],
                            left_on='gene_id_str', right_on='bnum', how='inner')
merged = merged.merge(st6[['bnum', 'PEC', 'MG_Tn5', 'Score']],
                      on='bnum', how='left')
merged = merged.rename(columns={'gene_name': 'gene_name_keio'})
n_merged = len(merged)
n_keio_E = int((merged['keio_call'] == 'E').sum())
n_keio_N = int((merged['keio_call'] == 'N').sum())
n_keio_u = int((merged['keio_call'] == 'u').sum())
print(f"merged n = {n_merged} ({100*n_merged/len(e12):.1f}% coverage); "
      f"E={n_keio_E} N={n_keio_N} u={n_keio_u}")
ct = pd.crosstab(merged['keio_call'], merged['y_essential'])
print("raw Keio call x in-silico essential (glucose-only):")
print(ct.to_string())

bin_df = merged[merged['keio_call'].isin(['E', 'N'])].copy()
bin_df['keio_E'] = (bin_df['keio_call'] == 'E').astype(int)
bin_df['log10_kV'] = np.log10(bin_df['kV'].clip(lower=1.0))
n = len(bin_df); nE = int(bin_df['keio_E'].sum())
print(f"binary subset: n={n} (E={nE}, N={n-nE}, base rate {nE/n:.4f})")

# 5. Direct validation
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
auc = roc_auc_score(y, x)
print(f"\nDIRECT: Pearson r = {r_p:.4f} (p={p_p:.3e})")
print(f"  Spearman = {r_s:.4f} (p={p_s:.3e}); point-biserial = {r_pb:.4f}")
print(f"  bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"  ROC AUC = {auc:.4f}")

# 6. Held-out logistic
X = x.reshape(-1, 1)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=20260830, stratify=y)
clf = LogisticRegression(class_weight='balanced', max_iter=200)
clf.fit(X_tr, y_tr)
y_pred = clf.predict(X_te)
y_prob = clf.predict_proba(X_te)[:, 1]
acc = float((y_pred == y_te).mean())
mcc = float(matthews_corrcoef(y_te, y_pred))
f1 = float(f1_score(y_te, y_pred))
sens = float(recall_score(y_te, y_pred))
tn, fp, fn, tp = confusion_matrix(y_te, y_pred).ravel()
spec = tn / (tn + fp)
prec = float(precision_score(y_te, y_pred))
auc_te = float(roc_auc_score(y_te, y_prob))
print(f"\nHeld-out 70/30: n_train={len(y_tr)} (E={int(y_tr.sum())}); "
      f"n_test={len(y_te)} (E={int(y_te.sum())})")
print(f"  acc={acc:.4f} sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}")
print(f"  F1={f1:.4f} MCC={mcc:.4f} ROC AUC={auc_te:.4f}")
print(f"  confusion: TP={tp} FP={fp} TN={tn} FN={fn}")

# 7. P@K
sorted_df = bin_df.sort_values('kV', ascending=False).reset_index(drop=True)
base_rate = nE / n
pKs = {}
for K in [10, 25, 50, 100, 200, 500]:
    if K > n:
        continue
    top = sorted_df.head(K)
    prec_K = float((top['keio_call'] == 'E').mean())
    pKs[f"K={K}"] = {"precision": prec_K, "base_rate": float(base_rate),
                     "lift": prec_K / base_rate,
                     "n_top_with_keio_E": int((top['keio_call'] == 'E').sum())}
    print(f"  P@{K:4d} = {prec_K:.4f}  (lift {prec_K/base_rate:.2f}x)")

# 8. PEC stratification
hi_conf_E = bin_df[(bin_df['keio_call'] == 'E') & (bin_df['PEC'] == 'E')]
lo_conf_E = bin_df[(bin_df['keio_call'] == 'E') & (bin_df['PEC'] == 'N')]
keio_N_df = bin_df[bin_df['keio_call'] == 'N']
print(f"\nPEC stratification: high-conf (E,E) n={len(hi_conf_E)}; "
      f"low-conf (E,N) n={len(lo_conf_E)}; Keio=N n={len(keio_N_df)}")
strat = {}
if len(hi_conf_E) >= 5 and len(keio_N_df) >= 5:
    x_s = np.concatenate([np.log10(hi_conf_E['kV'].clip(lower=1.0).values),
                          np.log10(keio_N_df['kV'].clip(lower=1.0).values)])
    y_s = np.concatenate([np.ones(len(hi_conf_E)), np.zeros(len(keio_N_df))])
    strat["high_conf_auc"] = float(roc_auc_score(y_s, x_s))
    print(f"  HIGH-CONF vs N: AUC = {strat['high_conf_auc']:.4f}")
if len(lo_conf_E) >= 5 and len(keio_N_df) >= 5:
    x_s2 = np.concatenate([np.log10(lo_conf_E['kV'].clip(lower=1.0).values),
                           np.log10(keio_N_df['kV'].clip(lower=1.0).values)])
    y_s2 = np.concatenate([np.ones(len(lo_conf_E)), np.zeros(len(keio_N_df))])
    strat["low_conf_auc"] = float(roc_auc_score(y_s2, x_s2))
    print(f"  LOW-CONF vs N:  AUC = {strat['low_conf_auc']:.4f}")

# 9. Model gaps (Keio=E AND PEC=E AND in-silico=N)
model_gaps = merged[(merged['keio_call'] == 'E') & (merged['PEC'] == 'E') &
                    (merged['y_essential'] == 0)]
print(f"\nModel gaps (Keio=E, PEC=E, in-silico=N): {len(model_gaps)}")

# 10. Artifacts
csv_path = os.path.join(OUT_DIR, "keio_glucose_only_e15.csv")
merged.to_csv(csv_path, index=False)
json_path = os.path.join(OUT_DIR, "keio_glucose_only_e15_results.json")
with open(json_path, "w") as f:
    json.dump({
        "task": "Glucose-only re-run of the direct Keio validation (E15 medium correction)",
        "kappa_source": "keio_glucose_only_e12.csv (EX_tre_e CLOSED)",
        "n_merged": int(n_merged), "n_keio_E": n_keio_E,
        "n_keio_N": n_keio_N, "n_keio_u": n_keio_u,
        "binary_subset": {"n": int(n), "n_E": int(nE),
                          "base_rate": float(nE / n)},
        "direct_validation": {
            "pearson_r": float(r_p), "pearson_p": float(p_p),
            "spearman_rho": float(r_s), "spearman_p": float(p_s),
            "point_biserial_r": float(r_pb), "point_biserial_p": float(p_pb),
            "bootstrap_95ci": [float(ci_lo), float(ci_hi)],
            "roc_auc": float(auc),
        },
        "held_out_70_30": {
            "n_test": int(len(y_te)), "n_test_E": int(y_te.sum()),
            "accuracy": acc, "sensitivity": sens, "specificity": float(spec),
            "precision": prec, "f1": f1, "mcc": mcc, "roc_auc": auc_te,
            "confusion": {"tp": int(tp), "fp": int(fp),
                          "tn": int(tn), "fn": int(fn)},
        },
        "precision_at_k": pKs,
        "pec_stratification": {
            "n_high_conf": int(len(hi_conf_E)),
            "n_low_conf": int(len(lo_conf_E)), **strat,
        },
        "n_model_gaps_pecE_insilicoN": int(len(model_gaps)),
    }, f, indent=2)
txt_path = os.path.join(OUT_DIR, "keio_glucose_only_e15.txt")
with open(txt_path, "w") as f:
    f.write("GLUCOSE-ONLY RE-RUN: DIRECT kV vs RAW Baba 2006 KEIO\n")
    f.write("=" * 78 + "\n\n")
    f.write(f"kappa source: keio_glucose_only_e12.csv (EX_tre_e CLOSED)\n")
    f.write(f"merged n = {n_merged}; binary n = {n} (E={nE}, N={n-nE})\n\n")
    f.write("DIRECT VALIDATION:\n")
    f.write(f"  Pearson r = {r_p:+.4f} (p={p_p:.3e})\n")
    f.write(f"  Spearman rho = {r_s:+.4f} (p={p_s:.3e})\n")
    f.write(f"  bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]\n")
    f.write(f"  ROC AUC = {auc:.4f}\n\n")
    f.write("HELD-OUT 70/30:\n")
    f.write(f"  n_test={len(y_te)} (E={int(y_te.sum())}); acc={acc:.4f}\n")
    f.write(f"  sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}\n")
    f.write(f"  F1={f1:.4f} MCC={mcc:.4f} AUC={auc_te:.4f}\n\n")
    f.write("P@K:\n")
    for k, v in pKs.items():
        f.write(f"  {k}: {v['precision']:.4f} (lift {v['lift']:.2f}x)\n")
    f.write(f"\nPEC stratification: high-conf n={len(hi_conf_E)}, "
            f"low-conf n={len(lo_conf_E)}\n")
    if "high_conf_auc" in strat:
        f.write(f"  high-conf AUC = {strat['high_conf_auc']:.4f}\n")
    if "low_conf_auc" in strat:
        f.write(f"  low-conf AUC = {strat['low_conf_auc']:.4f}\n")
    f.write(f"\nModel gaps (Keio=E, PEC=E, in-silico=N): {len(model_gaps)}\n")
print(f"\nWrote {csv_path}\n      {json_path}\n      {txt_path}")
