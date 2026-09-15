#!/usr/bin/env python3
"""Publication figure for the six-axis round: 4 panels.

(a) plain-FBA transitive r across all 31 probe levels, ordered by
    axis and wild-type reduction -- the deep-limitation collapse
    (and the ATPM/iJO moderate-stress strength)
(b) canonical (pFBA) r across the same levels -- the restoration,
    with the iML1515/ATPM near-tie corner marked
(c) at-optimum PGI FVA width per level -- the degeneracy signature
    (supply axes 45-202, the non-medium ATPM axis 0.0)
(d) iML1515 ATPM=100 compensable-kV histogram (log10) -- the
    near-tie floor at ~200.01 vs the ~0 cluster

Reads only committed artifacts; writes
download/keio_multiaxis_canonical_response.png
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
for _fp in ['/usr/share/fonts/truetype/chinese/NotoSansSC[wght].ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
    try:
        fm.fontManager.addfont(_fp)
    except Exception:
        pass
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Noto Sans SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = os.path.join(REPO, "download")

mtab = json.load(open(os.path.join(DL,
                                   "multiaxis_canonical_table.json")))
rows = mtab["rows"]
can100 = pd.read_csv(os.path.join(
    DL, "keio_atpm_pfba_control_iml_atpm_100.csv"))

AXIS_ORDER = ["nitrogen", "oxygen", "phosphate", "iron",
              "ATPM (non-medium)"]
AXIS_LABEL = {"nitrogen": "N supply/subst.",
              "oxygen": "O$_2$ limit",
              "phosphate": "P supply",
              "iron": "Fe supply",
              "ATPM (non-medium)": "ATPM stress\n(non-medium)"}
MODEL_STYLE = {"iJO1366": dict(marker="o", ms=6),
               "iML1515": dict(marker="s", ms=5)}
COLORS = {"nitrogen": "#4053d3", "oxygen": "#ddb310",
          "phosphate": "#b51d14", "iron": "#00beff",
          "ATPM (non-medium)": "#fb49b0"}

# ordered layout: axis blocks, within block by wt_red
ordered = []
for ax in AXIS_ORDER:
    for model in ["iJO1366", "iML1515"]:
        sub = sorted([r for r in rows
                      if r["axis"] == ax and r["model"] == model],
                     key=lambda r: r["wt_red"])
        ordered += [(ax, model, r) for r in sub]
n = len(ordered)
xs = np.arange(n)

fig, axes = plt.subplots(2, 2, figsize=(12.5, 8.6),
                         constrained_layout=True)

# ---- (a) plain r ----
ax = axes[0, 0]
for axname in AXIS_ORDER:
    for model, st in MODEL_STYLE.items():
        pts = [(i, r) for i, (a, m, r) in enumerate(ordered)
               if a == axname and m == model]
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1]["plain_r"] for p in pts],
                linestyle="none", color=COLORS[axname],
                label=f"{AXIS_LABEL[axname].split(chr(10))[0]} ({model[:3]})",
                **st, mec="k", mew=0.4, alpha=0.9)
ax.axhline(0, color="gray", lw=0.6, zorder=0)
ax.axhline(0.6034, color="k", lw=0.8, ls="--", zorder=0)
ax.text(n - 0.5, 0.63, "iJO baseline plain r = +0.603", ha="right",
        fontsize=7.5, color="k")
ax.set_ylabel("plain-FBA transitive r", fontsize=9)
ax.set_title("(a) plain arm: deep-limitation collapse", fontsize=10)
ax.set_ylim(-0.35, 1.05)

# ---- (b) canonical r ----
ax = axes[0, 1]
for axname in AXIS_ORDER:
    for model, st in MODEL_STYLE.items():
        pts = [(i, r) for i, (a, m, r) in enumerate(ordered)
               if a == axname and m == model]
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1]["canon_r"] for p in pts],
                linestyle="none", color=COLORS[axname],
                label=f"{AXIS_LABEL[axname].split(chr(10))[0]} ({model[:3]})",
                **st, mec="k", mew=0.4, alpha=0.9)
ax.axhline(0.9452, color="k", lw=0.8, ls="--", zorder=0)
ax.text(n - 0.5, 0.955, "iJO baseline canonical r = +0.945",
        ha="right", fontsize=7.5, color="k")
i_ml_atpm100 = [i for i, (a, m, r) in enumerate(ordered)
                if a == "ATPM (non-medium)" and m == "iML1515"
                and r["level"] == "atpm_100"][0]
ax.annotate("near-tie corner\n(iML, ATPM 100)", xy=(i_ml_atpm100, 0.4756),
            xytext=(i_ml_atpm100 - 6.5, 0.62), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_ylabel("canonical (pFBA) transitive r", fontsize=9)
ax.set_title("(b) canonical arm: restoration + the near-tie corner",
             fontsize=10)
ax.set_ylim(0.30, 1.03)
ax.legend(fontsize=6.2, ncol=2, loc="lower left", framealpha=0.9)

# ---- (c) PGI width ----
ax = axes[1, 0]
for axname in AXIS_ORDER:
    for model, st in MODEL_STYLE.items():
        pts = [(i, r) for i, (a, m, r) in enumerate(ordered)
               if a == axname and m == model
               and r.get("pgi_width") is not None]
        if not pts:
            continue
        ax.plot([p[0] for p in pts], [p[1]["pgi_width"] for p in pts],
                linestyle="none", color=COLORS[axname],
                label=f"{AXIS_LABEL[axname].split(chr(10))[0]} ({model[:3]})",
                **st, mec="k", mew=0.4, alpha=0.9)
ax.set_ylabel("at-optimum PGI FVA width", fontsize=9)
ax.set_title("(c) degeneracy signature: supply axes wide, "
             "ATPM axis 0.0", fontsize=10)

# ---- (d) near-tie floor ----
ax = axes[1, 1]
comp = can100[can100.b_ko >= 0.999 * can100.b_wt]
lkv = np.log10(comp.kV.clip(lower=1e-4))
ax.hist(lkv, bins=48, color="#7a0177", alpha=0.85, edgecolor="w",
        linewidth=0.3)
ax.axvline(np.log10(200.01), color="#fb49b0", lw=1.4, ls="--")
ax.text(np.log10(200.01) + 0.05, ax.get_ylim()[1] * 0.92,
        "near-tie floor\nkV $\\approx$ 200.01\n(782 / 1129 genes)",
        fontsize=8, color="#fb49b0")
ax.set_xlabel("log$_{10}$ kV (compensable knockouts, iML1515 ATPM 100)",
              fontsize=9)
ax.set_ylabel("genes", fontsize=9)
ax.set_title("(d) the L1 near-tie: bimodal compensable kV", fontsize=10)

# shared x cosmetics on the top row
for ax in [axes[0, 0], axes[0, 1]]:
    ax.set_xlim(-1, n)
    ax.set_xticks([])
for ax in [axes[1, 0]]:
    ax.set_xlim(-1, n)
    ticks = []
    labels = []
    pos = 0
    for axname in AXIS_ORDER:
        block = [(i, a, m) for i, (a, m, r) in enumerate(ordered)
                 if a == axname]
        if block:
            c = np.mean([b[0] for b in block])
            ticks.append(c)
            labels.append(AXIS_LABEL[axname])
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=7.5)
axes[1, 1].set_xlim(-4.2, 3.2)

fig.suptitle("Six perturbation axes, 31 levels, two reconstructions: "
             "labels invariant; the association is the invariant object "
             "under canonical flux selection",
             fontsize=11.5, y=0.995)
out = os.path.join(DL, "keio_multiaxis_canonical_response.png")
fig.savefig(out, dpi=200)
print("written", out)
