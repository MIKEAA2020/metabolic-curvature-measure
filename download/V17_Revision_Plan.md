# V17 Revision Plan — Enrichment and Insight Program

**Status: PLAN ONLY — NOT IMPLEMENTED.** Base version `journal_manuscript_v16.tex`
(+ companion `companion_categorical_v10.tex`) is untouched and remains the
current submission state. Nothing in this document has been added to any
manuscript. Per author directive: all revisions will be produced as NEW
versioned files (v17), never overwriting; every created artifact will be
committed and pushed immediately.

**Provenance.** Part A consolidates the round-214d40e enrichment-merit
assessment. Part B is the round-3 exploration of implications *beyond* the
paper's established results, requested explicitly ("profound biological
and/or chemical implications beyond what is already established"). Novelty
was calibrated by grep against v16: every Part B direction has zero coverage
in the current manuscript (0 hits for: priority effect, community, consortium,
operon, RegulonDB, Ishii, order of introduction, construction order, menu,
metabolite pool, growth-silent, evolvab*, free parameter).

**Audit discipline (governs everything below).** The v15-round standard
applies: no number enters the manuscript unless it is computed from
deposited artifacts and passes the numeric audit; predictions must be
labeled as predictions; correlational discipline is preserved. The pipeline
for implementation: audit extension (audit_v25) -> pattern_sweep_v16 ->
completeness diff vs v16 -> tectonic build -> VLM page checks -> fresh-dir
ZIP re-verification -> cover-letter/links retarget -> worklog -> commit ->
push.

---

## Part A — In-paper enrichment (assessed as merited, round 214d40e)

### A1. Anchored biological case study
- **Anchor.** The regulation evidence is statistical (r = +0.395, n = 424;
  rho_S = 0.865; 66% non-reverting cycles); regulon/TF anchoring appears
  once in v16.
- **Plan.** One deep-dive on the carbon-depletion switch the M3D association
  is measured on: reactions/genes carrying the largest curvature mass,
  matched against the regulons documented to govern that response
  (Crp-cAMP; kochanowski2013 already cited at 4 sites).
- **Placement.** Empirical section (sec:empirical) as a subsection
  "Anatomy of one switch."
- **Verification.** New numbers computed from deposited curvature
  artifacts; audited; no new wet-lab claim.

### A2. Metabolic Control Analysis comparison
- **Anchor.** Zero MCA/control/elasticity mentions in v16; the first
  objection a mathematical-biology reviewer will raise.
- **Plan.** One subsection: MCA coefficients are local smooth
  sensitivities at a stable steady state; kappa_mu is global,
  path-integrated, degeneracy-aware, concentrated on strata boundaries;
  the two coincide only inside the smooth window (h << sigma << L_var)
  and diverge exactly where rerouting happens.
- **Placement.** Discussion (positioning block), or end of Sec. 2.

### A3. Hand-checkable minimal worked example
- **Anchor.** No toy network in v16 (only solver stress-test "toys").
- **Plan.** 3–4 reaction network, one parameter: chamber complex,
  wall-crossing, atomic measure as deltas at the kink, kappa_mu by hand;
  include one degenerate vertex where curvature concentrates while
  fluxes stay continuous (ties to the tie-break work).
- **Placement.** End of Sec. 2 or standalone "A worked example" subsection.

### A4. (Conditional) Buffering elevation
- Merited only if the retarget venue is biology-facing (PLOS Comp Bio):
  promote the dissociation finding to a Discussion-level positioned
  claim. For JTB the current form is adequate. Superseded in part by
  Part B III below (which goes further than promotion).

---

## Part B — Implications beyond the established results

### I. The menu/order synthesis: transcription prices the option set, translation places the order
- **Established anchors.** Tie-break invariance (rho = 0.99998; five
  protocols, r in [+0.386, +0.396]) — transcriptional response is invariant
  to WHICH degenerate optimum is selected, hence it tracks the degeneracy
  structure, not the selected solution; the value-layer null control
  (shadow-price r = +0.032, p = 0.93) — it does not track growth
  sensitivities either; the dissociation (+0.395 transcript vs -0.083
  protein); the coupling identity D^2 Phi = sum_r c_r D^2 v*_r — walls
  with c_r = 0 are invisible to growth and exist in bulk.
- **New claims.** (1) Transcriptional induction should concentrate on
  growth-SILENT wall mass (c_r ~ 0 strata): regulation occupies the sector
  where selection on growth is silent, i.e. degeneracy is evolution's
  unconstrained design space (regulatory evolvability). (2) Co-regulated
  modules (operons/regulons) should map onto wall-adjacent reaction sets.
  (3) Corollary: enzymes move walls (kinetic parameters set constraint
  geometry); regulation chooses crossings (the pivot rule); growth
  constrains only the c_r != 0 subset.
- **Substantiation path.** Partition kappa_mu mass by c_r growth-visibility
  from deposited artifacts; per-partition M3D correlation; RegulonDB
  enrichment of high-kappa_mu modules. Discriminating either way.
- **Impact.** Re-frames the function of transcriptional regulation in
  metabolism as degeneracy management (menu curation), not rate tuning.
- **Status.** Derived prediction; computable from deposited artifacts.

### II. Construction-order epistasis: path dependence as a design variable
- **Anchors.** Non-commuting sequential knockouts (66%); linear holonomy
  (slope 1.00); epistasis-active-set alignment (rho_S = 0.865).
- **New claim.** For identical final genotypes, the realized flux state
  depends on introduction ORDER; active-set geometry ranks orders by
  predicted endpoint drift; wall-interference vs wall-addition explains
  epistasis sign.
- **Substantiation.** In-silico both-order construction across existing
  double-mutant panels; prediction verifiable against existing data.
- **Impact.** A design rule for strain construction (order planning in
  metabolic engineering); explains order effects reported in engineering
  practice.
- **Status.** Derived prediction; machinery already exists in the paper's
  experiments.

### III. The memory-substrate deduction
- **Anchors.** 66% non-reverting cycles (hysteresis in flux state) AND
  protein-layer buffering (-0.083).
- **New claim.** Since the flux state after restoration differs while
  translation is buffered, the material carrier of path dependence CANNOT
  be enzyme abundance: it must live in fast post-transcriptional state —
  metabolite pools and post-translational modification states. A forced
  choice from two established facts.
- **Substantiation.** Consistency with PRECISE/M3D kinetics; kochanowski's
  metabolite-level passive coordination already supports metabolite-level
  mediation.
- **Impact.** Converts the buffering null into a load-bearing structural
  constraint on memory implementation; sharpens the search for hysteresis
  mechanisms.
- **Status.** Logical deduction; strongest form is as a constraint.

### IV. Wall coordinates in chemistry: branch metabolites carry the geometry
- **Anchors.** Measure concentrated on codimension-one strata (93.4–100%);
  rank-one jump tensors; dual-cell coarse-graining (strong L1).
- **New claim.** Flux redistribution at a wall is realized biochemically
  through branch/hub metabolites whose saturation states flip the flux
  split: branch-metabolite pools are the chemical coordinates of the wall;
  their concentration trajectories should show kinks at wall crossings
  while dedicated-metabolite pools respond smoothly; the sigma-smoothed
  ensemble response converges like the dual-cell reconstruction.
- **Substantiation.** Prediction against public multi-omics panels
  (Ishii-2007-style series, PRECISE); in-silico mapping of curvature mass
  to reactions adjacent to branch metabolites.
- **Impact.** Gives the discrete measure a wet-lab observable; links the
  discrete differential geometry to metabolomics; same pools carry III.
- **Status.** Chemistry-flavored prediction; testable with public data.

### V. Drift-free interior architecture
- **Anchors.** Linear drift law (slope 1.00 — cyclic environments
  accumulate drift without bound); switch-mass concentration (93.4–100%);
  active-reaction census (438/2,583).
- **New claim.** Organisms in cyclic environments accumulate state drift
  proportional to cycling history, so selection should position core
  internal cycles in chamber interiors (drift-free) while concentrating
  curvature mass on exchange/transport/branch-point reactions: the wall
  structure is the species-specific regulatory interface; the interior is
  the conserved chemical core. Explains core-metabolism conservation
  alongside regulatory divergence.
- **Substantiation.** Curvature-mass distribution over reaction classes
  (transport/exchange vs internal cycles) from deposited artifacts;
  cross-check against the census and GPR class counts.
- **Impact.** An architectural design principle of metabolism derived from
  the drift law.
- **Status.** Architectural prediction; partially checkable now.

### VI. Priority effects as chamber selection (EXCLUDED from v17 — follow-up program)
- Cross-feeding makes each partner's growth a parameter of the other's LP:
  a joint chamber complex; assembly history is a path through it; the 66%
  single-organism hysteresis predicts persistent community priority
  effects with a geometric mechanism complementary to dynamical
  alternative-stable-states explanations.
- **Scope discipline.** The paper is single-organism by design (Limitations);
  this requires a two-organism extension. Logged for the follow-up
  program; NOT planned for v17.

---

## Part C — Explicitly refused as decorative
- A second organism or additional growth condition (generality is already
  honestly bounded in Limitations).
- Additional category theory imported from the companion (division of
  labor is deliberate and stated in both manuscripts).
- Glossaries, summary boxes, "key insights" restatements (the Gemini
  register already handles accessibility; the abstract is at the 255 cap).
- Any future-applications laundry list (engineering, antimicrobials,
  microbiome) without a computation behind it — the exact pattern the BMB
  desk rejection punished.

## Part D — Execution protocol (when green-lit)
1. New files only: `journal_manuscript_v17.tex` (from v16), companion
   unchanged unless separately directed; v16 and all earlier versions
   untouched.
2. Every new number: computed from deposited artifacts, entered into an
   extended numeric audit (audit_v25 via make_audit_v25.py), 301+check
   total; predictions labeled as predictions.
3. Full pipeline per manuscript round: pattern_sweep_v16 16/16;
   completeness diff vs v16 (allowing only audited additions);
   tectonic build zero-errors/zero-undefined; VLM page checks; fresh-dir
   ZIP re-verification; cover letters + links doc retargeted to the chosen
   venue.
4. Venue dependence: A1/A2/A3/I/II/IV/V fit JTB or Mathematical
   Biosciences as-is; A4 + prominence of I/III for PLOS Comp Bio
   (bio-first framing). VI excluded.
5. Each round: worklog entry, commit, push (one-off PAT-embedded URL; PAT
   never stored).
