#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the v9/v7 + v12-package round."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
s = s.replace(
    "Generated 2026-09-17 (merged-synthesis revision + v11 package\n"
    "round: journal_manuscript_v8 + companion_categorical_v7).",
    "Generated 2026-09-17 (post-synthesis flow polish + v12 package\n"
    "round: journal_manuscript_v9 + companion_categorical_v7).")

# 2. New revision note inserted before the merged-synthesis note
old_anchor = ("Revision note (2026-09-17, merged-synthesis revision + v11 package\n"
              "round):")
new_note = """Revision note (2026-09-17, post-synthesis flow polish + v12 package
round): new main version as a separate file, prior versions untouched
-- scripts/journal_manuscript_v9.tex (from v8); companion_categorical_v7.tex
stands unchanged. The round closed the five post-synthesis directives:
(1) flow -- the abstract's subject repetition smoothed ("The association
does not propagate" -> "It does not propagate"; 249 words, within the
150-250 guideline) and the Reproducibility sentence recast as "An
automated suite of 301 numeric checks re-derives every manuscript
number..."; (2) remnant/redundancy -- the 16-pattern forbidden-list
sweep clean on both papers, rendered-PDF scans clean (duplicate
sentences, placeholders, punctuation artifacts: all extraction
false-positives, verified in context); (3) error check -- the
humanizing-turn diffs re-audited line by line, every grafted number
re-verified against the body and artifacts; (4) content-loss scan
against the pre-humanized baselines (v6 main / v5 companion) -- no
substantive loss found: every item removed from the abstracts is fully
reported in the introduction/body (rho = 0.99998, five selection rules,
Glivenko-Cantelli rate, boundary-reset true-order, codimension-one
strata, thirteen sweeps, all Limitations items), and the standing
rejections from the humanized-file evaluation remain correct; (5) the
cover letters finalized: dates filled (September 17, 2026) and the TAC
board-member choice made -- Prof. Christina Vasilakopoulou (NTUA),
Transmitting Editor, cc tac@mta.ca, per TAC's author information
(submit to any Editorial Board member except the Managing Editor or
TeXnical editors). All numerical claims unchanged:
audit_v17_numbers.py 301/301 PASS; builds: main 29 pp, companion
74 pp, zero errors / zero undefined references; ZIPs rebuilt via
build_submission_zips_v12.sh with fresh-dir standalone tectonic
compiles verified (29/74 pp).

"""
assert old_anchor in s
s = s.replace(old_anchor, new_note + old_anchor, 1)

# 3. Main-paper rows v8 -> v9
s = s.replace(
    "| Manuscript PDF (29 pp, full proofs in appendices, declarations in backmatter; merged-synthesis revision: compressed abstract robustness clause, glossed value function and coupling, reconciled check count; prior versions retained as separate files) | [download/journal_manuscript_v8.pdf]",
    "| Manuscript PDF (29 pp, full proofs in appendices, declarations in backmatter; post-synthesis flow polish on the merged-synthesis revision: smoothed abstract transition, 249-word abstract, suite-of-checks Reproducibility sentence; prior versions retained as separate files) | [download/journal_manuscript_v9.pdf]")
s = s.replace(
    "| LaTeX source | [scripts/journal_manuscript_v8.tex]",
    "| LaTeX source | [scripts/journal_manuscript_v9.tex]")
s = s.replace(
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v8_bmb_refs.tex]",
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v9_bmb_refs.tex]")
s = s.replace(
    "| BibTeX database | [scripts/journal_manuscript_v8_refs.bib]",
    "| BibTeX database | [scripts/journal_manuscript_v9_refs.bib]")
s = s.replace(
    "files, upload them together with `journal_manuscript_v8_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v9_bmb_refs.tex` and")
# blob/raw URL tails for the swapped rows
for a, b in [("journal_manuscript_v8.pdf", "journal_manuscript_v9.pdf"),
             ("journal_manuscript_v8.tex", "journal_manuscript_v9.tex"),
             ("journal_manuscript_v8_bmb_refs.tex",
              "journal_manuscript_v9_bmb_refs.tex"),
             ("journal_manuscript_v8_refs.bib",
              "journal_manuscript_v9_refs.bib")]:
    s = s.replace(f"blob/main/download/{a})", f"blob/main/download/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{b})")
    s = s.replace(f"blob/main/scripts/{a})", f"blob/main/scripts/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{b})")

# 4. Checklist: audit retarget + resolved abstract count + remaining items
s = s.replace(
    "audit_v16 301/301\nPASS against journal_manuscript_v8.tex + companion_categorical_v7.tex;",
    "audit_v17 301/301\nPASS against journal_manuscript_v9.tex + companion_categorical_v7.tex;")
s = s.replace(
    "six keywords, 240-word abstract within the 150-250 guideline,",
    "six keywords, 249-word abstract within the 150-250 guideline,")
s = s.replace(
    "Remaining at submission time: fill the cover-letter `[Submission date]`\n"
    "placeholders; select the receiving Editorial Board member for TAC (from\n"
    "geninfo.html); register/log in at the BMB Editorial Manager portal.",
    "Remaining at submission time: register/log in at the BMB Editorial\n"
    "Manager portal. Resolved this round: the cover-letter dates are filled\n"
    "(September 17, 2026, both letters) and the TAC receiving board member\n"
    "is selected -- Prof. Christina Vasilakopoulou (NTUA), Transmitting\n"
    "Editor, with the submission emailed to her and copied to tac@mta.ca\n"
    "per TAC's author information (any Editorial Board member except the\n"
    "Managing Editor or TeXnical editors).")

open(p, "w").write(s)
import re
left = re.findall(r"journal_manuscript_v8", s)
print("leftover v8 mentions (historical notes expected):", len(left))
