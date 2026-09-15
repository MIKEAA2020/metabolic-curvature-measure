#!/usr/bin/env python3
"""Certify the one unrecorded supply-axis PGI width: iML1515 at the
nitrogen-limited level nh4 -2.5.

The manuscript's supply-axis PGI range ("45-201") cites every
nitrogen-, phosphate-, and iron-limited level.  All other widths are
deposited (iJO nitrogen 45.2/133.2/177.2/82.9; iJO phosphate
122.7/171.9/201.5; iML phosphate 151.7/188.9; iJO iron 102.8/162.0/
191.6; iML iron 139.2/176.5; oxygen 4.3/0.0); the iML1515 nh4_-2.5
cell was never recorded.  This script fills it using the nitrogen
probe's own medium setter and FVA convention (same FVA_TARGETS,
fraction_of_optimum=1.0).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
from cobra.io import load_json_model
from cobra.flux_analysis import flux_variability_analysis as fva

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from nitrogen_source_keio_probe import set_iml_medium, IML_LEVELS

FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]

lv = [d for d in IML_LEVELS if d["key"] == "nh4_-2.5"][0]
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
set_iml_medium(iml, lv)
bio = [r.id for r in iml.reactions
       if r.objective_coefficient != 0 and "iomass" in r.id][0]
opt = float(iml.slim_optimize())
fr = fva(iml, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
widths = {rid: round(float(fr.loc[rid, "maximum"] - fr.loc[rid, "minimum"]), 4)
          for rid in FVA_TARGETS}
out = {"model": "iML1515", "level": "nh4_-2.5 (EX_nh4_e lb -2.5)",
       "wild_type_biomass": opt, "fva_widths": widths,
       "PGI_width": widths["PGI"],
       "note": ("the one previously unrecorded supply-axis PGI width; "
                "certifies the manuscript range 45-201 (max deposited "
                "201.492, iJO1366 phosphate -0.1)")}
with open(os.path.join(REPO, "download", "keio_iml_nh4_pgi_width.json"),
          "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
print("DONE")
