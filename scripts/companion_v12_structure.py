#!/usr/bin/env python3
"""companion_v12_structure.py -- build companion_categorical_v12.tex (NEW
versioned file; v11 and all earlier versions untouched): the targeted
structural re-alignment round for the companion, answering the user's
question "does the companion merit similar structural re-alignment ...
for clarity, comprehension and human understanding?"

Diagnosis implemented here (evidence in the worklog):
  1. Abstract carried the EIC-flagged defects: opening sentence
     fragment ("When adaptive systems navigate ... to remain viable." --
     no main verb), telegraphic "Four pillars.", a fragment in pillar
     (iv) ("... proof-sketch status marked."), a vague gloss ("measuring
     the accumulation through policy holonomy" -- accumulation of
     what?), and two >40-word semicolon run-ons.
  2. No plan-of-the-paper paragraph: 14 sections, 76 pp, and the
     contributions list maps only 7 of 13 content sections (5, 8, 9, 11,
     13 unmapped). Landmark digest principle 12 (Orth; Baez-Stay): end
     of introduction = one paragraph describing what each section does.
  3. Two colliding "sevens" (seven optic bridges vs seven hierarchy
     claims A-G) never disambiguated.
  4. Two experimental sections (verdicts; network battery) in a theory
     paper without a framing sentence for why computation belongs here.

Scope deliberately NOT touched: section order (logical: core theory ->
composition -> verification -> extensions -> benchmarks; reordering 76
pp with ~200 cross-refs is high risk for low gain), titles, theorems,
proofs, numbers, proof-status conventions.

Anchored splices:
  A. header: filename line -> v12 + V12 round note
  B. abstract: full-block replacement (fragment repairs, run-on splits,
     gloss of the vague phrase) -- must stay < 265 words under the
     audit's own counter and keep the six-axis sentence tokens
  C. plan-of-the-paper paragraph inserted after Status conventions
  D. sec:verdicts lead: experiment-framing sentence inserted
  E. sec:network-battery lead: experiment-framing sentence inserted
  F. \\bibliography{companion_refs_v11} -> v12 + byte-identical bib copy
"""
import re, shutil

BASE = "/home/z/my-project/metabolic-curvature-measure"
SRC = f"{BASE}/scripts/companion_categorical_v11.tex"
DST = f"{BASE}/scripts/companion_categorical_v12.tex"

tex = open(SRC, encoding="utf-8").read()
orig = tex
applied = []


def rep(old, new, tag):
    global tex
    assert old in tex, f"ANCHOR NOT FOUND: {tag}"
    assert tex.count(old) == 1, f"ANCHOR NOT UNIQUE: {tag}"
    tex = tex.replace(old, new)
    applied.append(tag)


# ---- A. header ----------------------------------------------------------
rep("%  companion_categorical_v11.tex -- standalone theory paper.",
    "%  companion_categorical_v12.tex -- standalone theory paper.",
    "A0 header filename line")

rep("""%  V11 alignment round (v10 -> v11): two cross-paper sentences
%              updated to the v19 division of labor (intro
%              "Relation to the application paper" paragraph and the
%              future-directions discretization-bridge item); every
%              numerical claim, theorem, proof, and section
%              unchanged; companion_refs_v11.bib byte-identical.""",
    """%  V11 alignment round (v10 -> v11): two cross-paper sentences
%              updated to the v19 division of labor (intro
%              "Relation to the application paper" paragraph and the
%              future-directions discretization-bridge item); every
%              numerical claim, theorem, proof, and section
%              unchanged; companion_refs_v11.bib byte-identical.
%  V12 comprehension round (v11 -> v12): abstract fragment repair
%              (the opening fragment, the telegraphic "Four
%              pillars.", the pillar-(iv) fragment; run-on splits),
%              a plan-of-the-paper paragraph added at the end of the
%              introduction (mapping all sections, disambiguating the
%              two sevens), and one experiment-framing sentence in
%              each of the two computational sections (verdicts,
%              network battery); every theorem, proof, number, and
%              section order unchanged; companion_refs_v12.bib
%              byte-identical.""",
    "A1 header V12 round note")

# ---- B. abstract: full-block replacement -------------------------------
NEW_ABSTRACT = r"""\textbf{Abstract.} Adaptive systems survive fluctuating
environments by continuously adjusting their internal strategies.
While individual adaptations seem safe, a sequence of
individually harmless adjustments can push a system into failure
when the environmental shifts occur in a non-commuting order. We
develop the geometric and category-theoretic framework that defines
and quantifies this phenomenon: \emph{viability-weighted
curvature}, the viability loss a closed loop accumulates
through policy holonomy. The theory has four pillars.
(i)~The \emph{SAVGS architecture} unifies control base, Fisher--Rao
policy bundle, viability margin, maintenance graph, and
$2$-categorical boundary span into one stratified bundle.
(ii)~The $2$-category $\mathbf{StCon}(B)$ of stratified connections
carries a lax-functorial gluing theorem and a piecewise-holonomy
formula, with boundary resets at their true order for transversal
wall-crossing loops in \emph{pairs}. Each stratum carries the
Fisher-minimal transport law (KKT projection) as connection, and
the small-loop theorem bounds endpoint erosion of a viability
margin by the viability-weighted curvature.
(iii)~A single composition theorem types seven bridges as optics,
with per-optic Lipschitz constants and a Banach contraction of the
Krasnoselskii--Mann-averaged update; the projected CPTP contraction
settles the Zeno self-reference.
(iv)~The filtered-colimit construction of RAF sets is proved at Set
level with the adapter-level optic statement, verified at scale;
the $\infty$-categorical extension in homotopy type theory carries
marked proof-sketch status. The validation battery is
robust across six axes: carbon, oxygen, nitrogen, phosphate, and iron
supply plus non-medium maintenance stress leave labels invariant,
re-stratifying only at regime switches. The association is invariant under
canonical flux selection, the declared tie-break closing its
near-degeneracy boundary. The application paper develops the atomic
curvature measure and its genome-scale validation."""

start = tex.index("\\textbf{Abstract.}")
end = tex.index("\\par", start)
tex = tex[:start] + NEW_ABSTRACT + tex[end:]
applied.append("B abstract full-block replacement")

# ---- C. plan-of-the-paper paragraph -------------------------------------
PLAN = r"""
\paragraph{Plan of the paper.}
Section~\ref{sec:prelim} states the preliminaries one definition at
a time, none used before it is stated.
Sections~\ref{sec:savgs}--\ref{sec:noether} develop the core
geometric theory: the SAVGS architecture, the $2$-category
$\mathbf{StCon}(B)$ with its gluing theorem and piecewise-holonomy
formula, the Fisher-minimal transport law, the viability-weighted
curvature, and the Bregman--Noether correspondence.
Section~\ref{sec:hierarchy} organizes the framework's predictions
into a seven-claim falsification hierarchy.
Sections~\ref{sec:composition}--\ref{sec:lipschitz} develop the
optic-composition semantics: seven domain bridges typed as optics,
per-optic Lipschitz constants, and the Banach contraction of the
composed update; Section~\ref{sec:smooth-envelope} then constructs
the smooth envelope of the algorithmic rate-distortion surrogates
that its observables require. Section~\ref{sec:verdicts} executes
the falsification battery computationally --- experiments appear in
this theory paper because each claim is quantitative, so its
refutation is a terminating computation.
Sections~\ref{sec:invlim} and~\ref{sec:terminal-coalgebra}
construct autocatalytic (RAF) sets by filtered colimits and
characterize the maximal one as a terminal coalgebra.
Section~\ref{sec:hott} extends the composition to
$\infty$-categories in homotopy type theory and defines the
three-phase closure test; Section~\ref{sec:network-battery}
benchmarks that test on biochemical networks, in the same
computational spirit. Section~\ref{sec:conclusion} states the four
load-bearing conclusions, and Section~\ref{sec:future} collects
the open problems. Two distinct sevens appear in the paper: the
seven forward maps typed as optics in the composition theorem, and
the seven claims A--G of the falsification hierarchy.
"""
rep("""Open
problems are collected in Section~\\ref{sec:future}.

\\section{Preliminaries}\\label{sec:prelim}""",
    """Open
problems are collected in Section~\\ref{sec:future}.
""" + PLAN + """
\\section{Preliminaries}\\label{sec:prelim}""",
    "C plan-of-the-paper paragraph")

# ---- D. sec:verdicts framing sentence -----------------------------------
rep("""The falsification hierarchy of Definition~\\ref{def:hierarchy} is
cumulative, and the recommended test ordering places the cheap
foundational tests first (Remark~\\ref{rem:ordering}). This section
reports the executed test battery, in that order:""",
    """The falsification hierarchy of Definition~\\ref{def:hierarchy} is
cumulative, and the recommended test ordering places the cheap
foundational tests first (Remark~\\ref{rem:ordering}). The
experiments below are computations, not observations: each claim is
quantitative, so its refutation is a terminating computation, and
executing it doubles as machine verification of the constants the
theorems assert. This section reports the executed test battery, in
that order:""",
    "D sec:verdicts framing sentence")

# ---- E. sec:network-battery framing sentence ----------------------------
rep("""The three-phase closure test (Definitions~\\ref{def:autopoiesis}
and~\\ref{def:autopoiesis-phase3}) is operationalized on a battery
of biochemical networks with two arms of distinct evidential roles.
The \\emph{designed progression} is a sequence of integrated""",
    """The three-phase closure test (Definitions~\\ref{def:autopoiesis}
and~\\ref{def:autopoiesis-phase3}) is operationalized on a battery
of biochemical networks with two arms of distinct evidential roles.
As in Section~\\ref{sec:verdicts}, the evidence is computational:
the test is a terminating algorithm, exercised here on designed
networks and anchored against one external dataset. The
\\emph{designed progression} is a sequence of integrated""",
    "E sec:network-battery framing sentence")

# ---- F. bibliography pointer --------------------------------------------
rep("\\bibliography{companion_refs_v11}",
    "\\bibliography{companion_refs_v12}",
    "F bibliography pointer")

# ---- verification --------------------------------------------------------
# 1. audit's abstract word counter (replicated exactly from audit_v28)
_m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", tex, re.S)
_body = re.sub(r"\\[a-zA-Z]+", " ", _m.group(1))
_body = re.sub(r"[\\${}~]", " ", _body)
nwords = len([w for w in _body.split() if w != "---"])
assert nwords < 265, f"ABSTRACT OVER CAP: {nwords} words (cap < 265)"

# 2. six-axis sentence tokens must remain (audit N-17 gate)
assert "carbon, oxygen, nitrogen," in tex
assert "non-medium maintenance stress" in tex

# 3. audit tokens / numbers unchanged
for t in ["0.498", "0.853", "+0.395", "424", "-0.083", "366",
          "zai2026measure", "prop:keio-o2-limited", "rem:keio-o2-invariance",
          "prop:keio-n-source", "rem:keio-n-invariance"]:
    assert tex.count(t) == orig.count(t), f"TOKEN COUNT CHANGED: {t}"

# 4. plan paragraph references every content section label
for lbl in ["sec:prelim", "sec:savgs", "sec:noether", "sec:hierarchy",
            "sec:composition", "sec:lipschitz", "sec:smooth-envelope",
            "sec:verdicts", "sec:invlim", "sec:terminal-coalgebra",
            "sec:hott", "sec:network-battery", "sec:conclusion",
            "sec:future"]:
    assert f"\\ref{{{lbl}}}" in tex, f"PLAN PARAGRAPH MISSING LABEL: {lbl}"

# 5. fragments gone
assert "When adaptive systems navigate" not in tex
assert "\nFour pillars.\n" not in tex
assert "proof-sketch status marked. The validation battery" not in tex

# 6. no accidental damage: diff hunk count
import difflib
diff = list(difflib.unified_diff(orig.splitlines(), tex.splitlines(),
                                 "v11", "v12", lineterm="", n=0))
hunks = sum(1 for l in diff if l.startswith("@"))

open(DST, "w", encoding="utf-8").write(tex)
shutil.copyfile(f"{BASE}/scripts/companion_refs_v11.bib",
                f"{BASE}/scripts/companion_refs_v12.bib")

print("[companion_v12_structure] splices:", "; ".join(applied))
print(f"[companion_v12_structure] abstract words: {nwords} (< 265 cap)")
print(f"[companion_v12_structure] diff hunks: {hunks}")
print(f"[companion_v12_structure] wrote {DST} + companion_refs_v12.bib (byte-identical)")
print("[companion_v12_structure] ALL CHECKS PASSED")
