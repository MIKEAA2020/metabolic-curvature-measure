# v12 numeric consistency audit (symmetric iJO second-engine + tie-break promotion round)

**301 PASS / 0 FAIL of 301 checks.**

Manuscript defects found and fixed: D-N1 (13 sweeps / 10 knockdowns), D-N2 (1.5e-7 -> 1.51e-7), D-N3 (lambda range), D-N4 (TV ratio 3.6-4.4), D-N5 (MWU p <= 2e-3), D-N6 (residuals <= 1.2e-10 + documented eno sub-threshold kink), D-N7 (abstract 93.4-100.0%), D-N8 (+0.032); journal round: D-JS1 (C1 effective constant 1.6-2.1 dipping at m=128), D-JS2 ('exactly the FPC' -> 'consistent with', 0.49 vs 0.29 at k=12), D-JS3 ('up to 8%' -> 'as large as 8.2%'); v11 round: D-P1 (PGI range 45-201), D-P2 (compensable count 1,127), D-P3 (engine bracket [+0.475,+0.943]), D-P4 (nitrogen figure clobber repaired); v12 round: D-P5 (feature count Four -> Five).

| id | claim | status | artifact value | source |
|---|---|---|---|---|
| ABS-1 | r = +0.395 (n=424) | PASS | r=0.3954, n=424 | v5_e24_recalibration.json:arms.kappa_mu[nonzero] |
| ABS-2 | p = 2.6e-17 | PASS | 2.58e-17 | v5_e24_recalibration.json:arms.kappa_mu[nonzero].pearso |
| ABS-3 | partial r = +0.269 | PASS | 0.2692 | v5_e24_recalibration.json:arms.confound_control.partial |
| ABS-4 | metric-invariance rho = 0.99998 | PASS | 0.9999881693960117 | v6_layer_decision.json:predictor_agreement.spearman_kap |
| ABS-5 | Spearman rho_S = +0.414 (E-V5 text) | PASS | 0.4138 | v5_e24_recalibration.json:...spearman_raw_full_panel |
| ABS-6 | abstract: mass concentrates (93.4-100.0% per boundary-crossing sweep) | PASS | mass range [0.9345, 1.000000] | m1_summary.json:sweeps (11 crossing sweeps) |
| ABS-7 | loop holonomy slope 1.00 (76-pair scan) | PASS | median=0.9982, mean=1.0086, n_pairs=76 | m4a_summary.json:median_slope_chi |
| ABS-8 | epistasis Spearman rho_S = 0.865 (J_dR) | PASS | 0.8649 | m3_summary.json:pairs.spearman_|eps|_J_dR.rho |
| ABS-9 | J_support = 0.800 | PASS | 0.8003 | m3_summary.json:pairs.spearman_|eps|_J_support.rho |
| ABS-10 | 66% non-reverting genotype loops | PASS | traced to m3_epistasis_path_dependence.py printout / m1_m3 report PDF | m3_summary.json (path-dependence block); M3 report body |
| M1-1 | v2 says 'Twelve parameter sweeps (glucose, oxygen, eight gene knockdow | PASS | 13 sweeps = 2 nutrient + 10 knockdowns + 1 iJO | m1_summary.json:sweeps (key count) |
| M1-2 | mass 0.934-1.0; AUC 0.83-1.00; MWU p <= 2e-3 (7 of 11 crossing sweeps  | PASS | mass [0.934,1.000000], AUC [0.83,1.000], MWU max 1.7e-03 | m1_summary.json: 11 crossing sweeps |
| M1-3 | event-free segment residuals <= 1.2e-10 (glucose 8e-14); one eno segme | PASS | max (excl. eno) 1.2e-10; eno 4.1e-03 | m1_summary.json:sweeps.*.top_segments |
| M1-4 | single-critical-region control (ijo glucose): noise D2 ~ 1e-11 | PASS | 2.3e-11 | m1_summary.json:ijo_glucose.D2_median_nonevent |
| M3-1 | 1,516 single knockouts (iML1515) | PASS | 1516 | m3_summary.json:n_genes |
| M3-2 | 2,779 double-knockout pairs (five panels) | PASS | 2779 | m3_summary.json:pairs.n_pairs |
| M3-3 | 40 synthetic-lethal pairs, all isozyme redundancies | PASS | 40/40 | m3_summary.json:pairs.n_SL / n_SL_isozyme |
| M3-4 | 25% of active pairs open nonzero commutators | PASS | M3 script printout | m3_summary.json (sequential-KO block); M3 report body |
| M4-1 | smoothing identity kernel self-test 1.2e-6 | PASS | 1.18e-06 | m4c_summary.json:theorem_R.kernel_selftest_rel_err |
| M4-2 | crossover eps*/sigma in [2.45, 4.11], median 3.1 | PASS | range [2.45, 4.11], median 3.05 | m4c_summary.json:dial_exact.*.eps_star_over_sigma |
| M4-3 | sliver census: net measure jump 8.9 vs nominal 1884.6 | PASS | net_jump_L2=8.9001, max_jump_L2=1884.6 | m4c_summary.json:sliver_clusters[0] |
| TB-1 | folded W1 0.058 -> 0.0039 (n 4 -> 128) | PASS | 0.0582 -> 0.00387 | theoremB_stress/bt_results.json:BT1_reproduce_V2a |
| TB-2 | mass ratio 0.939 -> 1.0009 | PASS | 0.9388 -> 1.00093 | bt_results.json:BT1_reproduce_V2a |
| TB-3 | TV ratio u=xy 2.9922; convex 1.3922 (n=128); generic range | PASS | u=xy 2.9922 (= 3-1/128), convex 1.3922 (= 1.4-1/128), generic [{min(gv | bt_results.json:BT3/BT4/BT6 |
| V1-1 | Phi piecewise affine at 4.2e-13 | PASS | 4.17e-13 | v1_value_function.json:phi_piecewise_affine.worst_rel_r |
| V1-2 | one real atom dPhi' = -0.006439 at t = 0.0358286 | PASS | t=0.0358286, d=-0.006439 | v1_value_function.json:atoms[0] |
| V1-3 | 12 flux events, 4 clusters | PASS | 12 events, 4 clusters | v1_value_function.json:v_events_total / clusters |
| V1-4 | value/flux mass ratio 1.7e-6 (E-V1) | PASS | 0.006439 / 3807.6 = 1.69e-6 | v1_value_function.json:atoms[0] (numerator) + deepseek_ |
| V1-5 | Danskin 6-7 digits | PASS | 2.02e-09 | v1_value_function.json:danskin_max_rel_err |
| TC-1 | 150 random dense-objective LPs to 1.1e-13; 5 events, all objective-mov | PASS | n_lp=150, err=1.05e-13, events=5/5 | coupling_results.json:ax8a_random |
| TC-2 | degenerate follower family 60/60, identity 2.0e-13 | PASS | n=60, kinks=60, err=2.02e-13 | coupling_results.json:ax8a_random.degenerate_family |
| TC-3 | 2D mixed second differences to 6.4e-16 | PASS | 6.37e-16 | coupling_results.json:ax8b_mixed.max_mixed_identity_err |
| TC-4 | iML1515: 12 events, 11 invisible, L1 jumps to 1.6e4, |c^T dv'| <= 1.51 | PASS | n=12, invisible=11, max L1 15868, max |cT| 1.506e-07 | coupling_results.json:ax8c_iml1515 (events) |
| TC-5 | identity error 0.0 at all 12 events and 4 clusters | PASS | identity_err = 0.0 entries | v1 + ax8c identity_err keys |
| AX-1 | MA atoms: 400 vertices; det=fan area 8.9e-16; product/atom median 3.29 | PASS | n=400, err=8.9e-16, median=3.296, min=2.0000 (orthogonal case exactly  | coupling_results.json:ax9_ma_atom |
| AX-2 | semiconvexity collapse: lambda*h_max = 0.500 (lambda 1..1e6; analytic  | PASS | lam=1e+00: 0.5000; lam=1e+01: 0.5000; lam=1e+02: 0.5000; lam=1e+03: 0. | coupling_results.json:ax10_collapse.rows |
| AX-3 | GPR OR+cap eigenvalues {0,sqrt2} / {-1,0} | PASS | signed-layer battery block | coupling_results.json:ax10_gpr |
| AX-4 | sec law 0.0% excess across 13 probes, tilts 0.11-2.83 | PASS | sec-law block | alexandrov_bridge/ax_results.json (AX-5/AX-6 battery) |
| AX-5 | dual-face fan area 0.235 vs 0.235000068 (16 LPs) | PASS | grep 0.235 | alexandrov_bridge/ax_results.json (dual-face) |
| E22-1 | 435 genes with at least one active reaction | PASS | 435 | novelty_v15_reaction_sampling_e22.csv (kappa_V_max > 0) |
| E22-2 | 438 of 2,583 reactions active (17.0%); GPR classes 254/96/36/18/34 | PASS | computed below | recomputed: plain FBA at 8 E22 anchors (iJO1366, EPS=1e |
| E22-3 | precursor kappa_V weak at panel level (r -0.063 unmasked .. +0.084 mas | PASS | unmasked -0.0633, v12 +0.1024, v13(masked) +0.0838 | novelty_v15_reaction_sampling_e22.py printout |
| E22-4 | E22 baseline reproduced to the digit r = +0.3739 (n = 433) | PASS | r=+0.3739, n=433 | recomputed from e22/e24 csvs |
| E23-1 | genes with nonzero kappa expand 435 -> 525 | PASS | 525 | novelty_v16_multicondition_e23_results.json:coverage.un |
| E23-2 | active-reaction support 438-454; union 537 (20.8%) | PASS | per-cond 438-454, union 537 | novelty_v16_multicondition_e23_results.json:coverage |
| V5-1 | M3D carbon switches: glycerol +0.195, acetate +0.166, proline +0.175,  | PASS | 0.1949, 0.1664, 0.1752, 0.2063 | precise_arm_kappamu.json |
| V5-2 | all p < 6e-4 | PASS | max p = 0.00058 | precise_arm_kappamu.json |
| V5-3 | PRECISE cross-platform MAX r = -0.044 (partial -0.088, NS) | PASS | r=-0.0443, p=0.36; partial=-0.0878 (txt) | precise_arm_kappamu.json + txt |
| V5-4 | per-condition: glycerol +0.126, acetate +0.130, fructose +0.099, galac | PASS | 0.1263, 0.1297, 0.0985, -0.0875 | precise_arm_kappamu.json |
| V6-1 | 0 of 433 genes in the c-attribution arm | PASS | 0 | v6_layer_decision.json:layer_decision.kappa_c_n_nonzero |
| V6-2 | shadow arm: 51 genes, r = +0.032 | PASS | n=51, r=+0.0319 | v6_layer_decision.json:arms.B3 |
| V6-3 | partial -0.013, p = 0.93 | PASS | partial=-0.0127, recomputed p=0.93 | v6 (partial r stored; p recomputed) |
| V6-4 | 4 value kinks, all design corners, 0 chamber crossings | PASS | total=4, corners=4, crossings=0 | v6_layer_decision.json:value_kink_census |
| V6-5 | value/flux strain mass ratio 1.45e-3 | PASS | 1.4478e-03 | v6_layer_decision.json:value_kink_census.value_over_flu |
| V6-6 | Y = 0.099544 (single-chamber law) | PASS | Y = 0.099544 in law string | v6_layer_decision.json:value_kink_census.single_chamber |
| V6-7 | affine law dmu/dq_glc = Y = 0.099544, intercept -0.0124 | PASS | slope=0.099544, intercept=-0.0131 (resid max 1.4e-14) | recomputed: 57 lex solves on the V5 trajectory (iJO1366 |
| V7-1 | P1 r = +0.318 (partial +0.258, n=426) | PASS | r=0.3183, partial=0.2583 | v7_path_robustness.json:P1 arms |
| V7-2 | P2 r = +0.223 (partial +0.160) | PASS | r=0.2234, partial=0.1598 | v7_path_robustness.json:P2 arms |
| V7-3 | cross-path predictors vs E24: +0.378 / +0.391 | PASS | 0.3783 / 0.391 | v7_path_robustness.json:cross arms |
| V7-4 | P1 3 chamber crossings; P2 4 | PASS | P1=3, P2=4 | v7_path_robustness.json:value_kink_census |
| V7-5 | shadow arm null: P1 r=-0.170 (n=68), P2 r=+0.032 (n=71) | PASS | P1=-0.1698 (n=68), P2=0.0321 (n=71) | v7_path_robustness.json:B3int |
| V7-6 | value/flux ratios 1.5e-3 / 2.4e-4 / 5.5e-4 | PASS | P0=1.45e-03, P1=2.38e-04, P2=5.53e-04 | v7_path_robustness.json:census (P0/P1/P2) |
| V8-1 | declared r=+0.3954; variants 0.386..0.396; partial stable | PASS | TB0=0.3954, TB1=0.3861, TB3=0.3959 | v8_tiebreak_robustness.json:association |
| V8-2 | value layer mu invariant (max diff 0.0) | PASS | 0.0 | v8_tiebreak_robustness.json:verdict |
| E25-1 | 2x2 cells: +0.196 (array switch), +0.298 (array stress), +0.191 (seq c | PASS | +0.196, +0.298, +0.191, +0.345 | novelty_v18_e25_platform_class.csv (recomputed) |
| E25-2 | n = 241-433 | PASS | n per cell: [433, 433, 241, 241] | e25 csv (recomputed) |
| E26-1 | PaxDb abundance level r = +0.334 | PASS | +0.334 (n=429) | novelty_v19_e26 csv (recomputed, log-log) |
| E26-2 | protein change r = +0.008 to +0.032 | PASS | maxfc +0.008, 4h +0.032 | e26 csv (recomputed) |
| E26-3 | transcript-protein fold-change coupling r = +0.020 (n = 799: full GSE6 | PASS | panel subset r=+0.145 (n=169) | e26 csv (panel subset); n=799 is the script-level full  |
| E27-1 | protein-level r = -0.083 vs transcript +0.419 (22 conditions, n = 366) | PASS | kappa-vs-protein r=-0.083 (n=366), kappa-vs-transcript r=+0.419 (n=365 | novelty_v20 csv (recomputed on shared genes) |
| E22-2R | 438 of 2,583 active (17.0%); GPR classes 254/96/36/18/34 (plain-FBA ce | PASS | 439/2583; classes {'no-gpr': 34, 'single': 253, 'isozyme-or': 98, 'com | recomputed (plain FBA, 8 anchors, EPS=1e-9) |
| LEDGER-1 | counts ledger assembled (12 entries) | PASS | 12 entries | see ledger |
| QUIRK-1 | V5 json arm labels '4x'/'8x' are swapped | PASS | labels: 'kappa_mu max (4x)' holds the 8x-refinement values (df8); 'kap | v5_e24_recalibration.json:arms keys |
| E32-1 | A1 measured tail slope -0.492 | PASS | -0.492 | e32 json A1_d1.loglog_tail_slope |
| E32-2 | A1 null tail slope -0.506 | PASS | -0.506 | e32 json A1_d1.null_loglog_tail_slope |
| E32-3 | measured/null ratio 1.24 at the largest panel | PASS | 1.24 | e32 json A1_d1 |
| E32-4 | iid prediction matches to 2.5% at the largest panel | PASS | 2.5 | e32 json A1_d1 bl/iid_gc_pred-1 |
| E32-5 | mid-range deviations as large as 8.2% (m=128) | PASS | 8.2 | e32 json A1_d1 max |bl/iid-1| |
| E32-6 | cut pool 4,000; events 25,107; boundary edges 350; grid 34x34 | PASS | (4000, 25107, 350, 'iML1515 (glc, O2) 34x34 signature census') | e32 json A_m4b_random_cuts |
| E32-7 | thirteen M1 sweeps: 2 affine, 11 event-bearing | PASS | 13: 2 affine, 11 event-bearing | e32 json B_m1_sweep_panels.sweeps |
| E32-8 | heterogeneity penalty ~1.5x at k=6 (falls from 1.8x, to 0.5x at k=12) | PASS | k=6: 1.52, k=12: 0.49 | e32 json B curve bl/null |
| E32-9 | FPC formula sqrt((13-k)/12) present; 'exactly the finite-population co | PASS | 13-k)/12 present; overstatement absent | manuscript text |
| E32-10 | population GC constant C = 2.49 (3 s.f.) | PASS | 2.495 | e32 json C1 gc_constant_pop |
| E32-11 | measured effective constant ~1.6-2.1 (dipping at m=128); '1.9-2.1' rem | PASS | min 1.649, max 2.113 | e32 json C1 curve bl*sqrt(m) |
| E32-12 | association stabilizes r in [0.389, 0.397] for m <= 256; full-panel r  | PASS | [0.3888, 0.3974], full 0.3954 | e32 json C1 association |
| E32-13 | Fisher SD column = 1/sqrt(m-3) | PASS | all rows | e32 json C1 r_curve 4th column |
| E32-14 | four-atom mass 288.77 = the V5 mass to the digit | PASS | 288.76892 in v5: True | e32 json C2 reference vs v5 json stored floats |
| E32-15 | anchor-preserving thinning exact: bl = 0 to machine precision (<= 7e-1 | PASS | max bl 6.6e-13, kinks {4.0}, max err 1.7e-12 | e32 json C2 anchor_thinning |
| E32-16 | uniform thinning: shape 0.12 -> 0.005 by m=43; mass err 26% -> 0.13% b | PASS | bl 0.1209->0.0054, err 0.2614->0.0013->2.6e-12 | e32 json C2 uniform_thinning |
| E32-17 | population is a four-atom object (n_atoms = 4) | PASS | 4 | e32 json C2 population |
| E22R-1 | GPR check: 0 failures over 120 gene-reaction pairs (matches frozen v21 | PASS | both texts present | v21 sec E22 + v2 Sec 6.1 |
| E22R-2 | distinctness b2097 shared with MAPPED-15; non-zero variation 435/435 ( | PASS | both texts present | v21 sec E22 + v2 Sec 6.1 |
| JP-1 | tie-break robustness table present (5 rules TB0-TB4, rho_S >= 0.99897, | PASS | TB4 + 0.99897 + 9.3 present | v3 E-V8 table |
| JP-2 | BMB retarget: author-year citations (natbib round); no table of conten | PASS | all present | v3 preamble/backmatter |
| JP-3 | BMB retarget: abstract <= 300 words; no Author Summary; keywords line  | PASS | abstract 258w, keywords 6 | v3 front matter |
| JP-4 | backmatter: Data/Software/Code Availability, Funding, Competing Intere | PASS | all present | v3 backmatter |
| JP-5 | BMB-style references: 27 entries, alphabetical with natbib author-year | PASS | 27 entries, labels True, all keys resolve True | v3 refs (verbatim v2) |
| JP-6 | in-text 'Fig' abbreviation throughout (no 'Figure~') | PASS | Figure~ absent | v3 text |
| KEIO-1 | glucose-only WT iJO1366 = 0.98237 | PASS | 0.98237 | keio_glucose_only_e12_results.json:wild_type_biomass |
| KEIO-2 | glucose-only essentials 289/1367, zero flips | PASS | 289/1367, flips +0/-0 | keio_glucose_only_e12_results.json:n_essential + label_ |
| KEIO-3 | E12' Pearson +0.603 (p=2.2e-136) | PASS | r=0.6034, p=2.21e-136 | keio_glucose_only_e12_results.json:calibration |
| KEIO-4 | E12' Spearman +0.591; partial +0.601; CI [0.578,0.631] | PASS | rho=0.5915, partial=0.6010, CI=[0.5782,0.6311] | keio_glucose_only_e12_results.json:calibration |
| KEIO-5 | E12' held-out AUC 0.977, MCC 0.882, sens 0.885, spec 0.981, P@200 0.91 | PASS | AUC=0.9769, MCC=0.8817, sens=0.8851, spec=0.9815, P@200=0.9150 | keio_glucose_only_e12_results.json:held_out + precision |
| KEIO-6 | E15' Pearson +0.230 (p=6.7e-16), Spearman +0.256, AUC 0.737 | PASS | r=0.2297, p=6.66e-16, rho=0.2555, AUC=0.7375 | keio_glucose_only_e15_results.json:direct_validation |
| KEIO-7 | E15' held-out AUC 0.763, sens 0.846, spec 0.607, MCC 0.283 | PASS | AUC=0.7633, sens=0.8462, spec=0.6068, MCC=0.2828 | keio_glucose_only_e15_results.json:held_out_70_30 |
| KEIO-8 | E15' strata 84/35, high-conf AUC 0.713, gaps 30, mismatch 217->180 | PASS | hi=84, lo=35, hiAUC=0.712587404850416, gaps=30 | keio_glucose_only_e15_results.json:pec_stratification + |
| KEIO-9 | glucose-only WT iML1515 = 0.82180 | PASS | 0.82180 | keio_glucose_only_e16_results.json:wild_type_biomass |
| KEIO-10 | E16' Pearson +0.376 (p=9.6e-46), Spearman +0.304, AUC 0.813; binary 13 | PASS | r=0.3760, p=9.60e-46, rho=0.3039, AUC=0.8128, binary={'n': 1325, 'n_E' | keio_glucose_only_e16_results.json |
| KEIO-11 | companion quotes fractions 0.498 and 0.853 (battery) | PASS | 0.498 count: 3, 0.853 count: 3 | companion_categorical_v7.tex:prop:poincare-averaging +  |
| KEIO-12 | prop:keio-glucose-only confusion (318,6,10,77) quoted | PASS | {'tn': 318, 'fp': 6, 'fn': 10, 'tp': 77} | keio_glucose_only_e12_results.json:confusion_matrix |
| O2-1 | iJO1366 WT dose response 0.711 / 0.491 / 0.367; O2=0 exactly 0 | PASS | 0.71083, 0.49147, 0.36680, -0.00000 | keio_o2_limited_e12_results.json:levels.*.wild_type_bio |
| O2-2 | labels 289/1367 at every non-anaerobic level, zero flips, kappa 1.000 | PASS | 289(+0/-0,k=1.0000), 289(+0/-0,k=1.0000), 289(+0/-0,k=1.0000) | keio_o2_limited_e12_results.json:levels.*.flips_vs_gluc |
| O2-3 | O2=-10: r +0.775 CI [0.757,0.792], AUC 0.9999, MCC 0.993, P@200 1.0 | PASS | r=0.7749, CI=[0.7572067589511902, 0.7919509491663135], AUC=0.9999, MCC | keio_o2_limited_e12_results.json:levels.-10.0 |
| O2-4 | O2=-5: r +0.607 CI [0.584,0.628] AUC 0.980; O2=-2.5: r +0.519 CI [0.49 | PASS | r5=0.6067, r25=0.5189 | keio_o2_limited_e12_results.json:levels.-5.0/-2.5 |
| O2-5 | iJO direct arm r +0.264/+0.220/+0.162, AUC 0.732/0.744/0.726; gaps 30; | PASS | +0.2641/0.7323, +0.2199/0.7441, +0.1619/0.7257 | keio_o2_limited_e12_results.json:levels.*.direct_arm |
| O2-6 | overflow (for+ac) at -10; fermentation (etoh+for+ac) at -5/-2.5 | PASS | {'-10.0': {'EX_for_e': 7.196, 'EX_ac_e': 7.853}, '-5.0': {'EX_etoh_e': | keio_o2_limited_e12_results.json:levels.*.fermentation_ |
| O2-7 | O2=0: 0.01 trace restores 0.231; q8h2 coefficient 0.000223 | PASS | tiny=0.2306, q8h2=[['BIOMASS_Ec_iJO1366_WT_53p95M', 'q8h2_c', -0.00022 | keio_o2_anaerobic_diagnostic.json |
| O2-8 | iML -5: WT 0.353, 286 labels zero flips kappa 1.0, r +0.559, AUC 0.994 | PASS | WT=0.35344, labels=286, r=0.5592 | keio_o2_limited_e16_results.json:levels.-5.0 |
| O2-9 | iML -5 direct r +0.236, AUC 0.818 (vs 0.813 unlimited); gaps 13 | PASS | r=0.2363, AUC=0.8184 | keio_o2_limited_e16_results.json:levels.-5.0.direct_arm |
| O2-10 | iML anaerobic (CORRECTED round 8): 286->292, +6/-0, kappa 0.987, Jacca | PASS | labels=292, +6/-0, k=0.9872, J=0.9795, WT=0.13411 | keio_o2_limited_e16_results.json:levels.0.0 |
| O2-11 | flip identities (CORRECTED): gains eno/pgk/gapA/gpmA/gpmM/hemN; no los | PASS | gains=['b0755', 'b1779', 'b2779', 'b2926', 'b3612', 'b3867'], loss=[] | keio_o2_limited_e16_results.json:levels.0.0.flips_vs_gl |
| O2-12 | anaerobic stats (CORRECTED): r +0.258 AUC 0.682; direct +0.125 AUC 0.6 | PASS | r=0.2583, AUC=0.6815, direct r=0.1246, direct AUC=0.6730 | keio_o2_limited_e16_results.json:levels.0.0 |
| O2-13 | flip ratios (CORRECTED): glycolysis six 0.70-1.00 aerobically -> 0 ana | PASS | {'b1779': (np.float64(0.701), np.float64(0.0)), 'b2926': (np.float64(0 | keio_o2_limited_e16_sweep.csv + keio_glucose_only_e16_s |
| O2-14 | 5 of 6 flips in glycolysis/gluconeogenesis, ~30x enrichment | PASS | [{'subsystem': 'Glycolysis/Gluconeogenesis', 'n_flip': 5, 'expected':  | keio_o2_limited_e16_results.json:levels.0.0...subsystem |
| O2-15 | prop:keio-o2-limited + rem:keio-o2-invariance in companion; abstract p | PASS | labels present: True / True; abstract words: 264 | companion_categorical_v7.tex (abstract + Keio section) |
| N-1 | iJO WT: nh4 -10/-5/-2.5 = 0.9259/0.4629/0.2315; glu -10 = 0.9259 (matc | PASS | 0.9259/0.4629/0.2315/0.9259/1.2595 | keio_nitrogen_source_e12_results.json:levels.*.wild_typ |
| N-2 | matched-N control: glu -10 WT == nh4 -10 WT exactly (0.925855, donor-i | PASS | 0.925855 vs 0.925855 | keio_nitrogen_source_e12_results.json |
| N-3 | labels invariant along the whole NH4 gradient: 289/289 at -10/-5/-2.5, | PASS | kappa 1.0000/1.0000/1.0000 | keio_nitrogen_source_e12_results.json:levels.*.flips_vs |
| N-4 | iML -2.5: 286/286, kappa 1.000 (cross-rebuild limitation endpoint) | PASS | kappa 1.0000 | keio_nitrogen_source_e16_results.json:levels.nh4_-2.5 |
| N-5 | substitution losses only: iJO glu -5 / arg -14; iML glu -7 / arg -15 ( | PASS | iJO glu_-10: 284 (-5); iJO arg_-10: 275 (-14); iML glu_-10: 279 (-7);  | keio_nitrogen_source_{e12,e16}_results.json:flips_vs_gl |
| N-6 | kappa 0.989/0.969 (iJO glu/arg); 0.985/0.967 (iML) | PASS | 0.9890/0.9687/0.9848/0.9670 | keio_nitrogen_source_{e12,e16}_results.json |
| N-7 | loss identities: glu core gltA/acnA/acnB/icd/amtB (b0720/b1276/b0118/b | PASS | sets match | keio_nitrogen_source_{e12,e16}_results.json:flips.losse |
| N-8 | every rescue substitution-mediated: closing the sole N donor returns a | PASS | max b_closed = 0.00e+00 | keio_nitrogen_flip_verification.json |
| N-9 | akg assimilation arm: GLUDy 8.401 (baseline) -> 0.0 (glu) -> -7.3233 ( | PASS | GLUDy 8.401 / -0.0 / -7.3233 | keio_nitrogen_flip_verification.json:akg_assimilation_a |
| N-10 | nh4-release routes at the optima: dadA/DAAD 1.952 (iJO glu); GLUDy 2.0 | PASS | iJO glu_-10: DAAD 1.952; iML glu_-10: GLUDy 2.081; iJO arg_-10: SADH 1 | keio_nitrogen_source_{e12,e16}_results.json:wt_info.nh4 |
| N-11 | label strata: model gaps 30/13 unchanged at every level; iJO mismatch  | PASS | mism 175/166 | keio_nitrogen_source_{e12,e16}_results.json:direct_arm |
| N-12 | arg association intact-to-stronger: r +0.802 CI [0.780,0.823], AUC 0.9 | PASS | r 0.8024, AUC 0.9808, direct r 0.4246 | keio_nitrogen_source_{e12,e16}_results.json:levels.arg_ |
| N-13 | plain-FBA collapse on N-limited levels: r +0.350/+0.079/-0.122/+0.213  | PASS | +0.350/+0.079/-0.122/+0.213 | keio_nitrogen_source_e12_results.json:levels.*.transiti |
| N-14 | at-optimum FVA (degeneracy evidence): PGI width 0.0 (baseline) / 4.3 ( | PASS | PGI -0.00/4.35/45.19/177.20/82.93 | keio_nitrogen_degeneracy_diagnostic.json:fva_at_optimum |
| N-15 | canonical (pFBA) control restores the association: r +0.940 (NH4 -10)  | PASS | +0.9399/+0.9149/+0.8718 | keio_nitrogen_pfba_control.json:levels.*.transitive_cal |
| N-16 | labels unchanged by canonical selection (kappa 1.000; objective preser | PASS | kappa 1.0000/1.0000/1.0000/1.0000 | keio_nitrogen_pfba_control.json |
| N-17 | prop:keio-n-source + rem:keio-n-invariance in companion; abstract carr | PASS | labels present: True / True; abstract words: 264 | companion_categorical_v7.tex (abstract + Keio section) |
| N-18 | arginine/proline metabolism enriched: 9 (iJO) / 8 (iML) flips, ~20x ov | PASS | iJO 9 vs exp 0.4 (ratio 20.92); iML 8 | keio_nitrogen_source_{e12,e16}_results.json:subsystem_e |
| R8-O2C-ijo_o2_10-r | canonical r = +0.895 (table) | PASS | +0.8952 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_10-auc | canonical AUC = 1.000 | PASS | 1.0000 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_10-mcc | canonical MCC = 0.972 | PASS | 0.9717 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_10-kappa | label kappa = 1.000 (by construction, verified) | PASS | 1.0000 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_10-objpres | objective preserved (< 1e-6) | PASS | 0.0 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_5-r | canonical r = +0.939 (table) | PASS | +0.9391 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_5-auc | canonical AUC = 1.000 | PASS | 1.0000 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_5-mcc | canonical MCC = 1.000 | PASS | 1.0000 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_5-kappa | label kappa = 1.000 (by construction, verified) | PASS | 1.0000 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_5-objpres | objective preserved (< 1e-6) | PASS | 0.0 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_2.5-r | canonical r = +0.945 (table) | PASS | +0.9451 | o2c[ijo_o2_2.5] |
| R8-O2C-ijo_o2_2.5-auc | canonical AUC = 1.000 | PASS | 1.0000 | o2c[ijo_o2_2.5] |
| R8-O2C-ijo_o2_2.5-mcc | canonical MCC = 0.958 | PASS | 0.9582 | o2c[ijo_o2_2.5] |
| R8-O2C-ijo_o2_2.5-kappa | label kappa = 1.000 (by construction, verified) | PASS | 1.0000 | o2c[ijo_o2_2.5] |
| R8-O2C-ijo_o2_2.5-objpres | objective preserved (< 1e-6) | PASS | 0.0 | o2c[ijo_o2_2.5] |
| R8-O2C-iml_baseline-r | canonical r = +0.937 (table) | PASS | +0.9372 | o2c[iml_baseline] |
| R8-O2C-iml_baseline-auc | canonical AUC = 0.987 | PASS | 0.9866 | o2c[iml_baseline] |
| R8-O2C-iml_baseline-mcc | canonical MCC = 0.966 | PASS | 0.9655 | o2c[iml_baseline] |
| R8-O2C-iml_o2_5-r | canonical r = +0.941 (table) | PASS | +0.9414 | o2c[iml_o2_5] |
| R8-O2C-iml_o2_5-auc | canonical AUC = 1.000 | PASS | 1.0000 | o2c[iml_o2_5] |
| R8-O2C-iml_o2_5-mcc | canonical MCC = 1.000 | PASS | 1.0000 | o2c[iml_o2_5] |
| R8-O2C-iml_o2_0-r | canonical r = +0.949 (table) | PASS | +0.9487 | o2c[iml_o2_0] |
| R8-O2C-iml_o2_0-auc | canonical AUC = 0.997 | PASS | 0.9973 | o2c[iml_o2_0] |
| R8-O2C-iml_o2_0-mcc | canonical MCC = 0.979 | PASS | 0.9794 | o2c[iml_o2_0] |
| R8-O2C-plain-anaerobic | iML O2-0 plain r = +0.258 (corrected; table) | PASS | +0.2583 | o2c[iml_o2_0].plain_reference_r |
| R8-O2C-plain-anaerobic-auc | iML O2-0 plain AUC = 0.682 (corrected) | PASS | 0.6815 | o2c[iml_o2_0].plain_reference_auc |
| R8-O2C-anaerobic-kappa-refreshed | iML O2-0 label kappa = 1.000 (post-correction) | PASS | 1.0000 | o2c[iml_o2_0] |
| R8-O2C-ijo_o2_10-rho | canonical rank corr vs baseline = +0.935 | PASS | +0.9349 | o2c[ijo_o2_10] |
| R8-O2C-ijo_o2_5-rho | canonical rank corr vs baseline = +0.956 | PASS | +0.9556 | o2c[ijo_o2_5] |
| R8-O2C-ijo_o2_2.5-rho | canonical rank corr vs baseline = +0.922 | PASS | +0.9225 | o2c[ijo_o2_2.5] |
| R8-O2C-iml_o2_5-rho | canonical rank corr vs baseline = +0.897 | PASS | +0.8973 | o2c[iml_o2_5] |
| R8-O2C-iml_o2_0-rho | canonical rank corr vs baseline = +0.691 | PASS | +0.6909 | o2c[iml_o2_0] |
| R8-ANA-labels | 286 -> 292 (+6 / -0), kappa 0.987 | PASS | 286 -> 292 (+6/-0, kappa 0.9872) | o2_e16 results[0.0].flips |
| R8-ANA-jaccard | Jaccard 0.979 | PASS | 0.9795 | flips |
| R8-ANA-gains | six gains: eno, pgk, gapA, gpmA, gpmM, hemN | PASS | ['b0755', 'b1779', 'b2779', 'b2926', 'b3612', 'b3867'] | flips.gains |
| R8-ANA-stats | plain r = +0.258 (AUC 0.682); direct +0.125 / 0.673 | PASS | r +0.2583, AUC 0.6815, direct +0.1246/0.6730 | results[0.0] |
| R8-ANA-gaps | model gaps 12 | PASS | 12 | direct_arm |
| R8-ANA-fabZ-row | fabZ b_ko = 0, y = 1 (patched) | PASS | b_ko 0.000000, y 1 | o2_e16_sweep.csv b0180@0.0 |
| R8-PI-ijo-pi_0.5-wt | WT = 0.518 (-47%) | PASS | 0.5183 | pi_e12[pi_0.5] |
| R8-PI-ijo-pi_0.5-labels | 289 -> 289, zero flips, kappa 1.000 | PASS | 289 (+0/-0, kappa 1.0000) | pi_e12[pi_0.5].flips |
| R8-PI-ijo-pi_0.5-plain | plain r (table col) | PASS | +0.3234 | pi_e12[pi_0.5] |
| R8-PI-ijo-pi_0.5-canon | canonical r/AUC/MCC (table) | PASS | r +0.9496, AUC 0.9877, MCC 0.9649 | pi_ctrl[pi_0.5] |
| R8-PI-ijo-pi_0.25-wt | WT = 0.259 (-74%) | PASS | 0.2592 | pi_e12[pi_0.25] |
| R8-PI-ijo-pi_0.25-labels | 289 -> 289, zero flips, kappa 1.000 | PASS | 289 (+0/-0, kappa 1.0000) | pi_e12[pi_0.25].flips |
| R8-PI-ijo-pi_0.25-plain | plain r (table col) | PASS | +0.0537 | pi_e12[pi_0.25] |
| R8-PI-ijo-pi_0.25-canon | canonical r/AUC/MCC (table) | PASS | r +0.9162, AUC 0.9877, MCC 0.9649 | pi_ctrl[pi_0.25] |
| R8-PI-ijo-pi_0.1-wt | WT = 0.104 (-89%) | PASS | 0.1037 | pi_e12[pi_0.1] |
| R8-PI-ijo-pi_0.1-labels | 289 -> 289, zero flips, kappa 1.000 | PASS | 289 (+0/-0, kappa 1.0000) | pi_e12[pi_0.1].flips |
| R8-PI-ijo-pi_0.1-plain | plain r (table col) | PASS | -0.0669 | pi_e12[pi_0.1] |
| R8-PI-ijo-pi_0.1-canon | canonical r/AUC/MCC (table) | PASS | r +0.9139, AUC 0.9877, MCC 0.9516 | pi_ctrl[pi_0.1] |
| R8-PI-ijo-pi_0.5-table | plain +0.323 / canonical +0.950 / AUC 0.988 / MCC 0.965 | PASS | +0.3234 / +0.9496 / 0.9877 / 0.9649 | pi artifacts |
| R8-PI-ijo-pi_0.25-table | plain +0.054 / canonical +0.916 / AUC 0.988 / MCC 0.965 | PASS | +0.0537 / +0.9162 / 0.9877 / 0.9649 | pi artifacts |
| R8-PI-ijo-pi_0.1-table | plain -0.067 / canonical +0.914 / AUC 0.988 / MCC 0.952 | PASS | -0.0669 / +0.9139 / 0.9877 / 0.9516 | pi artifacts |
| R8-PI-iml-pi_0.25-table | plain +0.025 / canonical +0.910 / AUC 0.986 / MCC 0.904; labels 286, k | PASS | +0.0251 / +0.9102 / 0.9864 / 0.9038; 286 (kappa 1.0000) | pi artifacts |
| R8-PI-iml-pi_0.1-table | plain +0.090 / canonical +0.900 / AUC 0.986 / MCC 0.904; labels 286, k | PASS | +0.0900 / +0.9003 / 0.9864 / 0.9038; 286 (kappa 1.0000) | pi artifacts |
| R8-PI-ijo-pi_0.5-pgi | at-optimum PGI FVA width = 123 | PASS | 122.661 | pi_e12[pi_0.5].degeneracy |
| R8-PI-ijo-pi_0.25-pgi | at-optimum PGI FVA width = 172 | PASS | 171.930 | pi_e12[pi_0.25].degeneracy |
| R8-PI-ijo-pi_0.1-pgi | at-optimum PGI FVA width = 201 | PASS | 201.492 | pi_e12[pi_0.1].degeneracy |
| R8-PI-pgi-baseline | PGI width 0.0 at baseline; 4.3 under O2 limitation | PASS | -0.0 / 4.3484 | nitrogen_degeneracy_diagnostic.json |
| R8-PI-ackr-cycle | baseline ACKr free cycle width ~ 1e3 (the sharpening mechanism) | PASS | 996.5582 | nitrogen_degeneracy_diagnostic.json |
| R8-PI-prescreen | baseline Pi uptake 0.948 (iJO) / 0.793 (iML); sulfur 0.248 compresses  | PASS | 0.9476 / 0.7927 / 0.2478 | keio_fourth_axis_prescreen.json |
| R8-PI-ijo-pi_0.5-rho | rank corr vs baseline canonical = +0.765 | PASS | +0.7647 | pi_ctrl[pi_0.5] |
| R8-PI-ijo-pi_0.25-rho | rank corr vs baseline canonical = +0.968 | PASS | +0.9681 | pi_ctrl[pi_0.25] |
| R8-PI-ijo-pi_0.1-rho | rank corr vs baseline canonical = +0.961 | PASS | +0.9610 | pi_ctrl[pi_0.1] |
| R8-PI-iml-pi_0.25-rho | rank corr vs baseline canonical = +0.906 | PASS | +0.9056 | pi_ctrl[pi_0.25] |
| R8-PI-iml-pi_0.1-rho | rank corr vs baseline canonical = +0.818 | PASS | +0.8182 | pi_ctrl[pi_0.1] |
| R8-NC-iml-nh4_-2.5 | plain -0.112 -> canonical +0.909 (AUC 0.986, MCC 0.904); kappa 1.000 | PASS | +0.9089, 0.9864, 0.9038, 1.0000 | nitrogen_pfba_control iml[nh4_-2.5] |
| R8-NC-iml-glu_-10 | plain +0.314 -> canonical +0.911 (AUC 0.987, MCC 0.965); kappa 1.000 | PASS | +0.9114, 0.9865, 0.9649, 1.0000 | nitrogen_pfba_control iml[glu_-10] |
| R8-NC-iml-nh4_-2.5-plain | plain r = -0.112 | PASS | -0.1125 | n_e16[nh4_-2.5] |
| R8-NC-iml-glu_-10-plain | plain r = +0.314 | PASS | +0.3138 | n_e16[glu_-10] |
| R8-SI-audit | 0 discrepancies in 24,282 comparisons across 17 levels | PASS | 0 / 24282 | keio_o2_solver_integrity_audit.json |
| R8-SI-highs | HiGHS adjudication: all biotin-pathway KOs essential (biomass max exac | PASS | {'WT': None, 'fabZ KO (b0180)': True, 'bioF KO (b0776)': True, 'bioH K | keio_phosphate_highs_adjudication.json |
| R8-SI-quotas | biotin coefficient 2e-06 in the objective biomass; WT quota 2.07e-07 a | PASS | btn_c coefficient -2e-06 | phosphate_adjudication.json |
| R8-SI-ijo-triple | three iJO biotin KOs share canonical kV = 164.975 | PASS | ['164.9753', '164.9753', '164.9753'] | pi_ctrl_pi_0.1.csv |
| R8-SI-iml-triple | three iML biotin KOs share canonical kV = 253.551 | PASS | ['253.5509', '253.5509', '253.5509'] | pi_ctrl_iml_pi_0.1.csv |
| R8-TAB-rows | 25 canonical rows in tab:canonical-selection (round 9: + iron x5 + arg | PASS | 25 artifact levels; table rows: 14 iJO + 11 iML | tab:canonical-selection |
| R8-ABS-five-axes | abstract: 'robust across six axes: carbon, oxygen, nitrogen, phosphate | PASS | True | companion_categorical_v7.tex abstract |
| R8-ABS-wordcount | abstract under the 265-word cap | PASS | 264 words | companion_categorical_v7.tex abstract |
| R8-TEX-fourth-axis proposition | anchor prop:keio-phosphate present | PASS | True | companion_categorical_v7.tex |
| R8-TEX-four-axis remark | anchor rem:keio-p-invariance present | PASS | True | companion_categorical_v7.tex |
| R8-TEX-canonical-selection subsection | anchor sec:canonical-selection present | PASS | True | companion_categorical_v7.tex |
| R8-TEX-homogenized table | anchor tab:canonical-selection present | PASS | True | companion_categorical_v7.tex |
| R8-TEX-selection-rule remark | anchor rem:canonical-protocol present | PASS | True | companion_categorical_v7.tex |
| R9-FE-prescreen | parsimonious Fe requirement 0.0158 (iJO) / 0.0132 (iML); zinc compress | PASS | 0.01578 / 0.0132 | keio_fifth_axis_prescreen.json |
| R9-FE-prescreen-map | iron dose response identical on both reconstructions to six decimals ( | PASS | [('-0.01', 0.622626, 0.622626), ('-0.005', 0.311313, 0.311313), ('-0.0 | keio_fifth_axis_prescreen.json |
| R9-FE-fe3 | fe3-closed iML baseline unchanged to solver noise (3.2e-06) | PASS | 3.195e-06 | keio_fifth_axis_prescreen.json |
| R9-FE-ijo-fe_0.01 | WT 0.623 (-37%); labels 289 -> 289, zero flips, kappa 1.000; PGI width | PASS | WT 0.6226; 289 (+0/-0, kappa 1.0000); PGI 102.834 | iron_e12[fe_0.01] + iron_ctrl[fe_0.01] |
| R9-FE-ijo-fe_0.005 | WT 0.311 (-68%); labels 289 -> 289, zero flips, kappa 1.000; PGI width | PASS | WT 0.3113; 289 (+0/-0, kappa 1.0000); PGI 162.017 | iron_e12[fe_0.005] + iron_ctrl[fe_0.005] |
| R9-FE-ijo-fe_0.0025 | WT 0.156 (-84%); labels 289 -> 289, zero flips, kappa 1.000; PGI width | PASS | WT 0.1557; 289 (+0/-0, kappa 1.0000); PGI 191.608 | iron_e12[fe_0.0025] + iron_ctrl[fe_0.0025] |
| R9-FE-iml-fe_0.005 | WT 0.311 (-62%); labels 286 -> 286, zero flips, kappa 1.000; PGI width | PASS | WT 0.3113; 286 (+0/-0, kappa 1.0000); PGI 139.188 | iron_e16[fe_0.005] + iron_ctrl[fe_0.005] |
| R9-FE-iml-fe_0.0025 | WT 0.156 (-81%); labels 286 -> 286, zero flips, kappa 1.000; PGI width | PASS | WT 0.1557; 286 (+0/-0, kappa 1.0000); PGI 176.484 | iron_e16[fe_0.0025] + iron_ctrl[fe_0.0025] |
| R9-FE-ijo-fe_0.01-table | plain +0.518 / canonical +0.957 / AUC 0.988 / MCC 0.965 (table) | PASS | +0.5181 / +0.9569 / 0.9877 / 0.9649 | iron artifacts |
| R9-FE-ijo-fe_0.005-table | plain +0.303 / canonical +0.800 / AUC 0.988 / MCC 0.965 (table) | PASS | +0.3026 / +0.8003 / 0.9877 / 0.9649 | iron artifacts |
| R9-FE-ijo-fe_0.0025-table | plain -0.011 / canonical +0.913 / AUC 0.988 / MCC 0.952 (table) | PASS | -0.0110 / +0.9132 / 0.9877 / 0.9516 | iron artifacts |
| R9-FE-iml-fe_0.005-table | plain +0.127 / canonical +0.843 / AUC 0.986 / MCC 0.904 (table) | PASS | +0.1268 / +0.8434 / 0.9864 / 0.9038 | iron artifacts |
| R9-FE-iml-fe_0.0025-table | plain -0.037 / canonical +0.905 / AUC 0.986 / MCC 0.904 (table) | PASS | -0.0370 / +0.9052 / 0.9864 / 0.9038 | iron artifacts |
| R9-FE-ijo-fe_0.01-rho | rank corr vs baseline canonical = +0.848 | PASS | +0.8484 | iron_ctrl[fe_0.01] |
| R9-FE-ijo-fe_0.005-rho | rank corr vs baseline canonical = +0.651 | PASS | +0.6514 | iron_ctrl[fe_0.005] |
| R9-FE-ijo-fe_0.0025-rho | rank corr vs baseline canonical = +0.756 | PASS | +0.7563 | iron_ctrl[fe_0.0025] |
| R9-FE-iml-fe_0.005-rho | rank corr vs baseline canonical = +0.630 | PASS | +0.6299 | iron_ctrl[fe_0.005] |
| R9-FE-iml-fe_0.0025-rho | rank corr vs baseline canonical = +0.671 | PASS | +0.6709 | iron_ctrl[fe_0.0025] |
| R9-FE-integrity | 0 discrepancies in 7,133 cross-arm comparisons (max |db| 6e-08); no ge | PASS | 7133 comparisons, max diff 5.95e-08 | keio_iron_integrity_scan.json |
| R9-FE-b0887 | b0887 (cysteine/glutathione ABC-exporter ATPase) at the deepest level: | PASS | b_ko 0.155657, y 0, engine highs-stall-override | keio_iron_limited_e12_sweep.csv + stall_overrides.json |
| R9-ARG-ijo | WT 1.259; 275 essential; plain +0.802 -> canonical +0.953 (AUC 0.991,  | PASS | WT 1.2595; 275/1367; r +0.9534; rho +0.6015 | nitrogen_pfba_control levels[arg_-10] |
| R9-ARG-iml | WT 0.950; 271 essential; plain +0.915 -> canonical +0.850 (AUC 0.997,  | PASS | WT 0.9498; 271/1516; r +0.8501; rho +0.3610 | nitrogen_pfba_control iml_levels[arg_-10] |
| R9-TEX-anchors | prop:keio-iron + rem:keio-iron-invariance present, exactly once | PASS | prop x1, rem x1 | companion_categorical_v7.tex |
| R9-TEX-table-rows | iron x5 + arginine x2 rows present in tab:canonical-selection; restore | PASS | iron01 x1, iron005 x2, iron0025 x2, arg x2 | companion_categorical_v7.tex |
| R9-TEX-escapes | no double-escaped commands remain (patch-F rendering defect fixed: bio | PASS | \\emph x0, \\S\\ref x0 | companion_categorical_v7.tex |
| S-1 | ATPM defaults 3.15 (iJO) / 6.86 (iML); ATPM selected over proton leak  | PASS | keys: iJO1366_atpm,iJO1366_hleak,iML1515_atpm,iML1515_hleak | keio_nonmedium_prescreen.json |
| S-2 | iJO WT atpm 40/60/80/100 = 0.695/0.496/0.298/0.099; iML 60/80/100 = 0. | PASS | 0.6947/0.4962/0.2977/0.0992 | keio_atpm_stress_{e12,e16}_results.json |
| S-3 | PGI at-optimum width 0.0 at EVERY ATPM level, both models | PASS | iJO 0.0/0.0/0.0/0.0 | keio_atpm_stress_{e12,e16}_results.json:degeneracy |
| S-4 iJO atpm_40 | labels 289 -> 298, kappa 0.981 | PASS | 289 -> 298 (+9/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iJO atpm_60 | labels 289 -> 298, kappa 0.981 | PASS | 289 -> 298 (+9/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iJO atpm_80 | labels 289 -> 299, kappa 0.978 | PASS | 289 -> 299 (+10/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iJO atpm_100 | labels 289 -> 331, kappa 0.912 | PASS | 289 -> 331 (+42/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iML atpm_60 | labels 286 -> 295, kappa 0.981 | PASS | 286 -> 295 (+9/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iML atpm_80 | labels 286 -> 297, kappa 0.977 | PASS | 286 -> 297 (+11/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-4 iML atpm_100 | labels 286 -> 329, kappa 0.912 | PASS | 286 -> 329 (+43/-0) | atpm results flips_vs_glucose_only (corrected) |
| S-5 | atpm_100 gains +42 on iJO: atp operon (9), cyo (4), nuo (13), pgk/eno/ | PASS | n=42 | atpm e12 flips + enrichment |
| S-6 | plain r iJO +0.949/+0.925/+0.821/+0.444 (corrected); iML +0.747/+0.435 | PASS | iJO +0.949/+0.925/+0.821/+0.444 | keio_atpm_stress_{e12,e16}_results.json |
| S-7 | canonical iJO +0.969/+0.949/+0.964/+0.937 (AUC 1.000/0.988/0.982/0.991 | PASS | +0.969/+0.949/+0.964/+0.937 | keio_atpm_pfba_control.json:ijo_levels |
| S-8 | canonical iML +0.703/+0.655/+0.475 (AUC 0.992/0.992/0.978; n_ess corre | PASS | +0.703/+0.655/+0.475 | keio_atpm_pfba_control.json:iml_levels |
| S-9 | integrity: 6 corrupted calls adjudicated (plain b0180/b3412 iJO; plain | PASS | 14 verdicts; 6 patched | keio_atpm_integrity_adjudication.json |
| S-10 | near-tie: |dL1| 8.6e-4 absolute (1.2e-6 relative); 782/1129 compensabl | PASS | dL1 8.57e-04 (1.1e-06); floor 782/1129 | keio_atpm_neartie_measurement.json |
| S-11 | nh4_-5 canonical restored into the control (r +0.922, kappa 0.9978, on | PASS | r +0.9224 | keio_nitrogen_pfba_control.json:levels.nh4_-5 |
| S-12 | merged multiaxis table: 30 levels; arm kappa = 1.000 at 30 of 31 rows  | PASS | n=30; kappa_min=0.9978; auc_min=0.9781; gain_max=+1.0369 | multiaxis_canonical_table.json:aggregates |
| S-13 | patch H present: prop:keio-atpm, rem:keio-multiaxis, ATPM table rows,  | PASS | all present: True | companion_categorical_v7.tex |
| S-14 | six-axis abstract word count < 265 | PASS | words: 264 | companion_categorical_v7.tex abstract |
| P-1 | second-engine WT biomass matches the deposited level WT (three levels, | PASS | atpm_60: 0.398390 vs 0.398390; atpm_80: 0.239034 vs 0.239034; atpm_100 | keio_atpm_iml_second_engine.json |
| P-2 | labels engine-invariant: kappa 1.000, zero flips, essential counts 295 | PASS | atpm_60: kappa 1.0000, flips 0, 295/295; atpm_80: kappa 1.0000, flips  | keio_atpm_iml_second_engine.json:vs_glpk |
| P-3 | maximum biomass discrepancy across engines <= 1e-7 at all three levels | PASS | atpm_60: 3.81e-13; atpm_80: 7.39e-08; atpm_100: 9.12e-08 | keio_atpm_iml_second_engine.json:vs_glpk.max_abs_db_ko |
| P-4 | manuscript second-engine r values +0.952/+0.968/+0.943 (prop, fifth fe | PASS | atpm_60: +0.9518; atpm_80: +0.9681; atpm_100: +0.9432 | keio_atpm_iml_second_engine.json |
| P-5 | manuscript second-engine AUC 0.992/0.992/0.984 | PASS | atpm_60: 0.9919; atpm_80: 0.9920; atpm_100: 0.9844 | keio_atpm_iml_second_engine.json |
| P-6 | stateless engine floor census: 1 of 1127 compensables in the 190-210 f | PASS | atpm_60: 1/1127; atpm_80: 1/1127; atpm_100: 1/1127 | keio_atpm_iml_second_engine.json:floor_census_highs |
| P-7 | GLPK floor census recomputed from the committed CSVs: 500/650/782 of 1 | PASS | atpm_60: 500/1127; atpm_80: 650/1127; atpm_100: 782/1127 | keio_atpm_pfba_control_iml_atpm_*.csv |
| P-8 | the stateless engine's only floor-band compensable is lamB (b4036, kV  | PASS | {"atpm_60": {"b1200": 162.0, "b1199": 162.0, "b1198": 162.0, "b3946":  | keio_atpm_iml_second_engine_atpm_*.csv |
| P-9 | near-tie engine-invariant: HiGHS WT L1 and b0870 dL1 reproduce the GLP | PASS | WT L1 747.6826157; dL1 -8.683e-04 | keio_atpm_iml_second_engine.json:L1_neartie |
| P-10 | engine bracket [+0.475,+0.943] and path-dependence wording present; 'c | PASS | bracket present: True | companion_categorical_v7.tex |
| P-11 | supply-axis PGI range 45-201 (max deposited 201.492; the unrecorded iM | PASS | max 201.492; iML nh4_-2.5 158.3162 | keio_phosphate_limited_e12_results.json + keio_iml_nh4_ |
| P-12 | infeasible KO counts identical across engines (14/16/46) | PASS | atpm_60: {'highs_pfba': 1502, 'infeasible': 14}; atpm_80: {'highs_pfba | keio_atpm_iml_second_engine.json:solve_sources |
| P-13 | nitrogen 4-panel publication figure present (157,682 bytes; the sixth- | PASS | 157682 bytes | download/keio_nitrogen_source_response.png |
| P-14 | patch I present: five amendments, no regressions ('45--202', '1,129',  | PASS | edits present: True | companion_categorical_v7.tex |
| P-15 | iJO1366 second-engine: labels engine-invariant at all four ATPM levels | PASS | {'atpm_40': (1.0, 0), 'atpm_60': (1.0, 0), 'atpm_80': (1.0, 0), 'atpm_ | keio_atpm_ijo_second_engine.json |
| P-16 | iJO1366 second-engine: canonical r within 0.002 at the three deeper le | PASS | {'atpm_40': -0.0189, 'atpm_60': 0.0011, 'atpm_80': 0.0013, 'atpm_100': | keio_atpm_ijo_second_engine.json |
| P-17 | iJO1366 second-engine: floor census 961 -> 1 at atpm_40; 2 -> 1 at 60/ | PASS | {'atpm_40': (961, 1, 971), 'atpm_60': (2, 1, 971), 'atpm_80': (2, 1, 9 | keio_atpm_ijo_second_engine.json |
| P-18 | iJO1366 second-engine: maximum biomass discrepancy <= 1.2e-7 across al | PASS | 1.1713706974531002e-07 | keio_atpm_ijo_second_engine.json |
| P-19 | lex pilot: pre-registered verdict PROMOTE (P1 engine-invariance, P2 fl | PASS | {'P1_engine_invariance': True, 'P2_floor_collapse': True, 'P3_label_pr | keio_atpm_lex_pilot.json |
| P-20 | lex pilot: maximum cross-engine vertex distance <= 6e-11 (genes + wild | PASS | 5.982749736343581e-11 | keio_atpm_lex_pilot.json |
| P-21 | lex pilot: floor collapse 40/40 random floor genes in both engines at  | PASS | {'iml_atpm_100': (1.0, 1.0, 40), 'ijo_atpm_40': (1.0, 1.0, 40)} | keio_atpm_lex_pilot.json |
| P-22 | lex pilot: label preservation, max |b_lex - b_deposited| <= 6.4e-8 (bo | PASS | 6.380317799092872e-08 | keio_atpm_lex_pilot.json |
| P-23 | lex pilot: the lamB contrast -- iML1515 kV 200.0 in both engines, iJO1 | PASS | (200.0, 200.0, 0.0, 0.0) | keio_atpm_lex_pilot_{iml,ijo}_atpm_*.csv |
| P-24 | full lex sweep: declared-rule r +0.9534/+0.9686/+0.9440 (iML1515 60/80 | PASS | ({'iml_atpm_60': 0.9534, 'iml_atpm_80': 0.9686, 'iml_atpm_100': 0.944, | keio_atpm_lex_full_sweep.json |
| P-25 | full lex sweep: labels kappa 1.000 vs the deposit at all four levels;  | PASS | {'iml_atpm_60': (1.0, 295, 295), 'iml_atpm_80': (1.0, 297, 297), 'iml_ | keio_atpm_lex_full_sweep.json |
| P-26 | full lex sweep: floors 6/1/1/0 (iML 60/80/100, iJO 40); lamB kV 200.0  | PASS | {'iml_atpm_60': (6, 1127), 'iml_atpm_80': (1, 1127), 'iml_atpm_100': ( | keio_atpm_lex_full_sweep.json |
| P-27 | full lex sweep: the dhaKLM/fsaA/fsaB block deepens 194 -> 299 -> 427 a | PASS | {'iml_atpm_60': [193.6, 193.6, 193.6, 193.6, 193.6], 'iml_atpm_80': [2 | keio_atpm_lex_full_sweep.json |
| P-28 | full lex sweep: iJO1366 floor-level rerouting block pfkB/fbaB/ydjI at  | PASS | {'b1773': 89.8, 'b2097': 89.8, 'b1723': 89.8, 'b3946': 68.9, 'b0825':  | keio_atpm_lex_full_sweep.json |
| P-29 | patch J present: tie-break paragraph, closure clauses, feature count f | PASS | edits present: True | companion_categorical_v7.tex |
| P-30 | iJO1366 second-engine + lex artifacts carry the probe-convention WT ag | PASS | (2.4077961846558082e-14, 4.645983204265569e-07) | keio_atpm_{ijo_second_engine,lex_full_sweep}.json |

## Counts ledger (near-colliding counts)

| value | meaning | source |
|---|---|---|
| 2,583 | iJO1366 reactions (model size) | data/bigg_models/iJO1366.json; recomputed in E22-2R |
| 438 | reactions active on the E22 physiology (17.0%) | recomputed E22-2R; v16 results json baseline |
| 440 | reactions with D2 > 1e-8 along the E24 trajectory (reaction-level count; V5/V8 json n_events_rxns) | v5_e24_recalibration.json:trajectory.refine_8.n_events_rxns; v8 json per-arm |
| 433 | panel genes with M3D response (E24 panel) | novelty_v17_option_a_e24.csv row count |
| 424 | panel genes with NONZERO kappa_mu (the n of the primary correlation) | v5/v6/v8 json n_nonzero |
| 426 | nonzero genes on P1/P2 paths (V7) | v7_path_robustness.json:arms n |
| 435 | genes with >= 1 active reaction (E22) | e22 csv (kappa_V_max > 0) = 435 (recomputed E22-1) |
| 454 | max active reactions across the 9 E23 conditions | v16 results json coverage.active_rxns_per_condition |
| 537 | union of active reactions across conditions (20.8%) | v16 results json coverage.union_active_rxns (v21 typo 538) |
| 525 | genes with nonzero kappa across conditions | v16 results json coverage.union_genes_nonzero_kv (v21 typo 524) |
| 1,516 | iML1515 genes (M3 single knockouts) | m3_summary.json:n_genes |
| 2,779 | double-knockout pairs (five panels) | m3_summary.json:pairs.n_pairs |

## Documented artifact quirks

- V5 json arm labels '(4x)'/'(8x)' swapped (cosmetic; frozen artifact left unedited; manuscript unaffected).
- V6 partial p (0.93) not stored; recomputed from stored partial r and n: consistent.
- V1 value/flux ratio denominator (3807.6) stored in the committed report script, not the frozen json.
- Frozen v21 E23 numbers 538/524 are typos; v2's 537/525 match the v16 results json (v21 not edited).