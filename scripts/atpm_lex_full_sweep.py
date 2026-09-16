#!/usr/bin/env python3
"""Full canonical sweeps under the DECLARED lexicographic tie-break
(3-stage lex pFBA) at the four floor-affected ATPM levels, completing
the sixth axis under the declared protocol.

Evidence base (keio_atpm_lex_pilot.json, pre-registered verdict
PROMOTE): the deterministic stage-3 tie-break (min w^T v over the
pinned parsimony face, w = U(0.5,1.5) fixed seed 20240901 -- the
locked protocol's declared TB0 convention) selects the SAME vertex
under the GLPK warm-start path and stateless cold-start HiGHS
(cross-engine vertex distance <= 6e-11 on the 105-gene stratified
pilot + WT at both worst levels; floor collapse 40/40 random floor
genes in both engines; labels unchanged <= 6.4e-08).  This script
turns that vertex-level proof into the instrument-level reading: the
full per-gene lex sweeps, the same-convention statistics, and the
floor census under the declared rule.

Scope (the floor-affected levels only -- at the remaining ATPM levels
the at-optimum vertex is already unique and the two engines' 2-stage
readings agree to <= 0.002, so a lex re-run there would be empty
computation):
  - iML1515 ATPM 60 / 80 / 100 (deposited GLPK floors 500/650/782 of
    1,127 compensables; engine bracket disclosed by Patch I)
  - iJO1366 ATPM 40 (deposited GLPK floor 961/971; the stateless
    2-stage collapse measured by the symmetric second-engine round)

Engine: stateless cold-start HiGHS via the pilot's HighsLex class
(imported, not duplicated); the cross-engine claim stays at the
pilot's measured scope.  Medium, knockout conventions (substring for
iML / proper GPR for iJO -- each model's own deposit convention), kV
definition, label rule, and statistics functions identical to the
probe and the second-engine scripts; WT reference = the engine's own
fresh lex solve per level (biomass checked against the deposit).

Artifacts:
  download/keio_atpm_lex_full_sweep.json
  download/keio_atpm_lex_full_sweep_iml_{key}.csv
  download/keio_atpm_lex_full_sweep_ijo_{key}.csv
Resumable: per-level scratch CSV every 20 newly processed genes.
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score
from cobra.io import load_json_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
DL = os.path.join(REPO, "download")

# nitrogen_source_keio_probe is a flat script: importing it executes
# the (resumable, ~7 s) nitrogen round and clobbers the response
# figure with the legacy figure.  Snapshot BEFORE the import; restore
# on clean exit (timeout-killed chunks are restored manually via git).
NITRO_FIG = os.path.join(DL, "keio_nitrogen_source_response.png")
_nitro_snap = None
if os.path.exists(NITRO_FIG):
    with open(NITRO_FIG, "rb") as _f:
        _nitro_snap = _f.read()

from nitrogen_source_keio_probe import (keio_tables, transitive_calibration,
                                        direct_arm)
from atpm_lex_tiebreak_pilot import (HighsLex, set_iml, set_ijo, kv_dist,
                                     SEED_W)

LEVELS = {
    "iml": {"path": "data/bigg_models/iML1515.json", "setter": set_iml,
            "atpm": [60.0, 80.0, 100.0],
            "dep_wt": {60.0: 0.39839, 80.0: 0.239034, 100.0: 0.079678},
            "glpk_csv": "keio_atpm_pfba_control_iml_{key}.csv",
            "stateless_csv": "keio_atpm_iml_second_engine_{key}.csv",
            "glpk_r_key": ("iml_levels", "atpm_{key}")},
    "ijo": {"path": "data/bigg_models/iJO1366.json", "setter": set_ijo,
            "atpm": [40.0],
            "dep_wt": {40.0: 0.6947359182109596},
            "glpk_csv": "keio_atpm_pfba_control_{key}.csv",
            "stateless_csv": "keio_atpm_ijo_second_engine_{key}.csv",
            "glpk_r_key": ("ijo_levels", "atpm_{key}")},
}
OUT_JSON = os.path.join(DL, "keio_atpm_lex_full_sweep.json")


def key_of(lb):
    return f"atpm_{lb:g}"


def floor_census(df, b_wt):
    """Compensable = b_ko >= 0.999 * b_wt; floor band kV in [190, 210]."""
    comp = df[df.b_ko >= 0.999 * b_wt]
    kv = comp.kV
    floor = comp[(comp.kV >= 190.0) & (comp.kV <= 210.0)]
    return {
        "n_compensable": int(len(comp)),
        "n_floor_190_210": int(len(floor)),
        "floor_kv_median": (float(floor.kV.median())
                            if len(floor) else None),
        "n_kv_le_0p1": int((kv <= 0.1).sum()),
        "n_kv_0p1_to_190": int(((kv > 0.1) & (kv < 190.0)).sum()),
        "n_kv_gt_210": int((kv > 210.0).sum()),
        "compensable_kv_median": float(kv.median()),
    }


def _restore_nitro_fig():
    if _nitro_snap is not None:
        with open(NITRO_FIG, "rb") as f:
            cur = f.read()
        if cur != _nitro_snap:
            with open(NITRO_FIG, "wb") as f:
                f.write(_nitro_snap)
            print("[restored keio_nitrogen_source_response.png -- "
                  "probe-import clobber]", flush=True)


def main():
    out = {"method_note": (
        "Full canonical sweeps under the declared lexicographic "
        "tie-break (3-stage lex pFBA: max biomass -> min L1 -> "
        "deterministic tie-break min w^T v, w = U(0.5,1.5) fixed seed "
        "20240901) at the four floor-affected ATPM levels, stateless "
        "cold-start HiGHS via the pilot's HighsLex class. Engine-"
        "invariance of the lex vertex is the pilot's measured claim "
        "(cross-engine distance <= 6e-11, 105-gene stratified sample "
        "+ WT at both worst levels). Medium, knockout, kV, label, and "
        "statistics conventions identical to the probe.")}
    if os.path.exists(OUT_JSON):
        try:
            old = json.load(open(OUT_JSON))
            if "levels" in old:
                out["levels"] = old["levels"]
        except Exception:
            pass
    out.setdefault("levels", {})
    keio_tab, st6_tab = keio_tables()

    for mtag, cfg in LEVELS.items():
        model = load_json_model(os.path.join(REPO, cfg["path"]))
        R = len(model.reactions)
        W = np.random.default_rng(SEED_W).uniform(0.5, 1.5, R)
        gene_names = {g.id: (g.name or "") for g in model.genes}
        # gene -> KO reaction indices, each model's own convention
        if mtag == "iml":          # substring convention (the iML deposit)
            rules = [r.gene_reaction_rule for r in model.reactions]
            gene_rxn_idx = {g.id: [j for j in range(R) if g.id in rules[j]]
                            for g in model.genes}
        else:                      # proper GPR parsing (the iJO deposit)
            rid_to_j = {r.id: j for j, r in enumerate(model.reactions)}
            gene_rxn_idx = {g.id: [rid_to_j[r.id] for r in g.reactions]
                            for g in model.genes}

        for atpm in cfg["atpm"]:
            key = key_of(atpm)
            lkey = f"{mtag}_{key}"
            final_csv = os.path.join(DL, f"keio_atpm_lex_full_sweep_{lkey}.csv")
            if lkey in out["levels"] and os.path.exists(final_csv):
                print(f"{lkey}: already done -- skipping", flush=True)
                continue
            print(f"\n----- {mtag} ATPM >= {atpm} (declared lex rule) -----",
                  flush=True)
            cfg["setter"](model, atpm)
            engine = HighsLex(model)
            lb0 = np.array([r.lower_bound for r in model.reactions])
            ub0 = np.array([r.upper_bound for r in model.reactions])

            b_wt, v_wt, s2_wt, s3_wt, st_wt = engine.solve_lex(lb0, ub0, W)
            assert st_wt == "ok", st_wt
            dep_wt = cfg["dep_wt"][atpm]
            print(f"  WT lex: b = {b_wt:.6f} (deposited {dep_wt}; "
                  f"|diff| {abs(b_wt-dep_wt):.2e}); L1 = "
                  f"{float(np.abs(v_wt).sum()):.6f}", flush=True)
            assert abs(b_wt - dep_wt) < 1e-6, (b_wt, dep_wt)
            l1_wt = float(np.abs(v_wt).sum())

            scratch = os.path.join(DL, f"keio_atpm_lex_full_sweep_{lkey}_partial.csv")
            rows, done = [], set()
            if os.path.exists(scratch):
                _p = pd.read_csv(scratch)
                rows = _p.to_dict("records")
                done = set(_p.gene_id.tolist())
                print(f"    resuming: {len(done)} genes already done",
                      flush=True)
            t0 = time.time()
            n_new = 0
            for g in model.genes:
                gid = g.id
                if gid in done:
                    continue
                idxs = gene_rxn_idx.get(gid, [])
                if not idxs:
                    continue
                lb_g, ub_g = lb0.copy(), ub0.copy()
                for j in idxs:
                    lb_g[j] = 0.0
                    ub_g[j] = 0.0
                b_ko, v_ko, s2, s3, src = engine.solve_lex(lb_g, ub_g, W)
                if v_ko is None:
                    v_ko = np.zeros(R)
                kV = kv_dist(v_ko, v_wt, R)
                rows.append({
                    "gene_id": gid, "gene_name": gene_names.get(gid, ""),
                    "n_gpr_rxns": len(idxs),
                    "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
                    "y_essential": 1 if b_ko < 0.05 * b_wt else 0,
                    "kV": kV if kV is not None else 0.0,
                    "L1": float(np.abs(v_ko).sum()),
                    "solve_src": src,
                })
                n_new += 1
                if n_new % 20 == 0:
                    print(f"    progress +{n_new} new ({len(rows)}/"
                          f"{len(model.genes)} total, {time.time()-t0:.0f}s)",
                          flush=True)
                    pd.DataFrame(rows).to_csv(scratch, index=False)
            cdf = pd.DataFrame(rows)
            pd.DataFrame(rows).to_csv(scratch, index=False)
            if len(cdf) < len(model.genes):
                print(f"  WARNING: incomplete ({len(cdf)}/"
                      f"{len(model.genes)}); scratch retained", flush=True)

            # ---------------- statistics (shared conventions) ----------
            ccal = transitive_calibration(cdf)
            cda, _ = direct_arm(cdf, keio_tab, st6_tab)
            _vc = {str(k): int(v) for k, v in
                   cdf["solve_src"].value_counts().to_dict().items()}

            # ------------- comparisons: deposit + stateless 2-stage ------
            gdf = pd.read_csv(os.path.join(
                DL, cfg["glpk_csv"].format(key=key)))
            hdf = pd.read_csv(os.path.join(
                DL, cfg["stateless_csv"].format(key=key)))
            m1 = cdf.merge(gdf[["gene_id", "b_ko", "y_essential", "kV"]],
                           on="gene_id", suffixes=("", "_gl"))
            kappa_glpk = float(cohen_kappa_score(m1.y_essential,
                                                 m1.y_essential_gl))
            flips = m1.loc[m1.y_essential != m1.y_essential_gl,
                           "gene_id"].tolist()
            db_g = (m1.b_ko - m1.b_ko_gl).abs()
            m2 = cdf.merge(hdf[["gene_id", "kV"]], on="gene_id",
                           suffixes=("", "_hi"))
            rho_hi = float(spearmanr(m2.kV, m2.kV_hi).statistic)

            census_lex = floor_census(cdf, b_wt)
            census_glpk = floor_census(gdf, float(gdf.b_wt.iloc[0]))
            census_hi = floor_census(hdf, float(hdf.b_wt.iloc[0]))

            comp = cdf[cdf.b_ko >= 0.999 * b_wt]
            top = comp.nlargest(8, "kV")
            top_genes = [{"gene_id": r.gene_id, "gene_name": r.gene_name,
                          "kV_lex": float(r.kV)} for r in top.itertuples()]

            out["levels"][lkey] = {
                "model": mtag, "atpm_bound": atpm,
                "wild_type_biomass": b_wt, "wt_L1": l1_wt,
                "n_genes": int(len(cdf)),
                "n_essential": int(cdf.y_essential.sum()),
                "n_essential_glpk": int(gdf.y_essential.sum()),
                "transitive_calibration": ccal,
                "direct_arm": cda,
                "solve_sources": _vc,
                "vs_glpk_deposit": {
                    "label_kappa": kappa_glpk,
                    "label_flips": flips,
                    "max_abs_db_ko": float(db_g.max()),
                    "kV_spearman_lex_vs_glpk": float(
                        spearmanr(m1.kV, m1.kV_gl).statistic),
                    "glpk_canon_r": None,   # filled below
                },
                "vs_stateless_2stage": {
                    "kV_spearman_lex_vs_stateless": rho_hi,
                    "stateless_canon_r": None,  # filled below
                },
                "floor_census_lex": census_lex,
                "floor_census_glpk": census_glpk,
                "floor_census_stateless": census_hi,
                "top8_compensable_kV_lex": top_genes,
            }
            cdf.to_csv(final_csv, index=False)
            if os.path.exists(scratch):
                os.remove(scratch)
            with open(OUT_JSON, "w") as f:
                json.dump(out, f, indent=2)
            print(f"  done: {len(cdf)} genes, "
                  f"{int(cdf.y_essential.sum())} essential (GLPK "
                  f"{int(gdf.y_essential.sum())}); solve: {_vc}", flush=True)
            print(f"  CANON(lex): r = "
                  f"{ccal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
                  f"{ccal['held_out']['roc_auc']:.4f}; MCC "
                  f"{ccal['held_out']['mcc']:.4f}", flush=True)
            print(f"  vs GLPK deposit: kappa {kappa_glpk:.4f} "
                  f"({len(flips)} flips); max|db| {db_g.max():.2e}",
                  flush=True)
            print(f"  floor census lex: {census_lex}", flush=True)
            print(f"  floor census GLPK: {census_glpk}", flush=True)
            print(f"  floor census stateless: {census_hi}", flush=True)

    # attach reference r values
    ctrl = json.load(open(os.path.join(DL, "keio_atpm_pfba_control.json")))
    iml2 = json.load(open(os.path.join(DL, "keio_atpm_iml_second_engine.json")))
    ijo2 = json.load(open(os.path.join(DL, "keio_atpm_ijo_second_engine.json")))
    for lkey, lv in out["levels"].items():
        key = key_of(lv["atpm_bound"])
        if lv["model"] == "iml":
            lv["vs_glpk_deposit"]["glpk_canon_r"] = (
                ctrl["iml_levels"][key]["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"])
            lv["vs_stateless_2stage"]["stateless_canon_r"] = (
                iml2["levels"][key]["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"])
        else:
            lv["vs_glpk_deposit"]["glpk_canon_r"] = (
                ctrl["ijo_levels"][key]["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"])
            lv["vs_stateless_2stage"]["stateless_canon_r"] = (
                ijo2["levels"][key]["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"])
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)

    print("\nSummary (declared lex rule vs deposited paths):")
    for lkey, lv in out["levels"].items():
        c = lv["transitive_calibration"]
        print(f"  {lkey}: r {c['pearson_r_log_kV_delta_b']:+.4f} "
              f"(GLPK 2-stage {lv['vs_glpk_deposit']['glpk_canon_r']:+.4f}; "
              f"stateless 2-stage "
              f"{lv['vs_stateless_2stage']['stateless_canon_r']:+.4f}); "
              f"AUC {c['held_out']['roc_auc']:.4f}; kappa-labels "
              f"{lv['vs_glpk_deposit']['label_kappa']:.4f}; floor "
              f"{lv['floor_census_lex']['n_floor_190_210']}/"
              f"{lv['floor_census_lex']['n_compensable']} (GLPK "
              f"{lv['floor_census_glpk']['n_floor_190_210']}; stateless "
              f"{lv['floor_census_stateless']['n_floor_190_210']})",
              flush=True)
    print("\nFULL LEX SWEEP DONE.")


if __name__ == "__main__":
    try:
        main()
    finally:
        _restore_nitro_fig()
