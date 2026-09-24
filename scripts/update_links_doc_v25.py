#!/usr/bin/env python3
"""update_links_doc_v25.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
V20/V13 Discover Applied Mathematics round + v25 package round:
generation header, newest-first revision note (F1-F7 resolution + DAM
venue alignment), Paper 1 and Paper 2 sections retargeted to DAM
(title, venue status, journal links, package rows, build note), and
the pre-submission checklist updated (audit_v30 359/359, v25 ZIPs,
Snapp route)."""

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


REPO = "https://github.com/MIKEAA2020/metabolic-curvature-measure"
RAW = "https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure"

# ---- 1. generation header -----------------------------------------------
rep("Generated 2026-09-24 (V12 companion-comprehension round + v24\n"
    "package round: journal_manuscript_v19 (unchanged) +\n"
    "companion_categorical_v12; supersedes the V11 companion-alignment +\n"
    "v23 package round).",
    "Generated 2026-09-24 (V20/V13 Discover Applied Mathematics round +\n"
    "v25 package round: journal_manuscript_v20 + companion_categorical_v13;\n"
    "supersedes the V12 companion-comprehension + v24 package round).",
    "generation header")

# ---- 2. newest-first revision note (inserted before the V12 note) ------
V2013_NOTE = """Revision note (2026-09-24, V20/V13 DAM round + v25 package round,
F1-F7 light touch-up + venue alignment): the causal-coherence and
prose-alignment review (download/Causal_Coherence_and_Prose_Alignment_
Evaluation.md, findings F1-F7) is applied on NEW versioned files --
scripts/journal_manuscript_v20.tex (from v19; v19 and all earlier
versions untouched, via scripts/v20_main_f_fixes.py) and
scripts/companion_categorical_v13.tex (from v12; v12 and all earlier
versions untouched, via scripts/v13_companion_edits.py), with the
manuscripts retargeted to Discover Applied Mathematics (Springer
Nature, link.springer.com/journal/44585). MAIN: F3 the direct
per-gene trajectory rank correlation now reported in situ -- rho =
+0.92 (P1) and +0.96 (P2) over the 424 genes nonzero on both paths,
computed from the deposited per-gene path artifacts (scripts/
v20_f3_rank_stability.py -> download/deepseek_bridge/
v20_path_rank_stability.json); F4 the intro Glivenko-Cantelli
sentence gains the two-regime qualifier ("across random panels
(designed panels reproduce them exactly)"); F5 three near-identity
wordings corrected ("rank agreement"; "the two metrics agree to five
decimals"; the Discussion's "measured metric agreement") since rho =
0.99998 is agreement, not identity; F6 the translation-buffering
mechanism hedged at the abstract and intro ("consistent with") and
the title narrowed to the measured claim ("predicts transcriptional
regulation"; the buffering dissociation stays a hedged,
keyword-indexed finding); F1 the audit count refreshed to the v30
ledger (359); F7 moot (the v19 restructure had removed the flagged
site). COMPANION: F2 the six-axis abstract sentence now covers all
three body categories ("...re-stratifying only at regime switches and
nitrogen-source substitution"). VENUE (live-verified submission
guidelines, re-verified this round): Snapp submission system;
Research article; abstract less than 250 words (main 245, companion
248); numeric square-bracket citations (natbib [numbers,sort&compress,
square]) per "identified by numbers in square brackets"; "Fig. n"
caption labels (labelsep=space, no punctuation after the number);
single-anonymous review (author identity retained on both papers);
companion keywords 9 -> 6 (Springer 4-6 range); cross-citation titles
aligned both directions; reference list journal_manuscript_
v20_dam_refs.tex (entries byte-identical). Every theorem, proof,
number, section, table, and figure unchanged. VERIFIED:
audit_v30_numbers.py 359/359 PASS (v29 ledger extended with the V20
gates; first run caught 2 FAILs -- a third "metric invariance" site
and the stale 349 count -- both fixed); tectonic main 37 pp /
companion 76 pp, 0 errors / 0 '??'; v25 ZIPs
(build_submission_zips_v25.sh) fresh-dir verified 37/76 pp; DAM
cover letters written for both papers.

"""
V12_NOTE_HEAD = "Revision note (2026-09-24, V12 companion-comprehension + v24 package"
rep(V12_NOTE_HEAD, V2013_NOTE + V12_NOTE_HEAD,
    "newest-first revision note")

# ---- 3. Paper 1 header + title + venue status --------------------------
rep("## Paper 1 (Main) — Bulletin of Mathematical Biology (Springer)",
    "## Paper 1 (Main) — Discover Applied Mathematics (Springer Nature)",
    "Paper 1 section header")

rep("**Title:** A discrete curvature measure for flux balance analysis\n"
    "predicts transcriptional regulation and translational buffering in\n"
    "Escherichia coli (Original Research; 37 pp).",
    "**Title:** A discrete curvature measure for flux balance analysis\n"
    "predicts transcriptional regulation in Escherichia coli (Research\n"
    "Article; 37 pp).",
    "Paper 1 title (v20 narrowed form)")

rep("**Venue status (2026-09-23, V19 round):** JTB desk-rejected the v18\n"
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
    "**Venue status (2026-09-24, V20 round):** the target venue is now\n"
    "Discover Applied Mathematics (Springer Nature), per the author's\n"
    "venue decision. History: JTB desk-rejected the v18 submission on\n"
    "comprehensibility grounds; the paper was deeply restructured as v19\n"
    "(plain title, bio-first abstract, question-led introduction,\n"
    "categorical subsection removed, refinement bridge to Appendix A,\n"
    "counts appendix folded into Methods) and briefly retargeted to\n"
    "BMB (never submitted); the V20 round then applied the Discover\n"
    "Applied Mathematics submission guidelines (live-verified):\n"
    "Snapp submission system, Research article, abstract of less than\n"
    "250 words (245), numeric square-bracket citations, Fig. n caption\n"
    "labels, single-anonymous review. The v20 package has never been\n"
    "submitted to any journal. Fallback paths remain documented in\n"
    "download/V17_Venue_Evaluation.md.",
    "Paper 1 venue status")

# ---- 4. Paper 1 journal links table + scope blockquote ------------------
rep("### Journal / submission-portal links (BMB links verified live in the\n"
    "### earlier BMB rounds; JTB links retained for history)\n"
    "\n"
    "| Resource | Link |\n"
    "|---|---|\n"
    "| Journal home (Springer) | https://link.springer.com/journal/11538 |\n"
    "| Submission guidelines | https://link.springer.com/journal/11538/submission-guidelines |\n"
    "| Editorial Manager (code **bmab**) | https://www.editorialmanager.com/bmab/ |\n"
    "| JTB Guide for Authors (historical, v18 round) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/publish/guide-for-authors |",
    "### Journal / submission-portal links (DAM links live-verified this\n"
    "### round; BMB/JTB links retained for history)\n"
    "\n"
    "| Resource | Link |\n"
    "|---|---|\n"
    "| Journal home (Springer Nature) | https://link.springer.com/journal/44585 |\n"
    "| Submission guidelines (live-verified: Snapp; abstract < 250; single-anonymous; numeric square-bracket citations) | https://link.springer.com/journal/44585/submission-guidelines |\n"
    "| BMB journal home (historical, v19 round) | https://link.springer.com/journal/11538 |\n"
    "| JTB Guide for Authors (historical, v18 round) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/publish/guide-for-authors |",
    "Paper 1 journal links table")

rep("> Scope fit (from the live aims & scope): JTB is \"the leading forum for\n"
    "> theoretical perspectives that give insight into biological processes\";\n"
    "> papers must state the biological significance clearly, and Highlights\n"
    "> must feature the biological applications as well as theoretical\n"
    "> advancements -- the v18 package does both. Highly speculative or\n"
    "> purely-mathematical papers are out of scope; the manuscript's\n"
    "> genome-scale empirical association and named biology anchor it in\n"
    "> scope. The regulatory-FBA lineage precedent: Covert, Schilling &\n"
    "> Palsson, JTB 213:73-88, 2001.\n"
    ">\n"
    "> Fallback path (BMB pre-submission inquiry): journal home\n"
    "> https://link.springer.com/journal/11538, submission guidelines\n"
    "> https://link.springer.com/journal/11538/submission-guidelines,\n"
    "> portal https://www.editorialmanager.com/bmab (code **bmab**, not\n"
    "> `jomb`). Review model single-blind; the v18 package compiles\n"
    "> identically for the Springer route.",
    "> Scope fit (Discover Applied Mathematics, from the live submission\n"
    "> guidelines, re-verified this round): submissions via Snapp; for\n"
    "> all article types the journal requires the manuscript file, an\n"
    "> abstract of less than 250 words, and a cover letter outlining the\n"
    "> research and why it is appropriate for the journal; article type\n"
    "> Research (new scientific results within the journal's scope);\n"
    "> single-anonymous peer review; numeric square-bracket citations\n"
    "> (\"identified by numbers in square brackets e.g. [1-3, 7]\");\n"
    "> figure captions beginning \"Fig. n\" with no punctuation after the\n"
    "> number; all articles published open access. The v20 package\n"
    "> carries every one of these elements (245-word abstract, six\n"
    "> keywords, numeric natbib mode, Fig.-label captions, CRediT +\n"
    "> declarations in the backmatter).\n"
    ">\n"
    "> Historical routes: BMB (Editorial Manager, code bmab) and JTB\n"
    "> (EditorialManager.com/JTB) -- both superseded by the DAM target;\n"
    "> the package is venue-neutral and compiles identically.",
    "Paper 1 scope-fit blockquote")

# ---- 5. Paper 1 package rows ---------------------------------------------
rep("| **One-file upload ZIP (compile-ready, venue-neutral, BMB README)** | — | "
    "[download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/submission_main_bmb.zip) |",
    "| **One-file upload ZIP (compile-ready, DAM README; fresh-dir verified 37 pp)** | — | "
    "[download/submission_main_dam.zip](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/submission_main_dam.zip) |",
    "Paper 1 ZIP row")

rep("| Manuscript PDF (37 pp, v19 comprehension-restructure round: plain title, bio-first 243-word abstract, question-led introduction, categorical subsection removed, refinement bridge in Appendix A, counts folded into Methods; every v18 number unchanged, audit_v27 349/349; clickable email and ORCID; prior versions retained as separate files) | "
    "[download/journal_manuscript_v19.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/journal_manuscript_v19.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v19.pdf) |",
    "| Manuscript PDF (37 pp, v20 DAM round: the F1-F7 review findings applied as a light touch-up -- the direct trajectory rank correlation reported (rho = +0.92 P1 / +0.96 P2, 424 shared genes), the GC-rate two-regime qualifier, three near-identity wordings corrected, the translation-buffering mechanism hedged and the title narrowed to the measured claim; DAM alignment: numeric square-bracket citations, Fig.-label captions, 245-word abstract, 359-count refresh; every number unchanged, audit_v30 359/359; clickable email and ORCID; prior versions retained as separate files) | "
    "[download/journal_manuscript_v20.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/journal_manuscript_v20.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v20.pdf) |",
    "Paper 1 manuscript PDF row")

rep("| Cover letter -- BMB (primary, Original Research; declarations, companion disclosure, v19 title) | "
    "[download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_bmb.md) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_bmb.md) |",
    "| Cover letter -- DAM (primary, Research Article; declarations, companion disclosure, v20 title, 359/359 audit) | "
    "[download/cover_letter_dam.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_dam.md) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_dam.md) |\n"
    "| Cover letter -- BMB (historical, v19 round) | "
    "[download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_bmb.md) |",
    "Paper 1 cover letter rows")

rep("| LaTeX source | [scripts/journal_manuscript_v19.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v19.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19.tex) |",
    "| LaTeX source | [scripts/journal_manuscript_v20.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v20.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v20.tex) |",
    "Paper 1 LaTeX source row")

rep("| Reference list (alphabetical, 29 entries -- kacser1973 + heinrich1974 added; v19 BMB naming) | "
    "[scripts/journal_manuscript_v19_bmb_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v19_bmb_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19_bmb_refs.tex) |",
    "| Reference list (alphabetical, 29 entries -- kacser1973 + heinrich1974 present; v20 DAM naming; the zai2026categorical cross-citation title aligned to the companion's actual title) | "
    "[scripts/journal_manuscript_v20_dam_refs.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v20_dam_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v20_dam_refs.tex) |",
    "Paper 1 reference-list row")

rep("| BibTeX database | [scripts/journal_manuscript_v19_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v19_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v19_refs.bib) |",
    "| BibTeX database | [scripts/journal_manuscript_v20_refs.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v20_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v20_refs.bib) |",
    "Paper 1 BibTeX row")

rep("Build note: for Overleaf or any standalone compiler, upload **the ZIP** (it\n"
    "contains the .tex, the input'ed reference list, the .bib database, and all\n"
    "six figures at the exact relative subpaths the .tex expects — verified to\n"
    "compile standalone, 37 pp, 0 errors). If instead you upload individual\n"
    "files, upload them together with `journal_manuscript_v19_bmb_refs.tex` and\n"
    "the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,\n"
    "`association_robustness/`) so the paths resolve; the .tex searches both the\n"
    "upload directory and the repository layout\n"
    "(`\\graphicspath{{./}{../download/}}`). The v19 package: 37 pp.\n"
    "Upload `journal_manuscript_v19_bmb_refs.tex` (not the v18 refs\n"
    "name) together with the .tex.",
    "Build note: for Overleaf or any standalone compiler, upload **the ZIP** (it\n"
    "contains the .tex, the input'ed reference list, the .bib database, and all\n"
    "six figures at the exact relative subpaths the .tex expects — verified to\n"
    "compile standalone, 37 pp, 0 errors). If instead you upload individual\n"
    "files, upload them together with `journal_manuscript_v20_dam_refs.tex` and\n"
    "the three figure subfolders (`m1_m3/`, `alexandrov_bridge/`,\n"
    "`association_robustness/`) so the paths resolve; the .tex searches both the\n"
    "upload directory and the repository layout\n"
    "(`\\graphicspath{{./}{../download/}}`). The v20 package: 37 pp.\n"
    "Upload `journal_manuscript_v20_dam_refs.tex` (not the v19 refs\n"
    "name) together with the .tex.",
    "Paper 1 build note")

# ---- 6. Paper 2 section: header, title, journal links, submission route -
rep("## Paper 2 (Companion) — Theory and Applications of Categories",
    "## Paper 2 (Companion) — Discover Applied Mathematics (Springer Nature)",
    "Paper 2 section header")

rep("**Title:** Stratified Connections, Optic Composition, and the Homotopy\n"
    "Fixed-Point Extension: A Categorical Framework for Viability-Weighted\n"
    "Curvature (Research Article; 75 pp current build; electronic-only, free — no author charges).",
    "**Title:** A Geometric and Category-Theoretic Theory of Viability: How\n"
    "Sequential Adaptations Induce Path-Dependent Risk (Research Article;\n"
    "76 pp).",
    "Paper 2 title (actual current title; the stale pre-v11 title removed)")

rep("### Journal / submission links (all verified)\n"
    "\n"
    "| Resource | Link |\n"
    "|---|---|\n"
    "| Journal home | http://www.tac.mta.ca/tac/ |\n"
    "| Author information (format for submission) | http://www.tac.mta.ca/tac/authinfo.html |\n"
    "| Editorial board / general info | http://www.tac.mta.ca/tac/geninfo.html |\n"
    "| Managing Editor contact | tac@mta.ca |"
    "\n| Chosen Transmitting Editor | Prof. Michael Shulman, University of San Diego — shulman (at) sandiego.edu (verified on the live TAC board; HoTT/higher-category expertise) |",
    "### Journal / submission links (DAM links live-verified this round;\n"
    "### TAC links retained for history)\n"
    "\n"
    "| Resource | Link |\n"
    "|---|---|\n"
    "| Journal home (Springer Nature) | https://link.springer.com/journal/44585 |\n"
    "| Submission guidelines (Snapp; abstract < 250; single-anonymous; numeric square-bracket citations) | https://link.springer.com/journal/44585/submission-guidelines |\n"
    "| TAC journal home (historical, v10-v12 rounds) | http://www.tac.mta.ca/tac/ |\n"
    "| TAC author information (historical) | http://www.tac.mta.ca/tac/authinfo.html |",
    "Paper 2 journal links table")

rep("Submission route (from the official author information, fetched and verified):\n"
    "submit the article as **a PDF compiled from TeX source to any member of the\n"
    "Editorial Board except the Managing Editor or TeXnical editors**, copying\n"
    "every submission to the Managing Editor at **tac@mta.ca**; an article may be\n"
    "submitted to only one Editor; TeX source plus a compiled PDF are required\n"
    "only after acceptance. Review model: **not anonymized** -- the\n"
    "author information page (fetched and verified in full) contains no\n"
    "anonymization provisions, and submissions go by email to a named\n"
    "Editorial Board member, so the author identity is on the paper; TAC\n"
    "also asks that the final accepted source include keywords and an AMS\n"
    "2020 Subject Classification for external indexing (both now present\n"
    "below the abstract of the submitted PDF).",
    "Submission route (from the live DAM submission guidelines, re-verified\n"
    "this round): submissions are made using **Snapp**, the journal's\n"
    "manuscript tracking system; for all article types the journal requires\n"
    "the manuscript file, an abstract of less than 250 words, and a cover\n"
    "letter; article type **Research**. Review model: **single-anonymous**\n"
    "(reviewers know the author identity; the reviewer reports provided to\n"
    "authors are anonymous), so the author identity stays on the paper.\n"
    "Citations: numeric, square-bracket. All articles are published open\n"
    "access. The keywords and the AMS 2020 Subject Classification\n"
    "(18D05; 18N99; 92B05) are retained below the abstract. Historical\n"
    "route: the TAC email-to-board-member route (v10-v12 rounds),\n"
    "superseded by the DAM target.",
    "Paper 2 submission route")

# ---- 7. Paper 2 package rows ---------------------------------------------
rep("| **One-file upload ZIP (compile-ready)** | — | "
    "[download/submission_companion_tac.zip](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/submission_companion_tac.zip) |",
    "| **One-file upload ZIP (compile-ready, DAM README; fresh-dir verified 76 pp)** | — | "
    "[download/submission_companion_dam.zip](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/submission_companion_dam.zip) |",
    "Paper 2 ZIP row")

rep("| Manuscript PDF (76 pp; V12 companion-comprehension round -- abstract fragment repair, plan-of-the-paper paragraph mapping all sections with the two-sevens disambiguation, experiment-framing sentences in the two computational sections; every theorem, proof, and number unchanged from v11 (audit_v29 349/349); clickable email and ORCID; prior versions retained as separate files) | "
    "[download/companion_categorical_v12.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v12.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/companion_categorical_v12.pdf) |",
    "| Manuscript PDF (76 pp; V13 DAM round -- the review's F2 applied: the six-axis abstract sentence now covers all three body categories (regime switches and nitrogen-source substitution); DAM alignment: abstract 248 < 250 words, keywords 9 -> 6, numeric square-bracket citations, the zai2026measure cross-citation title aligned to the v20 application title; every theorem, proof, and number unchanged from v12 (audit_v30 359/359); clickable email and ORCID; prior versions retained as separate files) | "
    "[download/companion_categorical_v13.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/companion_categorical_v13.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/companion_categorical_v13.pdf) |",
    "Paper 2 manuscript PDF row")

rep("| Cover letter | [download/cover_letter_tac.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_tac.md) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_tac.md) |",
    "| Cover letter -- DAM (primary, Research Article; declarations, application-paper disclosure, v13 title) | "
    "[download/cover_letter_dam_companion.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_dam_companion.md) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/cover_letter_dam_companion.md) |\n"
    "| Cover letter -- TAC (historical, v12 round) | "
    "[download/cover_letter_tac.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_tac.md) |",
    "Paper 2 cover letter rows")

rep("| LaTeX source | [scripts/companion_categorical_v12.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v12.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v12.tex) |",
    "| LaTeX source | [scripts/companion_categorical_v13.tex](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_categorical_v13.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_categorical_v13.tex) |",
    "Paper 2 LaTeX source row")

rep("| BibTeX database (V12: byte-identical copy of the v11 database) | "
    "[scripts/companion_refs_v12.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v12.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_refs_v12.bib) |",
    "| BibTeX database (V13: the zai2026measure title aligned to the v20 application title; otherwise byte-identical to the v12 database) | "
    "[scripts/companion_refs_v13.bib](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/companion_refs_v13.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/companion_refs_v13.bib) |",
    "Paper 2 BibTeX row")

# ---- 8. pre-submission checklist -----------------------------------------
rep("Resolved (V19 comprehension-restructure round, 2026-09-23, BMB\n"
    "target): the JTB desk-rejection diagnosis addressed",
    "Resolved (V20/V13 Discover Applied Mathematics round, 2026-09-24):\n"
    "the F1-F7 causal-coherence/prose-alignment findings applied on NEW\n"
    "versioned files (main v20 from v19, companion v13 from v12; the\n"
    "earlier versions untouched) -- F3 the direct per-gene trajectory\n"
    "rank correlation reported (rho = +0.92 P1 / +0.96 P2, 424 shared\n"
    "genes, computed from the deposited per-gene artifacts); F4 the\n"
    "two-regime GC qualifier; F5 three near-identity wordings corrected;\n"
    "F6 the translation-buffering mechanism hedged and the title\n"
    "narrowed; F1 the audit count refreshed (359); F7 moot; F2 the\n"
    "companion six-axis sentence completed (nitrogen-source\n"
    "substitution); DAM venue alignment on both manuscripts (numeric\n"
    "square-bracket citations, Fig.-label captions, abstracts 245/248\n"
    "< 250, companion keywords 6, cross-citation titles aligned both\n"
    "directions); audit_v30_numbers.py 359/359 PASS; tectonic 37/76 pp,\n"
    "0 errors / 0 '??'; v25 ZIPs (submission_main_dam.zip,\n"
    "submission_companion_dam.zip) fresh-dir verified; DAM cover\n"
    "letters for both papers. Earlier rounds resolved: the V19\n"
    "comprehension-restructure round, 2026-09-23 (then BMB target):\n"
    "the JTB desk-rejection diagnosis addressed",
    "pre-submission checklist resolved paragraph")

rep("Remaining at submission time: only the BMB Editorial Manager account\n"
    "(https://www.editorialmanager.com/bmab/, code bmab) -- then upload\n"
    "the manuscript ZIP contents (or the single PDF) and\n"
    "download/cover_letter_bmb.md as the cover letter. Fallback paths\n"
    "(PLOS Comp Bio, Mathematical Biosciences) remain documented in\n"
    "download/V17_Venue_Evaluation.md. Resolved this round: the cover-letter dates are filled\n"
    "(September 17, 2026, both letters) and the TAC receiving board member\n"
    "is selected -- Prof. Michael Shulman (University of San Diego), Transmitting\n"
    "Editor, with the submission emailed to her and copied to tac@mta.ca\n"
    "per TAC's author information (any Editorial Board member except the\n"
    "Managing Editor or TeXnical editors).",
    "Remaining at submission time: only the Snapp account (submissions to\n"
    "Discover Applied Mathematics are made via Snapp, the journal's\n"
    "manuscript tracking system; guidelines at\n"
    "https://link.springer.com/journal/44585/submission-guidelines) --\n"
    "then upload the manuscript file (the ZIP compiles standalone, or\n"
    "upload the single PDF), the abstract is in the manuscript, and use\n"
    "download/cover_letter_dam.md (main) /\n"
    "download/cover_letter_dam_companion.md (companion) as the cover\n"
    "letter. The historical routes (BMB Editorial Manager, TAC email\n"
    "submission with Prof. Shulman as Transmitting Editor) are\n"
    "superseded by the DAM target; fallback paths remain documented in\n"
    "download/V17_Venue_Evaluation.md.",
    "pre-submission checklist remaining paragraph")

open(P, "w", encoding="utf-8").write(doc)
print("[update_links_doc_v25] applied:", "; ".join(applied))
print(f"[update_links_doc_v25] wrote {P} ({len(doc)} chars) [ALL EDITS DONE]")
