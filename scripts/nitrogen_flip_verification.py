#!/usr/bin/env python3
"""Mechanistic verification of the nitrogen-axis label losses.

All flips are LOSSES (essential on glucose-minimal ammonium medium,
non-essential under the substitution).  This script (i) maps the
flipped b-numbers to gene names/reactions, (ii) verifies for each
loss that the rescue is substitution-mediated (closing the sole N
source in the KO background restores lethality), and (iii) records
the alpha-ketoglutarate assimilation flux that the substitution
makes dispensable (the GLUDy/GLUSy reductive assimilation arm at
the baseline optimum vs the substitution optima).

Outputs: download/keio_nitrogen_flip_verification.json
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from nitrogen_source_keio_probe import (
    set_ijo_medium, set_iml_medium, IJO_LEVELS, IML_LEVELS)

res = {"iJO1366": {}, "iML1515": {}}

# ---------------------------------------------------------------------
# iJO1366
# ---------------------------------------------------------------------
ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
ijo_res = json.load(open(os.path.join(
    OUT_DIR, "keio_nitrogen_source_e12_results.json")))
base_sw = pd.read_csv(os.path.join(OUT_DIR, "keio_glucose_only_e12.csv"))
n_sw = pd.read_csv(os.path.join(OUT_DIR, "keio_nitrogen_source_e12_sweep.csv"))

for key in ["glu_-10", "arg_-10"]:
    fl = ijo_res["levels"][key]["flips_vs_glucose_only"]
    losses = [g["gene_id"] for g in fl["losses"]]
    lv = next(l for l in IJO_LEVELS if l["key"] == key)
    rows = []
    for gid in losses:
        g = ijo.genes.get_by_id(gid)
        rxns = [(r.id, r.name) for r in g.reactions]
        b0 = float(base_sw[base_sw.gene_id == gid].b_ko.iloc[0])
        lv_sw = n_sw[n_sw.level == key]
        b1 = float(lv_sw[lv_sw.gene_id == gid].b_ko.iloc[0])
        # rescue test: KO in the substitution medium, then close the
        # sole N source (reopen ammonium at its baseline bound)
        set_ijo_medium(ijo, lv)
        with ijo:
            for r in g.reactions:
                r.lower_bound = 0
                r.upper_bound = 0
            ijo.reactions.get_by_id(lv["n_source"]).lower_bound = 0
            ijo.reactions.EX_nh4_e.lower_bound = -1000.0
            b_closed = float(ijo.slim_optimize())
        rows.append({
            "gene": gid, "name": g.name, "reactions": rxns,
            "b_ko_baseline": round(b0, 6), "b_ko_substitution": round(b1, 6),
            "b_ko_substitution_N_closed": round(b_closed, 6),
            "rescue_is_substitution_mediated": bool(
                b_closed < 0.05 * b1 if b1 > 0 else False),
        })
        print(f"iJO {key} {gid} ({g.name}): {b0:.4f} -> {b1:.4f}; "
              f"N-source closed: {b_closed:.6f}", flush=True)
    res["iJO1366"][key] = rows

# akg assimilation arm at the three optima
arm = {}
for key, med in [("baseline", {"nh4_lb": -1000.0, "n_source": None}),
                 ("glu_-10", IJO_LEVELS[3]), ("arg_-10", IJO_LEVELS[4])]:
    set_ijo_medium(ijo, med)
    sol = ijo.optimize()
    arm[key] = {
        "biomass": round(float(sol.objective_value), 6),
        "GLUDy_reductive_assimilation": round(
            float(-sol.fluxes.get("GLUDy", 0.0)), 4),
        "GLUDx_reductive_assimilation": round(
            float(-sol.fluxes.get("GLUDx", 0.0)), 4),
        "GLUSy_GOGAT": round(float(sol.fluxes.get("GLUSy", 0.0)), 4),
        "GLNS": round(float(sol.fluxes.get("GLNS", 0.0)), 4),
        "akg_sinks_biomass_via_AKGPD/other": round(float(
            sol.fluxes.get("AKGDH", 0.0)), 4),
    }
    print(f"iJO akg arm @{key}: {arm[key]}", flush=True)
res["iJO1366"]["akg_assimilation_arm"] = arm

# ---------------------------------------------------------------------
# iML1515
# ---------------------------------------------------------------------
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
iml_res = json.load(open(os.path.join(
    OUT_DIR, "keio_nitrogen_source_e16_results.json")))
iml_sw = pd.read_csv(os.path.join(OUT_DIR,
                                  "keio_nitrogen_source_e16_sweep.csv"))
iml_base = pd.read_csv(os.path.join(OUT_DIR,
                                    "keio_glucose_only_e16_sweep.csv"))

for key in ["glu_-10", "arg_-10"]:
    fl = iml_res["levels"][key]["flips_vs_glucose_only"]
    losses = [g["gene_id"] for g in fl["losses"]]
    lv = next(l for l in IML_LEVELS if l["key"] == key)
    rows = []
    for gid in losses:
        g = iml.genes.get_by_id(gid)
        rxns = [(r.id, r.name) for r in g.reactions]
        b0 = float(iml_base[iml_base.gene_id == gid].b_ko.iloc[0])
        lv_sw = iml_sw[iml_sw.level == key]
        b1 = float(lv_sw[lv_sw.gene_id == gid].b_ko.iloc[0])
        set_iml_medium(iml, lv)
        with iml:
            for r in iml.reactions:
                if gid in r.gene_reaction_rule:
                    r.lower_bound = 0
                    r.upper_bound = 0
            iml.reactions.get_by_id(lv["n_source"]).lower_bound = 0
            iml.reactions.EX_nh4_e.lower_bound = -10.0
            b_closed = float(iml.slim_optimize())
        rows.append({
            "gene": gid, "name": g.name, "reactions": rxns,
            "b_ko_baseline": round(b0, 6), "b_ko_substitution": round(b1, 6),
            "b_ko_substitution_N_closed": round(b_closed, 6),
            "rescue_is_substitution_mediated": bool(
                b_closed < 0.05 * b1 if b1 > 0 else False),
        })
        print(f"iML {key} {gid} ({g.name}): {b0:.4f} -> {b1:.4f}; "
              f"N-source closed: {b_closed:.6f}", flush=True)
    res["iML1515"][key] = rows

with open(os.path.join(OUT_DIR, "keio_nitrogen_flip_verification.json"),
          "w") as f:
    json.dump(res, f, indent=2)
print("\nFLIP VERIFICATION WRITTEN.")
