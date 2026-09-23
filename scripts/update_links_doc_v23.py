#!/usr/bin/env python3
"""update_links_doc_v23.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
V11 companion-alignment round + v23 package round: newest-first revision
note, companion package rows retargeted to companion_categorical_v11 (PDF,
LaTeX source, BibTeX -- also fixing the stale companion_refs_v9.bib row),
and the pre-submission checklist updated (audit_v28, v23 ZIPs)."""

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
rep("Generated 2026-09-23 (V19 comprehension-restructure round + v22\n"
    "package round: journal_manuscript_v19 + companion_categorical_v10;\n"
    "supersedes the V18 JTB-alignment + v21 package round).",
    "Generated 2026-09-24 (V11 companion-alignment round + v23 package\n"
    "round: journal_manuscript_v19 (unchanged) + companion_categorical_v11;\n"
    "supersedes the V19 comprehension-restructure + v22 package round).",
    "generation header")

# ---- 2. newest-first revision note (inserted before the V19 note) ------
V11_NOTE = """Revision note (2026-09-24, V11 companion-alignment + v23 package round,
delegation of the removed categorical subsection): the categorical
subsection removed from the v19 main body is delegated to the companion
paper, where its full development already lives (Definition def:kv
carries the viability-weighted curvature with the active-atom
correspondence to the application paper's kappa-mu and survival
covectors; the regime-delineation remark maps the application paper's
slopes 2.000/1.00 to the companion's kappa(a)=a^2 small-loop law and
wall-crossing O(eps) theorem; the future-directions item records the open
ratio-form discretization correspondence; the intro "Relation to the
application paper" paragraph carries the division of labor). No appendix
and no supplementary section in the main paper: nothing in the main
argument depends on the categorical reading (v18's own statement, kept
in v19's Discussion), and re-embedding the flagged prose in the BMB
submission -- body, appendix, or ESM -- would re-create the desk-reject
risk. The companion was updated on a NEW versioned file --
scripts/companion_categorical_v11.tex (from v10; v10 and all earlier
versions untouched) via scripts/companion_v11_alignment.py -- to align
its two cross-paper sentences with that division of labor: the intro
paragraph no longer claims the application paper "states the load-bearing
definitions ... in brief, adapted form" (it now cites this paper and
records the division of labor in one Discussion paragraph), and the
future-directions discretization-bridge item reads "instantiated
measure-theoretically in the application paper" instead of "and in the
application paper". Header Relation comment updated;
companion_refs_v11.bib is a byte-identical copy. Main v19 is UNCHANGED.
VERIFIED: audit_v28_numbers.py 349/349 PASS (identical check set to
v27, companion filename retargeted); pattern_sweep_v16 16/16 clean on
both; verify_v19_completeness ALL COMPLETE; tectonic companion 76 pp,
0 errors / 0 '??'; v23 ZIPs (build_submission_zips_v23.sh) fresh-dir
verified 37/76 pp. Cover letters retargeted (TAC letter: application
title to the v19 plain title, division-of-labor bullet updated, repo
file pointer to journal_manuscript_v19.tex; BMB letter: companion file
pointer to companion_categorical_v11.tex).

"""
V19_NOTE_HEAD = "Revision note (2026-09-23, V19 comprehension-restructure + v22 package"
rep(V19_NOTE_HEAD, V11_NOTE + V19_NOTE_HEAD, "newest-first revision note")

# ---- 3. companion package rows ------------------------------------------
rep(
    "| Manuscript PDF (76 pp; Gemini-register adoption as base -- title, "
    "four-pillar abstract, intro narrative, contribution titles, section "
    "leads; v9 substance retained (refs, proof statuses, machine "
    "verifications); clickable email and ORCID; prior versions retained "
    "as separate files) | "
    "[download/companion_categorical_v10.pdf]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v10.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "companion_categorical_v10.pdf) |",
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
    "companion PDF row")

rep(
    "| LaTeX source | [scripts/companion_categorical_v10.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v10.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_categorical_v10.tex) |",
    "| LaTeX source | [scripts/companion_categorical_v11.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v11.tex) | "
    "[raw](https://raw.githubusercontent.com/MIAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_categorical_v11.tex) |".replace("MIAA2020", "MIKEAA2020"),
    "companion LaTeX source row")

rep(
    "| BibTeX database | [scripts/companion_refs_v9.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v9.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_refs_v9.bib) |",
    "| BibTeX database (V11: byte-identical copy of the v10 database; "
    "fixes this table's stale v9 pointer) | "
    "[scripts/companion_refs_v11.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v11.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "companion_refs_v11.bib) |",
    "companion BibTeX row (stale v9 pointer fixed)")

# ---- 4. pre-submission checklist -----------------------------------------
rep(
    "cover letter with companion disclosure (retargeted to the v19 title);\n"
    "audit_v27_numbers.py 349/349 PASS; pattern_sweep_v16 16/16;\n"
    "verify_v19_completeness ALL COMPLETE; tectonic 37 pp 0 errors;\n"
    "v22 ZIPs fresh-dir verified 37/76 pp. Earlier",
    "cover letter with companion disclosure (retargeted to the v19 title);\n"
    "companion V11 alignment round: the removed categorical subsection\n"
    "delegated to the companion, both papers now describing the same\n"
    "division of labor (no appendix / no supplementary in the main);\n"
    "cover letters retargeted (TAC: v19 title + file pointer; BMB:\n"
    "companion v11 file pointer); audit_v28_numbers.py 349/349 PASS\n"
    "(identical check set to v27, companion retargeted to v11);\n"
    "pattern_sweep_v16 16/16; verify_v19_completeness ALL COMPLETE;\n"
    "tectonic main 37 pp / companion 76 pp, 0 errors / 0 '??';\n"
    "v23 ZIPs fresh-dir verified 37/76 pp. Earlier",
    "pre-submission checklist")

open(P, "w", encoding="utf-8").write(doc)
print("[update_links_doc_v23] applied:", "; ".join(applied))
print(f"[update_links_doc_v23] wrote {P} ({len(doc)} chars)")
