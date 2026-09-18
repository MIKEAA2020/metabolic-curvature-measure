# -*- coding: utf-8 -*-
"""v16 splice data, part B: Section 2 core + Sections 3-4."""

SPLICES_B = []

# ---------------------------------------------------- S7 Sec 2.1 opening
SPLICES_B.append(("sec2-opening", (
"""In parametric flux balance analysis, environmental uptake limits and
metabolic capacities are modulated by a parameter vector $\\theta$ ---
uptake limits, knockdown scalings --- entering the lower and upper
bounds affinely. A network of $m$ reactions with stoichiometric matrix
$S \\in \\RR^{k \\times m}$, operating under steady state $Sv = 0$ and
bounds $\\ell(\\theta) \\le v \\le u(\\theta)$, therefore solves
\\begin{equation}\\label{eq:fba_lp}
\\max_{v}\\; c^\\top v
\\quad \\text{subject to} \\quad
Sv = 0, \\;\\; \\ell(\\theta) \\le v \\le u(\\theta),
\\end{equation}
with ties resolved by the three-stage engine of \\S\\ref{sec:methods}.
Multi-parametric linear programming theory \\citep{borrelli2003}
partitions parameter space into finitely many polyhedral chambers:
within each chamber the active set is constant and the optimal flux
is an affine function of $\\theta$, while the codimension-one facets
between adjacent chambers form the switching boundaries. When a
parameter path crosses one of these facets, the optimal flux vector
changes slope abruptly. The following definition collects all of
these slope changes into a single geometric object; read $u$ as the
optimal-flux map and $\\CC$ as its active-set complex."""),
(
"""Let a metabolic network be described by a stoichiometric matrix
$S \\in \\RR^{k \\times m}$ balancing $m$ reactions among $k$
metabolites, and let $\\theta \\in \\Theta \\subset \\RR^p$ represent a
vector of variable parameters --- such as nutrient uptake limits or
enzyme expression capacities --- which affinely dictate the lower and
upper flux bounds $\\ell(\\theta), u(\\theta) \\in \\RR^m$. The standard
flux balance analysis problem is formulated as
\\begin{equation}\\label{eq:fba_lp}
\\max_{v}\\; c^\\top v
\\quad \\text{subject to} \\quad
Sv = 0, \\;\\; \\ell(\\theta) \\le v \\le u(\\theta),
\\end{equation}
where $c \\in \\RR^m$ selects the biological objective (typically
biomass production), with ties resolved by the three-stage engine of
\\S\\ref{sec:methods}. From the theory of multi-parametric linear
programming \\citep{borrelli2003}, the parameter space $\\Theta$ is
divided into a collection of polyhedral regions called
\\emph{chambers}. Within each chamber $\\tau$, the subset of binding
constraints --- the network's \\emph{active set} --- is fixed, and the
optimal flux vector $v^*(\\theta)$ is governed by a local affine
equation $v^*(\\theta) = K_\\tau \\theta + d_\\tau$, where
$K_\\tau \\in \\RR^{m \\times p}$ is the local sensitivity matrix and
$d_\\tau \\in \\RR^m$ is an offset vector. When $\\theta$ crosses an
interface (facet $F$) separating two chambers $\\tau^-$ and $\\tau^+$,
one metabolic constraint releases while another becomes binding:
across this interface, the flux map remains continuous, but its slope
changes from $K_{\\tau^-}$ to $K_{\\tau^+}$. The following definition
collects all of these slope changes into a single geometric object;
read $u$ as the optimal-flux map and $\\CC$ as its active-set
complex."""),
))

# ------------------------------------------------------- S8 Definition 2.1
SPLICES_B.append(("def-mu", (
"""\\begin{definition}[Atomic curvature measure]\\label{def:mu}
Let $u : \\Omega \\to \\RR^m$ be continuous and piecewise affine on a
polyhedral complex $\\CC$ covering $\\Omega$. For each codimension-one facet
$F$ of $\\CC$ shared by cells $\\tau^-$, $\\tau^+$, let
$[\\nabla u]_F = \\nabla u|_{\\tau^+} - \\nabla u|_{\\tau^-}$, let $n_F$ be the
unit conormal oriented $\\tau^- \\to \\tau^+$, and let $|F|$ be the facet
measure. The \\emph{atomic curvature measure} is the matrix-valued Radon
measure
\\[
\\mu \\;=\\; D^2 u \\;=\\; \\sum_{F} A_F \\, \\delta_F,
\\qquad
A_F \\;=\\; [\\nabla u]_F \\otimes n_F \\; |F| \\;\\in\\; \\RR^{m \\times p \\times p}.
\\]
\\end{definition}"""),
(
"""\\begin{definition}[Atomic curvature measure]\\label{def:mu}
Let $u : \\Omega \\to \\RR^m$ be a continuous, piecewise-affine map
defined over a polyhedral complex $\\CC$ covering $\\Omega \\subset
\\RR^p$. Across each codimension-one boundary facet $F$ shared by
adjacent chambers $\\tau^-$ and $\\tau^+$, let
\\[
[\\nabla u]_F
= \\left.\\nabla u\\right|_{\\tau^+} - \\left.\\nabla u\\right|_{\\tau^-}
= K_{\\tau^+} - K_{\\tau^-}
\\;\\in\\; \\RR^{m \\times p}
\\]
denote the jump in the gradient. Let $n_F \\in \\RR^p$ be the unit
normal vector pointing from $\\tau^-$ to $\\tau^+$, and let $|F|$ denote
the $(p-1)$-dimensional area (Hausdorff measure) of the facet. The
\\emph{atomic curvature measure} is the matrix-valued Radon measure
\\[
\\mu \\;=\\; D^2 u \\;=\\; \\sum_{F} A_F \\, \\delta_F,
\\qquad
A_F \\;=\\; [\\nabla u]_F \\otimes n_F \\; |F| \\;\\in\\; \\RR^{m \\times p \\times p},
\\]
where $\\delta_F$ is the Dirac measure concentrated on facet $F$, and
$\\otimes$ denotes the outer tensor product.
\\end{definition}"""),
))

# --------------------------------------------------- S9 In-words gloss 2.1
SPLICES_B.append(("inwords-def-mu", (
"""In words: each codimension-one facet $F$ shared by two cells
$\\tau^-$ and $\\tau^+$ is one switching boundary; the jump matrix
$[\\nabla u]_F$ is the change of slope across it; $n_F$ orients the
jump, $|F|$ weights it by the size of the boundary, and $\\delta_F$
places unit mass on the boundary itself. The atom $A_F$ is thus the
slope change, oriented and weighted by the boundary it lives on --- an
impulse of curvature delivered on that wall --- and $\\mu$ is the sum
of all atoms, zero away from the switching boundaries. Curvature, in
this setting, is not spread over parameter space; it lives entirely on
the walls between chambers."""),
(
"""In simple terms: because the gradient is constant inside each
chamber, the second derivative vanishes everywhere except on the
boundary facets. On these facets, the second derivative acts as an
``impulse'' or directional shock wave whose magnitude and direction
are captured by the jump tensor $A_F$. For a one-dimensional path
($p=1$), these facets are simply the breakpoint coordinates where the
slope kinks, and $A_F$ is the scalar change in slope. Curvature, in
this setting, is not spread over parameter space; it lives entirely on
the walls between chambers."""),
))

# ------------------------------------------------------- S10 Sec 2.2 opening
SPLICES_B.append(("sec22-opening", (
"""Biological responses are typically observed along directed environmental
shifts --- progressive nutrient depletion, oxygen decline, a
carbon-source switch. The measure $\\mu$ lives on parameter space; to
connect it to genes, we integrate its mass along the trajectories that
environments actually take and attribute the accumulated mass to the
genes that govern the crossed boundaries."""),
(
"""In experimental biology, perturbations are typically applied along
continuous paths --- progressive glucose starvation over time, for
example. The measure $\\mu$ lives on parameter space; to determine how
much an environmental trajectory forces a specific gene's reactions to
reroute, we integrate its mass along the trajectories that
environments actually take and attribute the accumulated mass to the
genes that govern the crossed boundaries."""),
))

# ------------------------------------------------------ S11 Definition 2.2
SPLICES_B.append(("def-kmu", (
"""\\begin{definition}[$\\kmu$]\\label{def:kmu}
For a $C^1$ parameter trajectory $\\theta(t)$, $t \\in [0,T]$, and its
piecewise-affine optimal-flux response $v(\\theta(t))$, let
$\\{t_e\\}_e$ be the event times at which the trajectory crosses active-set
strata, with atoms $A_e = A_{F(e)}$ evaluated on the crossed facet. Define
\\[
\\kmu(g) \\;=\\; \\frac{1}{T}\\sum_{e} \\bigl\\| A_e \\bigr\\| \\, w_e(g),
\\]
where $\\|{\\cdot}\\|$ is the entrywise $1$-norm on
$\\RR^{m \\times p \\times p}$ and $w_e(g) \\in \\{0,1\\}$ selects the events
whose crossed stratum changes the activity of reactions assigned to gene
$g$ (max over its reactions, per the GPR association).
\\end{definition}"""),
(
"""\\begin{definition}[$\\kmu$]\\label{def:kmu}
Let $\\theta(t) : [0, T] \\to \\Theta$ be a parameter trajectory that
crosses active-set boundaries at discrete event times $\\{t_e\\}_e$,
and let $A_e = A_{F(e)}$ be the jump tensor evaluated on the crossed
facet. Define the \\emph{gene sensitivity metric} for gene $g$ as
\\[
\\kmu(g) \\;=\\; \\frac{1}{T}\\sum_{e} \\bigl\\| A_e \\bigr\\| \\, w_e(g),
\\]
where $\\|{\\cdot}\\|$ is the entrywise $1$-norm on
$\\RR^{m \\times p \\times p}$ and $w_e(g) \\in \\{0,1\\}$ is an
indicator variable that equals $1$ if the active-set change at event
$e$ alters the capacity bound or activity status of any reaction
catalyzed by gene $g$ (max over its reactions, via the standard
Gene--Protein--Reaction logical associations).
\\end{definition}"""),
))

# ------------------------------------------- S12 remark: 1D-path regime
SPLICES_B.append(("rem-kmu-1d", (
"""\\begin{remark}[$\\kmu$ integrates along a one-dimensional path]
$\\kmu$ integrates measure mass along a one-dimensional trajectory --- the
regime in which total variation and mass are automatically
consistent (see \\S\\ref{sec:theoremB}); its resolution
independence (measured mass $288.77$ stable under $4\\times$/$8\\times$
trajectory refinement) is exactly the $L^1$-reconstruction regime of
Theorem~\\ref{thm:Bprime}(iv). Its per-reaction masses are the components of the
flux-layer crease measure whose objective contraction is $D^2\\Phi$
(Theorem~\\ref{thm:coupling}): the metric is the primal layer of the
canonical object.
\\end{remark}"""),
(
"""\\begin{remark}[$\\kmu$ integrates along a one-dimensional path]
Because $\\kmu$ integrates discrete boundary shocks along a
one-dimensional trajectory, it operates in the regime where total
variation and measure mass are automatically consistent (see
\\S\\ref{sec:theoremB}); in computational simulations across multiple
grid resolutions, the total calculated value of $\\kmu$ remains
numerically stable (measured mass $288.77$, within machine precision
across $4\\times$/$8\\times$ trajectory refinement), making it a
robust, parameter-free metric --- and its resolution independence is
exactly the $L^1$-reconstruction regime of
Theorem~\\ref{thm:Bprime}(iv). Its per-reaction masses are the components of the
flux-layer crease measure whose objective contraction is $D^2\\Phi$
(Theorem~\\ref{thm:coupling}): the metric is the primal layer of the
canonical object.
\\end{remark}"""),
))

# ------------------------------------------------------- S13 Sec 2.3 opening
SPLICES_B.append(("sec23-opening", (
"""Parametric linear programming also produces a scalar object of
independent interest: the optimal value $\\Phi(\\theta)$, which in the
metabolic setting reflects the organism's maximum achievable growth
rate. The value function is canonical --- it does not depend on which
optimal flux the solver returns --- and classical convex analysis
attaches to it a curvature measure of its own. Should metabolic
sensitivity be read off the growth rate or off the internal fluxes?
This subsection develops the value layer, and the coupling identity
of the next subsection answers the question."""),
(
"""Parametric linear programming also produces a scalar object of
independent interest: the optimal value $\\Phi(\\theta)$, which in the
metabolic setting reflects the organism's maximum achievable growth
rate. A central question is whether metabolic sensitivity should be
measured through changes in overall growth rate (the objective value
function $\\Phi(\\theta) = \\max c^\\top v$) or through changes in the
internal fluxes ($v^*(\\theta)$). The value function is canonical ---
it does not depend on which optimal flux the solver returns --- and
classical convex analysis attaches to it a curvature measure of its
own. This subsection develops the value layer, and the coupling
identity of the next subsection answers the question."""),
))

# ------------------------------------------------------- S14 Proposition 2.3
SPLICES_B.append(("prop-alex", (
"""\\begin{proposition}[Existence and tie-break-freeness]\\label{prop:alex}
Let $\\Phi(\\theta) = \\max\\{ c^\\top v : Sv = 0,\\ \\ell(\\theta) \\le v \\le
u(\\theta)\\}$ with $\\ell, u$ affine, feasible and bounded. Then $\\Phi$ is
concave (pointwise infimum of affine dual objectives over a
$\\theta$-independent dual feasible set), and $-\\Phi$ carries a symmetric
matrix-valued Radon Hessian measure $D^2(-\\Phi)$ (Alexandrov
\\citep{alexandrov1939}), independent
of the optimal-flux selection rule. Concavity fails in general under OR
(isoenzyme) GPR rules for simultaneous multi-gene capacity vectors;
single-gene axes, exchange-bound families, and AND-only subnetworks
retain it. For OR-containing rules the value function remains
continuous piecewise affine and carries the signed crease measure of
Proposition~\\ref{prop:semiconvex}; only the Monge--Amp\\`ere layer
requires the concave class.
\\end{proposition}"""),
(
"""\\begin{proposition}[Properties of the value-function layer]\\label{prop:alex}
Let the capacity bounds $\\ell(\\theta)$ and $u(\\theta)$ depend
affinely on $\\theta$, with the LP feasible and bounded, and let
$\\Phi(\\theta) = \\max\\{ c^\\top v : Sv = 0,\\ \\ell(\\theta) \\le v \\le
u(\\theta)\\}$. The optimal value function $\\Phi(\\theta)$ is concave,
continuous, and piecewise affine (pointwise infimum of affine dual
objectives over a $\\theta$-independent dual feasible set). By
Alexandrov's theorem \\citep{alexandrov1939}, its negative
$-\\Phi(\\theta)$ carries a symmetric, positive semidefinite
matrix-valued Hessian measure $D^2(-\\Phi)$. This value-layer
curvature depends solely on the network bounds and stoichiometry, and
is completely invariant to how ties are broken between alternative
optimal flux solutions. Concavity fails in general under OR
(isoenzyme) GPR rules for simultaneous multi-gene capacity vectors;
single-gene axes, exchange-bound families, and AND-only subnetworks
retain it. For OR-containing rules the value function remains
continuous piecewise affine and carries the signed crease measure of
Proposition~\\ref{prop:semiconvex}; only the Monge--Amp\\`ere layer
requires the concave class.
\\end{proposition}"""),
))

# ------------------------------- S15 fitness-envelope bridge (insertion)
SPLICES_B.append(("fitness-envelope", (
"""\\begin{proposition}[Two-layer structure of $D^2(-\\Phi)$]\\label{prop:twolayer}"""),
(
"""The value function $\\Phi(\\theta)$ represents the organism's maximum
fitness envelope, and its chamber boundaries correspond to the sector
divisions seen in classical phenotype phase planes \\citep{edwards2001,
ibarra2002}. However, as we establish below, looking only at the
value function creates a profound blind spot.

\\begin{proposition}[Two-layer structure of $D^2(-\\Phi)$]\\label{prop:twolayer}"""),
))

# ------------------------------------------------------ S17 Theorem 2.4
SPLICES_B.append(("thm-coupling", (
"""\\begin{theorem}[Value--flux crease coupling]\\label{thm:coupling}
$\\Phi = c^\\top v^*$ pointwise; hence, as symmetric matrix-valued
signed Radon measures on the parameter domain,
\\[
D^2\\Phi \\;=\\; \\sum_{r} c_r\\, D^2 v^*_r .
\\]
Along any piecewise-affine trajectory, at every crease time $t_k$:
$\\Delta\\Phi'(t_k) = c^\\top \\Delta v'(t_k)$, and
$|\\Delta\\Phi'| \\le \\|c\\|_\\infty \\,\\|\\Delta v'\\|_1$.
\\begin{enumerate}[label=(\\roman*),leftmargin=2em]
\\item \\textbf{(Visibility dichotomy.)} An event with unique optima
      on both sides is a transversal optimal-vertex switch and is
      necessarily objective-moving; objective-invisible events
      ($c^\\top \\Delta v' = 0$, $\\Delta v' \\neq 0$) are exactly the
      degenerate reroutings inside $\\ge 1$-dimensional optimal faces
      (mask-type events). The tie-break sensitivity of the flux layer
      is concentrated in the invisible events; the $c$-contraction is
      tie-break-free because it annihilates the degenerate layer.
\\item \\textbf{(Sparse-objective corollary.)} If $c =
      \\gamma e_{\\mathrm{bio}}$, then $D^2\\Phi = \\gamma\\, D^2
      v^*_{\\mathrm{bio}}$: the value layer is the crease measure of
      the single biomass component, and per-gene attribution from the
      value layer is structurally impossible.
\\end{enumerate}
In words: an optimal switch is visible to the value layer only when it
moves growth; the objective-invisible events are zero-cost pathway
substitutions --- reroutings among flux patterns of equal growth ---
carrying large flux changes at unchanged value."""),
(
"""\\begin{theorem}[The value--flux coupling identity and visibility
dichotomy]\\label{thm:coupling}
Because $\\Phi(\\theta) = c^\\top v^*(\\theta)$ holds everywhere, the
distributional second derivatives satisfy, as symmetric
matrix-valued signed Radon measures on the parameter domain,
\\[
D^2 \\Phi \\;=\\; \\sum_{r} c_r \\, D^2 v^*_r .
\\]
Along any piecewise-affine trajectory $\\theta(t)$, the directional
slope jump of the objective value $\\Delta\\Phi'(t_k)$ and the flux
slope jumps $\\Delta v'(t_k)$ at every crease time $t_k$ satisfy
$\\Delta\\Phi'(t_k) = c^\\top \\Delta v'(t_k)$, with
$|\\Delta\\Phi'(t_k)| \\le \\|c\\|_\\infty \\,\\|\\Delta v'(t_k)\\|_1$.
This induces an exact structural dichotomy:
\\begin{enumerate}[label=(\\roman*),leftmargin=2em]
\\item \\textbf{(Visibility dichotomy.)} An event with unique optima
      on both sides is a transversal optimal-vertex switch and is
      necessarily objective-moving ($\\Delta\\Phi' \\neq 0$);
      objective-invisible events ($c^\\top \\Delta v' = 0$,
      $\\Delta v' \\neq 0$) are exactly the degenerate reroutings
      inside $\\ge 1$-dimensional optimal faces (mask-type events) ---
      metabolic pathway substitutions that sustain identical growth
      rates. The tie-break sensitivity of the flux layer
      is concentrated in the invisible events; the $c$-contraction is
      tie-break-free because it annihilates the degenerate layer.
\\item \\textbf{(Sparse-objective annihilation.)} In standard FBA the
      objective vector selects only the biomass reaction ($c =
      \\gamma e_{\\mathrm{bio}}$), and the coupling identity
      simplifies to $D^2\\Phi = \\gamma\\, D^2 v^*_{\\mathrm{bio}}$:
      the value layer is the crease measure of
      the single biomass component, and per-gene attribution from the
      value layer is structurally impossible.
\\end{enumerate}
In words: an optimal switch is visible to the value layer only when it
moves growth; the objective-invisible events are zero-cost pathway
substitutions --- reroutings among flux patterns of equal growth ---
carrying large flux changes at unchanged value."""),
))

# ------------------------------------------------------- S19 Sec 3 opening
SPLICES_B.append(("sec3-opening", (
"""Can discrete linear-programming switches be approximated by smooth,
continuous curves? Section~\\ref{sec:measure}
treated the discrete measure exactly; this section asks the
refinement question that any such approximation raises: as a triangulation of parameter space is refined,
does the discrete measure converge to the smooth curvature of a smooth
response map? The answer splits cleanly --- weakly and cell-wise yes,
in total variation no --- and a resolution parameter $\\sigma$ separates
the two regimes."""),
(
"""Computational biologists often ask: \\emph{can discrete
linear-programming switches be approximated by smooth, continuous
curves?} Section~\\ref{sec:measure} treated the discrete measure
exactly; this section establishes the \\emph{refinement--resolution
bridge}, which characterizes how discrete active-set jump measures
behave as the sampling mesh becomes arbitrarily fine ($h \\to 0$).
The answer splits cleanly --- weakly and cell-wise yes,
in total variation no --- and a resolution parameter $\\sigma$ separates
the two regimes."""),
))

# ------------------------------------------------------- S20 Theorem 3
SPLICES_B.append(("thm-bprime", (
"""\\begin{theorem}[Refinement--resolution bridge]
\\label{thm:Bprime}
Let $\\mu_h = D^2 u_h$ (Definition~\\ref{def:mu}) and
$\\mu = D^2u \\dvol$. Then:
\\begin{enumerate}[label=(\\roman*),leftmargin=2em]
\\item \\textbf{(Atoms / support.)} $\\mu_h$ is a finite matrix-valued Radon
      measure concentrated on the $(p-1)$-skeleton of $\\mathcal{T}_h$ with
      atoms $A_F = [\\nabla u_h]_F \\otimes n_F |F|$; there are no atoms on
      lower-dimensional strata.
\\item \\textbf{(Weak convergence.)} $\\mu_h \\Rightarrow \\mu$ weakly as
      matrix-valued measures: for every
      $\\varphi \\in C_c^\\infty(\\Omega)$,
      $\\langle \\mu_h, \\varphi \\rangle \\to \\langle \\mu, \\varphi \\rangle$.
      Moreover $\\|\\mu_h - \\mu\\|_{\\KR} \\to 0$ in the
      Kantorovich--Rubinstein (flat) norm.
\\item \\textbf{(Total variation: the exact statement.)}
      $\\sup_h \\|\\mu_h\\|_{\\TV} \\le C\\,|u|_{C^2}|\\Omega|$ (under
      quasi-uniformity) and
      $\\liminf_h \\|\\mu_h\\|_{\\TV} \\ge \\|\\mu\\|_{\\TV}$; but
      $\\|\\mu_h\\|_{\\TV} \\to \\|\\mu\\|_{\\TV}$ is \\emph{false in general} ---
      see Remark~\\ref{rem:tvcounter}. It holds in the one-signed regime
      (convex or concave data restricted to one-dimensional parameter
      families), which is the regime of the parametric-LP value function
      and of $\\kmu$.
\\item \\textbf{(No-mass-loss, correct form: $L^1$ reconstruction.)}
      On structured complexes, the per-cell reconstructed density
      $\\rho_h(\\mathrm{cell}) = |\\mathrm{cell}|^{-1} \\sum_{F \\to
      \\mathrm{cell}} A_F$ converges to $D^2 u$ \\emph{strongly in $L^1$}
      with rate $O(h)$ for $u \\in C^3$; consequently
      $\\|\\rho_h\\|_{L^1} \\to \\|\\mu\\|_{\\TV}$. On unstructured complexes the
      unweighted three-facet patch is not the dual cell; the general statement
      requires the discrete-duality (dual-diamond) pairing.
\\item \\textbf{(Resolution window.)} For the coarse-grained family
      $\\mu_{h,\\sigma} = \\mu_h * \\varphi_\\sigma$: at fixed $h$, the limit
      $\\sigma \\to 0$ is the \\emph{atomic} measure; the smooth object
      exists only as a family member at matched resolution through the
      window $h \\ll \\sigma \\ll L_{\\mathrm{var}}$, where $L_{\\mathrm{var}}$
      is the length scale on which the smooth curvature density itself
      varies (measured in \\S\\ref{sec:m4}).
\\end{enumerate}
\\end{theorem}"""),
(
"""\\begin{theorem}[Refinement--resolution bridge]
\\label{thm:Bprime}
Let $\\mu_h = D^2 u_h$ (Definition~\\ref{def:mu}) and
$\\mu = D^2u \\dvol$. Then:
\\begin{enumerate}[label=(\\roman*),leftmargin=2em]
\\item \\textbf{(Atoms / support.)} $\\mu_h$ is a finite matrix-valued Radon
      measure concentrated on the $(p-1)$-skeleton of $\\mathcal{T}_h$ with
      atoms $A_F = [\\nabla u_h]_F \\otimes n_F |F|$; there are no atoms on
      lower-dimensional strata.
\\item \\textbf{(Weak convergence.)} As the mesh is refined ($h \\to 0$),
      $\\mu_h$ converges weakly to the smooth measure: for every
      smooth test window $\\varphi \\in C_c^\\infty(\\Omega)$, the average
      behavior matches, $\\langle \\mu_h, \\varphi \\rangle \\to
      \\langle \\mu, \\varphi \\rangle$. Furthermore, this convergence
      holds in the flat Kantorovich--Rubinstein transport norm
      ($\\|\\mu_h - \\mu\\|_{\\KR} \\to 0$).
\\item \\textbf{(Total variation: the exact statement.)} Despite weak
      convergence, the total variation norm of $\\mu_h$ does
      \\emph{not} converge to the smooth total variation:
      $\\sup_h \\|\\mu_h\\|_{\\TV} \\le C\\,|u|_{C^2}|\\Omega|$ (under
      quasi-uniformity) and
      $\\liminf_h \\|\\mu_h\\|_{\\TV} \\ge \\|\\mu\\|_{\\TV}$; but
      $\\|\\mu_h\\|_{\\TV} \\to \\|\\mu\\|_{\\TV}$ is false in general ---
      see Remark~\\ref{rem:tvcounter}. It holds in the one-signed regime
      (convex or concave data restricted to one-dimensional parameter
      families), which is the regime of the parametric-LP value function
      and of $\\kmu$.
\\item \\textbf{(No-mass-loss, correct form: $L^1$ reconstruction.)}
      If the discrete jump atoms are averaged over local dual grid
      cells, the resulting reconstructed piecewise-constant density
      $\\rho_h(\\mathrm{cell}) = |\\mathrm{cell}|^{-1} \\sum_{F \\to
      \\mathrm{cell}} A_F$ converges to $D^2 u$ \\emph{strongly in $L^1$}
      with rate $O(h)$ for $u \\in C^3$; consequently
      $\\|\\rho_h\\|_{L^1} \\to \\|\\mu\\|_{\\TV}$. This holds on structured
      complexes; on unstructured complexes the
      unweighted three-facet patch is not the dual cell, and the general
      statement requires the discrete-duality (dual-diamond) pairing.
\\item \\textbf{(Resolution window.)} If the discrete measure is
      smoothed using a continuous filter (mollifier) of width
      $\\sigma$ --- the coarse-grained family $\\mu_{h,\\sigma} =
      \\mu_h * \\varphi_\\sigma$ --- the smooth curvature density
      emerges only at matched resolution, through the
      window $h \\ll \\sigma \\ll L_{\\mathrm{var}}$, where $L_{\\mathrm{var}}$
      is the length scale on which the smooth curvature density itself
      varies (measured in \\S\\ref{sec:m4}); at fixed $h$, the limit
      $\\sigma \\to 0$ is the \\emph{atomic} measure.
\\end{enumerate}
\\end{theorem}"""),
))

# ------------------------------------------------ S21 TV counterexample remark
SPLICES_B.append(("rem-tvcounter", (
"""\\begin{remark}[Exact counterexample calculus]\\label{rem:tvcounter}
The failure of total-variation convergence stems directly from the
directional anisotropy of the triangulation. On the right-triangle mesh of $[0,1]^2$ with Hessian
$H = \\left(\\begin{smallmatrix} a & b\\\\ b & c\\end{smallmatrix}\\right)$, the
per-cell atoms are $A_{\\mathrm{diag}} = b h^2 \\mathbf{1}\\mathbf{1}^\\top$,
$A_{\\mathrm{vert}} = (a-b) h^2\\, e_x \\otimes e_x$,
$A_{\\mathrm{horiz}} = (c-b) h^2\\, e_y \\otimes e_y$; their \\emph{sum} is
exactly $h^2 H$ (machine-verified to $0.0$), while the entrywise total
variation per cell is $|a-b| + |c-b| + 4|b|$ against the target
$|a| + |c| + 2|b|$: the signed atoms sum to the right curvature, but
their absolute magnitudes add the geometric overhead of the grid
detour --- like navigating a city whose streets run only in fixed
directions instead of walking as the crow flies. Hence for $u = xy$ the ratio is exactly $3 - 1/n$, for
the strictly convex $u = 2x^2 - xy + 2y^2$ it is $1.4 - 1/n$ (measured:
$2.9922$ and $1.3922$ at $n=128$), and for generic smooth maps $3.6$--$4.4$.
Total-variation convergence fails generically --- including under
convexity --- while weak convergence holds at rate $O(h^2)$ throughout.
\\end{remark}"""),
(
"""\\begin{remark}[Why total variation fails to converge]\\label{rem:tvcounter}
The failure of total-variation convergence stems directly from the
directional anisotropy of the triangulation --- grid-alignment bias.
When a curved surface is approximated by flat triangular tiles, the
edges of the tiles run along fixed geometric directions. To represent
a diagonal saddle surface like $u(x, y) = xy$, the discrete model
cannot bend smoothly; it must alternate between directional slope
jumps along the fixed grid axes. On the right-triangle mesh of $[0,1]^2$ with Hessian
$H = \\left(\\begin{smallmatrix} a & b\\\\ b & c\\end{smallmatrix}\\right)$, the
per-cell atoms are $A_{\\mathrm{diag}} = b h^2 \\mathbf{1}\\mathbf{1}^\\top$,
$A_{\\mathrm{vert}} = (a-b) h^2\\, e_x \\otimes e_x$,
$A_{\\mathrm{horiz}} = (c-b) h^2\\, e_y \\otimes e_y$; their \\emph{sum} is
exactly $h^2 H$ (machine-verified to $0.0$), while the entrywise total
variation per cell is $|a-b| + |c-b| + 4|b|$ against the target
$|a| + |c| + 2|b|$. These jumps sum algebraically to the correct net
curvature, but their absolute magnitudes add up with extra geometric
overhead --- exactly like navigating a grid-based city street layout
instead of walking as the crow flies. Hence for $u = xy$ the ratio of
discrete to continuous total variation is exactly $3 - 1/n$, for
the strictly convex $u = 2x^2 - xy + 2y^2$ it is $1.4 - 1/n$ (measured:
$2.9922$ and $1.3922$ at $n=128$), and for generic smooth maps $3.6$--$4.4$.
Total-variation convergence fails generically --- including under
convexity --- while weak convergence holds at rate $O(h^2)$ throughout.
\\end{remark}"""),
))

# -------------------------------------- S22 holonomy proposition + In words
SPLICES_B.append(("prop-dichotomy", (
"""\\begin{proposition}[Regime dichotomy, in closed form]
\\label{prop:dichotomy}
Let $B(\\varepsilon)$ be the curvature mass captured by a loop of radius
$\\varepsilon$. For a $C^2$ map, $B(\\varepsilon) = O(\\varepsilon^2)$; for a
piecewise-affine map whose kink complex meets the loop transversally,
$B(\\varepsilon) = O(\\varepsilon)$. Measured slopes on the regime-dial design (\\S\\ref{sec:m4}): $2.000$ (smooth) and $1.00$ (parametric FBA,
$76$-pair perturbation scan).
\\end{proposition}

In words: carried around a small closed loop, a smooth map drifts by
something of the order of the enclosed area, while an active-set map
pays a toll proportional to the loop's diameter for every wall it
crosses."""),
(
"""\\begin{proposition}[Scaling dichotomy of parameter holonomy]
\\label{prop:dichotomy}
A fundamental distinction between smooth physical systems and
active-set metabolic networks appears when tracing a closed parameter
loop. Let an organism be perturbed around a small closed loop, and
let $B(\\varepsilon)$ be the curvature mass captured by a loop of radius
$\\varepsilon$. For a smooth nonlinear system ($C^2$ map), the discrepancy
scales quadratically: $B(\\varepsilon) = O(\\varepsilon^2)$; for a
piecewise-affine map whose kink complex meets the loop transversally,
crossing a constraint boundary incurs a first-order jump, and the
discrepancy scales linearly: $B(\\varepsilon) = O(\\varepsilon)$. Measured
slopes on the regime-dial design (\\S\\ref{sec:m4}): $2.000$ (smooth) and
$1.00$ (parametric FBA, $76$-pair perturbation scan).
\\end{proposition}

In words: carried around a small closed loop, a smooth map drifts by
something of the order of the enclosed area, while an active-set map
pays a toll proportional to the loop's diameter for every wall it
crosses --- confirming that metabolic networks operate in the
discrete active-set regime rather than behaving like smooth
systems."""),
))

# ------------------------------------------------------ S23 Sec 4 opening
SPLICES_B.append(("sec4-opening", (
"""The geometric claims of Sections~\\ref{sec:measure}
and~\\ref{sec:theoremB} are operational rather than merely formal: they
refer to the active set of a solved linear program and can therefore
be tested directly on genome-scale models. Each subsection below
reports one such test."""),
(
"""We validated this active-set curvature framework across genome-scale
reconstructions of \\emph{E.~coli} (iML1515 \\citep{monk2017} and
iJO1366 \\citep{orth2011}). The geometric claims of
Sections~\\ref{sec:measure} and~\\ref{sec:theoremB} are operational
rather than merely formal: they refer to the active set of a solved
linear program and can therefore be tested directly on genome-scale
models. Each subsection below reports one such test."""),
))

# ------------------------------------------------------ S23b Sec 4.1 (m1)
SPLICES_B.append(("sec41-m1", (
"""We first verify the support claim: second-order response mass should
concentrate on active-set switches. To this end we executed thirteen
high-resolution parameter sweeps on the genome-scale \\emph{E.~coli}
model iML1515 (Fig~\\ref{fig:m1}) --- continuous variations in glucose
and oxygen uptake, alongside titrated capacity knockdowns of ten
metabolic genes (pgi, zwf, tktA, pfkA, eno, gltA, aceA, ppc, gnd,
rpe) --- with an iJO1366 glucose replication and an aceA
unused-pathway negative control, all solved by the three-stage
lexicographic pFBA engine (deterministic optimum; fixed seeded
tie-break weights resolving the vertex degeneracy of plain pFBA).
The result is unambiguous: $93.4$--$100.0\\%$ of the total second-order
response mass concentrates precisely at operational active-set
switches in every sweep that crosses critical-region boundaries ---
ten of the eleven crossing sweeps at mass exactly $1.000000$ (AUC
$0.83$--$1.00$; Mann--Whitney $p \\le 2 \\times 10^{-3}$, with seven of
eleven crossing sweeps at $p \\le 10^{-4}$; mass $0.934$--$1.0$).
Between events, the paths are piecewise affine to solver precision
(event-free segment residuals $\\le 1.2 \\times 10^{-10}$, with
$8 \\times 10^{-14}$ on the glucose sweep; one $19$-point segment of
the eno sweep carries $4.1 \\times 10^{-3}$ --- a sub-threshold kink
invisible to the operational event proxy, which is also why that
sweep's event mass is $0.934$ rather than $1.0$). The negative
controls behave exactly as theory dictates: the unused-pathway
knockdown produces zero events and zero curvature, and the
single-critical-region sweep sits at the noise level $D^2 \\sim
10^{-11}$."""),
(
"""To verify that second-order responses concentrate at active-set
boundaries, we executed thirteen high-resolution parameter sweeps on
the genome-scale \\emph{E.~coli} model iML1515 (Fig~\\ref{fig:m1}):
two environmental nutrient sweeps (progressive glucose uptake decline
and oxygen limitation); ten enzymatic capacity titrations of key
metabolic genes (pgi, zwf, tktA, pfkA, eno, gltA, aceA, ppc, gnd,
rpe); and one negative control sweep, titrating aceA (isocitrate
lyase) under glucose-excess conditions where the glyoxylate shunt is
inactive --- with an iJO1366 glucose replication, all solved by the
three-stage lexicographic pFBA engine (deterministic optimum; fixed
seeded tie-break weights resolving the vertex degeneracy of plain
pFBA). Across all eleven sweeps that crossed active-set boundaries,
$93.4$--$100.0\\%$ of the total second-order
response mass concentrated precisely at active-set transitions ---
ten of the eleven at mass exactly $1.000000$ (AUC
$0.83$--$1.00$; Mann--Whitney $p \\le 2 \\times 10^{-3}$, with seven of
eleven crossing sweeps at $p \\le 10^{-4}$; mass $0.934$--$1.0$).
Between events, the paths are piecewise affine to solver precision
(event-free segment residuals $\\le 1.2 \\times 10^{-10}$, with
$8 \\times 10^{-14}$ on the glucose sweep; one $19$-point segment of
the eno sweep carries $4.1 \\times 10^{-3}$ --- a sub-threshold kink
invisible to the operational event proxy, which is also why that
sweep's event mass is $0.934$ rather than $1.0$). The negative
control confirmed specificity: the unused-pathway
knockdown produced zero boundary crossings and zero curvature mass,
and the
single-critical-region sweep sits at the noise level $D^2 \\sim
10^{-11}$."""),
))

# ------------------------------------------------------ S24 Sec 4.2 epistasis
SPLICES_B.append(("sec42-epistasis", (
"""Epistasis --- the interaction between two knockouts beyond the sum of
their individual effects --- provides a combinatorial test of the
active-set reading: if the measure is a genuine geometry, pairs of
perturbations should interact through it. We test this on $1{,}516$
single knockouts and $2{,}779$ double-knockout pairs across five
panels. Defining epistasis $\\varepsilon_{ij} = \\kappa_{ij} - \\kappa_i -
\\kappa_j$, every one of the $40$ synthetic-lethal pairs is an
isozyme redundancy (tktA/tktB, acnA/acnB, metE/metH, \\dots) with
pure-emergence epistasis, and $|\\varepsilon_{ij}|$ aligns with
active-set footprint overlap (Spearman $\\rho_S = 0.865$,
$J_{\\mathrm{support}} = 0.800$). Sequential ($L_1$-MOMA
\\citep{segre2002}) knockouts open nonzero commutators in $25\\%$ of
active pairs, and closed genotype loops fail to return to the initial
state in $66\\%$ of pairs --- phenotypic memory, with median holonomy
$\\sim 110$."""),
(
"""Epistasis --- the interaction between two knockouts beyond the sum of
their individual effects --- provides a combinatorial test of the
active-set reading: if the measure is a genuine geometry, pairs of
perturbations should interact through it. We next analyzed whether
active-set geometry explains genetic interactions across $1{,}516$
single-gene knockouts and $2{,}779$ double-knockout pairs (five
panels). We measured epistatic curvature as
$\\varepsilon_{ij} = \\kappa_{ij} - \\kappa_i - \\kappa_j$:
\\begin{itemize}
\\item \\emph{Synthetic lethality:} all $40$ synthetic-lethal gene pairs
      (such as tktA/tktB, acnA/acnB, and metE/metH) corresponded to
      redundant isoenzyme pairs exhibiting pure emergence epistasis.
\\item \\emph{Footprint overlap:} across all viable double-knockout
      pairs, the magnitude of genetic interaction $|\\varepsilon_{ij}|$
      correlated strongly with the overlap (Jaccard index) of their
      individual active-set footprints (Spearman $\\rho_S = 0.865$,
      $J_{\\mathrm{support}} = 0.800$).
\\item \\emph{Phenotypic memory:} when sequential gene knockouts were
      introduced dynamically using regulatory minimization of
      metabolic adjustment ($L_1$-MOMA \\citep{segre2002}), sequential
      paths did not commute in $25\\%$ of active pairs; and when the
      network was subjected to closed cyclic perturbations
      ($A \\to AB \\to B \\to$ wild-type), $66\\%$ of pairs failed to
      return to their initial flux state, retaining persistent
      metabolic memory (median path holonomy $\\sim 110$).
\\end{itemize}"""),
))
