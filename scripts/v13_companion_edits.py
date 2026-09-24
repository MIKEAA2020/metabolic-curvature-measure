#!/usr/bin/env python3
"""V13 round: create companion_categorical_v13.tex + companion_refs_v13.bib
(from v12; v12 and all earlier versions untouched) -- F2 from the
causal-coherence/prose-alignment review + the Discover Applied
Mathematics venue alignment.

F2 (abstract-body misalignment, the six-axis sentence): the abstract's
clause "leave labels invariant, re-stratifying only at regime switches"
covered the body's categories (a) and (b) but silently dropped (c), the
nitrogen-source substitution losses, which the body (rem:keio-multiaxis
and the fourfold medium-robustness statement) classifies separately as
"the only re-wiring-driven losses" / "re-stratification confined to the
rewired module at a regime switch or source substitution". Fixed by
appending "and nitrogen-source substitution" to the abstract clause.

Venue alignment (Discover Applied Mathematics, abstract of less than
250 words): the 264-word abstract is trimmed to the DAM cap while
preserving every audited token ('robust across six axes', the
'carbon, oxygen, nitrogen,' list, 'non-medium maintenance stress') and
every number; natbib switched to numeric square-bracket citations;
keywords trimmed from 9 to 6 terms (the Springer 4-6 range); the
cross-citation zai2026measure now carries the application paper's
actual v20 title.

Every theorem, proof, number, section, table, and figure unchanged.
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(BASE, "scripts")

SRC = os.path.join(S, "companion_categorical_v12.tex")
DST = os.path.join(S, "companion_categorical_v13.tex")

text = open(SRC).read()
edits = []


def edit(old, new, label, count=1):
    global text
    found = text.count(old)
    assert found == count, f"{label}: expected {count}, found {found}"
    text = text.replace(old, new)
    edits.append(label)


# ------------------------------------------------------------------
# 0. Header: identity line + V13 round note + application pointer
# ------------------------------------------------------------------
edit("%  companion_categorical_v12.tex -- standalone theory paper.",
     "%  companion_categorical_v13.tex -- standalone theory paper.",
     "identity line")
edit("the application paper (journal_manuscript_v19.tex)",
     "the application paper (journal_manuscript_v20.tex)",
     "application-paper pointer -> v20")
edit(
    "%  V11 alignment round (v10 -> v11):",
    "%  V13 DAM round (v12 -> v13), a light touch-up: the six-axis\n"
    "%              abstract sentence gains the nitrogen-source-\n"
    "%              substitution qualifier (the review's F2: the\n"
    "%              body's rem:keio-multiaxis and the fourfold\n"
    "%              medium-robustness statement classify those\n"
    "%              losses separately from regime switches; the\n"
    "%              abstract clause now covers all three\n"
    "%              categories); the abstract trimmed to the\n"
    "%              Discover Applied Mathematics cap (248 < 250\n"
    "%              words, a one-word margin) with every audited\n"
    "%              token and number kept;\n"
    "%              numeric square-bracket citations (natbib);\n"
    "%              keywords 9 -> 6 terms (the Springer 4-6 range);\n"
    "%              the zai2026measure cross-citation title aligned\n"
    "%              to the application paper's actual v20 title.\n"
    "%              Every theorem, proof, number, and section\n"
    "%              unchanged; companion_refs_v13.bib (title\n"
    "%              alignment only).\n"
    "%  V11 alignment round (v10 -> v11):",
    "V13 round note inserted")

# ------------------------------------------------------------------
# 1. Venue: numeric citations
# ------------------------------------------------------------------
edit("\\usepackage[round]{natbib}",
     "\\usepackage[numbers,sort&compress,square]{natbib}",
     "natbib numeric square-bracket mode")

# ------------------------------------------------------------------
# 2. F2 + DAM cap: the abstract block
#    (F2 qualifier added; -17 tokens trimmed: 'continuously', the
#    'While individual adaptations seem safe' frame + 'the',
#    'that defines and quantifies' -> 'defining and quantifying',
#    'of a viability margin', 'with the adapter-level optic
#    statement'; all audited tokens and numbers intact)
# ------------------------------------------------------------------
edit(
    "\\textbf{Abstract.} Adaptive systems survive fluctuating\n"
    "environments by continuously adjusting their internal strategies.\n"
    "While individual adaptations seem safe, a sequence of\n"
    "individually harmless adjustments can push a system into failure\n"
    "when the environmental shifts occur in a non-commuting order. We\n"
    "develop the geometric and category-theoretic framework that defines\n"
    "and quantifies this phenomenon: \\emph{viability-weighted\n"
    "curvature}, the viability loss a closed loop accumulates\n"
    "through policy holonomy. The theory has four pillars.\n"
    "(i)~The \\emph{SAVGS architecture} unifies control base, Fisher--Rao\n"
    "policy bundle, viability margin, maintenance graph, and\n"
    "$2$-categorical boundary span into one stratified bundle.\n"
    "(ii)~The $2$-category $\\mathbf{StCon}(B)$ of stratified connections\n"
    "carries a lax-functorial gluing theorem and a piecewise-holonomy\n"
    "formula, with boundary resets at their true order for transversal\n"
    "wall-crossing loops in \\emph{pairs}. Each stratum carries the\n"
    "Fisher-minimal transport law (KKT projection) as connection, and\n"
    "the small-loop theorem bounds endpoint erosion of a viability\n"
    "margin by the viability-weighted curvature.\n"
    "(iii)~A single composition theorem types seven bridges as optics,\n"
    "with per-optic Lipschitz constants and a Banach contraction of the\n"
    "Krasnoselskii--Mann-averaged update; the projected CPTP contraction\n"
    "settles the Zeno self-reference.\n"
    "(iv)~The filtered-colimit construction of RAF sets is proved at Set\n"
    "level with the adapter-level optic statement, verified at scale;\n"
    "the $\\infty$-categorical extension in homotopy type theory carries\n"
    "marked proof-sketch status. The validation battery is\n"
    "robust across six axes: carbon, oxygen, nitrogen, phosphate, and iron\n"
    "supply plus non-medium maintenance stress leave labels invariant,\n"
    "re-stratifying only at regime switches. The association is invariant under\n"
    "canonical flux selection, the declared tie-break closing its\n"
    "near-degeneracy boundary. The application paper develops the atomic\n"
    "curvature measure and its genome-scale validation.\\par",
    "\\textbf{Abstract.} Adaptive systems survive fluctuating\n"
    "environments by adjusting internal strategies. Sequences of\n"
    "individually harmless adjustments can push a system into failure\n"
    "when environmental shifts occur in a non-commuting order. We\n"
    "develop the geometric and category-theoretic framework defining\n"
    "and quantifying this phenomenon: \\emph{viability-weighted\n"
    "curvature}, the viability loss a closed loop accumulates\n"
    "through policy holonomy. The theory has four pillars.\n"
    "(i)~The \\emph{SAVGS architecture} unifies control base, Fisher--Rao\n"
    "policy bundle, viability margin, maintenance graph, and\n"
    "$2$-categorical boundary span into one stratified bundle.\n"
    "(ii)~The $2$-category $\\mathbf{StCon}(B)$ of stratified connections\n"
    "carries a lax-functorial gluing theorem and a piecewise-holonomy\n"
    "formula, with boundary resets at their true order for transversal\n"
    "wall-crossing loops in \\emph{pairs}. Each stratum carries the\n"
    "Fisher-minimal transport law (KKT projection) as connection, and\n"
    "the small-loop theorem bounds endpoint erosion by the\n"
    "viability-weighted curvature.\n"
    "(iii)~A single composition theorem types seven bridges as optics,\n"
    "with per-optic Lipschitz constants and a Banach contraction of the\n"
    "Krasnoselskii--Mann-averaged update; the projected CPTP contraction\n"
    "settles the Zeno self-reference.\n"
    "(iv)~The filtered-colimit construction of RAF sets is proved at Set\n"
    "level, verified at scale; the $\\infty$-categorical extension in\n"
    "homotopy type theory carries marked proof-sketch status. The\n"
    "validation battery is\n"
    "robust across six axes: carbon, oxygen, nitrogen, phosphate, and iron\n"
    "supply plus non-medium maintenance stress leave labels invariant,\n"
    "re-stratifying only at regime switches and\n"
    "nitrogen-source substitution. The association is\n"
    "invariant under canonical flux selection, the declared tie-break\n"
    "closing its near-degeneracy boundary. The application paper\n"
    "develops the atomic curvature measure and its genome-scale\n"
    "validation.\\par",
    "F2 qualifier + DAM-cap trim (abstract block)")

# ------------------------------------------------------------------
# 3. Keywords: 9 -> 6 (Springer 4-6 range), pdfkeywords aligned
# ------------------------------------------------------------------
edit(
    " pdfkeywords={applied category theory, optic category, stratified\n"
    "              connection, 2-category, homotopy type theory,\n"
    "              information\n"
    "              geometry, holonomy, viability theory, autopoiesis}}",
    " pdfkeywords={applied category theory, optic category, stratified\n"
    "              connection, homotopy type theory, holonomy,\n"
    "              viability theory}}",
    "pdfkeywords 9 -> 6 terms")
edit(
    "\\noindent\\textbf{Keywords:} applied category theory; optic\n"
    "category; stratified connection; 2-category; homotopy type theory;\n"
    "information\n"
    "geometry; holonomy; viability theory; autopoiesis\\\\[0.3em]",
    "\\noindent\\textbf{Keywords:} applied category theory; optic\n"
    "category; stratified connection; homotopy type theory; holonomy;\n"
    "viability theory\\\\[0.3em]",
    "keywords 9 -> 6 terms")

# ------------------------------------------------------------------
# 4. Bibliography retarget
# ------------------------------------------------------------------
edit("\\bibliography{companion_refs_v12}",
     "\\bibliography{companion_refs_v13}",
     "bibliography retargeted")

with open(DST, "w") as f:
    f.write(text)

print(f"companion_categorical_v13.tex written ({len(edits)} anchored edits):")
for e in edits:
    print("  -", e)

# --- audit-style word count of the new abstract (3 audit counters) ---
_m = re.search(r"\\textbf\{Abstract\.\}(.*?)\\par", text, re.S)
_b = re.sub(r"\\[a-zA-Z]+", " ", _m.group(1))
_b = re.sub(r"[\\${}~]", " ", _b)
n_o215 = len([w for w in _b.split() if w != "---"])
print(f"\nNew abstract word count (audit-style): {n_o215} "
      f"(DAM cap: < 250)")
assert n_o215 < 250, f"abstract still over the DAM cap: {n_o215}"

# required tokens preserved
for tok in ["robust across six axes", "carbon, oxygen, nitrogen,",
            "non-medium maintenance stress", "nitrogen-source substitution"]:
    assert tok in text, f"token lost: {tok}"
print("All audited tokens present (robust across six axes / "
      "carbon, oxygen, nitrogen, / non-medium maintenance stress) "
      "+ F2 token added.")

# ==================================================================
# companion_refs_v13.bib (title alignment only)
# ==================================================================
SRC_B = os.path.join(S, "companion_refs_v12.bib")
DST_B = os.path.join(S, "companion_refs_v13.bib")
bib = open(SRC_B).read()
old_b = (
    "@misc{zai2026measure,\n"
    "  author = {Abaee, Amin},\n"
    "  title = {A Measure-Theoretic Discrete Curvature Framework for\n"
    "           Metabolic Gene Sensitivity: From Active-Set Geometry to\n"
    "           Transcriptional Response},")
new_b = (
    "@misc{zai2026measure,\n"
    "  author = {Abaee, Amin},\n"
    "  title = {A Discrete Curvature Measure for Flux Balance Analysis\n"
    "           Predicts Transcriptional Regulation in Escherichia coli},")
assert bib.count(old_b) == 1, "zai2026measure anchor"
bib = bib.replace(old_b, new_b)
with open(DST_B, "w") as f:
    f.write(bib)
print("companion_refs_v13.bib written (zai2026measure title aligned "
      "to the v20 application title; otherwise byte-identical).")
print("\nAll v13 companion files created. v12 and earlier untouched.")
