#!/usr/bin/env python3
"""
DIAGNOSTIC: why does iJO1366 give zero wild-type biomass at EX_o2_e = 0
under the glucose-only medium lineage used by the Keio arms?

Hypothesis: the biomass reaction requires ubiquinone-8 (q8), whose
biosynthesis contains O2-dependent (monooxygenase) steps, so with the
oxygen exchange closed the biomass objective itself becomes
infeasible (a model-level degeneracy of the label construction, not a
biological claim).  This script:

  1. Confirms b_wt = 0 at O2 = 0 with the probe's exact medium.
  2. Checks whether q8 (and heme) appear in the biomass reaction.
  3. Lists O2-consuming reactions in the q8 biosynthesis pathway
     (ubi monooxygenases) and whether any q8 source exists without O2.
  4. Relief tests (each with the same medium, single change):
     (a) tiny O2 (-0.25, -0.1) -- does growth restart?
     (b) a q8 sink/source demand opened (DM_q8_c free) -- does growth
         restart at O2 = 0?
  5. Same WT check for iML1515 at O2 = 0 (does the second model share
     the degeneracy?).

Output: download/keio_o2_anaerobic_diagnostic.json (+ stdout log).
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "download", "keio_o2_anaerobic_diagnostic.json")

from cobra.io import load_json_model
from cobra import Reaction

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']

res = {}

# ---------- 1-3: iJO1366 at O2 = 0 ----------
m = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
for r in m.exchanges:
    r.lower_bound = 0
m.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
m.reactions.get_by_id("EX_o2_e").lower_bound = 0.0
for ex in IJO_MINERALS:
    m.reactions.get_by_id(ex).lower_bound = -1000.0
sol = m.optimize()
res["ijo_o2_0_biomass"] = float(sol.objective_value)
res["ijo_o2_0_status"] = sol.status
print(f"iJO1366 O2=0: b_wt = {sol.objective_value:.8g} ({sol.status})")

bio = [r for r in m.reactions if "BIOMASS" in r.id.upper()]
res["ijo_biomass_reactions"] = [r.id for r in bio]
q8_in_biomass = []
for br in bio:
    for met, coef in br.metabolites.items():
        if met.id.split("_")[-1] == "c" and "q8" in met.id:
            q8_in_biomass.append((br.id, met.id, float(coef)))
res["ijo_q8_in_biomass"] = q8_in_biomass
print("q8 in biomass:", q8_in_biomass)

o2_rxns = [r for r in m.reactions if "o2_c" in r.metabolites]
q8_o2 = []
for r in o2_rxns:
    names = [met.id for met in r.metabolites]
    if any("q8" in n or "2octaprenyl" in n or "3octaprenyl" in n or
           "opbenzo" in n or "ubiquin" in n for n in names):
        q8_o2.append({"id": r.id, "name": r.name,
                      "formula": r.reaction,
                      "gene_rule": r.gene_reaction_rule})
res["ijo_q8_pathway_o2_dependent_reactions"] = q8_o2
print(f"O2-dependent q8-pathway reactions: {[x['id'] for x in q8_o2]}")
res["ijo_all_o2_consuming_reaction_ids"] = [r.id for r in o2_rxns]

# q8-producing reactions (is there an O2-free source?)
q8_prod = []
for r in m.reactions:
    mets = r.metabolites
    if any("q8_c" in met.id for met in mets) and "o2_c" not in mets:
        q8_prod.append({"id": r.id, "reaction": r.reaction,
                        "lb": r.lower_bound, "ub": r.upper_bound})
res["ijo_q8_reactions_without_o2"] = q8_prod
print(f"q8-touching reactions without o2: {[(x['id'], x['lb'], x['ub']) for x in q8_prod]}")

# ---------- 4a: tiny O2 ----------
tiny = {}
for lb in [-0.25, -0.1, -0.01]:
    with m:
        m.reactions.EX_o2_e.lower_bound = lb
        s = m.optimize()
        tiny[str(lb)] = float(s.objective_value) if s.status == "optimal" else None
res["ijo_tiny_o2_relief"] = tiny
print("tiny-O2 relief:", tiny)

# ---------- 4b: q8 demand relief at O2 = 0 ----------
with m:
    m.reactions.EX_o2_e.lower_bound = 0.0
    dm = None
    if "DM_q8_c" in [r.id for r in m.reactions]:
        dm = m.reactions.get_by_id("DM_q8_c")
    else:
        dm = Reaction("DM_q8_c", name="q8 demand (diagnostic)",
                      lower_bound=0, upper_bound=1000)
        m.add_reactions([dm])
        dm.add_metabolites({m.metabolites.get_by_id("q8_c"): -1})
        dm.lower_bound = -1000  # free source allowed
    s = m.optimize()
    res["ijo_o2_0_q8_free_biomass"] = (
        float(s.objective_value) if s.status == "optimal" else None)
    res["ijo_o2_0_q8_free_status"] = s.status
    print(f"O2=0 with free q8 source: b_wt = "
          f"{res['ijo_o2_0_q8_free_biomass']} ({s.status})")

# ---------- 5: iML1515 at O2 = 0 ----------
m2 = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
for r in m2.reactions:
    if r.id.startswith("EX_"):
        r.lower_bound = 0
m2.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
for o2_id in ['EX_o2_e', 'EX_o2s_e']:
    try:
        m2.reactions.get_by_id(o2_id).lower_bound = 0.0
        break
    except Exception:
        continue
for ex in IML_MINERALS:
    try:
        m2.reactions.get_by_id(ex).lower_bound = -10
    except Exception:
        pass
s2 = m2.optimize()
res["iml_o2_0_biomass"] = (float(s2.objective_value)
                           if s2.status == "optimal" else None)
res["iml_o2_0_status"] = s2.status
print(f"iML1515 O2=0: b_wt = {res['iml_o2_0_biomass']} ({s2.status})")
bio2 = [r.id for r in m2.reactions if "BIOMASS" in r.id.upper()]
q8b2 = []
for br in bio2:
    rx = m2.reactions.get_by_id(br)
    for met, coef in rx.metabolites.items():
        if "q8" in met.id:
            q8b2.append((br, met.id, float(coef)))
res["iml_q8_in_biomass"] = q8b2
print("iML1515 q8 in biomass:", q8b2)

with open(OUT, "w") as f:
    json.dump(res, f, indent=2)
print(f"\nWrote {OUT}")
