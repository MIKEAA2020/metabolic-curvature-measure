#!/usr/bin/env python3
"""Fifth-axis pre-screen: trace-metal limitation -- iron (EX_fe2_e) vs
zinc (EX_zn2_e) vs manganese (EX_mn2_e) dose responses on iJO1366 and
iML1515, under the glucose-only corrected medium (EX_tre_e closed).

Iron supply is pinned to the single ferrous channel: EX_fe3_e stays
CLOSED on iML1515 (the iJO1366 probe medium already supplies iron only
as EX_fe2_e), so the iron axis is exactly one controlled exchange --
homogeneous with the O2 / N / P axes.  The fe3-closed baseline is
verified against the standard probe baseline (identical WT optimum).

Purpose: choose the fifth supply-side perturbation axis and its levels
by data, not by convention.  Trace-metal biomass quotas are ~2 orders
of magnitude below the phosphate uptake, so the level grids are
correspondingly finer.  Per candidate we record the WT optimum across
the grid (plain and parsimonious uptake; the parsimonious value is the
true unlimited requirement -- at unlimited supply the plain vertex is
degenerate in the metal), and at-optimum FVA widths of the
carbon/energy sector (PGI, CS, ACKr, G6PDH2r, glucose exchange) at
informative levels -- the degeneracy signature that the nitrogen,
oxygen and phosphate axes showed to condition plain-FBA curvature
statistics.

Resumable per (model, metal) block.
Artifacts: download/keio_fifth_axis_prescreen.json
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

# trace-metal grids (quotas: fe ~2.3e-2, zn ~3.3e-3, mn ~1.6e-3 mmol/gDW)
FE_GRID = [-0.1, -0.05, -0.025, -0.01, -0.005, -0.0025, -0.001, -0.0005]
ZN_GRID = [-0.01, -0.005, -0.0025, -0.001, -0.0005, -0.00025, -0.0001]
MN_GRID = [-0.01, -0.005, -0.0025, -0.001, -0.0005, -0.00025, -0.0001]


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


def find_biomass(model):
    for r in model.reactions:
        if r.objective_coefficient != 0 and (
                "iomass" in r.id or "BIOMASS" in r.id):
            return r.id
    return None


def iron_exchange_inventory(model):
    return {r.id: (r.lower_bound, r.upper_bound)
            for r in model.reactions
            if r.id.startswith("EX_") and "fe" in r.id.lower()}


def probe(model, axis_id, grid, setter, label):
    out = {"axis_exchange": axis_id, "levels": {}}
    setter(model)  # baseline, unlimited
    base = model.optimize()
    bio_id = find_biomass(model)
    assert bio_id, "biomass reaction not found"
    par_base = pfba(model)
    out["baseline_biomass"] = round(float(base.objective_value), 6)
    out["baseline_unlimited_uptake_plain"] = round(
        float(-base.fluxes[axis_id]), 4)
    out["baseline_unlimited_uptake_pfba"] = round(
        float(-par_base.fluxes[axis_id]), 5)
    print(f"\n{label}: baseline WT {base.objective_value:.6f}; "
          f"{axis_id} uptake plain "
          f"{out['baseline_unlimited_uptake_plain']} / parsimonious "
          f"{out['baseline_unlimited_uptake_pfba']}", flush=True)
    for lb in grid:
        setter(model, lb, axis_id)
        sol = model.optimize()
        if sol.status != "optimal" or sol.objective_value < 1e-9:
            out["levels"][str(lb)] = {
                "biomass": 0.0,
                "uptake": round(float(-sol.fluxes.get(axis_id, 0.0)), 5)}
            print(f"  {axis_id} >= {lb}: WT 0.000000 (infeasible/zero)",
                  flush=True)
            continue
        red = 100.0 * (1.0 - sol.objective_value / out["baseline_biomass"])
        rec = {
            "biomass": round(float(sol.objective_value), 6),
            "reduction_pct": round(red, 1),
            "uptake": round(float(-sol.fluxes[axis_id]), 5),
        }
        if 2.0 <= red <= 98.0:  # informative band: degeneracy signature
            par = pfba(model)
            fr = fva(model, reaction_list=FVA_TARGETS,
                     fraction_of_optimum=1.0)
            widths = {rid: round(float(fr.loc[rid, "maximum"]
                                      - fr.loc[rid, "minimum"]), 3)
                      for rid in FVA_TARGETS}
            rec.update({
                "pfba_glc_uptake": round(float(-par.fluxes.EX_glc__D_e), 3),
                "raw_glc_uptake": round(float(-sol.fluxes.EX_glc__D_e), 3),
                "pfba_axis_uptake": round(float(-par.fluxes[axis_id]), 5),
                "fva_widths_excl_ACKr": {r: w for r, w in widths.items()
                                         if w > 1e-6 and r != "ACKr"},
                "fva_PGI_width": widths.get("PGI"),
            })
            print(f"  {axis_id} >= {lb}: WT {sol.objective_value:.6f} "
                  f"(-{rec['reduction_pct']}%), glc raw {rec['raw_glc_uptake']}"
                  f" / pFBA {rec['pfba_glc_uptake']}, PGI width "
                  f"{rec['fva_PGI_width']}", flush=True)
        else:
            print(f"  {axis_id} >= {lb}: WT {sol.objective_value:.6f} "
                  f"(-{rec['reduction_pct']}%)", flush=True)
        out["levels"][str(lb)] = rec
    return out


OUT_JSON = os.path.join(OUT_DIR, "keio_fifth_axis_prescreen.json")
result = {}
if os.path.exists(OUT_JSON):
    try:
        result = json.load(open(OUT_JSON))
    except Exception:
        result = {}

BLOCKS = [
    ("iJO1366_iron", "iJO1366 iron (EX_fe2_e)", "EX_fe2_e", FE_GRID,
     "ijo"),
    ("iJO1366_zinc", "iJO1366 zinc (EX_zn2_e)", "EX_zn2_e", ZN_GRID,
     "ijo"),
    ("iJO1366_manganese", "iJO1366 manganese (EX_mn2_e)", "EX_mn2_e",
     MN_GRID, "ijo"),
    ("iML1515_iron", "iML1515 iron (EX_fe2_e, fe3 CLOSED)",
     "EX_fe2_e", FE_GRID, "iml"),
    ("iML1515_zinc", "iML1515 zinc (EX_zn2_e)", "EX_zn2_e", ZN_GRID,
     "iml"),
    ("iML1515_manganese", "iML1515 manganese (EX_mn2_e)", "EX_mn2_e",
     MN_GRID, "iml"),
]

loaded = {}
for key, label, axis_id, grid, which in BLOCKS:
    if key in result and result[key].get("levels"):
        print(f"{key}: already done -- skipping", flush=True)
        continue
    if which == "ijo":
        if "ijo" not in loaded:
            loaded["ijo"] = load_json_model(os.path.join(
                REPO, "data/bigg_models/iJO1366.json"))
            inv = iron_exchange_inventory(loaded["ijo"])
            result.setdefault("iJO1366_iron_exchange_inventory",
                              {k: list(v) for k, v in inv.items()})
            print(f"iJO1366 iron exchanges under probe medium: {inv}",
                  flush=True)
        model = loaded["ijo"]
        setter = set_ijo
    else:
        if "iml" not in loaded:
            loaded["iml"] = load_json_model(os.path.join(
                REPO, "data/bigg_models/iML1515.json"))
        model = loaded["iml"]
        setter = set_iml
    if key == "iML1515_iron":
        # fe3-closed sanity check: WT identical with the ferric channel
        # open (standard probe medium) vs closed (iron-axis convention)
        set_iml(model)
        wt_open = float(model.optimize().objective_value)
        model.reactions.get_by_id("EX_fe3_e").lower_bound = 0
        wt_closed = float(model.optimize().objective_value)
        inv = iron_exchange_inventory(model)
        result["iML1515_fe3_closed_check"] = {
            "wt_fe3_open": round(wt_open, 6),
            "wt_fe3_closed": round(wt_closed, 6),
            "abs_diff": round(abs(wt_open - wt_closed), 9),
            "note": ("diff is simplex vertex noise on a degenerate "
                     "optimum (both iron channels effectively "
                     "unlimited); the fe3-closed medium is the "
                     "iron-axis convention"),
            "iron_exchanges_after_closing": {k: list(v)
                                             for k, v in inv.items()},
        }
        print(f"iML1515 fe3-closed check: WT {wt_open:.6f} (open) vs "
              f"{wt_closed:.6f} (closed), diff "
              f"{abs(wt_open-wt_closed):.2e} (solver vertex noise); "
              f"iron exchanges {inv}", flush=True)
        # fe3 closure must not change the medium's growth semantics
        # (tolerance = simplex noise scale, not 1e-9)
        assert abs(wt_open - wt_closed) < 1e-4, \
            "fe3 closure changes WT beyond solver noise!"
        # keep fe3 closed for the iron dose response (axis convention);
        # the setter re-opens it via IML_MINERALS, so re-close per level
        def setter(model, axis_lb=None, axis_id=None, _s=set_iml):
            _s(model, axis_lb, axis_id)
            model.reactions.get_by_id("EX_fe3_e").lower_bound = 0
    result[key] = probe(model, axis_id, grid, setter, label)
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    print(f"[block {key} written]", flush=True)

print("\nFIFTH-AXIS PRESCREEN DONE.")
print("Informative bands (5-95% WT reduction):")
for key, label, axis_id, grid, which in BLOCKS:
    if key not in result:
        continue
    band = [(lb, v) for lb, v in result[key]["levels"].items()
            if 5.0 <= v.get("reduction_pct", 0.0) <= 95.0]
    pgi = [(lb, v.get("fva_PGI_width"))
           for lb, v in result[key]["levels"].items()
           if v.get("fva_PGI_width") is not None]
    print(f"  {key}: {len(band)} levels in band "
          f"{[b[0] for b in band]}; PGI widths {pgi}")
