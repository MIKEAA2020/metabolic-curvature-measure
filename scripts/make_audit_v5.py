#!/usr/bin/env python3
"""Generate audit_v5_numbers.py from audit_v4_numbers.py:
header update, output paths v4->v5, appended Keio/T7 checks."""
import io

src = io.open("audit_v4_numbers.py", encoding="utf-8").read()

old_doc = 'Numeric consistency audit of journal_manuscript_v4.tex (3rd-wave repair round:'
new_doc = ('Numeric consistency audit of journal_manuscript_v4.tex + '
           'companion_categorical_v3.tex (glucose-only Keio re-run + T7b/T7c round; '
           'extends the v4 audit with the Keio section and the new propositions '
           'of patch D. Legacy header: 3rd-wave repair round:')
assert old_doc in src, "docstring anchor"
src = src.replace(old_doc, new_doc, 1)

assert src.count("v4_number_audit.json") == 2
assert src.count("v4_number_audit.md") == 2
src = src.replace("v4_number_audit.json", "v5_number_audit.json")
src = src.replace("v4_number_audit.md", "v5_number_audit.md")

NEWCHECKS = '''
# =====================================================================
# Z. Glucose-only Keio re-run round (companion v3 patch D)
# =====================================================================
gz = json.load(open(os.path.join(DL, "keio_glucose_only_e12_results.json")))
check("KEIO-1", "glucose-only WT iJO1366 = 0.98237",
      "keio_glucose_only_e12_results.json:wild_type_biomass",
      f"{gz['wild_type_biomass']:.5f}",
      close(gz["wild_type_biomass"], 0.98237, 1e-5))
check("KEIO-2", "glucose-only essentials 289/1367, zero flips",
      "keio_glucose_only_e12_results.json:n_essential + label_flip_comparison",
      f"{gz['n_essential']}/{gz['n_genes_processed']}, "
      f"flips +{gz['label_flip_comparison_vs_deposited']['new_only']}/"
      f"-{gz['label_flip_comparison_vs_deposited']['old_only']}",
      gz["n_essential"] == 289 and gz["n_genes_processed"] == 1367
      and gz["label_flip_comparison_vs_deposited"]["new_only"] == 0
      and gz["label_flip_comparison_vs_deposited"]["old_only"] == 0)
check("KEIO-3", "E12' Pearson +0.603 (p=2.2e-136)",
      "keio_glucose_only_e12_results.json:calibration",
      f"r={gz['calibration']['pearson_r_log_kV_delta_b']:.4f}, "
      f"p={gz['calibration']['pearson_p_value']:.2e}",
      close(gz["calibration"]["pearson_r_log_kV_delta_b"], 0.603)
      and close(gz["calibration"]["pearson_p_value"], 2.2e-136, 0.05))
check("KEIO-4", "E12' Spearman +0.592; partial +0.601; CI [0.578,0.631]",
      "keio_glucose_only_e12_results.json:calibration",
      f"rho={gz['calibration']['spearman_rho_kV_delta_b']:.4f}, "
      f"partial={gz['calibration']['partial_r_given_n_gpr_rxns']:.4f}, "
      f"CI=[{gz['calibration']['bootstrap_95ci_low']:.4f},"
      f"{gz['calibration']['bootstrap_95ci_high']:.4f}]",
      close(gz["calibration"]["spearman_rho_kV_delta_b"], 0.592)
      and close(gz["calibration"]["partial_r_given_n_gpr_rxns"], 0.601)
      and close(gz["calibration"]["bootstrap_95ci_low"], 0.578)
      and close(gz["calibration"]["bootstrap_95ci_high"], 0.631))
ho = gz["held_out_essentiality_prediction"]
check("KEIO-5", "E12' held-out AUC 0.977, MCC 0.882, sens 0.885, spec 0.982, P@200 0.915",
      "keio_glucose_only_e12_results.json:held_out + precision_at_k",
      f"AUC={ho['roc_auc']:.4f}, MCC={ho['mcc']:.4f}, "
      f"sens={ho['sensitivity']:.4f}, spec={ho['specificity']:.4f}, "
      f"P@200={gz['precision_at_k']['K=200']['precision']:.4f}",
      close(ho["roc_auc"], 0.977) and close(ho["mcc"], 0.882)
      and close(ho["sensitivity"], 0.885) and close(ho["specificity"], 0.982)
      and close(gz["precision_at_k"]["K=200"]["precision"], 0.915))

g15 = json.load(open(os.path.join(DL, "keio_glucose_only_e15_results.json")))
dv = g15["direct_validation"]
check("KEIO-6", "E15' Pearson +0.230 (p=6.7e-16), Spearman +0.256, AUC 0.738",
      "keio_glucose_only_e15_results.json:direct_validation",
      f"r={dv['pearson_r']:.4f}, p={dv['pearson_p']:.2e}, "
      f"rho={dv['spearman_rho']:.4f}, AUC={dv['roc_auc']:.4f}",
      close(dv["pearson_r"], 0.230)
      and close(dv["pearson_p"], 6.7e-16, 0.05)
      and close(dv["spearman_rho"], 0.256)
      and close(dv["roc_auc"], 0.738))
h15 = g15["held_out_70_30"]
check("KEIO-7", "E15' held-out AUC 0.763, sens 0.846, spec 0.607, MCC 0.283",
      "keio_glucose_only_e15_results.json:held_out_70_30",
      f"AUC={h15['roc_auc']:.4f}, sens={h15['sensitivity']:.4f}, "
      f"spec={h15['specificity']:.4f}, MCC={h15['mcc']:.4f}",
      close(h15["roc_auc"], 0.763) and close(h15["sensitivity"], 0.846)
      and close(h15["specificity"], 0.607) and close(h15["mcc"], 0.283))
check("KEIO-8", "E15' strata 84/35, high-conf AUC 0.713, gaps 30, mismatch 217->180",
      "keio_glucose_only_e15_results.json:pec_stratification + csv crosstab",
      f"hi={g15['pec_stratification']['n_high_conf']}, "
      f"lo={g15['pec_stratification']['n_low_conf']}, "
      f"hiAUC={g15['pec_stratification'].get('high_conf_auc')}, "
      f"gaps={g15['n_model_gaps_pecE_insilicoN']}",
      g15["pec_stratification"]["n_high_conf"] == 84
      and g15["pec_stratification"]["n_low_conf"] == 35
      and close(g15["pec_stratification"].get("high_conf_auc", 0), 0.713)
      and g15["n_model_gaps_pecE_insilicoN"] == 30)

g16 = json.load(open(os.path.join(DL, "keio_glucose_only_e16_results.json")))
d16 = g16["direct_validation"]
check("KEIO-9", "glucose-only WT iML1515 = 0.82180",
      "keio_glucose_only_e16_results.json:wild_type_biomass",
      f"{g16['wild_type_biomass']:.5f}",
      close(g16["wild_type_biomass"], 0.82180, 1e-5))
check("KEIO-10", "E16' Pearson +0.376 (p=9.6e-46), Spearman +0.304, AUC 0.813; binary 1325/114; gaps 13",
      "keio_glucose_only_e16_results.json",
      f"r={d16['pearson_r']:.4f}, p={d16['pearson_p']:.2e}, "
      f"rho={d16['spearman_rho']:.4f}, AUC={d16['roc_auc']:.4f}, "
      f"binary={g16['binary_subset']}, gaps={g16['n_model_gaps_pecE_insilicoN']}",
      close(d16["pearson_r"], 0.376)
      and close(d16["pearson_p"], 9.6e-46, 0.05)
      and close(d16["spearman_rho"], 0.304)
      and close(d16["roc_auc"], 0.813)
      and g16["binary_subset"]["n"] == 1325 and g16["binary_subset"]["n_E"] == 114
      and g16["n_model_gaps_pecE_insilicoN"] == 13)

companion = open(os.path.join(BASE, "scripts", "companion_categorical_v3.tex"),
                 encoding="utf-8").read()
check("KEIO-11", "companion quotes fractions 0.498 and 0.853 (battery)",
      "companion_categorical_v3.tex:prop:poincare-averaging + tab:network-battery",
      "0.498 count: %d, 0.853 count: %d" % (companion.count("0.498"),
                                             companion.count("0.853")),
      "0.498" in companion and "0.853" in companion)

check("KEIO-12", "prop:keio-glucose-only confusion (318,6,10,77) quoted",
      "keio_glucose_only_e12_results.json:confusion_matrix",
      str(ho["confusion_matrix"]),
      ho["confusion_matrix"] == {"tn": 318, "fp": 6, "fn": 10, "tp": 77})
'''
marker = "out = {"
assert marker in src
src = src.replace(marker, NEWCHECKS + "\n" + marker, 1)

io.open("audit_v5_numbers.py", "w", encoding="utf-8").write(src)
print("audit_v5_numbers.py written")
