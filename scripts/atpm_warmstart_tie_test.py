#!/usr/bin/env python3
"""Reproduce the iML1515 ATPM=100 canonical kV floor (kV ~ 200.01 for
~700 compensable genes) as a solver-path (warm-start) vertex tie.

Fresh-model recomputation gives kV ~ 0 for the same KOs, so the probe's
recorded floor arises because its WT pFBA reference was solved AFTER
degeneracy_signature (model.optimize + pfba + FVA with
fraction_of_optimum=1) -- i.e., with a different simplex path -- while
the per-KO pFBA solves, each entered through a `with model:` bound
update, land on the other tied vertex.

This script reproduces the sequence:
  A  pfba on the fresh model                        -> wt_A
  B  optimize/pfba/FVA (degeneracy_signature) THEN pfba -> wt_B
  C  one `with model:` no-op context THEN pfba       -> wt_C
and reports pairwise squared distances between the vertices.  If
||wt_A - wt_B||^2 ~ 200 the probe floor is fully explained.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]


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


def sqdist(f1, f2):
    d = (f1 - f2).abs()
    d = d[d > 1e-9]
    if len(d) == 0:
        return 0.0, 0
    return float((d ** 2).sum()), len(d)


iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
BIO = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO = r.id
        break
set_iml_atpm(iml, 100.0)

wtA = pfba(iml)
lA = float(wtA.fluxes.abs().sum())
print(f"A fresh pfba:        L1={lA:.6f}  b={float(wtA.fluxes[BIO]):.6f}",
      flush=True)

# B: degeneracy_signature sequence then pfba  (the probe's WT path)
raw = iml.optimize()
par = pfba(iml)
fr = fva(iml, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
wtB = pfba(iml)
lB = float(wtB.fluxes.abs().sum())
k, n = sqdist(wtA.fluxes, wtB.fluxes)
print(f"B post-sig pfba:     L1={lB:.6f}  b={float(wtB.fluxes[BIO]):.6f}  "
      f"||A-B||^2={k:.4f} (n={n})", flush=True)

# C: with-model no-op then pfba (the KO-solve entry path)
with iml:
    pass
wtC = pfba(iml)
lC = float(wtC.fluxes.abs().sum())
kAC, nAC = sqdist(wtA.fluxes, wtC.fluxes)
kBC, nBC = sqdist(wtB.fluxes, wtC.fluxes)
print(f"C post-context pfba: L1={lC:.6f}  b={float(wtC.fluxes[BIO]):.6f}  "
      f"||A-C||^2={kAC:.4f} (n={nAC})  ||B-C||^2={kBC:.4f} (n={nBC})",
      flush=True)

# D: a KO entered through with model, then WT re-solve after restore
gid = "b0870"
with iml:
    for r in iml.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    koD = pfba(iml)
lD = float(koD.fluxes.abs().sum())
kDA, nDA = sqdist(wtA.fluxes, koD.fluxes)
kDB, nDB = sqdist(wtB.fluxes, koD.fluxes)
print(f"D KO {gid}:            L1={lD:.6f}  b={float(koD.fluxes[BIO]):.6f}  "
      f"||A-D||^2={kDA:.4f} (n={nDA})  ||B-D||^2={kDB:.4f} (n={nDB})",
      flush=True)

# E: WT solve AFTER the KO context restored (accumulated warm state)
wtE = pfba(iml)
lE = float(wtE.fluxes.abs().sum())
kEA, nEA = sqdist(wtA.fluxes, wtE.fluxes)
kED, nED = sqdist(wtE.fluxes, koD.fluxes)
print(f"E post-KO pfba:      L1={lE:.6f}  b={float(wtE.fluxes[BIO]):.6f}  "
      f"||A-E||^2={kEA:.4f} (n={nEA})  ||E-D||^2={kED:.4f} (n={nED})",
      flush=True)
print("\nVERDICT: L1 ties =", abs(lA - lD) < 1e-4,
      "; probe floor explained by B-vs-D distance ~200:",
      abs(kDB - 200.0) < 5.0, flush=True)
