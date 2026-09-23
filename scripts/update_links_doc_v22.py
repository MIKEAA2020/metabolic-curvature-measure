#!/usr/bin/env python3
"""update_links_doc_v22.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
v19 comprehension-restructure round (BMB target after the JTB desk
rejection): newest-first revision note, Paper 1 section retitled to the
Bulletin of Mathematical Biology with BMB portal links, package rows
retargeted to journal_manuscript_v19 + submission_main_bmb.zip, and the
pre-submission checklist updated."""

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
rep("Generated 2026-09-21 (V18 JTB-alignment round + v21 package round:\n"
    "journal_manuscript_v18 + companion_categorical_v10; supersedes the\n"
    "V17 enrichment + venue-evaluation + v20 package round).",
    "Generated 2026-09-23 (V19 comprehension-restructure round + v22\n"
    "package round: journal_manuscript_v19 + companion_categorical_v10;\n"
    "supersedes the V18 JTB-alignment + v21 package round).",
    "generation header")

# ---- 2. newest-first revision note (inserted before the V18 note) ------
V19_NOTE = """Revision note (2026-09-23, V19 comprehension-restructure + v22 package
round, BMB target): after the JTB desk rejection (EIC: the article's
structure and intent could not be followed; AI-assisted formulation a
barrier), the main manuscript was restructured for comprehension on a
NEW versioned file -- scripts/journal_manuscript_v19.tex (from v18; v18
and all earlier versions untouched) via
scripts/v19_comprehension_restructure.py, re-ordering the paper so the
biological line of argument leads: (1) new plain title ("A discrete
curvature measure for flux balance analysis predicts transcriptional
regulation and translational buffering in Escherichia coli"); (2)
bio-first abstract rebuilt as a single narrative arc (243 audit-style
words, within the Springer/BMB 150-250 range; every audited number
kept); (3) keywords 6 terms (BMB 4-6; the JTB-only 7th term 'path
dependence' dropped); (4) the intro's five-finding roman-numeral
enumeration replaced by three question-led paragraphs (what
mathematics governs rerouting / does the geometry capture real
rerouting / does the geometry predict regulation); (5) the
categorical-reading subsection REMOVED from the body (the Discussion's
companion paragraph carries the pointer; the value-flux event
dichotomy corollary retained in the body as its own subsection); (6)
the refinement-resolution bridge MOVED to Appendix A (appendix order:
bridge, proofs, technical proofs); (7) the counts-disambiguation
appendix DELETED, its essential mapping folded into Methods; (8) refs
carried to journal_manuscript_v19_bmb_refs.tex (29 entries
byte-identical). Package renamed
submission_main_jtb.zip -> submission_main_bmb.zip (v22 ZIPs,
build_submission_zips_v22.sh) with a BMB README; the JTB-required
highlights file stays in the repository as JTB-path history
(download/highlights_jtb.docx) but is NOT part of the BMB package; the
companion/TAC package unchanged. VERIFIED: audit_v27_numbers.py
(make_audit_v27.py) 349/349 PASS (347 carried v26 checks, JTB gates
recapped to BMB, + V19 restructure gates); pattern_sweep_v16 16/16
clean on both; v19 structural gates PASS; verify_v19_completeness.py
ALL COMPLETE (every removed numeric token traced to an intentionally
deleted/rewritten region; labels/citations resolve; no dangling
references); tectonic main 37 pp, 0 errors / 0 undefined; v22 ZIPs
fresh-dir re-verified 37/76 pp. Cover letter
download/cover_letter_bmb.md retargeted to the v19 title + the
349-check audit count. Remaining at submission time: the BMB
Editorial Manager account (code bmab).

"""
rep("Revision note (2026-09-21, V18 JTB-alignment round + v21 package\nround):",
    V19_NOTE + "Revision note (2026-09-21, V18 JTB-alignment round + "
    "v21 package\nround):",
    "v19 revision note (newest first)")

# ---- 3. Paper 1 section header + venue status ---------------------------
rep("## Paper 1 (Main) — Journal of Theoretical Biology (Elsevier)\n\n"
    "**Title:** A Geometric Theory of Metabolic Flux Rerouting: How\n"
    "Active-Set Curvature Predicts Transcriptional Regulation and\n"
    "Protein-Layer Buffering (Regular Article; 38 pp).\n\n"
    "**Venue status (2026-09-21, V18 round):** the venue decision is\n"
    "**JTB (confirmed)** per the author directive; the v18 round aligns\n"
    "the full package to the live JTB Guide for Authors (abstract 249\n"
    "words under the 250 cap; 7 keywords; CRediT statement; the required\n"
    "separate Highlights file download/highlights_jtb.docx; cover letter\n"
    "download/cover_letter_jtb.md retargeted to Regular Article). The\n"
    "package itself is venue-neutral and compiles identically for any\n"
    "Elsevier/Springer target. Fallback paths remain documented in\n"
    "download/V17_Venue_Evaluation.md: BMB return only via\n"
    "pre-submission inquiry (resubmission-aware letter\n"
    "download/cover_letter_bmb.md, superseded package naming), PLOS\n"
    "Comp Bio the biology-maximizing alternative (APC).",
    "## Paper 1 (Main) — Bulletin of Mathematical Biology (Springer)\n\n"
    "**Title:** A discrete curvature measure for flux balance analysis\n"
    "predicts transcriptional regulation and translational buffering in\n"
    "Escherichia coli (Original Research; 37 pp).\n\n"
    "**Venue status (2026-09-23, V19 round):** JTB desk-rejected the v18\n"
    "submission on comprehensibility grounds (EIC: structure and intent\n"
    "hard to follow; AI-assisted formulation a barrier), so the paper was\n"
    "deeply restructured as v19 (plain title, bio-first abstract,\n"
    "question-led introduction, categorical subsection removed,\n"
    "refinement bridge to Appendix A, counts appendix folded into\n"
    "Methods) and retargeted to BMB, whose mathematical-biology\n"
    "readership matches the paper's formal content. BMB never received a\n"
    "previous submission of this manuscript, so this is a fresh first\n"
    "submission, not a resubmission. The package is venue-neutral and\n"
    "compiles identically for any Springer/Elsevier target. Fallback\n"
    "paths remain documented in download/V17_Venue_Evaluation.md (PLOS\n"
    "Comp Bio the biology-maximizing alternative, APC; Mathematical\n"
    "Biosciences the math-first alternative).",
    "paper 1 header + venue status")

# ---- 4. journal links table ---------------------------------------------
rep("""### Journal / submission-portal links (all verified live 2026-09-21)

| Resource | Link |
|---|---|
| Journal home (Elsevier) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology |
| Guide for Authors (abstract <= 250 words; keywords 1-7; Highlights required; CRediT) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/publish/guide-for-authors |
| Submit portal | https://submit.elsevier.com/JTB (resolves to Editorial Manager) |
| Editorial Manager (direct) | https://www.editorialmanager.com/JTB/ |
| Aims and scope | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/about/aims-and-scope |""",
    """### Journal / submission-portal links (BMB links verified live in the
### earlier BMB rounds; JTB links retained for history)

| Resource | Link |
|---|---|
| Journal home (Springer) | https://link.springer.com/journal/11538 |
| Submission guidelines | https://link.springer.com/journal/11538/submission-guidelines |
| Editorial Manager (code **bmab**) | https://www.editorialmanager.com/bmab/ |
| JTB Guide for Authors (historical, v18 round) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/publish/guide-for-authors |""",
    "journal links table")

# ---- 5. package rows -----------------------------------------------------
rep("| **One-file upload ZIP (compile-ready, venue-neutral, JTB README)** | — | [download/submission_main_jtb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_jtb.zip) |\n"
    "| **Highlights file (JTB-required separate upload, 5 bullets <= 85 chars)** | [download/highlights_jtb.docx](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/highlights_jtb.docx) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/highlights_jtb.docx) |",
    "| **One-file upload ZIP (compile-ready, venue-neutral, BMB README)** | — | [download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_bmb.zip) |\n"
    "| Highlights file (JTB-path history only; not part of the BMB package) | [download/highlights_jtb.docx](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/highlights_jtb.docx) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/highlights_jtb.docx) |",
    "package rows: ZIP + highlights")

rep("| Manuscript PDF (38 pp, v18 JTB-alignment round: all v17 enrichment content -- worked example, wall coordinates, interior architecture, construction-order rule, anatomy of one switch, MCA comparison, memory-substrate deduction -- with the abstract at 249 words under the JTB 250 cap, 7 keywords, and the CRediT statement; clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v18.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v18.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v18.pdf) |",
    "| Manuscript PDF (37 pp, v19 comprehension-restructure round: plain title, bio-first 243-word abstract, question-led introduction, categorical subsection removed, refinement bridge in Appendix A, counts folded into Methods; every v18 number unchanged, audit_v27 349/349; clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v19.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v19.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v19.pdf) |",
    "package rows: manuscript PDF")

rep("| Cover letter -- JTB (primary, Regular Article; declarations, companion disclosure) | [download/cover_letter_jtb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_jtb.md) |\n"
    "| Cover letter -- BMB resubmission-aware version (fallback inquiry path; prior desk decision flagged) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_bmb.md) |",
    "| Cover letter -- BMB (primary, Original Research; declarations, companion disclosure, v19 title) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_bmb.md) |\n"
    "| Cover letter -- JTB (historical, v18 round) | [download/cover_letter_jtb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_jtb.md) |",
    "package rows: cover letters")

rep("| LaTeX source | [scripts/journal_manuscript_v18.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v18.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v18.tex) |\n"
    "| Reference list (alphabetical, 29 entries -- kacser1973 + heinrich1974 added; venue-neutral v18 naming) | [scripts/journal_manuscript_v18_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v18_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v18_refs.tex) |\n"
    "| BibTeX database | [scripts/journal_manuscript_v18_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v18_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v18_refs.bib) |",
    "| LaTeX source | [scripts/journal_manuscript_v19.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v19.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19.tex) |\n"
    "| Reference list (alphabetical, 29 entries -- kacser1973 + heinrich1974 added; v19 BMB naming) | [scripts/journal_manuscript_v19_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v19_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19_bmb_refs.tex) |\n"
    "| BibTeX database | [scripts/journal_manuscript_v19_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/scripts/journal_manuscript_v19_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19_refs.bib) |",
    "package rows: source + refs")

# ---- 6. build note --------------------------------------------------------
rep("(`\\graphicspath{{./}{../download/}}`).",
    "(`\\graphicspath{{./}{../download/}}`). The v19 package: 37 pp.\n"
    "Upload `journal_manuscript_v19_bmb_refs.tex` (not the v18 refs\n"
    "name) together with the .tex.",
    "build note")

rep("contains the .tex, the input'ed reference list, the .bib database, and all\n"
    "six figures at the exact relative subpaths the .tex expects — verified to\n"
    "compile standalone, 38 pp, 0 errors). If instead you upload individual\n"
    "files, upload them together with `journal_manuscript_v18_refs.tex` and",
    "contains the .tex, the input'ed reference list, the .bib database, and all\n"
    "six figures at the exact relative subpaths the .tex expects — verified to\n"
    "compile standalone, 37 pp, 0 errors). If instead you upload individual\n"
    "files, upload them together with `journal_manuscript_v19_bmb_refs.tex` and",
    "build note page count + refs name")

# ---- 7. checklist ---------------------------------------------------------
rep("""Resolved (V18 JTB-alignment round, 2026-09-21): JTB-requirements
pass -- Regular Article type; abstract 249 audit-style words under
JTB's 250-word cap (rendered ~235); 7 keywords (JTB range 1-7); the
REQUIRED Highlights file download/highlights_jtb.docx (5 bullets,
each <= 85 characters incl. spaces, biological applications +
theoretical advancement featured; postcheck 9/9); the CRediT
authorship contribution statement in the backmatter; competing
interests, funding, generative-AI, and research-data statements
present; author-year references (Elsevier accepts any consistent
style at submission); continuous line numbering; declarations in
backmatter; cover letter with companion disclosure (retargeted to
Regular Article); audit_v26_numbers.py 347/347 PASS;
pattern_sweep_v16 16/16; verify_v18_completeness ALL COMPLETE;
tectonic 38 pp 0 errors; VLM CLEAN on the changed pages. Earlier""",
    """Resolved (V19 comprehension-restructure round, 2026-09-23, BMB
target): the JTB desk-rejection diagnosis addressed -- plain single-
claim title; bio-first 243-word abstract (Springer/BMB 150-250);
6 keywords (BMB 4-6); three question-led introduction paragraphs;
categorical subsection removed from the body; refinement bridge in
Appendix A; counts-disambiguation appendix folded into Methods; the
CRediT authorship contribution statement retained in the backmatter
(Springer accepts any consistent form); competing interests, funding,
generative-AI, and research-data statements present; author-year
references; continuous line numbering; declarations in backmatter;
cover letter with companion disclosure (retargeted to the v19 title);
audit_v27_numbers.py 349/349 PASS; pattern_sweep_v16 16/16;
verify_v19_completeness ALL COMPLETE; tectonic 37 pp 0 errors;
v22 ZIPs fresh-dir verified 37/76 pp. Earlier""",
    "checklist resolved block")

rep("""Remaining at submission time: only the JTB Editorial Manager account
(https://www.editorialmanager.com/JTB/, via
https://submit.elsevier.com/JTB) -- then upload the manuscript ZIP
contents (or the single PDF, per Your Paper Your Way),
download/highlights_jtb.docx as its own Highlights file, and
download/cover_letter_jtb.md as the cover letter. Fallback paths
(BMB pre-submission inquiry, PLOS Comp Bio) remain documented in
download/V17_Venue_Evaluation.md. Resolved this round:""",
    """Remaining at submission time: only the BMB Editorial Manager account
(https://www.editorialmanager.com/bmab/, code bmab) -- then upload
the manuscript ZIP contents (or the single PDF) and
download/cover_letter_bmb.md as the cover letter. Fallback paths
(PLOS Comp Bio, Mathematical Biosciences) remain documented in
download/V17_Venue_Evaluation.md. Resolved this round:""",
    "checklist remaining block")

open(P, "w").write(doc)
print("applied:", len(applied), "edits")
for t in applied:
    print("  -", t)
