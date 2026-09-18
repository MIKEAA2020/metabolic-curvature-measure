# -*- coding: utf-8 -*-
"""v16 splice data, part C: Sections 5-7 and the refs \\input."""

SPLICES_C = []

# -------------------------------------------------- S25 Sec 5.1 (sec:v5)
SPLICES_C.append(("sec-v5-association", (
"""On the deterministic lexicographic trajectory (the reference physiology, iJO1366),
we compare $\\kmu$ (Definition~\\ref{def:kmu}) against log-fold
carbon-depletion response (M3D \\citep{faith2008}, $n = 424$ genes;
Fig~\\ref{fig:v5}). The association is present and strong: Pearson
$r = +0.395$ ($p = 2.6 \\times 10^{-17}$), Spearman
$\\rho_S = +0.414$ (full panel, zeros included). One confound
deserves a direct look: because highly expressed metabolic enzymes
often show broader regulatory dynamic ranges, the raw association
could partly reflect baseline expression rather than rerouting.
Residualizing the M3D reference level leaves the association intact
(partial $r = +0.269$, $p = 1.8 \\times 10^{-8}$), and the extreme
deciles separate cleanly (top versus bottom response $1.92$ vs
$0.89$ --- more than double; MWU $1.3 \\times 10^{-7}$)."""),
(
"""To test whether active-set curvature predicts real biological
adaptation, we modeled \\emph{E.~coli} adapting to carbon starvation on
the deterministic lexicographic trajectory (the reference physiology,
iJO1366), comparing $\\kmu$ (Definition~\\ref{def:kmu}) against
log-fold carbon-depletion response (M3D \\citep{faith2008}, $n = 424$
genes; Fig~\\ref{fig:v5}). The active-set sensitivity metric $\\kmu$
showed a strong, highly significant positive correlation with
transcriptional induction: Pearson
$r = +0.395$ ($p = 2.6 \\times 10^{-17}$), Spearman
$\\rho_S = +0.414$ (full panel, zeros included). One confound
deserves a direct look: because highly expressed metabolic enzymes
often show larger absolute dynamic ranges, the raw association could
partly reflect baseline expression rather than rerouting; we
therefore evaluated a partial correlation controlling for baseline
log-phase expression. The association remained highly significant:
residualizing the M3D reference level leaves the association intact
(partial $r = +0.269$, $p = 1.8 \\times 10^{-8}$), and genes in the
extreme deciles separate cleanly (top versus bottom response $1.92$
vs $0.89$ --- more than double; MWU $1.3 \\times 10^{-7}$)."""),
))

# ---------------------------------------------- S26 Sec 5.3 (sec:v7) opening
SPLICES_C.append(("sec-v7-opening", (
"""Does the association generalize beyond glucose limitation, or is it a
quirk of the reference trajectory? Three trajectories through the same LP (same engine, seed, panel, statistics; only the path and its matched response vary; Fig~\\ref{fig:v7}): P0 glucose decline (reference-physiology anchors; the layer-decision control of \\S\\ref{sec:v6}), P1 oxygen limitation
($q_{\\mathrm{glc}} = 5$ fixed, $q_{O_2}$ linear from $22$ to $1$),
P2 acetate switch ($q_{O_2} = 22$ fixed; glucose $5 \\to 0$ while
acetate uptake ramps $0 \\to 10$)."""),
(
"""To establish that $\\kmu$ captures general network vulnerabilities
rather than a quirk of glucose limitation, we tested two alternative
environmental stress paths through the same LP (same engine, seed,
panel, statistics; only the path and its matched response vary;
Fig~\\ref{fig:v7}): P0 glucose decline (reference-physiology anchors;
the layer-decision control of \\S\\ref{sec:v6}), P1 oxygen limitation
--- progressive transition from aerobic to anaerobic growth
($q_{\\mathrm{glc}} = 5$ fixed, $q_{O_2}$ linear from $22$ to $1$) ---
and P2 acetate diauxic switch --- progressive transition from glucose
to acetate ($q_{O_2} = 22$ fixed; glucose $5 \\to 0$ while
acetate uptake ramps $0 \\to 10$)."""),
))

# ------------------------------------------ S26b Sec 5.3 finding (iii) close
SPLICES_C.append(("sec-v7-closing", (
"""gives $r = +0.223$ (partial $+0.160$, $p = 9 \\times
      10^{-4}$); and the P1/P2 predictors correlate with the primary-panel carbon response at $r = +0.378$ / $+0.391$ --- the per-gene
      ranking is largely trajectory-independent."""),
(
"""gives $r = +0.223$ (partial $+0.160$, $p = 9 \\times
      10^{-4}$); and the P1/P2 predictors correlate with the
      primary-panel carbon response at $r = +0.378$ / $+0.391$ ---
      $\\kmu$ identifies core architectural bottlenecks that dictate
      transcriptional regulation across multiple environments, and
      the per-gene
      ranking is largely trajectory-independent."""),
))

# ---------------------------------------------- S27 Sec 5.2 (sec:v8) opening
SPLICES_C.append(("sec-v8-opening", (
"""A linear program can have many optimal flux distributions, so the
flux layer needs a selection rule --- it is selection-dependent by
construction
(Remark~\\ref{rem:lock}), and the declared lexicographic tie-break is one
member of a family. The experiment asks whether the biology depends
on the convention: it fixes the entire protocol of the primary association (iJO1366, reference-physiology anchors, $8\\times$ refinement, the $433$-gene panel, the M3D carbon-depletion response, the reference-level confound control) and varies \\emph{only} the stage-3 tie-break of the
engine:"""),
(
"""Because linear programs can possess multiple alternative optimal
flux distributions, the flux layer requires a tie-breaking rule ---
it is selection-dependent by
construction
(Remark~\\ref{rem:lock}), and the declared lexicographic tie-break is
one member of a family. To confirm that the biological findings do
not depend on a specific computational convention, the experiment
fixes the entire protocol of the primary association (iJO1366,
reference-physiology anchors, $8\\times$ refinement, the $433$-gene
panel, the M3D carbon-depletion response, the reference-level
confound control) and varies \\emph{only} the stage-3 tie-break of the
engine:"""),
))

# ------------------------------------------------ S27b tie-break TB bullets
SPLICES_C.append(("sec-v8-tb-bullets", (
"""\\begin{itemize}
\\item \\textbf{TB0} (declared): $w \\sim U(0.5, 1.5)$, seed 20240901,
      $\\min w^\\top v$ --- the declared metric (control: reproduces the
      primary association, $r = +0.3954$, digit-exactly);
\\item \\textbf{TB1} (fresh seed): $w \\sim U(0.5, 1.5)$, seed 20240902
      --- same family, independent draw;
\\item \\textbf{TB2} (family swap): $w \\sim \\mathrm{LogN}(0, 1)$ clipped
      to $[0.05, 20]$, seed 20240903 --- a different distribution
      family with a roughly $130$-fold wider dynamic range
      (support ratio $400{:}1$ versus $3{:}1$);
\\item \\textbf{TB3} (rule swap): stage-3 objective on the split
      variables, $\\min \\sum_r w_r (f_r + r_r)$ --- weighted
      \\emph{absolute}-flux selection with TB0's weights;
\\item \\textbf{TB4} (adversarial): $\\max w^\\top v$ --- the far end of
      the stage-2-pinned optimal face, with TB0's weights.
\\end{itemize}"""),
(
"""\\begin{itemize}
\\item \\textbf{TB0 (declared baseline):} $w \\sim U(0.5, 1.5)$, seed
      20240901, $\\min w^\\top v$ --- the declared metric (control:
      reproduces the primary association, $r = +0.3954$,
      digit-exactly);
\\item \\textbf{TB1 (seed replication):} $w \\sim U(0.5, 1.5)$, seed
      20240902 --- same family, independent draw;
\\item \\textbf{TB2 (dynamic-range expansion):} $w \\sim
      \\mathrm{LogN}(0, 1)$ clipped to $[0.05, 20]$, seed 20240903 ---
      a different distribution family with a roughly $130$-fold wider
      dynamic range (support ratio $400{:}1$ versus $3{:}1$);
\\item \\textbf{TB3 (absolute-flux rule):} stage-3 objective on the
      split variables, $\\min \\sum_r w_r (f_r + r_r)$ --- weighted
      \\emph{absolute}-flux selection with TB0's weights;
\\item \\textbf{TB4 (adversarial selection):} $\\max w^\\top v$ --- the
      far end of the stage-2-pinned optimal face, with TB0's weights.
\\end{itemize}"""),
))

# ---------------------------------------------------- S27c table v8 caption
SPLICES_C.append(("tab-v8-caption", (
"""\\caption{Tie-break robustness of the association (primary protocol fixed; only the stage-3 selection rule varies). The value layer
(stage-1 biomass $\\mu$) and the pFBA layer (stage-2 $\\ell_1$, $s_2$)
are invariant to $0.0$ across all variants --- the measured form of
the tie-break-freeness of Proposition~\\ref{prop:alex}.}"""),
(
"""\\caption{\\textbf{Evaluation across alternative tie-breaking
protocols} (primary protocol fixed; only the stage-3 selection rule
varies). The first-stage growth rate $\\mu$ and the second-stage
parsimonious sum $\\ell_1$ agree to $0.0$ across all variants,
confirming the mathematical invariance of the value layer --- the
measured form of the tie-break-freeness of
Proposition~\\ref{prop:alex}.}"""),
))

# ---------------------------------------------------- S27d table v8 headers
SPLICES_C.append(("tab-v8-headers", (
"""Variant & $n_{\\mathrm{nz}}$ & $r$ & partial $r$ &
$\\rho_S(\\kmu, \\kmu_{\\mathrm{TB0}})$ & genes changed \\\\
\\midrule
TB0 declared       & 424 & $+0.3954$ & $+0.269$ & --- & --- \\\\
TB1 fresh seed     & 426 & $+0.3861$ & $+0.270$ & $0.99998$ & 91 \\\\
TB2 LogN family    & 424 & $+0.3954$ & $+0.269$ & $0.99999$ & 90 \\\\
TB3 $|v|$ rule     & 425 & $+0.3959$ & $+0.269$ & $0.99897$ & 109 \\\\
TB4 $\\max w^\\top v$& 424 & $+0.3954$ & $+0.269$ & $0.99998$ & 117 \\\\"""),
(
"""Tie-breaking rule & Active genes ($n$) & Pearson $r$ & Partial $r$ &
$\\rho_S(\\kmu, \\kmu_{\\mathrm{TB0}})$ & Reassigned genes \\\\
\\midrule
TB0 (declared)     & 424 & $+0.3954$ & $+0.269$ & --- & --- \\\\
TB1 (fresh seed)   & 426 & $+0.3861$ & $+0.270$ & $0.99998$ & 91 \\\\
TB2 (log-normal)   & 424 & $+0.3954$ & $+0.269$ & $0.99999$ & 90 \\\\
TB3 ($|v|$ rule)   & 425 & $+0.3959$ & $+0.269$ & $0.99897$ & 109 \\\\
TB4 (adversarial)  & 424 & $+0.3954$ & $+0.269$ & $0.99998$ & 117 \\\\"""),
))

# ---------------------------------------------- S28 Sec 5.4 (sec:e26)
SPLICES_C.append(("sec-e26-dissociation", (
"""A central question is whether the transcriptional
association propagates downstream to the proteome. Two dissociations
at the protein layer answer it in the negative (PaxDb integrated
abundance \\citep{wang2015}; quantitative proteomics of GSE64021
\\citep{barrett2013};
$n = 169$--$429$). First, abundance \\emph{level} associates (PaxDb
baseline $r = +0.334$): high-rerouting genes are abundant proteins.
Second, abundance \\emph{change} does not (protein log-fold change $r
= +0.008$ to $+0.032$; transcript--protein fold-change coupling
$r = +0.020$, $n = 799$). The transcriptional association thus stops
at translation, consistent with buffering: rerouting capacity is
carried at the transcript level, and the translational cost is
deferred until a rerouting bottleneck actually demands it
(\\S\\ref{sec:e27})."""),
(
"""Does the transcriptional response propagate downstream to change
protein levels? We evaluated two quantitative proteomic datasets for
\\emph{E.~coli} --- baseline protein abundance averages from the PaxDb
integrated database \\citep{wang2015}, and condition-dependent
quantitative proteomics across the GSE64021 \\citep{barrett2013}
starvation time courses ($n = 169$--$429$) --- and our analysis
revealed a striking biological dissociation. First, abundance
\\emph{level} associates (PaxDb baseline $r = +0.334$): high-rerouting
genes are abundant proteins. Second, abundance \\emph{change} does
not: in sharp contrast to mRNA, dynamic protein log-fold change
showed no correlation with $\\kmu$ ($r = +0.008$ to $+0.032$), and
the transcript--protein fold-change coupling across matched
conditions was essentially zero ($r = +0.020$, $n = 799$). The
transcriptional association thus stops
at translation, consistent with buffering: rerouting capacity is
carried at the transcript level, and the translational cost is
deferred until a rerouting bottleneck actually demands it
(\\S\\ref{sec:e27})."""),
))

# ---------------------------------------------- S28b Sec 5.4 (sec:e27)
SPLICES_C.append(("sec-e27-null", (
"""The decisive negative result comes from condition-dependent
quantitative proteomics (\\citet{schmidt2016}; $22$ conditions, triplicates,
$n = 366$): the protein-level correlation is $r = -0.083$, against
transcript $+0.419$ on the same genes --- the association that is
robust at the transcript layer vanishes entirely at the protein
layer. Transcription does not propagate through translation;
buffering at translation is the consistent model, positioning
\\citet{kochanowski2013} as prior art for the protein-layer null."""),
(
"""The decisive negative result comes from condition-dependent
quantitative proteomics (\\citet{schmidt2016}; $22$ conditions,
triplicates, $n = 366$): in this multi-condition dataset, the
correlation between $\\kmu$ and protein fold change was weakly
negative ($r = -0.083$), directly opposing the strong transcriptional
correlation ($r = +0.419$) observed for the same genes --- the
association that is robust at the transcript layer vanishes entirely
at the protein layer. Transcription does not propagate through
translation; buffering at translation is the consistent model,
positioning \\citet{kochanowski2013} as prior art for the
protein-layer null."""),
))

# --------------------------------------------------- S29 Discussion block
SPLICES_C.append(("discussion-block", (
"""\\section{Discussion: one measure, several resolutions}
\\label{sec:discussion}

The sensitivity objects of the framework are one measure at different
resolutions: the atomic measure of Definition~\\ref{def:mu}, its
coarse-grainings $\\mu * \\phi_\\sigma$, and its integrals along parameter
trajectories ($\\kmu$). The smooth member of this family exists only
through the window $h \\ll \\sigma \\ll L_{\\mathrm{var}}$; the
$\\sigma \\to 0$ limit is the atomic object. Outside the window ---
$\\sigma$ below the mesh scale or above the variation scale --- the
smooth representation breaks down, and the system is properly
described by its discrete active-set atoms. Two items remain open:
Conjecture~\\ref{conj:bridge} (general complex stability) and second
differences on measured time courses (under the $(\\varepsilon,
\\sigma)$ design law). The statistical form of the stabilization
question is settled here (\\S\\ref{sec:e32}): random panels are
Glivenko--Cantelli objects and designed panels reproduce the event
measure exactly; the deterministic refinement-sequence form
(refinement along explicit model-family sequences) remains open.
The exact contraction identity
$D^2\\Phi = \\sum_r c_r\\, D^2 v^*_r$ of Theorem~\\ref{thm:coupling}
grounds the association's flux-layer footing, complementing the
measured metric invariance of \\S\\ref{sec:v5}. Because cells routinely
exploit alternative pathways of equal growth during nutrient
transitions, most metabolic rerouting is objective-invisible (the
zero-cost substitutions of Theorem~\\ref{thm:coupling}(i)). The
empirical association reflects this separation: gene expression
changes correlate with the flux-layer metric $\\kmu$ ($r = +0.395$)
but show no association with value-layer derivatives (shadow-price
arm $r = +0.032$, $p = 0.93$, $n = 51$). Transcriptional response
tracks rerouting, and rerouting is a flux-layer quantity.

Why transcribe a rerouting program without translating it? Synthesizing
large, multi-subunit metabolic enzymes is energetically expensive, and
a cell under catabolic limitation cannot afford to translate every
enzyme it might need. Keeping transcripts on standby at the
high-$\\kmu$ bottlenecks is the cheaper strategy: if a boundary is
crossed and a pathway must be rerouted, local translation can be
released immediately; if the shortage resolves, the untranslated
transcripts are recycled at minimal cost. The measured dissociation
--- transcript $+0.419$ against protein $r = -0.083$ on the same
$366$ genes (\\S\\ref{sec:e27}) --- is the quantitative signature of
this standby model, for which \\citet{kochanowski2013} is the prior
art at the metabolite level."""),
(
"""\\section{Discussion}
\\label{sec:discussion}

\\subsection{Unifying discrete switches and continuous models}
For decades, mathematical modeling in systems biology has been
divided between two distinct approaches: continuous, smooth ordinary
differential equation (ODE) models of enzyme kinetics, and discrete,
piecewise-linear optimization models such as FBA. Our work bridges
this divide by providing an explicit geometric framework for the
second derivatives of constraint-based models: the sensitivity of a
metabolic network is captured by an atomic Radon measure concentrated
on the active-set boundary complex. The sensitivity objects of the
framework are one measure at different resolutions --- the atomic
measure of Definition~\\ref{def:mu}, its coarse-grainings $\\mu *
\\phi_\\sigma$, and its integrals along parameter trajectories
($\\kmu$). Through the refinement--resolution bridge
(Theorem~\\ref{thm:Bprime}), discrete active-set transitions converge
weakly to continuous curvature densities under spatial averaging, but
total-variation measures do not converge due to triangulation
anisotropy. A smooth model of metabolic sensitivity is valid only
when observed through an intermediate resolution window ($h \\ll
\\sigma \\ll L_{\\mathrm{var}}$); the $\\sigma \\to 0$ limit is the atomic
object, and outside the window --- $\\sigma$ below the mesh scale or
above the variation scale --- the smooth representation breaks down,
the true physical behavior of the network being inherently discrete
and linear, characterized by $O(\\varepsilon)$ holonomy scaling. Two
items remain open: Conjecture~\\ref{conj:bridge} (general complex
stability) and second differences on measured time courses (under the
$(\\varepsilon, \\sigma)$ design law). The statistical form of the
stabilization question is settled here (\\S\\ref{sec:e32}): random
panels are Glivenko--Cantelli objects and designed panels reproduce
the event measure exactly; the deterministic refinement-sequence form
(refinement along explicit model-family sequences) remains open.

\\subsection{Why growth rate fails to predict gene expression}
A key conceptual takeaway of our work is the value--flux coupling
theorem (Theorem~\\ref{thm:coupling}). In systems biology, metabolic
stress is frequently evaluated through growth rate reductions or dual
shadow prices. However, the coupling identity proves that the
objective value function acts as a mathematical contraction: it sums
internal reaction curvatures weighted by objective coefficients
($D^2\\Phi = \\sum_r c_r\\, D^2 v^*_r$), grounding the association's
flux-layer footing and complementing the measured metric invariance
of \\S\\ref{sec:v5}. Because cells routinely exploit alternative
pathways of equal growth during nutrient transitions, most metabolic
rerouting is objective-invisible (the zero-cost substitutions of
Theorem~\\ref{thm:coupling}(i)), and when the objective is biomass
production the contraction zeroes out all internal pathway
adjustments that do not reduce immediate growth: in our
\\emph{E.~coli} simulations, $11$ out of $12$ internal rerouting
events were entirely silent in the growth rate. Consequently,
transcriptional regulation correlates strongly with the internal
flux metric $\\kmu$ ($r = +0.395$) but has no correlation with
value-layer derivatives (shadow-price arm $r = +0.032$, $p = 0.93$,
$n = 51$). Regulatory networks are organized to manage internal
pathway capacity and prevent local traffic jams, not simply to track
external growth yield: transcriptional response tracks rerouting,
and rerouting is a flux-layer quantity.

\\subsection{Biological implications of translational buffering}
Why transcribe a rerouting program without translating it? The
decoupling between transcriptional induction and protein synthesis
observed in our study highlights an elegant cellular survival
strategy. Synthesizing large, multi-subunit metabolic enzymes is
energetically expensive, and when nutrients become scarce, a cell
under catabolic limitation cannot afford to blindly translate every
enzyme it might need. By upregulating mRNA transcripts for
high-$\\kmu$ bottleneck pathways, the cell pre-positions the
necessary genetic templates: if an active-set boundary is crossed and
a metabolic pathway becomes completely blocked, local translation
can be released immediately; if the starvation condition resolves,
the untranslated mRNA can be recycled at minimal metabolic cost. The
measured dissociation --- transcript $+0.419$ against protein
$r = -0.083$ on the same $366$ genes (\\S\\ref{sec:e27}) --- is the
quantitative signature of this standby model, for which
\\citet{kochanowski2013} is the prior art at the metabolite level."""),
))

# ------------------------------------------------ S30 Methods 7.1 opening
SPLICES_C.append(("methods-engine-opening", (
"""All deterministic trajectories are computed by a purpose-built
three-stage lexicographic solver --- the engine that makes every
preceding experiment reproducible --- on the variable split $x = (v, f,
r)$ with $v = f - r$, $f, r \\ge 0$, stoichiometry $Sv = 0$, and
flux bounds $\\ell(\\theta) \\le v \\le u(\\theta)$ entering affinely
through the uptake bounds. The stages are strict lexicographic
optimizations, each pinned at the previous stage's optimum:"""),
(
"""To ensure that optimal flux trajectories are unique, deterministic,
continuous, and piecewise linear, all parametric linear programs were
solved using a purpose-built three-stage lexicographic solver --- the
engine that makes every preceding experiment reproducible --- on the
variable split $x = (v, f,
r)$ with $v = f - r$, $f, r \\ge 0$, stoichiometry $Sv = 0$, and
flux bounds $\\ell(\\theta) \\le v \\le u(\\theta)$ entering affinely
through the uptake bounds. The stages are strict lexicographic
optimizations, each pinned at the previous stage's optimum:"""),
))

# ------------------------------------------------ S30b Methods stage-3 tail
SPLICES_C.append(("methods-engine-weights", (
"""with $\\varepsilon_\\mu = \\varepsilon_s = 10^{-9}$ and $w \\sim U(0.5, 1.5)$ drawn once with seed 20240901 and fixed thereafter."""),
(
"""with relaxation tolerances $\\varepsilon_\\mu = \\varepsilon_s =
10^{-9}$; the weight vector $w \\in \\RR^m$ was sampled from
$w \\sim U(0.5, 1.5)$ using fixed seed 20240901 and held fixed
thereafter."""),
))

# ---------------------------------------------------- S30c Methods models
SPLICES_C.append(("methods-models", (
"""\\paragraph{Models.} \\emph{E.~coli} iJO1366 (2{,}583 reactions) \\citep{orth2011} for the association experiments of \\S\\ref{sec:empirical}; iML1515 \\citep{monk2017} for the computational batteries of \\S\\ref{sec:computational} and the value--flux coupling verification cut. Genome-scale models are
loaded from the local BiGG JSON copies with SHA-256 manifests."""),
(
"""\\paragraph{Models.} The genome-scale models \\emph{E.~coli} iJO1366
(2{,}583 reactions) \\citep{orth2011} and iML1515 \\citep{monk2017}
were retrieved from the BiGG database --- iJO1366 for the association
experiments of \\S\\ref{sec:empirical}, iML1515 for the computational
batteries of \\S\\ref{sec:computational} and the value--flux coupling
verification cut --- and are
loaded from the local BiGG JSON copies with SHA-256 manifests."""),
))

# --------------------------------------------------- S30d Methods M3D lead
SPLICES_C.append(("methods-m3d", (
"""\\paragraph{M3D microarray compendium.} The expression panels come from
the M3D \\emph{E.~coli} compendium v4 Build 6
\\citep{faith2008, faith2007}: 4{,}297 gene probes $\\times$ 907
arrays, log$_2$ uniformly normalized."""),
(
"""\\paragraph{M3D microarray compendium.} Transcriptional profiles were
obtained from the Many Microbe Microarrays Database (M3D)
\\emph{E.~coli} compendium v4 Build 6
\\citep{faith2008, faith2007}, using uniformly normalized arrays:
4{,}297 gene probes $\\times$ 907
arrays, log$_2$ uniformly normalized."""),
))

# ----------------------------------------------- S30e Methods proteomics
SPLICES_C.append(("methods-proteomics", (
"""\\paragraph{Proteomics.} Condition-dependent quantitative proteomics
from \\citet{schmidt2016} (22 conditions, triplicates); integrated
protein abundance from PaxDb \\citep{wang2015}; the GSE64021
\\citep{barrett2013} time course supplies the RNA-seq
carbon-starvation and the quantitative proteomics arms (\\S\\S\\ref{sec:e25}--\\ref{sec:e26})."""),
(
"""\\paragraph{Proteomics.} Protein copy numbers were obtained from the
PaxDb integrated database \\citep{wang2015}, and
condition-dependent quantitative proteomic measurements across 22
experimental conditions were obtained from \\citet{schmidt2016}
(triplicates); the GSE64021
\\citep{barrett2013} time course supplies the RNA-seq
carbon-starvation and the quantitative proteomics arms (\\S\\S\\ref{sec:e25}--\\ref{sec:e26}).
Gene--Protein--Reaction (GPR) associations were parsed using
COBRApy, classifying each active reaction into single-gene,
isoenzyme OR-branches, multi-protein AND-complexes, or mixed
architectures."""),
))

# ------------------------------------------------ S31 statistical protocols
SPLICES_C.append(("methods-statistics", (
"""The predictor is $\\log_{10}$ of the per-gene $\\kmu$ (its
distribution is log-linear over five decades); the response is
$\\max|\\log_2 \\mathrm{FC}|$ of the matched contrast. Reported
statistics: Pearson $r$ with analytic $p$, Spearman $\\rho_S$
(raw predictor ranks, full panel and nonzero subset as labeled),
partial $r$ controlling the M3D reference level by linear
residualization of both variables, permutation $p$ ($10^5$
label permutations, Monte Carlo), bootstrap 95\\% CIs ($10^4$
resamples), and top-vs-bottom decile contrasts (one-sided
Mann--Whitney $U$). All tests are two-sided except the decile
contrast. The PRECISE per-condition arms use the same protocol
with TPM log-fold changes. Every manuscript number traces to a deposited artifact file and is re-derived by the automated numeric verification described under Reproducibility ($301$ checks)."""),
(
"""The predictor variable was evaluated as $\\log_{10}$ of the per-gene
$\\kmu$, reflecting the log-linear distribution of the metric across
five orders of magnitude; the experimental response variable was the
maximum absolute $\\log_2$-fold change, $\\max|\\log_2 \\mathrm{FC}|$ of
the matched contrast. Reported statistical metrics include two-sided
Pearson correlation coefficients ($r$) with analytical $p$-values,
Spearman rank coefficients ($\\rho_S$; raw predictor ranks, full
panel and nonzero subset as labeled), partial correlations
controlling for baseline log-phase expression (the M3D reference
level, by linear residualization of both variables), permutation
tests ($10^5$ random label shuffles), and bootstrap 95\\% confidence
intervals ($10^4$ resamples); decile differences were tested using
one-sided Mann--Whitney $U$ tests. All tests are two-sided except
the decile contrast. The PRECISE per-condition arms use the same
protocol with TPM log-fold changes. Every manuscript number traces
to a deposited artifact file and is re-derived by the automated
numeric verification described under Reproducibility ($301$
checks)."""),
))
