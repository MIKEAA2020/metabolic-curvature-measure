#!/usr/bin/env python3
"""Publication figure for the phosphate-axis probe: 4 panels, matching
the nitrogen-axis figure layout.

(a) label flips vs glucose-only baseline per level (all zero on this
    axis -- the supply-side closure)
(b) wild-type growth along the axis (47% -> 89% reduction)
(c) plain-FBA association statistics (the degeneracy collapse,
    tracking the at-optimum FVA width)
(d) canonical (pFBA) association statistics (restored at every level)

Reads only committed artifacts; writes
download/keio_phosphate_limited_response.png.
"""
import os, json
import numpy as np
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

ijo_res = json.load(open(os.path.join(
    DL, "keio_phosphate_limited_e12_results.json")))
iml_res = json.load(open(os.path.join(
    DL, "keio_phosphate_limited_e16_results.json")))
ctrl = json.load(open(os.path.join(DL, "keio_phosphate_pfba_control.json")))
nctrl = json.load(open(os.path.join(DL, "keio_nitrogen_pfba_control.json")))
base_ijo = json.load(open(os.path.join(
    DL, "keio_glucose_only_e12_results.json")))

IJO_KEYS = ["pi_0.5", "pi_0.25", "pi_0.1"]
IML_KEYS = ["pi_0.25", "pi_0.1"]
x_labels = ["baseline\n(Pi unlim.)", "Pi $-0.5$", "Pi $-0.25$",
            "Pi $-0.1$"]
xs = np.arange(len(x_labels))

gains = [0] + [ijo_res["levels"][k]["flips_vs_glucose_only"]["n_gain_essential"]
               for k in IJO_KEYS]
losses = [0] + [ijo_res["levels"][k]["flips_vs_glucose_only"]["n_loss_essential"]
                for k in IJO_KEYS]
wts = [base_ijo['wild_type_biomass']] + \
      [ijo_res["levels"][k]["wild_type_biomass"] for k in IJO_KEYS]
pgiw = [0.0] + [ijo_res["levels"][k]["degeneracy"]["fva_widths"]["PGI"]
                for k in IJO_KEYS]
pears = [base_ijo['calibration']['pearson_r_log_kV_delta_b']] + \
        [ijo_res["levels"][k]["transitive_calibration"]
         ["pearson_r_log_kV_delta_b"] for k in IJO_KEYS]
aucs = [base_ijo['held_out_essentiality_prediction']['roc_auc']] + \
       [ijo_res["levels"][k]["transitive_calibration"]["held_out"]["roc_auc"]
        for k in IJO_KEYS]

c_pears = [nctrl["levels"]["baseline"]["transitive_calibration"]
           ["pearson_r_log_kV_delta_b"]] + \
          [ctrl["ijo_levels"][k]["transitive_calibration"]
           ["pearson_r_log_kV_delta_b"] for k in IJO_KEYS]
c_aucs = [nctrl["levels"]["baseline"]["transitive_calibration"]
          ["held_out"]["roc_auc"]] + \
         [ctrl["ijo_levels"][k]["transitive_calibration"]["held_out"]
          ["roc_auc"] for k in IJO_KEYS]

fig, (axA, axB, axC, axD) = plt.subplots(
    1, 4, figsize=(19.5, 4.6), constrained_layout=True)

axA.bar(xs - 0.17, gains, 0.34, color='firebrick',
        label='iJO1366 gained')
axA.bar(xs + 0.17, losses, 0.34, color='steelblue',
        label='iJO1366 lost')
for i, k in enumerate(IML_KEYS):
    fl = iml_res["levels"][k]["flips_vs_glucose_only"]
    j = 2 + i
    axA.plot([j], [fl["n_gain_essential"]], '*', ms=15, color='firebrick',
             alpha=0.55, label='iML1515 gained' if i == 0 else None)
    axA.plot([j], [fl["n_loss_essential"]], '*', ms=15, color='steelblue',
             alpha=0.55, label='iML1515 lost' if i == 0 else None)
axA.set_xticks(xs)
axA.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axA.set_ylabel("label flips vs glucose-only baseline")
axA.set_title("(a) Label re-stratification\n(zero at every level: the supply side)",
              fontsize=10)
axA.legend(fontsize=7.5)
axA.grid(alpha=0.3, axis='y')

axB.plot(xs, wts, 'o-', color='black')
for x, w in zip(xs, wts):
    axB.annotate(f"{w:.3f}", (x, w), textcoords="offset points",
                 xytext=(0, 7), fontsize=7, ha='center')
axB.axhline(base_ijo['wild_type_biomass'], color='gray', ls=':',
            lw=1, label='baseline WT')
axB.set_xticks(xs)
axB.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axB.set_ylabel("wild-type biomass")
axB.set_title("(b) Growth along the phosphate axis\n(89% reduction at Pi $-0.1$)",
              fontsize=10)
axB.legend(fontsize=7.5)
axB.grid(alpha=0.3, axis='y')

axC.plot(xs, pears, 'o-', color='darkgreen',
         label=r"Pearson $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axC.plot(xs, aucs, 's--', color='darkorange',
         label="held-out ROC AUC")
axC2 = axC.twinx()
axC2.plot(xs, pgiw, '^:', color='slategray',
          label="at-optimum PGI FVA width")
axC2.set_ylabel("PGI FVA width", color='slategray', fontsize=8)
axC2.tick_params(axis='y', labelsize=7, colors='slategray')
axC.set_xticks(xs)
axC.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axC.set_ylabel("statistic (plain FBA vertices)")
axC.set_ylim(0.45, 1.02)
axC.set_title("(c) Plain-FBA association\n(collapses with the carbon-sector degeneracy)",
              fontsize=10)
h1, l1 = axC.get_legend_handles_labels()
h2, l2 = axC2.get_legend_handles_labels()
axC.legend(h1 + h2, l1 + l2, fontsize=7.5)
axC.grid(alpha=0.3, axis='y')

axD.plot(xs, c_pears, 'o-', color='darkgreen',
         label=r"canonical $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axD.plot(xs, c_aucs, 's--', color='darkorange',
         label="canonical held-out ROC AUC")
axD.set_xticks(xs)
axD.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axD.set_ylabel("statistic (pFBA canonical vertices)")
axD.set_ylim(0.45, 1.02)
axD.set_title("(d) Canonical-vertex control\n(restored at every level)",
              fontsize=10)
axD.legend(fontsize=7.5)
axD.grid(alpha=0.3, axis='y')

fig.suptitle("Fourth perturbation axis: phosphate limitation "
             "(iJO1366 gradient; iML1515 cross-rebuild)",
             fontsize=12, fontweight="bold")
plt.savefig(os.path.join(DL, "keio_phosphate_limited_response.png"), dpi=120)
plt.close()
print("phosphate figure written.")
