#!/usr/bin/env python3
"""journal_manuscript_v3.tex -> journal_manuscript_v4.tex.

3rd-wave application-paper edits: (C2) soften the discretization-bridge
sentence in the categorical subsection; (APP-1) the generic-weights
uniqueness step for Lemma lex; (APP-2) the semiconvexity-law
contradiction; (APP-3) conj:valueflux label -> cor:valueflux and drop
"corrected form"; (C5) the regime-delineation sentence; (C1) the
delegation-status qualifiers (two sites); (APP-5) selection-rule
count harmonization; (C9/APP-4) figure directory renamed
deepseek_bridge -> association_robustness.

Frozen lineage untouched: reads scripts/journal_manuscript_v3.tex,
writes scripts/journal_manuscript_v4.tex (new file)."""
import sys

SRC = "scripts/journal_manuscript_v3.tex"
DST = "scripts/journal_manuscript_v4.tex"

src = open(SRC).read()
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


# ---------------------------------------------------------------------
# C2: soften the bridge sentence in the categorical subsection.
# ---------------------------------------------------------------------
rep(r"""The
per-pair form of $\kmu$ is the measure-theoretic discretization of
that object --- the atomic crease measure replaces the curvature
$2$-form, and the value--flux coupling
(Theorem~\ref{thm:coupling}) supplies the survival covectors.""",
    r"""the positive part of the margin's change along the connection
curvature, normalized by the margin itself. The per-pair form of
$\kmu$ is modeled on that object --- the atomic crease measure is
the measure-theoretic analogue of the curvature $2$-form, and the
value--flux coupling (Theorem~\ref{thm:coupling}) supplies the
analogue survival covectors; the precise discretization
correspondence (a domination or ratio-form identity between the two)
is open, and is recorded as such in the companion.""",
    "C2/Fix8: bridge sentence softened to the analogue reading")

# ---------------------------------------------------------------------
# C5: regime-delineation sentence at the end of the bridge paragraph.
# ---------------------------------------------------------------------
rep(r"""\emph{Division of labor.} The present paper states only this brief
reading; the companion theory paper develops the SAVGS object, the""",
    r"""\emph{Regime delineation.} The two holonomy-scaling regimes of
Proposition~\ref{prop:dichotomy} are the measure-level image of the
companion's two loop regimes: the smooth arm (slope $2.000$) is
where the companion's quadratic small-loop law $\kappa(a) = a^{2}$
and its Fisher-minimal transport law live; the piecewise-affine
arm (slope $1.00$) is the companion's wall-crossing regime, where
a loop crossing a switching facet accumulates a boundary
contribution at $O(\varepsilon)$ per crossing (the companion's
pairs-crossing theorem).

\emph{Division of labor.} The present paper states only this brief
reading; the companion theory paper develops the SAVGS object, the""",
    "C5: regime-delineation paragraph in the categorical subsection")

# ---------------------------------------------------------------------
# C1: delegation-status qualifiers (two sites).
# ---------------------------------------------------------------------
rep(r"""adapted form, the categorical reading that first suggested the
active-set curvature interpretation; the full framework --- with its
constructions, proofs, and machine verifications --- is developed in
a companion theory paper \citep{zai2026categorical}, and nothing
below is a premise of the empirical results.""",
    r"""adapted form, the categorical reading that first suggested the
active-set curvature interpretation; the full framework --- with its
constructions, machine verifications, and proofs at the status
marked per result (complete for the gluing formula, the transport
law, the composition and contraction layers, and the
terminal-coalgebra theorem; machine-verified numerics;
citation-level stratified descent; proof-sketch-marked, as such, for
the homotopy-type-theoretic extension) --- is developed in
a companion theory paper \citep{zai2026categorical}, and nothing
below is a premise of the empirical results.""",
    "C1: delegation site 1 (categorical subsection)")

rep(r"""is developed in full,
as a standalone theory paper with its own proofs and machine
verifications, in a companion manuscript \citep{zai2026categorical}.""",
    r"""is developed in full,
as a standalone theory paper with its own proofs, machine
verifications, and per-result proof-status marking (the
homotopy-type-theoretic extension is proof-sketch-marked there; the
stratified gluing is descent-by-citation with construction-level
verification), in a companion manuscript \citep{zai2026categorical}.""",
    "C1: delegation site 2 (discussion)")

# ---------------------------------------------------------------------
# APP-1: Lemma lex generic-weights uniqueness step in the proof.
# ---------------------------------------------------------------------
rep(r"""$P_1(\theta)$, and so on; the final stage minimizes the coordinates
$v_1, \dots, v_n$ one at a time, in a fixed order, over the current
face. After the coordinate $v_j$ has been fixed to its conditional
minimum, the remaining set is the face intersected with the
hyperplane $v_j = m_j$; after all $n$ coordinates every component is
pinned to a specific value, so the final set is a single point
$v^{*}(\theta)$. Existence at every stage follows from compactness,
uniqueness from the coordinate pinning, and the lexicographic
optimum is therefore well defined.""",
    r"""$P_1(\theta)$, and so on. Two selection rules complete the
lexicographic stack, and we state both. The \emph{coordinate-pinned
completion} minimizes the coordinates $v_1, \dots, v_n$ one at a
time, in a fixed order, over the current face: after the coordinate
$v_j$ has been fixed to its conditional minimum, the remaining set
is the face intersected with the hyperplane $v_j = m_j$; after all
$n$ coordinates every component is pinned to a specific value, so
the final set is a single point $v^{*}(\theta)$ --- uniqueness is
unconditional. The \emph{engine's weighted stage~3}
(\S\ref{sec:methods}) minimizes $w^{\top}v$ over the compact
stage-2 face with the locked weight vector $w$ (seed $20240901$):
for stage-3 objectives of this form the argmin is a unique vertex
of the face for every $\theta$ outside a Lebesgue-null set of
weight vectors (the finitely many hyperplane arrangements
$\{w^{\top}v = w^{\top}v'\}$, $v \neq v'$ vertices of the face,
bound the exceptional set), so the locked seed realizes a generic
draw and the pinned vertex is unique for it; the chamber and
projection argument below then applies verbatim, and the
coordinate-pinned rule is the representative for which uniqueness
holds for \emph{every} $w$. Existence at every stage follows from
compactness, and the lexicographic optimum is therefore well
defined under both completions.""",
    "APP-1: Lemma lex proof generic-weights uniqueness step")

# ---------------------------------------------------------------------
# APP-2: semiconvexity-law contradiction (statement + proof).
# ---------------------------------------------------------------------
rep(r"""not an available weakening for LP value functions (measured: the
required constant blows up like $1/(2h)$; $\lambda \cdot h_{\max}
= 0.500$ numerically across $\lambda = 1 \dots 10^{6}$, the analytic
law $\lambda\, h_{\max} = 1/(2\lambda)$ holding at every scale,
with the numerical grid flooring above $\lambda \approx 10^{7}$).""",
    r"""not an available weakening for LP value functions (measured: the
required constant blows up like $1/(2h)$; $\lambda \cdot h_{\max}
= 0.500$ numerically across $\lambda = 1 \dots 10^{6}$, the analytic
law $h_{\max} = 1/(2\lambda)$ --- equivalently $\lambda\,
h_{\max} = 1/2$ --- holding at every scale,
with the numerical grid flooring above $\lambda \approx 10^{7}$).""",
    "APP-2: semiconvexity statement law corrected")

rep(r"""The numerical form: the
smallest violating scale $h_{\max}(\lambda)$ of the OR-plus-cap
value function satisfies $\lambda\,h_{\max} = 1/(2\lambda)$
exactly (the measured identity of the OR-plus-cap
value function below), i.e.\ no finite semiconvexity constant exists at
any scale.""",
    r"""The numerical form: the
smallest violating scale $h_{\max}(\lambda)$ of the OR-plus-cap
value function satisfies $h_{\max} = 1/(2\lambda)$ --- i.e.\
$\lambda\,h_{\max} = 1/2$, the measured $0.500$ identity of the
OR-plus-cap value function below --- exactly, i.e.\ no finite
semiconvexity constant exists at any scale.""",
    "APP-2: semiconvexity proof law corrected")

# ---------------------------------------------------------------------
# APP-3: conj:valueflux -> cor:valueflux; drop "corrected form".
# ---------------------------------------------------------------------
rep(r"""\begin{corollary}[Decoupling; resolves the value--flux layer
relation]\label{conj:valueflux}""",
    r"""\begin{corollary}[Decoupling; resolves the value--flux layer
relation]\label{cor:valueflux}""",
    "APP-3: label conj:valueflux -> cor:valueflux")
rep(r"""Corollary~\ref{conj:valueflux}); the association results of""",
    r"""Corollary~\ref{cor:valueflux}); the association results of""",
    "APP-3: ref site 1")
rep(r"""(Corollary~\ref{conj:valueflux}). The coupling identity of""",
    r"""(Corollary~\ref{cor:valueflux}). The coupling identity of""",
    "APP-3: ref site 2")
rep(r"""Corollary~\ref{conj:valueflux} this completes the robustness picture: the""",
    r"""Corollary~\ref{cor:valueflux} this completes the robustness picture: the""",
    "APP-3: ref site 3")
rep(r"""\begin{theorem}[Refinement--resolution bridge, corrected form]""",
    r"""\begin{theorem}[Refinement--resolution bridge]""",
    "APP-3: thm:Bprime title 'corrected form' dropped")

# ---------------------------------------------------------------------
# APP-5: selection-rule count harmonization.
# ---------------------------------------------------------------------
rep("tie-break-robust across four alternative selection rules, and the underlying event measures stabilize",
    "tie-break-robust across all five selection rules tested (declared plus four variants), and the underlying event measures stabilize",
    "APP-5: abstract selection-rule count")

rep("stable across four alternative selection rules, \\S\\ref{sec:v8});",
    "stable across all five selection rules tested (declared plus four variants, \\S\\ref{sec:v8});",
    "APP-5: limitations selection-rule count")

# ---------------------------------------------------------------------
# C9/APP-4: figure directory deepseek_bridge -> association_robustness.
# ---------------------------------------------------------------------
rep(r"\includegraphics[width=\textwidth]{deepseek_bridge/v5_e24_recalibration.png}",
    r"\includegraphics[width=\textwidth]{association_robustness/v5_e24_recalibration.png}",
    "C9: figure path 1")
rep(r"\includegraphics[width=0.86\textwidth]{deepseek_bridge/v7_path_robustness.png}",
    r"\includegraphics[width=0.86\textwidth]{association_robustness/v7_path_robustness.png}",
    "C9: figure path 2")
rep(r"\includegraphics[width=\textwidth]{deepseek_bridge/v8_tiebreak_robustness.png}",
    r"\includegraphics[width=\textwidth]{association_robustness/v8_tiebreak_robustness.png}",
    "C9: figure path 3")
rep(r"\includegraphics[width=\textwidth]{deepseek_bridge/e32_event_measure_stabilization.png}",
    r"\includegraphics[width=\textwidth]{association_robustness/e32_event_measure_stabilization.png}",
    "C9: figure path 4")

# Header comment: version identity.
rep(r"""% journal_manuscript_v3.tex""",
    r"""% journal_manuscript_v4.tex""",
    "header comment version", count=0) if False else None

open(DST, "w").write(src)
print(f"\nmain v4 complete: {n_applied} edits -> {DST}")
