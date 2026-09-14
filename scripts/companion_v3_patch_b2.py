#!/usr/bin/env python3
"""companion v3 part B2: 3rd-wave Fix 5 (Levy-area normalization +
fluctuation language), Fix 7 (AcCoA remark/table consistency +
step-(v) protocol alignment), Fix 8 (envelope domination restricted
to active surrogates), the localized serious items N6/N7/N8, and the
C6 (kappa-unification) / C8 (count-hygiene) readiness actions.
In place on scripts/companion_categorical_v3.tex."""
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


# =====================================================================
# Fix 5(a): X2 normalization in the Ito-expansion lemma.
# =====================================================================
rep(r"""where $X\sim\mathcal N(0,1)$ is the combined linear stochastic
correction and $X_2$ is the L\'evy area, a centered Gaussian with
$\mathrm{Var}(X_2)=1/12$ for unit time.""",
    r"""where $X\sim\mathcal N(0,1)$ is the combined linear stochastic
correction and
$X_2 := \tfrac12\oint_0^1\bigl(W_1\,\mathrm{d}W_2 -
W_2\,\mathrm{d}W_1\bigr)$ is half the planar L\'evy area, a centered
Gaussian with $\mathrm{Var}(X_2)=1/4$ for unit time.""",
    "Fix5: lemma statement X2 = half loop integral, Var = 1/4")

rep(r"""Expanding
$x\,\mathrm{d}y-y\,\mathrm{d}x$ and collecting by powers of
$\sigma$: the $O(1)$ term is
$\tfrac12\oint 2\pi a^{2}(\cos^{2}+\sin^{2})\,\mathrm{d}t=\pi
a^{2}$; the $O(\sigma^{2})$ term is the L\'evy area
$\tfrac{\sigma^{2}}{2}\oint(W_1\,\mathrm{d}W_2-W_2\,\mathrm{d}W_1)
$, of variance $\sigma^{4}/12$ for unit time; and the""",
    r"""Expanding
$x\,\mathrm{d}y-y\,\mathrm{d}x$ and collecting by powers of
$\sigma$: the $O(1)$ term is
$\tfrac12\oint 2\pi a^{2}(\cos^{2}+\sin^{2})\,\mathrm{d}t=\pi
a^{2}$; the $O(\sigma^{2})$ term is the L\'evy area
$\tfrac{\sigma^{2}}{2}\oint(W_1\,\mathrm{d}W_2-W_2\,\mathrm{d}W_1)
$, of variance $\sigma^{4}/4$ for unit time: the loop integral
$L=\oint(W_1\,\mathrm{d}W_2-W_2\,\mathrm{d}W_1)$ equals
$2\int_0^1 W_1\,\mathrm{d}W_2 - W_1(1)W_2(1)$ by It\^o integration
by parts (with
$\mathrm{d}(W_1W_2)=W_1\,\mathrm{d}W_2+W_2\,\mathrm{d}W_1$, the
independent components having zero quadratic covariation), and
$\mathrm{Var}\bigl(\int_0^1 W_1\,\mathrm{d}W_2\bigr)=\tfrac12$ by
the It\^o isometry while
$\mathrm{Cov}\bigl(\int_0^1 W_1\,\mathrm{d}W_2,\,
W_1(1)W_2(1)\bigr)=\tfrac12$ (both sides reduce to
$\int_0^1 t\,\mathrm{d}t$), so
$\mathrm{Var}(L)=4\cdot\tfrac12+1-4\cdot\tfrac12=1$ and the half
area $X_2=L/2$ has variance $1/4$. (The value $1/12$ is the
Brownian-bridge time-integral variance, not the
free-Brownian-motion L\'evy-area variance.); and the""",
    "Fix5: lemma proof variance derivation (Var(L)=1, half-area 1/4)")

# Fix 5(b): sub-leading scale in the 3/2 theorem proof.
rep(r"""Substituting the diffusion ansatz $\sigma^{2}=\nu a$ gives
$\tfrac{\sqrt5}{2}\sqrt{\nu a}\,a=\tfrac{\sqrt{5\nu}}{2}\,
a^{3/2}$, which is~\eqref{eq:cfat-formula}. The quadratic
L\'evy-area correction scales as
$\sigma^{2}/(2\sqrt{12})\sim a$, an analytic integer power; in the""",
    r"""Substituting the diffusion ansatz $\sigma^{2}=\nu a$ gives
$\tfrac{\sqrt5}{2}\sqrt{\nu a}\,a=\tfrac{\sqrt{5\nu}}{2}\,
a^{3/2}$, which is~\eqref{eq:cfat-formula}. The quadratic
L\'evy-area correction has standard deviation
$\sigma^{2}/4\sim\nu a/4$, an analytic integer power; in the""",
    "Fix5: theorem proof sub-leading scale sigma^2/4")

# Fix 5(b): the numerical remark reports c2.
rep(r"""The single-exponent coefficient is
$\widehat C=0.357$ and the two-term fit
$\mathrm{std}(\delta H)=c_1a^{3/2}+c_2a$ gives $c_1=0.349$, both
within $1.5\%$ of the exact value
$\sqrt{5\nu}/2=\sqrt{0.5}/2=0.3536$ of
Theorem~\ref{thm:levy-3half}: the exact variance computation of
Lemma~\ref{lem:ito-expand} --- the It\^o integral, the drift
integral, and their cross-covariance --- accounts for the full
coefficient, with no unexplained remainder.""",
    r"""The
single-exponent coefficient is
$\widehat C=0.357$ and the two-term fit
$\mathrm{std}(\delta H)=c_1a^{3/2}+c_2a$ gives $c_1=0.349$ and
$c_2=0.0081$, the leading coefficient within $1.5\%$ of the exact
value $\sqrt{5\nu}/2=\sqrt{0.5}/2=0.3536$ of
Theorem~\ref{thm:levy-3half}: the exact variance computation of
Lemma~\ref{lem:ito-expand} --- the It\^o integral, the drift
integral, and their cross-covariance --- accounts for the full
coefficient, with no unexplained remainder. The fitted $c_2$ is
reported so the sub-leading normalization is testable: the
analytic sub-leading fluctuation scale is $\sigma^{2}/4=\nu a/4$
(coefficient $\nu/4=0.025$ at $\nu=0.1$), and the fitted additive
coefficient $0.0081$ sits below it because the two-term additive
form is a proxy for the root-sum-of-squares of the leading and
sub-leading contributions (whose exact two-term fit over the same
grid gives $c_2=0.0020$); the sign and order of magnitude are
consistent with the corrected normalization.""",
    "Fix5: rem:levy-numerical reports c2 with the proxy caveat")

# Fix 5(b): figure caption term.
rep(r"""The log--log fit gives
$\widehat\beta=1.479$ (theory $3/2$) with $R^{2}=0.9999$; the
small-$a$ downward deviation of the single-exponent fit is the
linear L\'evy-area term.""",
    r"""The log--log fit gives
$\widehat\beta=1.479$ (theory $3/2$) with $R^{2}=0.9999$; the
small-$a$ downward deviation of the single-exponent fit is the
linear sub-leading L\'evy-area fluctuation scale.""",
    "Fix5: figure caption wording (curve label regenerated separately)")

# =====================================================================
# Fix 5(c) + N2 + N12 + N15: Claims C/D in fluctuation language.
# =====================================================================
rep(r"""\item[\textbf{C.}] (Holonomy-area scaling) $H(a) = c_1 a^2 + c_2
a^{3/2}$ with $c_1\sim\pi$, $c_2\sim C_{\mathrm{fat}}\neq 0$, $R^2\geq
0.95$.""",
    r"""\item[\textbf{C.}] (Holonomy-area scaling) The holonomy increment
of a loop of amplitude $a$ has mean $\pi a^{2}+O(\sigma^{3})$ and,
under the amplitude-scaled exposure $\sigma^{2}=\nu a$, leading
fluctuation scale $C_{\mathrm{fat}}\,a^{3/2}$ with
$C_{\mathrm{fat}}=\sqrt{5\nu}/2$
(Theorem~\ref{thm:levy-3half}); the operational two-term law
$H(a)=c_1a^{2}+c_2a^{3/2}$ ($c_1\sim\pi$, $c_2$ the calibrated
operating value of $C_{\mathrm{fat}}$, $R^{2}\geq 0.95$) treats the
fluctuation scale as a deterministic per-loop correction under the
envelope convention of Remark~\ref{rem:fatigue-convention}.""",
    "Fix5c/N2: Claim C in fluctuation language")

rep(r"""\item[\textbf{D.}] (Repeated-loop fatigue) Two-sided bound: the
\emph{conservative sufficient safety condition} $\sum_{k=1}^{K}(a_k\,
(\kk)_k + C_{\mathrm{fat}}\,a_k^{3/2} + \eta_k) < 1$ guarantees survival
through $K$ loops, and the \emph{failure condition}
$\sum_{k=1}^{K}(a_k\,\kk(a_k) + C_{\mathrm{fat}}\,a_k^{3/2} + \eta_k) > 1$
predicts fatigue failure; $V_{\max,K}=\prod_k(1-F_k)<e^{-1}$ at
$K_{\mathrm{obs}}$; relative error $<15\%$.""",
    r"""\item[\textbf{D.}] (Repeated-loop fatigue) Under the same
convention, the per-loop fractional erosion is
$F_k = a_k\,\kk(a_k) + C_{\mathrm{fat}}\,a_k^{3/2} + \eta_k$:
the \emph{conservative sufficient safety condition}
$\sum_{k=1}^{K}(a_k\,\kk(a_k) + C_{\mathrm{fat}}\,a_k^{3/2}) < 1$
guarantees survival through $K$ loops, and the \emph{failure
condition}
$\sum_{k=1}^{K}(a_k\,\kk(a_k) + C_{\mathrm{fat}}\,a_k^{3/2} + \eta_k) > 1$
predicts fatigue failure; $V_{\max,K}=\prod_k(1-F_k)<e^{-1}$ at
$K_{\mathrm{obs}}$; relative error $<15\%$. In fluctation form the
cumulative sum has mean $\sum_k a_k\,\kk(a_k)$ and the
$C_{\mathrm{fat}}$ term contributes a standard deviation
$\bigl(\sum_k (C_{\mathrm{fat}}\,a_k^{3/2})^{2}\bigr)^{1/2}$
(Remark~\ref{rem:fatigue-convention}).""",
    "Fix5c/N2/N15: Claim D in fluctuation language")

# The envelope-convention remark, placed after the hierarchy's
# cumulative paragraph.
rep(r"""The hierarchy is cumulative: failure at level $k$ renders the
subsequent levels operationally meaningless but does not refute the
underlying categorical construction (Theorem~\ref{thm:composition}).""",
    r"""The hierarchy is cumulative: failure at level $k$ renders the
subsequent levels operationally meaningless but does not refute the
underlying categorical construction (Theorem~\ref{thm:composition}).

\begin{remark}[Fluctuation status of the fatigue term]
\label{rem:fatigue-convention}
The derivation of Theorem~\ref{thm:levy-3half} establishes
$C_{\mathrm{fat}}\,a^{3/2}$ as the standard deviation of the leading
stochastic correction to the holonomy: the per-loop increment has
mean $\pi a^{2}+O(\sigma^{3})$, and its $a^{3/2}$ term is a
fluctuation scale, not a drift. Claims~C and~D, the $n=3$/$n=4$
operational batteries, and the heavy-tail stress test therefore
adopt a declared \emph{envelope convention}: the fluctuation scale
enters the fatigue increment as a deterministic per-loop term (the
conservative upper-envelope reading), so that the two-term law and
the failure conditions remain directly testable against the
deposited simulations. Under the pure fluctuation reading the
failure condition would instead read
$\sum_k a_k\kk(a_k) + z\,\bigl(\sum_k
(C_{\mathrm{fat}}\,a_k^{3/2})^{2}\bigr)^{1/2} > 1$ at confidence
$z$; both readings are stated, and the operational artifacts
implement the envelope one. The constant's operating value
($c_2=0.0500$, i.e.\ $C_{\mathrm{fat}}$ at $\nu=0.002$) is a
calibration of the exposure parameter $\nu$ --- the derivation's
Monte Carlo uses $\nu=0.1$, and the $n=4$ battery plants the
calibrated value in the synthetic data and recovers it within
$5\%$ (a calibration-recovery check; see the note after
Table~\ref{tab:n4}).
\end{remark}""",
    "Fix5c/N12: envelope-convention remark after the hierarchy")

# N12: the calibration note after tab:n4 (index-based insertion:
# immune to bracket/spacing drift around the figure environment).
idx = src.find("claims_ae_n4_nonabelian.png")
assert idx > 0, "figure not found"
fig_start = src.rfind("\\begin{figure}", 0, idx)
assert fig_start > 0, "figure env not found"
note = """
\\noindent\\emph{Calibration status of the Claim-C constants.} The
value $c_1=\\pi$ is derived (the holonomy mean of the prototype
connection); the value $c_2=0.0500$ is the calibrated operating
value of $C_{\\mathrm{fat}}=\\sqrt{5\\nu}/2$ at $\\nu=0.002$
(Remark~\\ref{rem:fatigue-convention}) --- a calibration of the
exposure parameter, not a derived constant (the derivation's
Monte Carlo of Section~\\ref{sec:verdict-levy} uses $\\nu=0.1$).
The $n=4$ battery's Claim-C arm plants the calibrated value in
the synthetic scaling data and recovers it within $5\\%$
($0.0526$ against $0.0500$): a calibration-recovery check, not an
independent derivation of the constant.

"""
src = src[:fig_start] + note + src[fig_start:]
n_applied += 1
print("ok   [N12: calibration-recovery note inserted before fig:n4]")

# Stress-test proof wording.
rep(r"""Direct Monte-Carlo computation ($200$ seeds per cell; deposited
artifacts). The cumulative fatigue sum $\sum_k F_k$ is dominated
by the deterministic mean $\mu_F=a\,\kk(a)+C_{\mathrm{fat}}\,
a^{3/2}=0.0352$ at the operating point, with $\kk(a)=a^{2}=0.09$
and the calibrated $C_{\mathrm{fat}}=0.05$ (the coefficient is
derived in Theorem~\ref{thm:levy-3half} below); the heavy-tail""",
    r"""Direct Monte-Carlo computation ($200$ seeds per cell; deposited
artifacts). The cumulative fatigue sum $\sum_k F_k$ is dominated by
its per-loop envelope scale $\mu_F=a\,\kk(a)+C_{\mathrm{fat}}\,
a^{3/2}=0.0352$ at the operating point --- the envelope convention
of Remark~\ref{rem:fatigue-convention} (the derived reading of the
$C_{\mathrm{fat}}$ term is a standard deviation) --- with
$\kk(a)=a^{2}=0.09$ and the calibrated $C_{\mathrm{fat}}=0.05$
(the term's form and exponent are derived in
Theorem~\ref{thm:levy-3half} below; the operating value is the
$\nu=0.002$ calibration); the heavy-tail""",
    "Fix5c/N2: stress-test proof envelope wording")

# =====================================================================
# Fix 7: AcCoA remark, Prediction-3, phase3 attachment, battery
# passage, step-(v) protocol alignment.
# =====================================================================
rep(r"""Under the univalence-identified fixed point
(Corollary~\ref{cor:hott-fixedpoint}), the AcCoA ``failure'' is
reinterpreted as a higher-categorical recovery: AcCoA's
homotopy-fixed-point in the $\infty$-categorical sense is the
contractible space of recovery oscillations, canonically a term in
$\mathcal{U}$; the endpoint-only closure-test verdict undercounts by
one; the pathwise + univalence-corrected verdict is $42/42 = 100\%$
causally internal, recovering the full autopoiesis closure.""",
    r"""Under the univalence-identified fixed point
(Corollary~\ref{cor:hott-fixedpoint}), the limit-cycle reading
would reinterpret such a ``failure'' as a higher-categorical
recovery (the contractible space of recovery oscillations). The
operationalized Phase~III criterion, however, does \emph{not}
convert Network~G's AcCoA: Table~\ref{tab:network-battery} records
$41/42$ in both phases for Network~G, and the deposited pathwise
record for the AcCoA family (at Network~J, the only one on
deposit) spends a fraction $0.275$ of the window above the
viability threshold with mean $3.59$ and fails the contractibility
check --- an oscillation mostly below threshold, not a recovery.
The Phase~III conversions of the battery occur elsewhere: at
Network~H (the ALA limit cycle, pathwise fraction $0.498$, mean
$49.8$; $43/44\to44/44$) and at Network~I (the FBP limit cycle,
pathwise fraction $0.853$, mean $47.4$; $45/46\to46/46$). AcCoA is
repaired at the endpoint level only by the designed ACS1/2 step
(Network~K, $52/52$ at Phase~I). The higher-categorical reading
applies to the converted limit-cycle components, not to
Network~G's AcCoA.""",
    "Fix7/N3: AcCoA remark aligned with the table and artifacts")

rep(r"""\item Prediction~3 is verified in the AcCoA limit-cycle regime of
Network~G (Remark~\ref{rem:netG-accola-cycle}), where the
endpoint-only closure-test verdict is HOMEOSTATIC but the pathwise
recovery is contractible (oscillations are homotopy-equivalent through
recoveries, by the pathwise viability tube of Remark~\ref{rem:pathwise}).""",
    r"""\item Prediction~3 is verified in the ALA limit-cycle regime of
Network~H and the FBP limit-cycle regime of Network~I
(Table~\ref{tab:network-battery}): the endpoint-only closure-test
verdict is HOMEOSTATIC but the pathwise recovery passes (fractions
$0.498$ and $0.853$ above threshold) with the contractibility check
passing, converting both to Phase~III recoveries --- oscillations
homotopy-equivalent through recoveries, by the pathwise viability
tube of Remark~\ref{rem:pathwise}. (The AcCoA limit cycle of
Network~G, Remark~\ref{rem:netG-accola-cycle}, is the case the
operationalized criterion does \emph{not} convert.)""",
    "Fix7/N3: Prediction-3 verified at H (ALA) and I (FBP)")

rep(r"""cycle (as for AcCoA in the Network~G benchmark, Remark~\ref{rem:netG-accola-cycle}, and
for ALA in the Network~H benchmark).""",
    r"""cycle (as for ALA in the Network~H benchmark and FBP in the
Network~I benchmark, Table~\ref{tab:network-battery}; the AcCoA
limit cycle of the Network~G benchmark,
Remark~\ref{rem:netG-accola-cycle}, is the case the operationalized
criterion does \emph{not} convert).""",
    "Fix7/N3: phase3 intro metabolite attachment corrected")

rep(r"""The designed progression then adds, at
each step, one redundant isozyme pair with a stated
cascade-breaking role; the monotone verdict sequence is
Table~\ref{tab:network-battery}. At the final step the Phase~I
endpoint-only verdict reaches $52/52$ and the divergence between
the Phase~I endpoint-only and the pathwise Phase~III verdicts
disappears --- the two last-remaining Phase~I ``failures'' are
limit-cycle oscillations that the pathwise criterion of
Definition~\ref{def:autopoiesis-phase3} already counts as
recoveries (Sections~\ref{sec:phase3}--\ref{sec:verdict-cptp}).""",
    r"""The designed progression then adds, at
each step, one redundant isozyme pair with a stated
cascade-breaking role; the monotone verdict sequence is
Table~\ref{tab:network-battery}. The Phase~I endpoint-only verdict
reaches $52/52$ only at the final step, whose ACS1/2 route repairs
the AcCoA failure that persists through the G--J segment; along
the progression, the pathwise Phase~III criterion converts exactly
the two limit-cycle oscillation failures --- ALA at H
($43/44\to44/44$) and FBP at I ($45/46\to46/46$) --- while the
AcCoA failure (pathwise fraction $0.275$, contractibility FAIL)
is not converted until the designed repair
(Sections~\ref{sec:phase3} and~\ref{sec:verdict-cptp}).""",
    "Fix7/N3: battery passage corrected (conversions at H and I)")

# Step-(v): protocol alignment (amend arm).
rep(r"""threshold. The component
is \emph{causally internal} iff the knockout destroys it and the
restoration recovers it; the system is autopoietic iff every
essential component is causally internal.""",
    r"""threshold. The component
is \emph{causally internal} iff the knockout destroys it and the
restoration recovers it; the system is autopoietic iff every
essential component is causally internal.

The operational protocol implements steps~(i)--(iv) of
Definition~\ref{def:autopoiesis} plus collapse--reversal; the
restoration control of step~(v) --- the return of all concentrations
to the reference state $x^{*}$ within the declared window --- is
\emph{not} part of the recorded verdicts, and the definition is
thereby aligned with the protocol by declaration: the verdicts
below certify the weakened, implemented criterion. The overshoot
rows of Table~\ref{tab:netA} show what the omitted control would
catch: rows $c$ and $f$ recover to $3.84$ and $443.8$ against
baselines $0.45$ and $2.65$ ($8.5\times$ and $167\times$
overshoot), and row $g$ recovers to $164.2$ against $84.4$
($1.9\times$) --- recoveries above the viability threshold, not
restorations of the reference state.""",
    "Fix7/N4: step-(v) protocol alignment + overshoot disclosure")

# =====================================================================
# Fix 8: envelope domination restricted to active surrogates.
# =====================================================================
rep(r"""\item[(e)] The envelope curvature
\begin{equation}\label{eq:kappa-alg}
  \kk^{\mathrm{alg}} \;:=\;
  \tfrac{1}{V_{\max}}\, \sup_{a \in (0, a_\star]}\,
  \sup_{\text{unit bivector } \hat\omega}\,
  \bigl[\,E'(x; F(u, v))\,\bigr]_+
\end{equation}
is effectively approximable --- on each compact parameter box the
supremum in~\eqref{eq:smooth-envelope} reduces, by continuity on
the compact range, to a finite maximization over an
$\varepsilon$-net with two-sided error control --- and it dominates
every smooth surrogate curvature:
\[
  \kk^{\mathrm{surrogate}} \;\leq\; \kk^{\mathrm{alg}}.
\]
\end{enumerate}
\end{theorem}""",
    r"""\item[(e1)] For every finite subfamily and every $x$, the
directional derivative of the envelope is the max over the
\emph{active} surrogates,
$E'(x; v) = \max_{q \in A(x)} r_q'(x; v)$, where $A(x)$ is the
argmax (the active set); consequently the Clarke identification of
item~(c) is recovered, and $E'(x; v) \geq r_{q^*}'(x; v)$ for
every \emph{maximizer} $q^{*} \in A(x)$.
\item[(e2)] The envelope curvature
\begin{equation}\label{eq:kappa-alg}
  \kk^{\mathrm{alg}} \;:=\;
  \tfrac{1}{V_{\max}}\,
  \sup_{\text{unit bivector } \hat\omega}\,
  \bigl[\,E'(x; F(u, v))\,\bigr]_+
\end{equation}
is effectively approximable --- on each compact parameter box the
supremum in~\eqref{eq:smooth-envelope} reduces, by continuity on
the compact range, to a finite maximization over an
$\varepsilon$-net with two-sided error control --- and it
dominates the curvature of every \emph{active} surrogate:
$r_{q^*}^{\mathrm{surrogate}} \leq \kk^{\mathrm{alg}}$ for every
maximizer $q^{*}$. Domination over \emph{non-active} surrogates is
false in general
($E=\max(0,g)$ with $g(x)=x$ at $x=-1$: $E'(\cdot;+1)=0 <
g'=1$); the comparison of $\kk^{\mathrm{alg}}$ with the
ratio-form $\kappa_\alpha$ of Definition~\ref{def:kv} --- the
discretization bridge --- is therefore recorded as an open
problem (Section~\ref{sec:future}), not claimed as a theorem.
\end{enumerate}
\end{theorem}""",
    "Fix8/F6: item (e) split into (e1) active-set identity + (e2) restricted domination")

rep(r"""(e) Effective approximability: by
continuity of $q \mapsto r_q(x)$ on the compact range, a finite
$\varepsilon$-net of the range yields upper and lower approximations
of $E(x)$ within $\varepsilon$, so $E$ is computable in the strong
two-sided sense on each box; the Clarke derivatives are obtained
from finite-subfamily computations on refining covers, and the
suprema over the compact ranges of $a$ and $\hat\omega$ in
\eqref{eq:kappa-alg} preserve effective approximability. Domination:
$E \ge r_q$ pointwise for every $q$ implies $E'(x; v) \ge
r_q'(x; v)$ for every $q$ and $v$ (at the $C^2$ points of $r_q$ the
classical derivative agrees with the Clarke derivative, and the
sup-function's Clarke derivative dominates the active members'),
hence $[E'(x; v)]_+ \ge [r_q'(x; v)]_+$, and the sup over
$(a, \hat\omega)$ gives
$\kk^{\mathrm{alg}} \ge \kappa^{\mathrm{surrogate}}_q$ for every $q$.""",
    r"""(e1) At a singleton argmax this is Danskin's conclusion (item~(b));
for a finite active set $A(x)$, the directional derivative of a
finite max is the max over the active members'
directional derivatives, which gives $E'(x;v)=\max_{q\in A(x)}
r_q'(x;v)$ and the stated maximizer domination. (e2) Effective
approximability: by
continuity of $q \mapsto r_q(x)$ on the compact range, a finite
$\varepsilon$-net of the range yields upper and lower approximations
of $E(x)$ within $\varepsilon$, so $E$ is computable in the strong
two-sided sense on each box; the Clarke derivatives are obtained
from finite-subfamily computations on refining covers, and the
supremum over the compact range of $\hat\omega$ in
\eqref{eq:kappa-alg} preserves effective approximability.
Restricted domination: $E \ge r_{q^*}$ pointwise for a maximizer
$q^{*} \in A(x)$ implies $E'(x; v) \ge r_{q^*}'(x; v)$ for every
$v$ (at the $C^2$ points of $r_{q^*}$ the classical derivative
agrees with the Clarke derivative, and the sup-function's Clarke
derivative dominates the active members'), hence
$[E'(x; v)]_+ \geq [r_{q^*}'(x; v)]_+$, and the sup over
$\hat\omega$ gives
$\kk^{\mathrm{alg}} \geq \kappa^{\mathrm{surrogate}}_{q^*}$ for
every maximizer $q^{*}$. For non-active $q$ the implication fails
(the two-line counterexample of item~(e2)); the ratio-form
comparison is open.""",
    "Fix8/F6: proof (e) restricted to active surrogates")

# def:kv discretization remark (C2 companion side).
rep(r"""The
instantiation~\eqref{eq:halpha} is one admissible choice: any $C^2$
viability function with the stated positivity works, and the
measure-theoretic discretization used in the application paper
\citep{zai2026measure} replaces the $2$-form $F$ by an atomic
crease measure.""",
    r"""The
instantiation~\eqref{eq:halpha} is one admissible choice: any $C^2$
viability function with the stated positivity works. The
application paper \citep{zai2026measure} realizes the
measure-theoretic \emph{analogue} of this object: its atomic crease
measure stands in for the curvature $2$-form and its value--flux
coupling supplies analogue survival covectors, with the per-event
mass corresponding, at active atoms, to the positive part of the
margin change at the crossed facet normalized by the local margin
--- a stated correspondence at active atoms, not a proved
domination; the ratio-form comparison is recorded as open
(Section~\ref{sec:future}).""",
    "Fix8/C2: def:kv discretization remark as active-atom correspondence")

# F20 clause: the envelope identity is a definition-vs-implementation check.
rep(r"""(a) the
envelope identity $E(x) = \sup_q r_q(x)$ holds pointwise, maximum
error $0.0$;""",
    r"""(a) the
envelope identity $E(x) = \sup_q r_q(x)$ holds pointwise, maximum
error $0.0$ --- the definition checked against its
implementation, not an independent test;""",
    "F20: envelope-numeric clause")

# Open problem: add the ratio-form domination item.
rep(r"""\item \emph{Operational instantiations of $\kk$.}""",
    r"""\item \emph{The ratio-form domination (discretization bridge).}
The envelope curvature $\kk^{\mathrm{alg}}$ of
Theorem~\ref{thm:smooth-envelope}(e2) is a raw directional
derivative of the envelope; Definition~\ref{def:kv} defines the
ratio form $\kappa_\alpha = [-D h_\alpha(F(u,v))]^{+}/h_\alpha$.
Establishing (or refuting) a domination or identity between the
two --- the precise discretization correspondence behind the
active-atom bridge stated in Definition~\ref{def:kv} and in the
application paper \citep{zai2026measure} --- is open.
\item \emph{Operational instantiations of $\kk$.}""",
    "Fix8: open problem (ratio-form domination / bridge)")

# =====================================================================
# N7: geometric-phase sign.
# =====================================================================
rep(r"""\item the holonomy of the model connection around $\gamma_a$ is
\begin{equation}\label{eq:kappa-radial}
  \mathrm{Hol}(\gamma_a) \;=\; \oint_{\gamma_a} A \;=\;
  \pi\;\frac{\overline{\delta V}(a)}{V_{\max}},
\end{equation}
which in the quadratic-deficit case
$\overline{\delta V}(a) = V_{\max}\,a^{2}/r_\star^{2}$ reduces to
$\pi a^{2}/r_\star^{2}$ --- with the prototype normalization
$V_{\max} = r_\star = 1$, the loop area $\pi a^{2}$, the
holonomy-area law of Claim~B;""",
    r"""\item the holonomy of the model connection around $\gamma_a$ is
\begin{equation}\label{eq:kappa-radial}
  \mathrm{Hol}(\gamma_a) \;=\; \oint_{\gamma_a} A \;=\;
  \pi\,\frac{V(a)-V_{\max}}{V_{\max}}
  \;=\; -\,\pi\;\frac{\overline{\delta V}(a)}{V_{\max}},
\end{equation}
a \emph{signed} quantity (the connection contains $V-V_{\max}$, a
deficit); the holonomy \emph{magnitude} is
$|\mathrm{Hol}(\gamma_a)| = \pi\,\overline{\delta V}(a)/V_{\max}$,
which in the quadratic-deficit case
$\overline{\delta V}(a) = V_{\max}\,a^{2}/r_\star^{2}$ reduces to
$\pi a^{2}/r_\star^{2}$ --- with the prototype normalization
$V_{\max} = r_\star = 1$, the loop area $\pi a^{2}$, the
holonomy-area law of Claim~B (which is stated for the magnitude);""",
    "N7: geometric-phase corollary signed display")

rep(r"""(ii) On the circle of radius $a$ the deficit
$V_{\max} - V \circ \gamma_a = \overline{\delta V}(a)$ is constant,
so $\oint_{\gamma_a} A = \frac{\overline{\delta V}(a)}{2V_{\max}}
\oint \mathrm{d}\vartheta = \pi\,\overline{\delta V}(a)/V_{\max}$,
and by Stokes the same value is the flux of the curvature form""",
    r"""(ii) On the circle of radius $a$ the deficit
$V_{\max} - V \circ \gamma_a = \overline{\delta V}(a)$ is constant,
so $\oint_{\gamma_a} A = \frac{V(a)-V_{\max}}{2V_{\max}}
\oint \mathrm{d}\vartheta =
-\pi\,\overline{\delta V}(a)/V_{\max}$, of magnitude
$\pi\,\overline{\delta V}(a)/V_{\max}$,
and by Stokes the same magnitude is the flux of the curvature form""",
    "N7: geometric-phase proof signed")

# =====================================================================
# N8: Noether-current identity.
# =====================================================================
rep(r"""\begin{equation}\label{eq:noether-current}
  J_\xi(q, \dot q) \;=\; g_\phi(q)(\dot q, \xi(q)) \;=\; \langle \nabla \phi(q), \xi(q) \rangle \cdot \dot q_{\mathrm{dual}}
\end{equation}
is conserved along Euler--Lagrange trajectories of $S$: $\frac{d}{dt}
J_\xi(q(t), \dot q(t)) = 0$ on-shell.""",
    r"""\begin{equation}\label{eq:noether-current}
  J_\xi(q, \dot q) \;=\; g_\phi(q)(\dot q, \xi(q)) \;=\;
  \bigl\langle \nabla^2\phi(q)\,\dot q,\; \xi(q)\bigr\rangle
  \;=\; \bigl\langle \dot q^{\mathrm{dual}},\, \xi(q)\bigr\rangle
\end{equation}
is conserved along Euler--Lagrange trajectories of $S$: $\frac{d}{dt}
J_\xi(q(t), \dot q(t)) = 0$ on-shell. Here
$\dot q^{\mathrm{dual}} := \nabla^2\phi(q)\,\dot q$ is the
Hessian-dual velocity --- the tangent-vector instance of the Bregman
dual coordinate of Definition~\ref{def:bregman}.""",
    "N8: Noether-current display via the Hessian-dual velocity")

rep(r"""the one-parameter symmetry yields the conserved momentum
$J_\xi(q, \dot q) = \partial L / \partial \dot q \cdot \xi(q) =
g_\phi(q)(\dot q, \xi(q))$. The dual-coordinate form follows by
identifying $\partial L / \partial \dot q = \nabla \phi(q) \cdot \dot
q_{\mathrm{dual}}$ via the dual-coordinate structure of Bregman
divergences (Definition~\ref{def:bregman}).""",
    r"""the one-parameter symmetry yields the conserved momentum
$J_\xi(q, \dot q) = \partial L / \partial \dot q \cdot \xi(q) =
g_\phi(q)(\dot q, \xi(q))$. The dual-coordinate form follows from
$\partial L/\partial\dot q = g_\phi(q)\,\dot q =
\nabla^2\phi(q)\,\dot q = \dot q^{\mathrm{dual}}$ (the Hessian-dual
velocity, the tangent-vector instance of the Bregman dual
coordinate of Definition~\ref{def:bregman}).""",
    "N8: Noether proof dual-coordinate step")

rep(r"""preserves the Hessian metric $g_\phi = \nabla^2 \phi$ (since
$\nabla^2(\phi \circ g_t) = \nabla^2 \phi$ on the affine transformation
$g_t$ by the chain rule, and $\nabla^2 \ell_t = 0$). Therefore the""",
    r"""preserves the Hessian metric $g_\phi = \nabla^2 \phi$ (the affine
map $g_t$ has vanishing second derivative, so
$\nabla^2(\phi \circ g_t) = (\nabla^2\phi)\circ g_t = \nabla^2\phi$,
and $\nabla^2 \ell_t = 0$). Therefore the""",
    "N8: affine-Bregman corollary justification")

# =====================================================================
# N6: homotopy product vs pullback.
# =====================================================================
rep(r"""optic composition, with the residual becoming the
homotopy product and the Banach fixed-point becoming a contractible""",
    r"""optic composition, with the residual becoming the homotopy
pullback of the residuals over the actions (the homotopy product
when the actions are trivial) and the Banach fixed-point becoming a
contractible""",
    "N6: HoTT intro residual wording")

rep(r"""(ii) the residual must be reinterpreted
as a homotopy product, which requires presentability of the ambient""",
    r"""(ii) the residual must be reinterpreted
as a homotopy pullback over the actions (reducing to the homotopy
product for trivial actions), which requires presentability of the ambient""",
    "N6: HoTT intro (ii) wording")

rep(r"""The residual of $T$ is the homotopy
product
\[
\mathrm{Res}_T \;=\; {}^{\mathrm{h}}\!\prod\nolimits_{i=1}^{7}\,\mathrm{Res}_i
\quad \text{in } \mathcal{C}_\infty,
\]
which exists by presentability of $\mathcal{C}_\infty$""",
    r"""The residual of $T$ is the iterated homotopy pullback of the
residuals over the actions --- the fiber-product form computed in
the proof sketch and in the concrete verification of
Remark~\ref{rem:hott-holim} --- which reduces to the homotopy
product
\[
\mathrm{Res}_T \;=\; {}^{\mathrm{h}}\!\prod\nolimits_{i=1}^{7}\,\mathrm{Res}_i
\quad \text{in } \mathcal{C}_\infty
\]
when the actions are trivial; both exist by presentability of
$\mathcal{C}_\infty$""",
    "N6: hott-composition theorem residual statement")

rep(r"""\item \emph{Higher-order probability}: the residual
$\mathrm{Res}_T = {}^{\mathrm{h}}\!\prod_i \mathrm{Res}_i$ is a homotopy product, which
under univalence is a dependent sum type""",
    r"""\item \emph{Higher-order probability}: the residual
$\mathrm{Res}_T$ is the iterated homotopy pullback of the
residuals over the actions (the homotopy product
${}^{\mathrm{h}}\!\prod_i \mathrm{Res}_i$ for trivial actions), which
under univalence is a dependent sum type""",
    "N6: implications bullet wording")

# =====================================================================
# C6: the kappa-unification remark.
# =====================================================================
rep(r"""The hierarchy is cumulative: failure at level $k$ renders the
subsequent levels operationally meaningless but does not refute the
underlying categorical construction (Theorem~\ref{thm:composition}).

\begin{remark}[Fluctuation status of the fatigue term]""",
    r"""The hierarchy is cumulative: failure at level $k$ renders the
subsequent levels operationally meaningless but does not refute the
underlying categorical construction (Theorem~\ref{thm:composition}).

\begin{remark}[Three objects, one family]
\label{rem:kappa-family}
Three objects appear under the $\kappa$ symbol family in this paper:
the pointwise geometric curvature $\kk(\theta,x)$ of
Definition~\ref{def:kv}; the loop-amplitude functional $\kappa(a)$
(the prototype law $\kappa(a)=a^{2}$ of the radially symmetric
regime); and the loop-averaged viability depth $D_V(a)$ of
Definition~\ref{def:kappa-depth}. They are one object at different
resolutions --- the pointwise curvature, its trajectory functional,
and its loop-averaged statistic --- mirroring the resolution of the
same conflation in the application paper \citep{zai2026measure},
whose Discussion identifies the geometric, flux-statistical, and
time-course sensitivity objects as one measure at different
resolutions. The empirical sections use $\kappa(a)$ throughout;
every such use is the prototype instantiation of
Definition~\ref{def:kv} under radial symmetry
(Corollary~\ref{cor:kappa-geometric-phase}).
\end{remark}

\begin{remark}[Fluctuation status of the fatigue term]""",
    "C6: kappa-unification remark added")

open(F, "w").write(src)
print(f"\npart B2 complete: {n_applied} edits (in place)")
