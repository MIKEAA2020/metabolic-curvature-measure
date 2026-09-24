#!/usr/bin/env python3
"""update_links_doc_v26.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
V21/V14 final-prose round + v26 package round: generation header,
newest-first revision note (read-through findings applied), Paper 1 and
Paper 2 current-package rows retargeted to v21/v14, and the
pre-submission checklist updated (audit_v31 366/366, v26 ZIPs)."""

P = ("/home/z/my-project/metabolic-curvature-measure/download/"
     "SUBMISSION_PACKAGE_LINKS.md")
doc = open(P, encoding="utf-8").read()
applied = []


def rep(old, new, tag):
    global doc
    if old not in doc and new in doc:
        applied.append(tag + " (already applied)")
        return
    assert old in doc, f"ANCHOR NOT FOUND: {tag}"
    assert doc.count(old) == 1, f"ANCHOR NOT UNIQUE: {tag}"
    doc = doc.replace(old, new)
    applied.append(tag)


REPO = "https://github.com/MIKEAA2020/metabolic-curvature-measure"
RAW = "https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure"

# ---- 1. generation header -----------------------------------------------
rep("Generated 2026-09-24 (V20/V13 Discover Applied Mathematics round +\n"
    "v25 package round: journal_manuscript_v20 + companion_categorical_v13;\n"
    "supersedes the V12 companion-comprehension + v24 package round).",
    "Generated 2026-09-24 (V21/V14 final-prose round + v26 package round: "
    "journal_manuscript_v21 + companion_categorical_v14;\n"
    "supersedes the V20/V13 Discover Applied Mathematics + v25 package "
    "round).",
    "generation header")

# ---- 2. newest-first revision note --------------------------------------
V2114_NOTE = """Revision note (2026-09-24, V21/V14 final-prose round + v26
package round, the final read-through pass of both manuscripts' prose):
the pass read both manuscripts end to end and applied its findings as a
light touch-up on NEW versioned files -- scripts/journal_manuscript_
v21.tex (from v20; v20 and all earlier versions untouched, via
scripts/v21_v14_final_prose_fixes.py) and scripts/companion_categorical_
v14.tex (from v13; v13 and all earlier versions untouched, same script).
MAIN: the Discussion memory subsection's same-gene transcript
correlation harmonized to +0.419 (the e27 artifact value gated by
audit E27-1, matching 5.9 and the buffering subsection -- the +0.420
token was the v17-ledger recomputation of the same quantity at slightly
different gene matching), the unexplained 'locked' qualifier replaced
by the actual provenance of the -0.098/+0.339 pair (the per-gene path
metric of 5.7, the V7 P0 deposits), and the six in-text figure
references normalized to the Springer 'Fig. n' form (Fig.~).
COMPANION: the where-clause of the piecewise-holonomy formula restored
to its equation (it had been displaced behind the affine-wall regime
paragraph, leaving a lowercase fragment), the two-contractions remark's
state space corrected to the theorem's box X = [-1.5,1.5]^d ([0,1]^d
fails the hypothesis by the paper's own box-invariance computation), a
punctuation repair in the Ito-expansion proof, and the figure-label
convention aligned with the main paper and the journal's 'Fig. n' form
(captions via the caption package; the three in-text 'Figure~'
references normalized). Every theorem, proof, number, section, table,
and figure unchanged. VERIFIED: audit_v31_numbers.py 366/366 PASS (the
v30 ledger carried + 7 V21 gates); tectonic main 37 pp / companion
76 pp, 0 errors / 0 '??'; v26 ZIPs (build_submission_zips_v26.sh)
fresh-dir verified 37/76 pp; DAM cover letters retargeted (366/366).

"""
rep("Revision note (2026-09-24, V20/V13 DAM round + v25 package round,\n"
    "F1-F7 light touch-up + venue alignment):",
    V2114_NOTE + "Revision note (2026-09-24, V20/V13 DAM round + v25 "
    "package round,\nF1-F7 light touch-up + venue alignment):",
    "newest-first revision note")

# ---- 3. Paper 1 current-package rows -------------------------------------
rep("| Manuscript PDF (37 pp, v20 DAM round: the F1-F7 review findings "
    "applied as a light touch-up -- the direct trajectory rank "
    "correlation reported (rho = +0.92 P1 / +0.96 P2, 424 shared genes), "
    "the GC-rate two-regime qualifier, three near-identity wordings "
    "corrected, the translation-buffering mechanism hedged and the title "
    "narrowed to the measured claim; DAM alignment: numeric square-bracket "
    "citations, Fig.-label captions, 245-word abstract, 359-count refresh; "
    "every number unchanged, audit_v30 359/359; clickable email and ORCID; "
    "prior versions retained as separate files) | "
    "[download/journal_manuscript_v20.pdf](" + REPO + "/blob/main/download/"
    "journal_manuscript_v20.pdf) | [raw](" + RAW + "/main/download/"
    "journal_manuscript_v20.pdf) |",
    "| Manuscript PDF (37 pp, v21 final-prose round: the read-through "
    "pass applied -- the Discussion memory subsection's same-gene "
    "transcript correlation harmonized to +0.419 (one audited value "
    "everywhere), the protein-layer robustness sentence's provenance "
    "named (the per-gene path metric of 5.7), and the six in-text figure "
    "references normalized to the 'Fig. n' form; every number unchanged "
    "from v20, audit_v31 366/366; clickable email and ORCID; prior "
    "versions retained as separate files) | "
    "[download/journal_manuscript_v21.pdf](" + REPO + "/blob/main/download/"
    "journal_manuscript_v21.pdf) | [raw](" + RAW + "/main/download/"
    "journal_manuscript_v21.pdf) |",
    "paper-1 PDF row")

rep("| Cover letter -- DAM (primary, Research Article; declarations, "
    "companion disclosure, v20 title, 359/359 audit) |",
    "| Cover letter -- DAM (primary, Research Article; declarations, "
    "companion disclosure, v21 title, 366/366 audit) |",
    "paper-1 cover-letter row")

rep("| LaTeX source | [scripts/journal_manuscript_v20.tex](" + REPO +
    "/blob/main/scripts/journal_manuscript_v20.tex) | [raw](" + RAW +
    "/main/scripts/journal_manuscript_v20.tex) |",
    "| LaTeX source | [scripts/journal_manuscript_v21.tex](" + REPO +
    "/blob/main/scripts/journal_manuscript_v21.tex) | [raw](" + RAW +
    "/main/scripts/journal_manuscript_v21.tex) |",
    "paper-1 source row")

rep("| Reference list (alphabetical, 29 entries -- kacser1973 + "
    "heinrich1974 present; v20 DAM naming; the zai2026categorical "
    "cross-citation title aligned to the companion's actual title) | "
    "[scripts/journal_manuscript_v20_dam_refs.tex](" + REPO +
    "/blob/main/scripts/journal_manuscript_v20_dam_refs.tex) | [raw](" +
    RAW + "/main/scripts/journal_manuscript_v20_dam_refs.tex) |",
    "| Reference list (alphabetical, 29 entries -- kacser1973 + "
    "heinrich1974 present; v21 naming, entries byte-identical to the "
    "v20 list; the zai2026categorical cross-citation title aligned to "
    "the companion's actual title) | "
    "[scripts/journal_manuscript_v21_dam_refs.tex](" + REPO +
    "/blob/main/scripts/journal_manuscript_v21_dam_refs.tex) | [raw](" +
    RAW + "/main/scripts/journal_manuscript_v21_dam_refs.tex) |",
    "paper-1 refs row")

rep("| BibTeX database | [scripts/journal_manuscript_v20_refs.bib](" +
    REPO + "/blob/main/scripts/journal_manuscript_v20_refs.bib) | "
    "[raw](" + RAW + "/main/scripts/journal_manuscript_v20_refs.bib) |",
    "| BibTeX database | [scripts/journal_manuscript_v21_refs.bib](" +
    REPO + "/blob/main/scripts/journal_manuscript_v21_refs.bib) | "
    "[raw](" + RAW + "/main/scripts/journal_manuscript_v21_refs.bib) |",
    "paper-1 bib row")

rep("The v20 package\n> carries every one of these elements",
    "The v21 package\n> carries every one of these elements",
    "paper-1 scope-fit note")

rep("files, upload them together with `journal_manuscript_v20_dam_refs.tex` "
    "and",
    "files, upload them together with `journal_manuscript_v21_dam_refs.tex` "
    "and",
    "paper-1 build note 1")

rep("(`\\graphicspath{{./}{../download/}}`). The v20 package: 37 pp.\n"
    "Upload `journal_manuscript_v20_dam_refs.tex` (not the v19 refs\n"
    "name) together with the .tex.",
    "(`\\graphicspath{{./}{../download/}}`). The v21 package: 37 pp.\n"
    "Upload `journal_manuscript_v21_dam_refs.tex` (not the v20 refs\n"
    "name) together with the .tex.",
    "paper-1 build note 2")

# ---- 4. Paper 2 current-package rows -------------------------------------
rep("| Manuscript PDF (76 pp; V13 DAM round -- the review's F2 applied: "
    "the six-axis abstract sentence now covers all three body categories "
    "(regime switches and nitrogen-source substitution); DAM alignment: "
    "abstract 248 < 250 words, keywords 9 -> 6, numeric square-bracket "
    "citations, the zai2026measure cross-citation title aligned to the "
    "v20 application title; every theorem, proof, and number unchanged "
    "from v12 (audit_v30 359/359); clickable email and ORCID; prior "
    "versions retained as separate files) | "
    "[download/companion_categorical_v13.pdf](" + REPO + "/blob/main/"
    "download/companion_categorical_v13.pdf) | [raw](" + RAW +
    "/main/download/companion_categorical_v13.pdf) |",
    "| Manuscript PDF (76 pp; V14 final-prose round -- the read-through "
    "pass applied: the where-clause of the piecewise-holonomy formula "
    "restored to its equation, the two-contractions remark's state space "
    "corrected to the theorem's box X = [-1.5,1.5]^d, an Ito-proof "
    "punctuation repair, and the figure-label convention aligned with "
    "the journal's 'Fig. n' form; every theorem, proof, and number "
    "unchanged from v13 (audit_v31 366/366); clickable email and ORCID; "
    "prior versions retained as separate files) | "
    "[download/companion_categorical_v14.pdf](" + REPO + "/blob/main/"
    "download/companion_categorical_v14.pdf) | [raw](" + RAW +
    "/main/download/companion_categorical_v14.pdf) |",
    "paper-2 PDF row")

rep("| Cover letter -- DAM (primary, Research Article; declarations, "
    "application-paper disclosure, v13 title) |",
    "| Cover letter -- DAM (primary, Research Article; declarations, "
    "application-paper disclosure, v14 title) |",
    "paper-2 cover-letter row")

rep("| LaTeX source | [scripts/companion_categorical_v13.tex](" + REPO +
    "/blob/main/scripts/companion_categorical_v13.tex) | [raw](" + RAW +
    "/main/scripts/companion_categorical_v13.tex) |",
    "| LaTeX source | [scripts/companion_categorical_v14.tex](" + REPO +
    "/blob/main/scripts/companion_categorical_v14.tex) | [raw](" + RAW +
    "/main/scripts/companion_categorical_v14.tex) |",
    "paper-2 source row")

rep("| BibTeX database (V13: the zai2026measure title aligned to the "
    "v20 application title; otherwise byte-identical to the v12 database)"
    " | [scripts/companion_refs_v13.bib](" + REPO + "/blob/main/scripts/"
    "companion_refs_v13.bib) | [raw](" + RAW + "/main/scripts/"
    "companion_refs_v13.bib) |",
    "| BibTeX database (V14: byte-identical to the v13 database; no "
    "reference changes in the final-prose round) | "
    "[scripts/companion_refs_v14.bib](" + REPO + "/blob/main/scripts/"
    "companion_refs_v14.bib) | [raw](" + RAW + "/main/scripts/"
    "companion_refs_v14.bib) |",
    "paper-2 bib row")

# ---- 5. pre-submission checklist -----------------------------------------
rep("Resolved (V20/V13 Discover Applied Mathematics round, 2026-09-24):",
    "Resolved (V21/V14 final-prose round, 2026-09-24): the final\n"
    "read-through pass of both manuscripts' prose applied on NEW\n"
    "versioned files (main v21 from v20, companion v14 from v13; the\n"
    "earlier versions untouched) -- the memory-subsection transcript\n"
    "token harmonized to +0.419 (one audited value everywhere), the\n"
    "protein-layer robustness sentence's provenance named (the per-gene\n"
    "path metric), six 'Fig. n' in-text references normalized, the\n"
    "companion where-clause restored, the two-contractions state space\n"
    "corrected, an Ito-proof punctuation repair, and the companion\n"
    "figure-label captions aligned to 'Fig. n'; audit_v31_numbers.py\n"
    "366/366 PASS; tectonic 37/76 pp, 0 errors / 0 '??'; v26 ZIPs\n"
    "(submission_main_dam.zip, submission_companion_dam.zip) fresh-dir\n"
    "verified; cover letters retargeted (366/366). Earlier rounds\n"
    "resolved: the V20/V13 Discover Applied Mathematics round,\n"
    "2026-09-24:",
    "checklist head")

open(P, "w", encoding="utf-8").write(doc)
print(f"SUBMISSION_PACKAGE_LINKS.md updated ({len(applied)} edits):")
for tag in applied:
    print("  -", tag)
