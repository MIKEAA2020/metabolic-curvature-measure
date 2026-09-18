# -*- coding: utf-8 -*-
"""v10 companion splice data: Gemini-register adoption (companion
humanized.txt lines 1-714, gemini section) as the prose base, with
v9 substance retained verbatim (refs, proof statuses, six-axis
battery, machine-verified claims); Grok's terse formulations and
own-voice bridges only where truly merited. ASCII art from the audit
NOT adopted. Gemini's bibliography NOT adopted (v9's bib kept).
Each splice: (name, old, new); old must occur exactly once in
companion_categorical_v9.tex.
"""

SPLICES = []

# ---------------------------------------------------- C1 hypersetup block
SPLICES.append(("hypersetup", (
"""\\hypersetup{
 pdftitle={Stratified Connections, Optic Composition, and the
           Homotopy Fixed-Point Extension: A Categorical Framework
           for Viability-Weighted Curvature},
 pdfauthor={Amin Abaee},
 pdfsubject={categorical framework for viability-weighted curvature:
             stratified connections, optic composition, homotopy
             type theory},
 pdfkeywords={optic category, stratified connection, 2-category,
              filtered colimit, homotopy type theory,
              applied category theory}}"""),
(
"""\\hypersetup{
 pdftitle={A Geometric and Category-Theoretic Theory of Viability:
           How Sequential Adaptations Induce Path-Dependent Risk},
 pdfauthor={Amin Abaee},
 pdfsubject={geometric and category-theoretic theory of viability:
             stratified connections, viability-weighted curvature,
             optic composition, homotopy type theory},
 pdfkeywords={applied category theory, optic category, stratified
              connection, 2-category, homotopy type theory,
              information
              geometry, holonomy, viability theory, autopoiesis}}"""),
))

# ---------------------------------------------------- C2 title center block
SPLICES.append(("title-block", (
"""  {\\large\\bfseries Stratified Connections, Optic Composition, and the
   Homotopy Fixed-Point Extension:\\par
   A Categorical Framework for Viability-Weighted Curvature\\par}"""),
(
"""  {\\large\\bfseries A Geometric and Category-Theoretic Theory of
   Viability:\\par
   How Sequential Adaptations Induce Path-Dependent Risk\\par}"""),
))

# -------------------------------------------------- C3 abstract + keywords
SPLICES.append(("abstract", (
"""\\textbf{Abstract.} An adaptive system must stay viable while its
environment changes; its policy is optimal subject to active
constraints, and a closed sequence of manageable changes can
accumulate into a threat. We develop the categorical and
homotopy-theoretic framework for viability-weighted curvature: the
geometric object measuring this accumulation through the policy
holonomy.
(i)~The SAVGS object assembles control base, Fisher--Rao
policy bundle, viability margin, maintenance graph, and a
$2$-categorical boundary span into one stratified bundle.
(ii)~The $2$-category $\\mathbf{StCon}(B)$ of stratified
$G_C$-connections carries a lax-functorial gluing theorem, a
piecewise-holonomy formula, and the small-loop expansion for loops
crossing a constraint-switching wall transversally in
\\emph{pairs}; on constant-active-set strata the connection is the
Fisher-minimal transport law (KKT projection), and the small-loop
viability--holonomy theorem bounds endpoint erosion of a viability
margin by the viability-weighted curvature, its worst-case
positive-part contraction with active survival covectors.
(iii)~A single composition theorem types the seven domain bridges
as optics, establishing a per-optic Lipschitz bound and a Banach
contraction of the Krasnoselskii--Mann-averaged update for its
instantiation; the projected CPTP contraction
settles the Zeno self-reference.
(iv)~The filtered-colimit construction of RAF sets is proved at Set
level with an adapter-level optic statement, verified at scale;
the $\\infty$-categorical extension is developed in homotopy type
theory, proof-sketch status marked. The validation battery is
robust across six axes: carbon, oxygen, nitrogen,
phosphate, and iron supply plus non-medium maintenance stress
leave labels invariant, re-stratifying only at
regime switches; the association is invariant under canonical
flux selection, the declared tie-break closing its near-degeneracy
boundary. The application paper
develops the atomic curvature measure and its genome-scale
validation.
\\par
\\vspace{0.5em}

\\noindent\\textbf{Keywords:} optic category; stratified connection;
2-category; filtered colimit; homotopy type theory;
applied category theory\\\\[0.3em]"""),
(
"""\\textbf{Abstract.} When adaptive systems navigate fluctuating
environments, they constantly adjust their internal strategies to
remain viable. While individual adaptations may appear completely
safe, a sequence of individually harmless adjustments can
unexpectedly push a system into failure if the environmental shifts
occur in a non-commuting order. We develop the geometric and
category-theoretic framework that defines and quantifies this
phenomenon: \\emph{viability-weighted curvature}, the geometric
object measuring this accumulation through the policy holonomy.
The framework rests on four pillars.
(i)~The \\emph{SAVGS architecture} unifies the control base, the
Fisher--Rao policy bundle, the viability margin, the maintenance
graph, and a $2$-categorical boundary span into one stratified
$G_C$-reduced bundle.
(ii)~The $2$-category $\\mathbf{StCon}(B)$ of stratified connections
carries a lax-functorial gluing theorem and a piecewise-holonomy
formula, with the boundary reset of a loop crossing a
constraint-switching wall transversally in \\emph{pairs} at its true
order; on each constant-active-set stratum the Fisher-minimal
transport law (KKT projection) defines the connection, and the
small-loop theorem bounds the endpoint erosion of a viability
margin by the viability-weighted curvature.
(iii)~A single composition theorem types the seven domain bridges
as optics, with per-optic Lipschitz constants and a Banach
contraction of the Krasnoselskii--Mann-averaged update; the
projected CPTP contraction settles the Zeno self-reference.
(iv)~The filtered-colimit construction of RAF sets is proved at Set
level with the adapter-level optic statement and verified at scale;
the $\\infty$-categorical extension is developed in homotopy type
theory, its proof-sketch status marked. The validation battery is
robust across six axes: carbon, oxygen, nitrogen, phosphate, and
iron supply plus non-medium maintenance stress leave labels
invariant, re-stratifying only at regime switches; the association
is invariant under canonical flux selection, the declared tie-break
closing its near-degeneracy boundary. The application paper
develops the atomic curvature measure and its genome-scale
validation.
\\par
\\vspace{0.5em}

\\noindent\\textbf{Keywords:} applied category theory; optic
category; stratified connection; 2-category; homotopy type theory;
information
geometry; holonomy; viability theory; autopoiesis\\\\[0.3em]"""),
))

# ------------------------------------------------------- C4 intro problem
SPLICES.append(("intro-problem", (
"""\\paragraph{The problem.}
An adaptive system that must remain viable while its environment
changes is governed, at each instant, by a policy that is optimal
subject to active constraints. A \\emph{policy} is the optimizer's
chosen response at each state; a \\emph{connection} is the rule for
comparing policies at nearby states; and its \\emph{holonomy} is the
drift accumulated around a closed loop of changes --- the geometric
signature of non-commutativity. In concrete terms: a system can
survive a change in temperature, and separately survive a change in
nutrient supply; applied as a closed cycle --- temperature, then
nutrients, then reverse temperature, then reverse nutrients --- the
same two changes can still return the system to its starting
environment with its internal reserves degraded. The order matters,
not only the magnitudes: adjustments governed by active constraints
need not commute. Classical viability theory \\citep{aubin2011} supplies
set-valued dynamics and tangential conditions, but no
\\emph{geometric} object that measures how a non-commuting sequence
of individually manageable changes accumulates into a viability
threat. The obstruction is structural: at a constraint-switching
boundary the active set changes, horizontal subspaces jump, the
connection $1$-form ceases to be defined, and the standard holonomy
integral fails exactly where the question is most interesting. This
paper constructs the missing object categorically: a stratified
connection with a boundary gluing law, a viability-weighted
curvature that contracts the curvature $2$-form with survival
covectors, and a compositional semantics (optics --- a map paired
with its feedback channel) under which
heterogeneous domain bridges compose into one typed endomorphism
whose fixed point is well posed and, for an explicit
instantiation, contractive."""),
(
"""\\paragraph{The problem.}
Living and engineered adaptive systems must continuously adjust
their internal controls to remain functional under shifting
external conditions. In classical viability theory, survival is
treated primarily as a set-membership problem: a system is viable
as long as its state stays within a predefined safe region
\\citep{aubin2011}. This static, set-theoretic perspective obscures
a subtle and ubiquitous failure mode: \\emph{path-dependent
vulnerability}. An organism or machine can successfully survive a
change in temperature, and it can separately survive a change in
nutrient availability. Yet, if these two environmental changes are
applied sequentially in a closed cycle --- first shifting
temperature, then nutrients, then reversing temperature, and
finally reversing nutrients --- the system may return to its
original environment with its internal reserves severely degraded.
The order matters, not only the magnitudes: this failure occurs
because optimal control strategies frequently do not
\\emph{commute} --- applying adaptation $A$ followed by adaptation
$B$ produces a different internal state than applying $B$ followed
by $A$. In differential geometry, the net discrepancy accumulated
around a closed loop is called \\emph{holonomy}, and its intensity
per unit area is called \\emph{curvature}. For orientation: a
\\emph{policy} is the optimizer's chosen response at each state; a
\\emph{connection} is the rule for comparing policies at nearby
states; and a policy loop's \\emph{holonomy} is the drift the closed
cycle accumulates --- the geometric signature of
non-commutativity.

\\paragraph{The obstruction.}
Why has this geometric insight not been systematically applied to
adaptive systems? The difficulty lies in \\emph{active-set
switches}. In any realistic system, adaptations are governed by
active physical bottlenecks --- maximum enzyme capacities, nutrient
uptake limits, thermal boundaries. Inside a regime where the active
bottlenecks do not change, the optimal strategy varies smoothly.
But when an environmental shift pushes the system across a
constraint boundary --- releasing an old bottleneck and activating
a new one --- the system's sensitivity changes abruptly. At these
boundary interfaces, the connection $1$-form describing
strategic adjustments undergoes a discontinuous jump, horizontal
subspaces cease to exist, classical smooth calculus and standard
curvature integrals break down, and traditional holonomy cannot be
evaluated across the interface --- exactly where the question is
most interesting. Classical viability theory supplies set-valued
dynamics and tangential conditions, but no geometric object that
measures how a non-commuting sequence of individually manageable
changes accumulates into a viability threat.

\\paragraph{The solution.}
This paper resolves the challenge by constructing a rigorous,
stratified geometric framework for adaptive systems. Rather than
treating constraint switches as troublesome discontinuities, we
show that the boundaries between operational regimes carry their
own well-defined, discrete geometric data. The missing object is
constructed categorically: a stratified connection with a boundary
gluing law, a viability-weighted curvature that contracts the
curvature $2$-form with survival covectors, and a compositional
semantics (optics --- a map paired with its feedback channel) under
which heterogeneous domain bridges compose into one typed
endomorphism whose fixed point is well posed and, for an explicit
instantiation, contractive."""),
))

# ---------------------------------------------------- C5 contributions
SPLICES.append(("contributions", (
"""\\paragraph{Contributions.}
\\begin{enumerate}[leftmargin=*,itemsep=2pt]
\\item The \\emph{SAVGS object}
(Definition~\\ref{def:savgs}): control base, policy bundle with
Fisher--Rao geometry, viability margin, maintenance graph, and a
$2$-categorical boundary span, assembled into one stratified
$G_C$-reduced bundle.
\\item The $2$-category $\\mathbf{StCon}(B)$ of stratified
$G_C$-connections (Definition~\\ref{def:stcon}), the
$2$-categorical gluing theorem (Theorem~\\ref{thm:2cat-gluing}), and
the piecewise holonomy formula
(Theorem~\\ref{thm:stratified-holonomy}), with the small-loop
expansion stated for closed loops crossing a switching wall
transversally in pairs and the boundary-reset contribution at its
true order, in agreement with the machine-verified numerics in
five loop geometries and three structure-group regimes.
\\item The \\emph{Fisher-minimal transport law} on
constant-active-set strata in closed KKT form
(Proposition~\\ref{prop:kkt}) and the \\emph{small-loop
viability--holonomy theorem} (Theorem~\\ref{thm:smallloop}): endpoint
erosion of a viability margin is bounded, to leading order, by the
viability-weighted curvature
(Definition~\\ref{def:kv}).
\\item The Bregman--Hessian Noether correspondence
(Proposition~\\ref{prop:noether}) with its falsifiable precondition
check, giving the gauge-covariance statement for the curvature.
\\item The \\emph{single composition theorem}
(Theorem~\\ref{thm:composition}): seven domain bridges typed as
optics, the realized update on a complete metric state space
(Definition~\\ref{def:realization}), per-optic analytic Lipschitz
constants (Lemma~\\ref{lem:lip-per-optic}), the Banach contraction
of the Krasnoselskii--Mann-averaged update for the chosen seven-map
instantiation (Theorem~\\ref{thm:unconditional-banach}), and the
projected CPTP channel contraction
(Theorem~\\ref{thm:zeno-contraction}) settling the Zeno
self-reference resolution.
\\item The filtered-colimit construction of RAF sets, proved at the
Set level with the adapter-level optic statement
(Theorem~\\ref{thm:filtered-colimits-optic}) and verified at scale
(Proposition~\\ref{prop:invlim-extended}).
\\item The $\\infty$-categorical extension via homotopy type theory
(Theorem~\\ref{thm:hott-composition},
Corollary~\\ref{cor:hott-fixedpoint}), with proof-sketch status
explicitly marked (Remark~\\ref{rem:proof-status-hott}), and the
three-phase autopoiesis closure test built on it
(Definition~\\ref{def:autopoiesis-phase3}).
\\end{enumerate}"""),
(
"""\\paragraph{Contributions.}
Our core contributions are organized as follows:
\\begin{enumerate}[leftmargin=*,itemsep=2pt]
\\item \\textbf{The SAVGS architecture}
(Section~\\ref{sec:savgs}): the \\emph{SAVGS object}
(Definition~\\ref{def:savgs}) --- control base, policy bundle with
Fisher--Rao geometry, viability margin, maintenance graph, and a
$2$-categorical boundary span, assembled into one stratified
$G_C$-reduced bundle.
\\item \\textbf{Stratified connections and boundary holonomy}
(Section~\\ref{sec:savgs}): the $2$-category $\\mathbf{StCon}(B)$ of
stratified $G_C$-connections (Definition~\\ref{def:stcon}), the
$2$-categorical gluing theorem (Theorem~\\ref{thm:2cat-gluing}), and
the piecewise holonomy formula
(Theorem~\\ref{thm:stratified-holonomy}), with the small-loop
expansion stated for closed loops crossing a switching wall
transversally in pairs and the boundary-reset contribution at its
true order, in agreement with the machine-verified numerics in
five loop geometries and three structure-group regimes.
\\item \\textbf{Viability-weighted curvature and vulnerability
bounds} (Section~\\ref{sec:savgs}): the \\emph{Fisher-minimal
transport law} on constant-active-set strata in closed KKT form
(Proposition~\\ref{prop:kkt}) and the \\emph{small-loop
viability--holonomy theorem} (Theorem~\\ref{thm:smallloop}): endpoint
erosion of a viability margin is bounded, to leading order, by the
viability-weighted curvature (Definition~\\ref{def:kv}).
\\item \\textbf{Conservation laws via information geometry}
(Section~\\ref{sec:noether}): the Bregman--Hessian Noether
correspondence (Proposition~\\ref{prop:noether}) with its
falsifiable precondition check, giving the gauge-covariance
statement for the curvature.
\\item \\textbf{Unified composition via optics}
(Sections~\\ref{sec:composition} and~\\ref{sec:lipschitz}): the
\\emph{single composition theorem}
(Theorem~\\ref{thm:composition}) --- seven domain bridges typed as
optics, the realized update on a complete metric state space
(Definition~\\ref{def:realization}), per-optic analytic Lipschitz
constants (Lemma~\\ref{lem:lip-per-optic}), the Banach contraction
of the Krasnoselskii--Mann-averaged update for the chosen seven-map
instantiation (Theorem~\\ref{thm:unconditional-banach}), and the
projected CPTP channel contraction
(Theorem~\\ref{thm:zeno-contraction}) settling the Zeno
self-reference resolution.
\\item \\textbf{Operational closure at scale}
(Section~\\ref{sec:invlim}): the filtered-colimit construction of
RAF sets, proved at the
Set level with the adapter-level optic statement
(Theorem~\\ref{thm:filtered-colimits-optic}) and verified at scale
(Proposition~\\ref{prop:invlim-extended}).
\\item \\textbf{The homotopy-theoretic extension}
(Section~\\ref{sec:hott}): the $\\infty$-categorical extension via
homotopy type theory
(Theorem~\\ref{thm:hott-composition},
Corollary~\\ref{cor:hott-fixedpoint}), with proof-sketch status
explicitly marked (Remark~\\ref{rem:proof-status-hott}), and the
three-phase autopoiesis closure test built on it
(Definition~\\ref{def:autopoiesis-phase3}).
\\end{enumerate}"""),
))

# -------------------------------------------- C6 application-paper bridge
SPLICES.append(("application-bridge", (
"""\\paragraph{Relation to the application paper.}
An application of this framework to metabolic flux rerouting appears
in a separate manuscript \\citep{zai2026measure}: there the"""),
(
"""\\paragraph{Relation to the application paper.}
In a companion manuscript \\citep{zai2026measure}, this geometric
framework is applied to genome-scale metabolic models of
\\emph{Escherichia coli}: there the"""),
))

# ------------------------------------------------- C7 Preliminaries lead
SPLICES.append(("prelim-lead", (
"""The standing objects of the paper are collected here for reference,
one definition at a time: the viability depth functional (and its"""),
(
"""To ensure precision while remaining accessible across disciplines,
we first define the core mathematical components of the framework,
one definition at a time: the viability depth functional (and its"""),
))

# ------------------------------------------------------ C8 SAVGS lead
SPLICES.append(("savgs-lead", (
"""The Stratified Autopoietic Viability Geometric System (SAVGS) is the
minimal object on which the viability-weighted curvature can be
stated with its type structure, gauge behavior, and premises
explicit. Five components assemble into one stratified object: a
control base, a policy bundle, a viability margin, a maintenance
graph, and a boundary span."""),
(
"""We now assemble the components into a single mathematical
structure: the Stratified Autopoietic Viability Geometric System
(SAVGS) --- the minimal object on which the viability-weighted
curvature can be stated with its type structure, gauge behavior,
and premises explicit. Five components assemble into one stratified
object: a control base, a policy bundle, a viability margin, a
maintenance graph, and a boundary span."""),
))

# ---------------------------------------------------- C9 Noether lead
SPLICES.append(("noether-lead", (
"""Noether's principle ties the symmetries of a Lagrangian to conserved
quantities. This section states the framework's analogue --- the
symmetry group of the distortion geometry yields the gauge covariance
of the curvature --- and checks the precondition where it applies."""),
(
"""In classical mechanics, Noether's theorem establishes that every
continuous symmetry of a physical system gives rise to a conserved
quantity (rotational symmetry yields conservation of angular
momentum). In adaptive systems, internal adjustments are often
driven by statistical divergences rather than physical kinetic
energy. This section states the framework's analogue --- an
analogous conservation law governs informational adaptation when
costs are modeled using Bregman divergences (such as relative
entropy or Kullback--Leibler divergence), so the symmetry group of
the distortion geometry yields the gauge covariance of the
curvature --- and checks the precondition where it applies."""),
))

# ------------------------------------------------- C10 Hierarchy lead
SPLICES.append(("hierarchy-lead", (
"""The quantitative claims of the framework are ordered by cost and
decisiveness, so that the cheapest decisive test comes first. This
section defines the hierarchy; Section~\\ref{sec:verdicts} executes the
battery."""),
(
"""To ensure the framework provides concrete, falsifiable empirical
utility rather than mere mathematical formalism, we establish a
seven-level testing hierarchy: each claim makes a specific,
quantitative prediction, and failure at any level refutes that
component of the model. The claims are ordered by cost and
decisiveness, so that the cheapest decisive test comes first. This
section defines the hierarchy; Section~\\ref{sec:verdicts} executes
the battery."""),
))

# ---------------------------------------------- C11 Composition lead
SPLICES.append(("composition-lead", (
"""The seven domain bridges of the framework are typed as optics so
that their composite is a single well-typed endomorphism of a state
space. This section constructs the composite, realizes it on a
complete metric space, and analyzes its contraction."""),
(
"""A central challenge in systems biology is connecting wildly
different levels of description: chemical reaction networks,
Bayesian information processing, fractals, conservation laws, and
geometric parallel transport. Here, we show that these
heterogeneous domains can be formalized as bidirectional optics and
composed into a single, unified mathematical system: the seven
domain bridges of the framework are typed as optics so that their
composite is a single well-typed endomorphism of a state space.
This section constructs the composite, realizes it on a complete
metric space, and analyzes its contraction."""),
))

# ------------------------------------------------ C12 Lipschitz lead
SPLICES.append(("lipschitz-lead", (
"""Does the composed seven-domain loop actually stabilize, or can it
drift or oscillate? A direct analysis gives a conditional answer: the"""),
(
"""Does this elaborate seven-domain feedback loop actually stabilize,
or can it drift or oscillate? A direct analysis gives a conditional
answer: the"""),
))
