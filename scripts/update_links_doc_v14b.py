#!/usr/bin/env python3
"""Finish the v14 retarget of SUBMISSION_PACKAGE_LINKS.md:
header generation line, current-package rows (main v10->v11,
companion v8->v9), page counts, and the audit-line/revision-note
references that describe the CURRENT package (historical revision
notes are preserved untouched)."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line (exact current state)
old = """Generated 2026-09-17 (Gemini-alignment revision + v13 package
round: journal_manuscript_v10 + companion_categorical_v8). All repository links follow"""
new = """Generated 2026-09-17 (universal Gemini-register revision + v14 package
round: journal_manuscript_v11 + companion_categorical_v9). All repository links follow"""
assert old in s, "header anchor"
s = s.replace(old, new, 1)

# 2. Main current-package rows (section around line 628)
old_row = "| Manuscript PDF (29 pp, full proofs in appendices, declarations in backmatter; Gemini-alignment revision: accessible intro lead, self-contained LP setup, wall-crossing/boundary-impedance glosses, protein-layer central question, labeled Limitations; prior versions retained as separate files) | [download/journal_manuscript_v10.pdf]"
new_row = "| Manuscript PDF (30 pp, full proofs in appendices, declarations in backmatter; universal Gemini-register revision of narrative prose throughout, clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v11.pdf]"
assert old_row in s, "main PDF row"
s = s.replace(old_row, new_row, 1)
s = s.replace("| LaTeX source | [scripts/journal_manuscript_v10.tex]",
             "| LaTeX source | [scripts/journal_manuscript_v11.tex]", 1)
s = s.replace("| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v10_bmb_refs.tex]",
             "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v11_bmb_refs.tex]", 1)
s = s.replace("| BibTeX database | [scripts/journal_manuscript_v10_refs.bib]",
              "| BibTeX database | [scripts/journal_manuscript_v11_refs.bib]", 1)

# 3. Main package prose: upload instructions + audit row for the
#    current package
s = s.replace("files, upload them together with `journal_manuscript_v10_bmb_refs.tex` and",
              "files, upload them together with `journal_manuscript_v11_bmb_refs.tex` and", 1)
s = s.replace("journal_manuscript_v10.tex` and",
              "journal_manuscript_v11.tex` and", 1)

# 4. Companion current-package rows
old_c = "| Manuscript PDF (75 pp; Gemini-alignment revision: narrative abstract opening, closed-cycle example, intuitive glosses, stabilization question, Conclusion section; prior versions retained as separate files) | [download/companion_categorical_v8.pdf]"
new_c = "| Manuscript PDF (75 pp; universal Gemini-register revision of narrative leads and conclusion, clickable email and ORCID; prior versions retained as separate files) | [download/companion_categorical_v9.pdf]"
assert old_c in s, "companion PDF row"
s = s.replace(old_c, new_c, 1)
s = s.replace("| LaTeX source | [scripts/companion_categorical_v8.tex]",
              "| LaTeX source | [scripts/companion_categorical_v9.tex]", 1)
s = s.replace("| BibTeX database | [scripts/companion_refs_v8.bib]",
              "| BibTeX database | [scripts/companion_refs_v9.bib]", 1)

open(p, "w").write(s)

# report remaining current-package references (excluding historical notes)
import re
body_after_first_note = s[s.find("Revision note (2026-09-17, Gemini-alignment"):]
rows = s[s.find("## " + chr(42) + "Main"):] if False else s
print("done; remaining v10/v8 refs in doc:",
      len(re.findall(r"journal_manuscript_v10", s)),
      len(re.findall(r"companion_categorical_v8", s)))
print("(historical revision notes are expected to retain these)")
