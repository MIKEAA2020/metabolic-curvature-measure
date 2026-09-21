#!/usr/bin/env python3
"""update_links_doc_v21.py -- retarget SUBMISSION_PACKAGE_LINKS.md to the
v18 JTB-alignment round: newest-first revision note, Paper 1 section
retitled to the Journal of Theoretical Biology (live-verified portal
links), package rows retargeted to journal_manuscript_v18 +
submission_main_jtb.zip + highlights_jtb.docx, and the pre-submission
checklist updated (JTB requirements resolved; portal account remains)."""

P = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
doc = open(P).read()


def rep(old, new, tag):
    global doc
    assert doc.count(old) == 1, f"anchor not unique for {tag}"
    doc = doc.replace(old, new)
    print("-", tag)


# ---- 1. header line ------------------------------------------------------
rep("Generated 2026-09-21 (V17 enrichment + venue-evaluation round + v20\n"
    "package round: journal_manuscript_v17 + companion_categorical_v10). "
    "All repository links follow",
    "Generated 2026-09-21 (V18 JTB-alignment round + v21 package round:\n"
    "journal_manuscript_v18 + companion_categorical_v10; supersedes the\n"
    "V17 enrichment + venue-evaluation + v20 package round). All repository\n"
    "links follow", "header round line")

# ---- 2. newest-first revision note ----------------------------------------
NOTE = """Revision note (2026-09-21, V18 JTB-alignment round + v21 package
round): the author confirmed the JTB venue, so the main manuscript was
retargeted on a NEW versioned file -- scripts/journal_manuscript_v18.tex
(from v17; v17 and all earlier versions untouched) via
scripts/v18_jtb_alignment.py, with the full JTB Guide for Authors
verified live (abstract "does not exceed 250 words"; keywords 1-7;
Highlights REQUIRED as a separate editable file, 3-5 bullets <= 85
characters, featuring biological applications and theoretical
advancements; CRediT authorship contribution statement; 'Regular
Article' type): (1) abstract trimmed 254 -> 249 audit-style words via
five word-level trims, every number, gloss, and connective kept;
(2) keywords 6 -> 7, adding 'path dependence' (indexes the holonomy,
66% non-reversion, construction-order, and memory findings); (3) the
Author Contributions backmatter recast as the CRediT taxonomy
statement; (4) the reference list carried to the venue-neutral
journal_manuscript_v18_refs.tex (29 entries byte-identical to the v17
list) + journal_manuscript_v18_refs.bib; (5) the header comment
retargeted BMB -> JTB. NEW REQUIRED FILE: download/highlights_jtb.docx
(scripts/v18_make_highlights.js; 5 bullets, lengths 66/69/72/76/76
characters, all <= 85; postcheck 9/9) -- upload it as its own file in
the JTB submission system. Package renamed
submission_main_bmb.zip -> submission_main_jtb.zip (v21 ZIPs,
build_submission_zips_v21.sh) with a JTB-specific README; the
companion/TAC package unchanged. VERIFIED: audit_v26_numbers.py
(make_audit_v26.py) 347/347 PASS (344 carried v25 checks + 3 new JTB
gates: CRediT, 7-term keywords, highlights file);
pattern_sweep_v16 16/16 clean on both; verify_v18_completeness.py
ALL COMPLETE (numeric delta = the \\input filename version digit
only; labels/citations/environments/sections/bibliography identical;
2,646 v17 body lines preserved verbatim); tectonic main 38 pp, 0
errors / 0 undefined / 0 '??'; clickable mailto + ORCID via qpdf;
VLM CLEAN on the changed pages (p1 abstract/keywords, p37 CRediT);
v21 ZIPs fresh-dir re-verified 38/76 pp; download copies byte-identical.
Cover letter retargeted to 'Regular Article' + the 347-check audit
count. Remaining at submission time: the JTB Editorial Manager
account only.

"""
rep("Revision note (2026-09-21, V17 enrichment round + venue-evaluation\n"
    "round + v20 package round):",
    NOTE + "Revision note (2026-09-21, V17 enrichment round + venue-evaluation\n"
    "round + v20 package round):", "newest-first v18 revision note")

# ---- 3. Paper 1 heading + title + venue status ----------------------------
rep("## Paper 1 (Main) — Bulletin of Mathematical Biology",
    "## Paper 1 (Main) — Journal of Theoretical Biology (Elsevier)",
    "paper 1 heading")

rep("""**Title:** A Geometric Theory of Metabolic Flux Rerouting: How
Active-Set Curvature Predicts Transcriptional Regulation and
Protein-Layer Buffering (Original Research Article; 38 pp).

**Venue status (2026-09-21):** BMB desk-rejected the earlier
version ("biological impact and implications not sufficiently
strong for our readership"). The V17 enrichment addresses that
verdict with computed, named-biology substance. Recommendation in
download/V17_Venue_Evaluation.md: **JTB primary** (cover letter
download/cover_letter_jtb.md); **BMB only via pre-submission
inquiry** (draft inside the memo; the resubmission-aware BMB
letter is download/cover_letter_bmb.md); **PLOS Comp Bio** the
biology-maximizing alternative (APC). The package below is
venue-neutral and compiles identically for all three.""",
    """**Title:** A Geometric Theory of Metabolic Flux Rerouting: How
Active-Set Curvature Predicts Transcriptional Regulation and
Protein-Layer Buffering (Regular Article; 38 pp).

**Venue status (2026-09-21, V18 round):** the venue decision is
**JTB (confirmed)** per the author directive; the v18 round aligns
the full package to the live JTB Guide for Authors (abstract 249
words under the 250 cap; 7 keywords; CRediT statement; the required
separate Highlights file download/highlights_jtb.docx; cover letter
download/cover_letter_jtb.md retargeted to Regular Article). The
package itself is venue-neutral and compiles identically for any
Elsevier/Springer target. Fallback paths remain documented in
download/V17_Venue_Evaluation.md: BMB return only via
pre-submission inquiry (resubmission-aware letter
download/cover_letter_bmb.md, superseded package naming), PLOS
Comp Bio the biology-maximizing alternative (APC).""",
    "paper 1 title + venue status")

# ---- 4. journal links table ------------------------------------------------
rep("""### Journal / submission-portal links (all verified)

| Resource | Link |
|---|---|
| Journal home (Springer) | https://link.springer.com/journal/11538 |
| Submission guidelines | https://link.springer.com/journal/11538/submission-guidelines |
| How to publish with us | https://link.springer.com/journal/11538/how-to-publish-with-us |
| Submission portal (Editorial Manager) | https://www.editorialmanager.com/bmab |
| Society page (SMB, official journal of the society) | https://smb.org/Bulletin-of-Mathematical-Biology |

> Review model (verified via the SMB society page): single-blind peer review -- the author identity is known to reviewers, and the name, affiliation, corresponding e-mail, and ORCID are on the title page as the Springer Title Page guideline requires.
>
> Portal code verified as **bmab** (via the SMB society page and multiple
> journal directories). Do not confuse with `editorialmanager.com/jomb`,
> which is the *Journal of Mathematical Biology* — a different Springer journal.""",
    """### Journal / submission-portal links (all verified live 2026-09-21)

| Resource | Link |
|---|---|
| Journal home (Elsevier) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology |
| Guide for Authors (abstract <= 250 words; keywords 1-7; Highlights required; CRediT) | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/publish/guide-for-authors |
| Submit portal | https://submit.elsevier.com/JTB (resolves to Editorial Manager) |
| Editorial Manager (direct) | https://www.editorialmanager.com/JTB/ |
| Aims and scope | https://www.sciencedirect.com/journal/journal-of-theoretical-biology/about/aims-and-scope |

> Scope fit (from the live aims & scope): JTB is "the leading forum for
> theoretical perspectives that give insight into biological processes";
> papers must state the biological significance clearly, and Highlights
> must feature the biological applications as well as theoretical
> advancements -- the v18 package does both. Highly speculative or
> purely-mathematical papers are out of scope; the manuscript's
> genome-scale empirical association and named biology anchor it in
> scope. The regulatory-FBA lineage precedent: Covert, Schilling &
> Palsson, JTB 213:73-88, 2001.
>
> Fallback path (BMB pre-submission inquiry): journal home
> https://link.springer.com/journal/11538, submission guidelines
> https://link.springer.com/journal/11538/submission-guidelines,
> portal https://www.editorialmanager.com/bmab (code **bmab**, not
> `jomb`). Review model single-blind; the v18 package compiles
> identically for the Springer route.""",
    "journal links table -> JTB")

# ---- 5. package rows --------------------------------------------------------
rep("| **One-file upload ZIP (compile-ready, venue-neutral)** | — | "
    "[download/submission_main_bmb.zip](https://raw.githubusercontent.com/"
    "MIKEAA2020/metabolic-curvature-measure/main/download/"
    "submission_main_bmb.zip) |",
    "| **One-file upload ZIP (compile-ready, venue-neutral, JTB README)** "
    "| — | [download/submission_main_jtb.zip]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/submission_main_jtb.zip) |",
    "package row: jtb zip")

rep("| Venue evaluation (BMB resubmission analysis + recommendation + "
    "pre-submission inquiry draft) | [download/V17_Venue_Evaluation.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/V17_Venue_Evaluation.md) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/V17_Venue_Evaluation.md) |",
    "| **Highlights file (JTB-required separate upload, 5 bullets <= 85 "
    "chars)** | [download/highlights_jtb.docx]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/highlights_jtb.docx) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/highlights_jtb.docx) |\n"
    "| Venue evaluation (BMB resubmission analysis + recommendation + "
    "pre-submission inquiry draft) | [download/V17_Venue_Evaluation.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/V17_Venue_Evaluation.md) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/V17_Venue_Evaluation.md) |",
    "package row: highlights + venue evaluation")

rep("| Manuscript PDF (38 pp, full proofs in appendices, declarations in "
    "backmatter; v17 enrichment round on the Gemini-register base: worked "
    "example, wall coordinates, interior architecture, construction-order "
    "rule, anatomy of one switch, MCA comparison, memory-substrate "
    "deduction; abstract bio-anchored at the 254-word cap; clickable email "
    "and ORCID; prior versions retained as separate files) | "
    "[download/journal_manuscript_v17.pdf](https://github.com/MIKEAA2020/"
    "metabolic-curvature-measure/blob/main/download/"
    "journal_manuscript_v17.pdf) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "journal_manuscript_v17.pdf) |",
    "| Manuscript PDF (38 pp, v18 JTB-alignment round: all v17 enrichment "
    "content -- worked example, wall coordinates, interior architecture, "
    "construction-order rule, anatomy of one switch, MCA comparison, "
    "memory-substrate deduction -- with the abstract at 249 words under "
    "the JTB 250 cap, 7 keywords, and the CRediT statement; clickable "
    "email and ORCID; prior versions retained as separate files) | "
    "[download/journal_manuscript_v18.pdf](https://github.com/MIKEAA2020/"
    "metabolic-curvature-measure/blob/main/download/"
    "journal_manuscript_v18.pdf) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/"
    "journal_manuscript_v18.pdf) |",
    "package row: v18 pdf")

rep("| Cover letter -- JTB (primary recommendation; declarations, "
    "companion disclosure) | [download/cover_letter_jtb.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_jtb.md) |",
    "| Cover letter -- JTB (primary, Regular Article; declarations, "
    "companion disclosure) | [download/cover_letter_jtb.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_jtb.md) |",
    "package row: jtb cover letter")

rep("| Cover letter -- BMB resubmission-aware version (prior desk "
    "decision flagged) | [download/cover_letter_bmb.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_bmb.md) | | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/cover_letter_bmb.md) |",
    "| Cover letter -- BMB resubmission-aware version (fallback inquiry "
    "path; prior desk decision flagged) | [download/cover_letter_bmb.md]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/download/cover_letter_bmb.md) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/cover_letter_bmb.md) |",
    "package row: bmb cover letter (cell fix)")

rep("| LaTeX source | [scripts/journal_manuscript_v17.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v17.tex) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v17.tex) |",
    "| LaTeX source | [scripts/journal_manuscript_v18.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v18.tex) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v18.tex) |",
    "package row: v18 tex")

rep("| Reference list (alphabetical, 29 entries -- kacser1973 + "
    "heinrich1974 added) | [scripts/journal_manuscript_v17_bmb_refs.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v17_bmb_refs.tex) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v17_bmb_refs.tex) |",
    "| Reference list (alphabetical, 29 entries -- kacser1973 + "
    "heinrich1974 added; venue-neutral v18 naming) | "
    "[scripts/journal_manuscript_v18_refs.tex]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v18_refs.tex) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v18_refs.tex) |",
    "package row: v18 refs")

rep("| BibTeX database | [scripts/journal_manuscript_v17_refs.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v17_refs.bib) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v17_refs.bib) |",
    "| BibTeX database | [scripts/journal_manuscript_v18_refs.bib]"
    "(https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/"
    "main/scripts/journal_manuscript_v18_refs.bib) | [raw]"
    "(https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v18_refs.bib) |",
    "package row: v18 bib")

# ---- 6. build note ----------------------------------------------------------
rep("upload them together with `journal_manuscript_v17_bmb_refs.tex` and",
    "upload them together with `journal_manuscript_v18_refs.tex` and",
    "build note refs name")

# ---- 7. checklist -----------------------------------------------------------
rep("""Resolved: BMB-formatted main paper (natbib author-year, 27 alphabetical
refs, six keywords, v15 two-paragraph abstract in Gemini's register,
trimmed under the author's 255-word cap at 254 audit-style words
(the audit's JP-3 gate remains <= 300) -- continuous line numbering,
brief declarations in backmatter, cover letter
with companion disclosure);""",
    """Resolved (V18 JTB-alignment round, 2026-09-21): JTB-requirements
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
tectonic 38 pp 0 errors; VLM CLEAN on the changed pages. Earlier
rounds resolved:""",
    "checklist resolved block")

rep("""Remaining at submission time: the author's venue decision (JTB vs
PLOS Comp Bio vs the BMB pre-submission inquiry path), then the
portal account (Editorial Manager bmab for BMB, Elsevier EM for JTB,
or PLOS Submission System).""",
    """Remaining at submission time: only the JTB Editorial Manager account
(https://www.editorialmanager.com/JTB/, via
https://submit.elsevier.com/JTB) -- then upload the manuscript ZIP
contents (or the single PDF, per Your Paper Your Way),
download/highlights_jtb.docx as its own Highlights file, and
download/cover_letter_jtb.md as the cover letter. Fallback paths
(BMB pre-submission inquiry, PLOS Comp Bio) remain documented in
download/V17_Venue_Evaluation.md.""",
    "checklist remaining block")

open(P, "w").write(doc)
print("SUBMISSION_PACKAGE_LINKS.md updated (v18 / v21 round)")
