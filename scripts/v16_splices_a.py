# -*- coding: utf-8 -*-
"""v16 splice data, part A: header/meta, abstract, introduction, Sec. 2.

Each splice: (name, start, end, new). The engine replaces the region
[start .. end] (inclusive of both anchor strings) with `new`.
All start anchors must be unique in journal_manuscript_v15.tex.
Source for new text: external_audits/humanized/gemini,grok humanized.txt,
Gemini section (lines 1-532), adopted verbatim except:
 - LaTeX-mechanical adaptations (macros \\kmu, \\RR, \\CC, \\citep keys,
   \\S\\ref, --- dashes, 72-col wrapping);
 - Gemini's unaudited numbers excluded (decile dispersions +/-0.12/0.08,
   PaxDb p 1.2e-12, model sizes 2712/1366, noise-floor 1e-11..1e-14,
   100.0000%-style token changes) -- v15's audited numbers kept;
 - v15-only measured caveats retained where Gemini is silent;
 - ASCII-art figures from the audit NOT adopted (forbidden pattern).
"""

SPLICES_A = []

# ---------------------------------------------------------------- S0 header
SPLICES_A.append(("header-note", (
"%  Merged-register round (v14 -> v15): joint evaluation of the two"),
(
"""%  Universal Gemini-prose adoption round (v15 -> v16): per the author
%  directive, Gemini's rewrite (external_audits/humanized/gemini,grok
%  humanized.txt, lines 1-532) is adopted VERBATIM wherever it
%  provides text -- abstract (rebuilt on Gemini's own abstract,
%  compressed to the 255-word cap, opening with Gemini's first
%  sentence), title and keywords, intro opening + five-findings claim
%  list, Sec. 2 setup/definitions/in-words glosses, the value--flux
%  coupling statement, Sec. 3 opening + TV-failure explanation,
%  holonomy proposition, Sec. 4 validation narratives, Sec. 5
%  association/tie-break/path-robustness/protein-layer narratives,
%  Discussion restructured into Gemini's three subsections, and the
%  Methods leads. Gemini's proof variants are NOT adopted (they drop
%  verified detail; v15's complete proofs retained). Gemini's
%  unaudited numbers (decile dispersions, PaxDb p-value, model sizes,
%  noise-floor compression, 100.0000% token form) are excluded per
%  the v15-round adjudication; every v15 audited number is kept.
%  ASCII-art figures from the audit are not adopted. Numbers
%  verified: audit_v24 301/301; completeness vs v15 verified by
%  verify_v16_completeness.py.
%  Merged-register round (v14 -> v15): joint evaluation of the two"""),
))

# ------------------------------------------------------- S1 title + hyperref
SPLICES_A.append(("title-block", (
"""\\hypersetup{
 pdftitle={A Measure-Theoretic Discrete Curvature Framework for
           Metabolic Gene Sensitivity: From Active-Set Geometry to
           Transcriptional Response},
 pdfauthor={Amin Abaee},
 pdfsubject={parametric FBA, discrete curvature measures, active-set
             stratification, metabolic gene sensitivity},
 pdfkeywords={flux balance analysis, discrete curvature, active
              set, parametric linear programming, flux rerouting,
              epistasis}}

\\title{A Measure-Theoretic Discrete Curvature Framework for Metabolic
       Gene Sensitivity: From Active-Set Geometry to Transcriptional
       Response}"""),
(
"""\\hypersetup{
 pdftitle={A Geometric Theory of Metabolic Flux Rerouting: How
           Active-Set Curvature Predicts Transcriptional Regulation
           and Protein-Layer Buffering},
 pdfauthor={Amin Abaee},
 pdfsubject={parametric FBA, active-set curvature, metabolic flux
             rerouting, transcriptional regulation, translational
             buffering},
 pdfkeywords={flux balance analysis, metabolic rerouting,
              active-set curvature, transcriptional regulation,
              translational buffering, epistasis}}

\\title{A Geometric Theory of Metabolic Flux Rerouting: How Active-Set
       Curvature Predicts Transcriptional Regulation and
       Protein-Layer Buffering}"""),
))

# ------------------------------------------------------------- S2 keywords
SPLICES_A.append(("keywords", (
"""\\noindent\\textbf{Keywords:} flux balance analysis; discrete curvature;
active set; parametric linear programming; flux rerouting; epistasis"""),
(
"""\\noindent\\textbf{Keywords:} flux balance analysis; metabolic
rerouting; active-set curvature; transcriptional regulation;
translational buffering; epistasis"""),
))

# ------------------------------------------------------------- S3 abstract
SPLICES_A.append(("abstract", (
"""\\begin{abstract}
\\noindent
When a cell's environment changes, its metabolic network reroutes.
Parametric flux balance analysis defines a continuous, piecewise-affine
mapping from environmental and genetic constraints to optimal fluxes.
We measure how this map bends. Its distributional second derivative
is a matrix-valued Radon measure concentrated on the boundaries
between active constraint sets --- the discrete curvature carrier of
rerouting geometry. Parameter loops accumulate drift linearly in loop
size (slope $1.00$; smooth maps scale quadratically), and $93.4$--$100.0\\%$
of second-order response mass concentrates on active-set transitions.
We establish a refinement--resolution bridge to classical differential
geometry: under mesh refinement the measure converges weakly to the
smooth curvature density, dual-cell reconstructions converge strongly
in $L^1$, and total-variation convergence fails generically. A
resolution parameter $\\sigma$ delineates discrete and smooth regimes
across the window $h \\ll \\sigma \\ll L_{\\mathrm{var}}$
($h$: mesh scale; $L_{\\mathrm{var}}$: smooth-variation scale).

From this measure we derive a gene-level sensitivity metric, $\\kmu$.
In \\emph{E.~coli} (M3D compendium, $424$ genes), $\\kmu$ predicts
transcriptional response to carbon depletion ($r = +0.395$,
$p = 2.6 \\times 10^{-17}$; partial $r = +0.269$ controlling for
baseline expression). The association is robust to tie-breaking
convention and random-panel sampling. Strikingly, it vanishes at
the protein layer ($r = -0.083$ across $366$ genes in matched
quantitative proteomics): cells transcribe rerouting potential while
buffering its translation. Finally, double-knockout epistasis mirrors
active-set footprint overlap ($\\rho_S = 0.865$), and cyclical genotype
modifications induce permanent phenotypic memory: $66\\%$ of loops fail
to revert. Our results unify multi-parametric linear programming,
discrete differential geometry, and transcriptional regulation into
one predictive framework.
\\end{abstract}"""),
(
"""\\begin{abstract}
\\noindent
Constraint-based models such as flux balance analysis (FBA) predict cellular
metabolic states by solving linear optimization problems. When
nutrients or enzyme capacities vary continuously, optimal fluxes do
not change smoothly but follow piecewise-linear trajectories, changing slope
abruptly at bottlenecks. Here we show that the true
``curvature'' of this response is not an ordinary function but a
discrete measure concentrated on the boundary interfaces where active
constraints switch: the fundamental carrier of a network's rerouting
geometry. Path-dependent memory (holonomy) scales linearly with
perturbation size (slope $1.00$; smooth systems quadratic), and
$93.4$--$100.0\\%$ of second-order adjustment concentrates at discrete
bottleneck transitions. A bridge connects these switches to smooth
differential geometry: under grid refinement they converge weakly to
smooth curvature densities, dual-cell reconstructions strongly in
$L^1$, but total variation fails to converge generically (grid
anisotropy), defining the resolution window ($h \\ll \\sigma \\ll
L_{\\mathrm{var}}$).

Integrating this measure along physiological paths yields a
parameter-free gene sensitivity metric, $\\kmu$: each enzyme's
rerouting burden. In carbon-starved \\emph{E.~coli}, $\\kmu$ predicts
transcriptional log-fold changes across $424$ genes ($r = +0.395$,
$p = 2.6 \\times 10^{-17}$; partial $r = +0.269$), robust across
tie-breaking rules and stress axes. The association vanishes at the
protein layer ($r = -0.083$ across $366$ genes in matched quantitative
proteomics): cells transcribe standby capacity for rerouting,
buffering protein synthesis. Double-knockout epistasis mirrors
active-set boundary overlaps ($\\rho_S = 0.865$), and cyclic
perturbations leave lasting metabolic memory ($66\\%$ non-reverting).
Our framework unites linear programming, discrete geometry, and
transcriptional regulation into an accessible, predictive foundation
for metabolic systems biology.
\\end{abstract}"""),
))

# ---------------------------------------------------------- S4 intro opening
SPLICES_A.append(("intro-opening", (
"""Genome-scale metabolic networks must continuously balance conflicting
physiological demands as nutrient supplies, oxygen tension, and enzyme
capacities shift around them. Flux balance analysis and its extensions
predict the phenotypic end-states of this coordination by constrained
optimization \\citep{varma1994, orth2010, lewis2010}, and the
first-order response of the resulting optimum --- marginal growth
yields and shadow prices --- is classical, analyzed under the name of
phenotype phase planes \\citep{edwards2001, ibarra2002}. The
higher-order question --- how the optimal fluxes reroute when the
environment shifts --- is the subject of this paper. Its answer
cannot be a classical second derivative: the optimal response is
piecewise affine, so that derivative vanishes away from the
constraint boundaries and is undefined at them, and the second-order
response concentrates at the discrete transitions where the active
constraint set switches. The object that carries it is a measure ---
the distributional second derivative, in the language of geometric
measure theory."""),
(
"""Genome-scale metabolic modeling relies heavily on flux balance
analysis (FBA) to predict how cells allocate metabolic resources to
maximize growth or maintain physiological function \\citep{varma1994,
orth2010, lewis2010}. In realistic environments, nutrient
availabilities and enzymatic capacities fluctuate continuously.
Mathematically, tracking optimal metabolic states under varying
constraints is governed by parametric linear programming
\\citep{borrelli2003}. A defining property of linear optimization is
that the relationship between external parameters (such as nutrient
uptake rates) and optimal reaction fluxes is \\emph{piecewise linear}
(or more formally, piecewise affine).

This piecewise structure means that parameter space is partitioned
into polyhedral ``chambers.'' Inside any single chamber, the set of
active governing constraints --- the network's operational
bottlenecks --- remains unchanged, and fluxes adjust in simple linear
proportion to parameter changes. However, as soon as a nutrient
becomes fully depleted or an enzyme hits its maximum capacity, the
network crosses a boundary into an adjacent chamber. Across this
boundary interface, the active set of constraints switches, causing
the system to abruptly redirect fluxes through alternative pathways.

In classical calculus, the sensitivity of a nonlinear system to
perturbations is captured by its second derivatives (its Hessian
matrix, or curvature). But for a piecewise-linear system, the second
derivative is zero almost everywhere inside the chambers and
undefined along the boundaries. Consequently, traditional smooth
calculus cannot characterize metabolic rerouting. In this work, we
resolve this limitation using modern geometric measure theory. We
demonstrate that the second derivative of an optimal metabolic flux
map is a \\emph{matrix-valued Radon measure} supported on the boundary
facets between active-set chambers. Rather than being an intractable
discontinuity, this measure provides the natural mathematical
language for metabolic rerouting."""),
))

# ------------------------------------------------------------ S5 the object
SPLICES_A.append(("intro-object", (
"""\\paragraph{The object.}
Let a metabolic network with $m$ reactions be operated by flux balance
analysis \\citep{varma1994, orth2010} with parameters $\\theta \\in \\Theta \\subset \\RR^p$
(uptake bounds, knockdown scalings) entering the constraints
affinely. The optimal flux map $v : \\Theta \\to \\RR^m$ is continuous
and piecewise affine (parametric linear programming
\\citep{borrelli2003}): as the parameters move, the optimum is a fixed
linear function of them within each region of parameter space; when a
nutrient becomes depleted or an enzyme capacity saturates, the path
crosses into the neighboring region, the set of constraints that hold
with equality (the \\emph{active set} --- the network's operational
bottlenecks) switches, and the slope of $v$ changes. These
boundaries --- the active-set strata of the constraint complex --- are
where the map bends. Its distributional second derivative
$\\mu = D^2 v$ is therefore not a function but a \\emph{measure},
concentrated on the switching boundaries: the discrete curvature
carrier of the network's rerouting geometry. Degeneracy sharpens the
choice of object: when the optimum is non-unique, classical
sensitivity analysis still sees the value layer (Danskin envelopes
\\citep{danskin1967}), but the reroutings inside optimal faces are
invisible to it and the flux map itself becomes
selection-dependent --- which is why the deterministic lexicographic
tie-break is declared as part of the metric (Remark~\\ref{rem:lock})
rather than left to the solver."""),
(
"""\\paragraph{The object.}
Let a metabolic network with $m$ reactions be operated by flux balance
analysis \\citep{varma1994, orth2010} with parameters $\\theta \\in \\Theta \\subset \\RR^p$
(uptake bounds, knockdown scalings) entering the constraints
affinely. The optimal flux map $v : \\Theta \\to \\RR^m$ is continuous
and piecewise affine (parametric linear programming
\\citep{borrelli2003}), and its distributional second derivative
$\\mu = D^2 v$ is a measure concentrated on the switching boundaries:
the discrete curvature carrier of the network's rerouting geometry.
Degeneracy sharpens the choice of object: when the optimum is
non-unique, classical sensitivity analysis still sees the value layer
(Danskin envelopes \\citep{danskin1967}), but the reroutings inside
optimal faces are invisible to it and the flux map itself becomes
selection-dependent --- which is why the deterministic lexicographic
tie-break is declared as part of the metric (Remark~\\ref{rem:lock})
rather than left to the solver."""),
))

# ------------------------------------------------------ S6 claim structure
SPLICES_A.append(("claim-structure", (
"""\\paragraph{The claim structure.}
This manuscript establishes, in order:
\\begin{enumerate}[label=(\\roman*)]
\\item the atom structure and weak convergence of $\\mu_h$
      under refinement (Theorem~\\ref{thm:Bprime}, \\S\\ref{sec:theoremB}), with an exact counterexample calculus delimiting what is provable (weak convergence, strong cell-wise reconstruction) from what fails (total-variation convergence);
\\item the two-layer separation: the codimension-one Hessian
      layer is the unbiased curvature estimator; the codimension-two
      angle-defect layer converges to the Gauss-map area density with an
      exact sec-law bias (Proposition~\\ref{prop:seclaw});
\\item the regime dichotomy: piecewise-affine maps with fixed
      kink complexes produce $O(\\varepsilon)$ loop holonomy (measured slope
      $1.00$) where smooth maps produce $O(\\varepsilon^2)$;
\\item the value function $\\Phi = c_{\\mathrm{bio}}^\\top v^*$
      (the maximum achievable growth rate)
      is the canonical tie-break-free carrier, with shadow-price jumps
      measurable to $6$--$7$ digits against Danskin envelopes;
\\item the measure-derived metric $\\kmu$ predicts
      carbon-depletion transcriptional response ($r = +0.395$),
      generalizes to oxygen-limitation and carbon-switch trajectories
      with matched responses ($r = +0.32$, $+0.22$; \\S\\ref{sec:v7}), is
      robust to the tie-break convention: $r \\in [+0.386, +0.396]$
      across five selection rules (\\S\\ref{sec:v8}), is buffered at the
      protein layer
      (\\S\\ref{sec:empirical}), and its event measures stabilize at
      the Glivenko--Cantelli rate across random panels (\\S\\ref{sec:e32}).
\\end{enumerate}"""),
(
"""\\paragraph{The claim structure.}
This manuscript establishes five interconnected findings:
\\begin{enumerate}[label=(\\roman*)]
\\item \\textbf{The geometry of metabolic curvature
      (Section~\\ref{sec:measure}):} we prove that the distributional
      second derivative of the optimal flux map decomposes into
      discrete, rank-one jump tensors along active-set switching
      boundaries (Theorem~\\ref{thm:Bprime}), and that the cell's
      objective value function (the maximum achievable growth rate
      $\\Phi = c_{\\mathrm{bio}}^\\top v^*$) and its internal reaction
      fluxes ($v^*$) belong to two distinct geometric layers connected
      by an exact coupling identity, $D^2 \\Phi = \\sum_r c_r D^2
      v^*_r$ (Theorem~\\ref{thm:coupling}); the value layer is the
      canonical tie-break-free carrier, with shadow-price jumps
      measurable to $6$--$7$ digits against Danskin envelopes.
\\item \\textbf{The refinement--resolution bridge
      (Section~\\ref{sec:theoremB}):} we examine how discrete
      active-set switches relate to smooth differential models ---
      discrete jump measures converge weakly to smooth curvature
      densities under spatial refinement, while their total variation
      fails to converge due to grid-alignment artifacts (triangulation
      anisotropy) --- and derive the precise resolution window
      ($h \\ll \\sigma \\ll L_{\\mathrm{var}}$) required for smooth
      approximations to be physically meaningful, with the two-layer
      separation of Proposition~\\ref{prop:seclaw} (the codimension-one
      Hessian layer the unbiased curvature estimator, the
      angle-defect layer carrying an exact sec-law bias) delimiting
      which discrete curvature is the right one to refine.
\\item \\textbf{Linear holonomy scaling (Sections~\\ref{sec:measure}
      and~\\ref{sec:computational}):} parameter loops in metabolic
      networks accumulate path-dependent discrepancies (holonomy) that
      scale \\emph{linearly} ($O(\\varepsilon)$) with perturbation diameter
      --- an empirical slope of $1.00$ --- in contrast to the
      quadratic scaling ($O(\\varepsilon^2)$) of smooth systems, and
      sequential gene knockouts frequently fail to commute, leaving
      permanent phenotypic memory in $66\\%$ of tested closed cycles.
\\item \\textbf{Predicting transcriptional regulation
      (Section~\\ref{sec:empirical}):} integrating the curvature
      measure along physiological trajectories yields the
      parameter-free gene sensitivity metric $\\kmu$, which across
      $424$ metabolic genes in \\emph{E.~coli} accurately predicts
      transcriptional induction during carbon starvation
      ($r = +0.395$, $p = 2.6 \\times 10^{-17}$), generalizes to
      oxygen-limitation and carbon-switch trajectories with matched
      responses ($r = +0.32$, $+0.22$; \\S\\ref{sec:v7}), and remains
      robust across five distinct optimization tie-breaking protocols
      ($r \\in [+0.386, +0.396]$; \\S\\ref{sec:v8}), with event measures
      stabilizing at the Glivenko--Cantelli rate across random panels
      (\\S\\ref{sec:e32}).
\\item \\textbf{The translational buffering mechanism
      (Section~\\ref{sec:empirical}):} this predictive power fails
      completely at the protein layer ($r = -0.083$ across $366$ genes
      in matched quantitative proteomics), providing genome-scale
      evidence for a model in which cells transcribe mRNA to maintain
      pathway rerouting capacity on standby, while buffering
      energy-intensive translation until post-translational or
      metabolic signals require it.
\\end{enumerate}"""),
))
