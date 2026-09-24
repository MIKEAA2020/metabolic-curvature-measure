#!/usr/bin/env python3
"""update_links_doc_v24.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
V12 companion-comprehension round + v24 package round: generation header,
newest-first revision note, companion package rows retargeted to
companion_categorical_v12 (PDF, LaTeX source, BibTeX), and the
pre-submission checklist updated (audit_v29, v24 ZIPs)."""

P = ("/home/z/my-project/metabolic-curvature-measure/download/"
     "SUBMISSION_PACKAGE_LINKS.md")
doc = open(P).read()
applied = []


def rep(old, new, tag):
    global doc
    assert old in doc, f"ANCHOR NOT FOUND: {tag}"
    assert doc.count(old) == 1, f"ANCHOR NOT UNIQUE: {tag}"
    doc = doc.replace(old, new)
    applied.append(tag)


# ---- 1. generation header -----------------------------------------------
rep("Generated 2026-09-24 (V11 companion-alignment round + v23 package\n"
    "round: journal_manuscript_v19 (unchanged) + companion_categorical_v11;\n"
    "supersedes the V19 comprehension-restructure + v22 package round).",
    "Generated 2026-09-24 (V12 companion-comprehension round + v24\n"
    "package round: journal_manuscript_v19 (unchanged) +\n"
    "companion_categorical_v12; supersedes the V11 companion-alignment +\n"
    "v23 package round).",
    "generation header")

# ---- 2. newest-first revision note (inserted before the V11 note) ------
V12_NOTE = """Revision note (2026-09-24, V12 companion-comprehension + v24 package
round, structural re-alignment of the companion): asked whether the
companion merits the same structural re-alignment the main paper
received after the JTB desk rejection, the diagnosis found four
defects of the same family (structure/intent/comprehension) and fixed
them on a NEW versioned file -- scripts/companion_categorical_v12.tex
(from v11; v11 and all earlier versions untouched) via
scripts/companion_v12_structure.py: (1) abstract fragment repair --
the opening sentence was a grammatical fragment ("When adaptive
systems navigate fluctuating environments, constantly adjusting
their internal strategies to remain viable." -- no main verb), the
pillar enumeration opened telegraphically ("Four pillars."), and
pillar (iv) ended in a fragment ("... proof-sketch status marked.");
two 40+-word semicolon run-ons were split and the vague gloss
"measuring the accumulation through policy holonomy" was made
explicit ("the viability loss a closed loop accumulates through
policy holonomy"); 264 words, under the 265 audit cap, with the
six-axis sentence and every audited token intact. (2) A
plan-of-the-paper paragraph was added at the end of the introduction
(the landmark-digest principle: end of introduction = one paragraph
describing what each section does) -- it maps all fourteen sections
and disambiguates the paper's two colliding "sevens" (the seven
forward maps typed as optics in the composition theorem vs the seven
claims A-G of the falsification hierarchy), which the contributions
list left unmapped (it covered only 7 of 13 content sections). (3)
One experiment-framing sentence in each computational section
(verdicts; network battery) stating why experiments appear in a
theory paper: each claim is quantitative, so its refutation is a
terminating computation. Deliberately NOT changed: section order
(theory -> composition -> verification -> extensions -> benchmarks is
logical, and reordering 76 pp with ~200 cross-references is high risk
for low gain), titles, theorems, proofs, numbers, proof-status
conventions, and the problem/obstruction/solution introduction
(already reader-oriented from the v6-v10 rounds). VERIFIED:
audit_v29_numbers.py 349/349 PASS (identical check set, companion
retargeted to v12); pattern_sweep_v16 16/16 clean; tectonic 76 pp,
0 errors / 0 '??'; v24 ZIPs (build_submission_zips_v24.sh) fresh-dir
verified 37/76 pp; main v19 UNCHANGED.

"""
V11_NOTE_HEAD = "Revision note (2026-09-24, V11 companion-alignment + v23 package"
rep(V11_NOTE_HEAD, V12_NOTE + V11_NOTE_HEAD, "newest-first revision note")

# ---- 3. companion package rows ------------------------------------------
rep(
    "| Manuscript PDF (76 pp; V11 companion-alignment round -- two "
    "cross-paper sentences updated to the v19 division of labor (the "
    "application paper is written in measure-theoretic terms alone and "
    "carries the relation as a Discussion-level pointer; the categorical "
    "definitions and the active-atom bridge are stated here alone); "
    "every theorem, proof, and number unchanged from v10 (audit_v28 "
    "349/349); clickable email and ORCID; prior versions retained as "
    "separate files) | "
    "[download/companion_categorical_v11.pdf]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v11.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "companion_categorical_v11.pdf) |",
    "| Manuscript PDF (76 pp; V12 companion-comprehension round -- "
    "abstract fragment repair, plan-of-the-paper paragraph mapping all "
    "sections with the two-sevens disambiguation, experiment-framing "
    "sentences in the two computational sections; every theorem, proof, "
    "and number unchanged from v11 (audit_v29 349/349); clickable email "
    "and ORCID; prior versions retained as separate files) | "
    "[download/companion_categorical_v12.pdf]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v12.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "companion_categorical_v12.pdf) |",
    "companion PDF row")

rep(
    "| LaTeX source | [scripts/companion_categorical_v11.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v11.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_categorical_v11.tex) |",
    "| LaTeX source | [scripts/companion_categorical_v12.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v12.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_categorical_v12.tex) |",
    "companion LaTeX source row")

rep(
    "| BibTeX database (V11: byte-identical copy of the v10 database; "
    "fixes this table's stale v9 pointer) | "
    "[scripts/companion_refs_v11.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v11.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_refs_v11.bib) |",
    "| BibTeX database (V12: byte-identical copy of the v11 database) | "
    "[scripts/companion_refs_v12.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v12.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_refs_v12.bib) |",
    "companion BibTeX row")

# ---- 4. pre-submission checklist -----------------------------------------
rep(
    "cover letters retargeted (TAC: v19 title + file pointer; BMB:\n"
    "companion v11 file pointer); audit_v28_numbers.py 349/349 PASS\n"
    "(identical check set to v27, companion retargeted to v11);\n"
    "pattern_sweep_v16 16/16; verify_v19_completeness ALL COMPLETE;\n"
    "tectonic main 37 pp / companion 76 pp, 0 errors / 0 '??';\n"
    "v23 ZIPs fresh-dir verified 37/76 pp. Earlier",
    "cover letters retargeted (TAC: v19 title + file pointer; BMB:\n"
    "companion v11 file pointer); companion V12 comprehension round:\n"
    "abstract fragment repair, plan-of-the-paper paragraph (all\n"
    "sections mapped, two sevens disambiguated), experiment-framing\n"
    "sentences in the two computational sections -- section order,\n"
    "theorems, proofs, and numbers untouched; audit_v29_numbers.py\n"
    "349/349 PASS (identical check set, companion retargeted to v12);\n"
    "pattern_sweep_v16 16/16; verify_v19_completeness ALL COMPLETE;\n"
    "tectonic main 37 pp / companion 76 pp, 0 errors / 0 '??';\n"
    "v24 ZIPs fresh-dir verified 37/76 pp. Earlier",
    "pre-submission checklist")

open(P, "w", encoding="utf-8").write(doc)
print("[update_links_doc_v24] applied:", "; ".join(applied))
print(f"[update_links_doc_v24] wrote {P} ({len(doc)} chars)")
