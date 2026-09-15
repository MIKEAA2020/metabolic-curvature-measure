#!/usr/bin/env python3
"""Assemble the multi-axis canonical-selection table from the five
control JSONs + probe-results JSONs (merged six-axis round: the
remote's corrected phosphate/iron artifacts + the sixth ATPM axis
with integrity corrections).

Outputs:
  download/multiaxis_canonical_table.json   (machine-readable)
  download/multiaxis_canonical_table.txt    (formatted working table)
"""
import os, json

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "download")


def load(fn):
    with open(os.path.join(OUT, fn)) as f:
        return json.load(f)


def canon_stats(v):
    c = v["transitive_calibration"]
    return {
        "canon_r": c["pearson_r_log_kV_delta_b"],
        "canon_auc": c["held_out"]["roc_auc"],
        "canon_mcc": c["held_out"]["mcc"],
        "kappa": v["label_agreement_fba_vs_pfba_kappa"],
        "n_essential": v["n_essential"], "n_genes": v["n_genes"],
        "wt": v["wild_type_biomass"],
    }


def plain_from_results(res, key):
    lv = None
    if key in res["levels"]:
        lv = res["levels"][key]
    else:
        try:
            kf = float(key)
        except ValueError:
            kf = None
        for k, v in res["levels"].items():
            try:
                if float(k) == kf:
                    lv = v
                    break
            except ValueError:
                continue
    if lv is None:
        raise KeyError(key)
    c = lv["transitive_calibration"]
    return {"plain_r": c["pearson_r_log_kV_delta_b"],
            "plain_auc": c["held_out"]["roc_auc"]}


WT_IJO = load("keio_glucose_only_e12_results.json")["wild_type_biomass"]
WT_IML = load("keio_glucose_only_e16_results.json")["wild_type_biomass"]

nit = load("keio_nitrogen_pfba_control.json")
nit_e12 = load("keio_nitrogen_source_e12_results.json")
nit_e16 = load("keio_nitrogen_source_e16_results.json")
o2 = load("keio_o2_pfba_control.json")
o2_e12 = load("keio_o2_limited_e12_results.json")
o2_e16 = load("keio_o2_limited_e16_results.json")
pi = load("keio_phosphate_pfba_control.json")
pi_e12 = load("keio_phosphate_limited_e12_results.json")
pi_e16 = load("keio_phosphate_limited_e16_results.json")
fe = load("keio_iron_pfba_control.json")
fe_e12 = load("keio_iron_limited_e12_results.json")
fe_e16 = load("keio_iron_limited_e16_results.json")
atpm_c = load("keio_atpm_pfba_control.json")
atpm_e12 = load("keio_atpm_stress_e12_results.json")
atpm_e16 = load("keio_atpm_stress_e16_results.json")

rows = []


def add(axis, model, key, cval, plain, wt, pgi=None, note=None):
    r = canon_stats(cval)
    r.update(plain)
    r["wt_red"] = 1 - r["wt"] / wt
    if pgi is not None:
        r["pgi_width"] = pgi
    if note:
        r["note"] = note
    rows.append({"axis": axis, "model": model, "level": key, **r})


# ---- nitrogen (limitation gradient + substitution)
for key in ["nh4_-10", "nh4_-5", "nh4_-2.5", "glu_-10", "arg_-10"]:
    v = nit["levels"][key]
    add("nitrogen", "iJO1366", key, v,
        plain_from_results(nit_e12, key), WT_IJO)
for pk in ["nh4_-2.5", "glu_-10", "arg_-10"]:
    v = nit["iml_levels"][pk if pk in nit["iml_levels"] else "iml_" + pk]
    add("nitrogen", "iML1515", pk, v,
        plain_from_results(nit_e16, pk), WT_IML)

# ---- oxygen
for key in ["ijo_o2_2.5", "ijo_o2_5", "ijo_o2_10"]:
    v = o2["ijo_levels"][key]
    pk = key.replace("ijo_o2_", "")
    add("oxygen", "iJO1366", f"O2 {pk}", v,
        plain_from_results(o2_e12, f"-{pk}"), WT_IJO)
add("oxygen", "iML1515", "baseline", o2["iml_levels"]["iml_baseline"],
    {"plain_r": 0.8751, "plain_auc": 0.99}, WT_IML)
for key in ["iml_o2_5", "iml_o2_0"]:
    v = o2["iml_levels"][key]
    pk = key.replace("iml_o2_", "")
    add("oxygen", "iML1515", f"O2 {pk}", v,
        plain_from_results(o2_e16, f"-{pk}"), WT_IML,
        note=("anaerobic regime switch" if pk == "0" else None))

# ---- phosphate (corrected artifacts)
for key in ["pi_0.5", "pi_0.25", "pi_0.1"]:
    v = pi["ijo_levels"][key]
    add("phosphate", "iJO1366", key, v,
        plain_from_results(pi_e12, key), WT_IJO)
for key in ["pi_0.25", "pi_0.1"]:
    v = pi["iml_levels"][key if key in pi["iml_levels"]
                         else "iml_" + key]
    add("phosphate", "iML1515", key, v,
        plain_from_results(pi_e16, key), WT_IML)

# ---- iron (remote's level design, above the tolerance boundary)
for key in ["fe_0.01", "fe_0.005", "fe_0.0025"]:
    v = fe["ijo_levels"][key]
    add("iron", "iJO1366", key, v,
        plain_from_results(fe_e12, key), WT_IJO)
for key in ["fe_0.005", "fe_0.0025"]:
    v = fe["iml_levels"][key if key in fe["iml_levels"]
                         else "iml_" + key]
    add("iron", "iML1515", key, v,
        plain_from_results(fe_e16, key), WT_IML)

# ---- ATPM (sixth axis, integrity-corrected)
for key in ["atpm_40", "atpm_60", "atpm_80", "atpm_100"]:
    v = atpm_c["ijo_levels"][key]
    pgi = atpm_e12["levels"][key]["degeneracy"]["fva_widths"]["PGI"]
    add("ATPM (non-medium)", "iJO1366", key, v,
        plain_from_results(atpm_e12, key), WT_IJO, pgi)
for key in ["atpm_60", "atpm_80", "atpm_100"]:
    v = atpm_c["iml_levels"][key]
    pgi = atpm_e16["levels"][key]["degeneracy"]["fva_widths"]["PGI"]
    note = ("L1 near-tie floor (782/1129 compensables at ~200.01)"
            if key == "atpm_100" else
            ("L1 near-tie floor present" if key in ("atpm_60", "atpm_80")
             else None))
    add("ATPM (non-medium)", "iML1515", key, v,
        plain_from_results(atpm_e16, key), WT_IML, pgi, note)

# ---- formatted output
L = []
L.append("MULTI-AXIS CANONICAL-SELECTION TABLE (six-axis round, merged "
         "and integrity-corrected)")
L.append(f"Baselines: iJO1366 WT {WT_IJO:.4f} plain +0.603 -> canonical "
         f"+0.945 (AUC 1.000); iML1515 WT {WT_IML:.4f} plain +0.875 -> "
         f"canonical +0.937 (AUC 0.987)")
L.append("")
hdr = (f"{'axis':18s} {'model':9s} {'level':12s} {'WTred':>6s} "
       f"{'plain r':>9s} {'canon r':>9s} {'canAUC':>7s} {'kappa':>7s} "
       f"{'PGIw':>7s}")
L.append(hdr)
L.append("-" * len(hdr))
for r in rows:
    pgi = (f"{r['pgi_width']:7.1f}" if r.get("pgi_width") is not None
           else f"{'-':>7s}")
    L.append(f"{r['axis']:18s} {r['model']:9s} {r['level']:12s} "
             f"{-r['wt_red']*100:5.0f}% {r['plain_r']:+9.4f} "
             f"{r['canon_r']:+9.4f} {r['canon_auc']:7.4f} "
             f"{r['kappa']:7.4f} {pgi}"
             + (f"   [{r['note']}]" if r.get("note") else ""))

n_lvl = sum(1 for r in rows if r["level"] != "baseline")
agg = {
    "n_levels": n_lvl, "n_rows": len(rows),
    "kappa_ge_099": sum(1 for r in rows if r["kappa"] >= 0.99),
    "kappa_eq_1": sum(1 for r in rows if r["kappa"] >= 0.9999),
    "kappa_min": min(r["kappa"] for r in rows),
    "canon_r_ge_090": sum(1 for r in rows if r["canon_r"] >= 0.90),
    "canon_auc_ge_098": sum(1 for r in rows if r["canon_auc"] >= 0.98),
    "canon_auc_min": min(r["canon_auc"] for r in rows),
    "canon_r_gain_gt_005": sum(1 for r in rows
                               if r["canon_r"] > r["plain_r"] + 0.05),
    "canon_r_gain_max": max(r["canon_r"] - r["plain_r"] for r in rows),
}
L.append("")
L.append(f"levels (excl. baselines): {n_lvl}; arm kappa = 1.000 at "
         f"{agg['kappa_eq_1']} of {len(rows)} rows; kappa min "
         f"{agg['kappa_min']:.4f}; canonical r >= 0.90: "
         f"{agg['canon_r_ge_090']}; canonical AUC >= 0.98: "
         f"{agg['canon_auc_ge_098']} (min {agg['canon_auc_min']:.4f}); "
         f"canonical r gain > 0.05: {agg['canon_r_gain_gt_005']}; "
         f"max gain {agg['canon_r_gain_max']:+.4f}")
with open(os.path.join(OUT, "multiaxis_canonical_table.txt"), "w") as f:
    f.write("\n".join(L) + "\n")
with open(os.path.join(OUT, "multiaxis_canonical_table.json"), "w") as f:
    json.dump({"WT_baseline": {"iJO1366": WT_IJO, "iML1515": WT_IML},
               "rows": rows, "aggregates": agg}, f, indent=2)
print("\n".join(L))
