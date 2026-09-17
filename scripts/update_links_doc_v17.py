#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the abstract round + v16
package round (journal_manuscript_v13 + companion_categorical_v9)."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
old_head = ("Generated 2026-09-17 (brevity round + v15 package round:\n"
            "journal_manuscript_v12 + companion_categorical_v9). "
            "All repository links follow")
new_head = ("Generated 2026-09-17 (abstract round + v16 package round:\n"
            "journal_manuscript_v13 + companion_categorical_v9). "
            "All repository links follow")
assert old_head in s, "header anchor not found"
s = s.replace(old_head, new_head)

# 2. New revision note inserted before the brevity-round note
old_anchor = ("Revision note (2026-09-17, brevity round + v15 package round): the\n"
              "author directive to tighten")
new_note = """Revision note (2026-09-17, abstract round + v16 package round): the
author directive that the main-paper abstract was still too
jargon-heavy, highly technical, and inaccessible to a broad
readership, and should adopt Gemini's abstract more faithfully, was
executed as an abstract-only rebuild on NEW versioned files (prior
versions untouched) -- scripts/journal_manuscript_v13.tex (from v12)
plus its refs copies. The abstract now follows Gemini's abstract
(external_audits/humanized/curvature humanized.txt L721-725) in
structure and register: two paragraphs (theory; biology), its
definition -> "We measure how this map bends" -> evidence ->
refinement--resolution bridge -> "From this measure" -> "Strikingly"
-> "Finally" -> "Our results unify" arc, in-words glosses for h and
L_var, full-sentence connectives replacing the compressed
telegraphic clauses, and the plain field-level closer (multi-
parametric linear programming, discrete differential geometry,
transcriptional regulation). The protein-layer dissociation now
carries its measured numbers (r = -0.083 across 366 genes, matched
quantitative proteomics); robustness stays one non-defensive
sentence per the M1 adjudication; every number is an audited body
claim (269 audit-style words; the audit's JP-3 gate is <= 300).
Nothing lost: the body is byte-identical to v12 outside the
abstract (verify_v13_completeness.py: body identity, number
multiset fully explained -- only the two re-quoted body numbers
added -- and label/citation/environment/section censuses plus the
bibliography all identical). Verified: audit_v21_numbers.py
(make_audit_v21.py) 301/301 PASS; pattern_sweep_v16 16/16 clean on
both; tectonic main 30 pp / companion 75 pp, 0 errors / 0 undefined
references; clickable mailto + ORCID annotations verified via qpdf;
VLM render checks of pages 1-2 CLEAN (two-paragraph abstract, no
typographic defects, blue underlined contacts); ZIPs rebuilt via
build_submission_zips_v16.sh with fresh-dir standalone compiles
re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v13.

""" + old_anchor
assert old_anchor in s, "revision-note anchor not found"
s = s.replace(old_anchor, new_note)

# 3. Retarget current-package rows (main) v12 -> v13
s = s.replace(
    "| Manuscript PDF (30 pp, full proofs in appendices, declarations in "
    "backmatter; universal Gemini-register revision of narrative prose "
    "throughout, clickable email and ORCID, brevity round applied; prior "
    "versions retained as separate files) | "
    "[download/journal_manuscript_v12.pdf](",
    "| Manuscript PDF (30 pp, full proofs in appendices, declarations in "
    "backmatter; universal Gemini-register revision of narrative prose "
    "throughout, clickable email and ORCID, brevity round applied, "
    "abstract rebuilt on Gemini's abstract; prior versions retained as "
    "separate files) | [download/journal_manuscript_v13.pdf](")
s = s.replace(
    "blob/main/download/journal_manuscript_v12.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/journal_manuscript_v12.pdf)",
    "blob/main/download/journal_manuscript_v13.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/journal_manuscript_v13.pdf)")
s = s.replace(
    "| LaTeX source | [scripts/journal_manuscript_v12.tex](",
    "| LaTeX source | [scripts/journal_manuscript_v13.tex](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v12.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/journal_manuscript_v12.tex)",
    "blob/main/scripts/journal_manuscript_v13.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/journal_manuscript_v13.tex)")
s = s.replace(
    "| Reference list (BMB alphabetical, 27 entries) | "
    "[scripts/journal_manuscript_v12_bmb_refs.tex](",
    "| Reference list (BMB alphabetical, 27 entries) | "
    "[scripts/journal_manuscript_v13_bmb_refs.tex](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v12_bmb_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v12_bmb_refs.tex)",
    "blob/main/scripts/journal_manuscript_v13_bmb_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v13_bmb_refs.tex)")
s = s.replace(
    "| BibTeX database | [scripts/journal_manuscript_v12_refs.bib](",
    "| BibTeX database | [scripts/journal_manuscript_v13_refs.bib](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v12_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v12_refs.bib)",
    "blob/main/scripts/journal_manuscript_v13_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v13_refs.bib)")

# 4. Build note retarget
s = s.replace(
    "files, upload them together with `journal_manuscript_v12_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v13_bmb_refs.tex` and")

open(p, "w").write(s)

# 5. Verify no current-package v12 rows remain (historical notes keep theirs)
import re
rows = re.findall(r"\| [^|\n]*\| \[scripts/journal_manuscript_v12", s)
assert not rows, f"stale v12 current-rows: {rows}"
print("SUBMISSION_PACKAGE_LINKS.md updated to the v13/v9 + v16 round;",
      len(s), "bytes")
