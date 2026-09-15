#!/usr/bin/env python3
"""Solver-tolerance integrity scan for the iron-limited probe.

The solver-integrity round (phosphate/O2 homogenization) characterized
a one-directional false-viability failure mode: at level WT growth
below ~0.14, growth-scaled trace-quota drains (biotin 2e-6, qu8 side
chain) fall within ~2x of the simplex's 1e-7 primal feasibility
tolerance, so bound violations at knocked-out trace-quota steps can be
accepted and a truly lethal KO can be reported with small positive
growth.  The iron probe's deepest levels sit at WT 0.156 -- just above
that boundary -- so this scan closes the residual risk explicitly.

Checks per level (both models, both arms):
  1. CROSS-ARM AGREEMENT (all genes): plain-FBA and pFBA preserve the
     same optimum, so b_ko must agree between the deposited plain and
     canonical sweeps to solver tolerance.  Any discrepancy is a
     solver artifact, wherever it lands.
  2. FALSE-VIABILITY BAND CENSUS: rows with 0.001 < b_ko < 0.14 (the
     empirical corruption band -- large enough to matter, small enough
     to be drain-limited) are listed with gene names.
  3. TRACE-QUOTA GENE CENSUS: the biotin / quinone-side-chain /
     fatty-acid-synthase gene rows are reported at every level
     regardless of band.
  4. HiGHS RE-ADJUDICATION: every gene flagged by (2), plus any gene
     whose cross-arm discrepancy exceeds 1e-6, is re-solved with the
     deterministic scipy/HiGHS engine (stage-1 for the plain
     convention, stage-1+2 min-L1 for the canonical convention); the
     verdict records agreement or corruption.

Artifacts: download/keio_iron_integrity_scan.json (+ console table)
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT_DIR = os.path.join(REPO, "download")

from cobra.io import load_json_model
from lp_engine import LPEngine

IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']

TRACE_QUOTA_NAMES = {
    "bioA", "bioB", "bioC", "bioD", "bioF", "bioH",  # biotin cluster
    "fabZ", "fabA", "fabB", "fabD", "fabF", "fabG", "fabH", "fabI",
    "fabK", "fabL", "fabM", "fabR", "fabV",           # FAS II
    "ubiA", "ubiB", "ubiC", "ubiD", "ubiE", "ubiF", "ubiG", "ubiH",
    "ubiI", "ubiX", "menA", "menB", "menC", "menD", "menE", "menF",
    "menH", "menI",                                    # quinone rings
}

LEVELS = {
    "ijo": {
        "fe_0.01": -0.01, "fe_0.005": -0.005, "fe_0.0025": -0.0025,
        "plain_csv": "keio_iron_limited_e12_sweep.csv",
        "canon_fmt": "keio_iron_pfba_control_{key}.csv",
        "results": "keio_iron_limited_e12_results.json",
        "model": "data/bigg_models/iJO1366.json",
    },
    "iml": {
        "fe_0.005": -0.005, "fe_0.0025": -0.0025,
        "plain_csv": "keio_iron_limited_e16_sweep.csv",
        "canon_fmt": "keio_iron_pfba_control_iml_{key}.csv",
        "results": "keio_iron_limited_e16_results.json",
        "model": "data/bigg_models/iML1515.json",
    },
}


def set_ijo_fe(model, fe_lb):
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
    model.reactions.get_by_id("EX_fe3_e").lower_bound = 0


def solve_stages(eng, lb, ub, bio_idx, mu_tol=1e-9):
    R = eng.R
    fub = np.maximum(ub, 0.0)
    rub = np.maximum(-lb, 0.0)
    vlb = np.concatenate([lb, np.zeros(R), np.zeros(R)])
    vub = np.concatenate([ub, fub, rub])
    c1 = np.zeros(3 * R)
    c1[:R] = -eng.c_bio
    res = eng._lp(c1, np.column_stack((vlb, vub)))
    if not res.success:
        return None, None
    mu = float(res.x[bio_idx])
    v_plain = res.x[:R].copy()
    vlb2 = vlb.copy()
    vlb2[bio_idx] = max(vlb2[bio_idx], mu - mu_tol * max(1.0, abs(mu)))
    c2 = np.concatenate([np.zeros(R), np.ones(R), np.ones(R)])
    res2 = eng._lp(c2, np.column_stack((vlb2, vub)))
    v_canon = res2.x[:R].copy() if res2.success else None
    return v_plain, v_canon


report = {"levels": {}, "note": (
    "Cross-arm agreement exploits objective preservation: plain FBA "
    "and pFBA return the same optimal growth, so per-gene b_ko must "
    "match across the deposited plain and canonical sweeps.  HiGHS "
    "re-adjudication uses the repo's deterministic split-variable "
    "engine (scripts/lp_engine.py).")}

models = {}
engines = {}


def gene_name_map(which, cfg):
    if which not in models:
        models[which] = load_json_model(os.path.join(REPO, cfg["model"]))
    return {g.id: (g.name or "") for g in models[which].genes}

for which, cfg in LEVELS.items():
    res_json = json.load(open(os.path.join(OUT_DIR, cfg["results"])))
    plain_all = pd.read_csv(os.path.join(OUT_DIR, cfg["plain_csv"]))
    fe_entries = {k: v for k, v in cfg.items() if k.startswith("fe_")}
    for key, fe_lb in fe_entries.items():
        lv_id = f"{which}_{key}"
        canon = pd.read_csv(os.path.join(
            OUT_DIR, cfg["canon_fmt"].format(key=key)))
        plain = plain_all[plain_all["fe_bound"] == fe_lb]
        b_wt = res_json["levels"][key]["wild_type_biomass"]
        thr = 0.05 * b_wt
        m = plain[["gene_id", "b_ko", "y_essential", "kV"]].merge(
            canon[["gene_id", "b_ko", "y_essential", "kV"]],
            on="gene_id", suffixes=("_plain", "_canon"))
        rec = {
            "wild_type_biomass": b_wt,
            "label_threshold": thr,
            "n_genes": int(len(m)),
            "label_disagreements": int(
                (m.y_essential_plain != m.y_essential_canon).sum()),
        }
        d = (m.b_ko_plain - m.b_ko_canon).abs()
        rec["cross_arm_max_abs_b_ko_diff"] = float(d.max())
        rec["cross_arm_n_diff_gt_1e-6"] = int((d > 1e-6).sum())
        rec["cross_arm_n_diff_gt_1e-9"] = int((d > 1e-9).sum())
        top = m.assign(diff=d).nlargest(5, "diff")[
            ["gene_id", "b_ko_plain", "b_ko_canon", "diff"]]
        rec["cross_arm_top5_diffs"] = top.round(9).to_dict("records")

        # false-viability band census (both arms)
        band = {}
        for arm in ("plain", "canon"):
            b = m[f"b_ko_{arm}"]
            band[arm] = {
                "exact_zero_lt_1e-9": int((b.abs() < 1e-9).sum()),
                "tiny_1e-9_to_0p001": int(
                    ((b.abs() >= 1e-9) & (b < 0.001)).sum()),
                "band_0p001_to_0p14": int(
                    ((b >= 0.001) & (b < 0.14)).sum()),
                "ge_0p14": int((b >= 0.14).sum()),
            }
        rec["b_ko_census"] = band
        susp = m[(m.b_ko_plain >= 0.001) & (m.b_ko_plain < 0.14) |
                 (m.b_ko_canon >= 0.001) & (m.b_ko_canon < 0.14)]
        # trace-quota gene rows
        if "gene_name" in plain.columns:
            tq = plain[plain["gene_name"].isin(TRACE_QUOTA_NAMES)][
                ["gene_id", "gene_name", "b_ko", "y_essential"]]
        else:
            nm = gene_name_map(which, cfg)
            tq = plain[plain["gene_id"].map(nm).isin(TRACE_QUOTA_NAMES)][
                ["gene_id", "b_ko", "y_essential"]].copy()
            tq["gene_name"] = tq["gene_id"].map(nm)
            tq = tq[["gene_id", "gene_name", "b_ko", "y_essential"]]
        rec["trace_quota_rows"] = tq.to_dict("records")
        rec["n_trace_quota_nonzero"] = int(
            (tq.b_ko.abs() > 1e-9).sum())

        flagged = set(susp["gene_id"]) | set(
            m[d > 1e-6]["gene_id"])
        rec["n_flagged_for_adjudication"] = len(flagged)
        if flagged:
            # HiGHS re-adjudication
            if which not in models:
                models[which] = load_json_model(
                    os.path.join(REPO, cfg["model"]))
            model = models[which]
            setter = set_ijo_fe if which == "ijo" else set_iml_fe
            setter(model, fe_lb)
            ekey = (which, key)
            if ekey not in engines:
                bio_idx = None
                c_bio = np.zeros(len(model.reactions))
                for j, r in enumerate(model.reactions):
                    if r.objective_coefficient != 0:
                        c_bio[j] = float(r.objective_coefficient)
                        if "iomass" in r.id or "BIOMASS" in r.id:
                            bio_idx = j
                assert bio_idx is not None
                engines[ekey] = (LPEngine(
                    model, np.zeros(len(model.reactions)), c_bio),
                    bio_idx,
                    np.array([r.lower_bound
                              for r in model.reactions]),
                    np.array([r.upper_bound
                              for r in model.reactions]))
            eng, bio_idx, lb0, ub0 = engines[ekey]
            verdicts = []
            for gid in sorted(flagged):
                g = model.genes.get_by_id(gid)
                gpr = [r for r in g.reactions if g in r.genes]
                lb, ub = lb0.copy(), ub0.copy()
                for r in gpr:
                    lb[eng.index[r.id]] = 0.0
                    ub[eng.index[r.id]] = 0.0
                v_plain, v_canon = solve_stages(eng, lb, ub, bio_idx)
                row = m[m.gene_id == gid].iloc[0]
                hp = float(v_plain[bio_idx]) if v_plain is not None else None
                hc = float(v_canon[bio_idx]) if v_canon is not None else None
                okp = hp is not None and abs(hp - row.b_ko_plain) <= 1e-6
                okc = hc is not None and abs(hc - row.b_ko_canon) <= 1e-6
                verdicts.append({
                    "gene_id": gid, "gene_name": g.name,
                    "b_ko_plain_deposited": float(row.b_ko_plain),
                    "b_ko_plain_highs": hp,
                    "b_ko_canon_deposited": float(row.b_ko_canon),
                    "b_ko_canon_highs": hc,
                    "plain_agrees": bool(okp),
                    "canon_agrees": bool(okc),
                    "verdict": ("CLEAN" if okp and okc else
                                "CORRUPTED -- requires patch"),
                })
            rec["adjudications"] = verdicts
        report["levels"][lv_id] = rec
        print(f"{lv_id}: WT {b_wt:.4f}; cross-arm max diff "
              f"{rec['cross_arm_max_abs_b_ko_diff']:.2e} "
              f"({rec['cross_arm_n_diff_gt_1e-6']} > 1e-6); band "
              f"0.001-0.14: plain "
              f"{band['plain']['band_0p001_to_0p14']} / canon "
              f"{band['canon']['band_0p001_to_0p14']}; trace-quota "
              f"nonzero {rec['n_trace_quota_nonzero']}; flagged "
              f"{rec['n_flagged_for_adjudication']}", flush=True)

with open(os.path.join(OUT_DIR, "keio_iron_integrity_scan.json"),
          "w") as f:
    json.dump(report, f, indent=2)

n_bad = sum(1 for lv in report["levels"].values()
            for a in lv.get("adjudications", [])
            if not (a["plain_agrees"] and a["canon_agrees"]))
print(f"\nIRON INTEGRITY SCAN DONE: {n_bad} corrupted call(s).")
