#!/usr/bin/env python3
"""Root-cause the iML1515 ATPM-stress canonical kV floor (kV ~ 200.01
for ~700 compensable genes, identical to 4 decimals, n_changed ~ 10).

Hypothesis: at elevated ATPM the iML1515 pFBA L1 stage is itself
degenerate -- there exist >= 2 distinct minimal-L1 flux vectors.  The
WT pFBA solve lands on vertex A; each compensable-KO solve (effectively
the same LP for zero-flux knockouts) lands on vertex B; the kV floor
is the squared distance between the tied vertices.

Decisive test: solve WT pFBA and a compensable-KO pFBA, compare the
L1 objectives and the actual flux differences.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model
from cobra.flux_analysis import pfba

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def set_iml_atpm(model, atpm_lb):
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
    model.reactions.get_by_id("ATPM").lower_bound = atpm_lb
    # EX_tre_e stays closed
    try:
        model.reactions.get_by_id("EX_tre_e").lower_bound = 0
    except Exception:
        pass


iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
BIO = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO = r.id
        break
set_iml_atpm(iml, 100.0)
iml.solver.configuration.timeout = 60

wt = pfba(iml)
l1_wt = float(wt.fluxes.abs().sum())
b_wt = float(wt.fluxes[BIO])
print(f"WT pFBA: biomass {b_wt:.6f}, L1 = {l1_wt:.6f}", flush=True)

for gid in ["b0870", "b2436", "b4467"]:
    with iml:
        for r in iml.reactions:
            if gid in r.gene_reaction_rule:
                r.lower_bound = 0
                r.upper_bound = 0
        ko = pfba(iml)
    l1_ko = float(ko.fluxes.abs().sum())
    b_ko = float(ko.fluxes[BIO])
    dv = (ko.fluxes - wt.fluxes).abs()
    dv = dv[dv > 1e-6].sort_values(ascending=False)
    kV = float((dv ** 2).sum())
    print(f"\nKO {gid}: biomass {b_ko:.6f} (delta {b_wt-b_ko:.2e}), "
          f"L1 = {l1_ko:.6f} (dL1 = {l1_ko-l1_wt:+.6f}), "
          f"kV = {kV:.4f}, n_changed = {len(dv)}", flush=True)
    print("  top |dv| reactions:")
    for rid, v in dv.head(12).items():
        print(f"    {rid:18s} {v:10.4f}   "
              f"(WT {wt.fluxes[rid]:+9.4f} -> KO {ko.fluxes[rid]:+9.4f})")
print("\nDONE")
