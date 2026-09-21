#!/usr/bin/env python3
"""Update download/SUBMISSION_PACKAGE_LINKS.md for the v17 round.

Adds the newest-first revision note (v17 enrichment + venue
evaluation + v20 ZIPs), retargets the Paper 1 package rows to the
v17 files (also repairing the stale v15 raw links), updates the
Paper 1 header (current title, 38 pp, venue status), and refreshes
the checklist audit line.
"""

p = "download/SUBMISSION_PACKAGE_LINKS.md"
t = open(p).read()

# 1. header generation line + newest-first note
t = t.replace(
    "Generated 2026-09-18 (universal Gemini-adoption round + v19 package\n"
    "round: journal_manuscript_v16 + companion_categorical_v10).",
    "Generated 2026-09-21 (V17 enrichment + venue-evaluation round + v20\n"
    "package round: journal_manuscript_v17 + companion_categorical_v10).")

note = """
Revision note (2026-09-21, V17 enrichment round + venue-evaluation
round + v20 package round): the committed V17 revision plan
(download/V17_Revision_Plan.md, commit 4776f2d) and its computed
insight ledger (download/v17_insight_substantiation.json +
download/V17_Insight_Development.md, commit 74934d0) were implemented
on a NEW versioned file -- scripts/journal_manuscript_v17.tex (from
v16, v16 untouched) + journal_manuscript_v17_bmb_refs.tex (27 -> 29
entries: kacser1973 + heinrich1974) + journal_manuscript_v17_refs.bib.
ADDED CONTENT (all in the paper's humanized Gemini register, every
number from the deposited ledger): Sec. 2 "A worked example" (three
chambers, two walls, one growth-silent; machine-verified by
scripts/v17_worked_example_verify.py, 16/16, deposited as
download/v17_worked_example_verification.json); Sec. 4 "The chemical
coordinates of the walls" (Table tab:walls: the twenty branch
metabolites carrying 59.7% of curvature mass) + "A conserved interior
architecture" (the revised Line-V claim: walls on internal
branch-point chemistry, flat exchange interface) + "Construction
order as a design variable" (the order rule with its honest null);
Sec. 5 "Anatomy of one switch" (Table tab:regulons: eleven enriched
regulons led by CRP q = 8.6e-16; operon granularity with the GPR
disjoint-reaction control; the growth-silent partition 0/433 on all
three paths); Discussion "Relation to metabolic control analysis"
(Kacser-Burns / Heinrich-Rapoport) + "Where metabolic memory lives"
(the memory-substrate deduction); the abstract rebuilt with the
bio-anchoring sentences at 254 words under the 255 cap; Limitations
item 8 (enrichment and prediction provenance); Methods enrichment
protocols. VENUE EVALUATION delivered per the author question "can
we resubmit to BMB?": download/V17_Venue_Evaluation.md -- verdict:
BMB resubmission mechanically possible but not advisable as a blind
new submission (desk verdict was a fit judgment; pre-submission
inquiry draft included in the memo); primary recommendation JTB
(regulatory-FBA lineage, Covert-Schilling-Palsson JTB 213:73
precedent; cover_letter_jtb.md written); PLOS Comp Bio the
biology-maximizing alternative (Machado 2014 genre precedent, APC ~
US$2.5k); companion/TAC unaffected. VERIFIED: audit_v25_numbers.py
(make_audit_v25.py from audit_v24, retargeted to v17) 344/344 PASS
(301 carried + 43 new V17 checks); pattern_sweep_v16 16/16 clean;
verify_v17_completeness.py ALL COMPLETE (removed tokens exactly the
abstract's partial-r re-quote and the two 301 audit counts; added
tokens confined to the v17 fragments; +9 labels; +2 tables; +7
subsections; refs +2); tectonic main 38 pp / companion 76 pp, 0
errors / 0 undefined / 0 '??'; VLM CLEAN on all 12 new-content
pages (pp. 8-9, 12-18, 23-25); v20 ZIPs
(build_submission_zips_v20.sh) with fresh-dir standalone compiles
re-verified (38/76 pp); download copies and ZIP contents
byte-identical to scripts; BMB cover letter rewritten as the
transparent resubmission-aware version (prior desk decision flagged
in sentence one, point-by-point response, 344-check audit line);
JTB cover letter written; this checklist updated.

"""
anchor = "Revision note (2026-09-18, universal Gemini-adoption round"
assert anchor in t
t = t.replace(anchor, note.lstrip("\n") + anchor, 1)

# 2. Paper 1 header: current title, page count, venue status
t = t.replace(
    "**Title:** A Measure-Theoretic Discrete Curvature Framework for Metabolic Gene\n"
    "Sensitivity: From Active-Set Geometry to Transcriptional Response\n"
    "(Original Research Article; 29 pp; subscription route — no author charges).",
    "**Title:** A Geometric Theory of Metabolic Flux Rerouting: How\n"
    "Active-Set Curvature Predicts Transcriptional Regulation and\n"
    "Protein-Layer Buffering (Original Research Article; 38 pp).\n\n"
    "**Venue status (2026-09-21):** BMB desk-rejected the earlier\n"
    "version (\"biological impact and implications not sufficiently\n"
    "strong for our readership\"). The V17 enrichment addresses that\n"
    "verdict with computed, named-biology substance. Recommendation in\n"
    "download/V17_Venue_Evaluation.md: **JTB primary** (cover letter\n"
    "download/cover_letter_jtb.md); **BMB only via pre-submission\n"
    "inquiry** (draft inside the memo; the resubmission-aware BMB\n"
    "letter is download/cover_letter_bmb.md); **PLOS Comp Bio** the\n"
    "biology-maximizing alternative (APC). The package below is\n"
    "venue-neutral and compiles identically for all three.")

# 3. Package rows: retarget v16 -> v17 (and repair the stale v15 raw
#    links that the v16 round left behind)
t = t.replace(
    "| Manuscript PDF (33 pp, full proofs in appendices, declarations in backmatter; universal verbatim adoption of Gemini's rewrite -- abstract rebuilt on Gemini's own abstract at the 255-word cap opening with Gemini's first sentence, Gemini's title and keywords, intro narrative, five-findings claim list, section narratives, Discussion in Gemini's three subsections; clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v16.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v15.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v15.pdf) |",
    "| Manuscript PDF (38 pp, full proofs in appendices, declarations in backmatter; v17 enrichment round on the Gemini-register base: worked example, wall coordinates, interior architecture, construction-order rule, anatomy of one switch, MCA comparison, memory-substrate deduction; abstract bio-anchored at the 254-word cap; clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v17.pdf](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/journal_manuscript_v17.pdf) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/journal_manuscript_v17.pdf) |")
t = t.replace(
    "| LaTeX source | [scripts/journal_manuscript_v16.tex]",
    "| LaTeX source | [scripts/journal_manuscript_v17.tex]")
t = t.replace(
    "blob/main/scripts/journal_manuscript_v16.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v16.tex)",
    "blob/main/scripts/journal_manuscript_v17.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v17.tex)")
t = t.replace(
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v16_bmb_refs.tex]",
    "| Reference list (alphabetical, 29 entries -- kacser1973 + heinrich1974 added) | [scripts/journal_manuscript_v17_bmb_refs.tex]")
t = t.replace(
    "blob/main/scripts/journal_manuscript_v16_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v16_bmb_refs.tex)",
    "blob/main/scripts/journal_manuscript_v17_bmb_refs.tex) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v17_bmb_refs.tex)")
t = t.replace(
    "| BibTeX database | [scripts/journal_manuscript_v16_refs.bib]",
    "| BibTeX database | [scripts/journal_manuscript_v17_refs.bib]")
t = t.replace(
    "blob/main/scripts/journal_manuscript_v16_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v16_refs.bib)",
    "blob/main/scripts/journal_manuscript_v17_refs.bib) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/journal_manuscript_v17_refs.bib)")
t = t.replace(
    "| Cover letter (with declarations, companion disclosure) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md)",
    "| Cover letter -- JTB (primary recommendation; declarations, companion disclosure) | [download/cover_letter_jtb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_jtb.md) |\n"
    "| Cover letter -- BMB resubmission-aware version (prior desk decision flagged) | [download/cover_letter_bmb.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/cover_letter_bmb.md) |")
# venue evaluation row after the ZIP row
t = t.replace(
    "| **One-file upload ZIP (compile-ready)** | — | [download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_bmb.zip) |",
    "| **One-file upload ZIP (compile-ready, venue-neutral)** | — | [download/submission_main_bmb.zip](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/submission_main_bmb.zip) |\n"
    "| Venue evaluation (BMB resubmission analysis + recommendation + pre-submission inquiry draft) | [download/V17_Venue_Evaluation.md](https://github.com/MIKEAA2020/metabolic-curvature-measure/blob/main/download/V17_Venue_Evaluation.md) | [raw](https://raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/V17_Venue_Evaluation.md) |")
# build note: v16 -> v17 file pointer + page count
t = t.replace(
    "upload them together with `journal_manuscript_v16_bmb_refs.tex` and",
    "upload them together with `journal_manuscript_v17_bmb_refs.tex` and")
t = t.replace("compile standalone, 30 pp, 0 errors)",
              "compile standalone, 38 pp, 0 errors)")

# 4. checklist audit line refresh
t = t.replace(
    "constructions; audit_v23 301/301\nPASS against journal_manuscript_v16.tex + companion_categorical_v10.tex;\nno-fee venue for both.",
    "constructions; audit_v25 344/344\nPASS against journal_manuscript_v17.tex + companion_categorical_v10.tex.\nVENUE (2026-09-21): BMB desk rejection superseded -- JTB primary\nrecommendation (no APC), PLOS Comp Bio the bio-first alternative\n(APC), BMB return only via pre-submission inquiry; decision memo\nand both letters in download/. TAC unchanged (no-fee).")
t = t.replace(
    "Remaining at submission time: register/log in at the BMB Editorial\nManager portal.",
    "Remaining at submission time: the author's venue decision (JTB vs\nPLOS Comp Bio vs the BMB pre-submission inquiry path), then the\nportal account (Editorial Manager bmab for BMB, Elsevier EM for JTB,\nor PLOS Submission System).")

open(p, "w").write(t)
print("links doc updated")
