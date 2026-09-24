# Causal Coherence & Prose–Math–Data Alignment Review

**Scope:** both current manuscripts — `scripts/journal_manuscript_v7.tex` (main / application paper, 28 pp) and `scripts/companion_categorical_v6.tex` (theory paper, 75 pp).
**Questions asked:** (1) scan both papers for causal coherence; (2) does the prose accurately align with and reflect the math, the empirical and numerical analyses, and the data?
**Method:** full read of the main paper; full read of the companion's load-bearing sections (SAVGS/κv definitions, gluing + holonomy + small-loop theorems, KKT law, seven-claim hierarchy, empirical verdicts, network battery, Keio anchor, canonical selection, solver-integrity, future directions); line-level verification of every definitional gloss against its formal statement; artifact spot-checks for claims outside the audit's numeric scope; cumulative audit re-run.

**Baseline re-established:** `audit_v15_numbers.py` re-executed today (cobra 0.32.1 reinstalled into `/home/z/.venv` after the sandbox reset): **301/301 PASS, 0 FAIL**; ledger refreshed at `download/deepseek_bridge/v15_number_audit.json`.

---

## Part 1 — Causal coherence

### 1.1 The main paper's causal chain: coherent, with disciplined inferential status

The paper's argument runs through six hops, and each hop is separately warranted:

| Hop | Claim | Warrant type |
|---|---|---|
| 1 | Environment → optimum is a continuous piecewise-affine map; slope changes at active-set switches | Cited parametric-LP theory (Borrelli et al.) — classical |
| 2 | D²v is a matrix-valued Radon measure concentrated on switching boundaries | Definition + Theorem B(i); machine-verified (93.4–100.0% of mass on operational switches, §m1) |
| 3 | Gene-level integration of that mass (κμ) is a well-defined sensitivity statistic | Definition + Lemma lex (well-posedness of the lex optimum); tie-break *declared*, not eliminated (rem:lock) |
| 4 | κμ associates with carbon-depletion transcriptional response | Empirical: r = +0.395, p = 2.6e-17, partial +0.269; replication on 2 further paths; robust across 5 selection rules |
| 5 | The association lives on the flux layer, by structural necessity | Theorem coupling(ii) (sparse objective ⇒ per-gene value attribution impossible) + measured null arms (§v6, §v7) |
| 6 | The association does not propagate to the protein layer | Empirical dissociation: protein-change r ≈ +0.01–0.03, Schmidt-2016 r = −0.083 (§e26, §e27) |

The paper never skips a hop, and it labels each hop's epistemic type. The Limitations paragraph opens with "The study is correlational by design" — the correct posture, since the κμ→transcript link is a concurrent statistical association, not an intervention. The two places where causal language slightly outruns this posture are flagged as findings F5 and F6 below (both wording-level).

Two structural-necessity claims deserve specific mention because they are the paper's strongest causal language and both are in fact sound:

- **"A flux-layer property by structural necessity, not merely by empirical choice" (Cor. valueflux).** The necessity is conditional on the sparse biomass objective (c = γ e_bio ⇒ D²Φ = γ D²v*_bio, so per-gene attribution from the value layer is impossible). The conditioning is real and disclosed — the 150 random *dense*-objective LPs (where all events are objective-moving) demonstrate that the necessity is exactly the sparsity, and the body says so. Sound.
- **"The tie-break is declared rather than eliminated" (rem:lock).** This is the correct causal hygiene for a selection-dependent statistic: rather than claiming the metric is selection-free (false for the flux layer), the paper declares the selection and then *measures* robustness over the protocol class (§v8: r ∈ [+0.386, +0.396] under five rules; value layer invariant to 0.0). Sound, and it is the same doctrine the companion adopts for its near-tie boundary — the two papers teach one consistent methodology.

### 1.2 The companion's causal chain: coherent; internal vs external evidence honestly separated

The theory chain (SAVGS → StCon(B) gluing → piecewise holonomy → κv → composition/contraction) is mathematics with per-result proof-status labels, and the status labels are conservative (descent-by-citation for gluing, proof-sketch for HoTT, complete for transport law / composition / contraction / terminal coalgebra). The empirical chain has three distinct evidential roles, and the paper keeps them distinct:

1. **Synthetic falsification battery (Claims A–G).** These verify the framework's own predictions on prototypes the framework defines. Two potential circularity traps are explicitly defused in the text: the Claim-C constant c₂ = 0.0500 is a *calibration* (planted in the synthetic data and recovered within 5%), labeled "a calibration-recovery check, not an independent derivation"; and the 3/2 fatigue term is a fluctuation scale that the battery treats under a *declared envelope convention*, with the pure-fluctuation reading stated alongside (rem:fatigue-convention). This is honest causal bookkeeping.
2. **Closure test on networks.** "Causally internal" is defined interventionistically (knockout destroys; restoration recovers) — genuinely causal, and the rescue checks are proper interventions (closing the sole nitrogen donor returns all 41 lost-label backgrounds to exactly zero growth; restoring exactly fabZ's two quinone-side-chain reactions restores the aerobic optimum). The designed-progression arm is disclosed as designed by the framework's authors (and the future-directions list names calibration on non-author-designed benchmarks as open). The fixed-model arm is labeled "an internal cross-check" against FBA essentiality.
3. **Keio external anchor.** The transitive arm is disclosed as a transitive hop through iJO1366's published 93.4% accuracy; the direct arm against the raw Baba table is the external validation and its weakness is reported flatly (r = +0.085, "the point-calibration is weak"); the E16 cross-rebuild non-transfer is reported "as a negative verdict"; the medium correction that reverses it is then reported with all statistics. The circularity remark (rem:operational-curvature) explicitly refuses essentiality-informed predictors, and κ^flux_V indeed carries no essentiality call.

One form-level note: prop:vulnerability ("Adaptive systems are endangered not by large environmental changes but by non-commuting sequences…") is an interpretive sentence staged as a Proposition; its mathematical content is the bound (which is proved), but the "endangered not by" framing is motivational rhetoric inside a formal environment. Not a content error; a staging choice a referee might query.

### 1.3 Cross-paper causal coherence: coherent; no circular dependency

- **Declared division of labor is implemented, not just stated.** "Neither manuscript depends on the other's claims" (both papers) — verified in the read: the main paper's empirical sections (§§m1–e27) never lean on a companion result; the companion's battery never imports a main-paper number; the main paper's §categorical carries only glosses + citations, each checked below.
- **The tie-break doctrine is identical across the two papers** — same three-stage lexicographic class, same stage-3 rule (w ~ U(0.5,1.5), seed 20240901, min w^⊤v), same "declared, not eliminated" framing (main rem:lock / §v8; companion §canonical-selection tie-break paragraph, pilot 6e-11 cross-engine identity, full-sweep closure +0.953/+0.969/+0.944/+0.951). This is consistency by design, not circularity: each paper uses the protocol for its own claims.
- **The main paper's glosses of the companion were checked one by one against the companion's actual statements:**

| Main-paper gloss | Companion ground truth | Verdict |
|---|---|---|
| Gluing "proved there by reduction to stack-descent theory"; "descent-by-citation with construction-level verification" | Proof by 2-descent citing Giraud/Breen; rem:gluing-proof-status says exactly this | ✓ |
| "Piecewise-holonomy consequences machine-verified in five loop geometries and three structure groups" | "five loop geometries and all three structure-group regimes: abelian U(1), non-abelian SO(3), endogenous-reversibility CO(3)" | ✓ (U(1)/SO(3)/CO(3) are three groups) |
| Small-loop viability–holonomy theorem "bounds the endpoint erosion of a viability margin … by the viability-weighted curvature: the worst case, over unit-area parameter bivectors and active viability margins, of the positive part of the margin's change … normalized by the margin itself" | def:kv (sup over unit bivectors, max over active covectors, [−D_F h]⁺/h) + thm:smallloop + prop:vulnerability (upper bound) | ✓ word-for-word faithful to def:kv |
| κμ "modeled on that object"; "the precise discretization correspondence … is open" | def:kv remark: "a stated correspondence at active atoms, not a proved domination; the ratio-form comparison is recorded as open" + Future-directions item 6 | ✓ both sides declare the same open status |
| "The viability-kernel reading of its dynamical closure test (a finite-time, feedback-certifying probe of kernel and capture-basin membership, with the Poincaré/averaging analysis of its pathwise levels)" | prop:closure-viability (feedback viability kernel, horizon-T recovery set, finite-horizon capture problem, cited Aubin) + prop:poincare-averaging | ✓ |
| Regime delineation: "the smooth arm (slope 2.000) is where the companion's quadratic small-loop law κ(a) = a² … live[s]; the piecewise-affine arm (slope 1.00) is the companion's wall-crossing regime" | thm:smallloop (ε² law) vs thm:stratified-holonomy (pairs-crossing wall regime); main's Prop dichotomy measures 2.000/1.00 | ✓ orders agree; one phrase-level imprecision (F7) |
| Proof-status list ("complete for the gluing formula, the Fisher-minimal transport law, the composition and contraction layers, and the terminal-coalgebra theorem; … proof-sketch … HoTT") | Companion's own status conventions and per-result remarks | ✓ exact match |

- The companion's description of the main paper ("validated at genome scale against carbon-depletion transcriptional response, with an explicit protein-layer null and selection-rule robustness checks") matches the main paper's actual content. No phantom objects, no stale cross-references (the earlier rounds' fixes hold).

### 1.4 Verdict on Q1

Both papers are causally coherent, and their mutual relationship is causal-coherent: every causal hop is proved, machine-verified, or explicitly labeled as correlational / consistent-with / calibration / internal cross-check / negative result. The single flat causal assertion in the main abstract (translation buffering) outruns its hedged body (F6), and the companion abstract's six-axis sentence compresses the label-invariance claim beyond the body's own taxonomy (F2). Neither affects any result.

---

## Part 2 — Prose ↔ math / empirical / numerical alignment

### 2.1 Math–prose alignment: verified line-by-line, all clean

Every load-bearing "in words" gloss was checked against its formal statement:

- **def:mu** (atomic curvature measure): gloss "the jump matrix is the change of slope; n_F orients the jump; |F| weights it by the size of the boundary; δ_F places unit mass on the boundary itself; μ is the sum of all atoms — zero away from the switching boundaries" — exactly A_F = [∇u]_F ⊗ n_F |F| on the (p−1)-skeleton. ✓
- **def:kmu**: "1/T Σ_e ‖A_e‖ w_e(g)", entrywise 1-norm, GPR max — matches rem:lock's three clarifications (carrier = D²v* of the lex optimum; per-reaction mass = unsigned total variation; value layer diagnostic-only). ✓
- **prop:alex**: "Φ is concave (pointwise infimum of affine dual objectives over a θ-independent dual feasible set)" — correct LP-duality argument; the OR-GPR concavity failure and the signed-crease fallback (prop:semiconvex) are stated consistently with the counterexample min(max(θ₁,θ₂),K). ✓
- **thm:coupling**: D²Φ = Σ_r c_r D²v*_r follows from Φ = c^⊤v* and linearity of distributional derivatives; the visibility dichotomy (objective-invisible = degenerate rerouting inside ≥1-dim optimal faces) is consistent with the machine-verified event census (11/12 invisible; jumps up to 1.6e4 vs |c^⊤Δv'| ≤ 1.51e-7). ✓
- **prop:twolayer / prop:maatom / rem:conventions**: codim-1 signed layer vs codim-2 MA atoms = normal-fan volumes; product-overestimate factor 2/sin∠ ≥ 2 — algebra checks (atom = ½|det(j₁,j₂)| = fan area). ✓
- **prop:seclaw**: the displayed identity det D²u/(1+|∇u|²)^{3/2} = K√(1+|∇u|²) with K = det D²u/(1+|∇u|²)² is algebraically consistent, and the "curvature per projected parameter area, not the intrinsic Gaussian curvature; bias factor √(1+|∇u|²); recovering intrinsic curvature requires the graph area correction" reading is the correct distinction between the projected-area density and the pointwise Gaussian curvature. ✓
- **rem:tvcounter**: per-cell atom sum = h²H exactly; TV per cell (|a−b|+|c−b|+4|b|)h² vs target (|a|+|c|+2|b|)h²; ratios 3−1/n (u=xy: 6/2=3) and 1.4 (2x²−xy+2y²: 14/10) — all reproduce by hand. ✓
- **thm:Bprime** (i)–(v) match the abstract's refinement sentence; the abstract does not claim the *mpLP* analogue (which is correctly a Conjecture with a machine-verified 1-D cut case). ✓
- **Companion def:kv**: "the worst fractional loss of viability margin per unit oriented environmental-loop area, to leading order; it contracts the geometric defect F with the survival covectors D h_α instead of reporting ‖F‖ alone" — faithful to the sup/max/positive-part formula, and the per-unit-area reading is consistent with thm:smallloop's ε² expansion. ✓
- **prop:kkt**: the closed-form constrained projection is the standard Lagrange solution of min ½v^⊤Gv s.t. J_p v + J_θθ̇ = 0; full-row-rank hypothesis ⇒ invertibility — correct. ✓
- **thm:smallloop / thm:stratified-holonomy**: non-abelian Stokes expansion; piecewise holonomy as chronological product with boundary transitions; cocycle cancellation of the two resets with O(ε) tangential residual — internally consistent, and the open-problem list honestly defers the O(ε²) boundary-interaction term. ✓
- **lem:comm**: ‖[R₁,R₂]‖_F = √2 α₁α₂ + O(α³) — correct (so(3) standard basis matrices have Frobenius norm √2). ✓
- **prop:noether**: standard Noether application to a Hessian (Bregman) metric with affine isometries preserving the potential — the conserved current formula is the standard one; provenance "cf. the contact-geometric Noether program" is appropriately modest. ✓
- **prop:raf-zeno-bound** and its verification remark: the bound 1/(1+log₂N) is derived under stated model assumptions ("part of the statement, not consequences"), verified on lineage E–K with margins 44.9–179.6; the τ-as-rate notation is unusual but used consistently. ✓
- **prop:poincare-averaging**: occupation fraction of a periodic orbit → phase average, phase-invariance — the proof is a one-line ergodic-average argument, correct; fractions 0.498/0.853 match the battery table. ✓

### 2.2 Numerical alignment: audit re-run + independent spot-checks

- **audit_v15: 301/301 PASS** (re-executed today after reinstalling cobra 0.32.1 into `/home/z/.venv`; ledger at `download/deepseek_bridge/v15_number_audit.json`, 301 checks, 0 fail).
- Independent spot-checks of claims *outside* the audit's scope (qualitative / cross-referencing):
  - v7 path-robustness cross-arm: artifact `deepseek_bridge/v7_path_robustness.json` gives P1 κμ vs E24 carbon response r = 0.3783, ρ = 0.4098, CI [0.303, 0.451] — matches the manuscript's "+0.378". ✓
  - Canonical-selection table rows vs `multiaxis_canonical_table.txt`: nh4_-10 (0.3498→+0.350; 0.9399→+0.940), pi_0.1 (−0.0669→−0.067), fe_0.0025 (−0.0110→−0.011), atpm_40 (0.9489→+0.949; 0.9685→+0.969) — all match at stated rounding. ✓
  - Solver-integrity account vs `keio_atpm_integrity_adjudication.json`: the false-viability pattern is exactly as described (e.g. b0180/b3412 at iML1515 ATPM 100: b_plain 0.099, b_canon 0.0, b_highs 0.0 — false-viability corrected to essential). ✓
  - Nitrogen-substitution losses vs `keio_nitrogen_source_e16_results.json`: iML1515 glutamate n_loss = 7, arginine n_loss = 15, gains = [], κ = 0.985/0.967 — matches the proposition. ✓
  - The three-regime machine verification (U(1)/SO(3)/CO(3), five geometries incl. triangular) is present with committed outputs (two_cat_gluing_*). ✓

### 2.3 Findings (actionable), ordered by materiality

- **F1 (stale number — the one concrete fix to make): main paper §Statistical protocols (line ~1360) and §Reproducibility (line ~1371) still say "(98 checks)".** The current cumulative audit is 301 checks across the two manuscripts and was re-verified today; the BMB cover letter was already updated to 301 in the last round, so the manuscript and its own cover letter now disagree. Fix: update both occurrences (e.g., "an automated numeric verification re-derives every manuscript number from the deposited artifacts (301 cumulative checks across this manuscript and its companion)").
- **F2 (abstract–body misalignment, companion): the six-axis sentence.** Abstract: "carbon, oxygen, nitrogen, phosphate, and iron supply plus non-medium maintenance stress leave labels invariant, re-stratifying only at regime switches." The body's own taxonomy is three-fold: (a) limitation gradients and medium perturbations that preserve the growth regime — labels invariant (κ = 1.000); (b) two gain-only *regime switches* (anaerobic; maintenance demand, which re-stratifies from its mildest level, 289→298); (c) nitrogen-source *substitution* losses (glutamate −5/−7, arginine −14/−15; 41 lost-label backgrounds), which rem:keio-multiaxis classifies separately as "the only re-wiring-driven losses" — not a regime switch. The abstract's clause covers (a) and (b) but silently drops (c). Fix: add the substitution qualifier (e.g., "…re-stratifying only at regime switches and under nitrogen-source substitution") or import the body's own accurate phrasing ("labels invariant under any perturbation that preserves the growth regime").
- **F3 (indirect inference, main §v7): "the per-gene ranking is largely trajectory-independent."** The quoted evidence is κμ(P1)/κμ(P2) vs the primary carbon response (r = +0.378/+0.391 — verified), not a predictor–predictor statistic ρ(κμ_P0, κμ_P1). The inference is plausible but indirect; the per-gene values are deposited, so the direct rank correlation is one computation away. Fix: report ρ(κμ_P0, κμ_P1/P2) or soften to "the association is trajectory-stable."
- **F4 (compression, main abstract): "its event measures stabilize at the Glivenko–Cantelli rate."** §e32's finding is explicitly two-regime — GC rate for random panels, *exact structural* stabilization for designed panels — and the section's Interpretation paragraph presents the two-regime structure as the finding. The abstract keeps only the statistical half (the intro's "across random panels" version is accurate). Fix: "…stabilize at the Glivenko–Cantelli rate across random panels (designed panels reproduce them exactly)" — the word budget is a few words.
- **F5 (wording, main abstract): "the association is invariant under the metric's lexicographic definition (ρ = 0.99998)."** "Invariant" is doing work for a rank agreement of 0.99998 (near-identity, not identity); the body says "metric invariance" with the number displayed and §v8 shows r moving within [+0.386, +0.396]. The parenthetical discloses the number, so this is cosmetic, but "rank-invariant to five decimals" or "stable" would be exact.
- **F6 (wording, main abstract): "cells transcribe rerouting potential while buffering its translation."** The body consistently hedges this as a model ("consistent with a model in which…", "consistent with buffering", e26/e27; alternative mechanisms for a transcript–protein dissociation — protein lifetime, timing, proteomics dynamic range — are not discussed). The abstract asserts the mechanism flatly. Fix: "consistent with cells transcribing rerouting potential while buffering its translation" (one word).
- **F7 (precision, main §categorical): "a loop crossing a switching facet accumulates a boundary contribution at O(ε) per crossing (the companion's pairs-crossing theorem)."** The companion's theorem gives an O(ε) residual per *pair* of crossings (tangential variation of the transition between the two crossing points; the individual O(1) resets cancel within the pair). Loop-level orders agree; "per crossing" is imprecise. Fix: "per crossing pair" or "per wall traversal."

### 2.4 Clean items (verified; no action)

- All definitional glosses listed in §2.1.
- Cross-paper descriptions in both directions (§1.3 table).
- Counts-disambiguation appendix (424/433/435/438/440/525/537/4/350/25,107/1,516/2,779) — each row traceable to a deposited artifact (audit LEDGER + counts checks pass).
- Tie-break conventions identical across the two papers; no shared numeric claims (no circularity).
- No phantom objects, no "earlier literature"/self-referential framing, no stale section pointers (prior rounds' fixes hold).
- All numeric claims in both abstracts are covered by passing audit checks (ABS families) — the numbers in both abstracts are exactly the deposited ones.

---

## Bottom line

**Q1 (causal coherence): yes.** Both papers are causally coherent and mutually coherent. Every causal hop is proved, machine-verified, or explicitly labeled (correlational / consistent-with / calibration / internal cross-check / negative result). The two blemishes are wording-level: one flat mechanistic assertion in the main abstract (F6) and one abstract-level compression in the companion (F2).

**Q2 (prose ↔ math / data): yes, with seven findings, one of which is a concrete stale number.** The load-bearing prose matches the mathematics line-by-line; the numbers match the deposited artifacts at the stated precision (301/301 audit + independent spot-checks). The actionable items: fix "98 checks" (F1, now inconsistent with the cover letter), qualify the companion's six-axis abstract sentence (F2), and optionally tighten five wording/precision items (F3–F7). None of the seven affects any result, proof, or statistic.
