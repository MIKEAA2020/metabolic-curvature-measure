#!/usr/bin/env python3
"""Quick WT feasibility scan for the nitrogen-source probe design.

Levels probed (iJO1366 + iML1515, glucose-only medium, tre closed):
  A. NH4 graded limitation: EX_nh4_e in {-10, -5, -2.5} (iJO baseline -1000)
  B. Glu swap:  EX_nh4_e = 0, EX_glu_L_e = -10   (glutamate sole N source)
  C. Glu limited: EX_nh4_e = 0, EX_glu_L_e = -2.5
  D. Arg swap:  EX_nh4_e = 0, EX_arg_L_e = -10   (arginine sole N source)
Records WT biomass + N-source uptake + nh4 release routes in use.
"""
import os, sys, warnings
warnings.filterwarnings("ignore")
import json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model

IJO_MINERALS = ["EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def set_med_ijo(m, nh4_lb, extra):
    for r in m.exchanges:
        r.lower_bound = 0
    m.reactions.EX_glc__D_e.lower_bound = -10.0
    m.reactions.EX_o2_e.lower_bound = -20.0
    for ex in IJO_MINERALS:
        m.reactions.get_by_id(ex).lower_bound = -1000.0
    m.reactions.EX_nh4_e.lower_bound = nh4_lb
    for ex_id, lb in extra.items():
        m.reactions.get_by_id(ex_id).lower_bound = lb


def set_med_iml(m, nh4_lb, extra):
    for r in m.reactions:
        if r.id.startswith("EX_"):
            r.lower_bound = 0
    m.reactions.EX_glc__D_e.lower_bound = -10.0
    for o2_id in ['EX_o2_e', 'EX_o2s_e']:
        try:
            m.reactions.get_by_id(o2_id).lower_bound = -20.0
            break
        except Exception:
            continue
    for ex in IML_MINERALS:
        try:
            m.reactions.get_by_id(ex).lower_bound = -10
        except Exception:
            pass
    m.reactions.EX_nh4_e.lower_bound = nh4_lb
    for ex_id, lb in extra.items():
        try:
            m.reactions.get_by_id(ex_id).lower_bound = lb
        except Exception:
            print(f"  !! iML1515 lacks {ex_id}")


LEVELS = [
    ("nh4=-10 (limitation)", -10.0, {}),
    ("nh4=-5  (limitation)", -5.0, {}),
    ("nh4=-2.5 (limitation)", -2.5, {}),
    ("glu -10 swap", 0.0, {"EX_glu__L_e": -10.0}),
    ("glu -2.5 (N-limited)", 0.0, {"EX_glu__L_e": -2.5}),
    ("arg -10 swap", 0.0, {"EX_arg__L_e": -10.0}),
]

for name, jsonf in [("iJO1366", "iJO1366.json"), ("iML1515", "iML1515.json")]:
    m = load_json_model(os.path.join(REPO, "data/bigg_models", jsonf))
    print(f"\n===== {name} =====")
    # baseline for reference
    if name == "iJO1366":
        set_med_ijo(m, -1000.0, {})
    else:
        set_med_iml(m, -10.0, {})
    wt = m.optimize()
    nh4_up = -wt.fluxes.get("EX_nh4_e", 0.0)
    print(f"baseline: WT {wt.objective_value:.4f}, nh4 uptake {nh4_up:.3f}")
    for label, nh4_lb, extra in LEVELS:
        if name == "iJO1366":
            set_med_ijo(m, nh4_lb, extra)
        else:
            set_med_iml(m, nh4_lb, extra)
        sol = m.optimize()
        if sol.status != "optimal" or sol.objective_value < 1e-9:
            print(f"  {label:24s}: INFEASIBLE / zero growth "
                  f"({sol.objective_value if sol.status == 'optimal' else sol.status})")
            continue
        ups = {}
        for ex in ["EX_nh4_e", "EX_glu__L_e", "EX_arg__L_e"]:
            v = sol.fluxes.get(ex, 0.0)
            if v < -1e-6:
                ups[ex] = round(-v, 3)
        # glutamate dehydrogenase + other nh4-release routes
        gdh = sol.fluxes.get("GLUDx", 0.0) + sol.fluxes.get("GLUDy", 0.0)
        aspA = sol.fluxes.get("ASPtpp", 0.0)
        print(f"  {label:24s}: WT {sol.objective_value:.4f}; uptakes {ups}; "
              f"GLUDx/y {gdh:.3f}")
