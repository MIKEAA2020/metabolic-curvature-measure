#!/usr/bin/env python3
"""Regenerate the oxygen-probe dose-response figure from the PATCHED
results JSONs (the fabZ row correction changed the iML anaerobic
flip counts: +6 gains / -0 losses).  Redraws the exact two-panel
figure of o2_limited_keio_probe.py PART 4 from artifacts only.
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

ijo_results = json.load(open(os.path.join(DL,
                                          "keio_o2_limited_e12_results.json")))
iml_results = json.load(open(os.path.join(DL,
                                          "keio_o2_limited_e16_results.json")))
base_ijo = json.load(open(os.path.join(DL,
                                       "keio_glucose_only_e12_results.json")))
O2_LEVELS_IJO = [-10.0, -5.0, -2.5]
IML_LEVELS = [-5.0, 0.0]

levs = [-20.0] + O2_LEVELS_IJO
gains = [0] + [ijo_results["levels"][str(o2)]["flips_vs_glucose_only"]["n_gain_essential"]
               for o2 in O2_LEVELS_IJO]
losses = [0] + [ijo_results["levels"][str(o2)]["flips_vs_glucose_only"]["n_loss_essential"]
                for o2 in O2_LEVELS_IJO]
pears = [base_ijo['calibration']['pearson_r_log_kV_delta_b']] + \
        [ijo_results["levels"][str(o2)]["transitive_calibration"]["pearson_r_log_kV_delta_b"]
         for o2 in O2_LEVELS_IJO]
aucs = [base_ijo['held_out_essentiality_prediction']['roc_auc']] + \
       [ijo_results["levels"][str(o2)]["transitive_calibration"]["held_out"]["roc_auc"]
        for o2 in O2_LEVELS_IJO]

fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.5, 5), constrained_layout=True)
axA.plot(levs, gains, 'o-', color='firebrick', label='gain essentiality')
axA.plot(levs, losses, 's-', color='steelblue', label='lose essentiality')
for o2 in IML_LEVELS:
    fl = iml_results["levels"][str(o2)]["flips_vs_glucose_only"]
    axA.plot([o2], [fl["n_gain_essential"]], '*', ms=14,
             color='firebrick', alpha=0.55,
             label=f'iML1515, O2 = {o2:g} (gain)')
    axA.plot([o2], [fl["n_loss_essential"]], '*', ms=14,
             color='steelblue', alpha=0.55,
             label=f'iML1515, O2 = {o2:g} (lose)')
axA.set_xlabel(r"oxygen exchange bound $[\mathrm{mmol/gDW/h}]$")
axA.set_ylabel("label flips vs glucose-only baseline")
axA.set_title("(a) Essentiality-label re-stratification")
axA.invert_xaxis()
axA.legend(fontsize=9)
axA.grid(alpha=0.3)

axB.plot(levs, pears, 'o-', color='darkgreen',
         label=r"Pearson $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)$")
axB.plot(levs, aucs, 's--', color='darkorange',
         label="held-out ROC AUC (label prediction)")
axB.set_xlabel(r"oxygen exchange bound $[\mathrm{mmol/gDW/h}]$")
axB.set_ylabel("statistic")
axB.set_title("(b) Curvature-phenotype association")
axB.invert_xaxis()
axB.legend(fontsize=9)
axB.grid(alpha=0.3)
fig.suptitle("Second perturbation probe: oxygen-limited medium "
             "(iJO1366 dose response; baseline O2 $-$20)",
             fontsize=12, fontweight="bold")
plt.savefig(os.path.join(DL, "keio_o2_limited_dose_response.png"), dpi=120)
plt.close()
print("O2 figure regenerated from patched artifacts.")
