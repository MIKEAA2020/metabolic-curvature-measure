#!/usr/bin/env python3
"""
THIRD PERTURBATION AXIS: NITROGEN SOURCE (label-invariance
generalization beyond the carbon and electron-acceptor axes).

Background.  The glucose-only re-run (prop:keio-glucose-only) showed
that correcting the carbon axis leaves both in-silico essentiality
label sets IDENTICAL while every rank-level association strengthens.
The oxygen probe (prop:keio-o2-limited) showed the same invariance
along the electron-acceptor axis (limitation dose response), with
re-stratification only at the anaerobic regime switch.  Both probes
leave the nitrogen supply untouched (ammonium unlimited on iJO1366,
ammonium -10 on iML1515).  This script runs the THIRD probe on the
nitrogen axis, in two complementary forms:

  (a) AMMONIUM-LIMITATION GRADIENT (supply perturbation, the direct
      analog of the oxygen dose response):
        iJO1366  EX_nh4_e in {-10, -5, -2.5}   (baseline: unlimited)
        iML1515  EX_nh4_e = -2.5               (baseline: -10)
  (b) NITROGEN-SOURCE SUBSTITUTION (identity perturbation, a form the
      first two axes did not test): ammonium closed, the sole N
      source replaced by
        L-glutamate  EX_glu__L_e = -10  (1 N per molecule: the N
          flux is stoichiometrically MATCHED to the nh4 -10 level,
          giving an exactly matched-N control), or
        L-arginine   EX_arg__L_e = -10  (4 N per molecule + carbon
          co-substrate: N-surplus/enrichment regime, iJO WT 1.260
          ABOVE the glucose-minimal baseline 0.982),
      on both models.

Design.
  Baseline: the glucose-only medium (glucose -10, O2 -20, minerals,
  EX_tre_e CLOSED) -- the live corrected medium of the companion.
  Per level (identical protocol/conventions to the glucose-only and
  oxygen rounds, so directly comparable):
    1. WT FBA (biomass; N-source uptake; nitrogen-route fluxes
       GLUDx/GLUDy/GLNS/GLUSy; internal nh4-release routes at the
       optimum for the substitution levels).
    2. Single-gene-deletion sweep over all genes (E12/E16
       conventions); kappa^flux_V(g); labels at 5% of THAT level's
       WT (relative, scale-free threshold).
    3. Label-flip comparison vs the glucose-only baseline
       (gains/losses, gene identities, Cohen kappa, Jaccard) and
       subsystem enrichment of the flip set.
    4. Transitive calibration (Pearson/Spearman/partial, bootstrap
       CI seed 42) + held-out 70/30 logistic (seed 42, stratified)
       + P@K -- E12 conventions; direct arm (seed 20260830) -- E15
       conventions; cross-rebuild arm on iML1515 -- E16 conventions.

Artifacts (download/):
  keio_nitrogen_source_e12_sweep.csv / _results.json (iJO1366, 5 lv)
  keio_nitrogen_source_e16_sweep.csv / _results.json (iML1515, 3 lv)
  keio_nitrogen_source_summary.txt
  keio_nitrogen_source_response.png
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
from scipy.stats import spearmanr, pearsonr, linregress, pointbiserialr
from sklearn.metrics import (roc_auc_score, roc_curve, matthews_corrcoef,
                             f1_score, recall_score, confusion_matrix,
                             precision_score, cohen_kappa_score)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------
# Probe levels.  Each level: ammonium bound + optional sole-N-source
# exchange replacing ammonium entirely (nh4 closed).
# ---------------------------------------------------------------------
IJO_LEVELS = [
    {"key": "nh4_-10", "kind": "limitation", "nh4_lb": -10.0,
     "n_source": None, "n_lb": None,
     "label": "NH4 -10 (mild limitation)"},
    {"key": "nh4_-5", "kind": "limitation", "nh4_lb": -5.0,
     "n_source": None, "n_lb": None,
     "label": "NH4 -5 (limitation)"},
    {"key": "nh4_-2.5", "kind": "limitation", "nh4_lb": -2.5,
     "n_source": None, "n_lb": None,
     "label": "NH4 -2.5 (severe limitation)"},
    {"key": "glu_-10", "kind": "substitution", "nh4_lb": 0.0,
     "n_source": "EX_glu__L_e", "n_lb": -10.0,
     "label": "Glu -10 sole-N (matched N flux)"},
    {"key": "arg_-10", "kind": "substitution", "nh4_lb": 0.0,
     "n_source": "EX_arg__L_e", "n_lb": -10.0,
     "label": "Arg -10 sole-N (N+C surplus)"},
]
IML_LEVELS = [
    {"key": "nh4_-2.5", "kind": "limitation", "nh4_lb": -2.5,
     "n_source": None, "n_lb": None,
     "label": "NH4 -2.5 (severe limitation)"},
    {"key": "glu_-10", "kind": "substitution", "nh4_lb": 0.0,
     "n_source": "EX_glu__L_e", "n_lb": -10.0,
     "label": "Glu -10 sole-N (matched N flux)"},
    {"key": "arg_-10", "kind": "substitution", "nh4_lb": 0.0,
     "n_source": "EX_arg__L_e", "n_lb": -10.0,
     "label": "Arg -10 sole-N (N+C surplus)"},
]

IJO_MINERALS = ["EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
N_TRACK = ["GLUDx", "GLUDy", "GLNS", "GLUSy", "ASPtpp", "ASPTA",
           "ARGDC", "ASTt2pp"]


def set_ijo_medium(model, lv):
    """Glucose-only corrected medium with the N axis at the probe level."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("EX_nh4_e").lower_bound = lv["nh4_lb"]
    if lv["n_source"]:
        model.reactions.get_by_id(lv["n_source"]).lower_bound = lv["n_lb"]
    # EX_tre_e stays CLOSED (glucose-only correction retained)


def set_iml_medium(model, lv):
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
    model.reactions.get_by_id("EX_nh4_e").lower_bound = lv["nh4_lb"]
    if lv["n_source"]:
        try:
            model.reactions.get_by_id(lv["n_source"]).lower_bound = lv["n_lb"]
        except Exception:
            print(f"  !! iML1515 lacks {lv['n_source']}")
    # EX_tre_e stays CLOSED


def nh4_release_routes(model, sol):
    """Reactions producing cytosolic nh4 at the optimum (for the
    substitution levels: where does nitrogen enter as ammonia?)."""
    routes = []
    try:
        nh4 = model.metabolites.get_by_id("nh4_c")
    except Exception:
        return routes
    for r in nh4.reactions:
        c = r.metabolites.get(nh4)
        try:
            v = float(sol.fluxes.get(r.id, 0.0))
        except Exception:
            v = 0.0
        prod = c * v  # signed net production rate of nh4_c through r
        if prod > 1e-6:
            gprs = ";".join(sorted({g.name or g.id for g in r.genes})) or \
                   "(no GPR)"
            routes.append({"reaction": r.id, "net_production": round(prod, 4),
                           "genes": gprs})
    routes.sort(key=lambda d: -d["net_production"])
    return routes


def keio_tables():
    xl9 = pd.ExcelFile(MOESM9)
    df9 = xl9.parse('Sup Table 7', header=None)
    keio = df9.iloc[2:, [0, 1, 2, 3, 4, 5, 6]].copy()
    keio.columns = ['keio_call', 'ECK', 'gene_name', 'JW', 'bnum',
                    'COG_id', 'COG_cat']
    keio = keio[keio['keio_call'].isin(['E', 'N', 'u'])].copy()
    keio['bnum'] = keio['bnum'].astype(str).str.strip()
    keio = keio.drop_duplicates('bnum', keep='first')
    xl8 = pd.ExcelFile(MOESM8)
    df8 = xl8.parse('Sup Table 6', header=None)
    st6 = df8.iloc[5:, [0, 1, 2, 6, 11, 12, 13]].copy()
    st6.columns = ['ECK', 'gene_name', 'JW', 'bnum', 'PEC', 'MG_Tn5',
                   'Score']
    st6 = st6.dropna(subset=['ECK'])
    st6['bnum'] = st6['bnum'].astype(str).str.strip()
    st6 = st6.drop_duplicates('bnum', keep='first')
    return keio, st6


def ko_sweep_ijo(model, b_wt, flux_wt):
    """E12-convention sweep on an already-configured iJO1366 model."""
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
            dv = flux_ko_dict.get(r_id, 0.0) - v_wt
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


def transitive_calibration(df):
    """E12-convention calibration block (seeds 42)."""
    kV_arr = df["kV"].values
    db_arr = df["delta_b"].values
    ess_arr = df["y_essential"].values.astype(int)
    nrx_arr = df["n_gpr_rxns"].values
    log_kV = np.log1p(kV_arr)
    mask = np.isfinite(log_kV) & np.isfinite(db_arr)
    log_kV_v = log_kV[mask]
    db_v = db_arr[mask]
    r_pear, p_pear = pearsonr(log_kV_v, db_v)
    rho_spe, p_spe = spearmanr(kV_arr, db_arr)
    slope_nrx, int_nrx, *_ = linregress(nrx_arr, db_arr)
    resid_db = db_arr - (slope_nrx * nrx_arr + int_nrx)
    slope2, int2, *_ = linregress(nrx_arr, log_kV)
    resid_kV = log_kV - (slope2 * nrx_arr + int2)
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
    X = log_kV.reshape(-1, 1)
    y = ess_arr
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y)
    clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=200)
    clf.fit(X_tr, y_tr)
    y_pred = clf.predict(X_te)
    y_proba = clf.predict_proba(X_te)[:, 1]
    acc = float(np.mean(y_pred == y_te))
    mcc = matthews_corrcoef(y_te, y_pred)
    auc = roc_auc_score(y_te, y_proba)
    tn, fp, fn, tp = confusion_matrix(y_te, y_pred, labels=[0, 1]).ravel()
    order = np.argsort(-kV_arr)
    pKs = {}
    for K in [10, 25, 50, 100, 200, 500]:
        if K > len(order):
            continue
        topK = ess_arr[order[:K]]
        pK = float(topK.sum() / K)
        base = float(ess_arr.sum() / len(ess_arr))
        pKs[f"K={K}"] = {"precision": pK, "base_rate": base,
                         "lift": pK / base if base > 0 else None}
    return {
        "pearson_r_log_kV_delta_b": float(r_pear),
        "pearson_p_value": float(p_pear),
        "spearman_rho": float(rho_spe), "spearman_p_value": float(p_spe),
        "partial_r_given_n_gpr_rxns": float(r_part),
        "partial_p_value": float(p_part),
        "bootstrap_95ci": [float(ci_lo), float(ci_hi)],
        "n_essential": int(ess_arr.sum()), "n_genes": int(len(df)),
        "held_out": {"n_test": int(len(y_te)),
                     "n_test_essential": int(y_te.sum()),
                     "accuracy": acc, "mcc": float(mcc),
                     "roc_auc": float(auc),
                     "sensitivity": float(tp / (tp + fn)) if tp + fn else 0.0,
                     "specificity": float(tn / (tn + fp)) if tn + fp else 0.0,
                     "confusion": {"tn": int(tn), "fp": int(fp),
                                   "fn": int(fn), "tp": int(tp)}},
        "precision_at_k": pKs,
    }


def direct_arm(df, keio, st6):
    """E15-convention direct validation block (seed 20260830)."""
    d = df.copy()
    d['gene_id_str'] = d['gene_id'].astype(str).str.strip()
    d = d.drop(columns=[c for c in ['gene_name'] if c in d.columns])
    merged = d.merge(keio[['bnum', 'keio_call', 'gene_name', 'COG_id']],
                     left_on='gene_id_str', right_on='bnum', how='inner')
    merged = merged.merge(st6[['bnum', 'PEC', 'MG_Tn5', 'Score']],
                          on='bnum', how='left')
    merged = merged.rename(columns={'gene_name': 'gene_name_keio'})
    bin_df = merged[merged['keio_call'].isin(['E', 'N'])].copy()
    bin_df['keio_E'] = (bin_df['keio_call'] == 'E').astype(int)
    bin_df['log10_kV'] = np.log10(bin_df['kV'].clip(lower=1.0))
    n = len(bin_df)
    nE = int(bin_df['keio_E'].sum())
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
    X = x.reshape(-1, 1)
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.3, random_state=20260830, stratify=y)
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
    prec = float(precision_score(y_te, y_pred, zero_division=0))
    auc_te = float(roc_auc_score(y_te, y_prob))
    hi_conf_E = bin_df[(bin_df['keio_call'] == 'E') & (bin_df['PEC'] == 'E')]
    lo_conf_E = bin_df[(bin_df['keio_call'] == 'E') & (bin_df['PEC'] == 'N')]
    keio_N_df = bin_df[bin_df['keio_call'] == 'N']
    strat = {}
    if len(hi_conf_E) >= 5 and len(keio_N_df) >= 5:
        xs = np.concatenate([np.log10(hi_conf_E['kV'].clip(lower=1.0).values),
                             np.log10(keio_N_df['kV'].clip(lower=1.0).values)])
        ys = np.concatenate([np.ones(len(hi_conf_E)),
                             np.zeros(len(keio_N_df))])
        strat["high_conf_auc"] = float(roc_auc_score(ys, xs))
        strat["n_high_conf"] = int(len(hi_conf_E))
    if len(lo_conf_E) >= 5 and len(keio_N_df) >= 5:
        xs2 = np.concatenate([np.log10(lo_conf_E['kV'].clip(lower=1.0).values),
                              np.log10(keio_N_df['kV'].clip(lower=1.0).values)])
        ys2 = np.concatenate([np.ones(len(lo_conf_E)),
                              np.zeros(len(keio_N_df))])
        strat["low_conf_auc"] = float(roc_auc_score(ys2, xs2))
        strat["n_low_conf"] = int(len(lo_conf_E))
    model_gaps = merged[(merged['keio_call'] == 'E') &
                        (merged['PEC'] == 'E') & (merged['y_essential'] == 0)]
    mismatch = merged[(merged['y_essential'] == 1) & (merged['keio_call'] == 'N')]
    return {
        "n_merged": int(len(merged)), "binary_n": int(n),
        "binary_n_E": int(nE),
        "pearson_r": float(r_p), "pearson_p": float(p_p),
        "spearman_rho": float(r_s), "spearman_p": float(p_s),
        "point_biserial_r": float(r_pb),
        "bootstrap_95ci": [float(ci_lo), float(ci_hi)],
        "roc_auc": auc,
        "held_out": {"n_test": int(len(y_te)),
                     "n_test_E": int(y_te.sum()), "accuracy": acc,
                     "sensitivity": sens, "specificity": float(spec),
                     "precision": prec, "f1": f1, "mcc": mcc,
                     "roc_auc": auc_te,
                     "confusion": {"tp": int(tp), "fp": int(fp),
                                   "tn": int(tn), "fn": int(fn)}},
        "pec_stratification": strat,
        "n_model_gaps_pecE_insilicoN": int(len(model_gaps)),
        "n_medium_mismatch_insilicoE_keioN": int(len(mismatch)),
    }, merged


def flip_analysis(new_df, base_csv, model, label):
    """Label flips vs the glucose-only baseline + subsystem enrichment."""
    base = pd.read_csv(base_csv)[["gene_id", "y_essential"]]
    new_cols = ["gene_id", "y_essential"] + (
        ["gene_name"] if "gene_name" in new_df.columns else [])
    mg = base.merge(new_df[new_cols], on="gene_id", how="inner",
                    suffixes=("_base", "_new"))
    gain = mg[(mg.y_essential_base == 0) & (mg.y_essential_new == 1)]
    loss = mg[(mg.y_essential_base == 1) & (mg.y_essential_new == 0)]
    both = int(((mg.y_essential_base == 1) & (mg.y_essential_new == 1)).sum())
    kappa = cohen_kappa_score(mg.y_essential_base, mg.y_essential_new)
    s_new = set(mg[mg.y_essential_new == 1].gene_id)
    s_old = set(mg[mg.y_essential_base == 1].gene_id)
    jac = len(s_new & s_old) / len(s_new | s_old) if s_new | s_old else 1.0

    def gene_subsystems(gid):
        gs = set()
        try:
            gene = model.genes.get_by_id(gid)
            for r in gene.reactions:
                if r.subsystem:
                    gs.add(r.subsystem)
        except Exception:
            pass
        return gs

    flip_genes = list(gain.gene_id) + list(loss.gene_id)
    flip_sub = {}
    for g in flip_genes:
        for s in gene_subsystems(g):
            flip_sub[s] = flip_sub.get(s, 0) + 1
    all_genes_with_gpr = [g.id for g in model.genes if len(g.reactions) > 0]
    base_sub = {}
    for g in all_genes_with_gpr:
        for s in gene_subsystems(g):
            base_sub[s] = base_sub.get(s, 0) + 1
    n_flip, n_all = len(flip_genes), len(all_genes_with_gpr)
    enrich = []
    for s, c in flip_sub.items():
        exp = n_flip * base_sub.get(s, 0) / n_all
        enrich.append({"subsystem": s, "n_flip": c, "expected": round(exp, 1),
                       "ratio": round(c / exp, 2) if exp > 0 else None})
    enrich.sort(key=lambda d: -d["n_flip"])
    gains = [{"gene_id": r.gene_id,
              "gene_name": getattr(r, "gene_name", "")}
             for r in gain.itertuples()]
    losses = [{"gene_id": r.gene_id,
               "gene_name": getattr(r, "gene_name", "")}
              for r in loss.itertuples()]
    return {
        "label": label, "n_compared": int(len(mg)),
        "n_essential_base": int(base.y_essential.sum()),
        "n_essential_new": int(new_df.y_essential.sum()),
        "n_gain_essential": int(len(gain)),
        "n_loss_essential": int(len(loss)),
        "n_both_essential": both,
        "cohen_kappa": float(kappa), "jaccard": float(jac),
        "gains": gains, "losses": losses,
        "subsystem_enrichment_top": enrich[:12],
    }, mg


BYPRODUCTS = ["EX_etoh_e", "EX_lac__D_e", "EX_for_e", "EX_succ_e",
              "EX_ac_e"]


def wt_block(model, lv):
    """WT FBA + nitrogen-route bookkeeping for one level."""
    wt = model.optimize()
    assert wt.status == "optimal" and wt.objective_value > 1e-9, \
        f"WT infeasible at {lv['key']}"
    b_wt = float(wt.objective_value)
    flux_wt = wt.fluxes.to_dict()
    ups = {}
    for ex in ["EX_nh4_e", "EX_glu__L_e", "EX_arg__L_e"]:
        v = flux_wt.get(ex, 0.0)
        if v < -1e-6:
            ups[ex] = round(-v, 3)
    byp = {r: round(float(flux_wt.get(r, 0.0)), 3) for r in BYPRODUCTS
           if abs(flux_wt.get(r, 0.0)) > 1e-6}
    glc_up = round(-float(flux_wt.get("EX_glc__D_e", 0.0)), 3)
    n_routes = {rid: round(float(flux_wt.get(rid, 0.0)), 3)
                for rid in N_TRACK if abs(flux_wt.get(rid, 0.0)) > 1e-6}
    nh4_rel = nh4_release_routes(model, wt) if lv["kind"] == "substitution" \
        else []
    return b_wt, flux_wt, {"uptakes": ups, "glucose_uptake": glc_up,
                           "byproducts": byp,
                           "n_route_fluxes": n_routes,
                           "nh4_release_routes": nh4_rel[:10]}


# =====================================================================
# PART 1: iJO1366 nitrogen-axis dose response + substitutions
# (resumable per level)
# =====================================================================
IJO_JSON = os.path.join(OUT_DIR, "keio_nitrogen_source_e12_results.json")
IJO_CSV = os.path.join(OUT_DIR, "keio_nitrogen_source_e12_sweep.csv")
keio_tab, st6_tab = keio_tables()

_probe_tmp = None
if os.path.exists(IJO_JSON) and os.path.exists(IJO_CSV):
    with open(IJO_JSON) as f:
        try:
            _probe_tmp = json.load(f)
        except Exception:
            _probe_tmp = None
if _probe_tmp is not None and all(l["key"] in _probe_tmp["levels"]
                                   for l in IJO_LEVELS):
    ijo_results = _probe_tmp
    print("PART 1 (iJO1366): artifacts found -- RESUMING from them.",
          flush=True)
    ijo_sweep = pd.read_csv(IJO_CSV)
else:
    if _probe_tmp is not None:
        print("PART 1 (iJO1366): INCOMPLETE artifacts -- recomputing "
              "missing levels.", flush=True)
    print("=" * 78)
    print("THIRD PERTURBATION AXIS: NITROGEN SOURCE (iJO1366)")
    print("  Baseline: glucose-only medium (glc -10, O2 -20, tre CLOSED)")
    print("  Levels:", [l["key"] for l in IJO_LEVELS])
    print("=" * 78, flush=True)
    ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))

    ijo_sweep_rows = []
    if _probe_tmp is not None:
        ijo_results = _probe_tmp
        # reload already-computed sweep rows from the partial CSV
        _partial = pd.read_csv(IJO_CSV)
        for l in IJO_LEVELS:
            if l["key"] not in ijo_results["levels"]:
                continue
            _rows = _partial[_partial["level"] == l["key"]]
            if len(_rows) > 0:
                ijo_sweep_rows.append(_rows)
    else:
        ijo_results = {"probe": "nitrogen-source axis, iJO1366",
                       "baseline_medium": "glucose -10, O2 -20, minerals "
                                          "-1000, nh4 unlimited, EX_tre_e "
                                          "CLOSED (glucose-only run)",
                       "levels": {}}
    t_all = time.time()
    for lv in IJO_LEVELS:
        if lv["key"] in ijo_results["levels"]:
            continue
        print(f"\n----- iJO1366, {lv['key']} ({lv['label']}) -----",
              flush=True)
        set_ijo_medium(ijo, lv)
        b_wt, flux_wt, wtinfo = wt_block(ijo, lv)
        print(f"  WT biomass = {b_wt:.6f}; uptakes = {wtinfo['uptakes']}",
              flush=True)
        if wtinfo["n_route_fluxes"]:
            print(f"  N-route fluxes = {wtinfo['n_route_fluxes']}", flush=True)
        if wtinfo["nh4_release_routes"]:
            print("  internal nh4 release: " + "; ".join(
                f"{r['reaction']}({r['genes']}) {r['net_production']}"
                for r in wtinfo["nh4_release_routes"][:5]), flush=True)
        t0 = time.time()
        rows = ko_sweep_ijo(ijo, b_wt, flux_wt)
        print(f"  sweep done ({time.time()-t0:.0f}s), {len(rows)} genes",
              flush=True)
        df = pd.DataFrame(rows)
        df.insert(0, "level", lv["key"])
        ijo_sweep_rows.append(df)
        cal = transitive_calibration(df)
        da, merged = direct_arm(df, keio_tab, st6_tab)
        fl, _ = flip_analysis(df, os.path.join(OUT_DIR,
                                               "keio_glucose_only_e12.csv"),
                              ijo, f"{lv['key']} vs glucose-only (nh4 "
                                   f"unlimited)")
        ijo_results["levels"][lv["key"]] = {
            "kind": lv["kind"], "label": lv["label"],
            "wild_type_biomass": b_wt, "wt_info": wtinfo,
            "transitive_calibration": cal, "direct_arm": da,
            "flips_vs_glucose_only": fl,
        }
        print(f"  calibration r = "
              f"{cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"held-out AUC = {cal['held_out']['roc_auc']:.4f}, "
              f"MCC = {cal['held_out']['mcc']:.4f}", flush=True)
        print(f"  labels: {fl['n_essential_base']} -> "
              f"{fl['n_essential_new']} "
              f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']} flips, "
              f"kappa = {fl['cohen_kappa']:.4f}); direct arm: "
              f"r = {da['pearson_r']:+.4f}, AUC = {da['roc_auc']:.4f}",
              flush=True)
        # checkpoint per level (resumability)
        ijo_sweep = pd.concat(ijo_sweep_rows) if ijo_sweep_rows else None
        if ijo_sweep is not None:
            ijo_sweep.to_csv(IJO_CSV, index=False)
        with open(IJO_JSON, "w") as f:
            json.dump(ijo_results, f, indent=2)
    ijo_sweep = pd.concat(ijo_sweep_rows)
    ijo_sweep.to_csv(IJO_CSV, index=False)
    with open(IJO_JSON, "w") as f:
        json.dump(ijo_results, f, indent=2)
    print(f"\niJO1366 nitrogen-axis probe complete "
          f"({time.time()-t_all:.0f}s).", flush=True)

# =====================================================================
# PART 2: iML1515 cross-rebuild arms
# =====================================================================
print("\n" + "=" * 78)
print("THIRD PERTURBATION AXIS: NITROGEN SOURCE (iML1515)")
print("=" * 78, flush=True)
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
IML_JSON = os.path.join(OUT_DIR, "keio_nitrogen_source_e16_results.json")
IML_CSV = os.path.join(OUT_DIR, "keio_nitrogen_source_e16_sweep.csv")

if os.path.exists(IML_JSON) and os.path.exists(IML_CSV):
    print("PART 2 (iML1515): artifacts found -- RESUMING from them.",
          flush=True)
    with open(IML_JSON) as f:
        iml_results = json.load(f)
    iml_sweep_all = pd.read_csv(IML_CSV)
else:
    iml_sweep_rows = []
    iml_results = {"probe": "nitrogen-source axis, iML1515 cross-rebuild",
                   "baseline_medium": "glucose -10, O2 -20, minerals -10, "
                                      "nh4 -10, EX_tre_e CLOSED",
                   "levels": {}}
    for lv in IML_LEVELS:
        print(f"\n----- iML1515, {lv['key']} ({lv['label']}) -----",
              flush=True)
        set_iml_medium(iml, lv)
        b_wt, flux_wt, wtinfo = wt_block(iml, lv)
        print(f"  WT biomass = {b_wt:.6f}; uptakes = {wtinfo['uptakes']}",
              flush=True)
        if wtinfo["nh4_release_routes"]:
            print("  internal nh4 release: " + "; ".join(
                f"{r['reaction']}({r['genes']}) {r['net_production']}"
                for r in wtinfo["nh4_release_routes"][:5]), flush=True)
        v_wt = np.array([flux_wt.get(r.id, 0.0) for r in iml.reactions])
        thr = 0.05 * b_wt
        t0 = time.time()
        iml_rows = []
        for g in iml.genes:
            g_id = g.id
            try:
                with iml:
                    for r in iml.reactions:
                        if g_id in r.gene_reaction_rule:
                            r.lower_bound = 0
                            r.upper_bound = 0
                    ko_sol = iml.optimize()
                    if ko_sol.status != "optimal":
                        b_ko = 0.0
                        v_ko = np.zeros_like(v_wt)
                    else:
                        b_ko = float(ko_sol.objective_value)
                        v_ko = np.array([ko_sol.fluxes.get(r.id, 0.0)
                                         for r in iml.reactions])
                dv = v_ko - v_wt
                mask = np.abs(dv) > 1e-6
                kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
                n_gpr = sum(1 for r in iml.reactions
                            if g_id in r.gene_reaction_rule)
                iml_rows.append({
                    "gene_id": g_id, "n_gpr_rxns": n_gpr,
                    "n_changed": int(mask.sum()), "b_wt": b_wt, "b_ko": b_ko,
                    "delta_b": float(b_wt - b_ko),
                    "y_essential": 1 if b_ko < thr else 0, "kV": kV,
                })
            except Exception:
                iml_rows.append({"gene_id": g_id, "n_gpr_rxns": 0,
                                 "n_changed": 0, "b_wt": b_wt,
                                 "b_ko": float('nan'),
                                 "delta_b": float('nan'), "y_essential": -1,
                                 "kV": 0.0})
            if len(iml_rows) % 300 == 0:
                print(f"    progress {len(iml_rows)}/{len(iml.genes)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
        iml_df = pd.DataFrame([r for r in iml_rows if r["y_essential"] >= 0])
        iml_df.insert(0, "level", lv["key"])
        iml_sweep_rows.append(iml_df)
        print(f"  sweep done ({time.time()-t0:.0f}s), {len(iml_df)} genes, "
              f"{int(iml_df.y_essential.sum())} essential", flush=True)

        iml_cal = transitive_calibration(iml_df)
        iml_da, _ = direct_arm(iml_df, keio_tab, st6_tab)
        iml_fl, _ = flip_analysis(
            iml_df, os.path.join(OUT_DIR, "keio_glucose_only_e16_sweep.csv"),
            iml, f"iML1515 {lv['key']} vs glucose-only (nh4 -10)")
        iml_results["levels"][lv["key"]] = {
            "kind": lv["kind"], "label": lv["label"],
            "wild_type_biomass": b_wt, "wt_info": wtinfo,
            "transitive_calibration": iml_cal, "direct_arm": iml_da,
            "flips_vs_glucose_only": iml_fl,
        }
        print(f"  calibration r = "
              f"{iml_cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"held-out AUC = {iml_cal['held_out']['roc_auc']:.4f}; "
              f"labels {iml_fl['n_essential_base']} -> "
              f"{iml_fl['n_essential_new']} (+{iml_fl['n_gain_essential']}/"
              f"-{iml_fl['n_loss_essential']}, kappa "
              f"{iml_fl['cohen_kappa']:.4f}); direct r "
              f"{iml_da['pearson_r']:+.4f}, AUC {iml_da['roc_auc']:.4f}",
              flush=True)
        # checkpoint per level
        iml_sweep_all = pd.concat(iml_sweep_rows)
        iml_sweep_all.to_csv(IML_CSV, index=False)
        with open(IML_JSON, "w") as f:
            json.dump(iml_results, f, indent=2)

    iml_sweep_all = pd.concat(iml_sweep_rows)
    iml_sweep_all.to_csv(IML_CSV, index=False)
    with open(IML_JSON, "w") as f:
        json.dump(iml_results, f, indent=2)

# =====================================================================
# PART 3: summary txt
# =====================================================================
lines = []
lines.append("THIRD PERTURBATION AXIS: NITROGEN SOURCE")
lines.append("Label invariance generalization (iJO1366 + iML1515)")
lines.append("=" * 78)
lines.append("Baseline: glucose-only corrected medium (trehalose closed),")
lines.append("ammonium unlimited on iJO1366 / -10 on iML1515.")
lines.append("Probe: (a) ammonium-supply limitation gradient;")
lines.append("(b) nitrogen-source substitution (nh4 closed, sole N")
lines.append("source = L-glutamate at matched N flux or L-arginine at")
lines.append("N+C surplus).")
lines.append("")
base_ijo = json.load(open(os.path.join(OUT_DIR,
                                       "keio_glucose_only_e12_results.json")))
lines.append(f"iJO1366 baseline (nh4 unlimited): WT "
             f"{base_ijo['wild_type_biomass']:.4f}, "
             f"{base_ijo['n_essential']}/{base_ijo['n_genes_processed']} "
             f"essential, "
             f"r = {base_ijo['calibration']['pearson_r_log_kV_delta_b']:+.4f}, "
             f"AUC {base_ijo['held_out_essentiality_prediction']['roc_auc']:.4f}")
for lv in IJO_LEVELS:
    d = ijo_results["levels"][lv["key"]]
    cal = d["transitive_calibration"]
    fl = d["flips_vs_glucose_only"]
    da = d["direct_arm"]
    lines.append(f"{lv['key']:>9}: WT {d['wild_type_biomass']:.4f} "
                 f"(uptake {d['wt_info']['uptakes']}); "
                 f"labels {fl['n_essential_base']} -> "
                 f"{fl['n_essential_new']} "
                 f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, "
                 f"kappa {fl['cohen_kappa']:.4f}); "
                 f"r = {cal['pearson_r_log_kV_delta_b']:+.4f}, "
                 f"held-out AUC {cal['held_out']['roc_auc']:.4f}, "
                 f"MCC {cal['held_out']['mcc']:.4f}; "
                 f"direct r {da['pearson_r']:+.4f}, "
                 f"AUC {da['roc_auc']:.4f}")
lines.append("")
base_iml = json.load(open(os.path.join(OUT_DIR,
                                       "keio_glucose_only_e16_results.json")))
lines.append(f"iML1515 baseline (nh4 -10): WT "
             f"{base_iml['wild_type_biomass']:.4f}, "
             f"{base_iml['n_essential_in_silico']}/"
             f"{base_iml['n_genes_processed']} essential, direct r "
             f"{base_iml['direct_validation']['pearson_r']:+.4f}, "
             f"AUC {base_iml['direct_validation']['roc_auc']:.4f}")
for lv in IML_LEVELS:
    d = iml_results["levels"][lv["key"]]
    fl = d["flips_vs_glucose_only"]
    da = d["direct_arm"]
    cal = d["transitive_calibration"]
    lines.append(f"iML1515 {lv['key']:>9}: WT {d['wild_type_biomass']:.4f} "
                 f"(uptake {d['wt_info']['uptakes']}); "
                 f"labels {fl['n_essential_base']} -> "
                 f"{fl['n_essential_new']} "
                 f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, "
                 f"kappa {fl['cohen_kappa']:.4f}); direct r "
                 f"{da['pearson_r']:+.4f}, AUC {da['roc_auc']:.4f}; "
                 f"transitive r {cal['pearson_r_log_kV_delta_b']:+.4f}, "
                 f"held-out AUC {cal['held_out']['roc_auc']:.4f}")
lines.append("")
lines.append("Matched-N control: glu_L carries one N per molecule, so the")
lines.append("glu -10 substitution supplies exactly the N flux of the nh4")
lines.append("-10 limitation; both give WT 0.9259 on iJO1366 (the N-to-")
lines.append("growth map is the same from either nitrogen donor).")
lines.append("")
lines.append("Internal nh4-release routes at the substitution optima:")
for lv in IJO_LEVELS:
    if lv["kind"] != "substitution":
        continue
    d = ijo_results["levels"][lv["key"]]
    rr = d["wt_info"]["nh4_release_routes"]
    lines.append(f"  iJO1366 {lv['key']}: " + ("; ".join(
        f"{r['reaction']} ({r['genes']}) {r['net_production']}" for r in rr[:6])
        if rr else "none at optimum"))
for lv in IML_LEVELS:
    if lv["kind"] != "substitution":
        continue
    d = iml_results["levels"][lv["key"]]
    rr = d["wt_info"]["nh4_release_routes"]
    lines.append(f"  iML1515 {lv['key']}: " + ("; ".join(
        f"{r['reaction']} ({r['genes']}) {r['net_production']}" for r in rr[:6])
        if rr else "none at optimum"))
lines.append("")
lines.append("Top subsystem enrichments of the flip sets (non-empty only):")
for lv in IJO_LEVELS:
    fl = ijo_results["levels"][lv["key"]]["flips_vs_glucose_only"]
    if fl["n_gain_essential"] + fl["n_loss_essential"] == 0:
        continue
    lines.append(f"  iJO1366 {lv['key']}: " + "; ".join(
        f"{d2['subsystem']} ({d2['n_flip']} vs exp {d2['expected']})"
        for d2 in fl["subsystem_enrichment_top"][:5]))
for lv in IML_LEVELS:
    fl = iml_results["levels"][lv["key"]]["flips_vs_glucose_only"]
    if fl["n_gain_essential"] + fl["n_loss_essential"] == 0:
        continue
    lines.append(f"  iML1515 {lv['key']}: " + "; ".join(
        f"{d2['subsystem']} ({d2['n_flip']} vs exp {d2['expected']})"
        for d2 in fl["subsystem_enrichment_top"][:5]))
with open(os.path.join(OUT_DIR, "keio_nitrogen_source_summary.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSummary written.")

# =====================================================================
# PART 4: nitrogen-axis response figure (categorical axis)
# =====================================================================
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

x_labels = ["baseline\n(nh4 unlimited)"] + [l["key"].replace("_", " ")
            for l in IJO_LEVELS]
xs = np.arange(len(x_labels))
gains = [0] + [ijo_results["levels"][l["key"]]["flips_vs_glucose_only"]["n_gain_essential"]
               for l in IJO_LEVELS]
losses = [0] + [ijo_results["levels"][l["key"]]["flips_vs_glucose_only"]["n_loss_essential"]
                for l in IJO_LEVELS]
pears = [base_ijo['calibration']['pearson_r_log_kV_delta_b']] + \
        [ijo_results["levels"][l["key"]]["transitive_calibration"]["pearson_r_log_kV_delta_b"]
         for l in IJO_LEVELS]
aucs = [base_ijo['held_out_essentiality_prediction']['roc_auc']] + \
       [ijo_results["levels"][l["key"]]["transitive_calibration"]["held_out"]["roc_auc"]
        for l in IJO_LEVELS]
wts = [base_ijo['wild_type_biomass']] + \
      [ijo_results["levels"][l["key"]]["wild_type_biomass"]
       for l in IJO_LEVELS]

fig, (axA, axB, axC) = plt.subplots(
    1, 3, figsize=(16, 4.8), constrained_layout=True)
axA.bar(xs - 0.17, gains, 0.34, color='firebrick',
        label='iJO1366 gain essentiality')
axA.bar(xs + 0.17, losses, 0.34, color='steelblue',
        label='iJO1366 lose essentiality')
for i, lv in enumerate(IML_LEVELS):
    fl = iml_results["levels"][lv["key"]]["flips_vs_glucose_only"]
    j = 1 + [l["key"] for l in IJO_LEVELS].index(lv["key"])
    axA.plot([j], [fl["n_gain_essential"]], '*', ms=15, color='firebrick',
             alpha=0.55, label='iML1515 (gain)' if i == 0 else None)
    axA.plot([j], [fl["n_loss_essential"]], '*', ms=15, color='steelblue',
             alpha=0.55, label='iML1515 (lose)' if i == 0 else None)
axA.set_xticks(xs)
axA.set_xticklabels(x_labels, fontsize=8, rotation=20, ha='right')
axA.set_ylabel("label flips vs glucose-only baseline")
axA.set_title("(a) Essentiality-label re-stratification")
axA.legend(fontsize=8)
axA.grid(alpha=0.3, axis='y')

axB.plot(xs, wts, 'o-', color='black')
for x, w in zip(xs, wts):
    axB.annotate(f"{w:.3f}", (x, w), textcoords="offset points",
                 xytext=(0, 7), fontsize=7, ha='center')
axB.axhline(base_ijo['wild_type_biomass'], color='gray', ls=':',
            lw=1, label='baseline WT')
axB.set_xticks(xs)
axB.set_xticklabels(x_labels, fontsize=8, rotation=20, ha='right')
axB.set_ylabel("wild-type biomass")
axB.set_title("(b) Growth along the nitrogen axis")
axB.legend(fontsize=8)
axB.grid(alpha=0.3, axis='y')

axC.plot(xs, pears, 'o-', color='darkgreen',
         label=r"Pearson $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axC.plot(xs, aucs, 's--', color='darkorange',
         label="held-out ROC AUC (label prediction)")
axC.set_xticks(xs)
axC.set_xticklabels(x_labels, fontsize=8, rotation=20, ha='right')
axC.set_ylabel("statistic")
axC.set_ylim(0.45, 1.02)
axC.set_title("(c) Curvature-phenotype association")
axC.legend(fontsize=8)
axC.grid(alpha=0.3, axis='y')
fig.suptitle("Third perturbation axis: nitrogen source "
             "(iJO1366; limitation gradient + source substitution)",
             fontsize=12, fontweight="bold")
plt.savefig(os.path.join(OUT_DIR, "keio_nitrogen_source_response.png"),
            dpi=120)
plt.close()
print("Figure written.")
print("\nNITROGEN-SOURCE PROBE DONE.")
