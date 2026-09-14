#!/usr/bin/env python3
"""companion v3 part B1: 3rd-wave Fix 2 (optic-colimit demotion + the
corrected adapter statement), Fix 3 (one catalysis condition =
Hordijk-Steel closure across def:raf / def:deflationary / appendix),
Fix 6 (enlarged state box; K instantiated; dangling hypotheses
dropped; KM gloss), plus the abstract/contribution/open-problem
rewordings these force. Reads and rewrites
scripts/companion_categorical_v3.tex in place.
"""
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
# Fix 2: the filtered-colimit theorem, corrected scope.
# =====================================================================

rep(r"""\begin{theorem}[Filtered colimits in $\Optic(\mathbf{Set})$]
\label{thm:filtered-colimits-optic}
Let $\mathbb I$ be a filtered category and
$F:\mathbb I\to\Optic(\mathbf{Set})$ a filtered diagram. Write
$F(i)=(M_{i},C_{i})$ for each $i\in\mathbb I$, and the morphism
$F(i\to j)$ as the optic $(R_{ij},f_{ij},g_{ij})$ with forward
$f_{ij}:M_{i}\times R_{ij}\to M_{j}$ and backward
$g_{ij}:R_{ij}\times C_{j}\to C_{i}$. Then the colimit of $F$ exists in
$\Optic(\mathbf{Set})$ and is given componentwise by
\begin{equation}\label{eq:filtered-colim}
  \colim F \;=\; \bigl(\,\colim_{i\in\mathbb I}\,M_{i},\;\;
  \colim_{i\in\mathbb I}\,C_{i}\,\bigr),
\end{equation}
with both colimits taken in $\mathbf{Set}$. The universal cocone optic
$\eta_{i}:F(i)\to\colim F$ has residual
\begin{equation}\label{eq:residual-i}
  R_{i}^{\infty} \;=\; \colim_{(i\to j)\in(i\downarrow\mathbb I)}\,R_{ij},
\end{equation}
the colimit of the residuals $R_{ij}$ over the comma category
$(i\downarrow\mathbb I)$ of arrows out of $i$ (which is filtered
because $\mathbb I$ is).
\end{theorem}

\begin{proof}
The construction proceeds in three steps.

\noindent\textit{Step 1: Object component.} Since $\mathbf{Set}$ is
locally finitely presentable~\cite{adamek1994}, filtered colimits
exist and commute with finite limits; in particular, the colimits
$M_{\infty}:=\colim_{i}M_{i}$ and $C_{\infty}:=\colim_{i}C_{i}$ exist
in $\mathbf{Set}$, with colimit cocone maps
$\mu_{i}:M_{i}\to M_{\infty}$ and $\nu_{i}:C_{i}\to C_{\infty}$.

\noindent\textit{Step 2: Residual and forward map.} For each $i\in
\mathbb I$, define $R_{i}^{\infty}$ by~\eqref{eq:residual-i}; this
colimit exists in $\mathbf{Set}$ because the comma category
$(i\downarrow\mathbb I)$ is filtered (a standard fact: filteredness is
inherited by comma categories over filtered diagrams). Let
$\rho_{ij}:R_{ij}\to R_{i}^{\infty}$ denote the colimit structure map
for each $(i\to j)\in(i\downarrow\mathbb I)$. Define the forward map
\begin{equation*}
  f_{i}^{\infty}:M_{i}\times R_{i}^{\infty}\to M_{\infty},
  \qquad
  f_{i}^{\infty}(m,\rho_{ij}(r)) \;=:\; \mu_{j}\!\bigl(f_{ij}(m,r)\bigr),
\end{equation*}
where for $r\in R_{i}^{\infty}$ we choose any representative
$(i\to j,r_{0}\in R_{ij})$ with $\rho_{ij}(r_{0})=r$ (such a
representative exists by the colimit's universal property). The map is
well-defined: for any other representative $(i\to j',r_{0}'\in
R_{ij'})$ with $\rho_{ij'}(r_{0}')=r$, filteredness of
$(i\downarrow\mathbb I)$ supplies $k\in\mathbb I$ with arrows
$\alpha:j\to k$, $\beta:j'\to k$; by the diagram's commutativity
(the optic composition law for $F(i\to j\to k)$ and
$F(i\to j'\to k)$), the two images $\mu_{j}(f_{ij}(m,r_{0}))$ and
$\mu_{j'}(f_{ij'}(m,r_{0}'))$ agree in $M_{\infty}$ (both map to
$\mu_{k}(f_{ik}(m,\bar r))$ for the appropriate $\bar r\in R_{ik}$
induced by the diagram).

\noindent\textit{Step 3: Backward map.} Define
\begin{equation*}
  g_{i}^{\infty}:R_{i}^{\infty}\times C_{\infty}\to C_{i},
  \qquad
  g_{i}^{\infty}(\rho_{ij}(r),\nu_{j'}(c)) \;=:\;
  g_{ij}(r,\,\nu_{j\to j'}^{C}(c))\quad\text{if }j'=j,
\end{equation*}
and extend by filteredness for general $j'$: choose $k$ with $j\to k$
and $j'\to k$, then map $(r,c)\in R_{ij}\times C_{j'}$ to
$g_{ij}(r,\bar c)\in C_{i}$ where $\bar c\in C_{j}$ is the pullback
of $c$ along $C_{j'}\to C_{k}\leftarrow C_{j}$. Well-definedness uses
the optic composition law $g_{ij}(r,g_{jk}(\bar r,c))=
g_{ik}(\bar r',c)$ (for the appropriate $\bar r'\in R_{ik}$), which is
the associativity of optic composition~\cite[Prop.~2.3]{riley2018optics}.

The universal property: for any cocone
$\gamma_{i}:F(i)\to(M',C')$ with residuals $S_{i}$, the unique map
$\colim F\to(M',C')$ is constructed from the universal property of the
$\mathbf{Set}$-colimits $M_{\infty}$, $C_{\infty}$, and
$R_{i}^{\infty}$; the optic morphism axioms are verified by chasing
the colimit structure maps through the cocone compatibility conditions.
Details are a routine categorical diagram chase.
\end{proof}""",
r"""\begin{theorem}[Filtered colimits of directed systems in
$\Optic(\mathbf{Set})$; corrected scope]
\label{thm:filtered-colimits-optic}
Let $\mathbb I$ be a filtered category and
$F:\mathbb I\to\Optic(\mathbf{Set})$ a diagram in the strict feedback
form of Remark~\ref{rem:optic-strict}. Write $F(i)=(M_{i},C_{i})$ for
each $i\in\mathbb I$, and the morphism $F(i\to j)$ as the optic
$(R_{ij},f_{ij},g_{ij})$ with forward
$f_{ij}:M_{i}\times R_{ij}\to M_{j}$ and backward
$g_{ij}:R_{ij}\times C_{j}\to C_{i}$. Then:
\begin{enumerate}[leftmargin=*,itemsep=2pt]
\item[\emph{(i)}] \emph{(RAF level; proved.)} If the diagram's
  forward carriers carry a declared directed system of inclusions
  (as in Construction~\ref{con:invlim}: each $F(i\to j)$ acts
  adapter-level on the forward carrier, $R_{ij}=1$ and
  $f_{ij}:M_i\hookrightarrow M_j$ an inclusion), then the colimit of
  the underlying directed system exists in $\mathbf{Set}$ and is the
  union $M_{\infty}=\bigcup_{i\in\mathbb I}M_{i}$; the lift of each
  stage to an object of $\Optic(\mathbf{Set})$ with the inclusions as
  structure arrows is a functor from the inclusion poset to
  $\Optic(\mathbf{Set})$, and the viability-preservation and
  consistency results of
  Propositions~\ref{prop:invlim}--\ref{prop:invlim-extended} refer to
  this Set-level colimit.
\item[\emph{(ii)}] \emph{(Adapter level; proved.)} If every morphism
  of the diagram is an adapter ($R_{ij}=1$), with forward
  $f_{ij}:M_{i}\to M_{j}$ and backward $g_{ij}:C_{j}\to C_{i}$, then
  the colimit of $F$ in the adapter subcategory exists and is
  \begin{equation}\label{eq:filtered-colim}
    \colim F \;=\; \bigl(\,\colim_{i\in\mathbb I}\,M_{i},\;\;
    \lim_{i\in\mathbb I^{\mathrm{op}}}\,C_{i}\,\bigr),
  \end{equation}
  with both (co)limits taken in $\mathbf{Set}$: the colimit of the
  forward carriers and the \emph{limit} of the backward carriers ---
  the backward components are contravariant along the diagram's
  arrows --- universal among adapter cocones.
\item[\emph{(iii)}] \emph{(General feedback diagrams: open.)} For
  diagrams with nontrivial feedback residuals, a componentwise
  cocone requires \emph{declared backward structure}: maps
  $k_{i}:C^{*}\to C_{i}$ satisfying $g_{ij}(r,k_{j}(c))=k_{i}(c)$
  for every residual value $r\in R_{ij}$ --- data that a general
  diagram does not supply. The general componentwise claim is
  therefore not stated as a theorem; its status and the obstruction
  are recorded in Remark~\ref{rem:colimit-status} and
  Open Problem~3.
\end{enumerate}
\end{theorem}

\begin{proof}
\emph{(i)} The union of a directed system of inclusions is the
$\mathbf{Set}$-colimit of the system: every element of the union lies
in some $M_{i}$, compatibility of the cocone legs
$\mu_{i}:M_{i}\hookrightarrow M_{\infty}$ is automatic for
inclusions, and any other cocone $(M', h_{i}:M_{i}\to M')$ factors
uniquely through $M_{\infty}$ by $h(m) := h_{i}(m)$ for
$m\in M_{i}$ (well defined because the $h_{i}$ agree on overlaps, and
unique because the $M_{i}$ cover $M_{\infty}$). The lift to
$\Optic(\mathbf{Set})$ is functorial because adapter composition on
the forward carrier is function composition and the inclusions
compose as inclusions.

\emph{(ii)} Let $M_{\infty}=\colim_{i}M_{i}$ with structure maps
$\mu_{i}:M_{i}\to M_{\infty}$, and let $C_{\infty}=
\lim_{i\in\mathbb I^{\mathrm{op}}}C_{i}$ with limit cone
$\pi_{i}:C_{\infty}\to C_{i}$ (the limit exists: $\mathbf{Set}$ is
complete; concretely it is the equalizer of the product of the
$C_{i}$ over the compatibility maps $g_{ij}$). Define the cocone leg
at $i$ as the adapter $\eta_{i}=(1,\mu_{i},\pi_{i}):
F(i)\to(M_{\infty},C_{\infty})$. For each arrow $i\to j$ of
$\mathbb I$, the composite
$\eta_{j}\circ F(i\to j)$ is the adapter $(1,\;
\mu_{j}\circ f_{ij}:M_{i}\to M_{\infty},\;
g_{ij}\circ\pi_{j}:C_{\infty}\to C_{i})$, and the cocone condition
$\eta_{j}\circ F(i\to j)=\eta_{i}$ reads
$\mu_{j}\circ f_{ij}=\mu_{i}$ (the colimit cocone condition on the
forward carriers) and $g_{ij}\circ\pi_{j}=\pi_{i}$ (the limit cone
condition on the backward carriers); both hold by construction.
Universality among adapter cocones: given another adapter cocone with
legs $(1,h_{i}:M_{i}\to M',k_{i}:C'\to C_{i})$, the colimit gives the
unique forward map $u:M_{\infty}\to M'$ with $u\circ\mu_{i}=h_{i}$,
and the family $k_{i}:C'\to C_{i}$ satisfies
$g_{ij}\circ k_{j}=k_{i}$ (the same cocone computation), i.e.\ it is
a cone over the $\mathbb I^{\mathrm{op}}$-diagram with vertex $C'$;
the limit gives the unique map $v:C'\to C_{\infty}$ with
$\pi_{i}\circ v=k_{i}$. The adapter $(1,u,v)$ is then the unique
mediating morphism.

\emph{(iii)} is a statement of scope, proved by the obstruction
recorded in Remark~\ref{rem:colimit-status}.
\end{proof}

\begin{remark}[Status of the general componentwise claim]
\label{rem:colimit-status}
For diagrams with nontrivial feedback residuals the backward
carriers are contravariant along the diagram's arrows: a morphism
$F(i\to j)$ carries $C_{j}$ to $C_{i}$, so there is no
$C_{j}\to C_{j'}$ structure map along which an element of $C_{j'}$
could be transported, and an element-level pullback along a cospan
$C_{j'}\to C_{k}\leftarrow C_{j}$ with no maps into $C_{j}$ cannot be
formed. A componentwise cocone therefore requires the declared
backward structure of Theorem~\ref{thm:filtered-colimits-optic}(iii)
--- a family $k_{i}:C^{*}\to C_{i}$ compatible with the diagram's
backward legs uniformly in the residual --- which is exactly what the
RAF instantiation supplies (the constant declared backward carrier)
and what a general diagram lacks. The same obstruction applies to
the residual side: a colimit of the $R_{ij}$ over the comma category
$(i\downarrow\mathbb I)$ would require declared residual structure
maps $R_{ij}\to R_{ij'}$ along the comma category's arrows, which
the strict composition law (product residuals) does not supply. The
scale-up verification of Proposition~\ref{prop:invlim-extended}
tests part~(i) --- the Set-level colimit of the RAF system --- and
does not depend on the optic-level claims.
\end{remark}""",
    "Fix2: filtered-colimits theorem corrected scope + proof + status remark")

# con:invlim forward pointer.
rep(r"""The construction is verified by direct computation on the small
network; the universal colimit existence in $\Optic(\mathbf{Set})$ for
larger networks is established componentwise below
(Theorem~\ref{thm:filtered-colimits-optic}).""",
    r"""The construction is verified by direct computation on the small
network; the colimit statement for larger networks --- the Set-level
union of part~(i), the adapter-level (colimit, limit) form of
part~(ii), and the scope of the optic-level claim --- is established
below (Theorem~\ref{thm:filtered-colimits-optic}).""",
    "Fix2: con:invlim pointer to the corrected theorem")

# rem:viability-inherit: drop the residual-colimit reference.
rep(r"""The viability-preservation claim of Proposition~\ref{prop:invlim}
extends from the small network's enumerated colimit to the general
filtered-colimit construction of Theorem~\ref{thm:filtered-colimits-optic}
under the same two hypotheses: (i) monotonicity $R\subseteq R'\implies
V(R)\leq V(R')$; (ii) directed continuity $V(\bigcup_{i}R_{i})=
\lim_{i}V(R_{i})$. The proof is identical to that of
Proposition~\ref{prop:invlim}, applied to the colimit of the residuals
$R_{i}^{\infty}$ rather than to the colimit of the RAF sets $R_{i}$
themselves.""",
    r"""The viability-preservation claim of Proposition~\ref{prop:invlim}
extends from the small network's enumerated colimit to the Set-level
filtered-colimit construction of
Theorem~\ref{thm:filtered-colimits-optic}(i) under the same two
hypotheses: (i) monotonicity $R\subseteq R'\implies
V(R)\leq V(R')$; (ii) directed continuity $V(\bigcup_{i}R_{i})=
\lim_{i}V(R_{i})$. The proof is identical to that of
Proposition~\ref{prop:invlim}, applied to the colimit object's
forward carriers (the union) rather than to the enumerated RAF sets
themselves.""",
    "Fix2: rem:viability-inherit reworded to the Set-level colimit")

# rem:set-suffices: reworded for the corrected proof.
rep(r"""The proof of Theorem~\ref{thm:filtered-colimits-optic} uses three
properties of $\mathbf{Set}$ that hold more generally for any locally
finitely presentable (lfp) category~\cite{adamek1994}: (i) filtered
colimits exist; (ii) filtered colimits commute with finite limits (so
the product $R_{i}^{\infty}\times C_{\infty}$ in Step~3 distributes
over the colimit, allowing the well-definedness argument); (iii) the
hom-functor $\mathbf{Set}(-,X)$ preserves filtered colimits (a
consequence of finite presentability of the singleton). For a general
monoidal category $\CC$ that lacks these properties, the
componentwise construction may fail; the conjecture's generalization
to arbitrary $\CC$ remains open but is not needed for the present
framework, which works over $\mathbf{Set}$ throughout.""",
    r"""The proof of Theorem~\ref{thm:filtered-colimits-optic} uses three
properties of $\mathbf{Set}$ that hold more generally for any locally
finitely presentable (lfp) category~\cite{adamek1994}: (i) filtered
colimits exist; (ii) limits of $\mathbb I^{\mathrm{op}}$-diagrams
exist ($\mathbf{Set}$ is complete); (iii) the hom-functor
$\mathbf{Set}(-,X)$ preserves filtered colimits (a consequence of
finite presentability of the singleton). For a general monoidal
category $\CC$ that lacks these properties, the componentwise
construction may fail; the extension to arbitrary $\CC$ remains open
but is not needed for the present framework, which works over
$\mathbf{Set}$ throughout.""",
    "Fix2: rem:set-suffices reworded")

# prop:invlim-extended item 2: adapter-level lift wording.
rep(r"""\item \emph{Filtered colimit}: there is a unique maximal RAF
  $R_{\max}=\{r_1,\ldots,r_{11}\}$ with $|R_{\max}|=11$, which
  equals the union of all $16$ enumerated RAFs. The $15$ structure
  arrows $R_i \to R_{\max}$ are the
  inclusions, witnessing the universal property of the colimit in
  $\Optic(\mathbf{Set})$.""",
    r"""\item \emph{Filtered colimit}: there is a unique maximal RAF
  $R_{\max}=\{r_1,\ldots,r_{11}\}$ with $|R_{\max}|=11$, which
  equals the union of all $16$ enumerated RAFs. The $15$ structure
  arrows $R_i \to R_{\max}$ are the inclusions, witnessing the
  universal property of the Set-level colimit; their lift to
  $\Optic(\mathbf{Set})$ is adapter-level on the forward carriers
  (Theorem~\ref{thm:filtered-colimits-optic}(i)).""",
    "Fix2: prop:invlim-extended item 2 adapter-level wording")

# F8-minimal: drop the undefined h_alpha / Bregman-projected phrases.
rep(r"""\item \emph{Consistency check}: $\kk(R_{\max})$ computed via the
  filtered-colimit construction (the colimit's viability-weighted
  curvature as the colimit of the per-$i$ curvatures, scaled by the
  $h_\alpha$ at $R_{\max}$) equals $\kk(R_{\max})$ computed via the
  operational form of Definition~\ref{def:kv} on the
  maximal RAF's Bregman-projected structure. Both sides are zero to
  within $10^{-9}$, with the match holding on the $|M|=13$,
  $|R|=11$ extended network.""",
    r"""\item \emph{Consistency check}: the $\kk$-evaluation transported
  to the discrete RAF setting (the colimit of the per-$i$
  evaluations) equals the direct evaluation at the colimit object.
  Both sides are zero to within $10^{-9}$ --- a structural
  consistency check, not a falsifiable claim
  (Remark~\ref{rem:zero-zero}) --- with the match holding on the
  $|M|=13$, $|R|=11$ extended network.""",
    "F8-minimal: undefined h_alpha/Bregman-projected phrases dropped")

# Open problem 3: extend with the obstruction + residual side.
rep(r"""\item \emph{Filtered colimits beyond $\mathbf{Set}$.} The
componentwise construction of
Theorem~\ref{thm:filtered-colimits-optic} uses that $\mathbf{Set}$ is
locally finitely presentable: filtered colimits exist, commute with
finite limits, and are preserved by hom-functors. The extension to
general lfp monoidal categories $\CC$ --- and the identification of
the minimal hypotheses under which componentwise colimits remain
optics --- is open (Remark~\ref{rem:set-suffices}).""",
    r"""\item \emph{Filtered colimits beyond $\mathbf{Set}$, and the
optic-level colimit.} The componentwise statements of
Theorem~\ref{thm:filtered-colimits-optic} use that $\mathbf{Set}$ is
locally finitely presentable and complete. Two extensions are open:
(a) the general lfp monoidal case of the adapter statement; and
(b) the componentwise colimit for diagrams with nontrivial feedback
residuals --- the backward carriers are contravariant along the
diagram's arrows, so a componentwise cocone requires declared
backward structure, which a general diagram does not supply
(Remark~\ref{rem:colimit-status}); the residual-level colimit over
the comma category $(i\downarrow\mathbb I)$ likewise requires
declared residual structure maps and is not constructed here.""",
    "Fix2: open problem 3 extended with the obstruction")

# =====================================================================
# Fix 3: one catalysis condition (Hordijk-Steel closure).
# =====================================================================

rep(r"""\begin{definition}[RAF set]
\label{def:raf}
Following Hordijk and Steel~\cite{steel2004,hordijk2011}, given a
catalytic reaction network $(X, \mathcal{R}, F, c)$ over a molecule set
$X$ with food set $F\subset X$ and catalysis assignment $c:\mathcal{R}
\to 2^X$, a subset $R'\subseteq\mathcal{R}$ is a \emph{reflexively
autocatalytic food-generated (RAF) set} if (i) every $r\in R'$ is
catalyzed by some element of $F\cup\bigcup_{r'\in R'}\mathrm{react}(r')$,
(ii) the food-generated closure of $R'$ contains all reactants of $R'$,
and (iii) $R'$ is closed under the induced closure operator.
\end{definition}""",
    r"""\begin{definition}[Hordijk--Steel closure and RAF set]
\label{def:raf}
Following Hordijk and Steel~\cite{steel2004,hordijk2011}, given a
catalytic reaction network $(X, \mathcal{R}, F, c)$ over a molecule set
$X$ with food set $F\subset X$ and catalysis assignment $c:\mathcal{R}
\to 2^X$, define for each $A\subseteq\mathcal{R}$ the
\emph{Hordijk--Steel closure} $\mathrm{cl}_{A}(F)$ of the food set
under $A$ as the least set of molecules containing $F$ and closed
under the reactions of $A$:
\begin{equation}\label{eq:hs-closure}
  \mathrm{cl}_{A}(F) \;:=\; \bigcup_{n\geq 0} S_{n}, \qquad
  S_{0}=F,\qquad
  S_{n+1} \;=\; S_{n}\cup\bigl\{\mathrm{react}(r)\cup\mathrm{prod}(r):
  r\in A,\ \mathrm{react}(r)\subseteq S_{n}\bigr\}.
\end{equation}
A subset $R'\subseteq\mathcal{R}$ is a \emph{reflexively
autocatalytic food-generated (RAF) set} if (i) every $r\in R'$ is
catalyzed by some element of $\mathrm{cl}_{R'}(F)$, and (ii) every
reactant of every $r\in R'$ lies in $\mathrm{cl}_{R'}(F)$. (Both
conditions use the closure: catalysts must be food-reachable through
$R'$, not merely present as reactants or products of $R'$.)
\end{definition}""",
    "Fix3: def:raf restated with the HS closure (catalysts from the closure)")

rep(r"""\begin{definition}[Catalytic closure and the deflationary closure
operator]\label{def:deflationary}
Fix a food set $F$ and a finite reaction universe $U\subseteq R$.
For $S\subseteq U$ let $\mathrm{prod}(S)$ be the set of molecules
produced by the reactions of $S$, and let
$\mathrm{cl}(F\cup\mathrm{prod}(S))$ be the food-generated closure
(the smallest set of molecules containing $F\cup
\mathrm{prod}(S)$ that is closed under the reactions of $S$).
Define the \emph{catalytic-closure operator}
\begin{equation}\label{eq:Phi-def}
\begin{split}
  \Phi(S) \;=\; \{\, & r\in U : \text{some catalyst of } r \text{ lies in }
  \mathrm{prod}(S)\cup F,\\
  & \text{and every reactant of } r \text{ lies in }
  \mathrm{cl}(F\cup\mathrm{prod}(S)) \,\},
\end{split}
\end{equation}
and the \emph{deflationary closure operator}
\begin{equation}\label{eq:D-def}
  D(S) \;=\; S \cap \Phi(S).
\end{equation}
\end{definition}""",
    r"""\begin{definition}[Catalytic closure and the deflationary closure
operator]\label{def:deflationary}
Fix a food set $F$ and a finite reaction universe $U\subseteq R$.
For $S\subseteq U$ write $\mathrm{cl}_{S}(F)$ for the
Hordijk--Steel closure of Definition~\ref{def:raf} (the closure of
the food set under the reactions of $S$; monotone in $S$). Define
the \emph{catalytic-closure operator}
\begin{equation}\label{eq:Phi-def}
\begin{split}
  \Phi(S) \;=\; \{\, & r\in U : \text{some catalyst of } r \text{ lies in }
  \mathrm{cl}_{S}(F),\\
  & \text{and every reactant of } r \text{ lies in }
  \mathrm{cl}_{S}(F) \,\},
\end{split}
\end{equation}
and the \emph{deflationary closure operator}
\begin{equation}\label{eq:D-def}
  D(S) \;=\; S \cap \Phi(S).
\end{equation}
With the catalyst pool taken as the closure $\mathrm{cl}_{S}(F)$
(rather than, say, $F\cup\mathrm{prod}(S)$), the fixed points of $D$
are exactly the RAFs of Definition~\ref{def:raf}: a product-pool
catalyst condition would be strictly weaker, admitting mutually
catalyzing cycles with nothing food-reachable
($r_{1}:X\to Y$, $r_{2}:Y\to X$) that the closure-based condition
excludes.
\end{definition}""",
    "Fix3: def:deflationary catalyst pool = cl_S(F)")

# Appendix: monotonicity argument + the (ii) identification + (iv).
rep(r"""(i) Deflationarity is immediate: $D(S)=S\cap\Phi(S)\subseteq S$.
For monotonicity, let $S\subseteq T$. Then
$\mathrm{prod}(S)\subseteq\mathrm{prod}(T)$, hence
$\mathrm{cl}(F\cup\mathrm{prod}(S))\subseteq
\mathrm{cl}(F\cup\mathrm{prod}(T))$ and the catalyst pool
$\mathrm{prod}(S)\cup F\subseteq\mathrm{prod}(T)\cup F$; both
conditions in~\eqref{eq:Phi-def} are therefore satisfied by at
least as many reactions for $T$ as for $S$, so
$\Phi(S)\subseteq\Phi(T)$ and
$D(S)=S\cap\Phi(S)\subseteq T\cap\Phi(T)=D(T)$.""",
    r"""(i) Deflationarity is immediate: $D(S)=S\cap\Phi(S)\subseteq S$.
For monotonicity, let $S\subseteq T$. The closure is monotone in
the reaction set: $\mathrm{cl}_{S}(F)\subseteq\mathrm{cl}_{T}(F)$
(a reaction applicable under $S$ is applicable under $T$, so the
iteration~\eqref{eq:hs-closure} from $F$ can only add molecules);
both conditions in~\eqref{eq:Phi-def} are therefore satisfied by at
least as many reactions for $T$ as for $S$, so
$\Phi(S)\subseteq\Phi(T)$ and
$D(S)=S\cap\Phi(S)\subseteq T\cap\Phi(T)=D(T)$.""",
    "Fix3: appendix monotonicity via the closure")

rep(r"""(ii) For $S\subseteq U$, $D(S)=S$ iff $S\subseteq\Phi(S)$ iff
every $r\in S$ has a catalyst in $\mathrm{prod}(S)\cup F$ and all
reactants of $r$ in $\mathrm{cl}(F\cup\mathrm{prod}(S))$. The
first clause is reflexive autocatalysis; the second is
food-generatedness (each reaction's inputs are reachable from the
food set through the reactions of $S$). These are exactly the RAF
conditions of \citealp{hordijk2011,steel2004}, restricted to
subsets of $U$.""",
    r"""(ii) For $S\subseteq U$, $D(S)=S$ iff $S\subseteq\Phi(S)$ iff
every $r\in S$ has a catalyst in $\mathrm{cl}_{S}(F)$ and all
reactants of $r$ in $\mathrm{cl}_{S}(F)$. The
first clause is reflexive autocatalysis (each reaction is catalyzed
by a molecule reachable from the food through $S$ itself); the
second is food-generatedness (each reaction's inputs are reachable
from the food set through the reactions of $S$). These are exactly
the RAF conditions of Definition~\ref{def:raf} and
of \citealp{hordijk2011,steel2004}, restricted to subsets of $U$.""",
    "Fix3: appendix (ii) via the closure (now exact)")

rep(r"""(iv) The Hordijk--Steel iterative-removal algorithm initializes
with the full reaction set and repeatedly deletes every reaction
that is neither catalyzed by the current set nor generatable from
the food given the current set, until no further deletion is
possible. The retained set after one deletion round is exactly
$S\cap\Phi(S)=D(S)$: the reactions of $S$ that satisfy both
conditions.""",
    r"""(iv) The Hordijk--Steel iterative-removal algorithm initializes
with the full reaction set and repeatedly deletes every reaction
that is neither catalyzed by an element of the current food-closure
nor has all its reactants in that closure, until no further
deletion is possible. The retained set after one deletion round is
exactly $S\cap\Phi(S)=D(S)$: the reactions of $S$ whose catalysts
and reactants both lie in $\mathrm{cl}_{S}(F)$.""",
    "Fix3: appendix (iv) HS algorithm step identification")

# =====================================================================
# Fix 6: enlarged state box; K instantiated; hypotheses dropped; KM.
# =====================================================================

rep(r"""For each $i\in\{1,3,4,5,6,7\}$ (the six contracting optics: RAF, IFS,
Noether, perturbation, WCIG, $n=3$ Fisher--Rao), instantiate the
forward map on $X=[0,1]^{d}$ as""",
    r"""For each $i\in\{1,3,4,5,6,7\}$ (the six contracting optics: RAF, IFS,
Noether, perturbation, WCIG, $n=3$ Fisher--Rao), instantiate the
forward map on $X=[-1.5,1.5]^{d}$ as""",
    "Fix6: instantiation box X = [-1.5,1.5]^d")

open(F, "w").write(src)
print(f"\npart B1 complete: {n_applied} edits (in place)")
