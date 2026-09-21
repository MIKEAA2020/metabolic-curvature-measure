# =====================================================================
# V17. Insight-substantiation + worked-example round
# (download/v17_insight_substantiation.json by
# scripts/v17_insight_substantiation.py, commit 74934d0;
# download/v17_worked_example_verification.json by
# scripts/v17_worked_example_verify.py)
# =====================================================================
V17 = json.load(open(os.path.join(DL, "v17_insight_substantiation.json")))
VX = json.load(open(os.path.join(
    DL, "v17_worked_example_verification.json")))


def vfind(d, *path):
    for p in path:
        d = d[p]
    return d


# --- I. anatomy: regulon / operon enrichment + growth-silent partition
gs = {r["path"]: r for r in V17["I_menu_order"]["growth_silent_partition"]}
reg = {r["set"]: r for r in V17["I_menu_order"]["regulon"]["top_regulons"]}
ops = {r["set"]: r for r in V17["I_menu_order"]["operon"]["top_operons"]}
imo = {r["set"]: r for r in V17["I_menu_order"]["imodulon"]["top"]}
eff = V17["I_menu_order"]["regulon"]["effect_split"]
opd = V17["I_menu_order"]["operon"]

check("V17-I1", "top quartile = 110 of the 424 nonzero-kappa genes",
      "v17 json regulon.expected back-solve (crp)",
      round(reg["crp"]["expected"] * 424 / reg["crp"]["n_targets_in_bg"],
            4),
      close(reg["crp"]["expected"] * 424 /
            reg["crp"]["n_targets_in_bg"], 110, 1e-3) and
      "110" in tex2 and "$424$" in tex2)

reg_specs = [
    ("crp", 56, 89, 2.43, 2.8e-17, 8.6e-16),
    ("cra", 39, 52, 2.89, 1.8e-15, 2.8e-14),
    ("fur", 24, 27, 3.43, 1.6e-12, 1.5e-11),
    ("fnr", 46, 77, 2.30, 2.0e-12, 1.5e-11),
    ("rpoS", 26, 33, 3.04, 4.4e-11, 2.7e-10),
    ("fis", 22, 31, 2.74, 5.6e-8, 2.9e-7),
    ("arcA", 41, 89, 1.78, 2.6e-6, 1.1e-5),
    ("narL", 14, 20, 2.70, 2.9e-5, 1.1e-4),
    ("ihf", 21, 38, 2.13, 5.1e-5, 1.8e-4),
    ("rpoD", 86, 274, 1.21, 3.1e-4, 9.7e-4),
    ("nagC", 6, 8, 2.89, 4.8e-3, 1.3e-2),
]
for i, (nm, nin, ntgt, fold, p, q) in enumerate(reg_specs):
    check(f"V17-I2-{nm}", f"{nm} {nin}/{ntgt} fold {fold} q {q:g}",
          f"v17 json regulon.{nm}",
          (reg[nm]["n_in_top"], reg[nm]["n_targets_in_bg"],
           round(reg[nm]["fold"], 2), f"q={reg[nm]['p_bh']:.3g}"),
          reg[nm]["n_in_top"] == nin and
          reg[nm]["n_targets_in_bg"] == ntgt and
          round(reg[nm]["fold"], 2) == fold and
          close(reg[nm]["p"], p, 0.05) and
          close(reg[nm]["p_bh"], q, 0.05) and
          f"{nin} / {ntgt}" in tex2)

check("V17-I3", "eleven regulons survive BH q < 0.10",
      "v17 json regulon top_regulons",
      sum(r["p_bh"] < 0.10 for r in V17["I_menu_order"]["regulon"]
          ["top_regulons"]),
      sum(r["p_bh"] < 0.10 for r in V17["I_menu_order"]["regulon"]
          ["top_regulons"]) == 11 and
      "eleven regulons" in tex2)

check("V17-I4", "CRP activation split: median kappa 0.64 vs 0.02, "
      "MWU p = 0.0016; repression p = 0.43",
      "v17 json regulon.effect_split[0:2]",
      (round(eff[0]["median_kappa_targets"], 2),
       round(eff[0]["median_kappa_rest"], 2),
       round(eff[0]["MWU_p"], 4), round(eff[1]["MWU_p"], 2)),
      round(eff[0]["median_kappa_targets"], 2) == 0.64 and
      round(eff[0]["median_kappa_rest"], 2) == 0.02 and
      round(eff[0]["MWU_p"], 4) == 0.0016 and
      round(eff[1]["MWU_p"], 2) == 0.43 and "0.64" in tex2 and
      "0.0016" in tex2)

op_specs = [
    ("nuoABCEFGHIJKLMN", 13, 13, 4.3e-7),
    ("atpIBEFHAGDC", 9, 9, 6.4e-5),
    ("sdhCDAB-sucABCD", 8, 8, 1.8e-4),
    ("cyoABCDE", 4, 4, 3.4e-2),
    ("manXYZ", 3, 3, 7.6e-2),
    ("ptsHI-crr", 3, 3, 7.6e-2),
    ("pdhR-aceEF-lpd", 3, 3, 7.6e-2),
]
ok_ops = all(ops[nm]["n_in_top"] == nin and
             ops[nm]["n_targets_in_bg"] == ntgt and
             close(ops[nm]["p_bh"], q, 0.05)
             for nm, nin, ntgt, q in op_specs)
check("V17-I5", "operons nuo 13/13 (q 4.3e-07), atp 9/9, sdh-suc 8/8, "
      "cyo 4/4, manXYZ/ptsHI-crr/pdhR-aceEF-lpd 3/3 each",
      "v17 json operon.top_operons", "7 operon rows",
      ok_ops and "13$ of its $13$" in tex2 and "9$ of $9$" in tex2)

check("V17-I6", "seven operons BH q < 0.10; 31 testable; 31 regulons, "
      "18 iModulons testable",
      "v17 json operon + regulon + imodulon",
      (opd["n_operons_BH_lt_0.10"], opd["n_operons_tested"],
       V17["I_menu_order"]["regulon"]["n_regulons_tested"],
       V17["I_menu_order"]["imodulon"]["n_tested"]),
      opd["n_operons_BH_lt_0.10"] == 7 and
      opd["n_operons_tested"] == 31 and
      V17["I_menu_order"]["regulon"]["n_regulons_tested"] == 31 and
      V17["I_menu_order"]["imodulon"]["n_tested"] == 18 and
      "$31$ regulons, $31$ operons, $18$ iModulons" in tex2)

check("V17-I7", "intra-operon gap 0.044 vs inter 1.045 (381 pairs, "
      "perm p < 2e-4)", "v17 json operon gaps",
      (round(opd["intra_operon_mean_kappa_gap"], 3),
       round(opd["inter_operon_mean_kappa_gap"], 3),
       opd["n_intra_operon_pairs"], opd["permutation_p_gap_smaller"]),
      close(opd["intra_operon_mean_kappa_gap"], 0.044) and
      close(opd["inter_operon_mean_kappa_gap"], 1.045) and
      opd["n_intra_operon_pairs"] == 381 and
      opd["permutation_p_gap_smaller"] == 0.0 and
      "0.044" in tex2 and "1.045" in tex2 and "381" in tex2)

gprc = opd["gpr_control"]
check("V17-I8", "GPR control: 205 disjoint-reaction pairs gap 0.082; "
      "176 shared-reaction pairs trivially identical",
      "v17 json operon.gpr_control",
      (gprc["n_disjoint_reaction_pairs"],
       round(gprc["disjoint_pairs_mean_gap"], 3),
       gprc["n_shared_reaction_pairs"]),
      gprc["n_disjoint_reaction_pairs"] == 205 and
      close(gprc["disjoint_pairs_mean_gap"], 0.082) and
      gprc["n_shared_reaction_pairs"] == 176 and
      "205" in tex2 and "176" in tex2)

imo_specs = [("DhaR/Mlc", 5, 5), ("ArcA-1", 9, 13), ("Crp-2", 6, 7),
             ("ArcA-2", 4, 5)]
ok_imo = all(imo[nm]["n_in_top"] == nin and
             imo[nm]["n_targets_in_bg"] == ntgt
             for nm, nin, ntgt in imo_specs)
check("V17-I9", "iModulons DhaR/Mlc 5/5, ArcA-1 9/13, Crp-2 6/7, "
      "ArcA-2 4/5 (carbon/energy modules)",
      "v17 json imodulon.top", "4 module rows", ok_imo and
      "DhaR/Mlc" in tex2)

silent_ok = all(gs[p]["kappa_c_nonzero_genes"] == 0 and
                gs[p]["B2_c_attribution_n"] == 0
                for p in gs)
ratio_ok = (close(gs["P0_glucose_decline"]["value_over_flux_mass_ratio"],
                  1.45e-3, 0.05) and
            close(gs["P1_oxygen_limitation"]["value_over_flux_mass_ratio"],
                  2.4e-4, 0.05) and
            close(gs["P2_acetate_switch"]["value_over_flux_mass_ratio"],
                  5.5e-4, 0.05))
flux_ok = (close(gs["P0_glucose_decline"]["arm_A_flux_r"], 0.3954) and
           close(gs["P1_oxygen_limitation"]["arm_A_flux_r"], 0.3183) and
           close(gs["P2_acetate_switch"]["arm_A_flux_r"], 0.2234))
check("V17-I10", "growth-silent partition: kappa_c nonzero 0/433 on all "
      "three paths; value/flux mass ratios 1.45e-3, 2.4e-4, 5.5e-4",
      "v17 json growth_silent_partition",
      "3 paths, ratios (1.45e-3, 2.4e-4, 5.5e-4)",
      silent_ok and ratio_ok and flux_ok and
      "0$ of the $433$" in tex2 and "0.024" in tex2 and "0.145" in tex2)

trn = V17["I_menu_order"]["trn_metabolite_effectors"]
check("V17-I11", "237 TRN regulators, 5 with metabolite effectors "
      "(FMN, L-tryptophan, adenosylcobalamin, molybdopterin, spermidine)",
      "v17 json trn_metabolite_effectors",
      (trn["n_unique_regulators"], trn["n_metabolite_effector_regulators"],
       trn["examples"]),
      trn["n_unique_regulators"] == 237 and
      trn["n_metabolite_effector_regulators"] == 5 and
      trn["examples"] == ["FMN", "L-tryptophan", "adenosylcobalamin",
                          "molybdopterin", "spermidine"] and
      "237" in tex2 and "spermidine" in tex2)

# --- II. construction order
II = V17["II_construction_order"]
orr = II["order_rule"]
check("V17-II1", "order asymmetry q90 = 101.3 l1 vs WT total flux 770 "
      "(~13%)", "v17 json II chi_q90 + WT_L1",
      (round(II["chi_q90_nonSL"], 1),
       round(II["WT_L1_flux_full_glucose"], 0),
       round(100 * II["chi_q90_nonSL"] /
             II["WT_L1_flux_full_glucose"], 1)),
      close(II["chi_q90_nonSL"], 101.3) and
      close(II["WT_L1_flux_full_glucose"], 770) and
      close(100 * II["chi_q90_nonSL"] / II["WT_L1_flux_full_glucose"],
            13.1, 0.01) and "101.3" in tex2 and "$770$" in tex2)

check("V17-II2", "order rule: rho = 0.442 (p = 2.0e-4), sign 59/66 "
      "(binomial p = 2.4e-11), 66 loops",
      "v17 json II.order_rule",
      (round(orr["spearman_P_vs_A_rho"], 3),
       f"p={orr['spearman_P_vs_A_p']:.2g}", orr["same_sign_count"],
       f"binom={orr['binomial_p']:.2g}", orr["n_pairs_analyzed"]),
      close(orr["spearman_P_vs_A_rho"], 0.442) and
      close(orr["spearman_P_vs_A_p"], 2.0e-4, 0.05) and
      orr["same_sign_count"] == 59 and orr["n_pairs_analyzed"] == 66 and
      close(orr["binomial_p"], 2.4e-11, 0.05) and
      "$59$ of $66$" in tex2 and "0.442" in tex2)

check("V17-II3", "honest null: chi vs J_dR rho = 0.07 (p = 0.38)",
      "v17 json II spearman_chi_vs_JdR",
      (round(II["spearman_chi_vs_JdR_rho"], 2),
       round(II["spearman_chi_vs_JdR_p"], 2)),
      round(II["spearman_chi_vs_JdR_rho"], 2) == 0.07 and
      round(II["spearman_chi_vs_JdR_p"], 2) == 0.38 and "0.07" in tex2)

# --- III. memory substrate
III = V17["III_memory_substrate"]
e27 = III["e27_recomputed"]
check("V17-III1", "protein r = -0.083 (n 366), R2 = 0.007 (at most "
      "0.7% of variance); transcript subset r = +0.420 (n 365)",
      "v17 json III e27_recomputed + protein_layer_r2",
      (round(e27["protein_exhaustion"]["r"], 3),
       round(III["protein_layer_r2"], 4),
       round(e27["transcript_M3D_on_protein_subset"]["r"], 3),
       e27["transcript_M3D_on_protein_subset"]["n"]),
      close(e27["protein_exhaustion"]["r"], -0.083) and
      e27["protein_exhaustion"]["n"] == 366 and
      close(III["protein_layer_r2"], 0.007) and
      close(e27["transcript_M3D_on_protein_subset"]["r"], 0.420) and
      e27["transcript_M3D_on_protein_subset"]["n"] == 365 and
      "R^2 = 0.007" in tex2 and "+0.420" in tex2)

check("V17-III2", "kappa_mu locked metric: protein r = -0.098 (p 0.06), "
      "transcript r = +0.339", "v17 json III e27 kappa_mu arms",
      (round(e27["protein_exhaustion_kappa_mu"]["r"], 3),
       round(e27["transcript_M3D_kappa_mu"]["r"], 3)),
      round(e27["protein_exhaustion_kappa_mu"]["r"], 3) == -0.098 and
      round(e27["transcript_M3D_kappa_mu"]["r"], 3) == 0.339 and
      "-0.098" in tex2 and "0.339" in tex2)

# --- IV. wall coordinates
IV = V17["IV_wall_coordinates"]
check("V17-IV1", "50 reactions (1.8% of the network) carry 85.9% of "
      "curvature mass", "v17 json IV top_mass_branch_concentration",
      (round(IV["top_mass_branch_concentration"]["top50_mass_share"], 3),
       round(50 / 2719, 4)),
      close(IV["top_mass_branch_concentration"]["top50_mass_share"],
            0.859, 0.005) and
      close(50 / 2719, 0.018, 0.05) and "85.9" in tex2 and
      "1.8\\%" in tex2)

n11 = sum(1 for r in IV["top25_reactions"] if r["sweep_participation"] == 11)
check("V17-IV2", "23 of the 25 heaviest reactions participate in all "
      "eleven sweeps", "v17 json IV top25 sweep_participation", n11,
      n11 == 23 and "twenty-three of the twenty-five" in tex2)

top_r = {r["reaction"]: r["kappa_share"] for r in IV["top25_reactions"]}
check("V17-IV3", "heaviest reactions: PGI 3.7%, ATPS4rpp 3.5%, PFK/FBA "
      "3.3% each, PPP entry 3.2% each",
      "v17 json IV top25_reactions",
      (round(top_r["PGI"], 3), round(top_r["ATPS4rpp"], 3),
       round(top_r["PFK"], 3), round(top_r["G6PDH2r"], 3)),
      close(top_r["PGI"], 0.037, 0.01) and
      close(top_r["ATPS4rpp"], 0.035, 0.01) and
      close(top_r["PFK"], 0.033, 0.01) and
      close(top_r["G6PDH2r"], 0.032, 0.01) and
      "glucose-6-phosphate isomerase" in tex2)

m20 = IV["top20_branch_metabolites"]
sum20 = sum(r["curvature_mass_share"] for r in m20)
mtab = {r["base_id"]: r["curvature_mass_share"] for r in m20}
check("V17-IV4", "top-20 branch metabolites carry 59.7% of mass",
      "v17 json IV top20 sum", round(sum20, 3),
      close(sum20, 0.597, 0.005) and "59.7" in tex2)

wall_rows = [("f6p", "8.1"), ("g3p", "6.9"), ("g6p", "5.5"),
             ("dhap", "4.9"), ("pep", "4.5"), ("akg", "3.6"),
             ("pyr", "3.6"), ("coa", "3.6"), ("oaa", "2.1"),
             ("succ", "2.1")]
wall_map = [("f6p", 8.1), ("g3p", 6.9), ("g6p", 5.5), ("dhap", 4.9),
            ("pep", 4.5), ("akg", 3.6), ("pyr", 3.6), ("coa", 3.6),
            ("oaa", 2.1), ("succ", 2.1)]
ok_walls = all(close(mtab[b], pct / 100, 0.01) for b, pct in wall_map)
tab_ok = all(f"${s}\\%$" in tex2 for _, s in wall_rows)
check("V17-IV5", "wall-coordinate table shares (f6p 8.1, g3p 6.9, g6p "
      "5.5, dhap 4.9, pep 4.5, akg/pyr/coa 3.6, oaa/succ 2.1)",
      "v17 json IV top20_branch_metabolites",
      "10 table rows", ok_walls and tab_ok)

cur = IV["including_currency_d6"]
check("V17-IV6", "currency-inclusive: 98.6% of mass on branch/currency-"
      "adjacent reactions (85.8% of reactions)",
      "v17 json IV including_currency_d6",
      (round(cur["mass_share"], 3), round(cur["count_share"], 3)),
      close(cur["mass_share"], 0.986, 0.005) and
      close(cur["count_share"], 0.858, 0.005) and "98.6" in tex2)

check("V17-IV7", "reaction-level: 46.3% of reactions branch-adjacent "
      "carry 60.9% of mass (perm p 0.017); d*=16: 28.1% carry 50.6% "
      "(p 0.002); AUC ~ 0.5",
      "v17 json IV primary + sensitivity",
      (round(IV["branch_adjacent_reaction_count_share"], 3),
       round(IV["branch_adjacent_mass_share"], 3), IV["permutation_p"],
       round(IV["AUC"], 2)),
      close(IV["branch_adjacent_reaction_count_share"], 0.463) and
      close(IV["branch_adjacent_mass_share"], 0.609) and
      close(IV["permutation_p"], 0.017, 0.05) and
      close(IV["AUC"], 0.50, 0.01) and "46.3" in tex2 and "60.9" in
      tex2)

tmc = IV["top_mass_branch_concentration"]
check("V17-IV8", "of the fifty heaviest reactions, 56% branch-adjacent "
      "vs 46.3% baseline", "v17 json IV top_mass_branch_concentration",
      (tmc["top50_branch_fraction"],
       round(tmc["baseline_branch_fraction"], 3)),
      tmc["top50_branch_fraction"] == 0.56 and
      close(tmc["baseline_branch_fraction"], 0.463) and
      "56\\%" in tex2)

# --- V. interior architecture
V_ = V17["V_drift_free_interior"]
cls = {r["class"]: r for r in V_["class_stats"]}
check("V17-V1", "class shares: exchange 12.4% of reactions / 3.9% of "
      "mass / 92.6% flat; transport 32.7 / 20.7 / 90.4; internal "
      "54.9 / 75.4 / 74.3 (p 0.0012)",
      "v17 json V class_stats",
      "3 classes",
      all([close(cls["exchange"]["count_share"], 0.124),
           close(cls["exchange"]["curvature_mass_share"], 0.039),
           close(cls["exchange"]["flat_fraction"], 0.926),
           close(cls["transport"]["count_share"], 0.327),
           close(cls["transport"]["curvature_mass_share"], 0.207),
           close(cls["transport"]["flat_fraction"], 0.904),
           close(cls["internal"]["count_share"], 0.549),
           close(cls["internal"]["curvature_mass_share"], 0.754),
           close(cls["internal"]["flat_fraction"], 0.743),
           close(cls["internal"]["perm_p"], 0.0012, 0.05)]) and
      "12.4" in tex2 and "75.4" in tex2)

fam = V_["per_family_class_shares"]
check("V17-V2", "per-family internal mass share: nutrient 74.1%, "
      "knockdown 75.7%", "v17 json V per_family_class_shares",
      (round(fam["nutrient"]["internal"]["mass_share"], 3),
       round(fam["knockdown"]["internal"]["mass_share"], 3)),
      close(fam["nutrient"]["internal"]["mass_share"], 0.741) and
      close(fam["knockdown"]["internal"]["mass_share"], 0.757) and
      "74.1" in tex2 and "75.7" in tex2)

sub = {r["subsystem"]: r["mass_share"] for r in V_["top10_subsystems"]}
subsum = (sub["Glycolysis/Gluconeogenesis"] + sub["Pentose Phosphate Pathway"]
          + sub["Citric Acid Cycle"] + sub["Oxidative Phosphorylation"]
          + sub["Anaplerotic Reactions"])
check("V17-V3", "subsystems: gly 23.4%, PPP 19.7%, TCA 13.9%, OXPHOS "
      "11.6%, anaplerosis 4.7% (sum 73.3%)",
      "v17 json V top10_subsystems", round(subsum, 3),
      round(sub["Glycolysis/Gluconeogenesis"], 3) == 0.234 and
      round(sub["Pentose Phosphate Pathway"], 3) == 0.197 and
      round(sub["Citric Acid Cycle"], 3) == 0.139 and
      round(sub["Oxidative Phosphorylation"], 3) == 0.116 and
      round(sub["Anaplerotic Reactions"], 3) == 0.047 and
      round(subsum, 3) == 0.733 and "23.4" in tex2 and "19.7" in tex2)

check("V17-V4", "branch-adjacent reactions carry 74.4% of the internal "
      "mass", "v17 json V internal_flatness",
      round(V_["internal_flatness"]
            ["branch_adjacent_mass_share_within_internal"], 3),
      close(V_["internal_flatness"]
          ["branch_adjacent_mass_share_within_internal"], 0.744) and
      "74.4" in tex2)

oc = V_["ijo_glucose_one_chamber"]
sup = V_["ijo_active_support"]
check("V17-V5", "iJO glucose one-chamber: D2 total 6.5e-9, zero "
      "interior crossings; support 421-440 brackets 438",
      "v17 json V ijo_glucose_one_chamber + ijo_active_support",
      (f"{oc['D2_total']:.2g}", oc["v7_P0_interior_crossings"],
       sup["glucose_1"], sup["glucose_10"], sup["manuscript_E24_endpoint"]),
      close(oc["D2_total"], 6.5e-9, 0.05) and
      oc["v7_P0_interior_crossings"] == 0 and
      sup["glucose_1"] == 421 and sup["glucose_10"] == 440 and
      sup["manuscript_E24_endpoint"] == 438 and
      "$6.5 \\times 10^{-9}$" in tex2 and "421" in tex2 and "440" in tex2)

# --- worked example (machine-verified LP re-solves)
check("V17-EX1", "worked example: 16/16 machine checks pass (phases, "
      "jumps, coupling, kappa, tie-break variants)",
      "v17_worked_example_verification.json", 
      f"{VX['n_pass']} PASS / {VX['n_fail']} FAIL",
      VX["n_pass"] == 16 and VX["n_fail"] == 0 and
      "machine-verified by LP re-solves" in tex2)

kappa_ok = any(c["name"] == "D-kappa-g1" and c["value"] == "1.000000"
               for c in VX["checks"]) and \
    any(c["name"] == "D-kappa-g2" and c["value"] == "2.000000"
        for c in VX["checks"])
silent_ok2 = any(c["name"] == "E-silent-wall" and
                 abs(float(c["value"].split()[-1])) < 1e-6
                 for c in VX["checks"])
moves_ok = any(c["name"] == "E-kink-moves" and
               c["value"].startswith("jump -1.00") for c in VX["checks"])
check("V17-EX2", "worked example specifics: kappa(g1) = 1, kappa(g2) = 2; "
      "a=b wall silent (jump ~ 0); v2-first tie-break moves the kink",
      "v17_worked_example_verification.json", "D/E checks",
      kappa_ok and silent_ok2 and moves_ok and
      "$\\kmu(g_1) = 1$" in tex2 and "$\\kmu(g_2) = 2$" in tex2)

# --- front matter and refs
m_abs17 = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                    tex2, re.S)
stripped17 = re.sub(r"\\[a-zA-Z]+", " ", m_abs17.group(1))
nwords17 = len(re.findall(r"[A-Za-z0-9\-]+", stripped17))
check("V17-FM1", "abstract <= 255 audit-style words with the "
      "bio-anchoring sentences (regulons, fork metabolites, "
      "post-translational memory)",
      "journal_manuscript_v17.tex abstract", f"{nwords17} words",
      nwords17 <= 255 and "regulons" in m_abs17.group(1) and
      "fork metabolites" in m_abs17.group(1) and
      "post-translational" in m_abs17.group(1))

refs17 = open(os.path.join(BASE, "scripts",
              "journal_manuscript_v17_bmb_refs.tex")).read()
n17 = len(re.findall(r"\\bibitem", refs17))
check("V17-FM2", "refs: 29 entries with kacser1973 + heinrich1974 "
      "added; both cited in the body",
      "journal_manuscript_v17_bmb_refs.tex", f"{n17} entries",
      n17 == 29 and "kacser1973" in refs17 and
      "heinrich1974" in refs17 and
      "kacser1973" in tex2 and "heinrich1974" in tex2)

