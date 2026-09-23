# Cover Letter — Bulletin of Mathematical Biology

**To:** The Editors, Bulletin of Mathematical Biology
**Date:** September 24, 2026
**Manuscript type:** Original Research Article
**Title:** A discrete curvature measure for flux balance analysis
predicts transcriptional regulation and translational
buffering in Escherichia coli

---

Dear Editors,

I am pleased to submit my manuscript "A discrete curvature measure for
flux balance analysis predicts transcriptional regulation and
translational buffering in Escherichia coli" for consideration as an
Original Research Article in the Bulletin of Mathematical
Biology.

The manuscript is written so that the biological line of argument leads:
the question, the measure, the validation, and the empirical association, with
the refinement theory and all proofs collected in appendices.

Parametric flux balance analysis defines a piecewise-affine map from
environmental and genetic parameters to optimal metabolic fluxes. The
manuscript establishes that the distributional second derivative of this
map is a matrix-valued Radon measure concentrated on the codimension-one
strata of the active-set complex — a discrete curvature carrier — and
that this measure organizes the network's rerouting geometry. Three
results make the work suitable for the journal's readership:

1. **A theory with a proved refinement bridge.** The atomic measure
   converges weakly to the smooth curvature density under mesh
   refinement, with a strong $L^1$ reconstruction law and an exact
   counterexample calculus delimiting total-variation convergence
   (Theorem B'). The value layer (biomass objective) is provably
   tie-break-free; loop holonomy scales linearly in loop size —
   slope 1.000000 — where any smooth map would scale quadratically.

2. **A validated, robustly tested gene-sensitivity metric.** From the
   measure the manuscript derives a per-gene sensitivity score and
   shows, in *E. coli* (M3D microarray compendium, n = 424 evaluated
   genes), that it predicts
   carbon-depletion transcriptional response
   (r = +0.395, p = 2.6 × 10⁻¹⁷; partial r = +0.269). The association
   survives every robustness check in the manuscript: metric invariance
   (ρ = 0.99998), five lexicographic tie-break conventions with the
   value layer exactly invariant, path variation, cross-platform
   replication (dissociating on PRECISE, as the layer theory predicts),
   and Glivenko–Cantelli stabilization of the underlying event measures
   across random panels. The association does not propagate to the
   protein layer (proteome r = −0.083 vs. transcript +0.419): cells
   transcribe the potential for rerouting while buffering translation.

3. **Biology beyond correlation.** The same geometry organizes
   double-knockout epistasis (Spearman ρ_S = 0.865 against active-set
   structure) and predicts the phenotypic memory of genetic loops
   (66% non-reverting).

4. **Named biology (the substance of this revision).** The induced
   genes sit in eleven enriched regulons led by CRP (Benjamini–Hochberg
   q = 8.6 × 10⁻¹⁶) at whole-operon granularity (nuo, atp, sdh–suc,
   cyo); the rerouting mass concentrates on twenty named branch
   metabolites of central carbon (59.7% of mass, led by F6P, GAP, G6P,
   DHAP, PEP), giving the theory a targeted-metabolomics readout; the
   buffering null is developed into a quantitative deduction that
   metabolic memory must live in fast post-translational state; and a
   construction-order design rule for strain engineering is derived
   from the same geometry (ρ = 0.442, sign agreement 59/66, binomial
   p = 2.4 × 10⁻¹¹). A hand-checkable worked example and a
   metabolic-control-analysis comparison (Kacser–Burns; Heinrich–
   Rapoport) have been added for the Bulletin's readership.

The mathematics is deliberately classical — parametric linear
programming (chamber complexes, active sets, Danskin duality),
Alexandrov's theorem, and distributional second derivatives of
piecewise-affine maps — applied systematically to flux-balance models
for the first time, I believe, at this level of exactness. This
methods-plus-application character is, in my view, a direct fit for
the Bulletin's mathematical-biology readership.

**Disclosure of a related manuscript.** In the interest of full
transparency I disclose that a companion manuscript is in preparation
for separate submission to *Theory and Applications of Categories*
(a no-fee, diamond open-access journal): "A Geometric and
Category-Theoretic Theory of Viability: How Sequential Adaptations
Induce Path-Dependent Risk" (theory paper). The two papers are related but distinct in purpose, and the
division of labor is deliberate:

- The **submitted manuscript** is the application: the
  measure-theoretic curvature of parametric FBA, the gene-level metric
  κ^μ, and the genome-scale empirical association with its layer
  decision. It is self-contained: all theorems it uses are proved in
  its own appendices, and no empirical claim depends on the companion.
  It is written in measure-theoretic terms alone; one paragraph of the
  Discussion points to the companion for the categorical constructions
  and proofs.
- The **companion manuscript** (provided below) develops the full
  categorical framework — stratified connections, optic composition,
  filtered colimits, the homotopy-type-theoretic extension — with its
  own proofs and machine verifications. It cites the submitted
  manuscript for the application.

The two manuscripts share no verbatim passages of length; each was
written to stand alone; neither presents the other's results as its
own. The companion is available for the editors' and reviewers'
inspection in the same public repository as the submitted
manuscript's code and data
(https://github.com/MIKEAA2020/metabolic-curvature-measure, file
`scripts/companion_categorical_v11.tex`, compiled PDF included) and will
be provided as a PDF on request; it is not under consideration
elsewhere.

The computational work is fully reproducible: every figure and number
in the manuscript is regenerated by committed scripts from deposited
artifacts, verified by a 349-check numeric audit (349/349 PASS) that
re-derives each manuscript value from its committed artifact. All
code, data manifests (SHA-256), and artifacts are publicly available;
all biological data are public (BiGG models, M3D, PRECISE, PaxDb, and
the condition-dependent *E. coli* proteome). Publication under the
journal's standard (subscription) route is intended; no open-access
charges are requested.

I am the sole author of this manuscript. I conceived the study
design, developed the methodology and analysis code, analyzed the
data, and drafted the manuscript. In accordance with the journal's
policy on generative AI in scientific writing, I disclose that
GLM (Z.ai) and DeepSeek large language models were used as writing
and coding assistants under my direction and supervision; all
assisted content was reviewed, verified, and edited by me, and I
take full responsibility for the content of the manuscript and the
integrity of its results.

I confirm that this manuscript is original, has not been published
previously, and is not under consideration by any other journal. This
work involved no human or animal subjects and required no ethics
approval.

Thank you for your consideration.

Sincerely,

Amin Abaee
Independent Researcher, Tehran, Iran
amin\_abaee@ut.ac.ir
ORCID: 0000-0002-0019-1842

**Declarations:**
- Funding: this research received no specific grant from any funding
  agency in the public, commercial, or not-for-profit sectors.
- Competing interests: the author declares none.
- Ethics approval: not applicable (fully computational study; no
  human or animal subjects; previously published public data only).
- Data availability: all data and code public; complete bundle at
  https://github.com/MIKEAA2020/metabolic-curvature-measure (SHA-256
  manifest included); companion theory manuscript available at the
  same repository and on request.
- Generative AI declaration: GLM (Z.ai) and DeepSeek assisted with
  drafting, editing, and analysis-code development under the author's
  direction; the author reviewed and edited all assisted content and
  takes full responsibility for the published work.
