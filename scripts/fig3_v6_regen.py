#!/usr/bin/env python3
"""
Regenerate the primary-association figure (v5_e24_recalibration.png)
from the DEPOSITED artifacts only (CSV + JSON), with two fixes:

  1. Layout: explicit y-headroom in the bar panel so the per-bar
     annotations (r and n) no longer collide with the panel title
     (the collision reported for the middle panel).
  2. Terminology: internal experiment codes removed from the figure
     (no suptitle; x-tick labels and axis labels use the manuscript's
     terminology: geometric kappa_V (plain FBA), kappa_V^lex (engine
     control), kappa^mu (measure)).

Data source: download/deepseek_bridge/v5_e24_recalibration.csv and
.json (deposited by e24_measure_kappa.py); the response variable is
read from the deposited E24 panel CSV.  All plotted values are taken
verbatim from the deposited artifacts; nothing is recomputed except
the panel-(a) least-squares line through the deposited points.
Outputs (same content, both manuscript-facing locations):
  download/association_robustness/v5_e24_recalibration.png
  download/deepseek_bridge/v5_e24_recalibration.png
"""
import json
import os

import numpy as np
import pandas as pd

BASE = "/home/z/my-project/metabolic-curvature-measure"
DL = os.path.join(BASE, "download")
SRC = os.path.join(DL, "deepseek_bridge")

df8 = pd.read_csv(os.path.join(SRC, "v5_e24_recalibration.csv")).set_index(
    "gene_bnumber")
with open(os.path.join(SRC, "v5_e24_recalibration.json")) as f:
    js = json.load(f)
arms = js["arms"]

e24 = pd.read_csv(os.path.join(DL, "novelty_v17_option_a_e24.csv")).set_index(
    "gene_bnumber")
stat_cols = ["fc_m3d_stationary_135min", "fc_m3d_stationary_330min",
             "fc_m3d_stationary_480min", "fc_m3d_stationary_720min"]
max_fc = e24[stat_cols].abs().max(axis=1)

x_mu = np.log10(df8["kappa_mu_max"]).values
y = max_fc.values
kv_e22 = df8["kappa_V_E22"].astype(float).values
m = df8["kappa_mu_max"].values > 0

names = ["kappa_V_E22 (baseline)", "kappa_V_lex (engine ctrl)",
         "kappa_mu max (4x)"]
rs = [arms[n]["nonzero"]["pearson_r"] for n in names]
ns = [arms[n]["n_nonzero"] for n in names]
rho = arms["predictor_agreement"]["spearman_kappamu_vs_kappaVE22"][0]

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for fp in ("/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.1),
                         constrained_layout=True)

ax = axes[0]
ax.scatter(x_mu[m], y[m], s=9, alpha=0.45, color="#1f4e79",
           edgecolors="none")
if m.sum() > 5:
    b1, b0 = np.polyfit(x_mu[m], y[m], 1)
    xx = np.linspace(x_mu[m].min(), x_mu[m].max(), 50)
    ax.plot(xx, b0 + b1 * xx, "-", color="#c00000", lw=1.8)
    ax.text(0.04, 0.95,
            f"r = {arms['kappa_mu max (4x)']['nonzero']['pearson_r']:+.3f}"
            f"  (n = {int(m.sum())})",
            transform=ax.transAxes, va="top", fontsize=9)
ax.set_xlabel(r"$\log_{10}\,\kappa^\mu$ (measure mass, per-gene max)")
ax.set_ylabel(r"max $|\log_2\mathrm{FC}|$ (M3D carbon exhaustion)")
ax.set_title("(a) measure-theoretic predictor")

ax = axes[1]
bars = ax.bar(range(3), rs, color=["#7f7f7f", "#548235", "#1f4e79"])
for i, (r_, n_) in enumerate(zip(rs, ns)):
    ax.text(i, r_ + 0.012, f"{r_:+.3f}\n(n={n_})", ha="center",
            fontsize=8.5)
ax.set_xticks(range(3))
ax.set_xticklabels(["geometric $\\kappa_V$\n(plain FBA)",
                    "$\\kappa_V^{\\mathrm{lex}}$\n(engine control)",
                    "$\\kappa^\\mu$\n(measure)"],
                   fontsize=9)
ax.set_ylabel("Pearson r (nonzero panel)")
ax.set_title("(b) metric comparison")
ax.axhline(0, color="k", lw=0.6)
# headroom so the two-line annotations stay inside the axes
ax.set_ylim(-0.06, max(rs) + 0.14)

ax = axes[2]
ax.scatter(np.log10(kv_e22)[m], x_mu[m], s=9, alpha=0.45,
           color="#595959", edgecolors="none")
ax.set_xlabel(r"$\log_{10}\,\kappa_V$ (geometric, plain FBA)")
ax.set_ylabel(r"$\log_{10}\,\kappa^\mu$")
ax.set_title(f"(c) predictor agreement "
             f"rho = {rho:+.2f}")

out_pngs = [os.path.join(DL, "association_robustness",
                         "v5_e24_recalibration.png"),
            os.path.join(SRC, "v5_e24_recalibration.png")]
for p in out_pngs:
    fig.savefig(p, dpi=170)
    print("[fig3-regen] wrote", p)
plt.close(fig)
print("[fig3-regen] bars:", rs, "ns:", ns, "rho:", round(rho, 4))
