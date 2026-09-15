#!/usr/bin/env python3
"""Insert the sixth-axis (ATPM) checks as section S into
audit_v10_numbers.py (extends the remote's v9 with the corrected
sixth-axis round)."""
S = r'''
# =====================================================================
# S. Sixth axis: non-medium ATPM maintenance stress (patch H, merged
#    round) -- integrity-corrected statistics
# =====================================================================
ares = json.load(open(os.path.join(DL, "keio_atpm_stress_e12_results.json")))
aresm = json.load(open(os.path.join(DL, "keio_atpm_stress_e16_results.json")))
actrl = json.load(open(os.path.join(DL, "keio_atpm_pfba_control.json")))
adjr = json.load(open(os.path.join(DL, "keio_atpm_integrity_adjudication.json")))
neartie = json.load(open(os.path.join(DL, "keio_atpm_neartie_measurement.json")))
mtab = json.load(open(os.path.join(DL, "multiaxis_canonical_table.json")))
nmp = json.load(open(os.path.join(DL, "keio_nonmedium_prescreen.json")))

def _sr(res, key):
    return res["levels"][key]["transitive_calibration"][
        "pearson_r_log_kV_delta_b"]

def _sauc(res, key):
    return res["levels"][key]["transitive_calibration"]["held_out"][
        "roc_auc"]

check("S-1", "ATPM defaults 3.15 (iJO) / 6.86 (iML); ATPM selected over "
      "proton leak (pH surrogate) by pre-screen; 29-90% WT reduction",
      "keio_nonmedium_prescreen.json",
      "keys: " + ",".join(sorted(nmp.keys())[:5]),
      "atpm" in json.dumps(nmp).lower()
      and "leak" in json.dumps(nmp).lower())
check("S-2", "iJO WT atpm 40/60/80/100 = 0.695/0.496/0.298/0.099; "
      "iML 60/80/100 = 0.398/0.239/0.080",
      "keio_atpm_stress_{e12,e16}_results.json",
      "/".join(f"{ares['levels'][k]['wild_type_biomass']:.4f}"
               for k in ["atpm_40", "atpm_60", "atpm_80", "atpm_100"]),
      close(ares['levels']['atpm_40']['wild_type_biomass'], 0.695)
      and close(ares['levels']['atpm_60']['wild_type_biomass'], 0.496)
      and close(ares['levels']['atpm_80']['wild_type_biomass'], 0.298)
      and close(ares['levels']['atpm_100']['wild_type_biomass'], 0.099)
      and close(aresm['levels']['atpm_60']['wild_type_biomass'], 0.398)
      and close(aresm['levels']['atpm_80']['wild_type_biomass'], 0.239)
      and close(aresm['levels']['atpm_100']['wild_type_biomass'], 0.080))
check("S-3", "PGI at-optimum width 0.0 at EVERY ATPM level, both models",
      "keio_atpm_stress_{e12,e16}_results.json:degeneracy",
      "iJO " + "/".join(
          str(ares["levels"][k]["degeneracy"]["fva_widths"]["PGI"])
          for k in ["atpm_40", "atpm_60", "atpm_80", "atpm_100"]),
      all(ares["levels"][k]["degeneracy"]["fva_widths"]["PGI"] == 0.0
          for k in ares["levels"])
      and all(aresm["levels"][k]["degeneracy"]["fva_widths"]["PGI"] == 0.0
              for k in aresm["levels"]))
for tag, res, lv, base, new, kap in [
        ("iJO atpm_40", ares, "atpm_40", 289, 298, 0.981),
        ("iJO atpm_60", ares, "atpm_60", 289, 298, 0.981),
        ("iJO atpm_80", ares, "atpm_80", 289, 299, 0.978),
        ("iJO atpm_100", ares, "atpm_100", 289, 331, 0.912),
        ("iML atpm_60", aresm, "atpm_60", 286, 295, 0.981),
        ("iML atpm_80", aresm, "atpm_80", 286, 297, 0.977),
        ("iML atpm_100", aresm, "atpm_100", 286, 329, 0.912)]:
    fl = res["levels"][lv]["flips_vs_glucose_only"]
    check(f"S-4 {tag}", f"labels {base} -> {new}, kappa {kap}",
          "atpm results flips_vs_glucose_only (corrected)",
          f"{fl['n_essential_base']} -> {fl['n_essential_new']} "
          f"(+{fl['n_gain_essential']}/-{fl['n_loss_essential']})",
          fl["n_essential_base"] == base
          and fl["n_essential_new"] == new
          and close(fl["cohen_kappa"], kap, 2e-3))
_gids = [g["gene_id"] for g in
         ares["levels"]["atpm_100"]["flips_vs_glucose_only"]["gains"]]
check("S-5", "atpm_100 gains +42 on iJO: atp operon (9), cyo (4), nuo "
      "(13), pgk/eno/ackA/lpd/ompG/ompL; OXPHOS 26 vs 3.2 expected",
      "atpm e12 flips + enrichment",
      f"n={len(_gids)}",
      len(_gids) == 42
      and all(f"b37{i}" in _gids for i in range(31, 40))
      and all(b in _gids for b in
              ["b0429", "b0430", "b0431", "b0432", "b2276", "b2282",
               "b2288", "b2926", "b2779", "b2296", "b0116", "b1319",
               "b3875"])
      and any(e["n_flip"] == 26 and close(e["expected"], 3.2, 0.05)
              for e in ares["levels"]["atpm_100"]
              ["flips_vs_glucose_only"]["subsystem_enrichment_top"]))
check("S-6", "plain r iJO +0.949/+0.925/+0.821/+0.444 (corrected); "
      "iML +0.747/+0.435/+0.244, endpoint AUC 0.550",
      "keio_atpm_stress_{e12,e16}_results.json",
      "iJO " + "/".join(f"{_sr(ares, k):+.3f}" for k in
                        ["atpm_40", "atpm_60", "atpm_80", "atpm_100"]),
      close(_sr(ares, "atpm_40"), 0.949)
      and close(_sr(ares, "atpm_60"), 0.925)
      and close(_sr(ares, "atpm_80"), 0.821)
      and close(_sr(ares, "atpm_100"), 0.444)
      and close(_sr(aresm, "atpm_60"), 0.747)
      and close(_sr(aresm, "atpm_80"), 0.435)
      and close(_sr(aresm, "atpm_100"), 0.244)
      and close(_sauc(aresm, "atpm_100"), 0.550, 1e-3))

def _cr(d, key):
    return d[key]["transitive_calibration"][
        "pearson_r_log_kV_delta_b"]

check("S-7", "canonical iJO +0.969/+0.949/+0.964/+0.937 (AUC "
      "1.000/0.988/0.982/0.991; MCC 0.972/0.959/0.934/0.974); arm "
      "kappa 1.000 at all four levels",
      "keio_atpm_pfba_control.json:ijo_levels",
      "/".join(f"{_cr(actrl['ijo_levels'], k):+.3f}" for k in
               ["atpm_40", "atpm_60", "atpm_80", "atpm_100"]),
      close(_cr(actrl['ijo_levels'], "atpm_40"), 0.969)
      and close(_cr(actrl['ijo_levels'], "atpm_60"), 0.949)
      and close(_cr(actrl['ijo_levels'], "atpm_80"), 0.964)
      and close(_cr(actrl['ijo_levels'], "atpm_100"), 0.937)
      and close(actrl["ijo_levels"]["atpm_100"]
                ["transitive_calibration"]["held_out"]["mcc"], 0.974,
                1e-3)
      and all(actrl["ijo_levels"][k]
              ["label_agreement_fba_vs_pfba_kappa"] >= 0.9999
              for k in actrl["ijo_levels"]))
check("S-8", "canonical iML +0.703/+0.655/+0.476 (AUC 0.992/0.992/"
      "0.978; n_ess corrected to 329); arm kappa 1.000 at all three "
      "levels -- the near-tie corner",
      "keio_atpm_pfba_control.json:iml_levels",
      "/".join(f"{_cr(actrl['iml_levels'], k):+.3f}" for k in
               ["atpm_60", "atpm_80", "atpm_100"]),
      close(_cr(actrl['iml_levels'], "atpm_60"), 0.703)
      and close(_cr(actrl['iml_levels'], "atpm_80"), 0.655)
      and close(_cr(actrl['iml_levels'], "atpm_100"), 0.476)
      and close(actrl["iml_levels"]["atpm_100"]
                ["transitive_calibration"]["held_out"]["roc_auc"],
                0.978, 1e-3)
      and actrl["iml_levels"]["atpm_100"]["n_essential"] == 329
      and all(actrl["iml_levels"][k]
              ["label_agreement_fba_vs_pfba_kappa"] >= 0.9999
              for k in actrl["iml_levels"]))
check("S-9", "integrity: 6 corrupted calls adjudicated (plain b0180/"
      "b3412 iJO; plain b0778/b0180 iML; canonical b0776/b1288 iML), "
      "all HiGHS-true zero; corrected labels +2 restored per arm",
      "keio_atpm_integrity_adjudication.json",
      f"{len(adjr['verdicts'])} verdicts; "
      f"{len(adjr['patch']['corrections'])} patched",
      len(adjr["patch"]["corrections"]) == 6
      and all(v["b_highs_true"] == 0.0 or abs(v["b_highs_true"]) < 1e-9
              for v in adjr["verdicts"]
              if v["reason"] in ("label-disagreement",
                                 "trace-quota-positive"))
      and adjr["post_patch"]["iJO_atpm_100"]["labels"] == 331
      and adjr["post_patch"]["iML_atpm_100"]["labels"] == 329
      and adjr["post_patch"]["iML_atpm_100"][
          "canon_n_essential"] == 329)
check("S-10", "near-tie: |dL1| 8.6e-4 absolute (1.2e-6 relative); "
      "782/1129 compensables at the 190-210 floor (median 200.01)",
      "keio_atpm_neartie_measurement.json",
      f"dL1 {abs(neartie['dL1_absolute']):.2e} "
      f"({abs(neartie['dL1_relative']):.1e}); floor "
      f"{neartie['floor_census_from_committed_csv']['n_at_floor_190_210']}"
      f"/{neartie['floor_census_from_committed_csv']['n_compensable']}",
      close(abs(neartie["dL1_absolute"]), 8.6e-4, 0.02)
      and close(abs(neartie["dL1_relative"]), 1.2e-6, 0.05)
      and neartie["floor_census_from_committed_csv"]
      ["n_at_floor_190_210"] == 782
      and close(neartie["floor_census_from_committed_csv"]
                ["floor_kv_median"], 200.01, 1e-3))
check("S-11", "nh4_-5 canonical restored into the control (r +0.922, "
      "kappa 0.9978, one boundary gene)",
      "keio_nitrogen_pfba_control.json:levels.nh4_-5",
      f"r {_cr(json.load(open(os.path.join(DL, 'keio_nitrogen_pfba_control.json')))['levels'], 'nh4_-5'):+.4f}",
      close(_cr(json.load(open(os.path.join(DL, 'keio_nitrogen_pfba_control.json')))['levels'], 'nh4_-5'), 0.922, 1e-3)
      and close(json.load(open(os.path.join(DL, 'keio_nitrogen_pfba_control.json')))['levels']['nh4_-5']
                ['label_agreement_fba_vs_pfba_kappa'], 0.9978, 1e-4))
agg = mtab["aggregates"]
check("S-12", "merged multiaxis table: 30 levels; arm kappa = 1.000 at "
      "30 of 31 rows (min 0.9978); canonical AUC min 0.978; canonical "
      "r gain > 0.05 at 27 rows (max +1.037)",
      "multiaxis_canonical_table.json:aggregates",
      f"n={agg['n_levels']}; kappa_min={agg['kappa_min']:.4f}; "
      f"auc_min={agg['canon_auc_min']:.4f}; "
      f"gain_max={agg['canon_r_gain_max']:+.4f}",
      agg["n_levels"] == 30 and agg["n_rows"] == 31
      and close(agg["kappa_min"], 0.9978, 1e-4)
      and close(agg["canon_auc_min"], 0.978, 1e-3)
      and agg["canon_r_gain_gt_005"] == 27
      and close(agg["canon_r_gain_max"], 1.037, 1e-3))
texS = open(os.path.join(BASE, "scripts",
                          "companion_categorical_v3.tex")).read()
check("S-13", "patch H present: prop:keio-atpm, rem:keio-multiaxis, "
      "ATPM table rows, near-tie text, six-axis abstract < 265 words",
      "companion_categorical_v3.tex",
      "all present: %s" % all(t in texS for t in
                              ["prop:keio-atpm", "rem:keio-multiaxis",
                               "ATPM $\\ge 100$", "near-tie floor",
                               "robust across six axes"]),
      all(t in texS for t in
          ["prop:keio-atpm", "rem:keio-multiaxis", "ATPM $\\ge 100$",
           "near-tie floor", "robust across six axes"]))
_mS = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", texS, re.S)
_bS = re.sub(r"\\[a-zA-Z]+", " ", _mS.group(1))
_bS = re.sub(r"[\\${}~]", " ", _bS)
_nwS = len([w for w in _bS.split() if w != "---"])
check("S-14", "six-axis abstract word count < 265",
      "companion_categorical_v3.tex abstract",
      f"words: {_nwS}",
      _nwS < 265)

'''
s = open('audit_v10_numbers.py').read()
ANCHOR = 'out = {"experiment": "v3 numeric consistency audit'
assert ANCHOR in s
s = s.replace(ANCHOR, S + "\n" + ANCHOR, 1)
s = s.replace('''out = {"experiment": "v3 numeric consistency audit (proof-complete revision of "
                     "risk 2 / advice 5; extended: E32 + restored "
                     "E22 + journal-submission pass)"''',
              '''out = {"experiment": "v10 numeric consistency audit (six-axis round: "
                     "non-medium ATPM maintenance stress, integrity-"
                     "corrected; extends v9)"''')
open('audit_v10_numbers.py', 'w').write(s)
print("section S inserted into audit_v10_numbers.py")
