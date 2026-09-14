#!/usr/bin/env python3
"""Update cover letters + links doc for the glucose-only/T7 round
(companion 63->65 pp; audit v5 110/110; the re-run + bridge closures)."""
import io

# ---------------------------------------------------------------- TAC letter
p = "download/cover_letter_tac.md"
t = io.open(p, encoding="utf-8").read()
old = ("closure test, its external anchor on the Keio\n"
       "   single-gene-deletion collection (transitive, direct, and\n"
       "   cross-rebuild arms), and a benchmark against the structural\n"
       "   closure instruments of chemical-organization theory and network\n"
       "   expansion.")
new = ("closure test; its external anchor on the Keio\n"
       "   single-gene-deletion collection (transitive, direct, and\n"
       "   cross-rebuild arms, with a disclosed medium audit and its\n"
       "   glucose-only re-run: both in-silico essentiality sets invariant,\n"
       "   every rank-level association strengthened, and the negative\n"
       "   cross-rebuild verdict reversed as a medium artifact); its\n"
       "   viability-kernel reading as a finite-time, feedback-certifying\n"
       "   probe of kernel and capture-basin membership (with the Nagumo\n"
       "   tangentiality condition); the Poincare/averaging analysis of its\n"
       "   pathwise levels (the occupation fraction as a phase-invariant\n"
       "   orbit statistic); and a benchmark against the structural\n"
       "   closure instruments of chemical-organization theory and network\n"
       "   expansion.")
assert t.count(old) == 1
t = t.replace(old, new)
io.open(p, "w", encoding="utf-8").write(t)
print("cover_letter_tac.md updated")

# ---------------------------------------------------------------- links doc
p = "download/SUBMISSION_PACKAGE_LINKS.md"
t = io.open(p, encoding="utf-8").read()
fixes = [
    ("`companion_categorical_v3.tex` (63 pp)",
     "`companion_categorical_v3.tex` (65 pp)"),
    ("(Research Article; 63 pp; electronic-only, free — no author charges)",
     "(Research Article; 65 pp; electronic-only, free — no author charges)"),
    ("| Manuscript PDF (63 pp, 3rd-wave repair revision: the eight-item "
     "repair set, the six restored citations, and the Keio/COT-NE "
     "external closures, on top of the restoration revision) |",
     "| Manuscript PDF (65 pp, 3rd-wave repair + glucose-only re-run "
     "revision: the eight-item repair set, the six restored citations, "
     "the Keio/COT-NE external closures, the medium-corrected "
     "glucose-only Keio re-run, and the viability-kernel + "
     "Poincare/averaging bridges, on top of the restoration revision) |"),
    ("association_robustness/. Main now 28 pp, companion 63 pp; both",
     "association_robustness/. Main now 28 pp, companion 65 pp; both"),
    ("the v4 audit passes\n98/98;",
     "the v5 audit passes\n110/110 (the v4 audit's 98 plus the 12 new "
     "Keio-section checks);"),
    ("ZIPs rebuilt as the v4 round and standalone-reverified (28 / 63\npp).",
     "ZIPs rebuilt as the v4 round and standalone-reverified (28 / 65\npp).\n\n"
     "Follow-up round (same files, amended in place on the live heads;\n"
     "frozen lineage untouched): the glucose-only Keio re-run executed\n"
     "with the trehalose exchange closed as the sole change — both\n"
     "in-silico essentiality sets unchanged (289/1367 and 286/1516, zero\n"
     "label changes), every rank-level association strengthened (E12\n"
     "Pearson 0.370→0.603, held-out AUC 0.953→0.977, MCC 0.719→0.882;\n"
     "E15 Pearson 0.085→0.230, AUC 0.713→0.737), and the E16\n"
     "cross-rebuild negative verdict reversed as a medium artifact\n"
     "(Pearson −0.018→+0.376, AUC 0.428→0.813) — plus the T7b\n"
     "viability-kernel bridge (closure test as a finite-time,\n"
     "feedback-certifying probe of kernel/capture-basin membership) and\n"
     "the T7c Poincare/averaging bridge (occupation fraction as a\n"
     "phase-invariant orbit statistic); companion 63→65 pp, 0 errors/0\n"
     "undefined/0 overfull; audit_v5 110/110 PASS; new artifacts\n"
     "download/keio_glucose_only_e12/e15/e16 (csv/txt/json/png)."),
]
for old, new in fixes:
    assert t.count(old) == 1, f"anchor not unique: {old[:60]}"
    t = t.replace(old, new)
    print("links fixed:", old[:48].replace("\n", " "))
io.open(p, "w", encoding="utf-8").write(t)
print("SUBMISSION_PACKAGE_LINKS.md updated")
