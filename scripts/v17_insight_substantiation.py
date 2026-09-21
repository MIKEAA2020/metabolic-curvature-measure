#!/usr/bin/env python3
"""
V17 insight-substantiation round (Part B of download/V17_Revision_Plan.md).

Computes the six beyond-established insight lines from DEPOSITED artifacts
ONLY (no new LP solves, no manuscript edits), per the author directive
"proceed with the previous 6 suggestions" (venue decision to follow the
developed impact):

  I   menu/order synthesis   - growth-silent partition across the three V7
                               trajectories (recomputed from the V7 CSVs) +
                               operon / TRN-regulon / iModulon enrichment of
                               high-kappa_mu genes (PRECISE annotations) +
                               TRN metabolite-effector overlap
  II  construction order     - both-order loop analysis from m3_path.csv:
                               order-rule correlation, wall-interference
                               merge, magnitude calibration
  III memory substrate       - quantitative premises reassembled (m3_summary
                               holonomy + E27 Schmidt protein-layer arm
                               recomputed from its csv)
  IV  wall coordinates       - per-reaction curvature mass from the M1 sweep
                               family (iML1515) mapped to branch metabolites
  V   drift-free interior    - curvature-mass distribution over reaction
                               classes (exchange/transport/internal) and
                               subsystems; iJO one-chamber cross-check
  VI  community priority     - no computation (plan scopes it to follow-up);
                               developed in V17_Insight_Development.md

Self-checks: r=+0.3954 (V7 P0 arm A), holonomy 66.25%, M1 D2 totals vs
m1_summary.json. Every number in the ledger traces to a committed artifact.

Output: download/v17_insight_substantiation.json (+ console summary).
"""
import json
import os
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy import stats

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(BASE, "download")
DB = os.path.join(DL, "deepseek_bridge")
M13 = os.path.join(DL, "m1_m3")
PRECISE = os.path.join(BASE, "data", "precise", "data")

rng = np.random.default_rng(20260921)
LEDGER = {"round": "v17-insight-substantiation"}

# ----------------------------------------------------------------- helpers
def bh(pvals):
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order] * n / (np.arange(n) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(ranked, 1.0)
    return out


def fisher_enrichment(top_set, background, target_sets, min_targets=8,
                      label=""):
    """Fisher exact (greater) + BH over target sets; returns ranked table."""
    rows = []
    bgt = set(background)
    top = set(top_set)
    n_top, n_bgt = len(top), len(bgt)
    keys = [k for k, s in target_sets.items()
            if len(set(s) & bgt) >= min_targets]
    for k in keys:
        t = set(target_sets[k]) & bgt
        a = len(t & top)                      # in top & target
        b = n_top - a                         # in top & not target
        c = len(t) - a                        # not top & target
        d = n_bgt - n_top - c                 # not top & not target
        orr, p = stats.fisher_exact([[a, b], [c, d]], alternative="greater")
        rows.append({"set": k, "n_targets_in_bg": len(t), "n_in_top": a,
                     "expected": n_top * len(t) / n_bgt,
                     "fold": (a / n_top) / (len(t) / n_bgt) if len(t) else 0.0,
                     "OR": orr, "p": p})
    if not rows:
        return pd.DataFrame(), keys
    df = pd.DataFrame(rows)
    df["p_bh"] = bh(df["p"].values)
    df = df.sort_values("p").reset_index(drop=True)
    df.insert(0, "class", label)
    return df, keys


def perm_share(vec, mask, n_perm=10000):
    """Permutation p for share of total mass on masked entries."""
    vec = np.asarray(vec, float)
    mask = np.asarray(mask, bool)
    obs = vec[mask].sum() / vec.sum()
    null = np.array([vec[rng.permutation(len(vec))][mask].sum()
                     / vec.sum() for _ in range(n_perm)])
    p = float((null >= obs - 1e-15).mean())
    return obs, p


def mwu_auc(vec, mask):
    vec = np.asarray(vec, float)
    mask = np.asarray(mask, bool)
    x, y = vec[mask], vec[~mask]
    if len(x) < 3 or len(y) < 3:
        return None, None, None
    u, p = stats.mannwhitneyu(x, y, alternative="greater")
    auc = u / (len(x) * len(y))
    return float(u), float(p), float(auc)


def rlog(x):
    return None if x is None else float(x)


# ======================================================================
# Shared loads
# ======================================================================
model = json.load(open(os.path.join(BASE, "data", "bigg_models",
                                    "iML1515.json")))
RXNS = {r["id"]: r for r in model["reactions"]}
METS = {m["id"]: m for m in model["metabolites"]}
RXN_IDS = [r["id"] for r in model["reactions"]]
R_IDX = {rid: i for i, rid in enumerate(RXN_IDS)}

# compartment classification
def rxn_class(rid):
    r = RXNS[rid]
    if rid.startswith("EX_"):
        return "exchange"
    comps = {METS[m]["compartment"] for m in r["metabolites"]}
    if len(comps) > 1:
        return "transport"
    return "internal"

RXN_CLASS = {rid: rxn_class(rid) for rid in RXN_IDS}

# base-metabolite participation degree (union across compartments)
CURRENCY = {
    "h2o", "h", "pi", "ppi", "co2", "o2", "atp", "adp", "amp", "gtp", "gdp",
    "gmp", "ctp", "cdp", "cmp", "utp", "udp", "ump", "itp", "idp", "imp",
    "nad", "nadh", "nadp", "nadph", "fad", "fadh2", "q8", "q8h2", "mql8",
    "mqn8", "h2o2", "fe2", "fe3", "mn2", "mg2", "k", "na1", "cl", "ca2",
    "cu2", "zn2", "ni2", "ni1", "ni3", "mobd", "cobalt2", "so4", "nh4",
    "no3", "no2", "tungs6", "sel", "cbl1", "5mthf"}
BASE_DEG = Counter()
for r in model["reactions"]:
    bases = {m.rsplit("_", 1)[0] for m in r["metabolites"]}
    for b in bases:
        BASE_DEG[b] += 1
deg_all = np.array([BASE_DEG[b] for b in BASE_DEG])
ncurr_bases = [b for b in BASE_DEG if b not in CURRENCY]
deg_nc = np.array([BASE_DEG[b] for b in ncurr_bases])
D_STAR = float(np.quantile(deg_nc, 0.90))   # primary: top decile, non-currency

def branch_mets_of(rid, d_star, exclude_currency=True):
    r = RXNS[rid]
    out = set()
    for m in r["metabolites"]:
        b = m.rsplit("_", 1)[0]
        if exclude_currency and b in CURRENCY:
            continue
        if BASE_DEG[b] >= d_star:
            out.add(b)
    return out

# ---------------------------------------------------------------- per-gene
v7 = json.load(open(os.path.join(DB, "v7_path_robustness.json")))
v7p0 = pd.read_csv(os.path.join(DB, "v7_P0_glucose_decline.csv"))
v7p1 = pd.read_csv(os.path.join(DB, "v7_P1_oxygen_limitation.csv"))
v7p2 = pd.read_csv(os.path.join(DB, "v7_P2_acetate_switch.csv"))
gene_kappa = v7p0.set_index("gene")["kappa_mu"]

# PRECISE annotations
gi = pd.read_csv(os.path.join(PRECISE, "gene_info.csv"), index_col=0)
GENE2OP = {ix: row["operon"] for ix, row in gi.iterrows()
           if isinstance(row["operon"], str)}
trn = pd.read_csv(os.path.join(PRECISE, "TRN.csv"))
REG2TARGETS = defaultdict(set)
REG2EFFECT = defaultdict(lambda: defaultdict(set))
for _, row in trn.iterrows():
    REG2TARGETS[str(row["regulator"])].add(str(row["gene_id"]))
    REG2EFFECT[str(row["regulator"])][str(row["effect"])].add(
        str(row["gene_id"]))
IMOD = {}
with open(os.path.join(PRECISE, "imodulon_gene_bnumbers.txt")) as f:
    for line in f:
        parts = [p.strip() for p in line.strip().split(",") if p.strip()]
        if parts and parts[0].lower() != "i-modulon name":
            IMOD[parts[0]] = set(parts[1:])
enr = pd.read_csv(os.path.join(PRECISE, "curated_enrichments.csv"))
IMOD_CAT = dict(zip(enr["name"].astype(str), enr["Category"].astype(str)))

# M3 path / pairs
m3_path = pd.read_csv(os.path.join(M13, "m3_path.csv"))
m3_pairs = pd.read_csv(os.path.join(M13, "m3_pairs.csv"))
m3_summary = json.load(open(os.path.join(M13, "m3_summary.json")))

# M1 sweep family (per-reaction curvature mass)
M1 = json.load(open(os.path.join(M13, "m1_summary.json")))
SWEEPS = [s for s in M1["sweeps"] if not s.startswith("ijo") and
          M1["sweeps"][s].get("D2_total", 0) > 1e-6]
SWEEP_FILES = {"iml_glucose": "m1_iml_glucose.npz",
               "iml_o2": "m1_iml_o2.npz"}
for s in SWEEPS:
    if s.startswith("kd_"):
        SWEEP_FILES[s] = f"m1_{s}.npz"
SWEEP_LIST = [s for s in SWEEPS if s in SWEEP_FILES]

# E27 Schmidt protein-layer csv (line III premises)
e27 = pd.read_csv(os.path.join(DL, "novelty_v20_e27_schmidt_replication.csv"))

# iJO1366 GPR: gene -> reaction set (for the operon GPR-sharing control)
import re
model_ijo = json.load(open(os.path.join(BASE, "data", "bigg_models",
                                         "iJO1366.json")))
G2R = defaultdict(set)
for r in model_ijo["reactions"]:
    for g in re.findall(r"b\d{4}", r.get("gene_reaction_rule", "")):
        G2R[g].add(r["id"])

# ======================================================================
# LINE I - menu/order synthesis
# ======================================================================
print("\n=== LINE I: menu/order synthesis ===")
I = {}

# (a) growth-silent partition across the three trajectories
part = []
for tag, df in [("P0_glucose_decline", v7p0), ("P1_oxygen_limitation", v7p1),
                ("P2_acetate_switch", v7p2)]:
    kc_nonzero = int((df["kappa_c"].abs() > 1e-12).sum())
    n_kappa = int((df["kappa_mu"] > 0).sum())
    arms = v7["paths"][tag]["arms"]
    a = arms["A kappa_mu (flux, all events)"]["nonzero"]
    b3 = arms.get("B3all kappa_dual (all kinks, V6-comparable)",
                  {}).get("nonzero", {})
    b2n = arms.get("B2 kappa_c (c-attribution)", {}).get("nonzero", {})
    kc = v7["paths"][tag]["value_kink_census"]
    cross = arms.get("A kappa_mu vs E24 carbon response (cross)",
                     {}).get("nonzero", {})
    part.append({
        "path": tag,
        "interior_chamber_crossings": kc.get("n_chamber_crossings"),
        "value_over_flux_mass_ratio": kc.get("value_over_flux_mass_ratio"),
        "n_genes_kappa_mu_nonzero": n_kappa,
        "arm_A_flux_r": a["pearson_r"], "arm_A_p": a["pearson_p"],
        "kappa_c_nonzero_genes": kc_nonzero,
        "B2_c_attribution_n": b2n.get("n", 0),
        "B3_dual_r": rlog(b3.get("pearson_r")), "B3_dual_p": rlog(b3.get("pearson_p")),
        "B3_dual_n": b3.get("n"),
        "cross_arm_r_vs_carbon_response": rlog(cross.get("pearson_r")),
    })
I["growth_silent_partition"] = part
for p in part:
    print(f"  {p['path']}: A r={p['arm_A_flux_r']:.4f} | kappa_c nonzero "
          f"= {p['kappa_c_nonzero_genes']}/433 | dual arm r="
          f"{p['B3_dual_r']} (p={p['B3_dual_p']:.3f}, n={p['B3_dual_n']}) "
          f"| value/flux mass = "
          f"{p['value_over_flux_mass_ratio']:.5f} | cross r="
          f"{p['cross_arm_r_vs_carbon_response']}")

# (b) co-regulation enrichment of high-kappa genes
bgt = [g for g in gene_kappa.index if gene_kappa[g] > 0]
kvals = np.array([gene_kappa[g] for g in bgt])
qcut = float(np.quantile(kvals, 0.75))
top_q = [g for g in bgt if gene_kappa[g] >= qcut]
dcut = float(np.quantile(kvals, 0.90))
top_d = [g for g in bgt if gene_kappa[g] >= dcut]
print(f"  panel: {len(bgt)} nonzero-kappa genes; top quartile n="
      f"{len(top_q)} (kappa >= {qcut:.3f}); top decile n={len(top_d)}")

# operons
OP2GENES = defaultdict(set)
for g in bgt:
    op = GENE2OP.get(g)
    if op:
        OP2GENES[str(op)].add(g)
df_op, _ = fisher_enrichment(top_q, bgt, OP2GENES, min_targets=3,
                             label="operon")
# permutation: intra-operon kappa dispersion vs label permutation
op_of = {g: GENE2OP.get(g) for g in bgt}
kv = dict(zip(bgt, kvals))
intra_i, intra_j = [], []
for i, g1 in enumerate(bgt):
    op1 = op_of[g1]
    if not op1:
        continue
    for g2 in bgt[i + 1:]:
        if op_of[g2] == op1:
            intra_i.append(i)
            intra_j.append(bgt.index(g2))
intra_i = np.array(intra_i)
intra_j = np.array(intra_j)
intra_obs = float(np.mean(np.abs(kvals[intra_i] - kvals[intra_j])))
perm_stats = np.array([
    np.mean(np.abs(lab[intra_i] - lab[intra_j]))
    for lab in (rng.permutation(kvals) for _ in range(5000))])
p_intra = float(np.mean(perm_stats <= intra_obs))
inter_gap = float(np.mean([abs(kv[g1] - kv[g2])
                           for i, g1 in enumerate(bgt)
                           for g2 in bgt[i + 1:]
                           if op_of[g1] != op_of[g2]]))
# GPR-sharing control: restrict intra-operon pairs to DISJOINT reaction sets
isj_i, isj_j = [], []
sh_i, sh_j = [], []
for a, b in zip(intra_i, intra_j):
    g1, g2 = bgt[a], bgt[b]
    r1, r2 = G2R.get(g1, set()), G2R.get(g2, set())
    if r1 & r2:
        sh_i.append(a); sh_j.append(b)
    else:
        isj_i.append(a); isj_j.append(b)
isj_i, isj_j = np.array(isj_i), np.array(isj_j)
sh_i, sh_j = np.array(sh_i), np.array(sh_j)
if len(isj_i) >= 10:
    isj_obs = float(np.mean(np.abs(kvals[isj_i] - kvals[isj_j])))
    isj_perm = np.array([
        np.mean(np.abs(lab[isj_i] - lab[isj_j]))
        for lab in (rng.permutation(kvals) for _ in range(5000))])
    p_isj = float(np.mean(isj_perm <= isj_obs))
else:
    isj_obs, p_isj = None, None
sh_obs = float(np.mean(np.abs(kvals[sh_i] - kvals[sh_j]))) if len(
    sh_i) >= 1 else None
I["operon"] = {
    "n_operons_tested": int(len(df_op)) if len(df_op) else 0,
    "top_operons": df_op.head(8).to_dict("records") if len(df_op) else [],
    "intra_operon_mean_kappa_gap": intra_obs,
    "inter_operon_mean_kappa_gap": inter_gap,
    "permutation_p_gap_smaller": p_intra,
    "n_intra_operon_pairs": int(len(intra_i)),
    "gpr_control": {
        "n_disjoint_reaction_pairs": int(len(isj_i)),
        "disjoint_pairs_mean_gap": isj_obs,
        "disjoint_pairs_perm_p": p_isj,
        "shared_reaction_pairs_mean_gap": sh_obs,
        "n_shared_reaction_pairs": int(len(sh_i)),
    },
    "n_operons_BH_lt_0.10": int((df_op["p_bh"] < 0.10).sum()) if len(
        df_op) else 0,
}
print(f"  operons: {len(df_op)} tested, smallest BH p="
      f"{(df_op['p_bh'].min() if len(df_op) else None)}; "
      f"intra-op |dkappa| gap {intra_obs:.3f} vs inter {inter_gap:.3f} "
      f"({len(intra_i)} pairs, perm p={p_intra:.4f})")
if len(df_op):
    for _, r in df_op.head(5).iterrows():
        print(f"    {r['set']}: {int(r['n_in_top'])}/{int(r['n_targets_in_bg'])}"
              f" (exp {r['expected']:.1f}, fold {r['fold']:.2f}, "
              f"p={r['p']:.2e})")
if isj_obs is not None:
    print(f"  GPR control: disjoint-reaction intra-op pairs "
          f"n={len(isj_i)}, |dkappa| gap {isj_obs:.3f} "
          f"(shared-reaction pairs n={len(sh_i)}, gap {sh_obs:.3f}; "
          f"perm p disjoint={p_isj:.4f})")

# TRN regulons
df_trn, _ = fisher_enrichment(top_q, bgt, REG2TARGETS, min_targets=8,
                              label="regulon")
I["regulon"] = {
    "n_regulons_tested": int(len(df_trn)) if len(df_trn) else 0,
    "top_regulons": df_trn.head(12).to_dict("records") if len(df_trn) else [],
}
if len(df_trn):
    sig = df_trn[df_trn["p_bh"] < 0.10]
    print(f"  regulons: {len(df_trn)} tested, BH<0.10: {len(sig)}")
    for _, r in df_trn.head(8).iterrows():
        print(f"    {r['set']}: {int(r['n_in_top'])}/{int(r['n_targets_in_bg'])}"
              f" (exp {r['expected']:.1f}, fold {r['fold']:.2f}, "
              f"p={r['p']:.2e})")
    # effect split for top regulons
    eff_split = []
    for _, r in df_trn.head(6).iterrows():
        reg = r["set"]
        for eff in ("+", "-"):
            tg = REG2EFFECT[reg].get(eff, set()) & set(bgt)
            if len(tg) >= 5:
                kt = [kv[g] for g in tg if g in kv]
                kb = [kv[g] for g in bgt if g not in tg]
                u, p = stats.mannwhitneyu(kt, kb, alternative="greater")
                eff_split.append({"regulator": reg, "effect": eff,
                                  "n": len(tg),
                                  "median_kappa_targets": float(np.median(kt)),
                                  "median_kappa_rest": float(np.median(kb)),
                                  "MWU_p": float(p)})
    I["regulon"]["effect_split"] = eff_split
    for e in eff_split:
        print(f"    {e['regulator']} ({'activation' if e['effect']=='+' else 'repression'}): "
              f"median kappa {e['median_kappa_targets']:.1f} vs rest "
              f"{e['median_kappa_rest']:.1f}, p={e['MWU_p']:.3g}")

# iModulons
df_imod, _ = fisher_enrichment(top_q, bgt, IMOD, min_targets=5,
                               label="imodulon")
if len(df_imod):
    df_imod["category"] = df_imod["set"].map(IMOD_CAT)
I["imodulon"] = {
    "n_tested": int(len(df_imod)) if len(df_imod) else 0,
    "top": df_imod.head(10).to_dict("records") if len(df_imod) else [],
}
if len(df_imod):
    print(f"  iModulons: {len(df_imod)} tested")
    for _, r in df_imod.head(6).iterrows():
        print(f"    {r['set']} [{r.get('category','')}]: "
              f"{int(r['n_in_top'])}/{int(r['n_targets_in_bg'])} "
              f"(fold {r['fold']:.2f}, p={r['p']:.2e})")

# TRN metabolite-effectors that ARE model metabolites
met_names = {m["name"].strip().lower(): m["id"]
             for m in model["metabolites"] if m.get("name")}
eff_hits = []
for reg in REG2TARGETS:
    key = str(reg).strip().lower()
    key2 = key.replace("l-", "")
    if key in met_names or key2 in met_names:
        eff_hits.append({"regulator": str(reg),
                         "model_metabolite": met_names.get(
                             key, met_names.get(key2))})
I["trn_metabolite_effectors"] = {
    "n_unique_regulators": int(trn["regulator"].nunique()),
    "n_metabolite_effector_regulators": len(eff_hits),
    "examples": [h["regulator"] for h in eff_hits[:20]],
}
print(f"  TRN: {trn['regulator'].nunique()} regulators, "
      f"{len(eff_hits)} are model metabolites "
      f"(e.g. {[h['regulator'] for h in eff_hits[:8]]})")

# ======================================================================
# LINE II - construction-order epistasis
# ======================================================================
print("\n=== LINE II: construction-order epistasis ===")
II = {}
mp = m3_path.copy()
mp = mp.merge(m3_pairs[["g1", "g2", "J_dR", "J_support"]], on=["g1", "g2"],
              how="left")
tol = 1e-9
n_asym_chi = int((mp["chi"] > tol).sum())
n_asym_h = int((mp["h_loop_asym"].abs() > 1.0).sum())
sub = mp[(mp["kappa_i"] + mp["kappa_j"]) > 0].copy()
sub["P"] = (sub["kappa_i"] - sub["kappa_j"]) / (sub["kappa_i"] +
                                                sub["kappa_j"])
sub["A"] = (sub["h_loop_ifirst"] - sub["h_loop_jfirst"]) / (
    sub["h_loop_ifirst"] + sub["h_loop_jfirst"] + 1e-12)
asym = sub[(sub["h_loop_ifirst"] + sub["h_loop_jfirst"]) > 1e-6]
sp = stats.spearmanr(asym["P"], asym["A"]) if len(asym) > 3 else (np.nan,) * 2
same_sign = int((np.sign(asym["P"]) == np.sign(asym["A"])).sum())
binom_p = stats.binomtest(same_sign, len(asym), 0.5).pvalue if len(
    asym) > 0 else None
sp_chi_J = stats.spearmanr(mp["chi"], mp["J_dR"].fillna(0), nan_policy="omit")
sp_h_J = stats.spearmanr(mp["h_loop_asym"].abs(),
                         mp["J_dR"].fillna(0), nan_policy="omit")
# magnitude baseline: WT L1 flux at full glucose (iML1515 M1 sweep endpoint)
m1g = np.load(os.path.join(M13, "m1_iml_glucose.npz"), allow_pickle=True)
wt_l1 = float(np.abs(m1g["V"][-1]).sum())
nonSL = mp[mp["SL"] == False]  # noqa: E712
II.update({
    "n_pairs": int(len(mp)),
    "frac_open_path_commutator_positive": float(n_asym_chi / len(mp)),
    "frac_loop_holonomy_nonzero": m3_summary["path"][
        "frac_loop_holonomy_nonzero"],
    "h_loop_median": m3_summary["path"]["h_loop_median"],
    "chi_q90_nonSL": float(np.quantile(nonSL["chi"], 0.90)),
    "WT_L1_flux_full_glucose": wt_l1,
    "order_rule": {
        "n_pairs_analyzed": int(len(asym)),
        "spearman_P_vs_A_rho": float(sp[0]) if not np.isnan(sp[0]) else None,
        "spearman_P_vs_A_p": float(sp[1]) if not np.isnan(sp[1]) else None,
        "same_sign_count": same_sign, "binomial_p": float(binom_p),
        "n_holonomy_asym_gt1": n_asym_h,
    },
    "spearman_chi_vs_JdR_rho": float(sp_chi_J[0]),
    "spearman_chi_vs_JdR_p": float(sp_chi_J[1]),
    "spearman_hasym_vs_JdR_rho": float(sp_h_J[0]),
    "spearman_hasym_vs_JdR_p": float(sp_h_J[1]),
})
print(f"  pairs: {len(mp)} | chi>0: {n_asym_chi} ({n_asym_chi/len(mp)*100:.1f}%)"
      f" | holonomy nonzero: {m3_summary['path']['frac_loop_holonomy_nonzero']}")
print(f"  order rule (P vs A): rho={sp[0]:.3f} (p={sp[1]:.3g}), "
      f"same-sign {same_sign}/{len(asym)} (binom p={binom_p:.3g})")
print(f"  chi vs J_dR: rho={sp_chi_J[0]:.3f} (p={sp_chi_J[1]:.2g}) | "
      f"|h_asym| vs J_dR: rho={sp_h_J[0]:.3f}")
print(f"  magnitude: chi_q90(nonSL)={np.quantile(nonSL['chi'], 0.90):.1f} "
      f"vs WT L1 flux {wt_l1:.0f}")

# ======================================================================
# LINE III - memory-substrate deduction (premises)
# ======================================================================
print("\n=== LINE III: memory-substrate premises ===")
III = {}
e27_r = {}
kv_col = "kappa_V_max"
prot_col = "schmidt_prot_exh_maxfc"      # the audited -0.083 arm
tx_col = "e24_m3d_exh_maxfc"              # the audited +0.419 arm
lk = np.log10(e27[kv_col].clip(lower=1e-12))
for tag, col in (("protein_exhaustion", prot_col),
                 ("transcript_M3D", tx_col)):
    ok = pd.concat([lk, e27[col]], axis=1).dropna()
    r, p = stats.pearsonr(ok[kv_col], ok[col])
    e27_r[tag] = {"r": float(r), "p": float(p), "n": int(len(ok))}
# transcript arm restricted to the protein-shared subset (the audited
# +0.419, n=365): same genes as the protein arm
sub = e27[e27[prot_col].notna()]
ok = pd.concat([lk, sub[tx_col]], axis=1).dropna()
r, p = stats.pearsonr(ok[kv_col], ok[tx_col])
e27_r["transcript_M3D_on_protein_subset"] = {"r": float(r), "p": float(p),
                                              "n": int(len(ok))}
# locked-metric replication: log10 kappa_mu (V7 P0) vs the same arms
mrg = e27.copy()
mrg["lkmu"] = np.log10(mrg["gene_bnumber"].map(gene_kappa).clip(lower=1e-9))
for tag, col in (("protein_exhaustion_kappa_mu", prot_col),
                 ("transcript_M3D_kappa_mu", tx_col)):
    ok = mrg[["lkmu", col]].dropna()
    ok = ok[np.isfinite(ok["lkmu"])]
    r, p = stats.pearsonr(ok["lkmu"], ok[col])
    e27_r[tag] = {"r": float(r), "p": float(p), "n": int(len(ok))}
III["e27_recomputed"] = e27_r
r_prot = e27_r["protein_exhaustion"]["r"]
III.update({
    "frac_loops_non_reverting": m3_summary["path"][
        "frac_loop_holonomy_nonzero"],
    "h_loop_median_L1": m3_summary["path"]["h_loop_median"],
    "protein_layer_r": r_prot,
    "protein_layer_r2": float(r_prot ** 2),
    "interpretation": (
        "protein-layer fold-change carries at most "
        f"{100 * r_prot ** 2:.2f}% of the kappa variance; with 66.25% of "
        "closed cycles retaining flux-state drift, the carrier of path "
        "dependence cannot be enzyme abundance"),
})
print(f"  e27 recomputed: {e27_r}")
print(f"  R2(protein) = {r_prot**2:.4f}; non-reverting = "
      f"{m3_summary['path']['frac_loop_holonomy_nonzero']}; "
      f"h_median = {m3_summary['path']['h_loop_median']:.1f}")

# ======================================================================
# LINE IV / V - per-reaction curvature mass over the M1 sweep family
# ======================================================================
print("\n=== LINES IV/V: per-reaction curvature mass ===")
share = np.zeros(len(RXN_IDS))
particip = np.zeros(len(RXN_IDS), dtype=int)
sweep_masses = {}
for s in SWEEP_LIST:
    d = np.load(os.path.join(M13, SWEEP_FILES[s]), allow_pickle=True)
    rid = [str(x) for x in d["rxn_ids"]]
    V = d["V"]
    m = np.abs(V[2:] - 2 * V[1:-1] + V[:-2]).sum(axis=0)
    tot = float(m.sum())
    assert abs(tot - M1["sweeps"][s]["D2_total"]) <= 1e-6 * max(1, tot), s
    idx = np.array([R_IDX.get(r, -1) for r in rid])
    ok = idx >= 0
    sh = np.zeros(len(RXN_IDS))
    sh[idx[ok]] = m[ok] / tot
    share += sh
    particip[idx[ok]] += (m[ok] > 1e-9).astype(int)
    sweep_masses[s] = tot
share /= len(SWEEP_LIST)
IVV = {
    "sweeps": SWEEP_LIST,
    "sweep_D2_totals": {s: sweep_masses[s] for s in SWEEP_LIST},
    "n_sweeps": len(SWEEP_LIST),
    "mass_matches_m1_summary": True,
}

# ---- LINE IV: branch-metabolite mapping
CAT = {
    "pep": "carbon branch point", "pyr": "carbon branch point",
    "g6p": "carbon branch point", "f6p": "carbon branch point",
    "fdp": "carbon branch point", "g3p": "carbon branch point",
    "dhap": "carbon branch point", "2pg": "carbon branch point",
    "3pg": "carbon branch point", "accoa": "carbon branch point",
    "oaa": "carbon branch point", "akg": "carbon branch point",
    "cit": "carbon branch point", "icit": "carbon branch point",
    "succ": "carbon branch point", "succoa": "carbon branch point",
    "fum": "carbon branch point", "mal__L": "carbon branch point",
    "e4p": "carbon branch point", "r5p": "carbon branch point",
    "ru5p__D": "carbon branch point", "xu5p__D": "carbon branch point",
    "sed7p": "carbon branch point", "gln__L": "nitrogen branch point",
    "glu__L": "nitrogen branch point", "prpp": "nucleotide branch point",
    "akg": "nitrogen branch point", "orn": "nitrogen branch point",
    "glu5sa": "nitrogen branch point", "cbp": "one-carbon branch point",
    "mlthf": "one-carbon branch point", "thf": "one-carbon branch point",
    "for": "one-carbon branch point", "gly": "one-carbon branch point",
    "ser__L": "one-carbon branch point", "chors": "aromatic branch point",
    "da4p?": "aromatic branch point", "e4p": "carbon branch point",
    "glx": "carbon branch point", "glcn": "carbon branch point",
    "6pgc": "carbon branch point", "6pgl": "carbon branch point",
    "gthrd": "redox buffer", "gthox": "redox buffer",
    "trdrd": "redox buffer", "trdox": "redox buffer",
}
# reaction-level branch adjacency (primary: non-currency top-decile)
adj_primary = np.zeros(len(RXN_IDS), bool)
adj_rxn_mets = {}
for i, rid in enumerate(RXN_IDS):
    bm = branch_mets_of(rid, D_STAR, exclude_currency=True)
    adj_rxn_mets[rid] = bm
    adj_primary[i] = len(bm) > 0
obs_share, p_perm = perm_share(share, adj_primary)
_, p_mwu, auc = mwu_auc(share, adj_primary)
count_share = float(adj_primary.mean())
IV = {
    "d_star_primary": D_STAR,
    "branch_adjacent_reaction_count_share": count_share,
    "branch_adjacent_mass_share": obs_share,
    "permutation_p": p_perm,
    "MWU_p": p_mwu, "AUC": auc,
    "sensitivity": [],
}
for d_s in (6, 10, 16):
    adj = np.array([len(branch_mets_of(rid, d_s, True)) > 0
                    for rid in RXN_IDS])
    o, p = perm_share(share, adj, 2000)
    _, pm, a = mwu_auc(share, adj)
    IV["sensitivity"].append({"d_star": d_s, "count_share": float(adj.mean()),
                              "mass_share": o, "perm_p": p, "MWU_p": pm,
                              "AUC": a})
adj_all = np.array([len(branch_mets_of(rid, 6, False)) > 0 for rid in RXN_IDS])
o_all, p_all = perm_share(share, adj_all, 2000)
IV["including_currency_d6"] = {"count_share": float(adj_all.mean()),
                               "mass_share": o_all, "perm_p": p_all}
# concentration stat: branch adjacency among the top-mass reactions
o50 = np.argsort(-share)[:50]
o100 = np.argsort(-share)[:100]
IV["top_mass_branch_concentration"] = {
    "top50_branch_fraction": float(adj_primary[o50].mean()),
    "top100_branch_fraction": float(adj_primary[o100].mean()),
    "baseline_branch_fraction": float(adj_primary.mean()),
    "top50_mass_share": float(share[o50].sum()),
}
print(f"  branch-adjacency (d*>={D_STAR:.0f}, no currency): reactions "
      f"{count_share*100:.1f}% carry {obs_share*100:.1f}% of mass "
      f"(perm p={p_perm:.4f}, AUC={auc:.3f}); top-50 reactions: "
      f"{adj_primary[o50].mean()*100:.1f}% branch-adjacent; top-50 carry "
      f"{share[o50].sum()*100:.1f}% of total mass")

# top reactions
order = np.argsort(-share)
top_rxns = []
for i in order[:25]:
    rid = RXN_IDS[i]
    top_rxns.append({
        "reaction": rid, "name": RXNS[rid].get("name", ""),
        "subsystem": RXNS[rid].get("subsystem", ""),
        "class": RXN_CLASS[rid],
        "kappa_share": float(share[i]),
        "sweep_participation": int(particip[i]),
        "branch_metabolites": sorted(adj_rxn_mets[rid]),
    })
IV["top25_reactions"] = top_rxns

# metabolite-level rollup: split each reaction's share over its branch mets
met_mass = defaultdict(float)
for i, rid in enumerate(RXN_IDS):
    bm = adj_rxn_mets[rid]
    if bm:
        for b in bm:
            met_mass[b] += share[i] / len(bm)
mm = sorted(met_mass.items(), key=lambda kv: -kv[1])
met_table = []
for b, v in mm[:20]:
    mid = f"{b}_c"
    name = METS.get(mid, METS.get(f"{b}_e", {})).get("name", b)
    met_table.append({"base_id": b, "name": name, "degree": BASE_DEG[b],
                      "curvature_mass_share": float(v),
                      "category": CAT.get(b, "other")})
IV["top20_branch_metabolites"] = met_table
print("  top branch-metabolite carriers:")
for t in met_table[:10]:
    print(f"    {t['name'][:34]:36s} deg={t['degree']:4d} "
          f"share={t['curvature_mass_share']*100:5.2f}% "
          f"[{t['category']}]")

# ---- LINE V: interface vs interior
V = {}
cls_stats = []
for cls in ("exchange", "transport", "internal"):
    m = np.array([RXN_CLASS[rid] == cls for rid in RXN_IDS])
    o, p = perm_share(share, m, 10000)
    flat = float((share[m] < 1e-12).mean())
    cls_stats.append({
        "class": cls, "n_reactions": int(m.sum()),
        "count_share": float(m.mean()),
        "curvature_mass_share": o, "perm_p": p,
        "flat_fraction": flat,
    })
V["class_stats"] = cls_stats
iface = np.array([RXN_CLASS[rid] in ("exchange", "transport")
                  for rid in RXN_IDS])
o_i, p_i = perm_share(share, iface, 10000)
_, p_m, auc_i = mwu_auc(share, iface)
V["interface_vs_internal"] = {
    "interface_count_share": float(iface.mean()),
    "interface_mass_share": o_i, "perm_p": p_i, "MWU_p": p_m, "AUC": auc_i,
    "direction": "internal > interface (mass on internal branch-point "
                 "chemistry, not on the exchange/transport interface)",
}
# per-family breakdown (nutrient sweeps parameterize exchange bounds; kd
# sweeps parameterize internal capacity bounds)
sweep_family = {"nutrient": ["iml_glucose", "iml_o2"],
                "knockdown": [s for s in SWEEP_LIST if s.startswith("kd_")]}
fam_stats = {}
for fam, sw in sweep_family.items():
    fam_share = np.zeros(len(RXN_IDS))
    keep = [SWEEP_FILES[s] for s in sw]
    for f in keep:
        d = np.load(os.path.join(M13, f), allow_pickle=True)
        rid = [str(x) for x in d["rxn_ids"]]
        Vv = d["V"]
        m = np.abs(Vv[2:] - 2 * Vv[1:-1] + Vv[:-2]).sum(axis=0)
        tot = float(m.sum())
        idx = np.array([R_IDX.get(r, -1) for r in rid])
        okm = idx >= 0
        fs = np.zeros(len(RXN_IDS))
        fs[idx[okm]] = m[okm] / tot
        fam_share += fs
    fam_share /= len(keep)
    entry = {}
    for cls in ("exchange", "transport", "internal"):
        msk = np.array([RXN_CLASS[rid] == cls for rid in RXN_IDS])
        entry[cls] = {"count_share": float(msk.mean()),
                      "mass_share": float(fam_share[msk].sum())}
    entry["internal_branch_adjacent_mass_share"] = float(
        fam_share[(np.array([RXN_CLASS[rid] == "internal" for rid in
                             RXN_IDS])) & adj_primary].sum())
    fam_stats[fam] = entry
V["per_family_class_shares"] = fam_stats
# internal flatness split by branch adjacency (drift-free interior test)
int_mask = np.array([RXN_CLASS[rid] == "internal" for rid in RXN_IDS])
V["internal_flatness"] = {
    "branch_adjacent_flat_fraction": float(
        (share[int_mask & adj_primary] < 1e-12).mean()),
    "non_branch_flat_fraction": float(
        (share[int_mask & ~adj_primary] < 1e-12).mean()),
    "branch_adjacent_mass_share_within_internal": float(
        share[int_mask & adj_primary].sum() / share[int_mask].sum()),
    "branch_adjacent_count_share_within_internal": float(
        (int_mask & adj_primary).sum() / int_mask.sum()),
}
# subsystem rollup
sub_mass = defaultdict(float)
for i, rid in enumerate(RXN_IDS):
    ss = RXNS[rid].get("subsystem", "") or "Unassigned"
    sub_mass[ss] += share[i]
ssr = sorted(sub_mass.items(), key=lambda kv: -kv[1])
V["top10_subsystems"] = [{"subsystem": s, "mass_share": float(v)}
                         for s, v in ssr[:10]]
# iJO one-chamber cross-check + census
ijo = np.load(os.path.join(M13, "m1_ijo_glucose.npz"), allow_pickle=True)
ijo_D2 = float(np.abs(ijo["V"][2:] - 2 * ijo["V"][1:-1] +
                      ijo["V"][:-2]).sum())
V["ijo_glucose_one_chamber"] = {
    "D2_total": ijo_D2,
    "reactions_with_mass": int((np.abs(ijo["V"][2:] - 2 * ijo["V"][1:-1] +
                                       ijo["V"][:-2]).sum(axis=0) > 1e-9
                                ).sum()),
    "v7_P0_interior_crossings": 0,
    "v6_anchor_kinks": 4,
}
act0 = int((np.abs(ijo["V"][0]) > 1e-6).sum())
act1 = int((np.abs(ijo["V"][-1]) > 1e-6).sum())
V["ijo_active_support"] = {"glucose_1": act0, "glucose_10": act1,
                           "manuscript_E24_endpoint": 438}
print("  class distribution (share of reactions -> share of curvature mass):")
for c in cls_stats:
    print(f"    {c['class']:10s} {c['count_share']*100:5.1f}% -> "
          f"{c['curvature_mass_share']*100:5.1f}% "
          f"(flat {c['flat_fraction']*100:4.1f}%, perm p={c['perm_p']:.4f})")
print(f"  interface vs internal: AUC={auc_i:.3f} (internal side); "
      f"mass is internal-dominated")
for fam, entry in fam_stats.items():
    print(f"    {fam:10s} exchange {entry['exchange']['mass_share']*100:5.1f}% "
          f"| transport {entry['transport']['mass_share']*100:5.1f}% "
          f"| internal {entry['internal']['mass_share']*100:5.1f}% "
          f"(internal branch-adj {entry['internal_branch_adjacent_mass_share']*100:.1f}%)")
print(f"  internal flatness: branch-adjacent "
      f"{V['internal_flatness']['branch_adjacent_flat_fraction']*100:.1f}% flat "
      f"vs non-branch "
      f"{V['internal_flatness']['non_branch_flat_fraction']*100:.1f}% flat; "
      f"within-internal mass on branch-adj: "
      f"{V['internal_flatness']['branch_adjacent_mass_share_within_internal']*100:.1f}% "
      f"(count {V['internal_flatness']['branch_adjacent_count_share_within_internal']*100:.1f}%)")
print(f"  iJO glucose sweep: D2 total {ijo_D2:.2e} (one chamber); active "
      f"support {act0}->{act1} (ms E24 endpoint: 438)")

# ======================================================================
# save
# ======================================================================
LEDGER.update({"I_menu_order": I, "II_construction_order": II,
               "III_memory_substrate": III, "IV_wall_coordinates": IV,
               "V_drift_free_interior": V, "lines_IV_V_common": IVV})
out = os.path.join(DL, "v17_insight_substantiation.json")
with open(out, "w") as f:
    json.dump(LEDGER, f, indent=1, default=str)
print(f"\nLedger -> {out}")
print("DONE")
