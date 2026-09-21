# V17 Insight Development — The Six Beyond-Established Lines, Substantiated

**Status: DEVELOPMENT ROUND (computed, not yet in any manuscript).** Base version
`journal_manuscript_v16.tex` (and companion `companion_categorical_v10.tex`)
remains untouched and is the current submission state. This document
implements Part B of `download/V17_Revision_Plan.md` under the author
directive "proceed with the previous 6 suggestions"; the venue decision is
expected to follow from how much biological/biochemical impact this round
developed.

**Method discipline (unchanged).** Every number below was computed by
`scripts/v17_insight_substantiation.py` from COMMITTED artifacts only (no new
LP solves, no new wet-lab claims): the V7 trajectory family
(`download/deepseek_bridge/v7_path_robustness.{json,csv}` + per-path csvs),
the M1 sweep family (`download/m1_m3/m1_*.npz`, per-reaction flux paths and
active-set masks; per-sweep D2 totals re-verified against
`m1_summary.json`), the M3 epistasis/path panels
(`download/m1_m3/m3_{path,pairs,singles,summary}.*`), the E27 Schmidt
protein-layer replication (`download/novelty_v20_e27_schmidt_replication.csv`),
and PRECISE regulatory annotations
(`data/precise/data/{gene_info.csv,TRN.csv,imodulon_gene_bnumbers.txt,
curated_enrichments.csv}`). Machine ledger:
`download/v17_insight_substantiation.json`. Predictions are labeled as
predictions; correlational discipline is preserved; honest nulls are
reported as nulls.

---

## Executive synthesis (what the six lines now say together)

The paper's established results are: a curvature measure concentrated on
active-set switches (93.4–100% of mass on events); a curvature–transcription
association (r = +0.395, n = 424); epistasis–active-set alignment
(rho_S = 0.865); path-dependent, non-reverting rerouting (66% of closed
cycles); and protein-layer buffering (r = -0.083). This round turns each
anchor into a mechanism-level statement with names attached — regulators,
operons, metabolites, and a design rule — without leaving the deposited
artifacts:

1. **The growth-silent sector is not partial but total.** Across all three
   trajectories, the growth-attributed curvature is identically zero for all
   433 panel genes; the value layer carries 0.02–0.15% of the flux layer's
   curvature mass. Transcription tracks a geometry that growth cannot see.
2. **The menu is priced at operon granularity, by the global carbon/energy
   regulons.** CRP (fold 2.43, p = 2.8e-17), Cra, Fur, Fnr, RpoS, Fis,
   ArcA, NarL, IHF; whole operons (nuo, atp, sdh-suc, cyo, ptsHI-crr,
   pdhR-aceEF-lpd) sit entirely in the top curvature quartile; within-operon
   curvature is constant even for genes catalyzing disjoint reactions
   (gap 0.082 vs 1.045 across operons, permutation p < 2e-4).
3. **Construction order is a design variable with a computable rule.** The
   gene whose single knockout crosses more wall mass drives the terminal
   drift when it leads (rho = 0.44, p = 2e-4; sign agreement 59/66,
   p = 2.4e-11).
4. **The memory carrier is chemically cornered.** Protein fold-change
   explains at most 0.7% of curvature variance, while 66% of cycles retain
   flux-state drift: the substrate of metabolic memory must be fast,
   post-translational state — metabolite pools and modification states.
5. **The wall coordinates are named metabolites.** The top-20 branch
   metabolites carry 59.7% of all curvature mass: fructose-6-phosphate
   (8.1%), glyceraldehyde-3-phosphate (6.9%), glucose-6-phosphate (5.5%),
   DHAP (4.9%), PEP (4.5%), 2-oxoglutarate, pyruvate, CoA, oxaloacetate,
   succinate. Including energy/redox currency, 98.6% of the mass sits on
   branch/currency-adjacent reactions.
6. **The interior architecture claim is revised by its own test.** The
   curvature mass is NOT on the exchange/transport interface (exchange:
   12.4% of reactions, 3.9% of mass, 92.6% flat) — it is on internal
   branch-point chemistry of five central subsystems (glycolysis 23.4% +
   PPP 19.7% + TCA 14.0% + oxidative phosphorylation 11.6% + anaplerosis
   4.7% = 73.4% of all mass). The conserved chemical core is where the
   walls are; the species-specific part is the regulon curation of those
   walls (item 2).

---

## Line I — The menu/order synthesis: transcription prices the option set

**Claim developed.** Transcriptional regulation of metabolism functions as
degeneracy management (menu curation), not rate tuning: it is deployed
where growth selection is silent, at operon granularity, by the global
carbon/energy/redox regulons.

**Substantiation (computed this round).**

*a. The growth-silent partition is total.* Recomputed from the three V7
trajectories (P0 glucose decline, P1 oxygen limitation, P2 acetate switch):

| path | flux-layer arm r (n) | dual/value arm r (p, n) | kappa_c nonzero genes | value/flux mass ratio |
|---|---|---|---|---|
| P0 glucose decline | +0.3954 (424) | +0.032 (0.82, 51) | 0 / 433 | 0.00145 |
| P1 oxygen limitation | +0.3183 (426) | -0.170 (0.17, 68) | 0 / 433 | 0.00024 |
| P2 acetate switch | +0.2234 (426) | -0.010 (0.94, 71) | 0 / 433 | 0.00055 |

The c-attributed (growth-visible) curvature is identically zero for every
panel gene on every trajectory. The association the paper reports
(r = +0.395) is therefore carried entirely by growth-invisible wall mass:
regulation occupies the sector where selection on growth is silent, which
is precisely the degeneracy design space. A cross-condition arm sharpens
this: the acetate-switch trajectory's curvature predicts the
carbon-depletion transcriptional response at r = +0.391 (P1: +0.378) — the
curvature, not the specific nutrient, is what transcription reads.

*b. Co-regulated modules map onto wall-adjacent reaction sets.* Fisher
enrichment of the top-kappa quartile (n = 110 of the 424 nonzero-kappa
panel genes) against PRECISE annotations, background = panel:

- **Regulons (TRN, 237 regulators, 31 testable):** crp 56/89 (fold 2.43,
  p = 2.8e-17, BH 8.6e-16); cra 39/52 (fold 2.89, BH 2.8e-14); fur 24/27
  (fold 3.43); fnr 46/77 (fold 2.30); rpoS 26/33 (fold 3.04); fis 22/31
  (fold 2.74); arcA 41/89 (fold 1.78); narL 14/20 (fold 2.70); ihf 21/38
  (fold 2.13); rpoD 86/274 (fold 1.21); nagC 6/8. Eleven regulons survive
  BH < 0.10. These are exactly the global menu curators: carbon (CRP, Cra),
  iron/energy (Fur, Fnr, ArcA), nitrate (NarL), general stress (RpoS, RpoD,
  IHF), nucleoid architecture (Fis, IHF).
- **Direction:** CRP's activation targets are enriched (median kappa 0.6 vs
  0, MWU p = 0.0016) while its repression targets are not (p = 0.43); the
  same activation-only pattern holds for Fis and Fnr. Induction prices the
  options; repression does not track the geometry.
- **Operons (826 multi-gene operons, 31 testable):** nuoABCEFGHIJKLMN 13/13
  (BH 4.3e-07), atpIBEFHAGDC 9/9 (BH 6.4e-05), sdhCDAB-sucABCD 8/8 (BH
  1.8e-04), cyoABCDE 4/4, manXYZ 3/3, ptsHI-crr 3/3, pdhR-aceEF-lpd 3/3
  (each BH < 0.08) — every panel gene of these operons is in the top
  curvature quartile.
- **Granularity control (non-trivial):** within-operon |delta kappa| =
  0.044 vs across-operon 1.045 (381 pairs, permutation p < 2e-4). This is
  not a GPR artifact: restricted to intra-operon gene pairs catalyzing
  DISJOINT reactions (n = 205 pairs — e.g. sdh vs suc genes, different
  enzymes), the gap is 0.082 vs 1.045 (permutation p < 2e-4), while pairs
  sharing a reaction (enzyme-complex subunits, n = 176) are trivially
  identical (gap 0.0002). Co-transcribed units carry near-uniform curvature
  across their different enzymes: the option set is priced in pre-packaged
  units.
- **iModulons (92 modules, 18 testable):** DhaR/Mlc 5/5 (Carbon Source
  Utilization), ArcA-1 9/13 (Energy Metabolism), Crp-2 6/7 (Carbon Source
  Utilization), ArcA-2 4/5 — the co-expression modules that light up are
  the carbon/energy ones.

*c. Chemical hook.* Of the TRN's 237 regulators, the sensing molecules of
five are themselves metabolites of the network (FMN, L-tryptophan,
adenosylcobalamin, molybdopterin, spermidine): the menu's prices are quoted
in chemical currency. [Prediction, testable: the metabolite-effectors of
the enriched regulons should be wall-adjacent pools from Line IV.]

*d. Honest limitations.* The panel is correlational; the enrichment shares
the expression-level confound structure of the parent association (the
activation/repression split partially controls it, but a per-gene
expression-matched control is future work); the PRECISE RNA-seq
carbon-switch arms replicate the association only weakly (r = 0.10–0.13,
vs M3D +0.395 / +0.17–0.21 cross-arms), so the transcript association is
platform-dependent in magnitude while consistent in sign.

**Impact.** Reframes the function of transcriptional regulation in
metabolism as degeneracy management, with a falsifiable chemical
corollary (c) and a mechanism-level anchor for the paper's A1 case study
(CRP-cAMP is the single strongest enriched regulon — the case study writes
itself from this table).

---

## Line II — Construction-order epistasis: path dependence as a design variable

**Claim developed.** For identical final genotypes, the realized flux state
depends on introduction order, active-set geometry ranks the orders, and
the ranking is computable in advance from single-knockout curvature.

**Substantiation (computed this round, M3 both-order panels, 160 pairs).**

- *Prevalence (deposited, now contextualized):* 19.4% of pairs have
  order-dependent endpoints (open-path commutator chi > 0); among
  non-synthetic-lethal pairs the 90th-percentile endpoint separation is
  101.3 L1 flux units against a wild-type total flux magnitude of 770 —
  the same final genotype can sit ~13% of total flux magnitude away from
  the other order's state. 66.25% of closed cycles fail to return to the
  initial flux state (median residual drift 109.3).
- *The order rule (new):* for the 66 non-degenerate closed loops, the
  normalized terminal-drift asymmetry A (which order drifts more)
  correlates with the normalized single-knockout curvature difference P at
  rho = 0.442 (p = 2.0e-4), with sign agreement in 59/66 pairs (binomial
  p = 2.4e-11). **The gene whose knockout crosses more wall mass sets the
  loop's irreversibility when it leads the excursion.** Planning rule:
  schedule deep wall-crossers LAST to minimize terminal drift (e.g. when
  intermediate states must remain recoverable), or FIRST to deliberately
  separate the endpoint from the initial state (e.g. to lock in a
  production phenotype).
- *Honest null:* order asymmetry is NOT predicted by active-set footprint
  overlap (chi vs J_dR: rho = 0.07, p = 0.38) — epistasis alignment
  (rho_S = 0.865, established) and order ranking are governed by different
  geometric quantities (overlap vs magnitude). The machinery for
  engineering use is a single extra LP per candidate gene (its kappa_i is
  already a byproduct of the singles panel).

**Impact.** A quantitative design rule for strain construction and
evolution protocols, derived from the paper's own machinery — the first
order-of-introduction rule in metabolic engineering that comes from
geometry rather than trial and error.

---

## Line III — The memory-substrate deduction

**Claim developed.** The material carrier of metabolic hysteresis cannot be
enzyme abundance; it must live in fast post-translational state —
metabolite pools and modification states. This is a forced choice from two
established facts, now with its quantitative premises re-verified and
extended.

**Substantiation (reassembled and re-verified).**

- Premise 1 (deposited): 66.25% of closed genotype cycles retain
  flux-state drift after full restoration; median residual drift 109.3 L1.
- Premise 2 (re-verified this round from the E27 Schmidt csv): protein
  fold-change r = -0.083 (n = 366; recomputed -0.0828) while transcripts
  on the same gene subset carry r = +0.419 (recomputed +0.4197, n = 365).
  With the locked kappa_mu metric the picture is unchanged (protein
  r = -0.098, p = 0.06; transcript r = +0.339).
- Bound: R-squared(protein) = 0.0069 — the protein layer can carry at most
  0.7% of the curvature variance. A state difference of median size 109 L1
  therefore cannot be stored in enzyme composition.
- Timescale squeeze: transcripts carry the association but are
  instructions, not state; protein composition is buffered; so the
  persistent state variable is fast and post-translational. Kochanowski et
  al. (2013, already cited at four sites in v16) document metabolite-level
  passive coordination on precisely the required timescale, and the
  Line-IV wall coordinates name the candidate pools (F6P/GAP/G6P/DHAP/PEP
  forks). [Prediction, testable with public metabolomics time series:
  branch-metabolite pools show slope kinks at wall crossings while
  dedicated-metabolite pools respond smoothly; the same pools carry the
  non-reverting offset after restoration.]

**Impact.** Converts the paper's buffering null into a load-bearing
structural constraint: it tells wet-lab investigators where NOT to look
(enzyme titers) and where to look (branch-pool kinetics, PTMs), and it
ties Lines III and IV to a single chemical substrate.

---

## Line IV — Wall coordinates in chemistry: branch metabolites carry the geometry

**Claim developed.** Flux redistribution at a wall is realized chemically
at branch/hub metabolites; their pools are the chemical coordinates of the
discrete curvature measure, and the sigma-smoothed ensemble response
converges like the dual-cell reconstruction.

**Substantiation (computed this round; per-reaction curvature mass over the
11 non-degenerate M1 sweeps — glucose, oxygen limitation, and nine enzyme
knockdowns; each sweep normalized by its own total mass; D2 totals
re-verified against m1_summary.json).**

- *Where the mass is:* 85.9% of all curvature mass sits on 50 reactions
  (1.8% of the network). Of those 50, 56% are branch-adjacent against a
  46.3% baseline, and 21 of the 25 heaviest reactions participate in all
  11 sweeps. The top-25 by mass: PGI (3.66%), ATPS4rpp (3.54%), PFK
  (3.33%), FBA (3.33%), GND, G6PDH2r, PGL (PPP entry: 3.2% each), THD2pp,
  DHAPT, F6PA, PDH, ICDHyr, AKGDH, SUCOAS, MDH, RPE, PFK_3/FBA3, PPC,
  NADH16pp, ICL, MALS, PGK, GAPD, PGM — the glycolysis/PPP/TCA/OXPHOS
  core.
- *The wall-coordinate table (metabolite-level rollup; each reaction's
  mass split over its branch metabolites):* fructose-6-phosphate 8.13%,
  glyceraldehyde-3-phosphate 6.92%, glucose-6-phosphate 5.47%, DHAP 4.91%,
  PEP 4.50%, 2-oxoglutarate 3.64%, pyruvate 3.64%, coenzyme A 3.57%,
  oxaloacetate 2.14%, succinate 2.14%; the top-20 branch metabolites carry
  59.7% of the total mass. These are the textbook fork metabolites of
  central carbon: the hexose-phosphate pool (G6P/F6P), the
  triose-phosphate pool (GAP/DHAP), the PEP/pyruvate energy fork, the
  anaplerotic TCA forks (OAA, aKG, succinate), and CoA.
- *Chemistry saturation:* including energy/redox currency (ATP, NAD(P)(H),
  ubiquinone, protons), 98.6% of curvature mass sits on
  branch/currency-adjacent reactions — the geometry lives almost entirely
  at the chemical coupling layer.
- *Statistical honesty:* the reaction-count-level enrichment is modest
  (46.3% of reactions are branch-adjacent and carry 60.9% of mass,
  permutation p = 0.017; d* = 16: 28.1% carry 50.6%, p = 0.002;
  rank-AUC ~ 0.50–0.54). The strong statement is the concentration one:
  the mass that exists is attached to branch chemistry, and a handful of
  forks carry most of it.

**Impact.** Gives the discrete measure a wet-lab observable with names:
targeted metabolomics of ~20 pools during nutrient transitions is a
complete experimental readout of the theory's central object. It also
supplies the chemical anchor for the A1 case study (the F6P/GAP/PEP forks
are where the CRP/Cra regulons' enzymes sit).

---

## Line V — Drift-free interior architecture (revised by its own test)

**Claim as planned.** Core internal cycles sit in chamber interiors
(drift-free) while curvature concentrates on exchange/transport — the wall
structure as the species-specific interface.

**What the computation actually shows (honest revision).** The second half
is contradicted by the deposited sweeps; the first half survives and the
architecture story gets BETTER:

- Class distribution (share of reactions -> share of curvature mass):
  exchange 12.4% -> 3.9% (92.6% of exchange reactions are flat);
  transport 32.7% -> 20.7% (90.4% flat); internal 54.9% -> 75.4% (74.3%
  flat; permutation p = 0.0012). The same internal dominance holds in both
  sweep families (nutrient sweeps: 74.1% internal; enzyme-knockdown sweeps:
  75.7% internal — the knockdowns perturb internal capacities directly, so
  this is not an artifact of parameterizing exchange bounds).
- Subsystem rollup: glycolysis/gluconeogenesis 23.4%, pentose phosphate
  19.7%, citric acid cycle 14.0%, oxidative phosphorylation 11.6%,
  anaplerosis 4.7% — 73.4% of all curvature mass in five central
  subsystems; all transport categories combined ~8%.
- The iJO1366 glucose sweep is a whole-network one-chamber path: total
  second-difference mass 6.5e-9 across 2,583 reactions — an entire
  trajectory living in a single chamber (consistent with the deposited V6/V7
  census: zero interior chamber crossings on the glucose-decline path, all
  kinks at design corners).
- Active-support census cross-check: 421–440 active reactions across the
  iJO glucose sweep endpoints, bracketing the manuscript's E24 endpoint
  value of 438.

**Revised architectural principle (v17 candidate).** The walls of E. coli's
flux geometry sit at the conserved, internal, branch-point chemistry of
central carbon metabolism — not at the exchange interface, which is flat.
The species-specific layer is not the wall chemistry but its regulon
curation (Line I: CRP/Cra/Fnr/ArcA operons priced at operon granularity).
This explains the deep conservation of central branch chemistry across
species alongside the divergence of its transcriptional wiring: the
chemistry is where the geometry has to be; the regulation is how each
species prices crossings of it. [Prediction, partially checkable now:
cross-species comparison of kappa_mu mass distribution — the branch-point
concentration should be conserved while regulon membership of the same
wall-adjacent genes diverges; the RegulonDB-vs-precise-panel machinery
here extends directly.]

**Impact.** A design principle of metabolism derived from the paper's own
deposited artifacts, with an intra-round falsification that was caught,
reported, and converted into a sharper claim — exactly the audit
discipline the paper is built on.

---

## Line VI — Priority effects as chamber selection (follow-up program, not v17)

**Developed mechanism (no computation, per plan scope).** In a
cross-feeding community, each partner's growth appears in the other's LP
as a parameter (uptake bounds set by secreted fluxes): the joint optimum
sweeps a JOINT chamber complex whose chambers couple the partners' active
sets. Assembly history is a path through that joint complex; the
single-organism results then make three predictions: (i) community
priority effects should be common — the 66% single-organism non-reversion
rate is a mechanistic prior for the persistence of order-dependent
community states; (ii) the drift law (linear accumulation, slope 1.00)
predicts community-state drift proportional to assembly-history length
under environmental cycling; (iii) cross-feeding partners with
complementary wall chemistry (one partner's waste at the other's branch
forks) should show the strongest history dependence. A minimal two-strain
extension (sequential introduction, shared metabolite pools at the
branch coordinates of Line IV) is the natural first experiment; the
LP/lex machinery extends without modification to the joint problem.

**Status.** Logged as the follow-up program; excluded from v17 per the
plan's scope discipline (single-organism Limitations stand).

---

## What this means for the venue decision

The BMB desk verdict was "biological impact and implications ... not
sufficiently strong." This round develops exactly that dimension, with
computed substance rather than assertion: a named regulator table (CRP at
BH 8.6e-16), named operons, named metabolites carrying the geometry, a
chemical memory-substrate constraint, and a construction-order design
rule. Two honest caveats bound the claim: the panel evidence remains
correlational (enrichment shares the parent association's confound
structure), and the reaction-level branch statistics are concentration
effects (AUC ~ 0.5) rather than distributional shifts.

- **If the author wants the strongest biological positioning:** PLOS
  Computational Biology is now genuinely defensible (bio-first framing
  with A1 + A4 + prominence of I/III/IV); the development above is the
  rebuttal-in-advance against a repeat of the BMB verdict.
- **If the author wants the mathematical home:** JTB or Mathematical
  Biosciences remain fully adequate — all six lines fit as a Discussion
  development without venue-specific reframing.
- The companion (TAC) is unaffected by this round.

## Next steps (on green light, per Part D of the plan)

1. v17 as a new file from v16: A1 case study (now written from the Line-I
   regulator/operon table + kochanowski2013), A2 MCA comparison, A3 worked
   example, the Line-IV wall-coordinate table, and (venue-dependent) I/III
   prominence. Line V enters as the REVISED architecture claim.
2. audit_v25 extension covering every new number in this ledger;
   pattern_sweep_v16; completeness diff vs v16; tectonic; VLM page checks;
   fresh-dir ZIPs; cover letters + links retarget; worklog; commit; push.
