#!/usr/bin/env python3
"""FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (trace-metal supply --
the last classical nutrient class after C, electron acceptor, N, P).

Background.  Four axes are established (companion v3, props
keio-glucose-only / keio-o2-limited / keio-n-source / keio-phosphate):
carbon source, electron acceptor, nitrogen supply, phosphate supply.
Supply perturbations leave the essentiality labels invariant (zero
flips, kappa 1.000) down to deep wild-type reductions; re-stratification
appears only at regime switches (anaerobic) or source substitutions
(organic N donors), confined to the rewired module.  The remaining
classical supply class is the trace metals.  The pre-screen
(fifth_axis_prescreen.py) selected IRON over zinc and manganese by
data: the parsimonious requirement is 0.0158 (iJO1366) / 0.0132
(iML1515) mmol/gDW/h, giving a three-level gradient EX_fe2_e
{-0.01,-0.005,-0.0025} spanning 37% / 68% / 84% wild-type reduction
(iJO1366) and 62% / 81% (iML1515) -- the same depth range as the
other axes.  Zinc and manganese compress their informative bands to
the 1e-4 bound scale (2 levels / boundary level respectively) and were
rejected on that basis (see the prescreen artifact).  Two structural
facts from the pre-screen: (i) pinning iron to the single ferrous
channel (EX_fe3_e CLOSED on iML1515; the iJO1366 probe medium already
supplies iron only as EX_fe2_e) leaves the WT optimum unchanged to
solver noise (3.2e-6); (ii) the iron dose response is IDENTICAL on
both reconstructions to six decimals -- both biomass equations share
the same iron quota c_fe = 0.016067 mmol/gDW, so iron limitation is
an exactly linear biomass-quota scaling (b = fe2/c_fe), the purest
supply perturbation of the five axes.

Design (homogeneous with the canonical-selection protocol).
  iJO1366:  EX_fe2_e in {-0.01, -0.005, -0.0025}
  iML1515:  EX_fe2_e in {-0.005, -0.0025}   (EX_fe3_e closed)
  Per level, BOTH arms are computed:
    PLAIN  -- plain-FBA sweep (E12/E16 conventions, labels at 5% of
              that level's WT) -- the axis's own plain reading and
              the label-flip comparison vs the glucose-only baseline;
    CANON  -- parsimonious-FBA sweep for the WT and every knockout
              (canonical vertex selection; labels unchanged by
              construction, verified; biomass read from the solution
              vector, objective preserved to <1e-6) -- the reported
              statistic, homogeneous with the O2/N/P canonical
              controls.
  Plus the degeneracy signature per level (at-optimum FVA on the
  carbon/energy sector; raw vs parsimonious glucose uptake).
  The deepest level (WT 0.156) stays above the growth<0.14 tolerance
  zone characterized by the solver-integrity round; the trace-quota
  rows of the deepest levels are re-adjudicated afterwards
  (iron_integrity_scan.py) to confirm no false-viability calls.

All four sweep arms are per-400-gene checkpointed (partial CSVs), so a
chunk timeout resumes instead of restarting.

Conventions identical to nitrogen_source_keio_probe.py (seeds 42 /
20260830; the analysis blocks are imported from it).

Artifacts (download/):
  keio_iron_limited_e12_results.json / _sweep.csv      (plain iJO)
  keio_iron_limited_e16_results.json / _sweep.csv      (plain iML)
  keio_iron_pfba_control.json
  keio_iron_pfba_control_<key>.csv                     (canonical iJO)
  keio_iron_pfba_control_iml_<key>.csv                 (canonical iML)
  keio_iron_limited_summary.txt
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from cobra.flux_analysis import pfba, flux_variability_analysis as fva
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score

from nitrogen_source_keio_probe import (
    keio_tables, transitive_calibration, direct_arm,
    flip_analysis)

IJO_FE_LEVELS = [-0.01, -0.005, -0.0025]
IML_FE_LEVELS = [-0.005, -0.0025]
BYPRODUCTS = ["EX_etoh_e", "EX_lac__D_e", "EX_for_e", "EX_succ_e",
              "EX_ac_e"]
FVA_TARGETS = ["EX_glc__D_e", "EX_ac_e", "EX_for_e", "EX_etoh_e",
               "EX_o2_e", "PGI", "CS", "ACKr", "PPCK", "G6PDH2r"]
IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']


def key_of(lb):
    return f"fe_{abs(lb):g}"


def set_ijo_fe(model, fe_lb):
    """Glucose-only corrected medium, ferrous iron at the probe level.
    EX_fe3_e is never opened (single-channel iron, as in the pre-screen);
    EX_tre_e stays CLOSED (glucose-only correction retained)."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("EX_fe2_e").lower_bound = fe_lb


def set_iml_fe(model, fe_lb):
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
    model.reactions.get_by_id("EX_fe2_e").lower_bound = fe_lb
    # iron-axis convention: ferric channel closed (single-channel iron;
    # pre-screen verified WT unchanged to solver noise)
    model.reactions.get_by_id("EX_fe3_e").lower_bound = 0


def degeneracy_signature(model, bio_id):
    raw = model.optimize()
    par = pfba(model)
    fr = fva(model, reaction_list=FVA_TARGETS, fraction_of_optimum=1.0)
    widths = {}
    for rid in FVA_TARGETS:
        try:
            lo, hi = float(fr.loc[rid, "minimum"]), float(fr.loc[rid, "maximum"])
            widths[rid] = round(hi - lo, 3)
        except Exception:
            widths[rid] = None
    return {
        "fba_optimum": round(float(raw.objective_value), 6),
        "pfba_biomass_flux": round(float(par.fluxes[bio_id]), 6),
        "objective_abs_diff": round(abs(float(raw.objective_value)
                                        - float(par.fluxes[bio_id])), 9),
        "raw_glc_uptake": round(float(-raw.fluxes.EX_glc__D_e), 3),
        "pfba_glc_uptake": round(float(-par.fluxes.EX_glc__D_e), 3),
        "fe2_uptake": round(float(-raw.fluxes.EX_fe2_e), 5),
        "fva_widths": widths,
    }


def _resume(part_csv):
    rows, done = [], set()
    if part_csv and os.path.exists(part_csv):
        prev = pd.read_csv(part_csv)
        rows = prev.to_dict("records")
        done = set(prev["gene_id"])
        print(f"    resuming from {len(rows)} genes ({part_csv.rsplit('/', 1)[-1]})",
              flush=True)
    return rows, done


def build_stall_rows(model, key, which, bio_id, flux_wt, b_wt, arm):
    """Rows for genes whose GLPK LP hangs (simplex cycling on a
    degenerate vertex, e.g. b0887/cysU at iJO fe -0.0025): flux
    vectors precomputed with the repo's deterministic scipy/HiGHS
    engine (scripts/iron_stall_override.py) under the matching arm
    convention (plain = stage-1 vertex; canon = stage-1+2 min-L1
    vertex).  kV is computed here against THIS arm's own WT
    reference, so the row is homogeneous with the GLPK rows."""
    reg_path = os.path.join(OUT_DIR, "keio_iron_stall_overrides.json")
    if not os.path.exists(reg_path):
        return {}
    try:
        reg = json.load(open(reg_path))
    except Exception:
        return {}
    entries = reg.get(key, {}).get(which, [])
    if not entries:
        return {}
    items = flux_wt.items() if hasattr(flux_wt, "items") else flux_wt
    out = {}
    for entry in entries:
        try:
            fv = pd.read_csv(entry["csv"])
        except Exception:
            continue
        col = "v_plain" if arm == "plain" else "v_canon"
        if col not in fv.columns:
            continue
        v = dict(zip(fv["rxn"], fv[col].astype(float)))
        b_ko = float(v.get(bio_id, 0.0))
        if not np.isfinite(b_ko):
            continue
        kV, n_changed = 0.0, 0
        for r_id, w in items:
            dv = v.get(r_id, 0.0) - w
            if abs(dv) > 1e-6:
                kV += dv * dv
                n_changed += 1
        try:
            g = model.genes.get_by_id(entry["gene_id"])
            n_gpr = len([r for r in g.reactions if g in r.genes])
            gname = g.name
        except Exception:
            n_gpr, gname = 0, ""
        out[entry["gene_id"]] = {
            "gene_id": entry["gene_id"], "gene_name": gname,
            "n_gpr_rxns": n_gpr, "n_changed": n_changed,
            "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
            "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
            "engine": "highs-stall-override",
        }
        print(f"    stall override ({arm}, {which} {key}): "
              f"{entry['gene_id']} b_ko={b_ko:.6f}", flush=True)
    return out


def plain_sweep_ijo(model, b_wt, flux_wt, part_csv=None, stall_rows=None):
    """E12-convention plain sweep (ko_sweep_ijo body verbatim),
    checkpointed every 200 genes with progress prints -- the deepest
    iron level's LPs are markedly slower and must survive chunk
    timeouts."""
    rows, done_ids = _resume(part_csv)
    t0 = time.time()
    for gene in model.genes:
        if gene.id in done_ids:
            continue
        if stall_rows and gene.id in stall_rows:
            rows.append(stall_rows[gene.id])
            continue
        gpr_rxns = [r for r in gene.reactions if gene in r.genes]
        if not gpr_rxns:
            continue
        with model:
            for r in gpr_rxns:
                r.lower_bound = 0
                r.upper_bound = 0
            try:
                sol = model.optimize()
            except Exception:
                sol = None
            if sol is None or sol.status != "optimal":
                b_ko = 0.0
                flux_ko_dict = {}
            else:
                b_ko = float(sol.objective_value)
                flux_ko_dict = sol.fluxes.to_dict()
        kV = 0.0
        n_changed = 0
        for r_id, v_wt in flux_wt.items():
            dv = flux_ko_dict.get(r_id, 0.0) - v_wt
            if abs(dv) > 1e-6:
                kV += dv * dv
                n_changed += 1
        rows.append({
            "gene_id": gene.id, "gene_name": gene.name,
            "n_gpr_rxns": len(gpr_rxns), "n_changed": n_changed,
            "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
            "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
        })
        if len(rows) % 200 == 0:
            if part_csv:
                pd.DataFrame(rows).to_csv(part_csv, index=False)
            print(f"    iJO plain progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    if part_csv and rows:
        pd.DataFrame(rows).to_csv(part_csv, index=False)
    return rows


def pfba_sweep_ijo(model, b_wt, flux_wt, bio_id, part_csv=None,
                  stall_rows=None):
    """E12-convention canonical sweep, checkpointed every 400 genes."""
    rows, done_ids = _resume(part_csv)
    t0 = time.time()
    for gene in model.genes:
        if gene.id in done_ids:
            continue
        if stall_rows and gene.id in stall_rows:
            rows.append(stall_rows[gene.id])
            continue
        gpr_rxns = [r for r in gene.reactions if gene in r.genes]
        if not gpr_rxns:
            continue
        with model:
            for r in gpr_rxns:
                r.lower_bound = 0
                r.upper_bound = 0
            try:
                sol = pfba(model)
                b_ko = float(sol.fluxes[bio_id])
                flux_ko = sol.fluxes.to_dict()
            except Exception:
                b_ko, flux_ko = 0.0, {}
        kV = 0.0
        n_changed = 0
        for r_id, v_wt in flux_wt.items():
            dv = flux_ko.get(r_id, 0.0) - v_wt
            if abs(dv) > 1e-6:
                kV += dv * dv
                n_changed += 1
        rows.append({
            "gene_id": gene.id, "gene_name": gene.name,
            "n_gpr_rxns": len(gpr_rxns), "n_changed": n_changed,
            "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
            "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
        })
        if len(rows) % 400 == 0:
            if part_csv:
                pd.DataFrame(rows).to_csv(part_csv, index=False)
            print(f"    iJO canon progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    if part_csv and rows:
        pd.DataFrame(rows).to_csv(part_csv, index=False)
    return rows


def plain_sweep_iml(model, b_wt, v_wt, part_csv=None, stall_rows=None):
    """E16-convention plain sweep (the deposited O2/N/P iML-arm code),
    checkpointed every 400 genes."""
    rows, done_ids = _resume(part_csv)
    t0 = time.time()
    for g in model.genes:
        g_id = g.id
        if g_id in done_ids:
            continue
        if stall_rows and g_id in stall_rows:
            rows.append(stall_rows[g_id])
            continue
        try:
            with model:
                for r in model.reactions:
                    if g_id in r.gene_reaction_rule:
                        r.lower_bound = 0
                        r.upper_bound = 0
                ko_sol = model.optimize()
                if ko_sol.status != "optimal":
                    b_ko = 0.0
                    v_ko = np.zeros_like(v_wt)
                else:
                    b_ko = float(ko_sol.objective_value)
                    v_ko = np.array([ko_sol.fluxes.get(r.id, 0.0)
                                     for r in model.reactions])
            dv = v_ko - v_wt
            mask = np.abs(dv) > 1e-6
            kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
            n_gpr = sum(1 for r in model.reactions
                        if g_id in r.gene_reaction_rule)
            rows.append({
                "gene_id": g_id, "n_gpr_rxns": n_gpr,
                "n_changed": int(mask.sum()), "b_wt": b_wt, "b_ko": b_ko,
                "delta_b": float(b_wt - b_ko),
                "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
            })
        except Exception:
            rows.append({"gene_id": g_id, "n_gpr_rxns": 0, "n_changed": 0,
                         "b_wt": b_wt, "b_ko": float('nan'),
                         "delta_b": float('nan'), "y_essential": -1,
                         "kV": 0.0})
        if len(rows) % 400 == 0:
            if part_csv:
                pd.DataFrame(rows).to_csv(part_csv, index=False)
            print(f"    iML plain progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    if part_csv and rows:
        pd.DataFrame(rows).to_csv(part_csv, index=False)
    return [r for r in rows if r["y_essential"] >= 0]


def pfba_sweep_iml(model, b_wt, v_wt_series, bio_id, part_csv=None,
                  stall_rows=None):
    """E16-convention canonical sweep, checkpointed every 400 genes."""
    v_wt = v_wt_series
    rows, done_ids = _resume(part_csv)
    t0 = time.time()
    for g in model.genes:
        g_id = g.id
        if g_id in done_ids:
            continue
        if stall_rows and g_id in stall_rows:
            rows.append(stall_rows[g_id])
            continue
        try:
            with model:
                for r in model.reactions:
                    if g_id in r.gene_reaction_rule:
                        r.lower_bound = 0
                        r.upper_bound = 0
                try:
                    sol = pfba(model)
                    b_ko = float(sol.fluxes[bio_id])
                    v_ko = sol.fluxes
                except Exception:
                    b_ko, v_ko = 0.0, None
            if v_ko is None:
                v_ko = pd.Series(0.0, index=v_wt.index)
            dv = v_ko - v_wt
            mask = np.abs(dv) > 1e-6
            kV = float(np.sum(dv[mask] ** 2)) if mask.any() else 0.0
            n_gpr = sum(1 for r in model.reactions
                        if g_id in r.gene_reaction_rule)
            rows.append({
                "gene_id": g_id, "n_gpr_rxns": n_gpr,
                "n_changed": int(mask.sum()), "b_wt": b_wt, "b_ko": b_ko,
                "delta_b": float(b_wt - b_ko),
                "y_essential": 1 if b_ko < 0.05 * b_wt else 0, "kV": kV,
            })
        except Exception:
            rows.append({"gene_id": g_id, "n_gpr_rxns": 0, "n_changed": 0,
                         "b_wt": b_wt, "b_ko": float('nan'),
                         "delta_b": float('nan'), "y_essential": -1,
                         "kV": 0.0})
        if len(rows) % 400 == 0:
            if part_csv:
                pd.DataFrame(rows).to_csv(part_csv, index=False)
            print(f"    iML canon progress {len(rows)}/{len(model.genes)}"
                  f" ({time.time()-t0:.0f}s)", flush=True)
    if part_csv and rows:
        pd.DataFrame(rows).to_csv(part_csv, index=False)
    return [r for r in rows if r["y_essential"] >= 0]


# =====================================================================
# PART 1: iJO1366 iron gradient -- plain + canonical per level
# (resumable per level; artifacts checkpointed after each)
# =====================================================================
IJO_JSON = os.path.join(OUT_DIR, "keio_iron_limited_e12_results.json")
IJO_CSV = os.path.join(OUT_DIR, "keio_iron_limited_e12_sweep.csv")
CTRL_JSON = os.path.join(OUT_DIR, "keio_iron_pfba_control.json")
keio_tab, st6_tab = keio_tables()

ijo_results = {"probe": "iron-limited medium, iJO1366 gradient",
               "baseline_medium": "glucose -10, O2 -20, minerals -1000, "
                                  "EX_tre_e CLOSED (glucose-only run), "
                                  "iron only via EX_fe2_e",
               "levels": {}}
control = {"ijo_levels": {}, "iml_levels": {},
           "method_note": (
               "Canonical kV values are pFBA (parsimonious) vertices for "
               "the wild type and every knockout; biomass rates are read "
               "from the solution vector at the biomass reaction (cobra's "
               "pfba().objective_value returns the minimized L1 total "
               "flux, not the growth rate). Objective preservation "
               "verified per level; labels unchanged by construction and "
               "verified against the plain arm (Cohen kappa).")}
if os.path.exists(IJO_JSON):
    ijo_results = json.load(open(IJO_JSON))
if os.path.exists(CTRL_JSON):
    try:
        old = json.load(open(CTRL_JSON))
        control.update({k: v for k, v in old.items()
                        if k in ("ijo_levels", "iml_levels")})
    except Exception:
        pass

ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
BIO_IJO = [r.id for r in ijo.reactions
           if "BIOMASS" in r.id and r.objective_coefficient != 0][0]
base_kV_ijo = pd.read_csv(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control_baseline.csv"))[
        ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})

ijo_sweep_rows = []
if os.path.exists(IJO_CSV):
    _done = pd.read_csv(IJO_CSV)
    ijo_sweep_rows = [g for _, g in _done.groupby("fe_bound")]
    have = {float(g["fe_bound"].iloc[0]) for g in ijo_sweep_rows}
else:
    have = set()

print("=" * 78)
print("FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (iJO1366)")
print("  Baseline: glucose-only medium (glc -10, O2 -20, tre CLOSED)")
print(f"  Probe levels: EX_fe2_e in {IJO_FE_LEVELS} (EX_fe3_e closed)")
print(f"  (resuming with {sorted(have)} already swept)")
print("=" * 78, flush=True)

for fe in IJO_FE_LEVELS:
    key = key_of(fe)
    need_plain = fe not in have or key not in ijo_results["levels"]
    need_canon = key not in control["ijo_levels"] or not os.path.exists(
        os.path.join(OUT_DIR, f"keio_iron_pfba_control_{key}.csv"))
    if not need_plain and not need_canon:
        print(f"{key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iJO1366, EX_fe2_e = {fe} -----", flush=True)
    set_ijo_fe(ijo, fe)
    sig = degeneracy_signature(ijo, BIO_IJO)
    assert sig["objective_abs_diff"] < 1e-6, sig
    print(f"  WT {sig['fba_optimum']:.6f}; Fe2 uptake "
          f"{sig['fe2_uptake']}; glc raw {sig['raw_glc_uptake']} / "
          f"pFBA {sig['pfba_glc_uptake']}; PGI width "
          f"{sig['fva_widths'].get('PGI')}", flush=True)

    plain_df = None
    if need_plain:
        t0 = time.time()
        wt = ijo.optimize()
        b_wt = float(wt.objective_value)
        flux_wt = wt.fluxes.to_dict()
        byp = {r: round(float(flux_wt.get(r, 0.0)), 3) for r in BYPRODUCTS
               if abs(flux_wt.get(r, 0.0)) > 1e-6}
        rows = plain_sweep_ijo(ijo, b_wt, flux_wt,
                               part_csv=os.path.join(
                                   OUT_DIR,
                                   f"keio_iron_partial_ijo_p_{key}.csv"),
                               stall_rows=build_stall_rows(
                                   ijo, key, "ijo", BIO_IJO, flux_wt,
                                   b_wt, "plain"))
        plain_df = pd.DataFrame(rows)
        plain_df.insert(0, "fe_bound", fe)
        print(f"  plain sweep done ({time.time()-t0:.0f}s), "
              f"{len(plain_df)} genes", flush=True)
        others = [r for r in ijo_sweep_rows
                  if float(r["fe_bound"].iloc[0]) != fe]
        ijo_sweep_rows = others + [plain_df]
        pd.concat(ijo_sweep_rows).to_csv(IJO_CSV, index=False)
        try:
            os.remove(os.path.join(
                OUT_DIR, f"keio_iron_partial_ijo_p_{key}.csv"))
        except Exception:
            pass
        cal = transitive_calibration(plain_df)
        da, _ = direct_arm(plain_df, keio_tab, st6_tab)
        fl, _ = flip_analysis(
            plain_df, os.path.join(OUT_DIR, "keio_glucose_only_e12.csv"),
            ijo, f"Fe={fe} vs glucose-only (Fe unlimited)")
        ijo_results["levels"][key] = {
            "fe_bound": fe, "wild_type_biomass": b_wt,
            "fe2_uptake": sig["fe2_uptake"], "byproducts": byp,
            "degeneracy": sig,
            "transitive_calibration": cal, "direct_arm": da,
            "flips_vs_glucose_only": fl,
        }
        with open(IJO_JSON, "w") as f:
            json.dump(ijo_results, f, indent=2)
        print(f"  PLAIN: r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"AUC = {cal['held_out']['roc_auc']:.4f}; labels "
              f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
              f"(+{fl['n_gain_essential']}/-{fl['n_loss_essential']}, "
              f"kappa {fl['cohen_kappa']:.4f}); direct "
              f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)
    else:
        _d = pd.read_csv(IJO_CSV)
        plain_df = _d[_d["fe_bound"] == fe]
        cal = ijo_results["levels"][key]["transitive_calibration"]

    if need_canon:
        t0 = time.time()
        par_wt = pfba(ijo)
        b_wt_c = float(par_wt.fluxes[BIO_IJO])
        rows = pfba_sweep_ijo(ijo, b_wt_c, par_wt.fluxes.to_dict(),
                              BIO_IJO,
                              part_csv=os.path.join(
                                  OUT_DIR, f"keio_iron_partial_ijo_c_{key}.csv"),
                              stall_rows=build_stall_rows(
                                  ijo, key, "ijo", BIO_IJO,
                                  par_wt.fluxes.to_dict(), b_wt_c,
                                  "canon"))
        cdf = pd.DataFrame(rows)
        print(f"  canonical sweep done ({time.time()-t0:.0f}s), "
              f"{len(cdf)} genes, {int(cdf.y_essential.sum())} essential",
              flush=True)
        ccal = transitive_calibration(cdf)
        cda, _ = direct_arm(cdf, keio_tab, st6_tab)
        mg = cdf[["gene_id", "kV"]].merge(base_kV_ijo, on="gene_id")
        rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
        mgl = plain_df[["gene_id", "y_essential"]].merge(
            cdf[["gene_id", "y_essential"]], on="gene_id",
            suffixes=("_fba", "_canon"))
        kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                            mgl.y_essential_canon))
        control["ijo_levels"][key] = {
            "wild_type_biomass": b_wt_c,
            "n_essential": int(cdf.y_essential.sum()),
            "n_genes": int(len(cdf)),
            "transitive_calibration": ccal, "direct_arm": cda,
            "kV_rank_corr_vs_baseline_canonical": rho,
            "label_agreement_fba_vs_pfba_kappa": kappa_lab,
            "objective_preservation": sig,
            "plain_reference_r": cal["pearson_r_log_kV_delta_b"],
            "plain_reference_auc": cal["held_out"]["roc_auc"],
        }
        cdf.to_csv(os.path.join(
            OUT_DIR, f"keio_iron_pfba_control_{key}.csv"), index=False)
        try:
            os.remove(os.path.join(
                OUT_DIR, f"keio_iron_partial_ijo_c_{key}.csv"))
        except Exception:
            pass
        with open(CTRL_JSON, "w") as f:
            json.dump(control, f, indent=2)
        print(f"  CANON: r = {ccal['pearson_r_log_kV_delta_b']:+.4f} "
              f"(plain {cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
              f"{ccal['held_out']['roc_auc']:.4f}; MCC "
              f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; "
              f"label kappa {kappa_lab:.4f}", flush=True)

with open(IJO_JSON, "w") as f:
    json.dump(ijo_results, f, indent=2)
with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)

# =====================================================================
# PART 2: iML1515 cross-rebuild at Fe -0.005 and -0.0025
# =====================================================================
print("\n" + "=" * 78)
print("FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM (iML1515)")
print("=" * 78, flush=True)
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
BIO_IML = None
for r in iml.reactions:
    if r.objective_coefficient != 0 and "iomass" in r.id:
        BIO_IML = r.id
        break
assert BIO_IML, "iML biomass reaction not found"

IML_JSON = os.path.join(OUT_DIR, "keio_iron_limited_e16_results.json")
IML_CSV = os.path.join(OUT_DIR, "keio_iron_limited_e16_sweep.csv")
iml_results = {"probe": "iron-limited medium, iML1515 cross-rebuild",
               "baseline_medium": "glucose -10, O2 -20, minerals -10, "
                                  "EX_tre_e CLOSED, EX_fe3_e CLOSED "
                                  "(iron only via EX_fe2_e)",
               "levels": {}}
if os.path.exists(IML_JSON):
    iml_results = json.load(open(IML_JSON))

# iML baseline canonical reference (glucose-only medium, O2 -20) --
# computed by the O2 canonical control
iml_base_canon_csv = os.path.join(OUT_DIR,
                                  "keio_o2_pfba_control_iml_baseline.csv")
assert os.path.exists(iml_base_canon_csv), \
    "iML canonical baseline missing (run o2_pfba_control first)"
base_kV_iml = pd.read_csv(iml_base_canon_csv)[
    ["gene_id", "kV"]].rename(columns={"kV": "kV_base"})
print("iML baseline kV reference: canonical (o2 control baseline)",
      flush=True)

iml_sweep_rows = []
if os.path.exists(IML_CSV):
    _done = pd.read_csv(IML_CSV)
    iml_sweep_rows = [g for _, g in _done.groupby("fe_bound")]
    have_iml = {float(g["fe_bound"].iloc[0]) for g in iml_sweep_rows}
else:
    have_iml = set()

for fe in IML_FE_LEVELS:
    key = key_of(fe)
    need_plain = fe not in have_iml or key not in iml_results["levels"]
    need_canon = key not in control["iml_levels"] or not os.path.exists(
        os.path.join(OUT_DIR, f"keio_iron_pfba_control_iml_{key}.csv"))
    if not need_plain and not need_canon:
        print(f"iML {key}: already done -- skipping", flush=True)
        continue
    print(f"\n----- iML1515, EX_fe2_e = {fe} (EX_fe3_e closed) -----",
          flush=True)
    set_iml_fe(iml, fe)
    sig = degeneracy_signature(iml, BIO_IML)
    assert sig["objective_abs_diff"] < 1e-6, sig
    print(f"  WT {sig['fba_optimum']:.6f}; Fe2 uptake "
          f"{sig['fe2_uptake']}; glc raw {sig['raw_glc_uptake']} / "
          f"pFBA {sig['pfba_glc_uptake']}; PGI width "
          f"{sig['fva_widths'].get('PGI')}", flush=True)

    plain_df = None
    if need_plain:
        t0 = time.time()
        wt = iml.optimize()
        b_wt = float(wt.objective_value)
        v_wt = np.array([wt.fluxes.get(r.id, 0.0) for r in iml.reactions])
        rows = plain_sweep_iml(iml, b_wt, v_wt,
                               part_csv=os.path.join(
                                   OUT_DIR,
                                   f"keio_iron_partial_iml_p_{key}.csv"),
                               stall_rows=build_stall_rows(
                                   iml, key, "iml", BIO_IML,
                                   dict(zip([r.id for r in iml.reactions],
                                            v_wt)), b_wt, "plain"))
        plain_df = pd.DataFrame(rows)
        plain_df.insert(0, "fe_bound", fe)
        print(f"  plain sweep done ({time.time()-t0:.0f}s), "
              f"{len(plain_df)} genes", flush=True)
        others = [r for r in iml_sweep_rows
                  if float(r["fe_bound"].iloc[0]) != fe]
        iml_sweep_rows = others + [plain_df]
        pd.concat(iml_sweep_rows).to_csv(IML_CSV, index=False)
        cal = transitive_calibration(plain_df)
        da, _ = direct_arm(plain_df, keio_tab, st6_tab)
        fl, _ = flip_analysis(
            plain_df, os.path.join(OUT_DIR,
                                   "keio_glucose_only_e16_sweep.csv"),
            iml, f"iML1515 Fe={fe} vs glucose-only (Fe unlimited)")
        iml_results["levels"][key] = {
            "fe_bound": fe, "wild_type_biomass": b_wt,
            "fe2_uptake": sig["fe2_uptake"],
            "degeneracy": sig,
            "transitive_calibration": cal, "direct_arm": da,
            "flips_vs_glucose_only": fl,
        }
        with open(IML_JSON, "w") as f:
            json.dump(iml_results, f, indent=2)
        print(f"  PLAIN: r = {cal['pearson_r_log_kV_delta_b']:+.4f}; "
              f"AUC = {cal['held_out']['roc_auc']:.4f}; labels "
              f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
              f"(+{fl['n_gain_essential']}/-{fl['n_loss_essential']}, "
              f"kappa {fl['cohen_kappa']:.4f}); direct "
              f"{da['pearson_r']:+.4f}/{da['roc_auc']:.4f}", flush=True)
    else:
        _d = pd.read_csv(IML_CSV)
        plain_df = _d[_d["fe_bound"] == fe]
        cal = iml_results["levels"][key]["transitive_calibration"]

    if need_canon:
        t0 = time.time()
        par_wt = pfba(iml)
        b_wt_c = float(par_wt.fluxes[BIO_IML])
        rows = pfba_sweep_iml(iml, b_wt_c, par_wt.fluxes, BIO_IML,
                              part_csv=os.path.join(
                                  OUT_DIR,
                                  f"keio_iron_partial_iml_c_{key}.csv"),
                              stall_rows=build_stall_rows(
                                  iml, key, "iml", BIO_IML,
                                  par_wt.fluxes.to_dict(), b_wt_c,
                                  "canon"))
        cdf = pd.DataFrame(rows)
        print(f"  canonical sweep done ({time.time()-t0:.0f}s), "
              f"{len(cdf)} genes, {int(cdf.y_essential.sum())} essential",
              flush=True)
        ccal = transitive_calibration(cdf)
        cda, _ = direct_arm(cdf, keio_tab, st6_tab)
        mg = cdf[["gene_id", "kV"]].merge(base_kV_iml, on="gene_id")
        rho = float(spearmanr(mg.kV, mg.kV_base).statistic)
        mgl = plain_df[["gene_id", "y_essential"]].merge(
            cdf[["gene_id", "y_essential"]], on="gene_id",
            suffixes=("_fba", "_canon"))
        kappa_lab = float(cohen_kappa_score(mgl.y_essential_fba,
                                            mgl.y_essential_canon))
        control["iml_levels"][key] = {
            "wild_type_biomass": b_wt_c,
            "n_essential": int(cdf.y_essential.sum()),
            "n_genes": int(len(cdf)),
            "transitive_calibration": ccal, "direct_arm": cda,
            "kV_rank_corr_vs_baseline_canonical": rho,
            "kV_rank_reference": "canonical (o2 control baseline)",
            "label_agreement_fba_vs_pfba_kappa": kappa_lab,
            "objective_preservation": sig,
            "plain_reference_r": cal["pearson_r_log_kV_delta_b"],
            "plain_reference_auc": cal["held_out"]["roc_auc"],
        }
        cdf.to_csv(os.path.join(
            OUT_DIR,
            f"keio_iron_pfba_control_iml_{key}.csv"), index=False)
        try:
            os.remove(os.path.join(
                OUT_DIR, f"keio_iron_partial_iml_c_{key}.csv"))
        except Exception:
            pass
        with open(CTRL_JSON, "w") as f:
            json.dump(control, f, indent=2)
        print(f"  CANON: r = {ccal['pearson_r_log_kV_delta_b']:+.4f} "
              f"(plain {cal['pearson_r_log_kV_delta_b']:+.4f}); AUC "
              f"{ccal['held_out']['roc_auc']:.4f}; MCC "
              f"{ccal['held_out']['mcc']:.4f}; rank corr {rho:+.4f}; "
              f"label kappa {kappa_lab:.4f}", flush=True)

with open(IML_JSON, "w") as f:
    json.dump(iml_results, f, indent=2)
with open(CTRL_JSON, "w") as f:
    json.dump(control, f, indent=2)

# =====================================================================
# PART 3: summary
# =====================================================================
lines = []
lines.append("FIFTH PERTURBATION AXIS: IRON-LIMITED MEDIUM")
lines.append("Trace-metal supply axis (iJO1366 + iML1515, iron only "
             "via EX_fe2_e)")
lines.append("=" * 78)
lines.append("Baseline: glucose-only corrected medium (trehalose "
             "closed), Fe unlimited. Probe: EX_fe2_e bound "
             "(EX_fe3_e closed; single-channel iron).")
lines.append("Levels chosen by pre-screen (parsimonious requirement "
             "0.0158 iJO / 0.0132 iML; identical linear quota map "
             "b = fe2/0.016067 on both reconstructions):")
lines.append("  iJO1366: -0.01, -0.005, -0.0025 "
             "(37% / 68% / 84% WT reduction)")
lines.append("  iML1515: -0.005, -0.0025 (62% / 81% WT reduction)")
lines.append("Zinc and manganese rejected by the pre-screen "
             "(compressed informative bands at the 1e-4 bound scale).")
lines.append("")
base_ijo = json.load(open(os.path.join(OUT_DIR,
                                       "keio_glucose_only_e12_results.json")))
lines.append(f"iJO1366 baseline: WT {base_ijo['wild_type_biomass']:.4f}, "
             f"{base_ijo['n_essential']}/{base_ijo['n_genes_processed']} "
             f"essential, plain r = "
             f"{base_ijo['calibration']['pearson_r_log_kV_delta_b']:+.4f}")
nctrl = json.load(open(os.path.join(
    OUT_DIR, "keio_nitrogen_pfba_control.json")))
bl = nctrl["levels"]["baseline"]["transitive_calibration"]
lines.append(f"             canonical r = "
             f"{bl['pearson_r_log_kV_delta_b']:+.4f} "
             f"(AUC {bl['held_out']['roc_auc']:.4f})")
for fe in IJO_FE_LEVELS:
    key = key_of(fe)
    lv = ijo_results["levels"][key]
    cal = lv["transitive_calibration"]
    fl = lv["flips_vs_glucose_only"]
    sig = lv["degeneracy"]
    c = control["ijo_levels"][key]
    ccal = c["transitive_calibration"]
    lines.append(
        f"Fe = {fe:>7}: WT {lv['wild_type_biomass']:.4f} "
        f"(-{100*(1-lv['wild_type_biomass']/base_ijo['wild_type_biomass']):.0f}%); "
        f"labels {fl['n_essential_base']} -> {fl['n_essential_new']} "
        f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, kappa "
        f"{fl['cohen_kappa']:.4f}); plain r = "
        f"{cal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{cal['held_out']['roc_auc']:.4f}; canonical r = "
        f"{ccal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{ccal['held_out']['roc_auc']:.4f} / MCC "
        f"{ccal['held_out']['mcc']:.4f}; PGI FVA width "
        f"{sig['fva_widths'].get('PGI')}")
lines.append("")
for fe in IML_FE_LEVELS:
    key = key_of(fe)
    lv = iml_results["levels"][key]
    cal = lv["transitive_calibration"]
    fl = lv["flips_vs_glucose_only"]
    c = control["iml_levels"][key]
    ccal = c["transitive_calibration"]
    lines.append(
        f"iML1515 Fe = {fe}: WT {lv['wild_type_biomass']:.4f}; labels "
        f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
        f"(+{fl['n_gain_essential']} / -{fl['n_loss_essential']}, kappa "
        f"{fl['cohen_kappa']:.4f}); plain r = "
        f"{cal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{cal['held_out']['roc_auc']:.4f}; canonical r = "
        f"{ccal['pearson_r_log_kV_delta_b']:+.4f} / AUC "
        f"{ccal['held_out']['roc_auc']:.4f}")
lines.append("")
lines.append("Flip details (iJO):")
for fe in IJO_FE_LEVELS:
    fl = ijo_results["levels"][key_of(fe)]["flips_vs_glucose_only"]
    if fl["n_gain_essential"] + fl["n_loss_essential"] == 0:
        continue
    lines.append(f"  Fe = {fe}: gains "
                 + ", ".join(f"{g['gene_id']}"
                             f"({g.get('gene_name', '')})"
                             for g in fl["gains"][:20])
                 + "; losses "
                 + ", ".join(f"{g['gene_id']}"
                             f"({g.get('gene_name', '')})"
                             for g in fl["losses"][:20]))
    lines.append(f"    enrichments: " + "; ".join(
        f"{d['subsystem']} ({d['n_flip']} vs exp {d['expected']})"
        for d in fl["subsystem_enrichment_top"][:5]))
with open(os.path.join(OUT_DIR, "keio_iron_limited_summary.txt"),
          "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nSummary written.")
print("IRON-LIMITED PROBE DONE.")
