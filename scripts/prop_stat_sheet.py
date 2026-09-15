#!/usr/bin/env python3
"""Prop-ready stat sheet for the phosphate / iron / ATPM propositions:
WT values, label flips vs glucose-only baseline, gain/loss gene names
(resolved from the model gene objects), per-level canonical stats.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
OUT = os.path.join(REPO, "download")

from cobra.io import load_json_model

ijo = load_json_model(os.path.join(REPO, "data/bigg_models/iJO1366.json"))
iml = load_json_model(os.path.join(REPO, "data/bigg_models/iML1515.json"))
NAME = {m.id: (m.name or "?") for m in ijo.genes}
NAME.update({m.id: (m.name or "?") for m in iml.genes})


def flips(res_json, prefix, model_tag):
    d = json.load(open(os.path.join(OUT, res_json)))
    for key, lv in sorted(d["levels"].items()):
        fl = lv.get("flips_vs_glucose_only", {})
        gains = [f"{g['gene_id']}({g.get('gene_name','?')})"
                 for g in fl.get("gains", [])]
        losses = [f"{g['gene_id']}({g.get('gene_name','?')})"
                  for g in fl.get("losses", [])]
        print(f"{model_tag} {key}: labels {fl.get('n_essential_base')}"
              f" -> {fl.get('n_essential_new')} "
              f"(+{fl.get('n_gain_essential')}/-{fl.get('n_loss_essential')}, "
              f"kappa {fl.get('cohen_kappa'):.4f})")
        if gains:
            print(f"   gains: {', '.join(gains[:45])}")
        if losses:
            print(f"   losses: {', '.join(losses[:45])}")


print("=== PHOSPHATE ===")
flips("keio_phosphate_limited_e12_results.json", "pi", "iJO")
flips("keio_phosphate_limited_e16_results.json", "pi", "iML")
print("\n=== IRON ===")
flips("keio_iron_limited_e12_results.json", "fe", "iJO")
flips("keio_iron_limited_e16_results.json", "fe", "iML")
print("\n=== ATPM ===")
flips("keio_atpm_stress_e12_results.json", "atpm", "iJO")
flips("keio_atpm_stress_e16_results.json", "atpm", "iML")

print("\n=== WT biomass + uptake details ===")
for fn, tag in [("keio_phosphate_limited_e12_results.json", "pi iJO"),
                ("keio_phosphate_limited_e16_results.json", "pi iML"),
                ("keio_iron_limited_e12_results.json", "fe iJO"),
                ("keio_iron_limited_e16_results.json", "fe iML"),
                ("keio_atpm_stress_e12_results.json", "atpm iJO"),
                ("keio_atpm_stress_e16_results.json", "atpm iML")]:
    d = json.load(open(os.path.join(OUT, fn)))
    for key, lv in sorted(d["levels"].items()):
        extra = []
        for f in ("pi_uptake", "fe_uptake", "atpm_flux"):
            if f in lv:
                extra.append(f"{f}={lv[f]}")
        print(f"{tag} {key}: WT={lv['wild_type_biomass']:.4f} "
              + " ".join(extra))

print("\n=== gene-name resolution for flip genes ===")
for gid in ["b0180", "b3412", "b0778", "b3731", "b3739", "b0429", "b0432",
            "b2926", "b3115", "b1849", "b2296", "b0116", "b2779", "b1319",
            "b3875", "b1136", "b0945", "b0870"]:
    print(f"  {gid}: {NAME.get(gid, '?')}")

print("\n=== iron prescreen (demand) ===")
p = os.path.join(OUT, "keio_fifth_axis_prescreen.json")
if os.path.exists(p):
    d = json.load(open(p))
    print(json.dumps(d, indent=1)[:900])
