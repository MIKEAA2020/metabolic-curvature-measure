#!/usr/bin/env python3
"""Pre-registered pilot: does a deterministic lexicographic tie-break
(stage 3, fixed seeded weights -- the main engine's declared TB0
convention) make the canonical vertex ENGINE-INVARIANT at the near-tie
ATPM levels where the two-stage pFBA vertex is only weakly determined?

Background.  The engine-invariance rounds
(keio_atpm_iml_second_engine.json, keio_atpm_ijo_second_engine.json)
established: labels fully engine-invariant (kappa 1.000 at all seven
levels of both models); the kV~200 floor is the deposited GLPK
warm-start path's realization (iML 500/650/782 -> 1/1,127; iJO atpm_40
961/971 -> 1/971); the one genuine compensable rerouting at kV = 200.0
in BOTH models is lamB (b4036).  The companion (Patch I) discloses the
resulting path dependence with the measured engine bracket
[+0.475, +0.943] at the deepest iML level.

The open question this pilot answers before any promotion decision:
a stage-3 deterministic tie-break (min w^T v over the pinned
parsimony face, w = U(0.5, 1.5) fixed seed 20240901 -- the declared
convention of the locked protocol and the V8 tie-break battery)
selects a UNIQUE vertex by construction; does it select the SAME
vertex under (a) the GLPK warm-start path (persistent model,
sequential knockouts, exactly the probe's sweep pattern) and (b) the
stateless cold-start scipy/HiGHS engine?

Pilot design (both worst levels, stratified gene sample):
  - iML1515 at ATPM 100 (deposited floor 782/1,127) and iJO1366 at
    ATPM 40 (deposited floor 961/971);
  - sample: 40 deposited-GLPK-floor compensable genes (rng seed 42),
    the near-tie gene b0870 (iML), lamB b4036 (both models), the
    top-kV compensable rerouting block from each model's stateless
    CSV (the genuine forced reroutings), and 10 non-floor compensable
    controls (seed 43);
  - engines: GLPK persistent model with per-gene `with model:` KO
    blocks in probe gene order (the warm-start path; 30 s native
    simplex time limit per the probe convention) vs HiGHS stateless
    cold-start (the validated HighsCanonical class extended with the
    stage-3 split-variable LP);
  - tolerances: biomass pinned at b - 1e-9, L1 pinned at
    s2 + max(1e-9, 1e-9*|s2|) -- both at least two orders below the
    measured near-tie gap (|dL1| 8.57e-4), so the pinned faces cannot
    merge across the near-tie.

PRE-REGISTERED DECISION RULE (fixed before running; the verdict is
computed mechanically at the end and written to the JSON):
  PROMOTE if and only if all three hold:
  (P1) ENGINE-INVARIANCE OF THE LEX VERTEX: every sampled gene with
       both engines solved has inter-engine squared distance
       kV(lex_glpk, lex_highs) <= 0.1 (the fresh-cold-pair scale
       measured by atpm_warmstart_tie_test.py is ~0.02; 0.1 is the
       generous bound), AND no GLPK stage timeout on the sample;
  (P2) FLOOR COLLAPSE UNDER THE DECLARED RULE: among the sampled
       deposited-floor genes, at least 90% have lex-kV (vs the WT lex
       vertex, per engine) <= 0.1 in BOTH engines -- i.e. the floor
       is not merely one engine's realization but vanishes under the
       declared deterministic rule itself;
  (P3) LABEL PRESERVATION: every sampled gene's lex biomass matches
       the deposited canonical b_ko within 1e-6 (labels unchanged by
       construction; verified, not assumed).
  If any fails: NOT MERITED, and the companion's current disclosure
  (engine bracket, path dependence stated as the simplex path's
  realization) stands as the honest endpoint.

Artifacts:
  download/keio_atpm_lex_pilot.json
  download/keio_atpm_lex_pilot_iml_atpm_100.csv
  download/keio_atpm_lex_pilot_ijo_atpm_40.csv
Resumable: per-model scratch CSV every 10 newly processed genes.
"""
import os, sys, json, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.optimize import linprog
from cobra.io import load_json_model
from optlang.symbolics import Zero

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
DL = os.path.join(REPO, "download")

IML_MINERALS = ['EX_nh4_e', 'EX_pi_e', 'EX_so4_e', 'EX_k_e', 'EX_na1_e',
                'EX_mg2_e', 'EX_ca2_e', 'EX_cl_e', 'EX_fe2_e', 'EX_fe3_e',
                'EX_cu2_e', 'EX_mn2_e', 'EX_zn2_e', 'EX_cobalt2_e',
                'EX_mobd_e', 'EX_ni2_e', 'EX_sel_e']
IJO_MINERALS = ["EX_nh4_e", "EX_pi_e", "EX_so4_e", "EX_mg2_e", "EX_ca2_e",
                "EX_cl_e", "EX_k_e", "EX_na1_e", "EX_fe2_e", "EX_mn2_e",
                "EX_zn2_e", "EX_cobalt2_e", "EX_cu2_e", "EX_mobd_e",
                "EX_ni2_e", "EX_sel_e"]
SEED_W = 20240901          # the declared TB0 weight seed
PIN_B = 1e-9               # biomass pin slack for stage 3
PIN_L1_REL = 1e-9          # L1 pin slack (relative), floor 1e-9 abs
OUT_JSON = os.path.join(DL, "keio_atpm_lex_pilot.json")


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


def set_ijo(model, atpm_lb):
    """Exact copy of the ATPM probe's iJO medium setter (EX_zn2_e --
    the run-verified id; see atpm_ijo_second_engine.py's note)."""
    for r in model.exchanges:
        r.lower_bound = 0
    model.reactions.get_by_id("EX_glc__D_e").lower_bound = -10.0
    model.reactions.get_by_id("EX_o2_e").lower_bound = -20.0
    for ex_id in IJO_MINERALS:
        model.reactions.get_by_id(ex_id).lower_bound = -1000.0
    model.reactions.get_by_id("ATPM").lower_bound = atpm_lb


# ---------------------------------------------------------------- GLPK arm
def glpk_lex_pfba(model, W):
    """3-stage lexicographic pFBA on the persistent (warm-started) GLPK
    model -- the prototype's declared convention.  MUST be called inside
    `with model:` so that the objective/pin changes are reverted on exit
    (the same guarantee the probe's per-gene pfba calls rely on).
    Returns (v, b, s2, s3, status); v=None on failure."""
    try:
        from cobra.flux_analysis.parsimonious import add_pfba
    except ImportError:
        from cobra.flux_analysis import add_pfba
    try:
        sol1 = model.optimize()                     # stage 1: max biomass
        if sol1.status != "optimal":
            return None, 0.0, None, None, "infeasible"
        b = float(sol1.objective_value)
        add_pfba(model, fraction_of_optimum=1.0)    # stage 2 setup
        s2 = model.slim_optimize()                  # stage 2: min L1
        if s2 is None or s2 != s2:
            return None, b, None, None, "stage2_fail"
        pin = model.problem.Constraint(
            model.objective.expression, lb=None,
            ub=s2 + max(1e-9, PIN_L1_REL * abs(s2)))
        model.add_cons_vars([pin])
        model.objective = model.problem.Objective(
            Zero, direction="min", sloppy=True)
        co = {}
        for i, r in enumerate(model.reactions):
            co[r.forward_variable] = float(W[i])
            co[r.reverse_variable] = -float(W[i])
        model.objective.set_linear_coefficients(co)
        s3 = model.slim_optimize()                  # stage 3: min w^T v
        if s3 is None or s3 != s3:
            return None, b, float(s2), None, "stage3_fail"
        v = np.empty(len(model.reactions))
        for i, r in enumerate(model.reactions):
            v[i] = r.forward_variable.primal - r.reverse_variable.primal
        return v, b, float(s2), float(s3), "ok"
    except Exception as e:
        return None, 0.0, None, None, f"error:{type(e).__name__}"


# --------------------------------------------------------------- HiGHS arm
def _lp(c, A_eq, b_eq, A_ub, b_ub, bounds):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                  bounds=bounds, method="highs",
                  options={"presolve": True})
    if not res.success:
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub,
                      bounds=bounds, method="highs",
                      options={"presolve": False})
    return res


class HighsLex:
    """Stateless 3-stage lexicographic pFBA on sparse split variables."""

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
        assert self.bio_j is not None
        self.A_eq2 = sp.hstack([self.S, -self.S], format="csr")
        I = sp.identity(n, format="csr")
        blocks = [sp.hstack([I, -I], format="csr"),
                  sp.hstack([-I, I], format="csr")]
        bio_row = sp.csr_matrix(
            ([-1.0, 1.0], ([0, 0], [self.bio_j, self.bio_j + n])),
            shape=(1, 2 * n))
        self.A_ub2 = sp.vstack(blocks + [bio_row], format="csr")
        self.cost2 = np.ones(2 * n)
        self.bounds2 = np.column_stack(
            [np.zeros(2 * n), np.full(2 * n, np.inf)])
        # stage-3 extra row: sum(vp + vm) <= s2 + tol  (an A_ub row)
        self.l1_row = sp.csr_matrix(
            (np.ones(2 * n), (np.zeros(2 * n, dtype=int),
                              np.arange(2 * n))), shape=(1, 2 * n))

    def solve_lex(self, lb, ub, W):
        """Returns (b, v, s2, s3, status); v=None for infeasible."""
        bnds = np.column_stack([lb, ub])
        res1 = _lp(-self.c, self.S, np.zeros(self.m), None, None, bnds)
        if not res1.success:
            return 0.0, None, None, None, "infeasible"
        b = float(-res1.fun)
        b_ub2 = np.concatenate([ub, -lb, [-(b - PIN_B)]])
        res2 = _lp(self.cost2, self.A_eq2, np.zeros(self.m),
                   self.A_ub2, b_ub2, self.bounds2)
        if not res2.success:
            return b, None, None, None, "stage2_fail"
        s2 = float(res2.fun)
        tol_l1 = max(1e-9, PIN_L1_REL * abs(s2))
        A_ub3 = sp.vstack(
            [self.A_ub2, self.l1_row], format="csr")
        b_ub3 = np.concatenate([b_ub2, [s2 + tol_l1]])
        c3 = np.concatenate([W, -W])
        res3 = _lp(c3, self.A_eq2, np.zeros(self.m), A_ub3, b_ub3,
                   self.bounds2)
        if not res3.success:
            return b, None, s2, None, "stage3_fail"
        v = res3.x[:self.n] - res3.x[self.n:]
        return b, v, s2, float(res3.fun), "ok"


def kv_dist(v_a, v_b, n):
    """Probe convention: sum of squared diffs over |dv| > 1e-6."""
    if v_a is None or v_b is None:
        return None
    dv = np.abs(v_a - v_b)
    mask = dv > 1e-6
    return float((dv[mask] ** 2).sum()) if mask.any() else 0.0


def select_sample(model_tag, glpk_csv, highs_csv, top_csv):
    """Stratified sample: 40 floor genes (seed 42), fixed anchors,
    the stateless top-kV rerouting block, 10 controls (seed 43)."""
    gdf = pd.read_csv(glpk_csv)
    hdf = pd.read_csv(highs_csv)
    tdf = pd.read_csv(top_csv)
    b_wt = float(gdf.b_wt.iloc[0])
    gf = gdf[gdf.b_ko >= 0.999 * b_wt]
    floor = gf[(gf.kV >= 190.0) & (gf.kV <= 210.0)]
    rng = np.random.default_rng(42)
    n_floor = min(40, len(floor))
    floor_pick = (floor.sample(n=n_floor, random_state=42).gene_id
                  .tolist() if n_floor else [])
    # anchors: near-tie gene (iML), lamB, the stateless top-kV block
    anchors = []
    if "b0870" in set(gdf.gene_id):
        anchors.append("b0870")
    if "b4036" in set(gdf.gene_id):
        anchors.append("b4036")
    comp_h = hdf[hdf.b_ko >= 0.999 * b_wt]
    top_kV = comp_h.nlargest(6, "kV").gene_id.tolist()
    # controls: compensable, kV <= 0.1 under BOTH engines
    mrg = gf[["gene_id", "kV"]].merge(
        hdf[["gene_id", "kV"]], on="gene_id", suffixes=("_gl", "_hi"))
    ctrl_pool = mrg[(mrg.kV_gl <= 0.1) & (mrg.kV_hi <= 0.1)].gene_id
    ctrl = (ctrl_pool.sample(n=min(10, len(ctrl_pool)),
                             random_state=43).tolist()
            if len(ctrl_pool) else [])
    sample = []
    strata = {}
    for g in floor_pick + anchors + top_kV + ctrl:
        if g not in sample:
            sample.append(g)
    for g in floor_pick:
        strata[g] = "floor_sample"       # unbiased random floor draw
    for g in anchors:
        strata[g] = "anchor"             # deliberate genuine rerouting
    for g in top_kV:
        strata.setdefault(g, "topkV")    # stateless top-kV block
    for g in ctrl:
        strata.setdefault(g, "control")  # non-floor compensable
    meta = {"n_floor_pick": len(floor_pick),
            "anchors": [a for a in anchors],
            "stateless_top_kV_block": top_kV,
            "n_controls": len(ctrl),
            "n_total": len(sample),
            "n_floor_available": int(len(floor))}
    return sample, strata, meta


def main():
    out = {"method_note": (
        "Pre-registered lexicographic tie-break pilot: 3-stage lex pFBA "
        "(biomass max -> parsimony min -> deterministic tie-break "
        "min w^T v, w = U(0.5,1.5) fixed seed 20240901, the declared "
        "TB0 convention) solved under the GLPK warm-start path "
        "(persistent model, sequential per-gene KO blocks in probe "
        "order, 30 s simplex time limit) and the stateless cold-start "
        "scipy/HiGHS engine, at the two worst near-tie levels "
        "(iML1515 ATPM 100, iJO1366 ATPM 40) on a stratified gene "
        "sample. Decision rule P1/P2/P3 pre-registered in the script "
        "docstring; verdict computed mechanically.")}
    models = {
        "iml_atpm_100": {
            "path": "data/bigg_models/iML1515.json", "setter": set_iml,
            "atpm": 100.0,
            "glpk_csv": "keio_atpm_pfba_control_iml_atpm_100.csv",
            "highs_csv": "keio_atpm_iml_second_engine_atpm_100.csv",
            "top_csv": "keio_atpm_iml_second_engine_atpm_100.csv",
            "dep_wt": 0.079678,
        },
        "ijo_atpm_40": {
            "path": "data/bigg_models/iJO1366.json", "setter": set_ijo,
            "atpm": 40.0,
            "glpk_csv": "keio_atpm_pfba_control_atpm_40.csv",
            "highs_csv": "keio_atpm_ijo_second_engine_atpm_40.csv",
            "top_csv": "keio_atpm_ijo_second_engine_atpm_40.csv",
            "dep_wt": 0.6947359182109596,
        },
    }
    if os.path.exists(OUT_JSON):
        try:
            old = json.load(open(OUT_JSON))
            if "models" in old:
                out["models"] = old["models"]
        except Exception:
            pass
    out.setdefault("models", {})

    for tag, cfg in models.items():
        if tag in out["models"] and os.path.exists(os.path.join(
                DL, f"keio_atpm_lex_pilot_{tag}.csv")):
            print(f"{tag}: already done -- skipping", flush=True)
            continue
        print(f"\n===== {tag}: lexicographic tie-break pilot =====",
              flush=True)
        model = load_json_model(os.path.join(REPO, cfg["path"]))
        model.solver = "glpk"
        model.solver.configuration.timeout = 30  # probe convention
        cfg["setter"](model, cfg["atpm"])
        R = len(model.reactions)
        W = np.random.default_rng(SEED_W).uniform(0.5, 1.5, R)

        sample, strata, meta = select_sample(
            tag, os.path.join(DL, cfg["glpk_csv"]),
            os.path.join(DL, cfg["highs_csv"]),
            os.path.join(DL, cfg["top_csv"]))
        print(f"  sample: {meta}", flush=True)

        # ---- WT lex vertices under both engines ------------------------
        t0 = time.time()
        with model:
            v_wt_g, b_wt_g, s2_g, s3_g, st_g = glpk_lex_pfba(model, W)
        t_glpk_wt = time.time() - t0
        print(f"  WT GLPK-lex: b={b_wt_g:.6f} s2={s2_g:.4f} "
              f"({t_glpk_wt:.1f}s, {st_g})", flush=True)
        # WT determinism check (declared-rule reproducibility)
        with model:
            v_wt_g2, _, _, _, _ = glpk_lex_pfba(model, W)
        det_wt = kv_dist(v_wt_g, v_wt_g2, R)
        print(f"  WT GLPK-lex determinism: kV = {det_wt}", flush=True)

        engine = HighsLex(model)
        lb0 = np.array([r.lower_bound for r in model.reactions])
        ub0 = np.array([r.upper_bound for r in model.reactions])
        t0 = time.time()
        b_wt_h, v_wt_h, s2_h, s3_h, st_h = engine.solve_lex(lb0, ub0, W)
        t_highs_wt = time.time() - t0
        print(f"  WT HiGHS-lex: b={b_wt_h:.6f} s2={s2_h:.4f} "
              f"({t_highs_wt:.1f}s, {st_h})", flush=True)
        wt_cross = kv_dist(v_wt_g, v_wt_h, R)
        print(f"  WT inter-engine lex distance: kV = {wt_cross}",
              flush=True)

        # ---- gene loop ---------------------------------------------------
        # GLPK KO indices: proper GPR parsing (cobra), probe convention
        rid_to_i = {r.id: i for i, r in enumerate(model.reactions)}
        gene_rxns = {g.id: [rid_to_i[r.id] for r in g.reactions]
                     for g in model.genes}
        gene_names = {g.id: (g.name or "") for g in model.genes}
        dep = pd.read_csv(os.path.join(DL, cfg["glpk_csv"])
                          ).set_index("gene_id")

        scratch = os.path.join(DL, f"keio_atpm_lex_pilot_{tag}_partial.csv")
        rows, done = [], set()
        if os.path.exists(scratch):
            _p = pd.read_csv(scratch)
            rows = _p.to_dict("records")
            done = set(_p.gene_id.tolist())
            print(f"  resuming: {len(done)} genes done", flush=True)
        t0 = time.time()
        n_new = 0
        for g in model.genes:            # probe gene order (warm path)
            gid = g.id
            if gid not in sample or gid in done:
                continue
            idxs = gene_rxns.get(gid, [])
            if not idxs:
                continue
            # ---- GLPK arm: persistent model, `with model:` KO
            with model:
                for i in idxs:
                    r = model.reactions[i]
                    r.lower_bound = 0
                    r.upper_bound = 0
                tg = time.time()
                v_g, b_g, s2g, s3g, stg = glpk_lex_pfba(model, W)
                t_g = time.time() - tg
            # ---- HiGHS arm: stateless cold start
            lb_g, ub_g = lb0.copy(), ub0.copy()
            for i in idxs:
                lb_g[i] = 0.0
                ub_g[i] = 0.0
            th = time.time()
            b_h, v_h, s2h, s3h, sth = engine.solve_lex(lb_g, ub_g, W)
            t_h = time.time() - th
            rows.append({
                "gene_id": gid, "gene_name": gene_names.get(gid, ""),
                "stratum": strata.get(gid, "anchor"),
                "glpk_status": stg, "highs_status": sth,
                "b_lex_glpk": b_g, "b_lex_highs": b_h,
                "b_deposited": float(dep.loc[gid, "b_ko"])
                if gid in dep.index else np.nan,
                "kV_deposited": float(dep.loc[gid, "kV"])
                if gid in dep.index else np.nan,
                "kV_lex_glpk_vs_wt": kv_dist(v_g, v_wt_g, R),
                "kV_lex_highs_vs_wt": kv_dist(v_h, v_wt_h, R),
                "kV_lex_cross_engine": kv_dist(v_g, v_h, R),
                "t_glpk_s": t_g, "t_highs_s": t_h,
            })
            n_new += 1
            if n_new % 10 == 0:
                print(f"    progress +{n_new} new ({len(rows)}/"
                      f"{len(sample)} sampled, {time.time()-t0:.0f}s)",
                      flush=True)
                pd.DataFrame(rows).to_csv(scratch, index=False)
        cdf = pd.DataFrame(rows)
        cdf.to_csv(scratch, index=False)

        out["models"][tag] = {
            "atpm_bound": cfg["atpm"],
            "n_sample": len(sample), "sample_meta": meta,
            "wt": {"glpk_b": b_wt_g, "glpk_s2": s2_g,
                   "highs_b": b_wt_h, "highs_s2": s2_h,
                   "wt_determinism_glpk": det_wt,
                   "wt_cross_engine_kV": wt_cross,
                   "t_glpk_wt_s": t_glpk_wt, "t_highs_wt_s": t_highs_wt},
            "median_t_glpk_s": float(cdf.t_glpk_s.median()),
            "median_t_highs_s": float(cdf.t_highs_s.median()),
        }
        final_csv = os.path.join(DL, f"keio_atpm_lex_pilot_{tag}.csv")
        cdf.to_csv(final_csv, index=False)
        if os.path.exists(scratch):
            os.remove(scratch)
        with open(OUT_JSON, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  done: {len(cdf)} genes -> {final_csv}", flush=True)

    # ---------------- mechanical verdict (pre-registered) ----------------
    verdict = {"P1_engine_invariance": None, "P2_floor_collapse": None,
               "P3_label_preservation": None, "VERDICT": None}
    detail = {}
    for tag, mv in out["models"].items():
        cdf = pd.read_csv(os.path.join(DL, f"keio_atpm_lex_pilot_{tag}.csv"))
        both_ok = cdf[(cdf.glpk_status == "ok") & (cdf.highs_status == "ok")]
        n_both = len(both_ok)
        n_glpk_fail = int((cdf.glpk_status != "ok").sum())
        cross_max = (float(both_ok.kV_lex_cross_engine.max())
                     if n_both else None)
        # P2: floor collapse evaluated on the UNBIASED random floor
        # sample (stratum floor_sample); anchors/topkV are deliberate
        # genuine-rerouting genes and are reported, not scored
        fl = both_ok[(both_ok.stratum == "floor_sample")
                     & (both_ok.kV_deposited >= 190)
                     & (both_ok.kV_deposited <= 210)]
        fl_collapse = (
            (fl.kV_lex_glpk_vs_wt <= 0.1).mean()
            if len(fl) else None)
        fl_collapse_h = (
            (fl.kV_lex_highs_vs_wt <= 0.1).mean()
            if len(fl) else None)
        # P3: label preservation vs deposited canonical b_ko
        db = (both_ok.b_lex_glpk - both_ok.b_deposited).abs()
        dbh = (both_ok.b_lex_highs - both_ok.b_deposited).abs()
        detail[tag] = {
            "n_sample": int(len(cdf)), "n_both_engines_ok": n_both,
            "n_glpk_fail": n_glpk_fail,
            "cross_engine_kV_max": cross_max,
            "n_floor_sampled": int(len(fl)),
            "floor_collapse_frac_glpk": fl_collapse,
            "floor_collapse_frac_highs": fl_collapse_h,
            "max_abs_db_vs_deposited_glpk": float(db.max()),
            "max_abs_db_vs_deposited_highs": float(dbh.max()),
        }
    d1, d2 = detail.get("iml_atpm_100", {}), detail.get("ijo_atpm_40", {})
    p1 = all(v.get("cross_engine_kV_max") is not None
             and v["cross_engine_kV_max"] <= 0.1
             and v.get("n_glpk_fail", 1) == 0
             for v in (d1, d2) if v)
    p2 = all(v.get("floor_collapse_frac_glpk") is not None
             and v["floor_collapse_frac_glpk"] >= 0.9
             and v.get("floor_collapse_frac_highs") is not None
             and v["floor_collapse_frac_highs"] >= 0.9
             for v in (d1, d2) if v)
    p3 = all(v.get("max_abs_db_vs_deposited_glpk") is not None
             and v["max_abs_db_vs_deposited_glpk"] <= 1e-6
             and v.get("max_abs_db_vs_deposited_highs") is not None
             and v["max_abs_db_vs_deposited_highs"] <= 1e-6
             for v in (d1, d2) if v)
    verdict.update({"P1_engine_invariance": bool(p1),
                    "P2_floor_collapse": bool(p2),
                    "P3_label_preservation": bool(p3),
                    "VERDICT": "PROMOTE" if (p1 and p2 and p3)
                    else "NOT_MERITED"})
    out["verdict"] = verdict
    out["verdict_detail"] = detail
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)

    print("\n===== PRE-REGISTERED VERDICT =====")
    for tag, d in detail.items():
        print(f"  {tag}: {json.dumps(d, default=str)}")
    print(f"  P1 (engine-invariance): {verdict['P1_engine_invariance']}")
    print(f"  P2 (floor collapse):    {verdict['P2_floor_collapse']}")
    print(f"  P3 (label preservation): {verdict['P3_label_preservation']}")
    print(f"  VERDICT: {verdict['VERDICT']}")
    print("LEX TIE-BREAK PILOT DONE.")


if __name__ == "__main__":
    main()
