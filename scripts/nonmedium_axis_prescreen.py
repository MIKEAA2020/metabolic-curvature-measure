#!/usr/bin/env python3
"""Sixth-axis pre-screen: NON-MEDIUM perturbation encodings.

Genome-scale FBA has no temperature or pH state variables; the two
standard constraint-based surrogates are pre-screened here, head to
head, under the glucose-only corrected medium (EX_tre_e closed):

  (T) ATP-maintenance escalation (temperature-style stress):
      raise the ATPM lower bound (non-growth-associated maintenance,
      default 6.86 mmol ATP/gDW/h) across a grid.  Higher maintenance
      = the canonical FBA encoding of temperature-style stress
      (protein turnover/repair diverts energy flux from growth).

  (P) proton-leak forcing (pH-style stress):
      force a net proton SECRETION floor on EX_h_e (lower bound +X).
      Encodes the acid-stress homeostasis burden: at low external pH
      the cell must export protons, paid for by the reversed F1F0
      ATPase / extra respiration.

For each candidate and level we record the WT optimum, pFBA glucose
uptake, and at-optimum FVA widths of the carbon/energy sector (the
degeneracy signature).  Selection criteria (same as the fourth- and
fifth-axis screens): >= 3 levels spanning ~50-90% WT reduction before
infeasibility, degeneracy present (PGI width > 1), in both models.

Artifacts: download/keio_nonmedium_prescreen.json
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

ATPM_GRID = [10.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 140.0,
             160.0, 180.0]
HLEAK_GRID = [5.0, 10.0, 20.0, 40.0, 60.0, 80.0, 100.0, 120.0]


def set_ijo(model):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0


def set_iml(model):
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


def find_biomass(model):
    for r in model.reactions:
        if r.objective_coefficient != 0 and (
                "iomass" in r.id or "BIOMASS" in r.id):
            return r.id
    assert False, "biomass reaction not found"


def probe_axis(model, kind, grid, setter, label, atpm_default):
    """kind: 'atpm' or 'hleak'.  atpm_default: the pristine ATPM lower
    bound captured at model load -- reset BEFORE the baseline so a
    previous probe's grid cannot contaminate this one."""
    out = {"kind": kind, "levels": {}}
    setter(model)
    model.reactions.get_by_id("ATPM").lower_bound = atpm_default
    model.reactions.get_by_id("EX_h_e").lower_bound = 0
    atpm = model.reactions.get_by_id("ATPM")
    out["atpm_default_lb"] = float(atpm.lower_bound)
    base = model.optimize()
    if base.status != "optimal" or base.objective_value < 1e-9:
        out["error"] = "baseline infeasible"
        print(f"\n{label} {kind}: baseline infeasible -- skipped")
        return out
    out["baseline_biomass"] = round(float(base.objective_value), 6)
    print(f"\n{label} {kind}: baseline WT {base.objective_value:.6f}, "
          f"ATPM lb {atpm.lower_bound}", flush=True)
    for x in grid:
        setter(model)
        if kind == "atpm":
            model.reactions.get_by_id("ATPM").lower_bound = x
        else:
            model.reactions.get_by_id("EX_h_e").lower_bound = x
        sol = model.optimize()
        key = f"{x:g}"
        if sol.status != "optimal" or sol.objective_value < 1e-9:
            out["levels"][key] = {"biomass": 0.0}
            print(f"  {kind} {key}: WT 0.000000 (infeasible/zero)")
            continue
        par = pfba(model)
        fr = fva(model, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
        widths = {rid: round(float(fr.loc[rid, "maximum"]
                                  - fr.loc[rid, "minimum"]), 3)
                  for rid in FVA_TARGETS}
        wide = {r: w for r, w in widths.items() if w > 1e-6 and r != "ACKr"}
        out["levels"][key] = {
            "biomass": round(float(sol.objective_value), 6),
            "reduction_pct": round(100 * (1 - sol.objective_value
                                          / out["baseline_biomass"]), 1),
            "pfba_glc_uptake": round(float(-par.fluxes.EX_glc__D_e), 3),
            "raw_glc_uptake": round(float(-sol.fluxes.EX_glc__D_e), 3),
            "fva_widths_excl_ACKr": wide,
            "fva_PGI_width": widths.get("PGI"),
        }
        print(f"  {kind} {key}: WT {sol.objective_value:.6f} "
              f"(-{out['levels'][key]['reduction_pct']}%), "
              f"PGI width {widths.get('PGI')}", flush=True)
    return out


result = {}
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
for mdl, model, setter, label in [
        ("iJO1366", ijo, set_ijo, "iJO1366"),
        ("iML1515", iml, set_iml, "iML1515")]:
    atpm_default = float(model.reactions.get_by_id("ATPM").lower_bound)
    result[f"{mdl}_atpm"] = probe_axis(model, "atpm", ATPM_GRID,
                                       setter, label, atpm_default)
    result[f"{mdl}_hleak"] = probe_axis(model, "hleak", HLEAK_GRID,
                                        setter, label, atpm_default)

with open(os.path.join(OUT_DIR, "keio_nonmedium_prescreen.json"), "w") as f:
    json.dump(result, f, indent=2)

print("\n=== SELECTION SUMMARY (usable levels = 10-95% WT reduction) ===")
for kind in ("atpm", "hleak"):
    for mdl in ("iJO1366", "iML1515"):
        d = result[f"{mdl}_{kind}"]
        if "error" in d:
            print(f"{kind:6s} {mdl}: {d['error']}")
            continue
        usable = [k for k, v in d["levels"].items()
                  if 10 <= v.get("reduction_pct", 0) <= 95]
        pgi = max([v.get("fva_PGI_width", 0)
                   for v in d["levels"].values()] or [0])
        deepest = max([v.get("reduction_pct", 0)
                       for v in d["levels"].values()] or [0])
        print(f"{kind:6s} {mdl}: {len(usable)} usable, deepest "
              f"{deepest:.0f}%, max PGI width {pgi}")
print("\nprescreen written.")
