#!/usr/bin/env python3
"""Second-engine re-run of the iML1515 ATPM levels (60/80/100): full
canonical (two-stage split-variable pFBA) KO sweep under
scipy.optimize.linprog(method='highs'), to test whether the near-tie
floor recorded by the GLPK probe (782/1,129 compensable knockouts at
kV ~ 200.01 at ATPM >= 100; canonical r +0.703/+0.655/+0.475) is
engine-invariant or a GLPK simplex-path artifact.

Background (keio_atpm_neartie_measurement.json,
atpm_warmstart_tie_test.py): the iML1515 parsimony stage at elevated
ATPM carries near-tied optima (|dL1| 8.57e-4 absolute / 1.15e-6
relative); the probe's WT reference solve and its warm-started per-KO
solves land on different near-tied vertices (squared distance ~200),
while fresh cold pairs land on the same vertex (sq ~ 0.02).  A
stateless cold-start engine therefore discriminates the genuinely
KO-forced vertex switches (floor persists) from path artifacts (floor
collapses to ~0).

Design (engine substitution, not regularization):
  - model state identical to scripts/atpm_stress_keio_probe.py
    (set_iml_atpm medium; knockout = zero bounds of every reaction
    whose gene_reaction_rule contains the gene id; all 1,516 genes
    processed, zero-GPR genes included);
  - canonical solve = the repo's independent-engine rule
    (atpm_integrity_fix.highs_pfba): stage 1 max biomass; stage 2
    min sum(vp+vm) with v = vp - vm, full reaction bounds
    lb <= v <= ub, biomass >= stage-1 optimum.  Sparse matrices
    (the fix script's dense [I,-I] blocks would be ~1.9 GB per call);
  - WT reference = the engine's own fresh canonical solve per level
    (biomass checked against the deposited level WT);
  - kV = sum (v_ko - v_wt)^2 over |dv| > 1e-6 (probe convention);
    labels at 5% of the level's own WT; per-gene solve_src column;
  - statistics = the shared probe functions (transitive_calibration,
    direct_arm, seeds unchanged) so every number is same-convention;
  - floor census recomputed with one census function applied to BOTH
    the deposited GLPK CSV and the HiGHS CSV (compensable =
    b_ko >= 0.999 * b_wt), validating the census definition against
    the recorded 782/1,129/200.01 before reading the HiGHS answer;
  - L1 near-tie block: WT L1, b0870 KO L1, and the |dL1| distribution
    over compensable genes.

Artifacts:
  download/keio_atpm_iml_second_engine.json
  download/keio_atpm_iml_second_engine_{key}.csv
Resumable: per-level scratch CSV every 20 newly processed genes.
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.optimize import linprog
from scipy.stats import spearmanr
from sklearn.metrics import cohen_kappa_score
from cobra.io import load_json_model

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
DL = os.path.join(REPO, "download")

from nitrogen_source_keio_probe import (keio_tables, transitive_calibration,
                                        direct_arm)

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
LEVELS = [60.0, 80.0, 100.0]
OUT_JSON = os.path.join(DL, "keio_atpm_iml_second_engine.json")

DEPOSITED_WT = {60.0: 0.39839, 80.0: 0.239034, 100.0: 0.079678}
NEARTIE_GENE = "b0870"
GLPK_NEARTIE = {"wt_pFBA_L1": 747.6826046580629,
                "ko_b0870_pFBA_L1": 747.6817474281629}


def key_of(lb):
    return f"atpm_{lb:g}"


def set_iml(model, atpm_lb):
    """Exact copy of the ATPM probe's iML medium setter."""
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


def _lp(c, A_eq, b_eq, A_ub, b_ub, bounds):
    """linprog(method='highs') with the deterministic presolve-off retry
    (lp_engine convention: only activates when the first call fails)."""
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                  bounds=bounds, method="highs",
                  options={"presolve": True})
    if not res.success:
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                      bounds=bounds, method="highs",
                      options={"presolve": False})
    return res


class HighsCanonical:
    """Two-stage split-variable pFBA on sparse matrices, stateless."""

    def __init__(self, model):
        self.rids = [r.id for r in model.reactions]
        self.n = n = len(self.rids)
        m = len(model.metabolites)
        midx = {met.id: i for i, met in enumerate(model.metabolites)}
        S = np.zeros((m, n))
        for j, r in enumerate(model.reactions):
            for met, coef in r.metabolites.items():
                S[midx[met.id], j] = coef
        self.m = m
        self.S = sp.csr_matrix(S)
        self.lb0 = np.array([r.lower_bound for r in model.reactions])
        self.ub0 = np.array([r.upper_bound for r in model.reactions])
        self.c = np.zeros(n)
        self.bio_j = None
        for j, r in enumerate(model.reactions):
            if r.objective_coefficient != 0:
                self.c[j] = r.objective_coefficient
                if (self.bio_j is None and ("BIOMASS" in r.id.upper()
                                            or "iomass" in r.id)):
                    self.bio_j = j
        assert self.bio_j is not None, "biomass objective not found"
        # stage-2 fixed structures: v = vp - vm
        self.A_eq2 = sp.hstack([self.S, -self.S], format="csr")
        I = sp.identity(n, format="csr")
        blocks = [sp.hstack([I, -I], format="csr"),
                  sp.hstack([-I, I], format="csr")]
        # biomass >= b:  -(vp_bio - vm_bio) <= -b   (fix-script signs)
        bio_row = sp.csr_matrix(
            ([-1.0, 1.0], ([0, 0], [self.bio_j, self.bio_j + n])),
            shape=(1, 2 * n))
        self.A_ub2 = sp.vstack(blocks + [bio_row], format="csr")
        self.cost2 = np.ones(2 * n)
        self.bounds2 = np.column_stack(
            [np.zeros(2 * n), np.full(2 * n, np.inf)])

    def solve(self, lb, ub):
        """Returns (b, v, solve_src); b=0.0/v=None for infeasible."""
        bnds = np.column_stack([lb, ub])
        res1 = _lp(-self.c, self.S, np.zeros(self.m), None, None, bnds)
        if not res1.success:
            return 0.0, None, "infeasible"
        b = float(-res1.fun)
        b_ub = np.concatenate([ub, -lb, [-b]])
        res2 = _lp(self.cost2, self.A_eq2, np.zeros(self.m),
                   self.A_ub2, b_ub, self.bounds2)
        if res2.success:
            v = res2.x[:self.n] - res2.x[self.n:]
            return b, v, "highs_pfba"
        # label-preserving fallback: plain stage-1 optimum vertex
        return b, res1.x.copy(), "highs_plain_fallback"


def floor_census(df, b_wt):
    """Compensable = b_ko >= 0.999 * b_wt (atpm_r_decomposition
    convention); floor band kV in [190, 210]."""
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


def main():
    out = {"method_note": (
        "Full iML1515 ATPM-level canonical re-run under the independent "
        "scipy/HiGHS engine (two-stage split-variable pFBA, cold-start "
        "stateless solves, full reaction bounds; the atpm_integrity_fix "
        "convention on sparse matrices). Medium, knockout convention, "
        "kV definition, label rule, and statistics functions identical "
        "to the GLPK probe (atpm_stress_keio_probe.py); WT reference = "
        "the engine's own fresh canonical solve per level.")}
    if os.path.exists(OUT_JSON):
        try:
            old = json.load(open(OUT_JSON))
            if "levels" in old:
                out["levels"] = old["levels"]
        except Exception:
            pass
    out.setdefault("levels", {})

    iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
    engine = HighsCanonical(iml)
    rids = engine.rids
    n = engine.n
    gene_names = {g.id: (g.name or "") for g in iml.genes}
    # gene -> KO reaction indices, the probe's substring convention
    t0 = time.time()
    rules = [r.gene_reaction_rule for r in iml.reactions]
    gene_rxn_idx = {}
    for g in iml.genes:
        gene_rxn_idx[g.id] = [j for j in range(n)
                              if g.id in rules[j]]
    print(f"gene->reaction map built ({time.time()-t0:.0f}s, "
          f"{len(gene_rxn_idx)} genes)", flush=True)

    keio_tab, st6_tab = keio_tables()

    for atpm in LEVELS:
        key = key_of(atpm)
        final_csv = os.path.join(DL, f"keio_atpm_iml_second_engine_{key}.csv")
        if key in out["levels"] and os.path.exists(final_csv):
            print(f"{key}: already done -- skipping", flush=True)
            continue
        print(f"\n----- iML1515 ATPM >= {atpm} (HiGHS canonical) -----",
              flush=True)
        set_iml(iml, atpm)
        lb0 = np.array([r.lower_bound for r in iml.reactions])
        ub0 = np.array([r.upper_bound for r in iml.reactions])

        b_wt, v_wt, src_wt = engine.solve(lb0, ub0)
        assert src_wt == "highs_pfba", src_wt
        dep = DEPOSITED_WT[atpm]
        print(f"  WT canonical: b = {b_wt:.6f} (deposited {dep}; "
              f"|diff| {abs(b_wt-dep):.2e}); L1 = "
              f"{float(np.abs(v_wt).sum()):.6f}", flush=True)
        assert abs(b_wt - dep) < 1e-6, (b_wt, dep)
        l1_wt = float(np.abs(v_wt).sum())

        scratch = os.path.join(
            DL, f"keio_atpm_iml_second_engine_{key}_partial.csv")
        rows, done = [], set()
        if os.path.exists(scratch):
            _part = pd.read_csv(scratch)
            rows = _part.to_dict("records")
            done = set(_part["gene_id"].tolist())
            print(f"    resuming: {len(done)} genes already done",
                  flush=True)
        t0 = time.time()
        n_new = 0
        for g in iml.genes:
            gid = g.id
            if gid in done:
                continue
            idxs = gene_rxn_idx[gid]
            lb_g, ub_g = lb0.copy(), ub0.copy()
            for j in idxs:
                lb_g[j] = 0.0
                ub_g[j] = 0.0
            b_ko, v_ko, src = engine.solve(lb_g, ub_g)
            if v_ko is None:
                v_ko = np.zeros(n)
            dv = np.abs(v_ko - v_wt)
            mask = dv > 1e-6
            kV = float((dv[mask] ** 2).sum()) if mask.any() else 0.0
            rows.append({
                "gene_id": gid, "gene_name": gene_names.get(gid, ""),
                "n_gpr_rxns": len(idxs), "n_changed": int(mask.sum()),
                "b_wt": b_wt, "b_ko": b_ko, "delta_b": b_wt - b_ko,
                "y_essential": 1 if b_ko < 0.05 * b_wt else 0,
                "kV": kV, "L1": float(np.abs(v_ko).sum()),
                "solve_src": src,
            })
            n_new += 1
            if n_new % 20 == 0:
                print(f"    progress +{n_new} new ({len(rows)}/"
                      f"{len(iml.genes)} total, {time.time()-t0:.0f}s)",
                      flush=True)
                if rows:
                    pd.DataFrame(rows).to_csv(scratch, index=False)
        cdf = pd.DataFrame(rows)
        if rows:
            pd.DataFrame(rows).to_csv(scratch, index=False)

        # ---------------- statistics (shared conventions) --------------
        ccal = transitive_calibration(cdf)
        cda, _ = direct_arm(cdf, keio_tab, st6_tab)
        _vc = {str(k): int(v) for k, v in
               cdf["solve_src"].value_counts().to_dict().items()}

        # ---------------- comparison vs the GLPK deposit ---------------
        glpk_csv = os.path.join(DL, f"keio_atpm_pfba_control_iml_{key}.csv")
        gdf = pd.read_csv(glpk_csv)
        m = cdf.merge(gdf[["gene_id", "b_ko", "y_essential", "kV"]],
                      on="gene_id", suffixes=("_hi", "_gl"))
        kappa_lab = float(cohen_kappa_score(m.y_essential_hi, m.y_essential_gl))
        flips = m.loc[m.y_essential_hi != m.y_essential_gl,
                      "gene_id"].tolist()
        db = (m.b_ko_hi - m.b_ko_gl).abs()
        rho_kv = float(spearmanr(m.kV_hi, m.kV_gl).statistic)

        census_hi = floor_census(cdf, b_wt)
        census_gl = floor_census(gdf, float(gdf.b_wt.iloc[0]))

        # ---------------- L1 near-tie block -----------------------------
        l1_block = {"wt_L1": l1_wt}
        near_row = cdf[cdf.gene_id == NEARTIE_GENE]
        if len(near_row):
            l1ko = float(near_row.L1.iloc[0])
            l1_block.update({
                f"ko_{NEARTIE_GENE}_L1": l1ko,
                "dL1_absolute": l1ko - l1_wt,
                "dL1_relative": (l1ko - l1_wt) / l1_wt,
                "glpk_reference_dL1_absolute": (
                    GLPK_NEARTIE["ko_b0870_pFBA_L1"]
                    - GLPK_NEARTIE["wt_pFBA_L1"]),
            })
        comp = cdf[cdf.b_ko >= 0.999 * b_wt]
        dl1 = (comp.L1 - l1_wt).abs()
        l1_block.update({
            "compensable_dL1_median": float(dl1.median()),
            "compensable_dL1_max": float(dl1.max()),
            "n_compensable_dL1_lt_1e-3": int((dl1 < 1e-3).sum()),
        })

        out["levels"][key] = {
            "atpm_bound": atpm,
            "wild_type_biomass": b_wt,
            "n_genes": int(len(cdf)),
            "n_essential": int(cdf.y_essential.sum()),
            "n_essential_glpk": int(gdf.y_essential.sum()),
            "transitive_calibration": ccal,
            "direct_arm": cda,
            "solve_sources": _vc,
            "vs_glpk": {
                "label_kappa": kappa_lab,
                "label_flips": flips,
                "max_abs_db_ko": float(db.max()),
                "n_abs_db_ko_gt_1e-6": int((db > 1e-6).sum()),
                "kV_spearman_hi_vs_gl": rho_kv,
                "glpk_canon_r": None,  # filled below
            },
            "floor_census_highs": census_hi,
            "floor_census_glpk": census_gl,
            "L1_neartie": l1_block,
        }
        cdf.to_csv(final_csv, index=False)
        if os.path.exists(scratch):
            os.remove(scratch)
        with open(OUT_JSON, "w") as f:
            json.dump(out, f, indent=2)

        print(f"  done ({time.time()-t0:.0f}s): {len(cdf)} genes, "
              f"{int(cdf.y_essential.sum())} essential (GLPK "
              f"{int(gdf.y_essential.sum())}); solve: {_vc}", flush=True)
        print(f"  CANON(HiGHS): r = "
              f"{ccal['pearson_r_log_kV_delta_b']:+.4f}; AUC "
              f"{ccal['held_out']['roc_auc']:.4f}; MCC "
              f"{ccal['held_out']['mcc']:.4f}", flush=True)
        print(f"  vs GLPK: label kappa {kappa_lab:.4f} "
              f"({len(flips)} flips); max|db| {db.max():.2e}; "
              f"kV rho {rho_kv:+.4f}", flush=True)
        print(f"  floor census HiGHS: {census_hi}", flush=True)
        print(f"  floor census GLPK: {census_gl}", flush=True)

    # attach the deposited GLPK canonical r values for convenience
    ctrl = json.load(open(os.path.join(DL, "keio_atpm_pfba_control.json")))
    for atpm in LEVELS:
        key = key_of(atpm)
        if key in out["levels"]:
            out["levels"][key]["vs_glpk"]["glpk_canon_r"] = (
                ctrl["iml_levels"][key]["transitive_calibration"]
                ["pearson_r_log_kV_delta_b"])
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)

    print("\nSummary (HiGHS vs GLPK, canonical arm):")
    for atpm in LEVELS:
        key = key_of(atpm)
        if key not in out["levels"]:
            continue
        lv = out["levels"][key]
        c = lv["transitive_calibration"]
        g = lv["vs_glpk"]
        print(f"  iML ATPM >= {atpm}: r {c['pearson_r_log_kV_delta_b']:+.4f} "
              f"(GLPK {g['glpk_canon_r']:+.4f}); AUC "
              f"{c['held_out']['roc_auc']:.4f}; kappa-labels "
              f"{g['label_kappa']:.4f}; floor "
              f"{lv['floor_census_highs']['n_floor_190_210']}/"
              f"{lv['floor_census_highs']['n_compensable']} (GLPK "
              f"{lv['floor_census_glpk']['n_floor_190_210']}/"
              f"{lv['floor_census_glpk']['n_compensable']})", flush=True)
    print("\nSECOND-ENGINE ATPM RE-RUN DONE.")


if __name__ == "__main__":
    main()
