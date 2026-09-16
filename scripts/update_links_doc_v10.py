#!/usr/bin/env python3
"""Update SUBMISSION_PACKAGE_LINKS.md for the v10 round (v7 main + v6 companion)."""
import re

PATH = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
src = open(PATH).read()

# 1) Header round description
src = src.replace(
    "Generated 2026-09-16 (formal-style completion + cross-citation\n"
    "authorship + v9 package round: journal_manuscript_v6 +\n"
    "companion_categorical_v5).",
    "Generated 2026-09-16 (reader-oriented prose revision + v10 package\n"
    "round: journal_manuscript_v7 + companion_categorical_v6).",
    1,
)

# 2) New revision note inserted before the formal-style note
new_note = """Revision note (2026-09-16, reader-oriented prose revision + v10
package round): new manuscript versions as separate files, prior
versions untouched -- scripts/journal_manuscript_v7.tex (main, BMB;
from v6) and scripts/companion_categorical_v6.tex (companion, TAC;
from v5). The revision is a style pass informed by a landmark-paper
study (Orth/Edwards-Palsson/Segre/Lewis/Baba/Mahadevan on the
metabolic side; Shannon, Baez-Stay, Baez-Fong, Leinster on the
formal side; digest at research/landmark_style_digest.md). Main: the
abstract now opens from the plain problem (piecewise-linear, not
smooth; all numbers kept, 248 words, within the 150-250 guideline);
the introduction's "object" paragraph glosses active set and strata
in words and a plan-of-the-paper paragraph is added; plain-language
openers precede the core definitions and follow the key displayed
equations; the Limitations paragraph is restructured from one
sentence into readable items; the "safe regime" remark is retitled.
Companion: the abstract opens from the plain problem (264 words,
under the 265-word cap, with the six-axis sentence and required
phrases intact); the introduction glosses policy/connection/holonomy
and optics at first use; one-sentence leads are added to the
Preliminaries, Noether, hierarchy, composition, and
filtered-colimit sections. All numerical claims unchanged:
audit_v15_numbers.py 301/301 PASS; builds: main 28 pp, companion
75 pp, zero undefined references; ZIPs rebuilt via
build_submission_zips_v10.sh with fresh-dir standalone tectonic
compiles verified (28/75 pp); cover letters retargeted (also: the
BMB letter's stale 98-check audit count corrected to 301, its
"rather than any smooth curvature" phrasing and
"replacing earlier total-variation claims" changelog phrasing made
factual, and the stale section 3.5 pointer corrected to 2.5).

"""
anchor = "Revision note (2026-09-16, formal-style completion + cross-citation"
src = src.replace(anchor, new_note + anchor, 1)

# 3) Main-paper table rows (v6 -> v7)
src = src.replace(
    "| Manuscript PDF (27 pp, full proofs in appendices, declarations in backmatter; "
    "formal-style completion: factual abstract statement, geometric-metric terminology, "
    "framework-object Discussion, Abaee cross-citation; prior versions retained as separate files) "
    "| [download/journal_manuscript_v6.pdf]",
    "| Manuscript PDF (28 pp, full proofs in appendices, declarations in backmatter; "
    "reader-oriented prose revision: plain-problem abstract, glossed definitions, "
    "plan of the paper, restructured Limitations; prior versions retained as separate files) "
    "| [download/journal_manuscript_v7.pdf]",
    1,
)
src = src.replace(
    "[download/journal_manuscript_v6.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v6.pdf)",
    "[download/journal_manuscript_v7.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v7.pdf)",
    1,
)
src = src.replace(
    "main/download/journal_manuscript_v6.pdf)",
    "main/download/journal_manuscript_v7.pdf)",
    1,
)
src = src.replace(
    "| LaTeX source | [scripts/journal_manuscript_v6.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v6.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v6.tex) |",
    "| LaTeX source | [scripts/journal_manuscript_v7.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v7.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v7.tex) |",
    1,
)
src = src.replace(
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v6_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v6_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v6_bmb_refs.tex) |",
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v7_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v7_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v7_bmb_refs.tex) |",
    1,
)
src = src.replace(
    "| BibTeX database | [scripts/journal_manuscript_v6_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v6_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v6_refs.bib) |",
    "| BibTeX database | [scripts/journal_manuscript_v7_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v7_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v7_refs.bib) |",
    1,
)
src = src.replace(
    "files, upload them together with `journal_manuscript_v6_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v7_bmb_refs.tex` and",
    1,
)
src = src.replace("the .tex now searches both the", "the .tex searches both the", 1)

# 4) Companion table rows (v5 -> v6)
src = src.replace(
    "| Manuscript PDF (74 pp; formal-style completion: earlier-drafts references and uncited prior-formulations framing removed, process vocabulary purged, designed-progression duplication deleted, Abaee cross-citation; prior versions retained as separate files) "
    "| [download/companion_categorical_v5.pdf]",
    "| Manuscript PDF (75 pp; reader-oriented prose revision: plain-problem abstract opening, glossed introduction, section leads; prior versions retained as separate files) "
    "| [download/companion_categorical_v6.pdf]",
    1,
)
src = src.replace(
    "[download/companion_categorical_v5.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/companion_categorical_v5.pdf)",
    "[download/companion_categorical_v6.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/companion_categorical_v6.pdf)",
    1,
)
src = src.replace(
    "main/download/companion_categorical_v5.pdf)",
    "main/download/companion_categorical_v6.pdf)",
    1,
)
src = src.replace(
    "| LaTeX source | [scripts/companion_categorical_v5.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_categorical_v5.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v5.tex) |",
    "| LaTeX source | [scripts/companion_categorical_v6.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_categorical_v6.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v6.tex) |",
    1,
)
src = src.replace(
    "| BibTeX database | [scripts/companion_refs_v5.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_refs_v5.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_refs_v5.bib) |",
    "| BibTeX database | [scripts/companion_refs_v6.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/companion_refs_v6.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_refs_v6.bib) |",
    1,
)

# 5) Audit line
src = src.replace(
    "PASS against journal_manuscript_v6.tex + companion_categorical_v5.tex;",
    "PASS against journal_manuscript_v7.tex + companion_categorical_v6.tex;",
    1,
)

open(PATH, "w").write(src)

# verify: no v6/v5 filenames remain in the current-package sections (lines 395-627)
lines = src.split("\n")
bad = [(i + 1, ln[:90]) for i, ln in enumerate(lines)
       if i + 1 >= 395 and ("journal_manuscript_v6" in ln or "companion_categorical_v5" in ln)]
print("remaining stale refs in package sections:", bad if bad else "NONE")
print("header:", lines[2][:80])
print("new note present:", "reader-oriented prose revision + v10" in src)
