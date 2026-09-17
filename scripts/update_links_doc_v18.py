#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the abstract cap round + v17
package round (journal_manuscript_v14 + companion_categorical_v9)."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
old_head = ("Generated 2026-09-17 (abstract round + v16 package round:\n"
            "journal_manuscript_v13 + companion_categorical_v9). "
            "All repository links follow")
new_head = ("Generated 2026-09-17 (abstract cap round + v17 package round:\n"
            "journal_manuscript_v14 + companion_categorical_v9). "
            "All repository links follow")
assert old_head in s, "header anchor not found"
s = s.replace(old_head, new_head)

# 2. New revision note inserted before the v13-round note
old_anchor = ("Revision note (2026-09-17, abstract round + v16 package round): the\n"
              "author directive that the main-paper abstract was still too")
new_note = """Revision note (2026-09-17, abstract cap round + v17 package round): the
author directive to keep the abstract close to Gemini's register while
not exceeding 255 words (the v13 abstract stood at 269 audit-style
words) was executed as an abstract-only trim on NEW versioned files
(prior versions untouched) -- scripts/journal_manuscript_v14.tex (from
v13) plus its refs copies. The register and structure are kept exactly
as rebuilt in the abstract round (two paragraphs; definition -> "We
measure how this map bends" -> evidence -> refinement--resolution
bridge -> "From this measure" -> "Strikingly" -> "Finally" -> "Our
results unify"; in-words glosses for h and L_var). The 15-word trim
removes only Gemini-side redundancy and statistics conventions: the
M1 sweep qualifier after the 93.4-100.0% range (the range itself
already encodes the sweep variability; Gemini's sentence ends there),
"n = 424 evaluated genes" -> "424 genes" (Gemini's own plain form),
"fails in general" -> "fails generically" (Gemini's exact word), the
boundaries gloss compressed to "the boundaries between active
constraint sets", "the measured window" -> "the window", and two
function words tightened. Result: 254 audit-style words (~238
rendered), under the 255 cap. Nothing lost: the body is
byte-identical to v13 outside the abstract (verify_v14_completeness.py:
body identity; number multiset delta = the version digit only, the
abstract swap changed zero numeric tokens; label/citation/environment/
section censuses and the bibliography all identical). Verified:
audit_v22_numbers.py (make_audit_v22.py) 301/301 PASS;
pattern_sweep_v16 16/16 clean on both; tectonic main 30 pp /
companion 75 pp, 0 errors / 0 undefined references; clickable mailto
+ ORCID annotations verified via qpdf; ZIPs rebuilt via
build_submission_zips_v17.sh with fresh-dir standalone compiles
re-verified (30/75 pp); download copies and ZIP contents
byte-identical to scripts; TAC cover letter retargeted to v14.

""" + old_anchor
assert old_anchor in s, "revision-note anchor not found"
s = s.replace(old_anchor, new_note)

# 3. Retarget current-package rows (main) v13 -> v14
s = s.replace(
    "| Manuscript PDF (30 pp, full proofs in appendices, declarations in "
    "backmatter; universal Gemini-register revision of narrative prose "
    "throughout, clickable email and ORCID, brevity round applied, "
    "abstract rebuilt on Gemini's abstract; prior versions retained as "
    "separate files) | [download/journal_manuscript_v13.pdf](",
    "| Manuscript PDF (30 pp, full proofs in appendices, declarations in "
    "backmatter; universal Gemini-register revision of narrative prose "
    "throughout, clickable email and ORCID, brevity round applied, "
    "abstract rebuilt on Gemini's abstract and trimmed under the author's "
    "255-word cap; prior versions retained as separate files) | "
    "[download/journal_manuscript_v14.pdf](")
s = s.replace(
    "blob/main/download/journal_manuscript_v13.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/journal_manuscript_v13.pdf)",
    "blob/main/download/journal_manuscript_v14.pdf) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/download/journal_manuscript_v14.pdf)")
s = s.replace(
    "| LaTeX source | [scripts/journal_manuscript_v13.tex](",
    "| LaTeX source | [scripts/journal_manuscript_v14.tex](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v13.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/journal_manuscript_v13.tex)",
    "blob/main/scripts/journal_manuscript_v14.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/journal_manuscript_v14.tex)")
s = s.replace(
    "| Reference list (BMB alphabetical, 27 entries) | "
    "[scripts/journal_manuscript_v13_bmb_refs.tex](",
    "| Reference list (BMB alphabetical, 27 entries) | "
    "[scripts/journal_manuscript_v14_bmb_refs.tex](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v13_bmb_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v13_bmb_refs.tex)",
    "blob/main/scripts/journal_manuscript_v14_bmb_refs.tex) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v14_bmb_refs.tex)")
s = s.replace(
    "| BibTeX database | [scripts/journal_manuscript_v13_refs.bib](",
    "| BibTeX database | [scripts/journal_manuscript_v14_refs.bib](")
s = s.replace(
    "blob/main/scripts/journal_manuscript_v13_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v13_refs.bib)",
    "blob/main/scripts/journal_manuscript_v14_refs.bib) | "
    "[raw](https://raw.githubusercontent.com/MIKEAA2020/"
    "metabolic-curvature-measure/main/scripts/"
    "journal_manuscript_v14_refs.bib)")

# 4. Build note retarget
s = s.replace(
    "files, upload them together with `journal_manuscript_v13_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v14_bmb_refs.tex` and")

# 5. Checklist: abstract line + current audit status
s = s.replace(
    "Resolved: BMB-formatted main paper (natbib author-year, 27 alphabetical\n"
    "refs, six keywords, v13 two-paragraph abstract rebuilt on Gemini's\n"
    "abstract at ~260 words -- the register-fidelity trade-off accepted in\n"
    "the abstract round; the audit's JP-3 gate caps at 300 and passes at\n"
    "269 audit-style words -- continuous line numbering, brief declarations\n"
    "in backmatter, cover letter",
    "Resolved: BMB-formatted main paper (natbib author-year, 27 alphabetical\n"
    "refs, six keywords, v14 two-paragraph abstract in Gemini's register,\n"
    "trimmed under the author's 255-word cap at 254 audit-style words\n"
    "(the audit's JP-3 gate remains <= 300) -- continuous line numbering,\n"
    "brief declarations in backmatter, cover letter")
s = s.replace(
    "audit_v18 301/301\n"
    "PASS against journal_manuscript_v10.tex + companion_categorical_v8.tex;",
    "audit_v22 301/301\n"
    "PASS against journal_manuscript_v14.tex + companion_categorical_v9.tex;")

open(p, "w").write(s)

# 6. Verify no current-package v13 rows remain (historical notes keep theirs)
import re
rows = re.findall(r"\| [^|\n]*\| \[(?:scripts|download)/journal_manuscript_v13", s)
assert not rows, f"stale v13 current-rows: {rows}"
print("SUBMISSION_PACKAGE_LINKS.md updated to the v14/v9 + v17 round;",
      len(s), "bytes")
