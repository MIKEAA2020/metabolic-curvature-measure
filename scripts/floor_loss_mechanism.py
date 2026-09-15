#!/usr/bin/env python3
"""Mechanism check for the extreme-limitation floor losses: why do
fabZ (b0180), bioH (b3412), bioD (b0778) -- strictly lethal at the
glucose-only baseline -- become FULLY compensable (b_ko = b_wt) at
the -90% floors (phosphate/iron/ATPM)?

Candidate mechanism: isoenzyme/alternative-route coverage that only
activates at reduced flux demand.  This script solves the floor-level
KO LPs and reports the flux through the relevant alternative routes
(biotin synthesis chain, fabA vs fabZ), plus the baseline contrast.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model

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

WATCH = ["BIOT2", "BIOT3", "BTN5L", "BTN5R", "BTS5", "EX_btn_e",
         "bioA-reaction", "FABZ", "fabA-reaction"]
bio_rxns = [r.id for r in ijo.reactions
            if r.id.upper().startswith(("BIOT", "BTN", "BTS"))]
fab_rxns = [r.id for r in ijo.reactions if r.id.startswith("FAB")]
print("biotin-side reactions:", bio_rxns)
print("fatty-acid reactions:", fab_rxns[:12], flush=True)

for label, kw, gid in [
        ("baseline", {}, "b3412"),
        ("pi -0.1", {"pi": -0.1}, "b3412"),
        ("pi -0.1", {"pi": -0.1}, "b0180"),
        ("atpm 100", {"atpm": 100.0}, "b3412")]:
    set_ijo(ijo, **kw)
    with ijo:
        for r in ijo.reactions:
            if gid in r.gene_reaction_rule:
                r.lower_bound = 0
                r.upper_bound = 0
        sol = ijo.optimize()
        b = float(sol.objective_value)
    print(f"\n{label}, KO {gid}: b_ko = {b:.6f}", flush=True)
    if b > 1e-9:
        for rid in bio_rxns + fab_rxns + ["EX_btn_e"]:
            try:
                v = float(sol.fluxes[rid])
            except Exception:
                continue
            if abs(v) > 1e-9:
                print(f"    {rid:12s} {v:+.4f}")
print("\nDONE")
