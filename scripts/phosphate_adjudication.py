#!/usr/bin/env python3
"""Adjudicate the three discrepant genes at iJO1366 Pi = -0.1 and
identify the bioF-bypass mechanism.

Plain sweep says: b0180 viable, b3412 viable, b0776 essential (287).
Canonical sweep says: b0180 essential, b3412 essential, b0776 viable
(288).  Fresh single-shot solves + FVA decide; then the biotin-
pathway fluxes of the canonical WT at Pi = -0.1 are inspected to
identify how the bioF knockout is buffered.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva

IJO_MINERALS = ["EX_nh4_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
PI = -0.1
GENES = ["b0180", "b0776", "b3412"]


def fresh_model(pi_lb=PI):
    m = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
    for r in m.exchanges:
        r.lower_bound = 0
    m.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    m.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        m.reactions.get_by_id(ex_id).lower_bound = -1000.0
    m.reactions.get_by_id("EX_pi_e").lower_bound = pi_lb
    return m


# ---- WT reference (fresh) ----
m0 = fresh_model()
wt = m0.optimize()
b_wt = float(wt.objective_value)
print(f"fresh WT at Pi={PI}: {b_wt:.10f}")
BIO = [r.id for r in m0.reactions
       if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
print("objective biomass:", BIO)
bio_rxn = m0.reactions.get_by_id(BIO)
btn_met = [k.id for k in bio_rxn.metabolites
           if "btn" in k.id.lower() or "biotin" in k.name.lower()]
print("biotin metabolite in objective biomass:", btn_met,
      {mm: bio_rxn.get_coefficient(mm) for mm in btn_met})

# ---- fresh KO solves (KO is the first solve of a fresh instance) ----
print("\n--- fresh single-shot KO adjudication ---")
verdicts = {}
for gid in GENES:
    mk = fresh_model()
    for r in mk.reactions:
        if gid in r.gene_reaction_rule:
            r.lower_bound = 0
            r.upper_bound = 0
    sol = mk.optimize()
    b_ko = float(sol.objective_value) if sol.status == "optimal" else 0.0
    # FVA cross-check on the biomass reaction (independent objectives)
    fr = fva(mk, reaction_list=[BIO], fraction_of_optimum=0.0)
    bmax = float(fr.loc[BIO, "maximum"])
    verdicts[gid] = {"plain_solve": b_ko, "fva_biomass_max": bmax,
                     "essential": bmax < 0.05 * b_wt}
    print(f"{gid}: fresh KO solve {b_ko:.10f}; FVA biomass max "
          f"{bmax:.10f}; essential = {bmax < 0.05 * b_wt}")

# ---- the bioF bypass mechanism at the canonical WT ----
print("\n--- biotin-pathway fluxes of the canonical (pFBA) WT ---")
mw = fresh_model()
par = pfba(mw)
BIO_ID = BIO
# find the biotin pathway reactions and 8aon consumers
targets = ["AOXSr2", "PMEACPE", "OGMEACPD", "OPMEACPD"]
for rid in targets:
    print(f"  {rid:10s} = {float(par.fluxes.get(rid, 0.0)):+.6f}")
m = mw.metabolites
for met_id in ["8aon_c", "pimelate_c", "btn_c", "6h8apan_c",
               "dpan_c", "alacns_c"]:
    try:
        met = m.get_by_id(met_id)
    except KeyError:
        continue
    prod = {r.id: round(float(par.fluxes.get(r.id, 0.0)
                             * r.get_coefficient(met_id)), 6)
            for r in met.reactions
            if abs(float(par.fluxes.get(r.id, 0.0)
                         * r.get_coefficient(met_id))) > 1e-9}
    print(f"  {met_id:12s} producing reactions: {prod}")

# ---- and the same at the baseline (Pi unlimited) for contrast ----
print("\n--- same fluxes at the Pi-unlimited baseline ---")
mb = fresh_model(-1000.0)
parb = pfba(mb)
for rid in targets:
    print(f"  {rid:10s} = {float(parb.fluxes.get(rid, 0.0)):+.6f}")

out = {"pi_level": PI, "wild_type_biomass": b_wt, "genes": verdicts,
       "objective_biomass": BIO,
       "biotin_in_objective_biomass": btn_met}
with open(os.path.join(REPO, "download",
                       "keio_phosphate_adjudication.json"), "w") as f:
    json.dump(out, f, indent=2)
print("\nadjudication written.")
