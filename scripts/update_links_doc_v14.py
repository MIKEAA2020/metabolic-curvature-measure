#!/usr/bin/env python3
"""Retarget SUBMISSION_PACKAGE_LINKS.md to the v11/v9 + v14-package round."""

p = "/home/z/my-project/metabolic-curvature-measure/download/SUBMISSION_PACKAGE_LINKS.md"
s = open(p).read()

# 1. Header generation line
s = s.replace(
    "Generated 2026-09-17 (post-synthesis flow polish + v12 package\n"
    "round: journal_manuscript_v9 + companion_categorical_v7).",
    "Generated 2026-09-17 (universal Gemini-register revision + v14 package\n"
    "round: journal_manuscript_v11 + companion_categorical_v9).")

# 2. New revision note inserted before the flow-polish note
old_anchor = ("Revision note (2026-09-17, post-synthesis flow polish + v12 package\n"
              "round):")
new_note = """Revision note (2026-09-17, universal Gemini-register revision + v14
package round): both papers carry the evaluated Gemini register
universally across their narrative prose, as new versioned files
(prior versions untouched) -- scripts/journal_manuscript_v11.tex
(from v10) and scripts/companion_categorical_v9.tex (from v8), plus
their refs files. The email (mailto:) and ORCID
(https://orcid.org/0000-0002-0019-1842) are now CLICKABLE in both
papers (main: author footnote; companion: title block; verified as
URI annotations in both built PDFs). MAIN v11: register-level
revision of the narrative prose -- intro lead, section leads and
interstitial prose of Sections 2-4, the computational-validation and
empirical result narratives (M1 sweeps, epistasis, regime dial, value
carrier, primary association with the partial-correlation motivation,
panel construction, platform 2x2, protein abundance/change and the
protein-layer null with the buffering close), discussion, methods
connectives, and the positioning paragraph recast in Gemini's
short-sentence form; every number, proof, citation, and the
compressed smooth-calculus statement unchanged. COMPANION v9:
abstract connective polish (word count kept under the 265 cap),
Preliminaries / SAVGS / Empirical-Verdicts section leads, the
four-point Conclusion opener, and the clickable author block; the
bibliography pointer retargeted to companion_refs_v9.bib. Verified:
number-integrity multiset diff (zero missing/added numeric tokens
beyond the ORCID link digits); pattern_sweep_v16 16/16 clean on
both; audit_v19_numbers.py 301/301 PASS; tectonic main 30 pp /
companion 75 pp, 0 errors / 0 undefined references; ZIPs rebuilt via
build_submission_zips_v14.sh with fresh-dir standalone compiles
re-verified (30/75 pp); cover letters retargeted to v11/v9.

Revision note (2026-09-17, Gemini-alignment revision + v13 package
round): both papers revised toward the accessible register of the
evaluated Gemini humanization attempts, as new versioned files (prior
versions untouched) -- scripts/journal_manuscript_v10.tex (from v9)
and scripts/companion_categorical_v8.tex (from v7), plus their refs
files. MAIN v10: an accessible-motivation lead paragraph opens the
Introduction (the rerouting question, why smooth calculus cannot
answer it, geometric measure theory as the natural language); a
self-contained parametric-FBA setup with the LP display and the
chamber-complex reading opens Section 2; wall-crossing and
integrated-boundary-impedance glosses in the categorical subsection;
the partial-correlation motivation (baseline-expression confound) at
the primary association; the protein-layer central question and a
buffering close at the abundance/change dissociation; discussion
sentences for the resolution-window breakdown and the
objective-invisibility of most rerouting; Limitations restructured as
a labeled list with every item kept. COMPANION v8: a narrative
harm-in-sequence abstract opening (264 words, under the 265 cap; the
six-axis sentence intact); the concrete closed-cycle example
(temperature/nutrients) in the Introduction; the intuitive gloss at
the viability-weighted-curvature definition; an in-words gloss at the
optic-category definition; the stabilization question at the head of
the Lipschitz section; the application-bridge numbers (r = +0.395,
n = 424; r = -0.083, n = 366) in the Introduction; a compact
Conclusion section before Future directions. The Gemini attempts'
defects remain rejected (fabricated "Zai, A." author, changelog
remnants, ASCII art, adverbial register, proof-argument swaps, and the
companion attempt's content loss). All numerical claims unchanged:
audit_v18_numbers.py 301/301 PASS; builds: main 29 pp, companion
75 pp, zero errors / zero undefined references; ZIPs rebuilt via
build_submission_zips_v13.sh with fresh-dir standalone tectonic
compiles verified (29/75 pp); cover letters retargeted to the new
filenames.

"""
assert old_anchor in s
s = s.replace(old_anchor, new_note + old_anchor, 1)

# 3. Main-paper rows v9 -> v10
s = s.replace(
    "| Manuscript PDF (29 pp, full proofs in appendices, declarations in backmatter; post-synthesis flow polish on the merged-synthesis revision: smoothed abstract transition, 249-word abstract, suite-of-checks Reproducibility sentence; prior versions retained as separate files) | [download/journal_manuscript_v9.pdf]",
    "| Manuscript PDF (30 pp, full proofs in appendices, declarations in backmatter; universal Gemini-register revision of narrative prose throughout, clickable email and ORCID; prior versions retained as separate files) | [download/journal_manuscript_v11.pdf]")
s = s.replace(
    "| LaTeX source | [scripts/journal_manuscript_v9.tex]",
    "| LaTeX source | [scripts/journal_manuscript_v11.tex]")
s = s.replace(
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v9_bmb_refs.tex]",
    "| Reference list (BMB alphabetical, 27 entries) | [scripts/journal_manuscript_v11_bmb_refs.tex]")
s = s.replace(
    "| BibTeX database | [scripts/journal_manuscript_v9_refs.bib]",
    "| BibTeX database | [scripts/journal_manuscript_v11_refs.bib]")
s = s.replace(
    "files, upload them together with `journal_manuscript_v9_bmb_refs.tex` and",
    "files, upload them together with `journal_manuscript_v11_bmb_refs.tex` and")
# blob/raw URL tails for the swapped rows
for a, b in [("journal_manuscript_v9.pdf", "journal_manuscript_v10.pdf"),
             ("journal_manuscript_v9.tex", "journal_manuscript_v10.tex"),
             ("journal_manuscript_v9_bmb_refs.tex",
              "journal_manuscript_v10_bmb_refs.tex"),
             ("journal_manuscript_v9_refs.bib",
              "journal_manuscript_v10_refs.bib")]:
    s = s.replace(f"blob/main/download/{a})", f"blob/main/download/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{b})")
    s = s.replace(f"blob/main/scripts/{a})", f"blob/main/scripts/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{b})")

# 4. Companion rows v7 -> v8
s = s.replace(
    "| Manuscript PDF (74 pp; merged-synthesis revision: boundary-rule breakdown, autopoiesis contrast, Zeno physical reading; prior versions retained as separate files) | [download/companion_categorical_v7.pdf]",
    "| Manuscript PDF (75 pp; Gemini-alignment revision: narrative abstract opening, closed-cycle example, intuitive glosses, stabilization question, Conclusion section; prior versions retained as separate files) | [download/companion_categorical_v8.pdf]")
s = s.replace(
    "| LaTeX source | [scripts/companion_categorical_v7.tex]",
    "| LaTeX source | [scripts/companion_categorical_v8.tex]")
s = s.replace(
    "| BibTeX database | [scripts/companion_refs_v7.bib]",
    "| BibTeX database | [scripts/companion_refs_v8.bib]")
for a, b in [("companion_categorical_v7.pdf", "companion_categorical_v8.pdf"),
             ("companion_categorical_v7.tex", "companion_categorical_v8.tex"),
             ("companion_refs_v7.bib", "companion_refs_v8.bib")]:
    s = s.replace(f"blob/main/download/{a})", f"blob/main/download/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/download/{b})")
    s = s.replace(f"blob/main/scripts/{a})", f"blob/main/scripts/{b})")
    s = s.replace(f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{a})",
                  f"raw.githubusercontent.com/MIKEAA2020/metabolic-curvature-measure/main/scripts/{b})")

# 5. Checklist: audit retarget
s = s.replace(
    "audit_v17 301/301\nPASS against journal_manuscript_v9.tex + companion_categorical_v7.tex;",
    "audit_v18 301/301\nPASS against journal_manuscript_v10.tex + companion_categorical_v8.tex;")

open(p, "w").write(s)
import re
left_v9 = re.findall(r"journal_manuscript_v9", s)
left_v7 = re.findall(r"companion_categorical_v7", s)
print("leftover v9 mentions (historical notes expected):", len(left_v9))
print("leftover v7 mentions (historical notes expected):", len(left_v7))
print("new v10 mentions:", len(re.findall(r"journal_manuscript_v10", s)))
print("new v8 mentions:", len(re.findall(r"companion_categorical_v8", s)))
