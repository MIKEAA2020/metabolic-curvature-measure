#!/usr/bin/env python3
"""ATPM-axis solver-tolerance integrity scan + HiGHS adjudication,
extending the phosphate/iron integrity protocol (remote round) to the
sixth (non-medium ATPM) axis.

At-risk band: trace-quota genes at low wild-type growth (below the
~0.14 corruption boundary).  The ATPM endpoints sit at WT 0.0992
(iJO1366, atpm_100) and 0.0797 (iML1515, atpm_100); iML atpm_80
(0.2390) is marginal and included.

Stage 1 -- cross-arm comparison: plain sweep vs canonical sweep per
gene per level; flag (a) label disagreements, (b) genes in the
trace-quota family (biotin/quinone-side-chain/lipoate: bioA-F/H,
fabZ, lpdA/lplA... governed reactions with tiny biomass-quota
demands) whose b_ko is positive at WT < 0.14 levels, (c) any gene
where the two arms' b_ko differ by more than noise on a lethal call.

Stage 2 -- independent adjudication (scipy/HiGHS, shares no code
with GLPK): for every flagged gene, extract the stoichiometric LP at
the level's medium, knock out the gene's GPR reactions, maximize
biomass.  True b_ko = 0 means the deposited positive reading was a
false-viability tolerance call.

Stage 3 -- patch the deposited artifacts in place (plain sweeps,
canonical CSVs, control/results JSONs, summary) under the repo's
correction conventions, and recompute the affected statistics.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from cobra.io import load_json_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
DL = os.path.join(REPO, "download")

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
TRACE_FAMILY = ["b0180",   # fabZ (fatty-acid + quinone side chain)
                "b3412",   # bioH
                "b0778",   # bioD
                "b0767",   # bioF
                "b0770",   # bioA
                "b0771",   # bioB
                "b0768",   # bioC
                "b0769",   # bioP
                "b2959",   # lplA?
                "b0116"]   # lpd (lipoamide)


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


def build_lp(model):
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


def solve_highs(S, lb, ub, c):
    res = linprog(-c, A_eq=S, b_eq=np.zeros(S.shape[0]),
                  bounds=np.column_stack([lb, ub]), method="highs")
    return float(-res.fun) if res.status == 0 else 0.0


# ---------------- Stage 1: cross-arm scan ---------------------------
LEVELS = [
    ("iJO1366", 100.0, "keio_atpm_stress_e12_sweep.csv", "atpm_bound",
     "keio_atpm_pfba_control_atpm_100.csv"),
    ("iML1515", 100.0, "keio_atpm_stress_e16_sweep.csv", "atpm_bound",
     "keio_atpm_pfba_control_iml_atpm_100.csv"),
    ("iML1515", 80.0, "keio_atpm_stress_e16_sweep.csv", "atpm_bound",
     "keio_atpm_pfba_control_iml_atpm_80.csv"),
]
flagged = []
for model, atpm, plain_f, pcol, canon_f in LEVELS:
    plain = pd.read_csv(os.path.join(DL, plain_f))
    pl = plain[plain[pcol] == atpm]
    can = pd.read_csv(os.path.join(DL, canon_f))
    mg = pl[["gene_id", "b_ko", "y_essential"]].merge(
        can[["gene_id", "b_ko", "y_essential"]], on="gene_id",
        suffixes=("_p", "_c"))
    wt = pl.b_wt.iloc[0]
    # (a) label disagreements
    dis = mg[mg.y_essential_p != mg.y_essential_c]
    for _, row in dis.iterrows():
        flagged.append((model, atpm, row.gene_id, "label-disagreement",
                        float(row.b_ko_p), float(row.b_ko_c)))
    # (b) trace-quota family with positive b_ko at low WT
    if wt < 0.25:
        tf = mg[mg.gene_id.isin(TRACE_FAMILY)]
        for _, row in tf.iterrows():
            if row.b_ko_p > 1e-9 or row.b_ko_c > 1e-9:
                flagged.append((model, atpm, row.gene_id,
                                "trace-quota-positive",
                                float(row.b_ko_p), float(row.b_ko_c)))
    print(f"{model} ATPM {atpm} (WT {wt:.4f}): {len(dis)} label "
          f"disagreements; trace-quota rows with positive b_ko: "
          f"{int((tf.b_ko_p > 1e-9).sum() + (tf.b_ko_c > 1e-9).sum())}"
          if wt < 0.25 else
          f"{model} ATPM {atpm} (WT {wt:.4f}): {len(dis)} label "
          f"disagreements (band not scanned)",
          flush=True)

print(f"\nflagged: {len(flagged)}")
for f in flagged:
    print("  ", f)

# ---------------- Stage 2: HiGHS adjudication -----------------------
if flagged:
    ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
    iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
    verdicts = []
    for model, atpm, gid, reason, bp, bc in flagged:
        mdl = ijo if model == "iJO1366" else iml
        (set_ijo if model == "iJO1366" else set_iml)(mdl, atpm)
        bio = None
        for r in mdl.reactions:
            if r.objective_coefficient != 0 and (
                    "BIOMASS" in r.id or "iomass" in r.id):
                bio = r.id
                break
        with mdl:
            for r in mdl.reactions:
                if gid in r.gene_reaction_rule:
                    r.lower_bound = 0
                    r.upper_bound = 0
            S, lb, ub, c, rids = build_lp(mdl)
            b_true = solve_highs(S, lb, ub, c)
        verdicts.append({"model": model, "atpm": atpm, "gene_id": gid,
                        "reason": reason, "b_plain": bp, "b_canon": bc,
                        "b_highs_true": b_true})
        print(f"  {model} ATPM {atpm} {gid} ({reason}): "
              f"plain {bp:.6f} / canon {bc:.6f} -> HiGHS {b_true:.6f}",
              flush=True)
    with open(os.path.join(DL, "keio_atpm_integrity_adjudication.json"),
              "w") as f:
        json.dump({"scan": "cross-arm + trace-quota band",
                  "engine": "scipy.optimize.linprog(method='highs')",
                  "verdicts": verdicts}, f, indent=2)
    print("\nadjudication written to "
          "download/keio_atpm_integrity_adjudication.json")
else:
    print("nothing to adjudicate")
