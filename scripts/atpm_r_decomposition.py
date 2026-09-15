#!/usr/bin/env python3
"""Decomposition of the canonical transitive-calibration r on the ATPM
axis: why does iJO1366 restore to +0.94 at ATPM=100 while iML1515 only
reaches +0.48 (AUC 0.98)?

Hypotheses:
  H1  infeasible-flag genes (b_ko = 0, kV = |v_wt|^2 huge) anchor the
      top end and are fine in both models -> not the cause.
  H2  silent-compensation genes (b_ko = b_wt exactly, kV > 0) add
      low-delta / high-log-kV noise; if they are more numerous or
      heavier-tailed in iML, they depress r.
  H3  the relationship is piecewise (two regimes: near-linear for
      partial-defect genes, flat for compensable genes) and the mix
      differs between models.

This script computes the correlation overall and on informative
subsets, plus spread statistics, from the level CSVs.
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "download")


def subset_stats(df, label):
    d = df[(df.b_ko >= 0) & (df.b_wt > 0)].copy()
    d["log_kV"] = np.log10(d.kV.clip(lower=1e-12))
    d = d[(d.delta_b >= 0)]
    n = len(d)
    if n < 10:
        print(f"  {label:34s} n={n:5d} (too few)")
        return
    r = pearsonr(d.log_kV, d.delta_b).statistic
    rho = spearmanr(d.log_kV, d.delta_b).statistic
    print(f"  {label:34s} n={n:5d}  r={r:+.4f}  rho={rho:+.4f}")


for model, key, wt in [("iJO", "atpm_100", None), ("iML", "atpm_100", None),
                       ("iML", "atpm_60", None), ("iJO", "atpm_60", None)]:
    fn = (f"keio_atpm_pfba_control_{key}.csv" if model == "iJO"
          else f"keio_atpm_pfba_control_iml_{key}.csv")
    df = pd.read_csv(os.path.join(OUT, fn))
    b_wt = df.b_wt.iloc[0]
    print(f"\n=== {model} {key} (n={len(df)}, WT={b_wt:.4f}, "
          f"n_ess={int((df.y_essential == 1).sum())}) ===")
    subset_stats(df, "all (b_ko>=0)")
    subset_stats(df[df.b_ko > 0], "viable only (b_ko>0)")
    subset_stats(df[(df.b_ko > 0) & (df.b_ko < 0.999 * b_wt)],
                "partial-defect (0<b_ko<WT)")
    subset_stats(df[df.b_ko >= 0.999 * b_wt], "compensable (b_ko~WT)")
    comp = df[df.b_ko >= 0.999 * b_wt]
    if len(comp):
        print(f"    compensable kV: median {comp.kV.median():.1f}, "
              f"p90 {comp.kV.quantile(0.9):.1f}, "
              f"p99 {comp.kV.quantile(0.99):.1f}, max {comp.kV.max():.1f}")
        print(f"    compensable with kV > 10x median: "
              f"{int((comp.kV > 10*comp.kV.median()).sum())} genes")
    pd_ = df[(df.b_ko > 0) & (df.b_ko < 0.999 * b_wt)]
    if len(pd_):
        print(f"    partial-defect kV: median {pd_.kV.median():.1f}, "
              f"p90 {pd_.kV.quantile(0.9):.1f}, max {pd_.kV.max():.1f}")
        print(f"    partial-defect b_ko spread: "
              f"{pd_.b_ko.min():.5f}..{pd_.b_ko.max():.5f}")
print("\nDONE")
