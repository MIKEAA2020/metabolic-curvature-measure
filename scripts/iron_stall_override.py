#!/usr/bin/env python3
"""Generate HiGHS stall overrides for the iron probe.

GLPK's simplex hangs (cycling on a degenerate vertex) on isolated
gene-KO LPs under the deepest iron limitation -- empirically: the
iJO1366 plain sweep at EX_fe2_e = -0.0025 stalls on the first
GPR-bearing gene after the anchor gene in model.genes order (two
chunks died there; no OOM events; all neighbouring solves run at
0.02 s/gene).

This script pinpoints that gene, solves its KO LP with the repo's
deterministic scipy/HiGHS engine (scripts/lp_engine.py) under BOTH
probe conventions --
  PLAIN  : stage-1 max-biomass vertex          (lp_engine stage 1)
  CANON  : stage-1 + stage-2 min-L1 vertex     (cobra-pfba equivalent)
-- and stores the flux vectors (CSV) + metadata (JSON) so the probe
can compute kV against its own WT references and append the row
without ever calling GLPK on the stalled gene.

KO convention matches the probe exactly: every reaction whose GPR
mentions the gene is zeroed (E12 convention), NOT the stricter
DNF-disabled set.

Usage:  iron_stall_override.py <ijo|iml> <level_key> <anchor_gene_id>
Artifacts (download/):
  keio_iron_stall_<key>_<model>_<gid>.csv    (rxn, v_plain, v_canon)
  keio_iron_stall_overrides.json             (registry)
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from lp_engine import LPEngine

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def set_ijo_fe(model, fe_lb):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("EX_fe2_e").lower_bound = fe_lb


def set_iml_fe(model, fe_lb):
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
    model.reactions.get_by_id("EX_fe2_e").lower_bound = fe_lb
    model.reactions.get_by_id("EX_fe3_e").lower_bound = 0


def solve_stages(eng, lb, ub, bio_idx, mu_tol=1e-9):
    """Stage-1 (max biomass) and stage-1+2 (pFBA) HiGHS solves.
    Returns (v_plain, v_canon, mu) or (None, None, None)."""
    R = eng.R
    fub = np.maximum(ub, 0.0)
    rub = np.maximum(-lb, 0.0)
    vlb = np.concatenate([lb, np.zeros(R), np.zeros(R)])
    vub = np.concatenate([ub, fub, rub])
    c1 = np.zeros(3 * R)
    c1[:R] = -eng.c_bio
    res = eng._lp(c1, np.column_stack((vlb, vub)))
    if not res.success:
        return None, None, None
    mu = float(res.x[bio_idx])
    v_plain = res.x[:R].copy()
    vlb2 = vlb.copy()
    vlb2[bio_idx] = max(vlb2[bio_idx], mu - mu_tol * max(1.0, abs(mu)))
    c2 = np.concatenate([np.zeros(R), np.ones(R), np.ones(R)])
    res2 = eng._lp(c2, np.column_stack((vlb2, vub)))
    if not res2.success:
        return v_plain, None, mu
    return v_plain, res2.x[:R].copy(), mu


def main():
    which, key, anchor = sys.argv[1], sys.argv[2], sys.argv[3]
    fe_lb = -float(key.split("_")[1])
    assert which in ("ijo", "iml") and key.startswith("fe_"), sys.argv

    if which == "ijo":
        model = load_json_model(os.path.join(
            REPO, "data/bigg_models/iJO1366.json"))
        setter = set_ijo_fe
    else:
        model = load_json_model(os.path.join(
            REPO, "data/bigg_models/iML1515.json"))
        setter = set_iml_fe
    setter(model, fe_lb)

    genes = list(model.genes)
    ids = [g.id for g in genes]
    i0 = ids.index(anchor)
    suspect = None
    for i in range(i0 + 1, len(genes)):
        gpr = [r for r in genes[i].reactions if genes[i] in r.genes]
        print(f"  {i}: {genes[i].id} gpr_rxns={len(gpr)}")
        if gpr:
            suspect = (i, genes[i], gpr)
            break
    assert suspect, "no GPR-bearing gene after anchor"
    i, gene, gpr_rxns = suspect
    print(f"SUSPECT: {gene.id} (index {i}), "
          f"{len(gpr_rxns)} GPR reactions: {[r.id for r in gpr_rxns]}",
          flush=True)

    # objective + biomass index
    bio_idx = None
    c_bio = np.zeros(len(model.reactions))
    for j, r in enumerate(model.reactions):
        if r.objective_coefficient != 0:
            c_bio[j] = float(r.objective_coefficient)
            if "iomass" in r.id or "BIOMASS" in r.id:
                bio_idx = j
    assert bio_idx is not None, "biomass objective reaction not found"

    t0 = time.time()
    eng = LPEngine(model, np.zeros(len(model.reactions)), c_bio)
    lb = np.array([r.lower_bound for r in model.reactions])
    ub = np.array([r.upper_bound for r in model.reactions])
    for r in gpr_rxns:  # E12 convention: zero every GPR-mentioning reaction
        lb[eng.index[r.id]] = 0.0
        ub[eng.index[r.id]] = 0.0
    v_plain, v_canon, mu = solve_stages(eng, lb, ub, bio_idx)
    dt = time.time() - t0
    assert v_plain is not None, "HiGHS stage-1 failed"
    b_plain = float(v_plain[bio_idx])
    b_canon = float(v_canon[bio_idx]) if v_canon is not None else None
    print(f"HiGHS solves done in {dt:.1f}s: mu = {mu:.9f}; "
          f"plain b_ko = {b_plain:.9f}; canon b_ko = {b_canon}",
          flush=True)

    csv_path = os.path.join(
        OUT_DIR, f"keio_iron_stall_{key}_{which}_{gene.id}.csv")
    pd.DataFrame({
        "rxn": eng.rxn_ids,
        "v_plain": v_plain,
        "v_canon": v_canon if v_canon is not None else np.full(eng.R, np.nan),
    }).to_csv(csv_path, index=False)

    reg_path = os.path.join(OUT_DIR, "keio_iron_stall_overrides.json")
    reg = {}
    if os.path.exists(reg_path):
        try:
            reg = json.load(open(reg_path))
        except Exception:
            reg = {}
    reg.setdefault(key, {}).setdefault(which, [])
    entry = {"gene_id": gene.id, "csv": csv_path,
             "mu": mu, "b_ko_plain": b_plain,
             "b_ko_canon": b_canon,
             "note": ("GLPK plain-FBA hang (simplex cycling on a "
                      "degenerate vertex); HiGHS stage-1 / stage-1+2 "
                      "vertices, E12 KO convention")}
    if not any(e["gene_id"] == gene.id for e in reg[key][which]):
        reg[key][which].append(entry)
    with open(reg_path, "w") as f:
        json.dump(reg, f, indent=2)
    print(f"override written: {csv_path}")
    print(f"registry updated: {reg_path}")


if __name__ == "__main__":
    main()
