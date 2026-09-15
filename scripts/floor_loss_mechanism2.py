#!/usr/bin/env python3
"""Careful floor-loss mechanism check v2: resolve the actual reactions
governed by b0180 (fabZ), b3412 (bioH), b0778 (bioD) via GPR, then
solve the floor-level KO LPs both fresh AND warm-started (reproducing
the probe's solve order), reporting the governing reactions' fluxes
and the biotin content of the biomass objective.

Motivation: the phosphate/iron probe sweeps recorded b_ko = b_wt
(retention 1.0, i.e. these genes LOSE essentiality at the -90%
floors), while a fresh single-LP recomputation of the same KO gives
b_ko = 0.  At ATPM=100 both agree on neutrality.  Determine whether
the pi/fe floor losses are genuine (alternative route at reduced
demand) or vertex/solver artifacts.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model
from cobra.flux_analysis import pfba

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]


def set_ijo(model, pi=None, fe=None, atpm=None):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex in IJO_MINERALS:
        model.reactions.get_by_id(ex).lower_bound = -1000.0
    if pi is not None:
        model.reactions.get_by_id("EX_pi_e").lower_bound = pi
    if fe is not None:
        model.reactions.get_by_id("EX_fe2_e").lower_bound = fe
    if atpm is not None:
        model.reactions.get_by_id("ATPM").lower_bound = atpm


ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO = [r.id for r in ijo.reactions
       if "BIOMASS" in r.id and r.objective_coefficient != 0][0]

# 1. governing reactions per gene
GOV = {}
for gid in ["b0180", "b3412", "b0778"]:
    GOV[gid] = [r.id for r in ijo.reactions if gid in r.gene_reaction_rule]
    print(f"{gid} governs: {GOV[gid]}")

# 2. biotin (btn_c) in the biomass reaction
bio = ijo.reactions.get_by_id(BIO)
btn = [(m, c) for m, c in bio.metabolites.items() if "btn" in m.id]
print(f"biomass biotin content: {btn}", flush=True)

# 3. WT biotin synthase flux at baseline (BTS5 = biotin synthase)
set_ijo(ijo)
wt0 = ijo.optimize()
print(f"baseline WT b={float(wt0.objective_value):.4f}, "
      f"BTS5={float(wt0.fluxes['BTS5']):+.4f}", flush=True)

# 4. floor KOs, fresh solve, reporting governing-reaction fluxes
for label, kw, gid in [
        ("pi -0.1", {"pi": -0.1}, "b3412"),
        ("pi -0.1", {"pi": -0.1}, "b0180"),
        ("fe -0.0016", {"fe": -0.0016}, "b0180"),
        ("atpm 100", {"atpm": 100.0}, "b3412")]:
    set_ijo(ijo, **kw)
    wt = ijo.optimize()
    b_wt = float(wt.objective_value)
    with ijo:
        for r in ijo.reactions:
            if gid in r.gene_reaction_rule:
                r.lower_bound = 0
                r.upper_bound = 0
        sol = ijo.optimize()
        b = float(sol.objective_value)
    print(f"\n{label} KO {gid}: b_wt={b_wt:.4f}, b_ko={b:.6f} "
          f"(retention {b/b_wt:.4f}) status={sol.status}", flush=True)
    for rid in GOV[gid]:
        print(f"    gov {rid}: WT {float(wt.fluxes[rid]):+.4f} "
              f"-> KO {float(sol.fluxes[rid]):+.4f}")
    for rid in ["BTS5", "BTNt2ipp", "BTNtex"]:
        print(f"    {rid}: WT {float(wt.fluxes[rid]):+.4f} "
              f"-> KO {float(sol.fluxes[rid]):+.4f}")
print("\nDONE")
