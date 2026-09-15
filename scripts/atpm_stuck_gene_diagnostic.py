#!/usr/bin/env python3
"""Diagnostic v2: identify pathological pFBA KO solves in the iJO1366
atpm_100 canonical sweep, using GLPK's native simplex time limit
(optlang glpk configuration.timeout -> smcp.tm_lim).

Findings from v1: genes 1-9 after the 400-gene partial solve in
0.1-0.4 s each; gene 10 hangs indefinitely (simplex cycling in the
pFBA L1-minimization stage; the plain FBA sweep completed all genes,
so stage-1 LPs are fine).

This scan (a) confirms the time limit interrupts the cycle, (b) counts
how many of the next 40 genes are pathological, and (c) verifies the
plain-FBA fallback vertex is available for each timed-out gene.
"""
import os, sys, time, warnings
warnings.filterwarnings("ignore")
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from cobra.io import load_json_model
from cobra.flux_analysis import pfba

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]


def set_ijo_atpm(model, atpm_lb):
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("ATPM").lower_bound = atpm_lb


ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO = [r.id for r in ijo.reactions
       if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
set_ijo_atpm(ijo, 100.0)
ijo.solver.configuration.timeout = 15  # GLPK tm_lim, seconds

par_wt = pfba(ijo)
print(f"WT pFBA ok, biomass {float(par_wt.fluxes[BIO]):.6f}", flush=True)

part = pd.read_csv(os.path.join(
    REPO, "download", "keio_atpm_pfba_control_atpm_100_partial.csv"))
done = set(part["gene_id"].tolist())
print(f"done genes: {len(done)}", flush=True)

n = n_ok = n_to = n_infeas = 0
timeouts = []
for gene in ijo.genes:
    if gene.id in done:
        continue
    gpr_rxns = [r for r in gene.reactions if gene in r.genes]
    if not gpr_rxns:
        continue
    n += 1
    t1 = time.time()
    status = "?"
    with ijo:
        for r in gpr_rxns:
            r.lower_bound = 0
            r.upper_bound = 0
        try:
            sol = pfba(ijo)
            b_ko = float(sol.fluxes[BIO])
            status = "ok"
            n_ok += 1
        except Exception:
            # plain fallback to distinguish timeout vs infeasible
            try:
                psol = ijo.optimize()
                b_ko = float(psol.objective_value)
                status = "TIMEOUT->plain-ok"
                n_to += 1
                timeouts.append(gene.id)
            except Exception:
                b_ko = float("nan")
                status = "infeasible"
                n_infeas += 1
    dt = time.time() - t1
    print(f"gene {n:2d} {gene.id:8s} {status:16s} b_ko={b_ko:.6f} "
          f"{dt:6.1f}s", flush=True)
    if n >= 40:
        break
print(f"\nSCAN DONE: ok={n_ok} timeout={n_to} infeasible={n_infeas}; "
      f"timeout genes: {timeouts}", flush=True)
