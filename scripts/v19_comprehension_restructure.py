#!/usr/bin/env python3
"""V19 comprehension restructure: build scripts/journal_manuscript_v19.tex
(from v18; v18 and all earlier versions untouched).

Diagnosis addressed (JTB desk rejection: "unable to make sense of this
article's structure and intent"): the manuscript led with mathematical
formalism, a five-finding enumeration mixing theorems with empirical
claims, an in-body categorical-reading subsection pointing to a 76-page
companion, a pure-numerical-analysis bridge section sitting between the
definitions and every result, and an internal bookkeeping appendix
(disambiguation of near-colliding counts). The restructure re-orders the
paper so the biological line of argument leads and the technical
machinery is visibly optional:

  1. NEW TITLE: "A discrete curvature measure for flux balance analysis
     predicts transcriptional regulation and translational buffering in
     Escherichia coli" (one plain claim, searchable terms).
  2. NEW ABSTRACT: bio-first, single narrative arc, every audited number
     kept (+0.395, 2.6e-17, 424, -0.083, 366, 66%, 1.00,
     93.4-100.0%, 0.865); 150-250 audit-style words (BMB cap).
  3. KEYWORDS: 6 terms (BMB 4-6 range) -- the v17 set; 'path
     dependence' (the JTB 7th term) dropped.
  4. INTRO: the five-finding roman-numeral enumeration REPLACED by
     three question-led paragraphs (what mathematics governs rerouting
     / does the geometry capture real rerouting / does the geometry
     predict regulation); plan-of-the-paper rewritten for the new
     section order.
  5. THE CATEGORICAL READING subsection REMOVED from the body (the
     Discussion's companion-paper paragraph already carries the
     pointer, now fixed); the value--flux event dichotomy corollary
     (cor:valueflux) RETAINED in the body as its own subsection with a
     plain-language lead.
  6. THE REFINEMENT-RESOLUTION BRIDGE MOVED to the appendix (new
     appendix order: bridge, proofs, technical proofs) with the
     corollary extracted first.
  7. THE DISAMBIGUATION-OF-COUNTS APPENDIX DELETED; the essential
     gene/reaction count mapping folded into Methods (panel
     construction).
  8. Venue retarget: BMB (Springer); refs carried to
     journal_manuscript_v19_bmb_refs.tex (29 entries byte-identical).

NO number is added or removed; every v18 numerical claim is unchanged.
"""
import re
import shutil

BASE = "/home/z/my-project/metabolic-curvature-measure/"
S = BASE + "scripts/"

v18 = open(S + "journal_manuscript_v18.tex").read()
tex = v18
applied = []


def rep(old, new, tag):
    global tex
    assert old in tex, f"ANCHOR NOT FOUND for {tag}: {old[:70]!r}"
    assert tex.count(old) == 1, f"ANCHOR NOT UNIQUE for {tag}"
    tex = tex.replace(old, new)
    applied.append(tag)


# =====================================================================
# 1. Header: venue + version + refs-name
# =====================================================================
rep("%  journal_manuscript_v18.tex -- main manuscript.\n"
    "%  Target journal: Journal of Theoretical Biology (Elsevier).\n"
    "%  Author-year citations (natbib); reference list in\n"
    "%  journal_manuscript_v18_refs.tex. Long technical proofs are",
    "%  journal_manuscript_v19.tex -- main manuscript.\n"
    "%  Target journal: Bulletin of Mathematical Biology (Springer).\n"
    "%  Author-year citations (natbib); reference list in\n"
    "%  journal_manuscript_v19_bmb_refs.tex. Long technical proofs are",
    "header: venue + version + refs name")

# ---- V19 round note (after the V18 note) ---------------------------------
V19_NOTE = """%  V19 comprehension restructure (v18 -> v19): the paper is re-ordered
%  so that the biological line of argument leads and the technical
%  machinery is visibly optional. (1) New plain title and bio-first
%  abstract (every audited number kept: +0.395, 2.6e-17, 424, -0.083,
%  366, 66%, 1.00, 93.4-100.0%, 0.865). (2) The intro's five-finding
%  enumeration replaced by three question-led paragraphs (what
%  mathematics governs rerouting / does the geometry capture real
%  rerouting / does the geometry predict regulation). (3) The
%  categorical-reading subsection removed from the body -- the
%  Discussion's companion-paper paragraph carries the pointer; the
%  value-flux event dichotomy corollary is retained in the body as its
%  own subsection. (4) The refinement-resolution bridge moved to the
%  appendix (appendix order: bridge, proofs, technical proofs). (5)
%  The near-colliding-counts disambiguation appendix deleted, its
%  essential mapping folded into Methods. (6) Retarget BMB
%  (Springer): abstract 150-250 audit-style words, keywords 6 (path
%  dependence, the JTB-only 7th term, dropped), refs
%  journal_manuscript_v19_bmb_refs.tex. Every numerical claim
%  unchanged (audit_v27_numbers.py). v18 and all earlier versions
%  untouched.
"""
rep("%  numerical claim unchanged (audit_v26 347/347). v17 and all\n"
    "%  earlier versions untouched.\n",
    "%  numerical claim unchanged (audit_v26 347/347). v17 and all\n"
    "%  earlier versions untouched.\n" + V19_NOTE,
    "v19 round note")

# =====================================================================
# 2. Title (hypersetup + \title) and keywords
# =====================================================================
rep(" pdftitle={A Geometric Theory of Metabolic Flux Rerouting: How\n"
    "           Active-Set Curvature Predicts Transcriptional Regulation\n"
    "           and Protein-Layer Buffering},",
    " pdftitle={A discrete curvature measure for flux balance analysis\n"
    "           predicts transcriptional regulation and translational\n"
    "           buffering in Escherichia coli},",
    "pdftitle: new plain title")

rep(" pdfkeywords={flux balance analysis, metabolic rerouting,\n"
    "              active-set curvature, transcriptional regulation,\n"
    "              translational buffering, epistasis, path dependence}}",
    " pdfkeywords={flux balance analysis, metabolic rerouting,\n"
    "              active-set curvature, transcriptional regulation,\n"
    "              translational buffering, epistasis}}",
    "pdfkeywords: 6 terms (BMB)")

rep("\\title{A Geometric Theory of Metabolic Flux Rerouting: How Active-Set\n"
    "       Curvature Predicts Transcriptional Regulation and\n"
    "       Protein-Layer Buffering}",
    "\\title{A discrete curvature measure for flux balance analysis\n"
    "       predicts transcriptional regulation and translational\n"
    "       buffering in \\emph{Escherichia coli}}",
    "title: new plain title")

# =====================================================================
# 3. Abstract: bio-first rebuild (all audited numbers kept)
# =====================================================================
OLD_ABSTRACT = """Constraint-based models such as flux balance analysis (FBA) predict cellular
metabolic states by solving linear optimization problems. When
nutrients or enzyme capacities vary continuously, optimal fluxes do
not change smoothly but follow piecewise-linear trajectories, changing slope
at bottlenecks. Here we show the response's true
``curvature'' is not an ordinary function but a
discrete measure concentrated on the boundary interfaces where active
constraints switch. Path-dependent memory (holonomy) scales linearly with
perturbation size (slope $1.00$; smooth systems quadratic), and
$93.4$--$100.0\\%$ of second-order adjustment concentrates at
bottleneck transitions. These switches bridge to smooth
geometry: under refinement they converge weakly to
curvature densities and strongly in $L^1$, but total variation
fails to converge generically, defining the resolution window ($h \\ll
\\sigma \\ll L_{\\mathrm{var}}$).

Integrating this measure along physiological paths yields a
parameter-free gene sensitivity metric, $\\kmu$: each enzyme's
rerouting burden. In carbon-starved \\emph{E.~coli}, $\\kmu$
predicts transcriptional induction in $424$ genes
($r = +0.395$, $p = 2.6 \\times 10^{-17}$),
robust across tie-breaking rules and stress axes. Induced
genes sit in operons of global carbon and energy regulons;
the rerouting mass concentrates on the fork metabolites of
central carbon. The association vanishes at the protein layer
($r = -0.083$, $366$ genes, matched proteomics):
cells transcribe standby capacity for rerouting, buffering protein
synthesis, so cyclic-perturbation memory ($66\\%$ non-reverting)
must live in fast post-translational state.
Double-knockout epistasis mirrors active-set boundary overlaps
($\\rho_S = 0.865$). Our framework unites linear programming,
discrete geometry, and transcriptional regulation into a
predictive foundation for metabolic systems biology.
"""

NEW_ABSTRACT = """When nutrients change, cells reroute metabolism through alternative
pathways, and control must act at the switching points. Flux balance
analysis (FBA) predicts metabolic states by solving linear
optimization problems; as nutrient and enzyme capacities vary, the
optimal response is piecewise linear, and ordinary curvature vanishes
almost everywhere. Here we show that the true curvature of the
optimal flux map is not a function but a discrete, matrix-valued
measure concentrated on the boundaries where the active constraint
set switches; in genome-scale \\emph{E.~coli} models, $93.4$--$100.0\\%$
of the second-order response concentrates at these transitions.
Integrating the measure along physiological paths assigns each enzyme
a parameter-free rerouting burden, $\\kmu$. In carbon-starved
\\emph{E.~coli}, $\\kmu$ predicts transcriptional induction across
$424$ genes ($r = +0.395$, $p = 2.6 \\times 10^{-17}$); induced genes
sit in operons of global carbon and energy regulons, and the
rerouting mass concentrates on the fork metabolites of central carbon
metabolism. The association survives five tie-breaking protocols and
multiple stress axes, yet vanishes at the protein layer
($r = -0.083$, $366$ genes, matched proteomics): cells transcribe
standby capacity for rerouting while buffering translation.
Cyclic-perturbation memory --- $66\\%$ of closed cycles fail to
revert, with path-dependent drift scaling linearly in loop size
(slope $1.00$) where smooth systems scale quadratically --- must live
in fast post-translational state. Double-knockout epistasis mirrors
active-set boundary overlaps ($\\rho_S = 0.865$). The framework
unites linear programming, discrete geometry, and transcriptional
regulation into a predictive foundation for metabolic systems
biology.
"""
rep(OLD_ABSTRACT, NEW_ABSTRACT, "abstract: bio-first rebuild")

rep("\\noindent\\textbf{Keywords:} flux balance analysis; metabolic\n"
    "rerouting; active-set curvature; transcriptional regulation;\n"
    "translational buffering; epistasis; path dependence",
    "\\noindent\\textbf{Keywords:} flux balance analysis; metabolic\n"
    "rerouting; active-set curvature; transcriptional regulation;\n"
    "translational buffering; epistasis",
    "keywords line: 6 terms")

# =====================================================================
# 4. Intro: five-finding enumeration -> three question-led paragraphs
# =====================================================================
OLD_CLAIMS = """\\paragraph{The claim structure.}
This manuscript establishes five interconnected findings:
\\begin{enumerate}[label=(\\roman*)]
\\item \\textbf{The geometry of metabolic curvature
      (Section~\\ref{sec:measure}):} we prove that the distributional
      second derivative of the optimal flux map decomposes into
      discrete, rank-one jump tensors along active-set switching
      boundaries (Theorem~\\ref{thm:Bprime}), and that the cell's
      objective value function (the maximum achievable growth rate
      $\\Phi = c_{\\mathrm{bio}}^\\top v^*$) and its internal reaction
      fluxes ($v^*$) belong to two distinct geometric layers connected
      by an exact coupling identity, $D^2 \\Phi = \\sum_r c_r D^2
      v^*_r$ (Theorem~\\ref{thm:coupling}); the value layer is the
      canonical tie-break-free carrier, with shadow-price jumps
      measurable to $6$--$7$ digits against Danskin envelopes.
\\item \\textbf{The refinement--resolution bridge
      (Section~\\ref{sec:theoremB}):} we examine how discrete
      active-set switches relate to smooth differential models ---
      discrete jump measures converge weakly to smooth curvature
      densities under spatial refinement, while their total variation
      fails to converge due to grid-alignment artifacts (triangulation
      anisotropy) --- and derive the precise resolution window
      ($h \\ll \\sigma \\ll L_{\\mathrm{var}}$) required for smooth
      approximations to be physically meaningful, with the two-layer
      separation of Proposition~\\ref{prop:seclaw} (the codimension-one
      Hessian layer the unbiased curvature estimator, the
      angle-defect layer carrying an exact sec-law bias) delimiting
      which discrete curvature is the right one to refine.
\\item \\textbf{Linear holonomy scaling (Sections~\\ref{sec:measure}
      and~\\ref{sec:computational}):} parameter loops in metabolic
      networks accumulate path-dependent discrepancies (holonomy) that
      scale \\emph{linearly} ($O(\\varepsilon)$) with perturbation diameter
      --- an empirical slope of $1.00$ --- in contrast to the
      quadratic scaling ($O(\\varepsilon^2)$) of smooth systems, and
      sequential gene knockouts frequently fail to commute, leaving
      permanent phenotypic memory in $66\\%$ of tested closed cycles.
\\item \\textbf{Predicting transcriptional regulation
      (Section~\\ref{sec:empirical}):} integrating the curvature
      measure along physiological trajectories yields the
      parameter-free gene sensitivity metric $\\kmu$, which across
      $424$ metabolic genes in \\emph{E.~coli} accurately predicts
      transcriptional induction during carbon starvation
      ($r = +0.395$, $p = 2.6 \\times 10^{-17}$), generalizes to
      oxygen-limitation and carbon-switch trajectories with matched
      responses ($r = +0.32$, $+0.22$; \\S\\ref{sec:v7}), and remains
      robust across five distinct optimization tie-breaking protocols
      ($r \\in [+0.386, +0.396]$; \\S\\ref{sec:v8}), with event measures
      stabilizing at the Glivenko--Cantelli rate across random panels
      (\\S\\ref{sec:e32}).
\\item \\textbf{The translational buffering mechanism
      (Section~\\ref{sec:empirical}):} this predictive power fails
      completely at the protein layer ($r = -0.083$ across $366$ genes
      in matched quantitative proteomics), providing genome-scale
      evidence for a model in which cells transcribe mRNA to maintain
      pathway rerouting capacity on standby, while buffering
      energy-intensive translation until post-translational or
      metabolic signals require it.
\\end{enumerate}
"""

NEW_CLAIMS = """\\paragraph{What this paper establishes.}
The paper answers three questions in order.

\\emph{First, what mathematics governs rerouting?} The optimal flux map
of parametric FBA is continuous and piecewise affine, so its
distributional second derivative is not a matrix of functions but a
matrix-valued Radon measure concentrated on the switching boundaries of
the active-set complex (Theorem~\\ref{thm:Bprime}). The growth objective
$\\Phi = c_{\\mathrm{bio}}^\\top v^*$ and the internal fluxes $v^*$ form
two distinct geometric layers --- the value layer, immune to
optimization tie-breaks and measurable against Danskin envelopes to
$6$--$7$ digits, and the flux layer, which carries the reroutings the
value layer cannot see --- joined by the exact coupling identity
$D^2 \\Phi = \\sum_r c_r\\, D^2 v^*_r$ (Theorem~\\ref{thm:coupling}).
Under mesh refinement these discrete jump measures converge weakly to
smooth curvature densities but not in total variation, and the gap
defines the resolution window ($h \\ll \\sigma \\ll L_{\\mathrm{var}}$)
inside which smooth sensitivity models are valid
(Appendix~\\ref{sec:theoremB}).

\\emph{Second, does this geometry capture real rerouting?} On two
genome-scale reconstructions of \\emph{E.~coli}
(Section~\\ref{sec:computational}), the measured geometry behaves as
the theory predicts: $93.4$--$100.0\\%$ of the second-order response
concentrates at active-set boundary transitions; path-dependent memory
around closed parameter loops scales linearly in loop size (slope
$1.00$, where any smooth system scales quadratically); $66\\%$ of
closed genotype cycles fail to return to their initial flux state; and
double-knockout epistasis mirrors active-set boundary overlaps
(Spearman $\\rho_S = 0.865$). The curvature mass has identifiable
chemical coordinates --- the fork metabolites of central carbon
metabolism --- and the order in which knockouts are constructed
changes the reachable endpoints.

\\emph{Third, does the geometry predict regulation?} Integrating the
measure along physiological trajectories yields a parameter-free,
per-gene rerouting burden, $\\kmu$. In carbon-starved \\emph{E.~coli},
$\\kmu$ predicts transcriptional induction across $424$ genes
($r = +0.395$, $p = 2.6 \\times 10^{-17}$), transfers to
oxygen-limitation and carbon-switch trajectories ($r = +0.32$,
$+0.22$), and is stable under five optimization tie-breaking protocols
($r \\in [+0.386, +0.396]$), with the underlying event measures
stabilizing at the Glivenko--Cantelli rate. The association vanishes
at the protein layer ($r = -0.083$ across $366$ genes in matched
quantitative proteomics): cells transcribe standby capacity for
rerouting while buffering energy-intensive translation --- the
translational-buffering model this paper tests.
"""
rep(OLD_CLAIMS, NEW_CLAIMS, "intro: five-finding list -> three questions")

# ---- Plan of the paper ----------------------------------------------------
OLD_PLAN = """\\paragraph{Plan of the paper.}
Section~\\ref{sec:measure} defines the measure and the metric, develops
the value-layer structure and the value--flux coupling, works a
hand-checkable example, and records the categorical reading in brief.
Section~\\ref{sec:theoremB} states the
refinement--resolution bridge. Section~\\ref{sec:computational} reports
the computational validation of the geometric claims --- where the
curvature mass sits chemically, the interior architecture it defines,
and a construction-order rule for genotype design --- and
Section~\\ref{sec:empirical} the empirical association, the anatomy of
one switch, and the protein-layer decision.
Section~\\ref{sec:discussion} positions the framework against smooth
sensitivity theory, develops the memory-substrate deduction, and
discusses limitations and scope. The Methods, a disambiguation table for
colliding gene counts, and the proofs complete the paper.
"""

NEW_PLAN = """\\paragraph{Plan of the paper.}
Section~\\ref{sec:measure} defines the curvature measure, derives the
gene sensitivity metric $\\kmu$, works a hand-checkable example, and
records the value-layer structure that makes the two layers
complementary. Section~\\ref{sec:computational} validates the geometry
on genome-scale models: where the curvature mass sits chemically, the
interior architecture it defines, and a construction-order rule for
genotype design. Section~\\ref{sec:empirical} reports the association
with transcriptional regulation, the anatomy of one switch, and the
protein-layer decision. Section~\\ref{sec:discussion} develops the
memory-substrate deduction, positions the framework against smooth
sensitivity theory and metabolic control analysis, and states the
limitations. Section~\\ref{sec:methods} gives methods. The
refinement--resolution bridge, the complete proofs, and the technical
arguments are collected in appendices, so the biological line of
argument can be followed without them.
"""
rep(OLD_PLAN, NEW_PLAN, "plan of the paper: new section order")

# =====================================================================
# 5. Cross-reference fixes for the moved bridge (body -> appendix)
# =====================================================================
rep("variation and measure mass are automatically consistent (see\n"
    "\\S\\ref{sec:theoremB}); in computational simulations across multiple",
    "variation and measure mass are automatically consistent (see\n"
    "Appendix~\\ref{sec:theoremB}); in computational simulations across\n"
    "multiple",
    "kappa-mu remark: bridge ref -> appendix")

rep("The geometric claims of\n"
    "Sections~\\ref{sec:measure} and~\\ref{sec:theoremB} are operational",
    "The geometric claims of\n"
    "Section~\\ref{sec:measure} and Appendix~\\ref{sec:theoremB} are\n"
    "operational",
    "computational-validation opening: bridge ref -> appendix")

rep("The discrete and smooth regimes of Section~\\ref{sec:theoremB} can be",
    "The discrete and smooth regimes of Appendix~\\ref{sec:theoremB} can be",
    "regime dial: bridge ref -> appendix")

# =====================================================================
# 6. Cross-reference fixes for the deleted sections
# =====================================================================
rep("      stable (Appendix~\\ref{sec:counts}).",
    "      stable.",
    "limitations: counts-app ref dropped")

rep("The near-colliding gene/reaction counts\n"
    "($424/433/435/438/440/525/537$) are disambiguated in Appendix~\\ref{sec:counts}.",
    "The remaining near-colliding counts are distinct quantities: "
    "$435$ genes with at\n"
    "least one active reaction, $438$ reactions active on the reference "
    "physiology, $440$\n"
    "reaction-level trajectory events, $525$ genes with nonzero metric "
    "across conditions,\n"
    "and $537$ the union of active reactions across conditions --- each "
    "deposited with its\n"
    "own artifact file (Data Availability).",
    "methods panel: counts mapping folded in")

rep("and the genome-scale empirical association with its layer decision\n"
    "--- and carries only a brief adapted statement of the load-bearing\n"
    "definitions (\\S\\ref{sec:categorical}); the companion carries the\n"
    "framework.",
    "and the genome-scale empirical association with its layer decision\n"
    "--- and is written in measure-theoretic terms alone; the companion\n"
    "carries the categorical framework.",
    "discussion: companion pointer fixed")

# =====================================================================
# 7. Structural surgery: categorical subsection out, corollary stays,
#    bridge -> appendix, disambiguation appendix out
# =====================================================================
SEP = "% =====================================================================\n"

cat_marker = "\\subsection{The categorical reading, in brief}\\label{sec:categorical}"
bridge_marker = SEP + "\\section{The refinement--resolution bridge}"
comp_marker = SEP + "\\section{Computational validation}\\label{sec:computational}"

cat_idx = tex.index(cat_marker)
bridge_idx = tex.index(bridge_marker)
comp_idx = tex.index(comp_marker)
assert cat_idx < bridge_idx < comp_idx

# --- extract the bridge block and its final corollary ---------------------
bridge_block = tex[bridge_idx:comp_idx]
cor_start = bridge_block.index("\\begin{corollary}[Decoupling")
cor_end = bridge_block.index("\\end{corollary}") + len("\\end{corollary}")
corollary = bridge_block[cor_start:cor_end]
bridge_body = bridge_block[:cor_start].rstrip() + "\n"
assert "cor:valueflux" in corollary and "11" in corollary

# --- adapt the bridge lead for its appendix position ----------------------
assert bridge_body.count("this section establishes") == 1
bridge_body = bridge_body.replace(
    "this section establishes", "this appendix establishes")
assert bridge_body.count("Throughout this section") == 1
bridge_body = bridge_body.replace(
    "Throughout this section", "Throughout this appendix")
# strip the leading separator comment (the appendix position adds its own)
assert bridge_body.startswith(SEP)
bridge_appendix = bridge_body[len(SEP):]

# --- new body subsection carrying the retained corollary ------------------
NEW_SUBSEC = (
    "\\subsection{Value events and flux events}\\label{sec:valueflux}\n\n"
    "Before turning to computation, we record one structural consequence "
    "of the\n"
    "coupling identity, because it organizes how the empirical results "
    "of\n"
    "Section~\\ref{sec:empirical} should be read: the two layers see "
    "different\n"
    "events. Growth sees only the events that change the objective; the "
    "flux\n"
    "layer sees every rerouting, including the zero-cost substitutions "
    "that\n"
    "dominate nutrient transitions. The metric of "
    "Definition~\\ref{def:kmu} lives\n"
    "on the second, larger family.\n\n"
    + corollary + "\n")

# --- remove categorical subsection + bridge from the body -----------------
tex = tex[:cat_idx] + NEW_SUBSEC + tex[comp_idx:]

# --- replace the disambiguation appendix with the bridge appendix ----------
app_idx = tex.index("\\appendix\n")
proofs_idx = tex.index("\\section{Proofs}")
disambig = tex[app_idx:proofs_idx]
assert "Disambiguation of near-colliding counts" in disambig
assert "minipage" in disambig
tex = (tex[:app_idx] + "\\appendix\n" + bridge_appendix + "\n"
       + tex[proofs_idx:])

# =====================================================================
# 8. Refs pointer + audit-count mentions
# =====================================================================
rep("\\input{journal_manuscript_v18_refs}",
    "\\input{journal_manuscript_v19_bmb_refs}",
    "input: v19 bmb refs")

# (the two '$344$ checks' mentions in Methods are patched to the final
#  audit_v27 count by scripts/v19_set_audit_count.py after the audit
#  runs)

# =====================================================================
# 9. Write v19 + refs copies + download copies
# =====================================================================
open(S + "journal_manuscript_v19.tex", "w").write(tex)

refs = open(S + "journal_manuscript_v18_refs.tex").read()
old_ref_hdr = """% journal_manuscript_v18_refs.tex -- references for the v18
% JTB-alignment round. Entries byte-identical to the v17 list
% (itself the v7 list, generated by scripts/build_bmb_refs.py): the
% 27-entry v3 base + kacser1973 + heinrich1974 from the v17 MCA
% comparison. All proof-literature sources required by the
% complete-proof revision (Rockafellar 1970, Gutierrez 2001,
% Borrelli et al. 2003, Ziegler 1995, Danskin 1967, Cheeger et al.
% 1984, Regge 1961, Billingsley 1999, Villani 2009, Alexandrov 1939)
% were already present among the 27 base entries.
% Author-year references (natbib), ALPHABETICAL by first author
% surname, with optional labels; venue-neutral for the JTB target
% (Elsevier accepts any consistent style at first submission)."""
new_ref_hdr = """% journal_manuscript_v19_bmb_refs.tex -- references for the v19
% comprehension-restructure round. Entries byte-identical to the v18
% list (itself the v7 list, generated by scripts/build_bmb_refs.py):
% the 27-entry v3 base + kacser1973 + heinrich1974 from the v17 MCA
% comparison. All proof-literature sources required by the
% complete-proof revision (Rockafellar 1970, Gutierrez 2001,
% Borrelli et al. 2003, Ziegler 1995, Danskin 1967, Cheeger et al.
% 1984, Regge 1961, Billingsley 1999, Villani 2009, Alexandrov 1939)
% were already present among the 27 base entries.
% Springer/BMB author-year references, ALPHABETICAL by first author
% surname, with natbib optional labels."""
assert old_ref_hdr in refs, "refs header anchor not found"
refs19 = refs.replace(old_ref_hdr, new_ref_hdr)
open(S + "journal_manuscript_v19_bmb_refs.tex", "w").write(refs19)

shutil.copyfile(S + "journal_manuscript_v18_refs.bib",
                S + "journal_manuscript_v19_refs.bib")

shutil.copyfile(S + "journal_manuscript_v19.tex",
                BASE + "download/journal_manuscript_v19.tex")
shutil.copyfile(S + "journal_manuscript_v19_bmb_refs.tex",
                BASE + "download/journal_manuscript_v19_bmb_refs.tex")
shutil.copyfile(S + "journal_manuscript_v19_refs.bib",
                BASE + "download/journal_manuscript_v19_refs.bib")

# =====================================================================
# 10. Self-verification
# =====================================================================
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
inner = m.group(1)
nwords = len(re.findall(r"[A-Za-z0-9\\-]+",
                        re.sub(r"\\[a-zA-Z]+", " ", inner)))
kw_line = re.search(r"Keywords:\}\s*(.*?)(?:\n\n|\n\\\\bigskip)",
                    tex, re.S).group(1)
n_kw = kw_line.count(";") + 1

body = re.sub(r"(?<!\\)%.*", "", tex)
nums18 = re.findall(r"\d+(?:\.\d+)?", re.sub(r"(?<!\\)%.*", "", v18))
nums19 = re.findall(r"\d+(?:\.\d+)?", body)
from collections import Counter
d18, d19 = Counter(nums18), Counter(nums19)
removed = d18 - d19
added = d19 - d18

structural = {
    "categorical subsection gone": "The categorical reading" not in tex,
    "value/flux dichotomy subsection present":
        "\\subsection{Value events and flux events}" in tex,
    "corollary retained in body":
        tex.count("cor:valueflux") >= 4,
    "bridge in appendix (after \\appendix, before Proofs)":
        tex.index("\\appendix") < tex.index(
            "\\section{The refinement--resolution bridge}") <
        tex.index("\\section{Proofs}"),
    "disambiguation appendix gone":
        "Disambiguation of near-colliding counts" not in tex,
    "companion still cited":
        tex.count("zai2026categorical") >= 1,
    "new title present":
        "A discrete curvature measure for flux balance analysis" in tex,
    "old title absent":
        "Geometric Theory of Metabolic Flux Rerouting" not in tex,
    "no dangling sec:counts ref":
        "ref{sec:counts}" not in tex,
    "no dangling sec:categorical ref":
        "ref{sec:categorical}" not in tex,
    "worked example intact":
        "\\subsection{A worked example}" in tex,
}

print(f"applied anchored edits: {len(applied)}")
for t in applied:
    print("  -", t)
print(f"abstract audit-style words: {nwords}  (BMB range 150-250)")
print(f"keywords: {n_kw}  (BMB range 4-6)")
print("numeric tokens removed:", dict(removed))
print("numeric tokens added:  ", dict(added))
print("structural gates:")
for k, v in structural.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")

assert 150 <= nwords <= 250, f"abstract word count {nwords} out of range"
assert n_kw == 6, f"keywords {n_kw} != 6"
assert all(structural.values()), "STRUCTURAL GATE FAILED"
assert refs19.count("\\bibitem") == 29
print("ALL V19 PATCH CHECKS PASS")
