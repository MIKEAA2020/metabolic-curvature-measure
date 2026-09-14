#!/usr/bin/env python3
"""companion v3 part B1b: the remaining Fix 6 edits (box-invariance
paragraph, K instantiation, KM gloss replacements, qbound hypothesis
drop, abstract/contribution wording). In place on
scripts/companion_categorical_v3.tex. Run after b1."""
import sys

F = "scripts/companion_categorical_v3.tex"
src = open(F).read()
n_applied = 0


def rep(old, new, what, count=1):
    global src, n_applied
    n = src.count(old)
    if n != count:
        print(f"FAIL [{what}]: found {n} (expected {count})")
        sys.exit(1)
    src = src.replace(old, new)
    n_applied += 1
    print(f"ok   [{what}] x{n}")


rep(r"""The mixing parameters $\alpha_{i}=0.40$, saturation scalings
$s_{i}=1.00$, and operator norms $\rho_{i}=0.80$ for $i\in
\{1,3,4,5,6,7\}$, together with $\lambda_{2}=1.15$, are chosen so
that the per-optic analytic bounds below are uniform across the
dimensional range and the product bound is comfortably below $1$.""",
    r"""The mixing parameters $\alpha_{i}=0.40$, saturation scalings
$s_{i}=1.00$, and operator norms $\rho_{i}=0.80$ for $i\in
\{1,3,4,5,6,7\}$, together with $\lambda_{2}=1.15$, are chosen so
that the per-optic analytic bounds below are uniform across the
dimensional range and the product bound is comfortably below $1$.

\emph{Box invariance (the hypothesis $T:X\to X$).} The maps
$W_{i}, b_{i}$ are not pinned to single values; the bounds below are
uniform over \emph{all} pairs $(W_{i}, b_{i})$ with the declared
operator norm $\|W_{i}\|_{\mathrm{op}}=\rho_{i}$ --- the
box-invariance computation never uses $b_{i}$ (the range of
$\tanh$ absorbs any bias) and uses $W_{i}$ only through its operator
norm. Each contracting $f_{i}$ maps the closed box of half-width
$B$, $[-B,B]^{d}$, into
$(1-\alpha)[-B,B]+\alpha\,s\,(-1,1)^{d}\subseteq
[-(0.6B+0.4),\,0.6B+0.4]^{d}$ (with $\alpha=0.40$, $s=1.00$); the
chain's widest image is attained immediately after the expansion
$f_{2}=1.15\,\mathrm{Id}$, giving half-width
$C=1.15\,(0.6B+0.4)$; every subsequent contracting map shrinks any
box of half-width $\geq 1$ (since $0.6C+0.4\leq C$ iff $C\geq 1$).
Invariance of $X=[-1.5,1.5]^{d}$ requires $C\leq B$, i.e.\
$1.15\,(0.6B+0.4)\leq B$, i.e.\ $0.69B+0.46\leq B$, i.e.\
$B\geq 0.46/0.31\approx 1.484$; $B=1.5$ satisfies it with margin
($C=1.15\cdot 1.3=1.495\leq 1.5$). Hence $T:X\to X$ and
$\Lip(T)\leq 0.92^{6}\cdot 1.15=0.697<1$: Banach's theorem applies
on the enlarged box. (On the smaller box $[0,1]^{d}$ the hypothesis
fails: the chain's image reaches approximately $[-1.0,1.01]^{d}$ on
the low side and $1.15$ on the high side.)""",
    "Fix6: box-invariance verification paragraph")

rep(r"""complete metric state space $S$ (e.g.\ $X=[0,1]^d$ with the Euclidean
metric) is the endomap""",
    r"""complete metric state space $S$ (e.g.\ $X=[-1.5,1.5]^d$ with the
Euclidean metric) is the endomap""",
    "Fix6: def:realization state space example")

rep(r"""\begin{proposition}[Lipschitz bound for the Bregman-regularized update]
\label{prop:treg-lip}""",
    r"""\begin{proposition}[Lipschitz bound for the
Krasnoselskii--Mann-averaged update]
\label{prop:treg-lip}""",
    "Fix6/F21: treg-lip title de-Bregmanized")

rep(r"""The
Krasnoselskii--Mann-averaged (Bregman-regularized) update
\begin{equation}\label{eq:treg-def}
  T_{\mathrm{reg}}(K) \;=\; (1-\lambda)\,T(K) +
  \lambda\,\Pi_{\mathcal K}(T(K)), \qquad \lambda \in [0,1),
\end{equation}""",
    r"""The
Krasnoselskii--Mann-averaged (Euclidean-projection) update
\begin{equation}\label{eq:treg-def}
  T_{\mathrm{reg}}(x) \;=\; (1-\lambda)\,T(x) +
  \lambda\,\Pi_{\mathcal K}(T(x)), \qquad \lambda \in [0,1),
\end{equation}""",
    "Fix6/F21: treg-def point variable + Euclidean projection gloss")

rep(r"""by the triangle inequality, the $\rho$-Lipschitz property of $T$,
and the $1$-Lipschitz property of the Euclidean projection onto a
closed convex set (Moreau decomposition).
\end{proof}""",
    r"""by the triangle inequality, the $\rho$-Lipschitz property of $T$,
and the $1$-Lipschitz property of the Euclidean projection onto a
closed convex set (Moreau decomposition).
\end{proof}

\begin{remark}[Instantiation of the regularization set]
\label{rem:km-instantiation}
For the seven-map instantiation the regularization set is instantiated
as $\mathcal K:=[-1,1]^{d}\subseteq X=[-1.5,1.5]^{d}$. Then
$T_{\mathrm{reg}}(X)\subseteq (1-\lambda)\,T(X)+\lambda\,
\Pi_{\mathcal K}(X)\subseteq (1-\lambda)\,[-1.495,1.495]^{d}
+\lambda\,[-1,1]^{d}\subseteq X$, so $T_{\mathrm{reg}}:X\to X$ and
Proposition~\ref{prop:treg-lip} applies with
$\rho=\Lip(T)\leq 0.697$.
\end{remark}""",
    "Fix6: K := [-1,1]^d instantiation remark")

rep(r"""Consequently, by
Proposition~\ref{prop:treg-lip}, the Bregman-regularized
update~\eqref{eq:treg-def}
is Lipschitz with""",
    r"""Consequently, by
Proposition~\ref{prop:treg-lip}, the Krasnoselskii--Mann-averaged
update~\eqref{eq:treg-def}
is Lipschitz with""",
    "Fix6: Banach theorem KM gloss")

rep(r"""for every $\lambda\in[0,1)$. The Banach fixed-point theorem then
applies without further hypotheses: $T_{\mathrm{reg}}:X\to X$ on the
complete metric space
$X=[0,1]^{d}$ has a unique
fixed point $K^{*}$, which is the unification object of
Corollary~\ref{cor:unification}.
\end{theorem}""",
    r"""for every $\lambda\in[0,1)$. The Banach fixed-point theorem then
applies: $T_{\mathrm{reg}}:X\to X$ on the complete metric space
$X=[-1.5,1.5]^{d}$ (the box-invariance hypothesis verified above)
has a unique fixed point $x^{*}$, which realizes the unification
object of Corollary~\ref{cor:unification}.
\end{theorem}""",
    "Fix6: Banach theorem box + fixed-point name x*")

rep(r"""theorem~\cite{banach1922} applies on the complete metric space
$X=[0,1]^{d}$ (compact subset of $\RR^{d}$, hence complete; the
Euclidean metric is complete) because $\Lip(T_{\mathrm{reg}})<1$.""",
    r"""theorem~\cite{banach1922} applies on the complete metric space
$X=[-1.5,1.5]^{d}$ (compact subset of $\RR^{d}$, hence complete; the
Euclidean metric is complete), where the box-invariance paragraph
above verifies $T:X\to X$ and hence $T_{\mathrm{reg}}:X\to X$,
because $\Lip(T_{\mathrm{reg}})<1$.""",
    "Fix6: Banach proof box")

rep(r"""to obtain~\eqref{eq:product-lip}. The Bregman-regularized bound
follows from Proposition~\ref{prop:treg-lip}""",
    r"""to obtain~\eqref{eq:product-lip}. The averaged-update bound
follows from Proposition~\ref{prop:treg-lip}""",
    "Fix6: Banach proof gloss")

rep(r"""\begin{proposition}[Analytic upper bound on the contraction rate]
\label{prop:qbound}
Let $f_1,\ldots,f_7:X\to X$ be the seven forward maps of
Construction~\ref{con:seven}, each a Lipschitz map on the compact
convex set $X\subset\RR^{d}$ with Lipschitz constants
$\Lip(f_i)$, each $\alpha_i$-strongly monotone with
$\alpha_i\geq0$ and $\beta_i$-cocoercive with $\beta_i\geq0$
(standard hypotheses of convex optimization). Then the
Bregman-regularized composite $T_{\mathrm{reg}}(K)=(1-\lambda)\,
T(K)+\lambda\,\Pi_{\mathcal K}(T(K))$ is Lipschitz with""",
    r"""\begin{proposition}[Analytic upper bound on the contraction rate]
\label{prop:qbound}
Let $f_1,\ldots,f_7:X\to X$ be the seven forward maps of
Construction~\ref{con:seven}, each a Lipschitz map on the compact
convex set $X\subset\RR^{d}$ with Lipschitz constants
$\Lip(f_i)$, and $T=f_7\circ\cdots\circ f_1$ the composite. Then the
Krasnoselskii--Mann-averaged composite
$T_{\mathrm{reg}}=(1-\lambda)\,T+\lambda\,\Pi_{\mathcal K}\circ T$
is Lipschitz with""",
    "Fix6/F21: qbound hypotheses dropped, KM composite")

rep(r"""the empirical $q$'s are smaller
because the Bregman regularization reorganizes the trajectories
toward the interior of $\mathcal K$ rather than merely averaging
them. Sharpening the bound to recover the empirical $q$'s
analytically is open.""",
    r"""the empirical $q$'s are smaller because the averaging projection
contracts every iterate toward $\mathcal K$ and the instantiation's
iterates are better behaved than the worst case the bound tracks.
Sharpening the bound to recover the empirical $q$'s
analytically is open.""",
    "Fix6/F21: tightness remark de-Bregmanized")

rep(r"""The seven forward maps of
Construction~\ref{con:seven} are implemented as continuous maps on
$X=[0,1]^{d}$ and iterated from compact starting subsets at five""",
    r"""The seven forward maps of
Construction~\ref{con:seven} are implemented as continuous maps on
$X=[-1.5,1.5]^{d}$ and iterated from compact starting subsets at five""",
    "Fix6: battery box")

rep(r"""Across $20$ base configurations (four starting compact subsets
$\times$ five Bregman regularization strengths
$\lambda\in\{0.0,0.1,0.3,0.5,0.7\}$)""",
    r"""Across $20$ base configurations (four starting compact subsets
$\times$ five averaging strengths
$\lambda\in\{0.0,0.1,0.3,0.5,0.7\}$)""",
    "Fix6: titer-base averaging strengths")

rep(r"""$\lambda$: the Bregman regularization and the other six
contractions dominate the single expansion.""",
    r"""$\lambda$: the averaging projection and the other six
contractions dominate the single expansion.""",
    "Fix6: titer-control wording")

rep(r"""\item \emph{Sharpening the contraction bound.} The analytic bound
$\prod_i \Lip(f_i) \leq 0.697$ is sufficient but not tight: the
measured contraction factors of the Bregman-regularized iteration
across the $375$-configuration grid are systematically smaller
(the regularization reorganizes trajectories toward the interior of
$\mathcal K$ rather than merely averaging them). Recovering the
empirical rates analytically is open.""",
    r"""\item \emph{Sharpening the contraction bound.} The analytic bound
$\prod_i \Lip(f_i) \leq 0.697$ is sufficient but not tight: the
measured contraction factors of the Krasnoselskii--Mann-averaged
iteration across the $375$-configuration grid are systematically
smaller (the averaging projection contracts each iterate toward
$\mathcal K$, and the instantiation's iterates are better behaved
than the worst case the bound tracks). Recovering the
empirical rates analytically is open.""",
    "Fix6: open problem 5 KM wording")

rep(r"""Banach contraction of the Bregman-regularized update; the projected
CPTP channel contraction settles the Zeno self-reference resolution.""",
    r"""Banach contraction of the Krasnoselskii--Mann-averaged update; the
projected CPTP channel contraction settles the Zeno self-reference
resolution.""",
    "Fix6: abstract KM gloss")

rep(r"""(iv)~The filtered-colimit construction of RAF sets in
$\Optic(\mathbf{Set})$ is proved componentwise and verified at
scale, and the $\infty$-categorical extension via homotopy type
theory is developed with its proof-sketch status explicitly marked.""",
    r"""(iv)~The filtered-colimit construction of RAF sets is proved at the
Set level with an adapter-level optic statement, and verified at
scale; and the $\infty$-categorical extension via homotopy type
theory is developed with its proof-sketch status explicitly marked.""",
    "Fix2: abstract colimit scope")

rep(r"""\item The filtered-colimit construction of RAF sets in
$\Optic(\mathbf{Set})$, proved componentwise
(Theorem~\ref{thm:filtered-colimits-optic}) and verified at scale
(Proposition~\ref{prop:invlim-extended}).""",
    r"""\item The filtered-colimit construction of RAF sets, proved at the
Set level with the adapter-level optic statement
(Theorem~\ref{thm:filtered-colimits-optic}) and verified at scale
(Proposition~\ref{prop:invlim-extended}).""",
    "Fix2: contribution 6 colimit scope")

rep(r"""Banach contraction
of the Bregman-regularized update for the chosen seven-map
instantiation (Theorem~\ref{thm:unconditional-banach}), and the""",
    r"""Banach contraction
of the Krasnoselskii--Mann-averaged update for the chosen seven-map
instantiation (Theorem~\ref{thm:unconditional-banach}), and the""",
    "Fix6: contribution 5 KM gloss")

open(F, "w").write(src)
print(f"\npart B1b complete: {n_applied} edits (in place)")
