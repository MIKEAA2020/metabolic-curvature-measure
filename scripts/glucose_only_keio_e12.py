#!/usr/bin/env python3
"""
GLUCOSE-ONLY RE-RUN OF THE TRANSITIVE KEIO ANCHOR (E12 medium correction).

Background (the disclosed open item, rem:keio-medium-audit in the companion):
  The deposited transitive Keio anchor (E12) computed its wild-type optimum
  (15.444) under a medium whose re-opened "minerals" list accidentally
  included the trehalose exchange EX_tre_e at -1000 (effective uptake
  -337 mmol/gDW/h).  Closing the trehalose exchange alone gives
  0.98237 h^-1, the canonical iJO1366 glucose-minimal optimum.  This script
  re-executes the ENTIRE E12 protocol with EX_tre_e CLOSED (the only change:
  the medium), so the re-run is directly comparable to the deposited study:

    1. iJO1366 (local BiGG JSON), glucose -10, O2 -20, minerals -1000
       (E12's exact list MINUS EX_tre_e).
    2. Wild-type FBA (same solver convention as the deposited study).
    3. Single-gene-deletion sweep over all genes with GPR reactions;
       kappa^flux_V(g) = sum_r (v_r(KO) - v_r(WT))^2 over |dv| > 1e-6.
    4. Essentiality label y(g)=1 iff b_KO < 0.05 b_wt.
    5. Calibration (Pearson r(log kV, db), Spearman, partial r, bootstrap CI,
       seed 42), held-out 70/30 logistic regression (seed 42, stratified),
       precision@K.
    6. Label-flip comparison against the deposited E12 CSV.

Outputs (download/):
  keio_glucose_only_e12.csv / .txt / _results.json / .png
"""
import os, sys, json, csv, time, warnings
warnings.filterwarnings("ignore")
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")
os.makedirs(OUT_DIR, exist_ok=True)

from cobra.io import load_json_model
from scipy.stats import spearmanr, pearsonr, linregress
from sklearn.metrics import (
    roc_auc_score, roc_curve, matthews_corrcoef, f1_score,
    precision_score, recall_score, confusion_matrix,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ----------------------------------------------------------------------
# 1. Model + corrected (glucose-only) medium
# ----------------------------------------------------------------------
print("=" * 78)
print("GLUCOSE-ONLY RE-RUN OF THE TRANSITIVE KEIO ANCHOR (iJO1366)")
print("  Medium: glucose -10, O2 -20, minerals -1000, EX_tre_e CLOSED")
print("=" * 78)
model = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
print(f"  {len(model.metabolites)} mets, {len(model.reactions)} rxns, "
      f"{len(model.genes)} genes")

for r in model.exchanges:
    r.lower_bound = 0
model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
# E12's exact mineral list, MINUS the trehalose exchange
for ex_id in ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
              "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
              "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
              "EX_ni2_e", "EX_sel_e"]:
    if ex_id in [r.id for r in model.reactions]:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
# EX_tre_e stays CLOSED (lower_bound = 0)  <-- the correction

# ----------------------------------------------------------------------
# 2. Wild-type baseline
# ----------------------------------------------------------------------
wt_sol = model.optimize()
assert wt_sol.status == "optimal"
b_wt = wt_sol.objective_value
flux_wt = wt_sol.fluxes.to_dict()
print(f"\nWild-type glucose-only biomass = {b_wt:.6f} h^-1 "
      f"(deposited trehalose-medium value: 15.444242)")

# ----------------------------------------------------------------------
# 3. Single-gene-deletion sweep (identical protocol to the deposited E12)
# ----------------------------------------------------------------------
print(f"\nSingle-gene-deletion sweep over all genes (n = {len(model.genes)})...")
t0 = time.time()
results = []
for i, gene in enumerate(model.genes):
    gpr_rxns = [r for r in gene.reactions if gene in r.genes]
    if not gpr_rxns:
        continue
    with model:
        for r in gpr_rxns:
            r.lower_bound = 0
            r.upper_bound = 0
        try:
            sol = model.optimize()
        except Exception:
            sol = None
        if sol is None or sol.status != "optimal":
            b_ko = 0.0
            flux_ko_dict = {}
        else:
            b_ko = float(sol.objective_value)
            flux_ko_dict = sol.fluxes.to_dict()
    kV = 0.0
    n_changed = 0
    for r_id, v_wt in flux_wt.items():
        v_ko = flux_ko_dict.get(r_id, 0.0)
        dv = v_ko - v_wt
        if abs(dv) > 1e-6:
            kV += dv * dv
            n_changed += 1
    results.append({
        "gene_id": gene.id, "gene_name": gene.name,
        "n_gpr_rxns": len(gpr_rxns), "n_changed": n_changed,
        "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
        "y_essential": 1 if b_ko < 0.05 * b_wt else 0,
        "kV": kV,
    })
    if (i + 1) % 300 == 0:
        print(f"  progress {i+1}/{len(model.genes)} "
              f"({time.time()-t0:.0f}s)")
print(f"Done in {time.time()-t0:.0f}s. {len(results)} genes processed.")
n_essential = sum(1 for r in results if r["y_essential"] == 1)
print(f"  Essential (< {0.05*b_wt:.4f}): {n_essential}/{len(results)} = "
      f"{100*n_essential/len(results):.2f}%")

# ----------------------------------------------------------------------
# 4. Calibration
# ----------------------------------------------------------------------
kV_arr = np.array([r["kV"] for r in results])
db_arr = np.array([r["delta_b"] for r in results])
ess_arr = np.array([r["y_essential"] for r in results])
nrx_arr = np.array([r["n_gpr_rxns"] for r in results])
log_kV = np.log1p(kV_arr)
mask = np.isfinite(log_kV) & np.isfinite(db_arr)
log_kV_v = log_kV[mask]; db_v = db_arr[mask]
r_pear, p_pear = pearsonr(log_kV_v, db_v)
rho_spe, p_spe = spearmanr(kV_arr, db_arr)
slope_nrx, int_nrx, *_ = linregress(nrx_arr, db_arr)
resid_db = db_arr - (slope_nrx * nrx_arr + int_nrx)
slope_nrx_kV, int_nrx_kV, *_ = linregress(nrx_arr, log_kV)
resid_kV = log_kV - (slope_nrx_kV * nrx_arr + int_nrx_kV)
r_part, p_part = pearsonr(resid_kV, resid_db)
rng = np.random.default_rng(42)
boot_rs = []
for _ in range(1000):
    idx = rng.integers(0, len(log_kV_v), len(log_kV_v))
    if len(set(idx)) < 5:
        continue
    r_b, _ = pearsonr(log_kV_v[idx], db_v[idx])
    if np.isfinite(r_b):
        boot_rs.append(r_b)
boot_rs = np.array(boot_rs)
ci_lo, ci_hi = np.percentile(boot_rs, [2.5, 97.5])
print(f"\nCalibration: Pearson r(log kV, db) = {r_pear:+.4f} (p={p_pear:.2e})")
print(f"  Spearman = {rho_spe:+.4f} (p={p_spe:.2e}); "
      f"partial r = {r_part:+.4f} (p={p_part:.2e})")
print(f"  Bootstrap 95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")

# ----------------------------------------------------------------------
# 5. Held-out essentiality prediction (seed 42, stratified, as deposited)
# ----------------------------------------------------------------------
X = log_kV.reshape(-1, 1)
y = ess_arr
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y)
clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=200)
clf.fit(X_tr, y_tr)
y_pred = clf.predict(X_te)
y_proba = clf.predict_proba(X_te)[:, 1]
acc = float(np.mean(y_pred == y_te))
prec = precision_score(y_te, y_pred, zero_division=0)
rec = recall_score(y_te, y_pred, zero_division=0)
f1 = f1_score(y_te, y_pred, zero_division=0)
mcc = matthews_corrcoef(y_te, y_pred)
auc = roc_auc_score(y_te, y_proba)
tn, fp, fn, tp = confusion_matrix(y_te, y_pred, labels=[0, 1]).ravel()
sens = tp / (tp + fn) if (tp + fn) > 0 else 0.0
spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
print(f"\nHeld-out 70/30: n={len(y_te)} (essential {int(y_te.sum())})")
print(f"  acc={acc:.4f} sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}")
print(f"  F1={f1:.4f} MCC={mcc:.4f} ROC AUC={auc:.4f}")
print(f"  confusion (tn,fp,fn,tp) = ({tn},{fp},{fn},{tp})")

# ----------------------------------------------------------------------
# 6. Precision @ K
# ----------------------------------------------------------------------
order = np.argsort(-kV_arr)
pKs = {}
for K in [10, 25, 50, 100, 200, 500]:
    if K > len(order):
        continue
    topK = ess_arr[order[:K]]
    pK = float(topK.sum() / K)
    base_rate = float(ess_arr.sum() / len(ess_arr))
    pKs[f"K={K}"] = {"precision": pK, "base_rate": base_rate,
                     "lift": pK / base_rate if base_rate > 0 else None}
    print(f"  P@{K:4d} = {pK:.3f}  (base {base_rate:.3f})")

# ----------------------------------------------------------------------
# 7. Label-flip comparison vs the deposited E12 CSV
# ----------------------------------------------------------------------
old_csv = os.path.join(OUT_DIR, "novelty_keio_validation_e12.csv")
flips = None
if os.path.exists(old_csv):
    import pandas as pd
    old = pd.read_csv(old_csv)[["gene_id", "y_essential"]]
    new = pd.DataFrame(results)[["gene_id", "y_essential"]]
    mg = old.merge(new, on="gene_id", how="inner", suffixes=("_old", "_new"))
    n_both = int(((mg.y_essential_old == 1) & (mg.y_essential_new == 1)).sum())
    n_lose = int(((mg.y_essential_old == 1) & (mg.y_essential_new == 0)).sum())
    n_gain = int(((mg.y_essential_old == 0) & (mg.y_essential_new == 1)).sum())
    n_none = int(((mg.y_essential_old == 0) & (mg.y_essential_new == 0)).sum())
    flips = {"n_compared": int(len(mg)), "old_essential": int(old.y_essential.sum()),
             "new_essential": int(new.y_essential.sum()),
             "both_essential": n_both, "old_only": n_lose,
             "new_only": n_gain, "neither": n_none}
    print(f"\nLabel flips vs deposited (trehalose-medium) run: "
          f"old {flips['old_essential']} essential -> new {flips['new_essential']}; "
          f"+{n_gain}/-{n_lose} flips, {n_both} common")

# ----------------------------------------------------------------------
# 8. Artifacts
# ----------------------------------------------------------------------
csv_path = os.path.join(OUT_DIR, "keio_glucose_only_e12.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    for r in results:
        w.writerow(r)
json_path = os.path.join(OUT_DIR, "keio_glucose_only_e12_results.json")
with open(json_path, "w") as f:
    json.dump({
        "task": "Glucose-only re-run of the transitive Keio anchor (E12 medium correction)",
        "model": "iJO1366 (local BiGG JSON)",
        "medium": "glucose -10, O2 -20, minerals -1000, EX_tre_e CLOSED "
                  "(deposited E12 list minus trehalose)",
        "wild_type_biomass": float(b_wt),
        "essential_threshold_5pct_of_wt": float(0.05 * b_wt),
        "n_genes_processed": len(results),
        "n_essential": int(n_essential),
        "essential_fraction": float(n_essential / len(results)),
        "calibration": {
            "pearson_r_log_kV_delta_b": float(r_pear),
            "pearson_p_value": float(p_pear),
            "spearman_rho_kV_delta_b": float(rho_spe),
            "spearman_p_value": float(p_spe),
            "partial_r_given_n_gpr_rxns": float(r_part),
            "partial_p_value": float(p_part),
            "bootstrap_95ci_low": float(ci_lo),
            "bootstrap_95ci_high": float(ci_hi),
            "n_bootstrap_resamples": 1000,
        },
        "held_out_essentiality_prediction": {
            "test_size_fraction": 0.30, "n_test": int(len(y_te)),
            "n_test_essential": int(y_te.sum()),
            "accuracy": acc, "sensitivity": float(sens),
            "specificity": float(spec), "precision": float(prec),
            "f1": float(f1), "mcc": float(mcc), "roc_auc": float(auc),
            "confusion_matrix": {"tn": int(tn), "fp": int(fp),
                                 "fn": int(fn), "tp": int(tp)},
        },
        "precision_at_k": pKs,
        "label_flip_comparison_vs_deposited": flips,
    }, f, indent=2)
txt_path = os.path.join(OUT_DIR, "keio_glucose_only_e12.txt")
with open(txt_path, "w") as f:
    f.write("GLUCOSE-ONLY RE-RUN OF THE TRANSITIVE KEIO ANCHOR (E12 correction)\n")
    f.write("=" * 78 + "\n\n")
    f.write("Medium: glucose -10, O2 -20, minerals -1000, EX_tre_e CLOSED\n")
    f.write(f"Wild-type biomass: {b_wt:.6f} h^-1 (deposited medium gave 15.444242)\n")
    f.write(f"Genes processed: {len(results)}\n")
    f.write(f"Essential (< 5% WT = {0.05*b_wt:.4f}): {n_essential} "
            f"({100*n_essential/len(results):.2f}%)\n\n")
    f.write("CALIBRATION:\n")
    f.write(f"  Pearson  r(log kV, db) = {r_pear:+.4f}  (p={p_pear:.2e})\n")
    f.write(f"  Spearman rho            = {rho_spe:+.4f}  (p={p_spe:.2e})\n")
    f.write(f"  Partial r | n_gpr_rxns  = {r_part:+.4f}  (p={p_part:.2e})\n")
    f.write(f"  Bootstrap 95% CI        = [{ci_lo:+.4f}, {ci_hi:+.4f}]\n\n")
    f.write("HELD-OUT 70/30 ESSENTIALITY:\n")
    f.write(f"  n_test = {len(y_te)} (essential {int(y_te.sum())})\n")
    f.write(f"  acc={acc:.4f} sens={sens:.4f} spec={spec:.4f} prec={prec:.4f}\n")
    f.write(f"  F1={f1:.4f} MCC={mcc:.4f} ROC AUC={auc:.4f}\n")
    f.write(f"  confusion (tn,fp,fn,tp)=({tn},{fp},{fn},{tp})\n\n")
    f.write("PRECISION @ K:\n")
    for k, v in pKs.items():
        f.write(f"  {k}: {v['precision']:.3f} (base {v['base_rate']:.3f})\n")
    if flips:
        f.write("\nLABEL FLIPS vs DEPOSITED (trehalose-medium) RUN:\n")
        f.write(f"  old essential {flips['old_essential']} -> new {flips['new_essential']}; "
                f"+{flips['new_only']} / -{flips['old_only']}; "
                f"{flips['both_essential']} common essential\n")
print(f"\nWrote {csv_path}\n      {json_path}\n      {txt_path}")

# ----------------------------------------------------------------------
# 9. Figure: old vs new (ROC + calibration)
# ----------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for _fp in ['/usr/share/fonts/truetype/chinese/NotoSansSC[wght].ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
    try:
        fm.fontManager.addfont(_fp)
    except Exception:
        pass
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.5, 5), constrained_layout=True)
fpr, tpr, _ = roc_curve(y_te, y_proba)
axA.plot(fpr, tpr, 'b-', lw=2, label=f"glucose-only (AUC {auc:.3f})")
# True deposited-medium ROC, recomputed from the deposited E12 CSV
old_csv_p = os.path.join(OUT_DIR, "novelty_keio_validation_e12.csv")
if os.path.exists(old_csv_p):
    import pandas as pd
    old = pd.read_csv(old_csv_p)
    ok = old[np.isfinite(old["kV"]) & np.isfinite(old["delta_b"])]
    Xo = np.log1p(ok["kV"].values).reshape(-1, 1)
    yo = ok["y_essential"].values.astype(int)
    Xo_tr, Xo_te, yo_tr, yo_te = train_test_split(
        Xo, yo, test_size=0.30, random_state=42, stratify=yo)
    clfo = LogisticRegression(C=1.0, solver="lbfgs", max_iter=200)
    clfo.fit(Xo_tr, yo_tr)
    yo_prob = clfo.predict_proba(Xo_te)[:, 1]
    auc_o = roc_auc_score(yo_te, yo_prob)
    fpro, tpro, _ = roc_curve(yo_te, yo_prob)
    axA.plot(fpro, tpro, 'r--', lw=1.6, alpha=0.8,
             label=f"trehalose medium, deposited (AUC {auc_o:.3f})")
axA.plot([0, 1], [0, 1], 'k:', lw=1, label="chance")
axA.set_xlabel("False positive rate")
axA.set_ylabel("True positive rate")
axA.set_title(f"(a) ROC, held-out 30% (n={len(y_te)})")
axA.legend(loc="lower right", fontsize=9)
axA.grid(alpha=0.3)

axB.scatter(log_kV, db_arr, s=8, alpha=0.35, c="steelblue")
slope, intercept = np.polyfit(log_kV, db_arr, 1)
xs = np.linspace(log_kV.min(), log_kV.max(), 100)
axB.plot(xs, slope * xs + intercept, 'r-', lw=2,
         label=f"r={r_pear:+.3f}, p={p_pear:.1e}")
axB.set_xlabel(r"$\log(1+\kappa^{\mathrm{flux}}_V)$")
axB.set_ylabel(r"$\Delta b$  [h$^{-1}$]")
axB.set_title("(b) Calibration, glucose-only")
axB.legend(loc="lower right", fontsize=9)
axB.grid(alpha=0.3)
fig.suptitle("Glucose-only re-run of the transitive Keio anchor (iJO1366, "
             f"n={len(results)}; WT {b_wt:.3f} h$^{{-1}}$)", fontsize=12,
             fontweight="bold")
png_path = os.path.join(OUT_DIR, "keio_glucose_only_e12.png")
plt.savefig(png_path, dpi=120)
plt.close()
print(f"      {png_path}")
print("\nGLUCOSE-ONLY E12 RE-RUN DONE.")
