#!/usr/bin/env python3
"""
Patch round D on companion_categorical_v3.tex (live head; frozen lineage
v1/v2 companions + v1/v2/v3 mains untouched):

 D1  Glucose-only Keio re-run closure:
     - pointer sentences in prop:keio-e12 / prop:keio-e15 / prop:keio-e16
     - rem:keio-medium-audit updated (open item -> executed re-run)
     - new prop:keio-glucose-only + rem:keio-invariance
     - pFBA -> FBA (three sites; the solver convention is plain FBA,
       verified by the medium-audit reproduction)
 D2  T7b: new prop:closure-viability (+ proof) + rem:closure-viability
     (closure test = finite-time, feedback-certifying viability-kernel /
     capture-basin probe; Nagumo/tangentiality link to eq:pdi).
 D3  T7c: new prop:poincare-averaging (+ proof) + rem:poincare-averaging
     after rem:phase3-operational (occupation fraction = phase average;
     Poincare-section/averaging reading of the Phase III levels).
 D4  bib: + guckenheimer1983, + sandersverhulst2007 (aubin2011 exists).
"""
import re
import sys

TEX = "companion_categorical_v3.tex"
BIB = "journal_manuscript_refs.bib"

edits_applied = 0


def flex_replace(text, anchor, replacement, count=1, label=""):
    """Whitespace-flexible exact-once replacement (word-level \s+)."""
    global edits_applied
    words = anchor.split()
    pat = re.compile(r"\s+".join(re.escape(w) for w in words))
    matches = pat.findall(text)
    assert len(matches) == count, (
        f"[{label}] expected {count} match(es), found {len(matches)}: "
        f"{anchor[:80]}")
    text = pat.sub(lambda m: replacement, text, count=count)
    edits_applied += count
    print(f"  [{label}] applied ({count})")
    return text


src = open(TEX, encoding="utf-8").read()
n0 = len(src)

# =====================================================================
# D1a: pointer sentence in prop:keio-e12 (after the P@K sentence)
# =====================================================================
src = flex_replace(
    src,
    "P@$200=0.805$ ($3.81\\times$ lift), P@$100=0.680$, "
    "P@$10=0.700$ ($3.31\\times$).",
    "P@$200=0.805$ ($3.81\\times$ lift), P@$100=0.680$,\n"
    "P@$10=0.700$ ($3.31\\times$). The medium-corrected glucose-only\n"
    "re-run of Proposition~\\ref{prop:keio-glucose-only} reproduces this\n"
    "essentiality set exactly (no label changes) and strengthens every\n"
    "rank-level statistic.",
    label="D1a e12-pointer")

# =====================================================================
# D1b: pointer sentence in prop:keio-e15 (after the PEC stratification)
# =====================================================================
src = flex_replace(
    src,
    "high-confidence essentials (Keio $=E$ and PEC $=E$) $n=84$; "
    "low-confidence essentials (Keio $=E$, PEC $=N$) $n=35$.",
    "high-confidence essentials (Keio $=E$\n"
    "and PEC $=E$) $n=84$; low-confidence essentials (Keio $=E$,\n"
    "PEC $=N$) $n=35$. Under the medium-corrected re-run\n"
    "(Proposition~\\ref{prop:keio-glucose-only}) the rank-level\n"
    "association strengthens and the confidence strata are unchanged.",
    label="D1b e15-pointer")

# =====================================================================
# D1c: pointer sentence in prop:keio-e16 (after 'flips sign')
# =====================================================================
src = flex_replace(
    src,
    "the in-silico essentiality fraction moves toward the experimental "
    "fraction; the direct association flips sign.",
    "the in-silico essentiality fraction moves toward the experimental\n"
    "fraction; the direct association flips sign. The flip is itself\n"
    "medium-induced: under the corrected glucose-only medium\n"
    "(Proposition~\\ref{prop:keio-glucose-only}) the same protocol\n"
    "transfers positively, with association strength comparable to the\n"
    "iJO1366 arm.",
    label="D1c e16-pointer")

# =====================================================================
# D1d: rem:keio-medium-audit final sentences -> executed re-run
# =====================================================================
src = flex_replace(
    src,
    "A corrected glucose-only re-run remains an open methodological "
    "item; the deposited results are reported unaltered and flagged "
    "here rather than silently recomputed.",
    "The corrected glucose-only re-run has since been executed with\n"
    "the trehalose exchange closed as the sole change\n"
    "(Proposition~\\ref{prop:keio-glucose-only}): both in-silico\n"
    "essentiality sets are unchanged (zero label changes in either\n"
    "model), every rank-level association strengthens, and the\n"
    "cross-rebuild negative verdict of Proposition~\\ref{prop:keio-e16}\n"
    "does not survive the correction. The deposited results are\n"
    "retained unaltered above as the record of what was originally\n"
    "deposited; the corrected statistics are the ones the studies' own\n"
    "medium declaration intended.",
    label="D1d medium-audit")

# =====================================================================
# D1e: new proposition + remark before sec:network-keio-e14
# =====================================================================
NEWPROP = r"""
\begin{proposition}[Medium-corrected glucose-only re-run]
\label{prop:keio-glucose-only}
Re-executing the three studies with the trehalose exchange closed
(the sole change; wild-type optima $0.98237$ on iJO1366 and
$0.82180$ on iML1515, the canonical glucose-minimal values) leaves
both in-silico essentiality sets unchanged --- $289/1{,}367$ and
$286/1{,}516$, zero label changes in either model --- and
strengthens every rank-level statistic. Transitive arm: Pearson
$r(\log\kappa^{\mathrm{flux}}_V,\Delta b)=+0.603$
($p=2.2\times10^{-136}$), Spearman $+0.592$, partial $r=+0.601$,
bootstrap $95\%$ CI $[0.578,0.631]$; held-out ROC AUC $0.977$,
sensitivity $0.885$, specificity $0.982$, MCC $0.882$, confusion
$(318,6,10,77)$, P@$200=0.915$. Direct arm: Pearson
$r(\log\kappa^{\mathrm{flux}}_V,\mathrm{Keio}\text{-}E)=+0.230$
($p=6.7\times10^{-16}$), Spearman $+0.256$
($p=2.0\times10^{-19}$), ROC AUC $0.738$; held-out ROC AUC
$0.763$, sensitivity $0.846$, specificity $0.607$, MCC $0.283$;
the confidence strata are unchanged ($84$/$35$) with the
high-confidence AUC $0.713$, the model-gap set is unchanged at
$30$, and the medium-mismatch stratum (in-silico essential, Keio
$N$) shrinks from $217$ to $180$ genes. Cross-rebuild arm: Pearson
$+0.376$ ($p=9.6\times10^{-46}$), Spearman $+0.304$
($p=1.0\times10^{-29}$), ROC AUC $0.813$, with the binary matched
set unchanged ($1{,}325$ genes, $114$ essential) and the model-gap
set unchanged at $13$: the non-transfer recorded as the negative
verdict of Proposition~\ref{prop:keio-e16} does not survive the
medium correction.
\end{proposition}

\begin{remark}[Why the labels are invariant but the statistics are not]
\label{rem:keio-invariance}
The label invariance is consistent with the wide separation of the
relative knockout ratio $b_{\mathrm{KO}}/b_{\mathrm{wt}}$ around the
declared $5\%$ line: for every gene the ratio sits near zero or near
one in both media, so the roughly sixteen-fold change in the
wild-type optimum moves no gene across the threshold, in either
reconstruction. The statistic $\kappa^{\mathrm{flux}}_V$, by
contrast, aggregates \emph{absolute} squared flux changes: the
unlimited-trehalose optimum routes large fluxes through pathways
irrelevant to the glucose-minimal phenotype, and removing that
spurious rerouting removes a dilution of the statistic. This is why
every association strengthens without a single essentiality label
changing, and why the cross-rebuild sign flip reverses: the
trehalose fluxes enter the iML1515 knockout solutions differently
than the iJO1366 ones, contaminating the rank comparison itself.
\end{remark}

"""
src = flex_replace(
    src,
    "\\subsection{Benchmark against the structural closure instruments}",
    NEWPROP +
    "\\subsection{Benchmark against the structural closure instruments}",
    label="D1e new-prop")

# =====================================================================
# D1f: pFBA -> FBA (three sites)
# =====================================================================
src = flex_replace(
    src, "computed by pFBA on the deposited model files",
    "computed by flux-balance analysis on the deposited model files",
    label="D1f pFBA-1")
src = flex_replace(
    src, "wild-type pFBA biomass $15.444$;",
    "wild-type FBA biomass\n$15.444$;",
    label="D1f pFBA-2")
src = flex_replace(
    src, "wild-type pFBA biomass $0.926$;",
    "wild-type FBA biomass $0.926$;",
    label="D1f pFBA-3")

# =====================================================================
# D2: T7b — viability-kernel proposition after the non-circularity remark
# =====================================================================
T7B = r"""
\begin{proposition}[Closure test as a finite-time viability probe]
\label{prop:closure-viability}
Let
$V := \{x \in \RR^{M}_{\geq 0} : x_j \geq x_{\mathrm{thresh}}\
\text{for all } m_j \in M_{\mathrm{ess}}\}$
be the viability constraint set determined by the declared threshold,
and write the dynamics of Definition~\ref{def:autopoiesis} in
control form by splitting the repair reactions off the rate law:
$\dot x = N_{\mathrm{fix}} v_{\mathrm{fix}}(x) + N_{\mathrm{rep}} u
- D x + u_{\mathrm{food}}$, with control entries $u_k \in
[0, \bar r_k]$ the repair-reaction rates and $\bar r$ their
pre-knockout values; the \emph{endogenous law} sets $u_k = v_k(x)$.
For $m_j \in M_{\mathrm{ess}}$, let $\Sigma_j$ be the restricted
system with $u_j \equiv 0$ (the knockout).
\begin{enumerate}[label=\textit{(\roman*)},leftmargin=*,itemsep=2pt]
\item If the solution of $\Sigma_j$ under the endogenous law
launched at the pre-knockout steady state $x^*$ remains in $V$ for
all $t \geq 0$ --- $x^*$ lies in the feedback viability kernel of
$V$ for that law --- then step~(iii) of
Definition~\ref{def:autopoiesis} passes at every horizon at which
the trajectory meets the interior of $V$.
\item If steps~(i)--(iii) pass under the autonomous post-knockout
law, then $x^*$ belongs to the horizon-$T$ recovery set
$\{x_0 : x_j(T; x_0) \geq x_{\mathrm{thresh}}\}$ of that law; and if
the post-knockout solution is uniformly persistent
($\liminf_{t \to \infty} x_j(t) > x_{\mathrm{thresh}}$), then its
$\omega$-limit set is contained in $V$ --- the trajectory-level
relaxation of kernel membership appropriate when the perturbation
forces an excursion below the threshold.
\item Step~(v) passes iff, under the restored law, the
post-knockout state is recaptured by the steady state within the
horizon: the restoration flux solves the finite-horizon capture
problem for the target $\{x^*\}$ under the constraint $V$
\citep{aubin2011}.
\end{enumerate}
\end{proposition}

\begin{proof}
(i) Viability under the stationary law means $x(t) \in V$ for all
$t \geq 0$, in particular $x_j(T) \geq x_{\mathrm{thresh}}$, and the
conclusion is the strict form of this inequality at horizons where
the trajectory is interior. (ii) The first clause is the definition
of passing step~(iii); under uniform persistence there exists $T_0$
with $x_j(t) \geq x_{\mathrm{thresh}}$ for all $t \geq T_0$, so
every accumulation point of the solution lies in the closed set
$V$, which is the stated containment. (iii) Step~(v) is the
definition of finite-horizon capture of $x^*$ under the restored
dynamics, restated in the vocabulary of viability theory.
\end{proof}

\begin{remark}[Nagumo tangentiality and the scope of the probe]
\label{rem:closure-viability}
Three comments. First, at the threshold face
$\{x_j = x_{\mathrm{thresh}}\}$ the contingent cone to $V$ is
$\{w : w_j \geq 0\}$, so re-entry through the face requires the
$j$-th velocity component of the recovery dynamics to be
non-negative there --- Nagumo's inward-pointing condition for the
box $V$; at constraint-switching boundaries of the stratified law
the same requirement is enforced by the projected differential
inclusion~\eqref{eq:pdi}, whose Bouligand contingent cone is the
general form of the tangent cone. Second, the protocol is
deliberately stronger than viability-kernel membership in the
existential sense of viability theory (some admissible control
keeps the state in $V$): it fixes the \emph{endogenous} feedback
and forbids exogenous rescue, so a positive verdict certifies that
the system's own control law is a viable one at the probed horizon
--- the property the non-circularity reading of
Definition~\ref{def:autopoiesis} requires. Third, the probe is
single-perturbation and finite-horizon: guaranteed viability under
a \emph{family} of persistent disturbances (the invariance-kernel
problem) is the stronger program-level property, and the pathwise
levels --- the occupation fractions of Phase~II/III
(Definition~\ref{def:autopoiesis-phase3}) --- are the
occupation-measure approximations of that property over the sampled
window, as Proposition~\ref{prop:poincare-averaging} makes precise
for the limit-cycle regime.
\end{remark}

"""
src = flex_replace(
    src,
    "\\begin{definition}[Closure-aware viability curvature]",
    T7B + "\\begin{definition}[Closure-aware viability curvature]",
    label="D2 t7b")

# =====================================================================
# D3: T7c — Poincare/averaging after rem:phase3-operational
# =====================================================================
T7C = r"""
\begin{proposition}[Poincar\'e/averaging content of the pathwise levels]
\label{prop:poincare-averaging}
Suppose the post-knockout trajectory of $m_j$ converges to a
periodic orbit $x^{\mathrm{lc}}$ of period $\tau_c$ (the
limit-cycle recovery regime). Then the occupation fraction of the
pathwise criterion,
\[
  \varphi_T \;=\; \tfrac{1}{T}\int_0^T
  \mathbf{1}\{x_j(t) \geq x_{\mathrm{thresh}}\}\,dt,
\]
converges as $T \to \infty$ to the phase average
$\varphi_\infty = \tau_c^{-1}\int_0^{\tau_c}
\mathbf{1}\{x^{\mathrm{lc}}_j(t) \geq x_{\mathrm{thresh}}\}\,dt$,
and $\varphi_\infty$ is invariant under phase shifts of the orbit:
it is a function of the orbit, not of the initial phase. The
Phase~I endpoint statistic $x_j(T)$, by contrast, samples a single
phase and can fail purely by phase alignment --- the mechanism by
which limit-cycle recoveries fail the endpoint test while their
orbits spend a positive fraction of the window above the threshold
(fractions $0.498$ and $0.853$ in the two benchmark cases,
Table~\ref{tab:network-battery}).
\end{proposition}

\begin{proof}
For a $\tau_c$-periodic input $g(t) = \mathbf{1}\{
x^{\mathrm{lc}}_j(t) \geq x_{\mathrm{thresh}} \}$, the integral
over $[0,T]$ equals $\lfloor T/\tau_c \rfloor \int_0^{\tau_c} g
\,dt + O(1)$, so $\varphi_T \to \tau_c^{-1}\int_0^{\tau_c} g\,dt$;
a phase shift $t \mapsto t + s$ changes the integral over one
period by at most $|s|$ worth of boundary indicator, which is
absorbed into the $O(1)$ remainder and vanishes in the limit.
\end{proof}

\begin{remark}[Classical reading of the Phase~III criterion]
\label{rem:poincare-averaging}
This is the Poincar\'e-section/averaging reading of the pathwise
levels: the occupation fraction is an orbit average, the
finite-window statistic a stroboscopic sample of it, and
transversal-section (Poincar\'e) sampling the phase-unbiased way to
estimate the same quantity
\citep{guckenheimer1983,sandersverhulst2007}. Two consequences.
First, the path reparameterization $\gamma_a \mapsto \gamma_a
\circ \rho$ that item~(3) of
Definition~\ref{def:autopoiesis-phase3} uses to identify
phase-shifted recoveries is the $\infty$-groupoid packaging of
exactly this phase invariance: the classical content of ``limit
cycles are not endpoint failures'' is that the pass statistic
should be a function of the orbit rather than of the sampling
phase, and the occupation fraction is the minimal such statistic.
Second, for bounded recoveries that are not eventually periodic,
$\varphi_T$ converges along subsequences to occupation measures
supported on the $\omega$-limit set, so the pathwise level is the
occupation-measure form of the $\omega$-limit viability containment
of Proposition~\ref{prop:closure-viability}(ii): the three-level
disjunction of Definition~\ref{def:autopoiesis-phase3} is a
finite-window, phase-aware approximation hierarchy for that single
classical property.
\end{remark}

"""
src = flex_replace(
    src,
    "\\subsection{Falsifiable prediction and operationalization}",
    T7C + "\\subsection{Falsifiable prediction and operationalization}",
    label="D3 t7c")

open(TEX, "w", encoding="utf-8").write(src)
print(f"{TEX}: {n0} -> {len(src)} chars, {edits_applied} edits")

# =====================================================================
# D4: bib additions
# =====================================================================
bib = open(BIB, encoding="utf-8").read()
assert "guckenheimer1983" not in bib and "sandersverhulst2007" not in bib
bib += """
@book{guckenheimer1983,
  author    = {J. Guckenheimer and P. Holmes},
  title     = {Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields},
  publisher = {Springer},
  address   = {New York},
  year      = {1983}
}

@book{sandersverhulst2007,
  author    = {J. A. Sanders and F. Verhulst and J. Murdock},
  title     = {Averaging Methods in Nonlinear Dynamical Systems},
  edition   = {2nd},
  publisher = {Springer},
  address   = {New York},
  year      = {2007}
}
"""
open(BIB, "w", encoding="utf-8").write(bib)
print(f"{BIB}: appended guckenheimer1983 + sandersverhulst2007")
print("PATCH D COMPLETE")
