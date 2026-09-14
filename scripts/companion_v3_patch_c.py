#!/usr/bin/env python3
"""companion v3 part C: the Keio external-anchor closure (E12/E15/E16,
restored from the frozen v1 sources with artifact-verified numbers and
the v21 medium-audit note), the E14 COT/NE structural-benchmark closure
(closing the Novelty report's Upgrade 3(iii)), the C1 delegation-status
framing, the C5 regime-delineation remark, and the C8 count-hygiene
column. In place on scripts/companion_categorical_v3.tex."""
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
# Keio closure + E14 structural benchmark: two new subsections after
# the fixed-model iJO1366 arm.
# =====================================================================
rep(r"""\begin{proof}
Direct computation on the unmodified model (deposited artifacts):
the confusion matrix, the $\kappa$/MCC/$F_1$/precision/recall
values, and the ROC curve are the deposited outputs of the two
independent computations (closure-test dependency ratios; FBA
single-reaction deletions) on the same model.
\end{proof}""",
    r"""\begin{proof}
Direct computation on the unmodified model (deposited artifacts):
the confusion matrix, the $\kappa$/MCC/$F_1$/precision/recall
values, and the ROC curve are the deposited outputs of the two
independent computations (closure-test dependency ratios; FBA
single-reaction deletions) on the same model.
\end{proof}

\begin{remark}[Threshold provenance of the fixed-model arm]
\label{rem:ijo-threshold}
The reaction-level threshold $\tau^{*}=0.5$ of
Proposition~\ref{prop:iJO1366-external} is tuned on the full
evaluation set ($n=1{,}638$; no reaction-level held-out split);
the fixed-model arm is thereby an internal cross-validation on an
unmodified model, and the external-data anchor of the next
subsection is what carries genuinely outside information.
\end{remark}

\subsection{External anchor: the Keio collection}\label{sec:network-keio}

The fixed-model arm validates the closure test against independently
computed FBA essentiality --- an internal cross-check. This
subsection adds the external data anchor named by the novelty
assessment: the growth-phenotype panel of the Keio
single-gene-deletion collection of \emph{E.~coli} K-12
\citep{baba2006keio} ($\sim4{,}000$ measured single-gene-deletion
growth phenotypes on glucose minimal and rich media). The
reconstruction whose in-silico phenotypes anchor the transitive arm
is iJO1366 \citep{orth2011ijo1366}, whose essentiality predictions
were validated against the experimental Keio collection at
$93.4\%$ accuracy on glucose minimal media by its authors; the
cross-rebuild arm uses iML1515 \citep{monk2017iml1515}. The
predictor validated throughout is the \emph{unmasked} flux-rerouting
magnitude
\[
  \kappa^{\mathrm{flux}}_V(g) \;=\; \textstyle\sum_{r\in\Delta R(g)}
  \bigl(v_r(\mathrm{KO})-v_r(\mathrm{WT})\bigr)^{2},
  \qquad
  \Delta R(g)=\{r : |v_r(\mathrm{KO})-v_r(\mathrm{WT})|>10^{-6}\},
\]
computed by pFBA on the deposited model files --- a statistic that
carries no essentiality call and is therefore not the circular,
indicator-masked construction whose retirement
Remark~\ref{rem:fba-kappa-superseded} records. Three studies
(deposited scripts and result records; Data Availability):

\begin{proposition}[Transitive Keio anchor (E12)]\label{prop:keio-e12}
For every gene $g$ in iJO1366 ($n=1{,}367$; wild-type pFBA biomass
$15.444$; essentiality threshold $5\%$ of wild type), the
in-silico phenotype $y(g)=1$ iff $b_{\mathrm{KO}}(g)<
0.05\,b_{\mathrm{wt}}$ gives $289/1{,}367=21.1\%$ essential
(published Keio fraction $\sim18\%$). Calibration against
$\kappa^{\mathrm{flux}}_V$:
Pearson $r(\log\kappa^{\mathrm{flux}}_V,\Delta b)=+0.370$
($p=1.8\times10^{-45}$); Spearman $\rho=+0.390$
($p=6.7\times10^{-51}$); partial $r$ controlling the number of
GPR reactions $+0.364$ ($p=5.1\times10^{-44}$); bootstrap $95\%$
CI $[0.351,0.389]$. Held-out $70/30$ logistic regression on
$\log\kappa^{\mathrm{flux}}_V$ ($n=411$ test genes, $87$
essential): ROC AUC $=0.953$, sensitivity $0.759$, specificity
$0.948$, precision $0.795$, $F_1=0.777$, MCC $=0.719$; confusion
$(\mathrm{tn},\mathrm{fp},\mathrm{fn},\mathrm{tp})=
(307,17,21,66)$. Top-$K$ precision against the $21.1\%$ base rate:
P@$200=0.805$ ($3.81\times$ lift), P@$100=0.680$,
P@$10=0.700$ ($3.31\times$).
\end{proposition}

\begin{proposition}[Direct primary-source validation (E15)]
\label{prop:keio-e15}
Matching the $1{,}367$ genes to the \emph{raw} Keio essentiality
call of Baba et al.'s Supplementary Table~7 (values
$\{E,N,u\}$; after de-duplication of $867$ repeated b-numbers,
$3{,}144$ unique b-numbers remain) by Blattner b-number gives
$1{,}212$ matched genes ($88.7\%$ coverage); the binary subset
(drop $u$) is $n=1{,}206$ ($130$ E, $1{,}076$ N; base rate
$10.8\%$). Direct validation, no transitive hop: Pearson
$r(\log\kappa^{\mathrm{flux}}_V,\mathrm{Keio}\text{-}E)=+0.085$
($p=3.3\times10^{-3}$); Spearman $\rho=+0.228$
($p=9.6\times10^{-16}$); ROC AUC $0.713$. Held-out $70/30$
logistic regression: ROC AUC $0.757$, sensitivity $0.923$,
specificity $0.180$, precision $0.120$, MCC $0.085$, confusion
$(58,265,3,36)$ on $n=362$ ($39$ essential). The rank-level
association is significant and the AUC is moderate; the
point-calibration is weak --- $\kappa^{\mathrm{flux}}_V$ is
heavy-tailed, and the top of its ranking contains both Keio-$E$
genes and glucose-minimal-only essentials that the original screen
scored $N$ on rich media. Supplementary Table~6 stratification
(within the matched set): high-confidence essentials (Keio $=E$
and PEC $=E$) $n=84$; low-confidence essentials (Keio $=E$,
PEC $=N$) $n=35$.
\end{proposition}

\begin{proposition}[Cross-rebuild stress test (E16)]
\label{prop:keio-e16}
Repeating the direct protocol on the iML1515 rebuild ($1{,}516$
genes; wild-type pFBA biomass $0.926$; $286/1{,}516=18.9\%$
essential in silico; $1{,}325$ genes matched to the raw Keio call,
$114$ E) gives Pearson $r=-0.018$ ($p=0.52$), Spearman
$\rho=-0.070$ ($p=0.011$), ROC AUC $0.428$: the direct one-hop
association does \emph{not} transfer to the rebuild --- a negative
verdict, reported as such. The model-gap candidates shrink from
$30$ (iJO1366) to $13$ (iML1515) and the in-silico essentiality
fraction moves toward the experimental fraction; the direct
association flips sign.
\end{proposition}

\begin{remark}[Medium audit (the $15.444$ versus $0.926$ question)]
\label{rem:keio-medium-audit}
The two wild-type optima were re-computed on the deposited model
files by the verification script
(\texttt{verify\_e12\_e16\_biomass\_units.py}, output deposited):
the E12 value $15.444$ is an artifact of the medium construction
--- the script's re-opened ``minerals'' include the trehalose
exchange at unlimited uptake ($-337$~mmol/gDW/h at the optimum;
closing the trehalose exchange alone gives $0.982$~h$^{-1}$, the
canonical iJO1366 glucose-minimal optimum) --- while the E16
protocol re-opens the same exchange at $-10$ (effective uptake
$-6.4$), giving $0.926$ against a glucose-only optimum of
$0.822$. The two wild-type values are therefore neither mutually
comparable growth rates nor a stoichiometry effect, and both media
were mislabeled ``glucose minimal'' in the deposited study
records. Essentiality calls use the relative $5\%$-of-wild-type
threshold within each model, which is invariant to the absolute
scale; the identity of the available carbon sources, however,
enters every knockout solution, so the E12/E15/E16 essentiality
sets, the $\kappa^{\mathrm{flux}}_V$ values, and the calibration
statistics inherit the medium asymmetry. A corrected glucose-only
re-run remains an open methodological item; the deposited results
are reported unaltered and flagged here rather than silently
recomputed.
\end{remark}

\subsection{Benchmark against the structural closure instruments}
\label{sec:network-keio-e14}

The closure criteria of Definition~\ref{def:closure-criteria} are
the dynamical counterpart of chemical organization
theory~\citep{dittrich2007cot}, and the designed progression sits
in the network-expansion territory of~\citet{handorf2005network}.
This subsection benchmarks the dynamical closure test against both
structural instruments on the same iJO1366 model.

\begin{proposition}[Structural-instrument benchmark (E14)]
\label{prop:e14-structural}
With the network-expansion (NE) scope computed from the
glucose-minimal-medium seed ($18$ extracellular metabolites;
iterative expansion converges in $3$ rounds to a scope of $45$
metabolites, expansion factor $2.50\times$) and the largest
chemical organization (COT) computed on the central-carbon
subnetwork ($28$ cytosolic metabolites, $14$ reactions; the
largest closed set is the full $28$ and is self-maintaining by LP
feasibility), the $50$-metabolite dynamical closure-test record
($28$ causally internal, $22$ homeostatic) compares as follows.
Of the $28$ dynamically internal metabolites, $0$ are in the NE
scope and $19$ are outside the COT organization (the discriminative
cases: versus NE, all $28$, e.g.\ \texttt{g6p\_c},
\texttt{pep\_c}, \texttt{pyr\_c}, \texttt{accoa\_c},
\texttt{cit\_c}; versus COT, $19$, e.g.\ \texttt{25drapp\_c},
\texttt{2ahbut\_c}, \texttt{h2mb4p\_c}, \texttt{skm\_c},
\texttt{xmp\_c}). Agreement with the dynamical verdict: $0.440$
(NE), $0.600$ (COT). The dynamical closure test identifies as
causally internal metabolites that both structural instruments
miss --- the cases the external novelty assessment explicitly
asked for, in which the dynamical test separates systems the
structural tests cannot.
\end{proposition}

\begin{proof}
Direct computation (deposited artifacts): the NE scope and the COT
largest organization are computed on the deposited model files;
the dynamical verdicts are the deposited closure-test records; the
cross-tabulations, agreement statistics, and discriminative-case
lists are the deposited benchmark outputs.
\end{proof}""",
    "Keio closure (E12/E15/E16) + E14 structural benchmark subsections")

# rem:network-battery-reading: two arms -> three arms.
rep(r"""\begin{remark}[What the two arms establish together]
\label{rem:network-battery-reading}
The designed progression establishes sensitivity: each flagged
failure is converted by exactly the modification that repairs the
named cascade, so the test localizes the missing closure rather
than merely scoring networks. The fixed-model arm establishes
external validity: on a model no one modified for the purpose, the
dynamical dependency structure predicts independently computed
essentiality at $\kappa=0.835$. Neither arm alone would carry the
conclusion; together they anchor the closure-test language of
Sections~\ref{sec:savgs} and~\ref{sec:hott} in executed
computations.
\end{remark}""",
    r"""\begin{remark}[What the three arms establish together]
\label{rem:network-battery-reading}
The designed progression establishes sensitivity: each flagged
failure is converted by exactly the modification that repairs the
named cascade, so the test localizes the missing closure rather
than merely scoring networks. The fixed-model arm establishes
internal cross-validity: on a model no one modified for the
purpose, the dynamical dependency structure predicts independently
computed essentiality at $\kappa=0.835$ (with the threshold
provenance of Remark~\ref{rem:ijo-threshold}). The external anchor
carries the outside information: transitive validation against the
Keio collection at held-out ROC AUC $0.953$, a significant direct
rank-level association against the raw screen, an honestly
reported non-transfer across rebuilds, and the structural-instrument
benchmark. No arm alone would carry the conclusion; together they
anchor the closure-test language of
Sections~\ref{sec:savgs} and~\ref{sec:hott} in executed
computations.
\end{remark}""",
    "Keio: battery reading remark extended to three arms")

# =====================================================================
# C8: count-hygiene column in tab:network-battery.
# =====================================================================
rep(r"""\caption{The network battery. Phase~I is the fraction of essential
components causally internal at the endpoint-only criterion;
Phase~III is the pathwise, univalence-corrected criterion of
Definition~\ref{def:autopoiesis-phase3}. Each designed step adds
one redundant isozyme pair breaking the named cascade.}
\label{tab:network-battery}
\footnotesize
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}} l l l l l}
\toprule
Network & Description & Phase~I & Phase~III \\
\midrule
A & Hordijk--Steel RAF (anchor) & $2/5$ & $2/5$ \\
B & \emph{E.~coli} core metabolism (anchor) & $0/10$ & $0/10$ \\
C & B's metabolites in full iJO1366 & $9/10$ & $9/10$ \\
D & B + enzyme synthesis (MR--GR) & $5/17$ & $5/17$ \\
E & closed MR--GR network & $24/29$ & $24/29$ \\
F & E + ALT3/4 (ASP--PYR route) & $29/31$ & $29/31$ \\
G & F + ALT5/6 ($\alpha$KG route) & $41/42$ & $41/42$ \\
H & G + ASPAT3/4 (ASP cascade) & $43/44$ & $44/44$ \\
I & H + ALT7/8 (ALA reversible) & $45/46$ & $46/46$ \\
J & I + ALDO3/4 (FBP reversible) & $49/50$ & $49/50$ \\
K & J + ACS1/2 (NAD$^{+}$-independent) & $52/52$ & $52/52$ \\
\bottomrule
\end{tabular*}
\end{table}""",
    r"""\caption{The network battery. Phase~I is the fraction of essential
components causally internal at the endpoint-only criterion;
Phase~III is the pathwise, univalence-corrected criterion of
Definition~\ref{def:autopoiesis-phase3}. Each designed step adds
one redundant isozyme pair breaking the named cascade. The last
column disambiguates the counts: the Phase~I failing components
and their mode (lc = limit-cycle oscillation, converted by
Phase~III; res.\ = residual oscillation, not converted), traced to
the deposited per-component verdict records.}
\label{tab:network-battery}
\footnotesize
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}} l l l l l}
\toprule
Network & Description & Phase~I & Phase~III & Phase~I failures \\
\midrule
A & Hordijk--Steel RAF (anchor) & $2/5$ & $2/5$ & $d,e,g$ (catalyst-fragile) \\
B & \emph{E.~coli} core metabolism (anchor) & $0/10$ & $0/10$ & all $10$ \\
C & B's metabolites in full iJO1366 & $9/10$ & $9/10$ & FBP \\
D & B + enzyme synthesis (MR--GR) & $5/17$ & $5/17$ & $12$ components \\
E & closed MR--GR network & $24/29$ & $24/29$ & G6P, PYR, AcCoA, ALA, ASP \\
F & E + ALT3/4 (ASP--PYR route) & $29/31$ & $29/31$ & FBP, PYR \\
G & F + ALT5/6 ($\alpha$KG route) & $41/42$ & $41/42$ & AcCoA (lc, not conv.) \\
H & G + ASPAT3/4 (ASP cascade) & $43/44$ & $44/44$ & ALA (lc, conv.) \\
I & H + ALT7/8 (ALA reversible) & $45/46$ & $46/46$ & FBP (lc, conv.) \\
J & I + ALDO3/4 (FBP reversible) & $49/50$ & $49/50$ & AcCoA (res., not conv.) \\
K & J + ACS1/2 (NAD$^{+}$-independent) & $52/52$ & $52/52$ & --- \\
\bottomrule
\end{tabular*}
\end{table}""",
    "C8: count-hygiene column in tab:network-battery")

# =====================================================================
# C1: delegation-status framing (status line + relation paragraph).
# =====================================================================
rep(r"""\emph{Status: standalone theory paper; the application paper
\citep{zai2026measure} cites it for constructions and proofs.}""",
    r"""\emph{Status: standalone theory paper; the application paper
\citep{zai2026measure} cites it for constructions, machine
verifications, and proofs at the status marked per result.}""",
    "C1: status line delegation qualifier")

rep(r"""The application paper states the load-bearing definitions
of the present framework in brief, adapted form and cites this
paper for the constructions and proofs; the present paper develops
the full categorical machinery and cites the application paper
where the empirical line is concerned.""",
    r"""The application paper states the load-bearing definitions
of the present framework in brief, adapted form and cites this
paper for the constructions, machine verifications, and proofs at
the status marked per result --- complete proofs for the gluing
formula, the Fisher-minimal transport law, the composition and
contraction layers, and the terminal-coalgebra theorem;
machine-verified statements for the numerics; citation-level
reduction for the stratified descent; proof-sketch status, marked
as such, for the homotopy-type-theoretic extension. The present
paper develops the full categorical machinery and cites the
application paper where the empirical line is concerned.""",
    "C1: relation paragraph delegation qualifier")

# =====================================================================
# C5: regime-delineation bridging remark (companion side).
# =====================================================================
rep(r"""This is
the regime verified numerically in
Remark~\ref{rem:2cat-gluing-numeric} (boundary reset linear in the
wall coordinate with slope $\varepsilon$, the loop width).
\end{proof}""",
    r"""This is
the regime verified numerically in
Remark~\ref{rem:2cat-gluing-numeric} (boundary reset linear in the
wall coordinate with slope $\varepsilon$, the loop width).
\end{proof}

\begin{remark}[Regime delineation with the application paper]
\label{rem:regime-delineation}
The two holonomy-scaling regimes are complementary, and the pair of
papers states both. Loops contained in a single constant-active-set
stratum accumulate curvature at $O(\varepsilon^{2})$ per loop ---
the smooth arm, where the companion's quadratic law
$\kappa(a)=a^{2}$ and the Fisher-minimal transport law live.
Loops that cross a constraint-switching wall accumulate the
boundary contribution at $O(\varepsilon)$ per crossing (Theorem~%
\ref{thm:stratified-holonomy}) --- the wall-crossing arm, which the
application paper's regime dichotomy measures as the
piecewise-affine slope $1.00$ against the smooth arm's $2.000$.
\end{remark}""",
    "C5: regime-delineation remark after the pairs-crossing proof")

open(F, "w").write(src)
print(f"\npart C complete: {n_applied} edits (in place)")
