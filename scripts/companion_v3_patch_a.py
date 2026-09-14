#!/usr/bin/env python3
"""companion_categorical_v2.tex -> companion_categorical_v3.tex, part A.

P0 fixes (external-audit scan, user directive) + 3rd-wave Fix 1 (optic
formalism) + Fix 4 (gluing hypothesis / remainder label) + the
structural and cosmetic items (F16, N13, N16, N17, N9, V6-paren,
C3-adjective, P0 stabilizer labels, P0 def:ard V-V attribution, P0
HoTT univalence sentence, P0 citation wiring for Hirota / Segura /
Dittrich / Handorf / Becker / Bravetti).

Frozen lineage untouched: reads scripts/companion_categorical_v2.tex,
writes scripts/companion_categorical_v3.tex (new file).
"""
import sys

SRC = "scripts/companion_categorical_v2.tex"
DST = "scripts/companion_categorical_v3.tex"

src = open(SRC).read()
n_applied = 0


def rep(old, new, what, count=1):
    global src, n_applied
    n = src.count(old)
    if n != count:
        print(f"FAIL [{what}]: found {n} occurrences (expected {count})")
        sys.exit(1)
    src = src.replace(old, new)
    n_applied += 1
    print(f"ok   [{what}] x{n}")


# ---------------------------------------------------------------------
# P0-1 / Fix 4a: gluing theorem hypothesis -> the standard gauge
# transform of Definition (O3), verbatim.
# ---------------------------------------------------------------------
rep(
    """satisfying
the matching condition $g_{ij}^* A_j = A_i + d(\\log g_{ij}) - [A_i, \\log
g_{ij}]$ on each $B_{ij}$, there exists a unique (up to 2-isomorphism)""",
    """satisfying
the matching condition (O3) of Definition~\\ref{def:stcon} on each
$B_{ij}$,
\\begin{equation*}
  A_j|_{B_{ij}} \\;=\\; g_{ij}^{-1}\\, A_i\\, g_{ij} \\;+\\; g_{ij}^{-1}\\,
  d g_{ij},
\\end{equation*}
there exists a unique (up to 2-isomorphism)""",
    "P0/Fix4: gluing hypothesis -> (O3) standard gauge transform",
)

# ---------------------------------------------------------------------
# Fix 4b: relabel the piecewise-F remainder O(eps^3) -> O(eps^2) with
# the affine-regime parenthetical.
# ---------------------------------------------------------------------
rep(
    """  - \\bigl[\\log g_{+-}(p_+) - \\log g_{+-}(p_-)\\bigr]
  + O(\\varepsilon^3)\\Bigr),
\\end{equation}""",
    """  - \\bigl[\\log g_{+-}(p_+) - \\log g_{+-}(p_-)\\bigr]
  + O(\\varepsilon^2)\\Bigr),
\\end{equation}
For affine wall transitions the terms neglected beyond the displayed
$O(\\varepsilon)$ and $O(\\varepsilon^2)$ contributions are
$O(\\varepsilon^3)$ --- the regime the numerics of
Remark~\\ref{rem:2cat-gluing-numeric} verify; for general
transitions, second-order Taylor terms of $\\log g_{+-}$ along the
wall and commutators of the two resets enter at $O(\\varepsilon^2)$
(Open Problem~1).""",
    "Fix4: piecewise-F remainder O(eps^3) -> O(eps^2) + affine parenthetical",
)

# ---------------------------------------------------------------------
# N13: one symbol for the stratified holonomy inside the same theorem
# (H^strat -> Hol^strat in eq:piecewise-F).
# ---------------------------------------------------------------------
rep(
    """\\begin{equation}\\label{eq:piecewise-F}
  H^{\\mathrm{strat}}(\\gamma_\\varepsilon) \\;=\\;""",
    """\\begin{equation}\\label{eq:piecewise-F}
  \\mathrm{Hol}^{\\mathrm{strat}}(\\gamma_\\varepsilon) \\;=\\;""",
    "N13: H^strat -> Hol^strat in eq:piecewise-F",
)

# ---------------------------------------------------------------------
# P0-5 / F17: stabilizer labels in rem:n3-n4 aligned with
# def:struct (SO(2)/SO(3) prototypes; O(n-1) point stabilizer; CO(r)
# only under the Weyl structure).
# ---------------------------------------------------------------------
rep(
    """At $n=3$ the policy simplex is two-dimensional, the Fisher--Rao
stabilizer is $\\CO(2)=\\RR_+\\ltimes\\SO(2)$, and the Lie algebra""",
    """At $n=3$ the policy simplex is two-dimensional, the prototype's
structure group is $\\SO(2)$
(Definition~\\ref{def:struct}; the full Fisher--Rao point stabilizer
on the simplex is $O(n-1)\\supseteq SO(n-1)$, and $\\CO(2)=\\RR_+
\\ltimes\\SO(2)$ arises only under the Weyl structure of
Remark~\\ref{rem:fisher-weyl}), and the Lie algebra""",
    "P0/F17: n=3 stabilizer label aligned with def:struct",
)
rep(
    """At $n=4$ the policy simplex is three-dimensional, the stabilizer is
$\\CO(3)=\\RR_+\\ltimes\\SO(3)$, and $\\so(3)$ is three-dimensional with""",
    """At $n=4$ the policy simplex is three-dimensional, the prototype's
structure group is $\\SO(3)$ (Definition~\\ref{def:struct}; $\\CO(3)$
again only under the Weyl structure), and $\\so(3)$ is
three-dimensional with""",
    "P0/F17: n=4 stabilizer label aligned with def:struct",
)

# ---------------------------------------------------------------------
# P0-4: Vereshchagin-Vitanyi attribution at Definition def:ard itself.
# ---------------------------------------------------------------------
rep(
    """It is monotone non-increasing in $D$, bounded above by the Kolmogorov
complexity $K(x)$, and upper-semicomputable by dovetailing over all
programs. It is a single-string, intrinsically deterministic
quantity: no set-average rate and no random-coding gap arise.""",
    """It is monotone non-increasing in $D$, bounded above by the Kolmogorov
complexity $K(x)$, and upper-semicomputable by dovetailing over all
programs. It is a single-string, intrinsically deterministic
quantity: no set-average rate and no random-coding gap arise. The
construction is the algorithmic rate--distortion distance of
Vereshchagin and Vit\\'anyi~\\citep{vereshchagin2010rate}, stated
here in its single-string form; the set-level rate--distortion
theory of Shannon is the coarse-grained
counterpart.""",
    "P0: V-V attribution at def:ard",
)

# ---------------------------------------------------------------------
# P0-3 / F9: the false univalence sentence in the HoTT proof sketch.
# ---------------------------------------------------------------------
rep(
    """unique fixed point in each hom-set. The homotopy limit of the
constant tower $\\mathrm{holim}_\\Delta T$ aggregates these fixed points
into a contractible $\\infty$-groupoid. By the univalence axiom
(``equivalence is equivalent to equality''), the type of contractible
$\\infty$-groupoids is equivalent to the universe type $\\mathcal{U}$,
providing the canonical identification. (A model-independent treatment""",
    """unique fixed point in each hom-set. The homotopy limit of the
constant tower $\\mathrm{holim}_\\Delta T$ aggregates these fixed points
into a contractible $\\infty$-groupoid. By the univalence axiom
(``equivalence is equivalent to equality''), any contractible
$\\infty$-groupoid is equivalent to the unit type $1$, so the
fixed-point $\\infty$-groupoid is identified with a single term of
the universe $\\mathcal{U}$ up to a contractible space of choices ---
the type of contractible $\\infty$-groupoids is itself contractible
(not $\\mathcal{U}$-equivalent), which is the precise content of the
identification. (A model-independent treatment""",
    "P0/F9: univalence sentence corrected (contractible ~ 1, not U)",
)

# The N11 Bousfield-Kan attribution repair (minor, one line).
rep(
    """By the Bousfield--Kan
construction~\\cite[Ch.~XI]{cisinski2019}, the homotopy pullback of a""",
    """By the Bousfield--Kan
construction~\citep{bousfield1972}, the homotopy pullback of a""",
    "N11: Bousfield-Kan attribution to the 1972 construction",
)

# ---------------------------------------------------------------------
# P0-2 / Fix 1: one optic formalism. Replace the triple-form
# Definition def:optic by Riley's pair form with the coend relation;
# add the strict-feedback representative remark.
# ---------------------------------------------------------------------
rep(
    """\\begin{definition}[Optic category]
\\label{def:optic}
Following Riley~\\cite{riley2018optics}, for a category $\\CC$ with finite
limits the \\emph{optic category} $\\Optic(\\CC)$ has as objects triples
$(M, C, R)$ of a forward carrier $M$, a backward carrier $C$, and a
residual $R$, and as morphisms pairs $(\\varphi, \\rho)$ of a forward map
$\\varphi:M\\to M'$ and a backward map $\\rho:R'\\to R$ satisfying the
residual-compatibility condition. The monoidal structure of
$\\Optic(\\CC)$ supplies composition, associativity, and unitality
(Proposition~2.3 of~\\cite{riley2018optics}).
\\end{definition}""",
    """\\begin{definition}[Optic category]
\\label{def:optic}
Following Riley~\\cite{riley2018optics}, for a monoidal category
$(\\CC, \\otimes, I)$ with finite limits the \\emph{optic category}
$\\Optic(\\CC)$ has as \\emph{objects} pairs $(M, C)$ of a forward
carrier $M$ and a backward carrier $C$, and as \\emph{morphisms} from
$(M, C)$ to $(M', C')$ the equivalence classes $[R, f, g]$ of triples
consisting of a residual object $R$, a forward map
$f : M \\otimes R \\to M'$, and a backward map $g : C' \\to C \\otimes
R$, quotiented by the coend relation: $[R, f, g] = [R', f', g']$
whenever there exists $h : R \\to R'$ with
$f' \\circ (\\mathrm{id}_M \\otimes h) = f$ and
$(\\mathrm{id}_C \\otimes h) \\circ g' = g$. Composition is
Riley's Proposition~2.3~\\cite{riley2018optics}: the composite of
$[R, f, g]$ followed by $[R', f', g']$ is
$[R \\otimes R',\\; f' \\circ (f \\otimes \\mathrm{id}_{R'}),\\;
(g \\otimes \\mathrm{id}_{R'}) \\circ g']$, with unit
$[I, \\rho, \\eta]$ given by the left/right unitors of $\\CC$. The
adapter subcategory is the case $R = I$ (trivial residual).
\\end{definition}

\\begin{remark}[Strict feedback representatives]
\\label{rem:optic-strict}
The operational sections of this paper
(Construction~\\ref{con:seven}, Table~\\ref{tab:optics},
Definition~\\ref{def:realization}, and
Section~\\ref{sec:invlim}) work with \\emph{strict feedback
representatives} over $\\CC = \\mathbf{Set}$ (cartesian monoidal): a
morphism from $(M, C)$ to $(M', C')$ is a triple $(R, f, g)$ with
$f : M \\times R \\to M'$ and $g : R \\times C' \\to C$ --- the
representative-level shape in which the residual, consumed by the
forward pass, is reused as the backward pass's input (the feedback
instantiation appropriate when the forward pass transports the
residual, as in Definition~\\ref{def:realization}). Strict feedback
morphisms compose by
\\begin{equation}\\label{eq:feedback-comp}
  (R_2, f_2, g_2) \\circ (R_1, f_1, g_1)
  \\;=\\; \\bigl(R_1 \\times R_2,\\;
  f_2 \\circ (f_1 \\times \\mathrm{id}_{R_2}),\\;
  g_1 \\circ (\\mathrm{id}_{R_1} \\times g_2)\\bigr),
\\end{equation}
with unit $(1, \\pi, \\mathrm{co}\\pi)$ on the (co)product projections;
associativity and unitality follow directly from function
composition and the associativity of finite products, and the
composite's residual $R_1 \\times R_2$ is the representative-level
form of Riley's $R \\otimes R'$. On the adapter subcategory
($R = 1$) the strict feedback form and the coend form of
Definition~\\ref{def:optic} coincide. The general translation
between the strict feedback form and the coend-quotient form is
recorded as an open problem (Section~\\ref{sec:future}); nothing
below depends on it: every statement of this paper is typed in the
strict form and every composition law is verified at the
representative level.
\\end{remark}""",
    "P0/Fix1: Def def:optic -> Riley pairs + coend; strict feedback remark",
)

# Construction con:seven: declare the strict feedback typing.
rep(
    """Let $\\CC$ be a category with finite limits. Let $\\OO_1,\\ldots,\\OO_7\\in
\\Optic(\\CC)$ be the seven optics corresponding to the seven arcs of
domain unification:""",
    """Let $\\CC$ be a category with finite limits. Let $\\OO_1,\\ldots,\\OO_7$
be the seven optics corresponding to the seven arcs of domain
unification, typed as strict feedback morphisms
(Remark~\\ref{rem:optic-strict}) with carrier pairs
$(M_i, C_i)$:""",
    "Fix1: con:seven typed as strict feedback morphisms",
)

# Table caption: pair form.
rep(
    """\\caption{Seven-optic composition. Each arc is decomposed as an optic
$(M_i, C_i, R_i)$ in $\\Optic(\\CC)$ with forward $\\varphi_i$ (encoder),
backward $\\rho_i$ (decoder), and residual $\\mathrm{Res}_i$ (information
flowing forward to backward). The compatibility condition
$A_i = M_{i+1}$ holds by construction. The total residual of $T$ is the
product $\\mathrm{Res}_1\\times\\cdots\\times\\mathrm{Res}_7$ in $\\CC$.}""",
    """\\caption{Seven-optic composition. Each arc is decomposed as a strict
feedback optic with carrier pair $(M_i, C_i)$
(Remark~\\ref{rem:optic-strict}) and residual $\\mathrm{Res}_i$: forward
$\\varphi_i : M_i \\times \\mathrm{Res}_i \\to M_{i+1}$ (encoder), backward
$\\rho_i : \\mathrm{Res}_i \\times C_{i+1} \\to C_i$ (decoder), the
residual the object transported from the forward to the backward
pass. The compatibility condition $A_i = M_{i+1}$ holds by
construction. The total residual of $T$ is the product
$\\mathrm{Res}_1\\times\\cdots\\times\\mathrm{Res}_7$ in $\\CC$,
the representative-level form of the composite residual of
Riley's Proposition~2.3.}""",
    "Fix1: tab:optics caption in the pair/strict form",
)

# Composition theorem proof: replace the monoidal-language sentences.
rep(
    """\\begin{proof}[Proof]
$\\Optic(\\CC)$ is a monoidal category under optic composition: the
tensor product is $\\OO_2\\circ\\OO_1$ with the identity optic as unit;
the associativity and unitality axioms follow from the universal
property of the product $\\mathrm{Res}_1\\times\\mathrm{Res}_2$ in $\\CC$
(Proposition~2.3 of~\\cite{riley2018optics}).
The seven-fold composition $T=\\OO_7\\circ\\cdots\\circ\\OO_1$ is therefore
well-defined as the iterated monoidal product. The associativity axiom
gives
$(\\OO_7\\circ\\OO_6)\\circ(\\OO_5\\circ\\OO_4)\\circ(\\OO_3\\circ\\OO_2)\\circ\\OO_1
= \\OO_7\\circ(\\OO_6\\circ\\OO_5)\\circ(\\OO_4\\circ\\OO_3)\\circ(\\OO_2\\circ\\OO_1)
= \\cdots = $ the canonical seven-fold product, by the associativity
isomorphism. All parenthesizations are equal modulo the canonical
associativity isomorphisms. The unitality axioms $T\\circ\\mathrm{Id}=T$
and $\\mathrm{Id}\\circ T=T$ follow from the terminality of the unit
residual. The residual of $T$ is $\\mathrm{Res}_T=\\mathrm{Res}_1\\times
\\cdots\\times\\mathrm{Res}_7$, with the canonical associativity and
unitality isomorphisms from $\\CC$ (which is a category with finite
limits, so finite products exist and are well-defined up to canonical
isomorphism).""",
    """\\begin{proof}[Proof]
Optic composition is associative and unital: in the strict feedback
form of Remark~\\ref{rem:optic-strict} the composition
law~\\eqref{eq:feedback-comp} reduces associativity to the
associativity of function composition together with the canonical
associativity of the finite products
$\\mathrm{Res}_1 \\times \\mathrm{Res}_2 \\times \\mathrm{Res}_3$ in
$\\CC$, and unitality to the product/unitality isomorphisms of
$\\CC$; the same holds for the coend classes of
Definition~\\ref{def:optic} by Riley's
Proposition~2.3~\\cite{riley2018optics}, whose composite residual is
$R \\otimes R'$ (the cartesian product in $\\mathbf{Set}$).
The seven-fold composition $T=\\OO_7\\circ\\cdots\\circ\\OO_1$ is therefore
well-defined as the iterated composite. Associativity gives
$(\\OO_7\\circ\\OO_6)\\circ(\\OO_5\\circ\\OO_4)\\circ(\\OO_3\\circ\\OO_2)\\circ\\OO_1
= \\OO_7\\circ(\\OO_6\\circ\\OO_5)\\circ(\\OO_4\\circ\\OO_3)\\circ(\\OO_2\\circ\\OO_1)
= \\cdots = $ the canonical seven-fold composite. All parenthesizations
are equal modulo the canonical associativity isomorphisms. The
unitality axioms $T\\circ\\mathrm{Id}=T$ and $\\mathrm{Id}\\circ T=T$
hold with the trivial-residual unit. The residual of $T$ is
$\\mathrm{Res}_T=\\mathrm{Res}_1\\times\\cdots\\times\\mathrm{Res}_7$, with
the canonical associativity and unitality isomorphisms from $\\CC$
(which is a category with finite limits, so finite products exist and
are well-defined up to canonical isomorphism).""",
    "Fix1: composition proof in composition-law language",
)

# cor:unification: retype to realization fixed points.
rep(
    """\\begin{corollary}[Unification object]\\label{cor:unification}
Under the conditions of Theorem~\\ref{thm:composition}, suppose further
that $T$ has a fixed point $\\OO^*$ with $T(\\OO^*)=\\OO^*$. Then $\\OO^*$
is the unification object of the cross-domain unification. The forward
component of $\\OO^*$ encodes the entire RAF $\\to$ RPSI $\\to$ IFS $\\to$
Noether $\\to$ perturbation $\\to$ WCIG $\\to$ $n=3$ Fisher--Rao chain in
a single encoding; the backward component decodes the entire chain; the
residual of $\\OO^*$ is the product of all seven residuals.
\\end{corollary}""",
    """\\begin{corollary}[Unification object]\\label{cor:unification}
Under the conditions of Theorem~\\ref{thm:composition}, let $O$ be the
typed endo-optic~\\eqref{eq:comp} with realization $R(O) : S \\to S$
(Definition~\\ref{def:realization}), and suppose $R(O)$ is a
contraction on the complete metric state space $S$
(Theorem~\\ref{thm:unconditional-banach}). Then $R(O)$ has a unique
fixed point $x^{*} \\in S$. The \\emph{unification object} of the
cross-domain unification is the pair $(O, x^{*})$: the endo-optic $O$
encodes the entire RAF $\\to$ RPSI $\\to$ IFS $\\to$ Noether $\\to$
perturbation $\\to$ WCIG $\\to$ $n=3$ Fisher--Rao chain in a single
typed morphism (forward components encoding, backward components
decoding, residual the product of the seven residuals), and $x^{*}$
is the self-consistent state it synthesizes. The endo-optic $T$ of
\\eqref{eq:comp} is itself a morphism and has no object-level fixed
points (Remark~\\ref{rem:typed-optic}); fixed points live on the
realized state space.
\\end{corollary}""",
    "Fix1: cor:unification retyped (realization fixed points)",
)

# prop:sufficient: fixed-point object + gloss.
rep(
    """\\begin{proposition}[Sufficient condition for fixed-point existence]
\\label{prop:sufficient}
A sufficient condition for the existence of $\\OO^*$ is the Bregman-
regularized contraction of $T$. Under this condition, $T$ has a unique
fixed point by Banach's fixed-point theorem~\\cite{banach1922}.
\\end{proposition}""",
    """\\begin{proposition}[Sufficient condition for fixed-point existence]
\\label{prop:sufficient}
A sufficient condition for the existence of the fixed point
$x^{*}$ of Corollary~\\ref{cor:unification} is the contraction of the
Krasnoselskii--Mann-averaged realization
$R(O)_{\\mathrm{reg}}$ of Proposition~\\ref{prop:treg-lip}. Under this
condition $R(O)_{\\mathrm{reg}}$ has a unique fixed point by Banach's
fixed-point theorem~\\cite{banach1922}.
\\end{proposition}""",
    "Fix1/F21: prop:sufficient retyped + KM gloss",
)

# def:hott-optic: declare the diagonal specialization.
rep(
    """The $\\infty$-category $\\Optic(\\mathcal{C}_\\infty)$ is the cartesian
fibration over the twisted-arrow $\\infty$-category
$\\mathrm{Tw}(\\mathcal{C}_\\infty)$ encoding these morphisms; the
construction generalizes the 1-categorical optic category
of~\\cite{riley2018optics} to the $\\infty$-categorical setting via the
$\\infty$-cosmos framework of~\\cite{riehlverity2022}.""",
    """The $\\infty$-category $\\Optic(\\mathcal{C}_\\infty)$ is the cartesian
fibration over the twisted-arrow $\\infty$-category
$\\mathrm{Tw}(\\mathcal{C}_\\infty)$ encoding these morphisms. This is the
\\emph{diagonal} specialization of the 1-categorical optic shape of
Definition~\\ref{def:optic}: the forward and backward carriers are
identified per interface ($S$ at the source, $A$ at the target), and
the residual enters both components --- the $\\infty$-categorical
lift of the strict feedback form of
Remark~\\ref{rem:optic-strict} rather than of the general pair
form; the general $\\infty$-level pair form is not constructed here
(Open Problem~4). The $\\infty$-cosmos framework
of~\\cite{riehlverity2022} supplies the ambient model theory.""",
    "Fix1: def:hott-optic declared the diagonal specialization",
)

# ---------------------------------------------------------------------
# F16: radius-2 sphere in prop:sqrt.
# ---------------------------------------------------------------------
rep(
    """The square-root embedding $\\psi_a = 2\\sqrt{p_a}$ places the open simplex
$\\Delta^{n-1}$ on the positive orthant of the unit sphere
$S^{n-1}\\subset\\RR^n$.""",
    """The square-root embedding $\\psi_a = 2\\sqrt{p_a}$ places the open simplex
$\\Delta^{n-1}$ on the positive orthant of the sphere of radius
$2$, $\{x\\in\\RR^n : \\|x\\| = 2\\}$ (the map $p \\mapsto \\psi(p)$ has
$\\|\\psi\\| = 2$ since $\\sum_a p_a = 1$).""",
    "F16: unit sphere -> radius-2 sphere",
)

# ---------------------------------------------------------------------
# N16: fourteen orders of magnitude.
# ---------------------------------------------------------------------
rep(
    """The verdict of Claim~F is positive: the commuting and
non-commuting control families are separated by fifteen orders of
magnitude in signature size.""",
    """The verdict of Claim~F is positive: the commuting and
non-commuting control families are separated by fourteen orders of
magnitude in signature size ($7.82\\times 10^{-16}$ versus
$0.1522$).""",
    "N16: fifteen -> fourteen orders",
)

# ---------------------------------------------------------------------
# N17: remove the functionless misner1973 import.
# ---------------------------------------------------------------------
rep(
    """Bregman-regularization strengths, with the Hausdorff distance
between successive iterates fit to a geometric tail. Holonomy
terminology follows \\citealp{misner1973}.""",
    """averaging strengths, with the Hausdorff distance
between successive iterates fit to a geometric tail.""",
    "N17: stray misner1973 citation removed",
)

# ---------------------------------------------------------------------
# N9: tightness remark numbers 0.69 -> 0.697.
# ---------------------------------------------------------------------
rep(
    """The analytic bound~\\eqref{eq:qbound} is sharp in the regime of
Proposition~\\ref{prop:titer-control} below --- six contractions
and one expansion, $\\Lip(f_2)=1.15$, product $\\approx0.69$ --- and
yet it stays above the measured $q$'s: at $\\lambda=0.5$ the bound
is $0.845$ against the measured $q=0.5182$; at $\\lambda=0.7$ it is
$0.907$ against $q=0.7075$.""",
    """The analytic bound~\\eqref{eq:qbound} is sharp in the regime of
Proposition~\\ref{prop:titer-control} below --- six contractions
and one expansion, $\\Lip(f_2)=1.15$, product $0.697$ --- and
yet it stays above the measured $q$'s: at $\\lambda=0.5$ the bound
is $0.8485$ against the measured $q=0.5182$; at $\\lambda=0.7$ it is
$0.909$ against $q=0.7075$.""",
    "N9: tightness remark 0.69 -> 0.697 (0.845 -> 0.8485, 0.907 -> 0.909)",
)

# ---------------------------------------------------------------------
# V6: the stray unbalanced parenthesis in prop:invlim-extended.
# ---------------------------------------------------------------------
rep(
    """Direct enumeration of all $2^{11}-1=2047$ non-empty subsets of the
$11$-reaction set of Construction~\\ref{con:invlim-extended} ) produces $16$ non-trivial""",
    """Direct enumeration of all $2^{11}-1=2047$ non-empty subsets of the
$11$-reaction set of Construction~\\ref{con:invlim-extended} produces $16$ non-trivial""",
    "V6: stray parenthesis removed",
)

# ---------------------------------------------------------------------
# C3: tie-break adjective in rem:fba-kappa-superseded.
# ---------------------------------------------------------------------
rep(
    "(tie-break robustness across five lexicographic selection rules)",
    "(tie-break robustness across the five-rule stage-3 selection "
    "battery --- declared plus four variants --- of the lexicographic "
    "protocol class)",
    "C3: tie-break battery phrasing in rem:fba-kappa-superseded",
)

# ---------------------------------------------------------------------
# P0-1 citation wiring: Hirota/Segura (categorical autopoiesis),
# Dittrich (closure criteria = COT), Becker (CPTP-Zeno), Bravetti
# (Noether). Sites chosen where each topic is introduced.
# ---------------------------------------------------------------------
rep(
    """\\begin{definition}[Operational closure criteria]
\\label{def:closure-criteria}
A SAVGS is \\emph{operationally closed} at the maintenance graph""",
    """\\begin{definition}[Operational closure criteria]
\\label{def:closure-criteria}
These criteria are the dynamical counterpart of the closed,
self-maintaining sets of chemical organization
theory~\\citep{dittrich2007cot} and of the categorical-autopoiesis
formalizations of \\citet{hirota2023alife}
and \\citet{segura2026topos}. A SAVGS is \\emph{operationally closed}
at the maintenance graph""",
    "P0/F22: Dittrich + Hirota + Segura cited at def:closure-criteria",
)

rep(
    """\\begin{proposition}[Bregman--Hessian Noether correspondence]""",
    """\\begin{proposition}[Bregman--Hessian Noether correspondence;
cf.\\ the contact-geometric Noether program of thermodynamics,
\\citet{bravetti2023noether}]""",
    "P0: Bravetti cited at prop:noether",
)

rep(
    """\\subsection{The CPTP--Zeno lift and the Claim G scaling verdict}
\\label{sec:verdict-cptp}""",
    """\\subsection{The CPTP--Zeno lift and the Claim G scaling verdict}
\\label{sec:verdict-cptp}

The open-quantum-systems treatment of the Zeno effect whose
Kraus/Lindblad skeleton is used below is due
to~\\citet{becker2021zeno} (among others).""",
    "P0: Becker cited at the CPTP-Zeno lift",
)

# Handorf: network-expansion citation at the designed-progression
# framing (F22's battery-sits-in-NE-territory point).
rep(
    """converts precisely the components the test flags as failing.""",
    """The \\emph{designed progression} is a sequence of integrated
metabolic--gene-regulatory networks in which each modification is
a hypothesis about what organizational closure requires; it
measures the test's sensitivity, since each added redundant route
converts precisely the components the test flags as failing. The
progression sits in the network-expansion territory
of~\\citet{handorf2005network}; the structural-instrument benchmark
of Section~\\ref{sec:network-keio-e14} compares the two instruments
directly.""",
    "P0: Handorf cited at the designed-progression framing",
)

open(DST, "w").write(src)
print(f"\npart A complete: {n_applied} edits -> {DST}")
