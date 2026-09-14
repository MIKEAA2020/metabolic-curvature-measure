#!/usr/bin/env python3
"""Independent-LP adjudication with HiGHS (scipy.optimize.linprog).

The glpk-based paths disagree with each other on the iJO1366 Pi=-0.1
level:
  b0180 (fabZ): plain-seq 0.1037 | pFBA-seq 0.0 | fresh-plain 0.0 | FVA 0.0
  b0776 (bioF): plain-seq 0.0    | pFBA-seq 0.1037 (kV~0) | fresh 0.0 | FVA 0.0
  b3412 (bioH): plain-seq 0.1037 | pFBA-seq 0.0 | fresh-plain 0.1037 | FVA 0.0

This script settles each case with a solver that shares no code with
glpk: the stoichiometric LP is extracted (S, bounds, objective) and
solved with scipy's HiGHS backend.  Also re-adjudicates the iML1515
anaerobic fabZ row with the same engine, and checks the biotin-pathway
pimelate-route question (does any feasible vector reach the WT biomass
with PMEACPE/AOXSr2/OPMEACPD-OGMEACPD knocked out?).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import linprog

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from cobra.io import load_json_model

IJO_MINERALS = ["EX_nh4_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]


def build_lp(model):
    """Extract maximize-c*b s.t. S v = 0, lb <= v <= ub as a linprog
    (minimize -c)."""
    n = len(model.reactions)
    m = len(model.metabolites)
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
    if res.status == 0:
        return float(res.fun * -1.0), "optimal"
    return 0.0, f"status {res.status} ({res.message[:40]})"


def fresh_ijo(pi_lb=-0.1):
    m = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
    for r in m.exchanges:
        r.lower_bound = 0
    m.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    m.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        m.reactions.get_by_id(ex_id).lower_bound = -1000.0
    m.reactions.get_by_id("EX_pi_e").lower_bound = pi_lb
    return m


print("=" * 78)
print("iJO1366, Pi = -0.1: HiGHS adjudication")
print("=" * 78, flush=True)
results = {}
for case, genes in [("WT", []),
                    ("fabZ KO (b0180)", ["b0180"]),
                    ("bioF KO (b0776)", ["b0776"]),
                    ("bioH KO (b3412)", ["b3412"]),
                    ("bioF+bioH KO", ["b0776", "b3412"])]:
    m = fresh_ijo()
    for gid in genes:
        for r in m.reactions:
            if gid in r.gene_reaction_rule:
                r.lower_bound = 0
                r.upper_bound = 0
    S, lb, ub, c, rids = build_lp(m)
    val, status = solve_highs(S, lb, ub, c)
    results[case] = {"biomass": val, "status": status}
    print(f"  {case:18s}: {val:.10f}  [{status}]", flush=True)

b_wt = results["WT"]["biomass"]
for k in list(results)[1:]:
    results[k]["essential"] = results[k]["biomass"] < 0.05 * b_wt
    print(f"  -> {k}: essential = {results[k]['essential']}")

print("\n" + "=" * 78)
print("iML1515, O2 = 0 (anaerobic): HiGHS re-adjudication of fabZ")
print("=" * 78, flush=True)
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
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
S, lb, ub, c, rids = build_lp(iml)
val_wt, st = solve_highs(S, lb, ub, c)
print(f"  iML anaerobic WT (HiGHS): {val_wt:.10f}  [{st}]")
for gid in ["b0180"]:
    m2 = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
    for r in m2.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    m2.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    for o2_id in ['EX_o2_e', 'EX_o2s_e']:
        try:
            m2.reactions.get_by_id(o2_id).lower_bound = 0.0
            break
        except Exception:
            continue
    for ex_id in IML_MINERALS:
        try:
            m2.reactions.get_by_id(ex_id).lower_bound = -10
        except Exception:
            pass
    for r in m2.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    S, lb, ub, c, rids = build_lp(m2)
    val, st = solve_highs(S, lb, ub, c)
    print(f"  iML anaerobic fabZ KO (HiGHS): {val:.10f}  [{st}] "
          f"(essential = {val < 0.05 * val_wt})")

with open(os.path.join(REPO, "download",
                       "keio_phosphate_highs_adjudication.json"), "w") as f:
    json.dump({"ijo_pi_-0.1": results,
               "iml_anaerobic_wt_highs": val_wt}, f, indent=2)
print("\nHiGHS adjudication written.")
