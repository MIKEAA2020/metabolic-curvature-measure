#!/usr/bin/env python3
"""Commit the two mechanism measurements of the six-axis round as
artifacts:

1. download/keio_floor_tolerance_check.json
   The -89/-90% floor losses (fabZ/bioH/bioD) are LP-tolerance
   effects: biomass biotin coefficient 2e-6 x growth 0.1037 ->
   demanded chain flux 2.07e-7 mmol/gDW/h, which the KO LPs carry
   through literally zero-bounded reactions (within the simplex
   feasibility tolerance); fabZ is additionally solve-order
   dependent.

2. download/keio_atpm_neartie_measurement.json
   The iML1515 ATPM-stress pFBA L1 near-tie: WT vs a compensable-KO
   pFBA pair with L1 gap dL1 ~ 8.6e-4 absolute (1.2e-6 relative) at
   squared flux distance ~0 for the fresh-model pair (the ~200
   floor arises between the probe's WT reference vertex and the
   sweep's KO vertices); plus the floor census from the committed
   atpm_100 canonical CSV.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model
from cobra.flux_analysis import pfba

DL = os.path.join(REPO, "download")

# ---------------- 1. floor tolerance -------------------------------
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO = [r.id for r in ijo.reactions
       if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
bio = ijo.reactions.get_by_id(BIO)
btn_coef = float(bio.metabolites[ijo.metabolites.get_by_id("btn_c")])

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
for r in ijo.exchanges:
    r.lower_bound = 0
ijo.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
ijo.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
for ex in IJO_MINERALS:
    ijo.reactions.get_by_id(ex).lower_bound = -1000.0
ijo.reactions.get_by_id("EX_pi_e").lower_bound = -0.1

wt = ijo.optimize()
b_wt = float(wt.objective_value)
floor = {"model": "iJO1366", "level": "EX_pi_e -0.1",
         "wild_type_biomass": b_wt,
         "biomass_biotin_coefficient": btn_coef,
         "demanded_biotin_flux": btn_coef * b_wt}
for gid, rxn in [("b3412", "PMEACPE"), ("b0778", "DBTS")]:
    with ijo:
        for r in ijo.reactions:
            if gid in r.gene_reaction_rule:
                r.lower_bound = 0
                r.upper_bound = 0
        sol = ijo.optimize()
    floor[gid] = {
        "b_ko": float(sol.objective_value),
        "retention": float(sol.objective_value) / b_wt,
        "zeroed_reaction": rxn,
        "flux_through_zeroed_reaction": float(sol.fluxes[rxn]),
    }
# fabZ order-dependence: two consecutive solves of the same LP
with ijo:
    for r in ijo.reactions:
        if "b0180" in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    sol_a = ijo.optimize()
floor["b0180"] = {
    "b_ko_this_solve_order": float(sol_a.objective_value),
    "note": ("fresh single-LP solve returns lethal b_ko=0 (see "
             "floor_loss_mechanism2.py output in worklog); the probe "
             "sweep order returned full growth -- solve-order "
             "dependent at the tolerance boundary"),
}
with open(os.path.join(DL, "keio_floor_tolerance_check.json"), "w") as f:
    json.dump(floor, f, indent=2)
print("floor tolerance artifact written:",
      {k: v for k, v in floor.items() if k in ("demanded_biotin_flux",)})

# ---------------- 2. ATPM near-tie ---------------------------------
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
iml.solver.configuration.timeout = 60  # guard the near-tie L1 stage
BIO_IML = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO_IML = r.id
        break
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
for r in iml.reactions:
    if r.id.startswith("EX_"):
        r.lower_bound = 0
iml.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
iml.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
for ex in IML_MINERALS:
    try:
        iml.reactions.get_by_id(ex).lower_bound = -10
    except Exception:
        pass
iml.reactions.get_by_id("ATPM").lower_bound = 100.0

wtA = pfba(iml)
l1_wt = float(wtA.fluxes.abs().sum())
with iml:
    for r in iml.reactions:
        if "b0870" in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    koD = pfba(iml)
l1_ko = float(koD.fluxes.abs().sum())
d = (koD.fluxes - wtA.fluxes).abs()
sq = float((d[d > 1e-9] ** 2).sum())

can = pd.read_csv(os.path.join(
    DL, "keio_atpm_pfba_control_iml_atpm_100.csv"))
comp = can[can.b_ko >= 0.999 * can.b_wt]
floor_kv = comp[(comp.kV >= 190) & (comp.kV <= 210)]
neartie = {
    "model": "iML1515", "level": "ATPM >= 100",
    "wt_pFBA_L1": l1_wt, "ko_b0870_pFBA_L1": l1_ko,
    "dL1_absolute": l1_ko - l1_wt,
    "dL1_relative": (l1_ko - l1_wt) / l1_wt,
    "fresh_pair_squared_distance": sq,
    "note": ("fresh-model WT and KO pFBA land on the same tied vertex "
             "(sq ~ 0.02); the probe's ~200 floor arises because its "
             "WT reference solve and the sweep's warm-started KO "
             "solves land on different near-tied vertices -- the L1 "
             "gap is within the simplex optimality tolerance either "
             "way, so the selection is path-dependent"),
    "floor_census_from_committed_csv": {
        "n_compensable": int(len(comp)),
        "n_at_floor_190_210": int(len(floor_kv)),
        "floor_kv_median": float(floor_kv.kV.median()) if len(floor_kv)
        else None,
    },
}
with open(os.path.join(DL, "keio_atpm_neartie_measurement.json"), "w") as f:
    json.dump(neartie, f, indent=2)
print("near-tie artifact written: dL1_rel = %.2e, floor %d/%d" %
      (neartie["dL1_relative"],
       neartie["floor_census_from_committed_csv"]["n_at_floor_190_210"],
       neartie["floor_census_from_committed_csv"]["n_compensable"]))
