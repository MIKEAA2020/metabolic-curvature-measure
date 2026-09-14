#!/usr/bin/env python3
"""Fourth-axis pre-screen: phosphate (EX_pi_e) vs sulfur (EX_so4_e)
limitation dose responses on iJO1366 and iML1515, under the glucose-
only corrected medium (EX_tre_e closed).

Purpose: choose the fourth supply-side perturbation axis by data, not
by convention.  For each candidate we record the WT optimum across a
level grid, the baseline uptake at unlimited supply, and at-optimum
FVA widths of the carbon/energy sector (PGI, CS, ACKr, G6PDH2r,
glucose exchange) -- the degeneracy signature that the nitrogen axis
showed to scramble plain-FBA curvature statistics.

Artifacts: download/keio_fourth_axis_prescreen.json
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]

P_GRID = [-10.0, -5.0, -2.5, -1.0, -0.5, -0.25, -0.1]
S_GRID = [-10.0, -5.0, -2.5, -1.0, -0.5, -0.25, -0.1]


def set_ijo(model, axis_lb=None, axis_id=None):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    if axis_id is not None:
        model.reactions.get_by_id(axis_id).lower_bound = axis_lb


def set_iml(model, axis_lb=None, axis_id=None):
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
    if axis_id is not None:
        model.reactions.get_by_id(axis_id).lower_bound = axis_lb


def probe(model, axis_id, grid, setter, label):
    out = {"axis_exchange": axis_id, "levels": {}}
    setter(model)  # baseline, unlimited
    base = model.optimize()
    bio_id = None
    for r in model.reactions:
        if r.objective_coefficient != 0 and (
                "iomass" in r.id or "BIOMASS" in r.id):
            bio_id = r.id
            break
    if bio_id is None:  # fall back to the objective's first reaction
        bio_id = str(model.objective.expression.free_symbols.pop())\
            .split("*")[1].strip() if len(
                model.objective.expression.free_symbols) == 1 else None
        bio_id = bio_id.rsplit("_reverse_", 1)[0] if bio_id else None
    assert bio_id, "biomass reaction not found"
    base_upt = float(-base.fluxes[axis_id])
    out["baseline_biomass"] = round(float(base.objective_value), 6)
    out["baseline_unlimited_uptake"] = round(base_upt, 4)
    print(f"\n{label}: baseline WT {base.objective_value:.6f}, "
          f"{axis_id} uptake {base_upt:.4f}", flush=True)
    for lb in grid:
        setter(model, lb, axis_id)
        sol = model.optimize()
        if sol.status != "optimal" or sol.objective_value < 1e-9:
            out["levels"][str(lb)] = {"biomass": 0.0,
                                      "uptake": round(float(
                                          -sol.fluxes.get(axis_id, 0.0)), 4)}
            print(f"  {axis_id} >= {lb}: WT 0.000000 (infeasible/zero)")
            continue
        par = pfba(model)
        fr = fva(model, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
        widths = {rid: round(float(fr.loc[rid, "maximum"]
                                  - fr.loc[rid, "minimum"]), 3)
                  for rid in FVA_TARGETS}
        wide = {r: w for r, w in widths.items() if w > 1e-6 and r != "ACKr"}
        out["levels"][str(lb)] = {
            "biomass": round(float(sol.objective_value), 6),
            "reduction_pct": round(100 * (1 - sol.objective_value
                                          / out["baseline_biomass"]), 1),
            "uptake": round(float(-sol.fluxes[axis_id]), 4),
            "pfba_glc_uptake": round(float(-par.fluxes.EX_glc__D_e), 3),
            "raw_glc_uptake": round(float(-sol.fluxes.EX_glc__D_e), 3),
            "fva_widths_excl_ACKr": wide,
            "fva_PGI_width": widths.get("PGI"),
        }
        print(f"  {axis_id} >= {lb}: WT {sol.objective_value:.6f} "
              f"(-{out['levels'][str(lb)]['reduction_pct']}%), "
              f"glc raw {-sol.fluxes.EX_glc__D_e:.2f} / "
              f"pFBA {-par.fluxes.EX_glc__D_e:.2f}, "
              f"PGI width {widths.get('PGI')}", flush=True)
    return out


result = {}
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
result["iJO1366_phosphate"] = probe(ijo, "EX_pi_e", P_GRID, set_ijo,
                                    "iJO1366 phosphate")
result["iJO1366_sulfur"] = probe(ijo, "EX_so4_e", S_GRID, set_ijo,
                                 "iJO1366 sulfur")
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
result["iML1515_phosphate"] = probe(iml, "EX_pi_e", P_GRID, set_iml,
                                    "iML1515 phosphate")
result["iML1515_sulfur"] = probe(iml, "EX_so4_e", S_GRID, set_iml,
                                 "iML1515 sulfur")

with open(os.path.join(OUT_DIR, "keio_fourth_axis_prescreen.json"), "w") as f:
    json.dump(result, f, indent=2)
print("\nprescreen written.")
