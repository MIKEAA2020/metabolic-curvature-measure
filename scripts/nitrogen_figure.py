#!/usr/bin/env python3
"""Final publication figure for the nitrogen-axis probe: 4 panels.

(a) label flips vs glucose-only baseline per level (iJO bars + iML stars)
(b) wild-type growth along the axis (the matched-N control visible)
(c) plain-FBA association statistics (the N-limited collapse)
(d) canonical (pFBA) association statistics (the restoration)

Reads only committed artifacts; writes download/keio_nitrogen_source_response.png
(same filename the probe used).
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

ijo_res = json.load(open(os.path.join(DL,
                                      "keio_nitrogen_source_e12_results.json")))
iml_res = json.load(open(os.path.join(DL,
                                      "keio_nitrogen_source_e16_results.json")))
ctrl = json.load(open(os.path.join(DL, "keio_nitrogen_pfba_control.json")))
base_ijo = json.load(open(os.path.join(DL,
                                       "keio_glucose_only_e12_results.json")))
base_iml = json.load(open(os.path.join(DL,
                                       "keio_glucose_only_e16_results.json")))

IJO_KEYS = ["nh4_-10", "nh4_-5", "nh4_-2.5", "glu_-10", "arg_-10"]
IML_KEYS = ["nh4_-2.5", "glu_-10", "arg_-10"]
x_labels = ["baseline\n(nh4 unlim.)"] + \
           [k.replace("_", " ").replace("nh4", "NH$_4$")
            .replace("glu", "Glu").replace("arg", "Arg")
            + ("\n(swap)" if "glu" in k or "arg" in k else "")
            for k in IJO_KEYS]
xs = np.arange(len(x_labels))

gains = [0] + [ijo_res["levels"][k]["flips_vs_glucose_only"]["n_gain_essential"]
               for k in IJO_KEYS]
losses = [0] + [ijo_res["levels"][k]["flips_vs_glucose_only"]["n_loss_essential"]
                for k in IJO_KEYS]
wts = [base_ijo['wild_type_biomass']] + \
      [ijo_res["levels"][k]["wild_type_biomass"] for k in IJO_KEYS]
pears = [base_ijo['calibration']['pearson_r_log_kV_delta_b']] + \
        [ijo_res["levels"][k]["transitive_calibration"]
         ["pearson_r_log_kV_delta_b"] for k in IJO_KEYS]
aucs = [base_ijo['held_out_essentiality_prediction']['roc_auc']] + \
       [ijo_res["levels"][k]["transitive_calibration"]["held_out"]["roc_auc"]
        for k in IJO_KEYS]
ctrl_order = ["baseline", "nh4_-10", "glu_-10", "nh4_-2.5"]
ctrl_pos = {k: i for i, k in enumerate(ctrl_order)}
c_pears, c_aucs, c_x = [], [], []
for k in ctrl_order:
    d = ctrl["levels"][k]
    if k == "baseline":
        c_x.append(0); c_pears.append(d["transitive_calibration"]
                                       ["pearson_r_log_kV_delta_b"])
        c_aucs.append(d["transitive_calibration"]["held_out"]["roc_auc"])
    else:
        c_x.append(1 + IJO_KEYS.index(k))
        c_pears.append(d["transitive_calibration"]
                       ["pearson_r_log_kV_delta_b"])
        c_aucs.append(d["transitive_calibration"]["held_out"]["roc_auc"])

fig, (axA, axB, axC, axD) = plt.subplots(
    1, 4, figsize=(19.5, 4.6), constrained_layout=True)

axA.bar(xs - 0.17, gains, 0.34, color='firebrick',
        label='iJO1366 gained')
axA.bar(xs + 0.17, losses, 0.34, color='steelblue',
        label='iJO1366 lost')
for i, k in enumerate(IML_KEYS):
    fl = iml_res["levels"][k]["flips_vs_glucose_only"]
    j = 1 + IJO_KEYS.index(k)
    axA.plot([j], [fl["n_gain_essential"]], '*', ms=15, color='firebrick',
             alpha=0.55, label='iML1515 gained' if i == 0 else None)
    axA.plot([j], [fl["n_loss_essential"]], '*', ms=15, color='steelblue',
             alpha=0.55, label='iML1515 lost' if i == 0 else None)
axA.set_xticks(xs)
axA.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axA.set_ylabel("label flips vs glucose-only baseline")
axA.set_title("(a) Label re-stratification\n(only losses; N-assimilation module)",
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
axB.set_title("(b) Growth along the nitrogen axis\n(Glu $-$10 = NH$_4$ $-$10: matched N flux)",
              fontsize=10)
axB.legend(fontsize=7.5)
axB.grid(alpha=0.3, axis='y')

axC.plot(xs, pears, 'o-', color='darkgreen',
         label=r"Pearson $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axC.plot(xs, aucs, 's--', color='darkorange',
         label="held-out ROC AUC")
axC.set_xticks(xs)
axC.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axC.set_ylabel("statistic (plain FBA vertices)")
axC.set_ylim(0.45, 1.02)
axC.set_title("(c) Plain-FBA association\n(collapses on the N-limited levels)",
              fontsize=10)
axC.legend(fontsize=7.5)
axC.grid(alpha=0.3, axis='y')

axD.plot(c_x, c_pears, 'o-', color='darkgreen',
         label=r"canonical $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axD.plot(c_x, c_aucs, 's--', color='darkorange',
         label="canonical held-out ROC AUC")
axD.set_xticks(xs)
axD.set_xticklabels(x_labels, fontsize=7.5, rotation=22, ha='right')
axD.set_ylabel("statistic (pFBA canonical vertices)")
axD.set_ylim(0.45, 1.02)
axD.set_title("(d) Canonical-vertex control\n(association restored everywhere)",
              fontsize=10)
axD.legend(fontsize=7.5)
axD.grid(alpha=0.3, axis='y')

fig.suptitle("Third perturbation axis: nitrogen source "
             "(iJO1366: NH$_4$ limitation gradient + Glu/Arg substitution; "
             "iML1515 cross-rebuild)",
             fontsize=12, fontweight="bold")
plt.savefig(os.path.join(DL, "keio_nitrogen_source_response.png"), dpi=120)
plt.close()
print("Figure rewritten.")
